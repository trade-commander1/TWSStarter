"""Extract the embedded TWS / IB Gateway icons from the installed executables.

Uses Qt's file icon provider, so the real IBKR icons are shown without bundling
any copyrighted artwork. Results are cached per executable path.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from PyQt6.QtCore import QFileInfo
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFileIconProvider

_TWS_EXES = ["tws.exe", "Jts.exe", "jts.exe"]
_GW_EXES = ["ibgateway.exe", "gateway.exe"]

_provider: Optional[QFileIconProvider] = None
_cache: dict[str, Optional[QIcon]] = {}


def _prov() -> QFileIconProvider:
    global _provider
    if _provider is None:
        _provider = QFileIconProvider()
    return _provider


def _find_exe(directory: str, candidates: list[str]) -> Optional[str]:
    if not directory:
        return None
    base = Path(directory)
    for name in candidates:
        p = base / name
        if p.exists():
            return str(p)
    return None


def _icon_for(directory: str, candidates: list[str]) -> Optional[QIcon]:
    exe = _find_exe(directory, candidates)
    if not exe:
        return None
    if exe in _cache:
        return _cache[exe]
    icon = _prov().icon(QFileInfo(exe))
    result = icon if (icon is not None and not icon.isNull()) else None
    _cache[exe] = result
    return result


def tws_icon(directory: str) -> Optional[QIcon]:
    return _icon_for(directory, _TWS_EXES)


def gateway_icon(directory: str) -> Optional[QIcon]:
    return _icon_for(directory, _GW_EXES)
