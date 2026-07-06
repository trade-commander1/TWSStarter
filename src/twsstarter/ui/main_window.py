"""Main window: header, batch control row, the scrollable list of connection
cards, and the trace panel. Owns the RuntimeMonitor and turns its signals into
per-card status updates."""
from __future__ import annotations
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QScrollArea, QLabel, QPushButton, QFrame, QMessageBox, QCheckBox,
    QDialog,
)
from PyQt6.QtCore import Qt, QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QActionGroup, QKeySequence
from twsstarter import launcher, storage
from twsstarter import i18n
from twsstarter.i18n import tr
from twsstarter.i18n.strings import LANGUAGES
from twsstarter.models import AppSettings, ConnectionEntry
from twsstarter.launcher import ProcessHandle
from twsstarter.runtime_monitor import RuntimeMonitor, ConnSnapshot
from twsstarter.process_scan import scan_running, terminate_pid
from twsstarter.tracing import tracer
from twsstarter.version import title_string
from twsstarter.resources.flags import flag_icon
from twsstarter.ui.theme import START_BTN_CSS, STOP_BTN_CSS
from twsstarter.ui.connection_card import ConnectionCard
from twsstarter.ui.connection_dialog import ConnectionDialog
from twsstarter.ui.settings_dialog import SettingsDialog
from twsstarter.ui.about_dialog import AboutDialog
from twsstarter.ui.help_browser import open_help_in_browser
from twsstarter.ui.trace_panel import TracePanel


class _AutofillBridge(QObject):
    message = pyqtSignal(str)


