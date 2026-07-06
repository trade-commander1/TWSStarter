STYLESHEET = """
/* ── Base ──────────────────────────────────────────────── */
QMainWindow, QDialog, QWidget {
    background-color: #0f1117;
    color: #ffffff;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
}

/* ── Header bar ─────────────────────────────────────────── */
#header {
    background-color: #090c12;
    border-bottom: 1px solid #1e2235;
}

#appTitle {
    font-size: 18px;
    font-weight: 700;
    color: #3b82f6;
    letter-spacing: -0.3px;
    background: transparent;
}

#appSubtitle {
    font-size: 11px;
    color: #94a3b8;
    background: transparent;
}

/* ── Connection card ─────────────────────────────────────── */
#connectionCard {
    background-color: #151825;
    border: 1px solid #1e2235;
    border-radius: 10px;
}

#connectionCard:hover {
    border-color: #2d3f6e;
}

#connName {
    font-size: 14px;
    font-weight: 600;
    color: #f1f5f9;
    background: transparent;
}

#connUser {
    font-size: 12px;
    color: #ffffff;
    background: transparent;
}

#connPath {
    font-size: 11px;
    color: #94a3b8;
    background: transparent;
}

/* ── Buttons ─────────────────────────────────────────────── */
QPushButton {
    background-color: #1a1d2e;
    color: #ffffff;
    border: 1px solid #2d3148;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #212540;
    border-color: #3b5998;
    color: #f1f5f9;
}

QPushButton:pressed {
    background-color: #16192c;
}

QPushButton:disabled {
    color: #334155;
    border-color: #1a1d2e;
}

QPushButton#btnTWS {
    background-color: #1e3a8a;
    border: none;
    color: #bfdbfe;
    font-weight: 600;
    min-width: 62px;
}

QPushButton#btnTWS:hover {
    background-color: #1d4ed8;
    color: #ffffff;
}

QPushButton#btnTWS:pressed {
    background-color: #1e40af;
}

QPushButton#btnGW {
    background-color: #14532d;
    border: none;
    color: #bbf7d0;
    font-weight: 600;
    min-width: 72px;
}

QPushButton#btnGW:hover {
    background-color: #166534;
    color: #ffffff;
}

QPushButton#btnStop {
    background-color: transparent;
    border: 1px solid #b45309;
    color: #fbbf24;
    font-weight: 600;
}

QPushButton#btnStop:hover {
    background-color: #78350f;
    border-color: #fbbf24;
    color: #ffffff;
}

QPushButton#btnAdd {
    background-color: #3b82f6;
    border: none;
    color: #ffffff;
    font-weight: 600;
    font-size: 13px;
    padding: 8px 20px;
    border-radius: 7px;
}

QPushButton#btnAdd:hover {
    background-color: #2563eb;
}

QPushButton#btnAdd:pressed {
    background-color: #1d4ed8;
}

/* Control row: Start buttons (blue, like Add) + red Stop */
QPushButton#btnCtl {
    background-color: #3b82f6;
    border: none;
    color: #ffffff;
    font-weight: 600;
    font-size: 12px;
    padding: 0;
}
QPushButton#btnCtl:hover {
    background-color: #2563eb;
    color: #ffffff;
}
QPushButton#btnCtl:pressed {
    background-color: #1d4ed8;
}

QPushButton#btnCtlStop {
    background-color: #dc2626;
    border: none;
    color: #ffffff;
    font-weight: 600;
    font-size: 12px;
    padding: 0;
}
QPushButton#btnCtlStop:hover {
    background-color: #b91c1c;
    color: #ffffff;
}
QPushButton#btnCtlStop:pressed {
    background-color: #991b1b;
}

QPushButton#btnSettings {
    background-color: transparent;
    border: 1px solid #2d3148;
    color: #ffffff;
    padding: 6px 14px;
    border-radius: 6px;
}

QPushButton#btnSettings:hover {
    background-color: #1a1d2e;
    color: #ffffff;
    border-color: #3b5998;
}

QPushButton#btnDanger {
    background-color: transparent;
    border: 1px solid #2d3148;
    color: #ffffff;
}

QPushButton#btnDanger:hover {
    background-color: #450a0a;
    border-color: #991b1b;
    color: #fca5a5;
}

QPushButton#btnOK {
    background-color: #3b82f6;
    border: none;
    color: #ffffff;
    font-weight: 600;
    padding: 8px 24px;
}

QPushButton#btnOK:hover {
    background-color: #2563eb;
}

QPushButton#btnCancel {
    background-color: transparent;
    border: 1px solid #2d3148;
    color: #ffffff;
    padding: 8px 24px;
}

QPushButton#btnCancel:hover {
    background-color: #1a1d2e;
    color: #ffffff;
}

/* ── Icon/Tool buttons ───────────────────────────────────── */
QToolButton {
    background: transparent;
    border: none;
    color: #475569;
    border-radius: 5px;
    padding: 4px 6px;
}

QToolButton:hover {
    background: #1a1d2e;
    color: #94a3b8;
}

/* ── Line edits ──────────────────────────────────────────── */
QLineEdit {
    background-color: #151825;
    color: #ffffff;
    border: 1px solid #252840;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: #3b82f6;
    selection-color: #ffffff;
}

QLineEdit:focus {
    border-color: #3b82f6;
    background-color: #151825;
}

QLineEdit:disabled {
    color: #475569;
    background-color: #0f1117;
}

/* ── Labels ──────────────────────────────────────────────── */
QLabel {
    background: transparent;
    color: #ffffff;
}

#labelForm {
    color: #ffffff;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

#labelHint {
    color: #94a3b8;
    font-size: 11px;
}

#sectionTitle {
    font-size: 11px;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ── Group boxes ─────────────────────────────────────────── */
QGroupBox {
    border: 1px solid #1e2235;
    border-radius: 8px;
    margin-top: 14px;
    padding-top: 8px;
    font-weight: 600;
    font-size: 11px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    background: #0f1117;
}

/* ── Scroll areas ────────────────────────────────────────── */
QScrollArea {
    background: transparent;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 6px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #1e2235;
    border-radius: 3px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #3b82f6;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

/* ── Status bar ──────────────────────────────────────────── */
QStatusBar {
    background-color: #090c12;
    color: #94a3b8;
    border-top: 1px solid #1e2235;
    font-size: 11px;
    padding-left: 4px;
}

QStatusBar::item {
    border: none;
}

/* ── Dialogs ─────────────────────────────────────────────── */
QDialog {
    background-color: #0f1117;
}

/* ── Separator lines ─────────────────────────────────────── */
QFrame[frameShape="4"],
QFrame[frameShape="5"] {
    color: #1e2235;
}

/* ── Empty state label ───────────────────────────────────── */
#emptyState {
    color: #94a3b8;
    font-size: 14px;
}
"""


# ── Shared inline button styles ─────────────────────────────────────────────
# Set directly on the widgets (not via the cascading stylesheet) so nothing can
# override the blue/red background. Used by BOTH the "All" batch control row and
# the per-card start/stop buttons, so their BK/FG colors are guaranteed identical.
START_BTN_CSS = (
    "QPushButton{background:#3b82f6;color:#ffffff;border:none;"
    "border-radius:6px;font-weight:600;font-size:12px;}"
    "QPushButton:hover{background:#2563eb;}"
    "QPushButton:pressed{background:#1d4ed8;}"
)
STOP_BTN_CSS = (
    "QPushButton{background:#dc2626;color:#ffffff;border:none;"
    "border-radius:6px;font-weight:600;font-size:12px;}"
    "QPushButton:hover{background:#b91c1c;}"
    "QPushButton:pressed{background:#991b1b;}"
)
