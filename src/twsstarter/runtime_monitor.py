"""
Background runtime monitor for TWS / Gateway instances.

Checks once immediately on start, then every `interval` seconds — running in a
dedicated daemon thread so the GUI is never blocked.  State changes are reported
to the main thread via a Qt signal (thread-safe); the monitor never touches Qt
widgets itself.

It reports a *real* three-state status per connection:
  * "running"  — really up: a logged-in TWS main window matches, OR an IB Gateway
                 is listening on this connection's API port (jts.ini) and the
                 gateway's active account directory matches the learned one.
  * "starting" — launched from this app and still waiting (login dialog open /
                 launcher alive / short grace period). NOT counted as running.
  * "stopped"  — neither of the above.

TWS is detected by window title ("<account> Interactive Brokers …"). Gateway has
no account in its title (the running window shares the login dialog's title), so
it is detected via its TCP port and attributed to a connection via the per-account
settings directory under the gateway path (see process_scan).

Master-account check (TWS only): after autofill submits a login, the monitor
watches the main windows of that login's process. If none of them shows the
connection's master account (the connection name) within a grace period, the
wrong account was logged in and the process is terminated.

This is *status monitoring only* — it never restarts processes.
"""
from __future__ import annotations

import sys
import threading
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

from twsstarter.process_scan import (
    scan_running,
    gateway_listening,
    active_gateway_dir,
    is_account_id,
    terminate_pid,
)

if TYPE_CHECKING:
    from twsstarter.launcher import ProcessHandle

_WIN32 = sys.platform == "win32"

# How long to keep trying to learn an account id / gateway dir after a launch.
_LEARN_TIMEOUT = 150.0
# Minimum time a freshly launched connection is shown as "starting", to bridge
# the brief window before the login dialog appears / launcher settles.
_START_GRACE = 25.0
# How long after the login was submitted to wait for the TWS main window
# (covers slow logins incl. two-factor confirmation).
_VERIFY_TIMEOUT = 300.0
# How long a logged-in TWS may show only foreign accounts before it is closed
# (FA logins open several account windows; the master may appear a bit later).
_VERIFY_GRACE = 15.0


@dataclass
class ConnSnapshot:
    id: str
    name: str
    username: str
    account_id: str       # learned TWS account ('' if none)
    gateway_path: str     # effective gateway path ('' if none)
    gateway_dir: str      # learned gateway account directory ('' if none)


