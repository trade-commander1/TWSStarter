"""Persistence in a single config.json under the per-user app data directory.

Holds everything: settings (paths, language), connections (incl. default mode
and checked flag), and UI state. Migrates the old ~/.twsstarter/data.json once.
"""
from __future__ import annotations

import json
from pathlib import Path

from twsstarter import crypto
from twsstarter.models import AppSettings, ConnectionEntry
from twsstarter.paths import config_file, legacy_data_file

_CONFIG: Path = config_file()


def _load_raw() -> dict:
    path = _CONFIG
    if not path.exists():
        # One-time migration from the legacy location.
        legacy = legacy_data_file()
        if legacy.exists():
            try:
                with legacy.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                _save_raw(data)
                return data
            except (OSError, json.JSONDecodeError):
                return {}
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_raw(data: dict) -> None:
    _CONFIG.parent.mkdir(parents=True, exist_ok=True)
    with _CONFIG.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_settings() -> AppSettings:
    return AppSettings.from_dict(_load_raw().get("settings", {}))


def save_settings(settings: AppSettings) -> None:
    raw = _load_raw()
    raw["settings"] = settings.to_dict()
    _save_raw(raw)


def load_connections() -> list[ConnectionEntry]:
    return [ConnectionEntry.from_dict(d) for d in _load_raw().get("connections", [])]


def save_connections(connections: list[ConnectionEntry]) -> None:
    raw = _load_raw()
    raw["connections"] = [c.to_dict() for c in connections]
    _save_raw(raw)


def migrate_encryption() -> int:
    """Re-encrypt passwords stored under the old, unstable host+MAC key with the
    current MachineGuid key. Idempotent, non-destructive (a token that cannot be
    recovered is left untouched). Returns the number of tokens migrated.

    Call once at startup — see crypto.reencrypt_legacy for why this is needed.
    """
    raw = _load_raw()
    migrated = 0
    for c in raw.get("connections", []):
        token = c.get("password_enc")
        if not token:
            continue
        try:
            crypto.decrypt(token)  # already valid under the current key
            continue
        except ValueError:
            pass
        new_token = crypto.reencrypt_legacy(token)
        if new_token:
            c["password_enc"] = new_token
            migrated += 1
    if migrated:
        _save_raw(raw)
    return migrated
