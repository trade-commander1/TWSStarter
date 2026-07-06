"""Add/Edit dialog for a single connection: credentials (password shown behind
an eye toggle), trading mode, default launch target and optional paths."""
from __future__ import annotations
import uuid
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QFileDialog,
    QButtonGroup, QRadioButton,
)
from PyQt6.QtCore import Qt
from twsstarter import crypto
from twsstarter.i18n import tr
from twsstarter.models import ConnectionEntry

_TOGGLE_CSS = """
QRadioButton {
    color: #ffffff;
    font-size: 13px;
    font-weight: 500;
    spacing: 10px;
    padding: 3px 0px;
    background: transparent;
    border: none;
}
QRadioButton:checked {
    color: #ffffff;
    font-weight: 600;
}
QRadioButton:hover:!checked {
    color: #ffffff;
}
QRadioButton::indicator {
    width: 17px;
    height: 17px;
    border-radius: 9px;
    border: 2px solid #475569;
    background: #151825;
}
QRadioButton::indicator:hover {
    border-color: #3b82f6;
}
QRadioButton::indicator:checked {
    border: 2px solid #3b82f6;
    background: qradialgradient(
        cx: 0.5, cy: 0.5, radius: 0.5, fx: 0.5, fy: 0.5,
        stop: 0.00 #ffffff,
        stop: 0.30 #ffffff,
        stop: 0.42 #3b82f6,
        stop: 1.00 #3b82f6
    );
}
"""


