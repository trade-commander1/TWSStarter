"""Central application paths (config + logs) in a per-user data directory."""
from __future__ import annotations

import os
import sys
from pathlib import Path


def app_data_dir() -> Path:
    """Writable per-user data directory for TWSStarter (created if missing)."""
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        d = Path(base) / "TWSStarter"
    elif sys.platform == "darwin":
        d = Path.home() / "Library" / "Application Support" / "TWSStarter"
    else:
        base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
        d = Path(base) / "TWSStarter"
    d.mkdir(parents=True, exist_ok=True)
    return d


def config_file() -> Path:
    return app_data_dir() / "config.json"


def log_dir() -> Path:
    d = app_data_dir() / "log"
    d.mkdir(parents=True, exist_ok=True)
    return d


def legacy_data_file() -> Path:
    """Old location used before config.json (for one-time migration)."""
    return Path.home() / ".twsstarter" / "data.json"
