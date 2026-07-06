"""Render each application window to a PNG under res/ for use in the help/docs.

Run:  uv run python build/make_screens.py [lang]

Uses QWidget.grab() to capture just the window content (no OS title bar) —
ideal for embedding in the help. Renders on the native Qt platform so real fonts
are available (the offscreen platform has none and would produce empty boxes),
i.e. this needs a desktop session. `lang` is a language code (default: en);
pass e.g. `de` for German shots.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT / "src"))

from PyQt6.QtWidgets import QApplication  # noqa: E402

from twsstarter import i18n, storage  # noqa: E402
from twsstarter.ui.theme import STYLESHEET  # noqa: E402
from twsstarter.ui.main_window import MainWindow  # noqa: E402
from twsstarter.ui.connection_dialog import ConnectionDialog  # noqa: E402
from twsstarter.ui.settings_dialog import SettingsDialog  # noqa: E402
from twsstarter.ui.about_dialog import AboutDialog  # noqa: E402
from twsstarter.ui.help_dialog import HelpDialog  # noqa: E402
from twsstarter.ui.disclaimer_dialog import DisclaimerDialog  # noqa: E402

_RES = _ROOT / "res"


def _shot(app: QApplication, widget, name: str, size=None) -> None:
    """Lay out `widget`, render it, and save res/<name>.png."""
    widget.show()
    if size:
        widget.resize(*size)
    else:
        widget.adjustSize()
    for _ in range(3):
        app.processEvents()
    (_RES).mkdir(exist_ok=True)
    out = _RES / f"{name}.png"
    widget.grab().save(str(out))
    print("wrote", out.relative_to(_ROOT))
    widget.close()


def main() -> None:
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    app = QApplication.instance() or QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    i18n.set_language(lang)

    win = MainWindow()
    win.resize(900, 740)
    # Stop the background monitor so it can't override our illustrative status,
    # then show one connection as running (green dot, run-type icon, Stop button).
    win._monitor.stop()
    cards = list(win._cards.values())
    if cards:
        cards[0].set_status("running", "tws")
    _shot(app, win, "ui_main", size=(900, 740))

    conns = storage.load_connections()
    if conns:
        _shot(app, ConnectionDialog(win, entry=conns[0]), "ui_connection_edit")
    _shot(app, ConnectionDialog(win), "ui_connection_add")
    _shot(app, SettingsDialog(storage.load_settings(), win), "ui_settings")
    _shot(app, AboutDialog(win), "ui_about")
    _shot(app, HelpDialog(win), "ui_help", size=(720, 620))
    _shot(app, DisclaimerDialog(win), "ui_disclaimer", size=(560, 460))


if __name__ == "__main__":
    main()
