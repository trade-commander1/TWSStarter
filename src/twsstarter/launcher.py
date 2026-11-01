"""Launch TWS / IB Gateway from a connection's configured path, then hand the
decrypted credentials to the autofill thread. Returns a ProcessHandle whose only
job is to represent the spawned launcher process (runtime state is tracked
separately by runtime_monitor via a system-wide window/port scan)."""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
from typing import Callable, Optional
from twsstarter import autofill, crypto
from twsstarter.models import AppSettings, ConnectionEntry


_WIN32 = sys.platform == "win32"

# Launcher names per platform (the Linux installers create shell launchers
# 'tws' / 'ibgateway' without extension).
if _WIN32:
    _TWS_EXES = ["tws.exe", "Jts.exe", "jts.exe", "launch.bat"]
    _GW_EXES  = ["ibgateway.exe", "gateway.exe", "launch.bat"]
else:
    _TWS_EXES = ["tws"]
    _GW_EXES  = ["ibgateway"]


class ProcessHandle:
    def __init__(self, proc: subprocess.Popen, is_gateway: bool = False):
        self._proc = proc
        self.is_gateway = is_gateway

    @property
    def pid(self) -> int:
        return self._proc.pid

    def is_running(self) -> bool:
        return self._proc.poll() is None

    def terminate(self) -> None:
        if self.is_running():
            try:
                self._proc.terminate()
            except OSError:
                pass


def launch_tws(
    entry: ConnectionEntry,
    settings: AppSettings,
    on_autofill_done: Optional[Callable[[bool, str], None]] = None,
    on_login_submitted: Optional[Callable[[int], None]] = None,
) -> ProcessHandle:
    """Start TWS; `on_login_submitted(pid)` reports the PID of the filled login
    window so the caller can verify the master account after login."""
    path = (entry.tws_path or settings.default_tws_path or "").strip()
    if not path:
        raise ValueError("No TWS path configured. Set it in Settings or on the connection entry.")
    handle = _launch_direct(path, _TWS_EXES, is_gateway=False)
    password = crypto.decrypt(entry.password_enc)
    autofill.start_thread(
        entry.username, password, entry.paper_trading,
        is_gateway=False, on_done=on_autofill_done, pid=handle.pid,
        on_submitted=on_login_submitted,
    )
    return handle


def launch_gateway(
    entry: ConnectionEntry,
    settings: AppSettings,
    on_autofill_done: Optional[Callable[[bool, str], None]] = None,
) -> ProcessHandle:
    path = (entry.gateway_path or settings.default_gateway_path or "").strip()
    if not path:
        raise ValueError("No Gateway path configured. Set it in Settings or on the connection entry.")
    handle = _launch_direct(path, _GW_EXES, is_gateway=True)
    password = crypto.decrypt(entry.password_enc)
    autofill.start_thread(
        entry.username, password, entry.paper_trading,
        is_gateway=True, on_done=on_autofill_done, pid=handle.pid,
    )
    return handle


def _launch_direct(app_path: str, candidates: list[str], is_gateway: bool) -> ProcessHandle:
    if not _WIN32:
        # Repair paths stored with Windows separators by older versions
        # ('\home\user\Jts' would otherwise be a single relative name).
        app_path = app_path.replace("\\", "/")
    path = Path(app_path).expanduser()
    if _WIN32:
        extra = {"creationflags": subprocess.CREATE_NEW_CONSOLE}
    else:
        # Own session: TWS is not tied to the terminal/process group of TWSStarter.
        # Its console chatter is dropped; TWS writes its own launcher.log.
        extra = {"start_new_session": True,
                 "stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    for name in candidates:
        exe = path / name
        if exe.exists():
            proc = subprocess.Popen(
                [str(exe)],
                cwd=str(path),
                **extra,
            )
            return ProcessHandle(proc, is_gateway)
    raise FileNotFoundError(
        f"No executable found in '{app_path}'.\n"
        f"Searched: {', '.join(candidates)}"
    )
