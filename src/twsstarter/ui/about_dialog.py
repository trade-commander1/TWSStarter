from __future__ import annotations
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from twsstarter.i18n import tr
from twsstarter.resources.icon import make_icon
from twsstarter.version import VERSION, BUILD


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr('about_title'))
        self.setModal(True)
        self.setFixedSize(360, 260)
        self._build()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 24)
        root.setSpacing(0)

        # Icon + app name row
        top = QHBoxLayout()
        top.setSpacing(18)

        icon_lbl = QLabel()
        px = make_icon(64)
        icon_lbl.setPixmap(px)
        icon_lbl.setFixedSize(64, 64)
        top.addWidget(icon_lbl, 0, Qt.AlignmentFlag.AlignVCenter)

        name_col = QVBoxLayout()
        name_col.setSpacing(4)
        app_name = QLabel("TWSStarter")
        app_name.setStyleSheet(
            "font-size:20px; font-weight:700; color:#ffffff; background:transparent;"
        )
        ver_lbl = QLabel(f"{tr('about_version')} {VERSION}  ·  Build {BUILD}")
        ver_lbl.setStyleSheet("font-size:12px; color:#94a3b8; background:transparent;")
        name_col.addWidget(app_name)
        name_col.addWidget(ver_lbl)
        top.addLayout(name_col)
        top.addStretch()
        root.addLayout(top)

        root.addSpacing(20)

        desc = QLabel(tr('about_desc'))
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size:13px; color:#cbd5e1; background:transparent;")
        root.addWidget(desc)

        root.addSpacing(16)

        copy_lbl = QLabel(tr('about_copyright'))
        copy_lbl.setStyleSheet("font-size:12px; color:#64748b; background:transparent;")
        root.addWidget(copy_lbl)

        root.addStretch()

        btn_ok = QPushButton("OK")
        btn_ok.setObjectName("btnOK")
        btn_ok.setFixedWidth(80)
        btn_ok.clicked.connect(self.accept)
        btn_ok.setDefault(True)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn_ok)
        root.addLayout(btn_row)
