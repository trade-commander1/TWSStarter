"""Central tracing: a colored GUI trace feed plus a rotating file log.

- GUI: emits `message(text, level)` on the main thread; the trace panel renders
  it white (info) / orange (warn) / red (error). Each line is prefixed with the
  weekday abbreviation and the time to the second, e.g. "Mon 14:23:07".
- File: rotating log under <app_data>/log (5 MB per file, several backups).
- Retention: files older than 3 days are purged (call purge_old_logs() at
  startup and on a timer).
"""
from __future__ import annotations

import logging
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

from PyQt6.QtCore import QObject, pyqtSignal

from twsstarter.paths import log_dir

LEVEL_INFO = "info"
LEVEL_WARN = "warn"
LEVEL_ERROR = "error"

_LOG_MAX_BYTES = 5 * 1024 * 1024   # 5 MB per file (current, modern size)
_LOG_BACKUPS = 20                  # plus age-based purge below
RETENTION_DAYS = 3

# Deterministic English weekday abbreviations (locale-independent).
_WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class Tracer(QObject):
    """Singleton-style tracer. Use tracing.tracer() to obtain the instance."""

    message = pyqtSignal(str, str)  # display_text, level

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._logger = logging.getLogger("twsstarter.trace")
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False
        if not self._logger.handlers:
            handler = RotatingFileHandler(
                log_dir() / "twsstarter.log",
                maxBytes=_LOG_MAX_BYTES,
                backupCount=_LOG_BACKUPS,
                encoding="utf-8",
            )
            handler.setFormatter(
                logging.Formatter("%(asctime)s  %(levelname)-5s  %(message)s")
            )
            self._logger.addHandler(handler)

    # ── Public API ─────────────────────────────────────────────────

    def info(self, text: str) -> None:
        self._emit(text, LEVEL_INFO, logging.INFO)

    def warn(self, text: str) -> None:
        self._emit(text, LEVEL_WARN, logging.WARNING)

    def error(self, text: str) -> None:
        self._emit(text, LEVEL_ERROR, logging.ERROR)

    def purge_old_logs(self, days: int = RETENTION_DAYS) -> int:
        """Delete log files older than `days`. Returns the number removed."""
        cutoff = time.time() - days * 86400
        removed = 0
        for f in log_dir().glob("twsstarter.log*"):
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
                    removed += 1
            except OSError:
                pass
        return removed

    # ── Internal ───────────────────────────────────────────────────

    def _emit(self, text: str, level: str, pylevel: int) -> None:
        now = datetime.now()
        stamp = f"{_WEEKDAYS[now.weekday()]} {now.strftime('%H:%M:%S')}"
        self.message.emit(f"{stamp}  {text}", level)
        self._logger.log(pylevel, text)


_instance: Tracer | None = None


def tracer() -> Tracer:
    """Return the process-wide Tracer (created lazily)."""
    global _instance
    if _instance is None:
        _instance = Tracer()
    return _instance
