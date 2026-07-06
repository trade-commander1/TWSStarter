from __future__ import annotations
import html
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit
from PyQt6.QtGui import QFont
from twsstarter.i18n import tr

# info = white, warn = orange, error = red
_COLORS = {"info": "#f8fafc", "warn": "#f59e0b", "error": "#ef4444"}
_MAX_BLOCKS = 5000
_MIN_LINES = 12


class TracePanel(QWidget):
    """Black trace feed with a Clear button (top-left) and auto-scroll."""

    def __init__(self, parent=None):
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QHBoxLayout()
        header.setContentsMargins(10, 5, 10, 5)
        header.setSpacing(8)
        self._clear_btn = QPushButton(tr('trace_clear'))
        self._clear_btn.setToolTip(tr('tip_trace_clear'))
        self._clear_btn.setFixedHeight(30)
        self._clear_btn.clicked.connect(self.clear)
        header.addWidget(self._clear_btn)
        header.addStretch()
        root.addLayout(header)

        self._text = QPlainTextEdit()
        self._text.setReadOnly(True)
        self._text.setMaximumBlockCount(_MAX_BLOCKS)
        font = QFont("Consolas")
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setPointSize(9)
        self._text.setFont(font)
        self._text.setStyleSheet(
            "QPlainTextEdit{background:#000000;color:#f8fafc;border:none;"
            "padding:4px 8px;}"
        )
        line_h = self._text.fontMetrics().lineSpacing()
        self._text.setMinimumHeight(line_h * _MIN_LINES + 12)
        root.addWidget(self._text)

    def append(self, text: str, level: str) -> None:
        color = _COLORS.get(level, _COLORS["info"])
        safe = html.escape(text).replace(" ", "&nbsp;")
        self._text.appendHtml(f'<span style="color:{color};">{safe}</span>')
        sb = self._text.verticalScrollBar()
        sb.setValue(sb.maximum())

    def clear(self) -> None:
        self._text.clear()

    def retranslate(self) -> None:
        self._clear_btn.setText(tr('trace_clear'))
        self._clear_btn.setToolTip(tr('tip_trace_clear'))
