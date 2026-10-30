#!/usr/bin/env bash
# TWSStarter — Linux setup (per user, no root needed).
#   ./install.sh               install / update
#   ./install.sh --uninstall   remove program, icon and menu entry
# Installs to ~/.local/bin, ~/.local/share/icons and ~/.local/share/applications.
# User data (~/.local/share/TWSStarter: connections, logs) is never touched.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
ICON_FILE="${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor/256x256/apps/twsstarter.png"
DESKTOP_FILE="${XDG_DATA_HOME:-$HOME/.local/share}/applications/twsstarter.desktop"

refresh_caches() {
    update-desktop-database "$(dirname "$DESKTOP_FILE")" 2>/dev/null || true
    gtk-update-icon-cache -f -t "${XDG_DATA_HOME:-$HOME/.local/share}/icons/hicolor" 2>/dev/null || true
}

if [ "${1:-}" = "--uninstall" ]; then
    rm -f "$BIN_DIR/TWSStarter" "$ICON_FILE" "$DESKTOP_FILE"
    refresh_caches
    echo "TWSStarter removed. Your settings remain in ~/.local/share/TWSStarter."
    exit 0
fi

if pgrep -x TWSStarter >/dev/null 2>&1; then
    echo "TWSStarter is running — please close it first, then run the setup again."
    exit 1
fi

install -Dm755 "$HERE/TWSStarter" "$BIN_DIR/TWSStarter"
install -Dm644 "$HERE/twsstarter.png" "$ICON_FILE"
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=TWSStarter
Comment=Launcher for IB Trader WorkStation and IB Gateway
Exec=$BIN_DIR/TWSStarter
Icon=twsstarter
Terminal=false
Categories=Office;Finance;
StartupWMClass=TWSStarter
EOF
refresh_caches

echo "TWSStarter installed: $BIN_DIR/TWSStarter"
echo "Start it from the application menu (\"TWSStarter\")."
# Qt needs these X11 libraries on X11 sessions (not needed under Wayland).
if ! ldconfig -p 2>/dev/null | grep -q "libxcb-cursor.so.0"; then
    echo "Note: on an X11 session install: sudo apt install libxcb-cursor0 libxcb-keysyms1"
fi
