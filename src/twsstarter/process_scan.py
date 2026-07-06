"""System-wide detection of running TWS / IB Gateway instances (Windows).

Why scan instead of relying on the launcher's subprocess handle:
  * Instances started in a previous TWSStarter session have no handle, so they
    would never show up.
  * The status must reflect reality even for externally started instances.

A logged-in TWS main window has a title such as:
    "DUH077320 Interactive Brokers (Simulated Trading)"   (paper)
    "U1234567 Interactive Brokers"                         (live)
i.e.  "<account> Interactive Brokers [ (Simulated Trading) ]".

IB Gateway main windows are titled "IBKR Gateway" / "IB Gateway" (these are also
the login-dialog titles, so a gateway in login vs. running state cannot always
be distinguished by title alone).

Mapping a running instance to a stored connection uses the account string in
the window title: if the connection's username appears in the title (case-
insensitive) it is treated as a match. For paper accounts the login username
equals the account id shown in the title, so this is reliable. For live
accounts whose login username differs from the displayed account id, the
mapping can fail — the instance is still detected, but cannot be attributed to
a specific card.
"""
from __future__ import annotations

import ctypes
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_WIN32 = sys.platform == "win32"

if _WIN32:
    import win32gui

# "<account> Interactive Brokers [ (Simulated Trading) ]"  → logged-in TWS window
_TWS_RE = re.compile(
    r"^(?P<acct>\S+)\s+Interactive Brokers(?P<sim>\s*\(Simulated Trading\))?\s*$"
)
# Login-dialog titles. These are NOT a running instance — they are the
# pre-login dialog. ("IBKR Gateway" is unfortunately also the title of the
# Gateway login dialog, so it is treated as a login dialog, not as running.)
# The TWS login title is localized ("Login" en, "Anmelden" de, ...); keep this
# list in sync with autofill._TWS_LOGIN_TITLES so a non-English login dialog is
# still recognized (otherwise the card would drop to "stopped" during login).
_LOGIN_TITLES = {"Login", "Anmelden", "IB Gateway", "IBKR Gateway"}


@dataclass
class RunningInstance:
    kind: str            # 'tws' | 'gateway' | 'login'
    title: str
    account: str | None  # account/username parsed from the title (TWS only)
    paper: bool | None   # True = simulated/paper (TWS only)
    pid: int


def _pid_of(hwnd: int) -> int:
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return int(pid.value)


def scan_running() -> list[RunningInstance]:
    """Return all currently visible TWS / Gateway main windows."""
    if not _WIN32:
        return []
    out: list[RunningInstance] = []

    def _cb(hwnd: int, _) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        m = _TWS_RE.match(title)
        if m:
            out.append(RunningInstance(
                kind="tws",
                title=title,
                account=m.group("acct"),
                paper=bool(m.group("sim")),
                pid=_pid_of(hwnd),
            ))
            return
        if title in _LOGIN_TITLES:
            out.append(RunningInstance(
                kind="login",
                title=title,
                account=None,
                paper=None,
                pid=_pid_of(hwnd),
            ))

    win32gui.EnumWindows(_cb, None)
    return out


def instance_matches(username: str, inst: RunningInstance) -> bool:
    """True if a running instance can be attributed to the given username."""
    if not username:
        return False
    return username.lower() in inst.title.lower()


def terminate_pid(pid: int) -> bool:
    """Best-effort terminate of a process by PID (Windows)."""
    if not _WIN32:
        return False
    PROCESS_TERMINATE = 0x0001
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, pid)
    if not handle:
        return False
    try:
        return bool(ctypes.windll.kernel32.TerminateProcess(handle, 0))
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


# ── Gateway detection via TCP port + jts.ini ───────────────────────────────
# The Gateway main window shares the login dialog's title, so it cannot be told
# apart by title. Instead we detect a running Gateway by the API port it listens
# on (jts.ini → LocalServerPort) and attribute it to a connection via the
# per-account settings directory IB Gateway maintains under the gateway path.

_CREATE_NO_WINDOW = 0x08000000


def process_image_name(pid: int) -> str:
    """Full image path of a process by PID, or '' (Windows)."""
    if not _WIN32 or pid <= 0:
        return ""
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    h = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        return ""
    try:
        buf = ctypes.create_unicode_buffer(1024)
        size = ctypes.c_uint(1024)
        ok = ctypes.windll.kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size))
        return buf.value if ok else ""
    finally:
        ctypes.windll.kernel32.CloseHandle(h)


def _listening_pids() -> set[int]:
    """All PIDs with at least one TCP socket in LISTENING state."""
    if not _WIN32:
        return set()
    try:
        out = subprocess.run(
            ["netstat", "-ano", "-p", "TCP"],
            capture_output=True, text=True, timeout=6,
            creationflags=_CREATE_NO_WINDOW,
        ).stdout
    except Exception:
        return set()
    pids: set[int] = set()
    # `out` can be None if netstat produced no capturable output — guard so the
    # monitor thread never crashes on `.splitlines()`.
    for line in (out or "").splitlines():
        parts = line.split()
        # e.g. ['TCP', '0.0.0.0:4002', '0.0.0.0:0', 'LISTENING', '70380']
        if len(parts) >= 5 and parts[0] == "TCP" and parts[-2].upper() == "LISTENING":
            try:
                pids.add(int(parts[-1]))
            except ValueError:
                continue
    return pids


def gateway_listening() -> bool:
    """True if an IB Gateway is logged in and serving its API.

    A running, logged-in Gateway opens its API socket (port depends on
    live/paper, e.g. 4001/4002 — NOT necessarily jts.ini's LocalServerPort).
    The pre-login dialog opens no port, so "an ibgateway.exe listens on some
    port" cleanly means "a Gateway is up", independent of the configured port.
    """
    for pid in _listening_pids():
        if "ibgateway" in process_image_name(pid).lower():
            return True
    return False


def active_gateway_dir(gateway_path: str) -> str | None:
    """The obfuscated per-account settings directory most recently written.

    IB Gateway creates one long lowercase-letter directory per account under the
    gateway path; the most recently modified one belongs to the current login.
    """
    try:
        base = Path(gateway_path)
        subs = [
            d for d in base.iterdir()
            if d.is_dir() and len(d.name) >= 30 and d.name.isalpha()
        ]
    except Exception:
        return None
    if not subs:
        return None
    return max(subs, key=lambda d: d.stat().st_mtime).name
