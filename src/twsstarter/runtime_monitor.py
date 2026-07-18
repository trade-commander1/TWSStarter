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

This is *status monitoring only* — it never restarts processes.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

from twsstarter.process_scan import (
    scan_running,
    gateway_listening,
    active_gateway_dir,
)

if TYPE_CHECKING:
    from twsstarter.launcher import ProcessHandle

# How long to keep trying to learn an account id / gateway dir after a launch.
_LEARN_TIMEOUT = 150.0
# Minimum time a freshly launched connection is shown as "starting", to bridge
# the brief window before the login dialog appears / launcher settles.
_START_GRACE = 25.0


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

    def __init__(self, interval: float = 10.0, parent: QObject | None = None):
        super().__init__(parent)
        self._interval = interval
        self._lock = threading.Lock()
        self._handles: dict[str, "ProcessHandle"] = {}
        self._conns: list[ConnSnapshot] = []
        self._states: dict[str, str] = {}   # entry_id → "running" | "starting"
        # entry_id → (tws accounts before launch, learn_deadline, grace_until)
        self._pending: dict[str, tuple[set[str], float, float]] = {}
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
            self._wakeup.wait(self._interval)
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
        # Never attribute the same account to two connections: accounts already
        # assigned to a connection, or just claimed by another pending one, are
        # excluded from the fresh pool.
        learned: list[tuple[str, str]] = []
        claimed_accounts: set[str] = {s.account_id for s in conns if s.account_id}
        with self._lock:
            for entry_id, (before, deadline, _grace) in list(self._pending.items()):
                fresh = (tws_accounts - before) - claimed_accounts
                if fresh:
                    acc = sorted(fresh)[0]
                    learned.append((entry_id, acc))
                    claimed_accounts.add(acc)
                elif now_mono > deadline:
                    del self._pending[entry_id]

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
        for entry_id, account in learned:
            self.account_learned.emit(entry_id, account)
        for entry_id, gdir in gw_learned:
            self.gateway_dir_learned.emit(entry_id, gdir)
        for entry_id, state in changes:
            self.status_changed.emit(entry_id, state, types.get(entry_id, ""))
        for entry_id in stopped:
            self.status_changed.emit(entry_id, "stopped", "")

    @staticmethod
    def _match_real(name, username, account_id, instances, claimed_pids):
        """Return an unclaimed logged-in TWS main window for a connection, or None.

        Only real main windows count (kind != 'login'). The account id is the
        first token of the TWS title, so account_id and name are matched with
        startswith to avoid false positives on common words ("Interactive",
        "Brokers", "Trading", …); username is matched as a substring. Instances
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
                if inst.title.lower().startswith(needle.lower()):
                    return inst
        if username:
            for inst in mains:
                if username.lower() in inst.title.lower():
                    return inst
        return None
