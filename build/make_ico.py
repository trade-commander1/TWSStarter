"""Generate build/TWSStarter.ico from the app's vector icon (resources.icon).

Run whenever the icon design changes:
    uv run python build/make_ico.py
Produces a multi-resolution, PNG-compressed .ico used for the Windows .exe
(TWSStarter.spec → EXE icon) and the installer (installer.iss → SetupIconFile).
Qt is the only dependency; no Pillow needed.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

from PyQt6.QtCore import QBuffer, QByteArray, QIODevice
from PyQt6.QtWidgets import QApplication

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from twsstarter.resources.icon import make_icon  # noqa: E402

_SIZES = [16, 24, 32, 48, 64, 128, 256]
_OUT = Path(__file__).resolve().parent / "TWSStarter.ico"


def _png_bytes(size: int) -> bytes:
    ba = QByteArray()
    buf = QBuffer(ba)
    buf.open(QIODevice.OpenModeFlag.WriteOnly)
    make_icon(size).save(buf, "PNG")
    buf.close()
    return bytes(ba)


def main() -> None:
    _app = QApplication.instance() or QApplication(sys.argv)
    images = [(s, _png_bytes(s)) for s in _SIZES]

    # ICONDIR header
    out = struct.pack("<HHH", 0, 1, len(images))
    offset = 6 + 16 * len(images)
    entries, blobs = b"", b""
    for size, data in images:
        dim = 0 if size >= 256 else size  # 0 means 256 in the ICO spec
        # ICONDIRENTRY: w,h,colors,reserved,planes,bitcount,bytesize,offset
        entries += struct.pack(
            "<BBBBHHII", dim, dim, 0, 0, 1, 32, len(data), offset
        )
        offset += len(data)
        blobs += data

    _OUT.write_bytes(out + entries + blobs)
    print(f"wrote {_OUT} ({len(_SIZES)} sizes, {_OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