class RuntimeMonitor(QObject):
    """Watches TWS/Gateway runtime in a background thread."""

    # entry.id, state ("running" | "starting" | "stopped"), run_type ("tws"|"gateway"|"")
    status_changed = pyqtSignal(str, str, str)
    # entry.id, learned TWS account id
    account_learned = pyqtSignal(str, str)
    # entry.id, learned gateway account directory
    gateway_dir_learned = pyqtSignal(str, str)
    # entry.id, result ("ok" | "mismatch" | "unverified"), accounts found
    master_checked = pyqtSignal(str, str, str)

    def __init__(self, interval: float = 10.0, parent: QObject | None = None):
        super().__init__(parent)
        self._interval = interval
        self._lock = threading.Lock()
        self._handles: dict[str, "ProcessHandle"] = {}
        self._conns: list[ConnSnapshot] = []
        self._states: dict[str, str] = {}   # entry_id → "running" | "starting"
        # entry_id → (tws accounts before launch, learn_deadline, grace_until)
        self._pending: dict[str, tuple[set[str], float, float]] = {}
        # entry_id → [login pid, deadline, first time only foreign accounts seen]
        self._verify: dict[str, list] = {}
        self._wakeup = threading.Event()
        self._stopping = False
        self._thread: threading.Thread | None = None

    # ── Public API (main thread) ───────────────────────────────────

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stopping = False
        self._wakeup.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="RuntimeMonitor"
        )
        self._thread.start()

    def stop(self) -> None:
        self._stopping = True
        self._wakeup.set()

    def set_connections(self, snapshot: list[ConnSnapshot]) -> None:
        with self._lock:
            self._conns = list(snapshot)
        self._wakeup.set()

    def add_handle(self, entry_id: str, handle: "ProcessHandle") -> None:
        """Register a session-launched process and re-check immediately."""
        with self._lock:
            self._handles[entry_id] = handle
        self._wakeup.set()

    def remove_handle(self, entry_id: str) -> None:
        with self._lock:
            self._handles.pop(entry_id, None)
            self._pending.pop(entry_id, None)
            self._verify.pop(entry_id, None)
        self._wakeup.set()

    def start_learning(self, entry_id: str) -> None:
        """Begin learning + a 'starting' phase for a launch.

        Snapshots the TWS accounts currently running; the first *new* account
        that appears is attributed to this connection (robust against TWS
        re-spawning itself with a different PID). For a Gateway launch the
        attribution happens in _check_once via the active account directory.
        """
        before = {
            inst.account
            for inst in scan_running()
            if inst.kind == "tws" and inst.account
        }
        now = time.monotonic()
        with self._lock:
            self._pending[entry_id] = (before, now + _LEARN_TIMEOUT, now + _START_GRACE)
        self._wakeup.set()

    def expect_master(self, entry_id: str, pid: int) -> None:
        """Verify the master account of the TWS process that owns the submitted
        login window (called from the autofill thread)."""
        with self._lock:
            self._verify[entry_id] = [pid, time.monotonic() + _VERIFY_TIMEOUT, None]
        self._wakeup.set()

    def is_running(self, entry_id: str) -> bool:
        with self._lock:
            return self._states.get(entry_id) == "running"

    def is_active(self, entry_id: str) -> bool:
        """Running OR starting."""
        with self._lock:
            return entry_id in self._states

    def request_check(self) -> None:
        self._wakeup.set()

    # ── Worker thread ──────────────────────────────────────────────

    def _run(self) -> None:
        # Immediate check on start, then every `interval` seconds.
        while not self._stopping:
            self._check_once()
            with self._lock:
                # A suspected wrong login is re-checked quickly so it is closed
                # right after the grace period, not one full interval later.
                suspect = any(v[2] is not None for v in self._verify.values())
            self._wakeup.wait(min(self._interval, 2.0) if suspect else self._interval)
            self._wakeup.clear()

    def _check_once(self) -> None:
        with self._lock:
            conns = list(self._conns)
            handles = dict(self._handles)
            pending = dict(self._pending)

        instances = scan_running()
        tws_accounts = {
            inst.account for inst in instances
            if inst.kind == "tws" and inst.account
        }
        login_open = any(inst.kind == "login" for inst in instances)
        now_mono = time.monotonic()

        # Is a logged-in Gateway serving its API? (one netstat scan per cycle).
        gw_alive = any(snap.gateway_path for snap in conns) and gateway_listening()
        # Active account directory per distinct gateway path.
        gw_active: dict[str, str | None] = {}
        if gw_alive:
            for snap in conns:
                p = snap.gateway_path
                if p and p not in gw_active:
                    gw_active[p] = active_gateway_dir(p)

        # ── TWS account-id learning by difference ──────────────────────
        # Learn an account for a connection only ONCE — only for a connection
        # that does not already have one. This is essential for Financial Advisor
        # (FA) logins, where one TWS opens the master plus many sub-account
        # windows: without the "learn once" guard a connection would flip-flop
        # between those accounts every cycle, and each learn re-triggers a check
        # (learn → push → re-check → learn …), spamming the journal.
        # Never attribute the same account to two connections either.
        # A connection whose name is a master account needs no learning — the
        # master account itself identifies its TWS.
        acct_by_id = {s.id: s.account_id for s in conns}
        has_master = {s.id for s in conns if is_account_id(s.name)}
        learned: list[tuple[str, str]] = []
        claimed_accounts: set[str] = {a for a in acct_by_id.values() if a}
        with self._lock:
            for entry_id, (before, deadline, _grace) in list(self._pending.items()):
                if entry_id not in has_master and not acct_by_id.get(entry_id):
                    fresh = (tws_accounts - before) - claimed_accounts
                    if fresh:
                        acc = sorted(fresh)[0]
                        learned.append((entry_id, acc))
                        claimed_accounts.add(acc)
                if now_mono > deadline:
                    del self._pending[entry_id]

        # ── Master-account verification ────────────────────────────────
        checked, killed = self._verify_masters(conns, instances, now_mono)
        if killed:
            # The terminated TWS must not be reported as running this cycle.
            instances = [i for i in instances if i.pid not in killed]

        # ── Three-state detection ──────────────────────────────────────
        states: dict[str, str] = {}
        types: dict[str, str] = {}       # entry_id → "tws" | "gateway"
        gw_learned: list[tuple[str, str]] = []
        drop_pending: list[str] = []

        claimed_pids: set[int] = set()
        for snap in conns:
            # 1) TWS main window. Each running instance is attributed to at most
            #    one connection (claimed by PID), so a single TWS is never
            #    counted twice — even if two connections share an account id.
            inst = self._match_real(
                snap.name, snap.username, snap.account_id, instances, claimed_pids
            )
            if inst is not None:
                claimed_pids.add(inst.pid)
                states[snap.id] = "running"
                types[snap.id] = "tws"
                continue
            # 2) Gateway via listening API socket + account directory
            p = snap.gateway_path
            if p and gw_alive:
                active = gw_active.get(p)
                if snap.gateway_dir and active and snap.gateway_dir == active:
                    states[snap.id] = "running"
                    types[snap.id] = "gateway"
                    continue
                if snap.id in pending and not snap.gateway_dir and active:
                    # First Gateway launch for this connection → learn its dir.
                    gw_learned.append((snap.id, active))
                    states[snap.id] = "running"
                    types[snap.id] = "gateway"
                    continue
            # 2b) No window/port scan outside Windows: a session-launched process
            #     that is still alive counts as running. Without this the
            #     connection would drop to "stopped" after the starting phase
            #     and the autostart watchdog would launch it again and again.
            handle = handles.get(snap.id)
            if not _WIN32 and handle is not None and handle.is_running():
                states[snap.id] = "running"
                types[snap.id] = "gateway" if handle.is_gateway else "tws"
                continue
            # 3) Starting phase
            if snap.id in pending:
                _before, _deadline, grace_until = pending[snap.id]
                handle = handles.get(snap.id)
                alive = handle is not None and handle.is_running()
                if now_mono < grace_until or alive or login_open:
                    states[snap.id] = "starting"
                else:
                    drop_pending.append(snap.id)

        if drop_pending:
            with self._lock:
                for entry_id in drop_pending:
                    self._pending.pop(entry_id, None)

        with self._lock:
            prev = self._states
            self._states = states
            changes = [
                (eid, st) for eid, st in states.items() if prev.get(eid) != st
            ]
            stopped = [eid for eid in prev if eid not in states]

        if self._stopping:
            return
        for entry_id, result, accounts in checked:
            self.master_checked.emit(entry_id, result, accounts)
        for entry_id, account in learned:
            self.account_learned.emit(entry_id, account)
        for entry_id, gdir in gw_learned:
            self.gateway_dir_learned.emit(entry_id, gdir)
        for entry_id, state in changes:
            self.status_changed.emit(entry_id, state, types.get(entry_id, ""))
        for entry_id in stopped:
            self.status_changed.emit(entry_id, "stopped", "")

    def _verify_masters(self, conns, instances, now_mono):
        """Check pending master-account verifications against the window scan.

        Returns (results, killed_pids); results are (entry_id, "ok" | "mismatch"
        | "unverified", accounts seen). A mismatching TWS process is terminated.
        """
        masters = {s.id: s.name.strip() for s in conns}
        results: list[tuple[str, str, str]] = []
        killed: set[int] = set()
        with self._lock:
            for entry_id, item in list(self._verify.items()):
                pid, deadline, foreign_since = item
                master = masters.get(entry_id, "")
                if not is_account_id(master):
                    # Legacy free-text name: nothing to verify against.
                    del self._verify[entry_id]
                    continue
                accounts = sorted({
                    i.account for i in instances
                    if i.kind == "tws" and i.pid == pid and i.account
                })
                if any(a.lower() == master.lower() for a in accounts):
                    results.append((entry_id, "ok", ", ".join(accounts)))
                    del self._verify[entry_id]
                elif accounts:
                    if foreign_since is None:
                        item[2] = now_mono
                    elif now_mono - foreign_since >= _VERIFY_GRACE:
                        terminate_pid(pid)
                        killed.add(pid)
                        results.append((entry_id, "mismatch", ", ".join(accounts)))
                        del self._verify[entry_id]
                elif now_mono > deadline:
                    # Main window never appeared in the login's process (login
                    # aborted, or TWS re-spawned under another PID).
                    results.append((entry_id, "unverified", ""))
                    del self._verify[entry_id]
        return results, killed

    @staticmethod
    def _match_real(name, username, account_id, instances, claimed_pids):
        """Return an unclaimed logged-in TWS main window for a connection, or None.

        Only real main windows count (kind != 'login'). The account id is the
        first token of the TWS title; account_id and name (master account) must
        equal it exactly, so "U123" never matches "U1234" and common title words
        ("Interactive", "Brokers", …) never match; username is matched as a substring. Instances
        whose PID is already claimed by another connection are skipped, so one
        running TWS maps to a single connection.
        """
        mains = [
            i for i in instances
            if i.kind in ("tws", "gateway") and i.pid not in claimed_pids
        ]
        for needle in (account_id, name):
            if not needle:
                continue
            for inst in mains:
                if inst.account and inst.account.lower() == needle.lower():
                    return inst
        if username:
            for inst in mains:
                if username.lower() in inst.title.lower():
                    return inst
        return None
