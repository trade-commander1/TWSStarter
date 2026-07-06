"""Application entry point: sets up Qt, language, icon and the main window."""
from __future__ import annotations
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from twsstarter.ui.theme import STYLESHEET
from twsstarter.ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("TWSStarter")
    app.setOrganizationName("trade-commander")
    app.setStyleSheet(STYLESHEET)

    # Language: load settings first, then determine language
    from twsstarter import storage
    from twsstarter import i18n

    settings = storage.load_settings()
    if settings.language == "auto":
        lang = i18n.detect_language()
    else:
        lang = settings.language
    i18n.set_language(lang)

    # One-time re-encryption of credentials stored under the old, unstable
    # host+MAC key (<=1.4) to the stable MachineGuid key.
    from twsstarter.tracing import tracer

    migrated = storage.migrate_encryption()
    if migrated:
        tracer().info(f"Migrated {migrated} stored password(s) to the new key.")

    # Set application icon
    from twsstarter.resources.icon import make_icon
    icon = QIcon(make_icon(256))
    app.setWindowIcon(icon)

    # First-run disclaimer: show once; quitting/closing declines and exits.
    if not settings.disclaimer_accepted:
        from twsstarter.ui.disclaimer_dialog import DisclaimerDialog
        if not DisclaimerDialog().exec():
            sys.exit(0)
        settings.disclaimer_accepted = True
        storage.save_settings(settings)

    window = MainWindow()
    window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