class MainWindow(QMainWindow):
    _MONITOR_INTERVAL = 10.0          # seconds between runtime checks
    _LOG_CLEANUP_MS = 6 * 3600 * 1000  # purge old logs every 6 hours

    def __init__(self):
        super().__init__()
        self.settings: AppSettings = storage.load_settings()
        self.connections: list[ConnectionEntry] = storage.load_connections()
        self._handles: dict[str, ProcessHandle] = {}   # session-launched only
        self._cards: dict[str, ConnectionCard] = {}
        self._running_ids: set[str] = set()            # driven by the monitor
        self._run_types: dict[str, str] = {}           # id → "tws"|"gateway"

        self._autofill_bridge = _AutofillBridge()
        self._autofill_bridge.message.connect(
            lambda msg: tracer().info(msg)
        )

        self._monitor = RuntimeMonitor(interval=self._MONITOR_INTERVAL)
        self._monitor.status_changed.connect(self._on_status_changed)
        self._monitor.account_learned.connect(self._learn_account)
        self._monitor.gateway_dir_learned.connect(self._learn_gateway_dir)

        self.setWindowTitle(title_string())
        self.setMinimumSize(760, 640)
        self.resize(880, 760)

        self._build_central()
        self._build_menu()
        tracer().message.connect(self._append_trace)
        self._rebuild_cards()
        self.statusBar().showMessage(tr('status_ready'))
        tracer().info(f"{title_string()} — {tr('status_ready')}")

        self._push_connections()
        self._monitor.start()

        # Periodic log cleanup (>3 days), plus once at startup.
        removed = tracer().purge_old_logs()
        if removed:
            tracer().info(f"Removed {removed} old log file(s).")
        self._cleanup_timer = QTimer(self)
        self._cleanup_timer.timeout.connect(lambda: tracer().purge_old_logs())
        self._cleanup_timer.start(self._LOG_CLEANUP_MS)

    def _push_connections(self) -> None:
        """Send the connection snapshot (incl. effective gateway path) to monitor."""
        snapshot = [
            ConnSnapshot(
                id=e.id,
                name=e.name,
                username=e.username,
                account_id=e.account_id or "",
                gateway_path=(e.gateway_path or self.settings.default_gateway_path or ""),
                gateway_dir=e.gateway_account_dir or "",
            )
            for e in self.connections
        ]
        self._monitor.set_connections(snapshot)

    @staticmethod
    def _instances_for(entry: ConnectionEntry) -> list:
        """Running TWS instances attributable to a connection (for stop)."""
        out = []
        starts = [n.lower() for n in (entry.account_id, entry.name) if n]
        user = entry.username.lower() if entry.username else ""
        for inst in scan_running():
            if inst.kind not in ("tws", "gateway"):
                continue
            title = inst.title.lower()
            if any(title.startswith(n) for n in starts) or (user and user in title):
                out.append(inst)
        return out

    # ── UI construction ───────────────────────────────────────────

    def _build_central(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)

        vbox.addWidget(self._build_header())
        vbox.addWidget(self._build_control_row())
        vbox.addWidget(self._hline())
        vbox.addWidget(self._build_scroll(), 1)
        vbox.addWidget(self._hline())
        self._trace = TracePanel()
        vbox.addWidget(self._trace)

    @staticmethod
    def _hline() -> QFrame:
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedHeight(1)
        line.setStyleSheet("background:#1e2235; border:none;")
        return line

    def _build_header(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("header")
        bar.setFixedHeight(60)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 16, 0)
        layout.setSpacing(8)

        col = QVBoxLayout()
        col.setSpacing(1)
        title = QLabel("TWSStarter")
        title.setObjectName("appTitle")
        sub = QLabel(tr('subtitle'))
        sub.setObjectName("appSubtitle")
        col.addWidget(title)
        col.addWidget(sub)
        layout.addLayout(col)
        layout.addStretch()

        btn_add = QPushButton(tr('btn_add'))
        btn_add.setObjectName("btnAdd")
        btn_add.clicked.connect(self._on_add)
        layout.addWidget(btn_add)

        btn_settings = QPushButton(tr('btn_settings'))
        btn_settings.setObjectName("btnSettings")
        btn_settings.clicked.connect(self._on_settings)
        layout.addWidget(btn_settings)
        return bar

    # Shared inline button styles live in theme.py (START_BTN_CSS / STOP_BTN_CSS)
    # so the control row and the per-card buttons use identical BK/FG colors.
    _START_BTN_CSS = START_BTN_CSS
    _STOP_BTN_CSS = STOP_BTN_CSS

    def _build_control_row(self) -> QWidget:
        bar = QWidget()
        bar.setObjectName("controlRow")
        bar.setFixedHeight(48)
        # Selector-scoped so the background does NOT cascade onto child buttons.
        bar.setStyleSheet("QWidget#controlRow{background:#0d0f16;}")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(8)

        self._chk_all = QCheckBox(tr('chk_all'))
        self._chk_all.setTristate(True)
        self._chk_all.setToolTip(tr('tip_all'))
        self._chk_all.clicked.connect(self._on_all_clicked)
        layout.addWidget(self._chk_all)

        layout.addSpacing(8)

        btn_tws = QPushButton(f"{tr('ctl_start')} TWS")
        btn_tws.setToolTip(tr('tip_start_tws'))
        btn_tws.clicked.connect(lambda: self._start_checked("tws"))

        btn_gw = QPushButton(f"{tr('ctl_start')} Gateway")
        btn_gw.setToolTip(tr('tip_start_gw'))
        btn_gw.clicked.connect(lambda: self._start_checked("gateway"))

        btn_def = QPushButton(f"{tr('ctl_start')} {tr('mode_default')}")
        btn_def.setToolTip(tr('tip_start_default'))
        btn_def.clicked.connect(lambda: self._start_checked("default"))

        btn_stop = QPushButton(tr('btn_stop'))
        btn_stop.setToolTip(tr('tip_stop'))
        btn_stop.clicked.connect(self._stop_checked)

        for b in (btn_def, btn_tws, btn_gw):
            b.setStyleSheet(self._START_BTN_CSS)
        btn_stop.setStyleSheet(self._STOP_BTN_CSS)

        # Order: Start Default first (left-most), then TWS, Gateway, Stop.
        for b in (btn_def, btn_tws, btn_gw, btn_stop):
            b.setFixedSize(132, 30)   # all buttons identical size
            layout.addWidget(b)

        layout.addStretch()
        self._run_count_lbl = QLabel("")
        self._run_count_lbl.setStyleSheet("color:#64748b; font-size:11px; background:transparent;")
        layout.addWidget(self._run_count_lbl)
        return bar

    def _build_scroll(self) -> QScrollArea:
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._cards_container = QWidget()
        self._cards_layout = QVBoxLayout(self._cards_container)
        self._cards_layout.setContentsMargins(16, 16, 16, 16)
        self._cards_layout.setSpacing(8)
        self._cards_layout.addStretch()

        scroll.setWidget(self._cards_container)
        return scroll

    def _build_menu(self) -> None:
        mb = self.menuBar()
        mb.clear()

        lang_menu = mb.addMenu(tr('lbl_language'))
        lang_group = QActionGroup(self)
        lang_group.setExclusive(True)
        current_lang = i18n.current()
        for code, name in LANGUAGES.items():
            act = QAction(name, self)
            act.setCheckable(True)
            act.setChecked(code == current_lang)
            act.setData(code)
            icon = flag_icon(code)          # national flag before the language name
            if icon is not None:
                act.setIcon(icon)
            act.triggered.connect(lambda checked, c=code: self._on_language_changed(c))
            lang_group.addAction(act)
            lang_menu.addAction(act)

        help_menu = mb.addMenu(tr('menu_help'))
        act_help = QAction(tr('action_help'), self)
        act_help.setShortcut(QKeySequence.StandardKey.HelpContents)
        act_help.triggered.connect(self._on_help)
        help_menu.addAction(act_help)
        help_menu.addSeparator()
        act_about = QAction(tr('action_about'), self)
        act_about.triggered.connect(self._on_about)
        help_menu.addAction(act_about)

    # ── Trace ─────────────────────────────────────────────────────

    def _append_trace(self, text: str, level: str) -> None:
        if hasattr(self, "_trace"):
            self._trace.append(text, level)

    # ── Language switch ───────────────────────────────────────────

    def _on_language_changed(self, lang_code: str) -> None:
        if lang_code == i18n.current():
            return
        i18n.set_language(lang_code)
        self.settings.language = lang_code
        storage.save_settings(self.settings)
        self._retranslate_ui()
        tracer().info(f"Language: {LANGUAGES.get(lang_code, lang_code)}")

    def _retranslate_ui(self) -> None:
        sz = self.size()
        self._cards.clear()
        self._build_central()
        self._build_menu()
        self.statusBar().showMessage(tr('status_ready'))
        self.resize(sz)
        self._rebuild_cards()

    # ── Card management ───────────────────────────────────────────

    def _rebuild_cards(self) -> None:
        for card in self._cards.values():
            self._cards_layout.removeWidget(card)
            card.deleteLater()
        self._cards.clear()

        stretch = self._cards_layout.takeAt(self._cards_layout.count() - 1)

        for entry in self.connections:
            card = ConnectionCard(
                entry=entry,
                settings=self.settings,
                on_checked=self._on_card_checked,
                on_edit=self._on_edit,
                on_delete=self._on_delete,
                on_stop=self._stop_one,
                on_start=self._start_from_card,
            )
            self._cards[entry.id] = card
            self._cards_layout.addWidget(card)

            if self._monitor.is_running(entry.id):
                card.set_status("running", self._run_types.get(entry.id, ""))
            elif self._monitor.is_active(entry.id):
                card.set_status("starting")

        if not self.connections:
            lbl = QLabel(tr('empty_state'))
            lbl.setObjectName("emptyState")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setMinimumHeight(120)
            self._cards_layout.addWidget(lbl)

        if stretch:
            self._cards_layout.addStretch()

        self._update_run_count()
        self._sync_all_checkbox()

    def _update_run_count(self) -> None:
        active = len(self._running_ids)
        self._run_count_lbl.setText(f"{active} active" if active else "")

    # ── Checkbox handling ─────────────────────────────────────────

    def _on_card_checked(self, entry: ConnectionEntry, checked: bool) -> None:
        entry.checked = checked
        storage.save_connections(self.connections)
        self._sync_all_checkbox()

    def _on_all_clicked(self, _checked: bool) -> None:
        # Tristate click cycles; decide target from current entries.
        target = not all(e.checked for e in self.connections) if self.connections else False
        for e in self.connections:
            e.checked = target
            card = self._cards.get(e.id)
            if card:
                card.set_checked(target)
        storage.save_connections(self.connections)
        self._sync_all_checkbox()

    def _sync_all_checkbox(self) -> None:
        if not hasattr(self, "_chk_all"):
            return
        n = len(self.connections)
        checked = sum(1 for e in self.connections if e.checked)
        self._chk_all.blockSignals(True)
        if n == 0 or checked == 0:
            self._chk_all.setCheckState(Qt.CheckState.Unchecked)
        elif checked == n:
            self._chk_all.setCheckState(Qt.CheckState.Checked)
        else:
            self._chk_all.setCheckState(Qt.CheckState.PartiallyChecked)
        self._chk_all.blockSignals(False)

    def _checked_entries(self) -> list[ConnectionEntry]:
        return [e for e in self.connections if e.checked]

    # ── Runtime monitoring (background thread → main thread) ──────

    def _on_status_changed(self, entry_id: str, state: str, run_type: str) -> None:
        if state == "running":
            self._running_ids.add(entry_id)
            self._run_types[entry_id] = run_type
        else:
            self._running_ids.discard(entry_id)
            self._run_types.pop(entry_id, None)
            if state == "stopped":
                self._handles.pop(entry_id, None)
        card = self._cards.get(entry_id)
        if card:
            card.set_status(state, run_type)
        self._update_run_count()
        name = next((e.name for e in self.connections if e.id == entry_id), entry_id)
        if state == "running":
            label = "Gateway" if run_type == "gateway" else "TWS"
            tracer().info(f"'{name}' running · {label}")
        elif state == "stopped":
            tracer().info(f"'{name}' stopped.")

    def _learn_account(self, entry_id: str, account: str) -> None:
        for e in self.connections:
            if e.id == entry_id and e.account_id != account:
                e.account_id = account
                storage.save_connections(self.connections)
                self._push_connections()
                tracer().info(f"'{e.name}': learned account {account}")
                break

    def _learn_gateway_dir(self, entry_id: str, gateway_dir: str) -> None:
        for e in self.connections:
            if e.id == entry_id and e.gateway_account_dir != gateway_dir:
                e.gateway_account_dir = gateway_dir
                storage.save_connections(self.connections)
                self._push_connections()
                tracer().info(f"'{e.name}': learned gateway account.")
                break

    # ── Connection CRUD ───────────────────────────────────────────

    def _on_add(self) -> None:
        dlg = ConnectionDialog(self)
        if dlg.exec() == ConnectionDialog.DialogCode.Accepted:
            entry = dlg.get_entry()
            if entry:
                self.connections.append(entry)
                storage.save_connections(self.connections)
                self._push_connections()
                self._rebuild_cards()
                tracer().info(tr('msg_added', name=entry.name))
                self.statusBar().showMessage(tr('msg_added', name=entry.name), 3000)

    def _on_edit(self, entry: ConnectionEntry) -> None:
        dlg = ConnectionDialog(self, entry=entry)
        if dlg.exec() == ConnectionDialog.DialogCode.Accepted:
            updated = dlg.get_entry()
            if updated:
                idx = next(i for i, e in enumerate(self.connections) if e.id == updated.id)
                self.connections[idx] = updated
                storage.save_connections(self.connections)
                self._push_connections()
                self._rebuild_cards()
                tracer().info(tr('msg_updated', name=updated.name))
                self.statusBar().showMessage(tr('msg_updated', name=updated.name), 3000)

    def _on_delete(self, entry: ConnectionEntry) -> None:
        if entry.id in self._running_ids:
            QMessageBox.warning(
                self, tr('dlg_delete_title'),
                tr('err_del_running', name=entry.name),
            )
            return
        reply = QMessageBox.question(
            self, tr('dlg_delete_title'),
            tr('dlg_delete_msg', name=entry.name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.connections = [e for e in self.connections if e.id != entry.id]
            storage.save_connections(self.connections)
            self._push_connections()
            self._rebuild_cards()
            tracer().warn(tr('msg_deleted', name=entry.name))
            self.statusBar().showMessage(tr('msg_deleted', name=entry.name), 3000)

    # ── Batch start / stop ────────────────────────────────────────

    def _start_from_card(self, entry: ConnectionEntry, mode: str) -> None:
        """Start a single connection from its card. mode: 'default'|'tws'|'gateway'."""
        if mode == "default":
            is_gw = entry.default_mode == "gateway"
        else:
            is_gw = mode == "gateway"
        self._start_one(entry, is_gateway=is_gw)

    def _start_checked(self, mode: str) -> None:
        """mode: 'tws' | 'gateway' | 'default'."""
        entries = self._checked_entries()
        if not entries:
            tracer().warn(tr('msg_none_checked'))
            self.statusBar().showMessage(tr('msg_none_checked'), 3000)
            return
        for entry in entries:
            if mode == "default":
                is_gw = entry.default_mode == "gateway"
            else:
                is_gw = mode == "gateway"
            self._start_one(entry, is_gateway=is_gw)

    def _stop_checked(self) -> None:
        entries = self._checked_entries()
        if not entries:
            tracer().warn(tr('msg_none_checked'))
            self.statusBar().showMessage(tr('msg_none_checked'), 3000)
            return
        for entry in entries:
            self._stop_one(entry)

    def _start_one(self, entry: ConnectionEntry, is_gateway: bool) -> None:
        kind = tr('btn_gateway') if is_gateway else tr('btn_tws')
        if self._monitor.is_active(entry.id):
            tracer().warn(tr('err_already_run', name=entry.name, pid=0))
            return

        card = self._cards.get(entry.id)
        if card:
            card.set_status("starting")
        tracer().info(tr('msg_starting', kind=kind, name=entry.name))
        self.statusBar().showMessage(tr('msg_starting', kind=kind, name=entry.name))

        bridge = self._autofill_bridge

        def _on_autofill(ok: bool, msg: str) -> None:
            bridge.message.emit(msg)

        try:
            if is_gateway:
                handle = launcher.launch_gateway(entry, self.settings, on_autofill_done=_on_autofill)
            else:
                handle = launcher.launch_tws(entry, self.settings, on_autofill_done=_on_autofill)
        except Exception as exc:
            if card:
                card.set_status("stopped")
            tracer().error(f"{tr('msg_start_err')} '{entry.name}': {exc}")
            self.statusBar().showMessage(tr('msg_start_err'), 4000)
            return

        self._handles[entry.id] = handle
        self._monitor.add_handle(entry.id, handle)
        self._monitor.start_learning(entry.id)
        tracer().info(tr('msg_started', kind=kind, name=entry.name, pid=handle.pid))
        self.statusBar().showMessage(
            tr('msg_started', kind=kind, name=entry.name, pid=handle.pid), 5000
        )

    def _stop_one(self, entry: ConnectionEntry) -> None:
        for inst in self._instances_for(entry):
            terminate_pid(inst.pid)
        handle = self._handles.pop(entry.id, None)
        if handle:
            self._monitor.remove_handle(entry.id)
            handle.terminate()
        self._running_ids.discard(entry.id)
        self._run_types.pop(entry.id, None)
        card = self._cards.get(entry.id)
        if card:
            card.set_status("stopped")
        tracer().warn(tr('msg_stopped', name=entry.name))
        self.statusBar().showMessage(tr('msg_stopped', name=entry.name), 3000)
        self._update_run_count()
        self._monitor.request_check()

    # ── Misc slots ────────────────────────────────────────────────

    def _on_settings(self) -> None:
        dlg = SettingsDialog(self.settings, self)
        if dlg.exec() == SettingsDialog.DialogCode.Accepted:
            updated = dlg.get_settings()
            if updated:
                self.settings = updated
                storage.save_settings(updated)
                self._push_connections()
                self._rebuild_cards()
                tracer().info(tr('msg_settings_ok'))
                self.statusBar().showMessage(tr('msg_settings_ok'), 3000)

    def _on_help(self) -> None:
        open_help_in_browser()

    def _on_about(self) -> None:
        AboutDialog(self).exec()

    # ── Window events ─────────────────────────────────────────────

    def closeEvent(self, event) -> None:
        active = list(self._running_ids)
        if active:
            choice = self._confirm_close_with_running(active)
            if choice == "stay":
                event.ignore()
                return
            if choice == "close_all":
                for entry in [e for e in self.connections if e.id in active]:
                    self._stop_one(entry)
                tracer().info("Closing: stopped all running instances.")
            # choice == "leave": exit the app, leave TWS/Gateway running.
        self._monitor.stop()
        event.accept()

    def _confirm_close_with_running(self, active: list[str]) -> str:
        """Close-confirmation dialog when instances are still running.

        Returns 'close_all' | 'leave' | 'stay'. Custom dialog (not QMessageBox)
        so the button order is exact: "Exit anyway" sits on the far left, the
        primary actions on the right.
        """
        names = [e.name for e in self.connections if e.id in active]
        dlg = QDialog(self)
        dlg.setWindowTitle(tr('dlg_active_title'))
        dlg.setModal(True)
        dlg.setMinimumWidth(400)

        v = QVBoxLayout(dlg)
        v.setContentsMargins(20, 18, 20, 16)
        v.setSpacing(14)

        msg = QLabel(
            tr('dlg_active_body', count=len(active)) + "\n" +
            "\n".join(f"  • {n}" for n in names) +
            "\n\n" + tr('dlg_active_quit')
        )
        msg.setWordWrap(True)
        v.addWidget(msg)

        row = QHBoxLayout()
        row.setSpacing(8)
        btn_leave = QPushButton(tr('dlg_active_leave'))
        btn_close_all = QPushButton(tr('dlg_active_close_all'))
        btn_stay = QPushButton(tr('btn_cancel'))
        btn_close_all.setStyleSheet(START_BTN_CSS)   # primary
        btn_close_all.setMinimumHeight(30)
        btn_stay.setMinimumHeight(30)
        btn_leave.setMinimumHeight(30)
        # "Exit anyway" far left; primary actions grouped on the right.
        row.addWidget(btn_leave)
        row.addStretch()
        row.addWidget(btn_close_all)
        row.addWidget(btn_stay)
        v.addLayout(row)

        result = {"v": "stay"}
        btn_leave.clicked.connect(lambda: (result.update(v="leave"), dlg.accept()))
        btn_close_all.clicked.connect(lambda: (result.update(v="close_all"), dlg.accept()))
        btn_stay.clicked.connect(dlg.reject)
        btn_stay.setDefault(True)   # safe default; Esc / window-X also = stay
        dlg.exec()
        return result["v"]
