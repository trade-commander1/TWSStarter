"""First-run disclaimer, shown once until accepted (see main.py).

Intentionally English-only and not part of i18n: it is a legal notice whose
wording should not vary by UI language.
"""
from __future__ import annotations

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextBrowser,
)

_DISCLAIMER_HTML = """
<h3 style="color:#f1f5f9;">Disclaimer</h3>
<p>TWSStarter is an independent tool and is <b>not affiliated with, endorsed by,
or connected to Interactive Brokers LLC</b>. &quot;Trader Workstation (TWS)&quot;,
&quot;IB Gateway&quot; and &quot;IBKR&quot; are trademarks of their respective
owners.</p>

<p>This software is provided <b>&quot;as is&quot;, without warranty of any
kind</b>. It automates launching and login &mdash; including simulated keystrokes
and clipboard use &mdash; for your convenience. You alone are responsible for its
use, for keeping your credentials secure, and for all activity in your account.</p>

<p>Trading financial instruments involves substantial risk of loss.
<b>Nothing in this software constitutes financial advice.</b> To the maximum
extent permitted by law, the authors accept no liability for any loss or damage
arising from the use of this software.</p>

<p>By clicking <b>Accept &amp; Continue</b> you acknowledge that you have read and
agree to these terms. If you do not agree, click <b>Quit</b>.</p>
"""


class DisclaimerDialog(QDialog):
    """Modal first-run disclaimer. exec() returns Accepted only if the user
    explicitly accepts; closing or Quit counts as rejection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TWSStarter — Disclaimer")
        self.setModal(True)
        self.setMinimumSize(560, 460)
        self._build()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 18)
        root.setSpacing(14)

        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setHtml(_DISCLAIMER_HTML)
        text.setStyleSheet(
            "QTextBrowser {"
            "  background:#151825;"
            "  color:#cbd5e1;"
            "  font-size:13px;"
            "  border:1px solid #252840;"
            "  border-radius:8px;"
            "  padding:14px;"
            "}"
        )
        root.addWidget(text, 1)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_quit = QPushButton("Quit")
        btn_quit.setObjectName("btnDanger")
        btn_quit.setFixedWidth(96)
        btn_quit.clicked.connect(self.reject)

        btn_accept = QPushButton("Accept && Continue")
        btn_accept.setObjectName("btnOK")
        btn_accept.setMinimumWidth(150)
        btn_accept.setDefault(True)
        btn_accept.clicked.connect(self.accept)

        btn_row.addStretch()
        btn_row.addWidget(btn_quit)
        btn_row.addWidget(btn_accept)
        root.addLayout(btn_row)
