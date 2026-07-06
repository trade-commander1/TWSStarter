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
uv add --dev pyinstaller

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

# Versioned binary name + tarball
VERSIONED="TWSStarter-${APP_VERSION}.${APP_BUILD}"
cp -f "dist/TWSStarter" "dist/${VERSIONED}"
tar -czf "dist/${VERSIONED}-linux-x86_64.tar.gz" -C dist "${VERSIONED}"

echo ""
echo " Output: dist/TWSStarter            (generic binary)"
echo " Output: dist/${VERSIONED}          (versioned binary)"
echo " Output: dist/${VERSIONED}-linux-x86_64.tar.gz"
