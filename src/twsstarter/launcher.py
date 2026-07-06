"""Launch TWS / IB Gateway from a connection's configured path, then hand the
decrypted credentials to the autofill thread. Returns a ProcessHandle whose only
job is to represent the spawned launcher process (runtime state is tracked
separately by runtime_monitor via a system-wide window/port scan)."""
from __future__ import annotations
import subprocess
from pathlib import Path
from typing import Callable, Optional
from twsstarter import autofill, crypto
from twsstarter.models import AppSettings, ConnectionEntry


_TWS_EXES = ["tws.exe", "Jts.exe", "jts.exe", "launch.bat"]
_GW_EXES  = ["ibgateway.exe", "gateway.exe", "launch.bat"]


class ProcessHandle:
    def __init__(self, proc: subprocess.Popen):
        self._proc = proc

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
) -> ProcessHandle:
    path = (entry.tws_path or settings.default_tws_path or "").strip()
    if not path:
        raise ValueError("No TWS path configured. Set it in Settings or on the connection entry.")
    handle = _launch_direct(path, _TWS_EXES)
    password = crypto.decrypt(entry.password_enc)
    autofill.start_thread(
        entry.username, password, entry.paper_trading,
        is_gateway=False, on_done=on_autofill_done,
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
    handle = _launch_direct(path, _GW_EXES)
    password = crypto.decrypt(entry.password_enc)
    autofill.start_thread(
        entry.username, password, entry.paper_trading,
        is_gateway=True, on_done=on_autofill_done,
    )
    return handle


def _launch_direct(app_path: str, candidates: list[str]) -> ProcessHandle:
    import sys
    path = Path(app_path)
    extra = {"creationflags": subprocess.CREATE_NEW_CONSOLE} if sys.platform == "win32" else {}
    for name in candidates:
        exe = path / name
        if exe.exists():
            proc = subprocess.Popen(
                [str(exe)],
                cwd=str(path),
                **extra,
            )
            return ProcessHandle(proc)
    raise FileNotFoundError(
        f"No executable found in '{app_path}'.\n"
        f"Searched: {', '.join(candidates)}"
    )
