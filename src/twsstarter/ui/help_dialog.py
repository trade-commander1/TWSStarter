from __future__ import annotations
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QTextBrowser
from PyQt6.QtCore import Qt
from twsstarter.i18n import tr


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr('help_title'))
        self.setMinimumSize(600, 500)
        self.resize(680, 560)
        self.setModal(False)
        self._build()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setStyleSheet(
            "QTextBrowser {"
            "  background:#151825;"
            "  color:#e2e8f0;"
            "  font-size:13px;"
            "  border:none;"
            "  padding:20px;"
            "}"
        )
        browser.setHtml(tr('help_text'))
        root.addWidget(browser, 1)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(16, 10, 16, 12)
        btn_row.addStretch()
        btn_close = QPushButton("OK")
        btn_close.setObjectName("btnOK")
        btn_close.setFixedWidth(80)
        btn_close.setDefault(True)
        btn_close.clicked.connect(self.accept)
        btn_row.addWidget(btn_close)
        root.addLayout(btn_row)
