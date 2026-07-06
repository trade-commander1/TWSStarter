"""One row in the connection list: status dot, name, mode/live badges, the
per-connection start buttons (Default | TWS | Gateway) plus Stop/Edit/Delete."""
from __future__ import annotations
from typing import Callable
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QCheckBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter, QBrush
from twsstarter.i18n import tr
from twsstarter.models import AppSettings, ConnectionEntry
from twsstarter.resources.exe_icons import tws_icon, gateway_icon
from twsstarter.ui.theme import START_BTN_CSS, STOP_BTN_CSS


class _StatusDot(QLabel):
    _COLORS = {
        "stopped":  "#334155",
        "starting": "#f59e0b",
        "running":  "#22c55e",
        "error":    "#ef4444",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._status = "stopped"
        self.setFixedSize(10, 10)

    def set_status(self, status: str) -> None:
        self._status = status
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(self._COLORS.get(self._status, "#334155"))
        if self._status in ("running", "starting"):
            glow = QColor(color)
            glow.setAlpha(40)
            p.setBrush(QBrush(glow))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(-2, -2, 14, 14)
        p.setBrush(QBrush(color))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(0, 0, 10, 10)


class ConnectionCard(QFrame):
    def __init__(
        self,
        entry: ConnectionEntry,
        settings: AppSettings,
        on_checked: Callable[[ConnectionEntry, bool], None],
        on_edit:    Callable[[ConnectionEntry], None],
        on_delete:  Callable[[ConnectionEntry], None],
        on_stop:    Callable[[ConnectionEntry], None],
        on_start:   Callable[[ConnectionEntry, str], None],
        parent=None,
    ):
        super().__init__(parent)
        self.entry = entry
        self.settings = settings
        self._on_checked = on_checked
        self._on_edit = on_edit
        self._on_delete = on_delete
        self._on_stop = on_stop
        self._on_start = on_start

        self.setObjectName("connectionCard")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setMinimumHeight(72)
        self._build()

    def _build(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(14, 12, 16, 12)
        root.setSpacing(12)

        # Selection checkbox
        self._chk = QCheckBox()
        self._chk.setChecked(self.entry.checked)
        self._chk.toggled.connect(self._on_toggle)
        root.addWidget(self._chk, 0, Qt.AlignmentFlag.AlignVCenter)

        # Status dot
        self._dot = _StatusDot()
        root.addWidget(self._dot, 0, Qt.AlignmentFlag.AlignVCenter)

        # Info column
        info = QVBoxLayout()
        info.setSpacing(3)
        info.setContentsMargins(0, 0, 0, 0)

        name_row = QHBoxLayout()
        name_row.setSpacing(8)
        name_row.setContentsMargins(0, 0, 0, 0)
        self._name_lbl = QLabel(self.entry.name)
        self._name_lbl.setObjectName("connName")
        self._mode_badge = QLabel(
            tr('badge_paper') if self.entry.paper_trading else tr('badge_live')
        )
        self._mode_badge.setFixedHeight(18)
        self._mode_badge.setStyleSheet(self._badge_css(self.entry.paper_trading))
        self._def_badge = QLabel(self._default_mode_text())
        self._def_badge.setFixedHeight(18)
        self._def_badge.setStyleSheet(self._def_badge_css())
        # Live running-type icon (real TWS/Gateway), far left before the name.
        # Fixed-width slot so names stay aligned whether an icon is shown or not.
        self._run_lbl = QLabel("")
        self._run_lbl.setFixedWidth(22)
        self._run_lbl.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._run_lbl.setStyleSheet("font-size:11px; font-weight:600; background:transparent;")
        name_row.addWidget(self._run_lbl)
        name_row.addWidget(self._name_lbl)
        name_row.addWidget(self._mode_badge)
        name_row.addWidget(self._def_badge)
        name_row.addStretch()
        info.addLayout(name_row)

        self._user_lbl = QLabel(self.entry.username)
        self._user_lbl.setObjectName("connUser")
        self._path_lbl = QLabel(self._format_paths())
        self._path_lbl.setObjectName("connPath")
        info.addWidget(self._user_lbl)
        info.addWidget(self._path_lbl)
        root.addLayout(info, 1)

        # Right-side buttons at a fixed position: Default | TWS | Gateway [Stop],
        # then Edit / Delete. Default is left-most (matching the control row).
        # Stop is shown only while running; it retains its slot when hidden so
        # the start buttons never shift.
        btns = QHBoxLayout()
        btns.setSpacing(6)
        btns.setContentsMargins(0, 0, 0, 0)

        self._btn_stop = QPushButton(tr('btn_stop'))
        self._btn_stop.setToolTip(tr('tooltip_stop'))
        self._btn_stop.setStyleSheet(STOP_BTN_CSS)
        self._btn_stop.clicked.connect(lambda: self._on_stop(self.entry))
        sp = self._btn_stop.sizePolicy()
        sp.setRetainSizeWhenHidden(True)
        self._btn_stop.setSizePolicy(sp)
        self._btn_stop.setVisible(False)

        self._btn_start_tws = self._make_start_btn(tr('btn_tws'), tr('tooltip_tws'), "tws")
        self._btn_start_gw = self._make_start_btn(tr('btn_gateway'), tr('tooltip_gw'), "gateway")
        self._btn_start_def = self._make_start_btn(tr('mode_default'), tr('tip_start_default'), "default")

        # TWS/Gateway/Default share one width = the Gateway button's natural width;
        # Stop matches too for a uniform row. Same height as the "All" buttons.
        unit_w = max(72, self._btn_start_gw.sizeHint().width())
        for b in (self._btn_stop, self._btn_start_tws, self._btn_start_gw, self._btn_start_def):
            b.setFixedSize(unit_w, 30)

        btns.addWidget(self._btn_start_def)
        btns.addWidget(self._btn_start_tws)
        btns.addWidget(self._btn_start_gw)
        btns.addWidget(self._btn_stop)
        btns.addSpacing(8)

        btn_edit = QPushButton(tr('btn_edit'))
        btn_edit.setFixedWidth(52)
        btn_edit.setToolTip(tr('btn_edit'))
        btn_edit.clicked.connect(lambda: self._on_edit(self.entry))

        btn_del = QPushButton(tr('btn_delete'))
        btn_del.setObjectName("btnDanger")
        btn_del.setFixedWidth(72)
        btn_del.setToolTip(tr('btn_delete'))
        btn_del.clicked.connect(lambda: self._on_delete(self.entry))

        btns.addWidget(btn_edit)
        btns.addWidget(btn_del)
        root.addLayout(btns)

    # ── helpers ───────────────────────────────────────────────────

    def _make_start_btn(self, label: str, tooltip: str, mode: str) -> QPushButton:
        """Create a per-card start button that launches this connection in `mode`
        ('default' | 'tws' | 'gateway'). Same BK/FG as the 'All' control row."""
        btn = QPushButton(label)
        btn.setToolTip(tooltip)
        btn.setStyleSheet(START_BTN_CSS)
        btn.clicked.connect(lambda: self._on_start(self.entry, mode))
        return btn

    def _default_mode_text(self) -> str:
        return "▶ " + ("Gateway" if self.entry.default_mode == "gateway" else "TWS")

    @staticmethod
    def _def_badge_css() -> str:
        return (
            "QLabel{background:#1e2235;color:#94a3b8;border:1px solid #2a2f45;"
            "border-radius:4px;padding:1px 7px;font-size:10px;font-weight:700;}"
        )

    @staticmethod
    def _badge_css(paper: bool) -> str:
        if paper:
            # PAPER → red
            return (
                "QLabel{background:#7f1d1d;color:#fecaca;border-radius:4px;"
                "padding:1px 7px;font-size:10px;font-weight:700;}"
            )
        # LIVE → green
        return (
            "QLabel{background:#14532d;color:#86efac;border-radius:4px;"
            "padding:1px 7px;font-size:10px;font-weight:700;}"
        )

    def _format_paths(self) -> str:
        default_tag = f" ({tr('path_default')})"
        tws = self.entry.tws_path or self.settings.default_tws_path or "—"
        gw = self.entry.gateway_path or self.settings.default_gateway_path
        if not self.entry.tws_path and self.settings.default_tws_path:
            tws = f"{tws}{default_tag}"
        line = f"TWS: {tws}"
        if gw:
            if not self.entry.gateway_path:
                gw = f"{gw}{default_tag}"
            line += f"   |   GW: {gw}"
        return line

    # ── public ────────────────────────────────────────────────────

    def is_checked(self) -> bool:
        return self._chk.isChecked()

    def set_checked(self, value: bool) -> None:
        self._chk.blockSignals(True)
        self._chk.setChecked(value)
        self._chk.blockSignals(False)

    def set_status(self, status: str, run_type: str = "") -> None:
        """status: stopped|starting|running. run_type: '', 'tws' or 'gateway'."""
        self._dot.set_status(status)
        self._btn_stop.setVisible(status in ("running", "starting"))
        if status in ("running", "starting") and run_type:
            self._show_run_type(run_type, status)
        else:
            self._run_lbl.clear()
            self._run_lbl.setText("")
            self._run_lbl.setToolTip("")

    def _show_run_type(self, run_type: str, status: str) -> None:
        """Show the real TWS/Gateway exe icon (text fallback if unavailable)."""
        is_gw = run_type == "gateway"
        label = "Gateway" if is_gw else "TWS"
        if is_gw:
            directory = self.entry.gateway_path or self.settings.default_gateway_path
            icon = gateway_icon(directory or "")
        else:
            directory = self.entry.tws_path or self.settings.default_tws_path
            icon = tws_icon(directory or "")

        self._run_lbl.setToolTip(label)
        if icon is not None:
            self._run_lbl.setPixmap(icon.pixmap(18, 18))
        else:
            color = "#22c55e" if status == "running" else "#f59e0b"
            self._run_lbl.setText(f"· {label}")
            self._run_lbl.setStyleSheet(
                f"color:{color}; font-size:11px; font-weight:600; background:transparent;"
            )

    def refresh(self, entry: ConnectionEntry, settings: AppSettings) -> None:
        self.entry = entry
        self.settings = settings
        self._name_lbl.setText(entry.name)
        self._user_lbl.setText(entry.username)
        self._path_lbl.setText(self._format_paths())
        self._mode_badge.setText(tr('badge_paper') if entry.paper_trading else tr('badge_live'))
        self._mode_badge.setStyleSheet(self._badge_css(entry.paper_trading))
        self._def_badge.setText(self._default_mode_text())
        self.set_checked(entry.checked)

    # ── internal ──────────────────────────────────────────────────

    def _on_toggle(self, checked: bool) -> None:
        self._on_checked(self.entry, checked)