class ConnectionDialog(QDialog):
    def __init__(self, parent=None, entry: Optional[ConnectionEntry] = None):
        super().__init__(parent)
        self._existing = entry
        self._result_entry: Optional[ConnectionEntry] = None

        self.setWindowTitle(tr('dlg_edit_title') if entry else tr('dlg_add_title'))
        self.setMinimumWidth(500)
        self.setModal(True)
        self._build()
        if entry:
            self._populate(entry)

    # ── UI ────────────────────────────────────────────────────────

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        lbl_title = QLabel(tr('dlg_heading_edit') if self._existing else tr('dlg_heading_new'))
        lbl_title.setStyleSheet(
            "font-size:15px; font-weight:700; color:#f1f5f9; background:transparent;"
        )
        root.addWidget(lbl_title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep)

        # ── Credentials ───────────────────────────────────────────
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(10)
        form.setContentsMargins(0, 0, 0, 0)

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText(tr('ph_name'))
        form.addRow(self._lbl(tr('lbl_name')), self._name_edit)

        self._user_edit = QLineEdit()
        self._user_edit.setPlaceholderText(tr('ph_username'))
        self._user_edit.textChanged.connect(self._on_username_changed)
        form.addRow(self._lbl(tr('lbl_username')), self._user_edit)

        pw_row = QHBoxLayout()
        pw_row.setSpacing(6)
        self._pw_edit = QLineEdit()
        self._pw_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self._pw_edit.setPlaceholderText(tr('ph_password'))
        btn_eye = QPushButton("👁")
        btn_eye.setFixedSize(36, 36)
        btn_eye.setCheckable(True)
        btn_eye.setToolTip(tr('ph_password'))
        btn_eye.clicked.connect(self._toggle_pw)
        btn_eye.setStyleSheet(
            "QPushButton{background:#151825;border:1px solid #252840;border-radius:5px;"
            "color:#475569;font-size:14px;padding:0;}"
            "QPushButton:checked{color:#3b82f6;border-color:#3b82f6;}"
        )
        pw_row.addWidget(self._pw_edit)
        pw_row.addWidget(btn_eye)
        form.addRow(self._lbl(tr('lbl_password')), pw_row)

        root.addLayout(form)

        # ── Trading Mode ──────────────────────────────────────────
        root.addWidget(self._build_mode_section())

        # ── Default start target (TWS / Gateway) ──────────────────
        root.addWidget(self._build_default_mode_section())

        # ── Paths ─────────────────────────────────────────────────
        root.addWidget(self._build_paths_section())

        root.addStretch()

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        root.addWidget(sep2)

        # Buttons
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

    def _build_mode_section(self) -> QFrame:
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        mode_lbl = self._lbl(tr('lbl_mode'))
        mode_lbl.setMinimumWidth(94)
        layout.addWidget(mode_lbl)
        layout.addSpacing(8)

        self._rb_live = QRadioButton(tr('mode_live'))
        self._rb_paper = QRadioButton(tr('mode_paper'))
        self._rb_live.setStyleSheet(_TOGGLE_CSS)
        self._rb_paper.setStyleSheet(_TOGGLE_CSS)
        self._rb_paper.setChecked(True)

        self._mode_group = QButtonGroup(self)
        self._mode_group.addButton(self._rb_live, 0)
        self._mode_group.addButton(self._rb_paper, 1)

        layout.addWidget(self._rb_live)
        layout.addSpacing(6)
        layout.addWidget(self._rb_paper)
        layout.addStretch()
        return frame

    def _build_default_mode_section(self) -> QFrame:
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        lbl = self._lbl(tr('lbl_default_mode'))
        lbl.setMinimumWidth(94)
        layout.addWidget(lbl)
        layout.addSpacing(8)

        self._rb_tws = QRadioButton("TWS")
        self._rb_gw = QRadioButton("Gateway")
        self._rb_tws.setStyleSheet(_TOGGLE_CSS)
        self._rb_gw.setStyleSheet(_TOGGLE_CSS)
        self._rb_tws.setChecked(True)  # TWS is the default

        self._defmode_group = QButtonGroup(self)
        self._defmode_group.addButton(self._rb_tws, 0)
        self._defmode_group.addButton(self._rb_gw, 1)

        layout.addWidget(self._rb_tws)
        layout.addSpacing(6)
        layout.addWidget(self._rb_gw)
        layout.addStretch()
        return frame

    def _build_paths_section(self) -> QFrame:
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(8)

        hint = QLabel(tr('hint_paths'))
        hint.setObjectName("labelHint")
        layout.addWidget(hint)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.setSpacing(8)
        form.setContentsMargins(0, 0, 0, 0)

        self._tws_edit = QLineEdit()
        self._tws_edit.setPlaceholderText(r"C:\jts")
        form.addRow(self._lbl(tr('lbl_tws_path')), self._path_row(self._tws_edit))

        self._gw_edit = QLineEdit()
        self._gw_edit.setPlaceholderText(r"C:\ibgateway")
        form.addRow(self._lbl(tr('lbl_gw_path')), self._path_row(self._gw_edit))

        layout.addLayout(form)
        return frame

    def _path_row(self, edit: QLineEdit) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)
        btn = QPushButton("…")
        btn.setFixedSize(36, 36)
        btn.setStyleSheet(
            "QPushButton{background:#151825;border:1px solid #252840;"
            "border-radius:5px;color:#64748b;font-size:15px;padding:0;}"
            "QPushButton:hover{color:#f1f5f9;border-color:#3b82f6;}"
        )
        btn.clicked.connect(lambda: self._browse(edit))
        row.addWidget(edit)
        row.addWidget(btn)
        return row

    @staticmethod
    def _lbl(text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("labelForm")
        lbl.setMinimumWidth(94)
        return lbl

    # ── Slots ──────────────────────────────────────────────────────

    def _on_username_changed(self, text: str) -> None:
        if not self._name_edit.text() or (
            self._existing and self._name_edit.text() == self._existing.username
        ):
            self._name_edit.blockSignals(True)
            self._name_edit.setText(text)
            self._name_edit.blockSignals(False)

    def _toggle_pw(self, checked: bool) -> None:
        self._pw_edit.setEchoMode(
            QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        )

    def _browse(self, target: QLineEdit) -> None:
        path = QFileDialog.getExistingDirectory(self, tr('settings_title'), target.text() or "C:\\")
        if path:
            target.setText(path.replace("/", "\\"))

    def _on_ok(self) -> None:
        name = self._name_edit.text().strip()
        username = self._user_edit.text().strip()
        password = self._pw_edit.text()

        if not name:
            self._name_edit.setFocus()
            self._name_edit.setStyleSheet("border-color:#ef4444;")
            return
        if not username:
            self._user_edit.setFocus()
            self._user_edit.setStyleSheet("border-color:#ef4444;")
            return
        if not password and not self._existing:
            self._pw_edit.setFocus()
            self._pw_edit.setStyleSheet("border-color:#ef4444;")
            return

        pw_enc = crypto.encrypt(password) if password else self._existing.password_enc
        paper = self._rb_paper.isChecked()
        default_mode = "gateway" if self._rb_gw.isChecked() else "tws"

        self._result_entry = ConnectionEntry(
            id=self._existing.id if self._existing else str(uuid.uuid4()),
            name=name,
            username=username,
            password_enc=pw_enc,
            tws_path=self._tws_edit.text().strip() or None,
            gateway_path=self._gw_edit.text().strip() or None,
            paper_trading=paper,
            default_mode=default_mode,
            checked=self._existing.checked if self._existing else False,
            account_id=self._existing.account_id if self._existing else None,
            gateway_account_dir=(
                self._existing.gateway_account_dir if self._existing else None
            ),
        )
        self.accept()

    # ── Public ─────────────────────────────────────────────────────

    def get_entry(self) -> Optional[ConnectionEntry]:
        return self._result_entry

    def _populate(self, e: ConnectionEntry) -> None:
        self._name_edit.setText(e.name)
        self._user_edit.setText(e.username)
        self._pw_edit.setPlaceholderText(tr('ph_pw_unchanged'))
        # Pre-fill the current password (masked) so the eye button can reveal it.
        # If the stored token cannot be decrypted, leave the field empty — the
        # "unchanged" placeholder then applies and the user can set a new one.
        try:
            self._pw_edit.setText(crypto.decrypt(e.password_enc))
        except ValueError:
            pass
        self._rb_paper.setChecked(e.paper_trading)
        self._rb_live.setChecked(not e.paper_trading)
        self._rb_gw.setChecked(e.default_mode == "gateway")
        self._rb_tws.setChecked(e.default_mode != "gateway")
        if e.tws_path:
            self._tws_edit.setText(e.tws_path)
        if e.gateway_path:
            self._gw_edit.setText(e.gateway_path)
