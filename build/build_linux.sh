#!/usr/bin/env bash
# TWSStarter — Linux build script
# Requires: uv installed, Python 3.11+, PyQt6 system libs or bundled
# Output: dist/TWSStarter

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# ── Read version/build from the single source of truth ──────────────
read APP_VERSION APP_BUILD < <(uv run python -c "import twsstarter.version as v; print(v.VERSION, v.BUILD)")
echo "Building TWSStarter v${APP_VERSION} Build ${APP_BUILD}"

echo "[1/3] Installing PyInstaller ..."
uv sync --dev

echo "[2/3] Building Linux binary ..."
uv run pyinstaller \
    --clean \
    --noconfirm \
    --name TWSStarter \
    --onefile \
    --windowed \
    --hidden-import twsstarter.i18n \
    --hidden-import twsstarter.i18n.strings \
    --hidden-import twsstarter.resources.icon \
    --hidden-import cryptography \
    --hidden-import cryptography.fernet \
    --hidden-import cryptography.hazmat.primitives \
    --hidden-import cryptography.hazmat.primitives.kdf.pbkdf2 \
    --hidden-import cryptography.hazmat.backends \
    --hidden-import pyautogui \
    --exclude-module tkinter \
    --exclude-module matplotlib \
    --exclude-module numpy \
    --exclude-module win32gui \
    --exclude-module win32con \
    --exclude-module win32api \
    --exclude-module win32clipboard \
    --exclude-module pywinauto \
    src/twsstarter/main.py

echo "[3/3] Packaging ..."
if [ ! -f "dist/TWSStarter" ]; then
    echo " ERROR: Build failed — dist/TWSStarter not found."
    exit 1
fi

# Versioned binary name + tarball. The tarball holds a folder with the binary,
# the app icon and the per-user setup script (install.sh).
VERSIONED="TWSStarter-${APP_VERSION}.${APP_BUILD}"
cp -f "dist/TWSStarter" "dist/${VERSIONED}"
PKG="dist/${VERSIONED}-linux-x86_64"
rm -rf "$PKG"
mkdir -p "$PKG"
cp -f "dist/TWSStarter" "$PKG/TWSStarter"
cp -f build/install_linux.sh "$PKG/install.sh"
chmod +x "$PKG/install.sh"
QT_QPA_PLATFORM=offscreen uv run python -c "
import sys
from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)
from twsstarter.resources.icon import make_icon
assert make_icon(256).save(sys.argv[1])" "$PKG/twsstarter.png"
tar -czf "${PKG}.tar.gz" -C dist "$(basename "$PKG")"

echo ""
echo " Output: dist/TWSStarter            (generic binary)"
echo " Output: dist/${VERSIONED}          (versioned binary)"
echo " Output: ${PKG}.tar.gz  (binary + icon + install.sh)"
