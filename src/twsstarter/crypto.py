"""Machine-bound symmetric encryption for stored credentials.

The Fernet key is derived from a stable, per-machine identifier so that a stolen
config file cannot be decrypted on a different computer.

Key input (v1.5+): the Windows **MachineGuid**
(HKLM\\SOFTWARE\\Microsoft\\Cryptography\\MachineGuid), which is created once at
OS installation and never changes for hardware, network adapters, VMs or VPNs.

Prior versions (<=1.4) derived the key from `platform.node() + uuid.getnode()`.
`uuid.getnode()` returns whichever network-adapter MAC is enumerated first, which
is *not* stable: on machines with several NICs (onboard + VMware/VPN/USB) the
returned MAC changes when adapters come and go — even between processes. That
made previously stored passwords undecryptable ("Decryption failed"), breaking
autofill. `reencrypt_legacy()` migrates such tokens to the new key.
"""
from __future__ import annotations

import base64
import platform
import re
import subprocess
import sys
import uuid

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

_SALT = b"TWSStarter_v1_2024_salt"
_ITERATIONS = 480_000

# Windows CREATE_NO_WINDOW — keep the getmac helper from flashing a console.
_CREATE_NO_WINDOW = 0x08000000


def _kdf_key(machine_id: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(machine_id))


def _machine_guid() -> str | None:
    """Stable Windows MachineGuid, or None if unavailable (non-Windows)."""
    if sys.platform != "win32":
        return None
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography",
            0,
            winreg.KEY_READ | winreg.KEY_WOW64_64KEY,
        ) as key:
            value, _ = winreg.QueryValueEx(key, "MachineGuid")
            return str(value) or None
    except OSError:
        return None


def _derive_key() -> bytes:
    """Current machine-bound Fernet key (MachineGuid based on Windows)."""
    guid = _machine_guid()
    if guid:
        machine_id = (guid + "TWSStarter").encode()
    else:
        # Platforms without a MachineGuid fall back to the legacy identity.
        machine_id = (platform.node() + str(uuid.getnode()) + "TWSStarter").encode()
    return _kdf_key(machine_id)


def encrypt(plaintext: str) -> str:
    return Fernet(_derive_key()).encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    try:
        return Fernet(_derive_key()).decrypt(ciphertext.encode()).decode()
    except InvalidToken as e:
        raise ValueError(
            "Decryption failed — data may be corrupted or from a different machine."
        ) from e


# ── Legacy migration (<=1.4 host+MAC key → MachineGuid key) ─────────────────

def _mac_nodes() -> set[int]:
    """Every MAC the machine currently exposes, as integer node values.

    `uuid.getnode()` alone is unreliable — it returns only one of several NICs,
    and which one varies per process — so we also enumerate via `getmac`, which
    lists adapters `uuid.getnode()` skips. This is what makes the one-time
    migration able to recover a token no matter which adapter encrypted it.
    """
    nodes: set[int] = set()
    n = uuid.getnode()
    if n and not (n >> 40) & 1:  # ignore fabricated (random/multicast) nodes
        nodes.add(n)
    if sys.platform == "win32":
        try:
            out = subprocess.run(
                ["getmac", "/nh", "/fo", "csv"],
                capture_output=True,
                text=True,
                timeout=10,
                creationflags=_CREATE_NO_WINDOW,
            ).stdout
            for mac in re.findall(r"[0-9A-Fa-f]{2}(?:[-:][0-9A-Fa-f]{2}){5}", out):
                nodes.add(int(re.sub(r"[-:]", "", mac), 16))
        except (OSError, subprocess.SubprocessError):
            pass
    return nodes


def reencrypt_legacy(ciphertext: str) -> str | None:
    """Migrate a token from the old host+MAC key to the current key.

    Tries the legacy key for every MAC the machine exposes. Returns a fresh token
    re-encrypted under the current (MachineGuid) key, or None if no candidate
    key decrypts it (already migrated, or genuinely foreign/corrupt).
    """
    host = platform.node()
    for node in _mac_nodes():
        legacy_key = _kdf_key((host + str(node) + "TWSStarter").encode())
        try:
            plaintext = Fernet(legacy_key).decrypt(ciphertext.encode()).decode()
        except InvalidToken:
            continue
        return encrypt(plaintext)
    return None
