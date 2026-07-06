"""Core data models: a stored connection and the global application settings,
each with JSON (de)serialization for storage.py."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class ConnectionEntry:
    name: str
    username: str
    password_enc: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tws_path: Optional[str] = None
    gateway_path: Optional[str] = None
    paper_trading: bool = False
    # Default launch target used by the "Start Default" control button.
    default_mode: str = "tws"      # "tws" | "gateway"
    # Whether this connection is ticked in the list (persisted).
    checked: bool = False
    # Account id learned from the TWS window title (e.g. "DUH077320") the first
    # time this connection is launched. Used for session-independent runtime
    # detection, because the login username often differs from the account id.
    account_id: Optional[str] = None
    # Obfuscated per-account settings directory learned from the gateway path the
    # first time this connection is started as Gateway. Used to attribute a
    # running Gateway (detected via its TCP port) to this specific connection,
    # because the Gateway window/title carries no account information.
    gateway_account_dir: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "password_enc": self.password_enc,
            "tws_path": self.tws_path,
            "gateway_path": self.gateway_path,
            "paper_trading": self.paper_trading,
            "default_mode": self.default_mode,
            "checked": self.checked,
            "account_id": self.account_id,
            "gateway_account_dir": self.gateway_account_dir,
        }

    @classmethod
    def from_dict(cls, d: dict) -> ConnectionEntry:
        return cls(
            id=d.get("id", str(uuid.uuid4())),
            name=d["name"],
            username=d["username"],
            password_enc=d["password_enc"],
            tws_path=d.get("tws_path"),
            gateway_path=d.get("gateway_path"),
            paper_trading=d.get("paper_trading", False),
            default_mode=d.get("default_mode", "tws"),
            checked=d.get("checked", False),
            account_id=d.get("account_id"),
            gateway_account_dir=d.get("gateway_account_dir"),
        )


@dataclass
class AppSettings:
    default_tws_path: str = r"C:\jts"
    default_gateway_path: str = ""
    language: str = "auto"
    # Whether the one-time first-run disclaimer has been accepted.
    disclaimer_accepted: bool = False

    def to_dict(self) -> dict:
        return {
            "default_tws_path": self.default_tws_path,
            "default_gateway_path": self.default_gateway_path,
            "language": self.language,
            "disclaimer_accepted": self.disclaimer_accepted,
        }

    @classmethod
    def from_dict(cls, d: dict) -> AppSettings:
        return cls(
            default_tws_path=d.get("default_tws_path", r"C:\jts"),
            default_gateway_path=d.get("default_gateway_path", ""),
            language=d.get("language", "auto"),
            disclaimer_accepted=d.get("disclaimer_accepted", False),
        )
