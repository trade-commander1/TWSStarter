from __future__ import annotations
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QFileDialog,
)
from PyQt6.QtCore import Qt
from twsstarter.i18n import tr
from twsstarter.models import AppSettings


class SettingsDialog(QDialog):
    def __init__(self, settings: AppSettings, parent=None):
        super().__init__(parent)
        self._result: AppSettings | None = None
        self.setWindowTitle(tr('settings_title'))
        self.setMinimumWidth(480)
        self.setModal(True)
        self._build()
        self._populate(settings)

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        lbl = QLabel(tr('settings_title'))
        lbl.setStyleSheet("font-size:15px; font-weight:700; color:#ffffff; background:transparent;")
        root.addWidget(lbl)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep)

        root.addWidget(self._section(tr('section_paths')))

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(10)
        form.setContentsMargins(0, 0, 0, 0)

        self._tws_edit = QLineEdit()
        self._tws_edit.setPlaceholderText(r"C:\jts")
        form.addRow(self._lbl(tr('lbl_tws_dir')), self._path_row(self._tws_edit))

        self._gw_edit = QLineEdit()
        self._gw_edit.setPlaceholderText(r"C:\ibgateway")
        form.addRow(self._lbl(tr('lbl_gw_dir')), self._path_row(self._gw_edit))

        root.addLayout(form)
        root.addStretch()

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep2)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        btn_ok = QPushButton(tr('btn_save'))
        btn_ok.setObjectName("btnOK")
        btn_ok.setDefault(True)
        btn_ok.clicked.connect(self._on_ok)
        btn_cancel = QPushButton(tr('btn_cancel'))
        btn_cancel.setObjectName("btnCancel")
        btn_cancel.clicked.connect(self.reject)
        btn_row.addStretch()
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        root.addLayout(btn_row)

    @staticmethod
    def _section(title: str) -> QLabel:
        lbl = QLabel(title)
        lbl.setObjectName("sectionTitle")
        return lbl

    @staticmethod
    def _lbl(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("labelForm")
        lbl.setMinimumWidth(130)
        return lbl

    def _path_row(self, edit: QLineEdit) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)
        btn = QPushButton("…")
        btn.setFixedSize(36, 36)
        btn.setStyleSheet(
            "QPushButton{background:#151825;border:1px solid #252840;"
            "border-radius:5px;color:#94a3b8;font-size:15px;padding:0;}"
            "QPushButton:hover{color:#ffffff;border-color:#3b82f6;}"
        )
        btn.clicked.connect(lambda: self._browse(edit))
        row.addWidget(edit)
        row.addWidget(btn)
        return row

    def _browse(self, target: QLineEdit) -> None:
        path = QFileDialog.getExistingDirectory(self, tr('settings_title'), target.text() or "C:\\")
        if path:
            target.setText(path.replace("/", "\\"))

    def _on_ok(self) -> None:
        self._result = AppSettings(
            default_tws_path=self._tws_edit.text().strip() or r"C:\jts",
            default_gateway_path=self._gw_edit.text().strip(),
            language=self._current_lang,
        )
        self.accept()

    def _populate(self, s: AppSettings) -> None:
        self._current_lang = s.language
        self._tws_edit.setText(s.default_tws_path)
        self._gw_edit.setText(s.default_gateway_path)

    def get_settings(self) -> AppSettings | None:
        return self._result
