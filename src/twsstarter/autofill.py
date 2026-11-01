"""
Automated login form filler for the TWS / IB Gateway login dialog.

Detects whether the TWS or Gateway dialog is open by window title,
then fills username, password and selects the trading mode using
relative coordinates (fraction of window width/height).

Windows uses the Win32 API + pyautogui. Linux sends synthetic X11 events to the
login window (XWayland under Wayland) through x11input; there only TWS is
supported so far (the Gateway dialog layout has not been measured on Linux).
"""
from __future__ import annotations

import logging
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

_WIN32 = sys.platform == "win32"

if _WIN32:
    import pyautogui
    import win32clipboard
    import win32con
    import win32gui
    import win32process

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.04
else:
    from twsstarter import x11input

logger = logging.getLogger(__name__)

# Minimum size (px) a window must have to be accepted as a real login dialog —
# filters out the install4j splash/loader that briefly shares the same title.
_MIN_LOGIN_W = 480
_MIN_LOGIN_H = 300

_LOG_FILE = Path.home() / ".twsstarter" / "autofill.log"

# Keyboard, mouse and clipboard are global: when several instances are started
# at once, their autofill threads must not type concurrently (usernames would
# get concatenated). The lock serializes the interaction phase; every login
# window is claimed by exactly one thread so no window is filled twice.
_FILL_LOCK = threading.Lock()
_claimed_hwnds: set[int] = set()
# Pause after submitting, still holding the lock, so the dialog processes the
# Enter before the next thread takes the focus.
_SUBMIT_GRACE = 1.5


def _log(msg: str) -> None:
    """Append a timestamped line to the autofill log (best-effort)."""
    try:
        _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        with _LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(f"{ts}  {msg}\n")
    except Exception:
        pass
    logger.info(msg)

# ── Relative positions — TWS login dialog ────────────────────────────────
# Measured on the standard TWS Login dialog (~1006 × 586 px).
_TWS_POS: dict[str, tuple[float, float]] = {
    "tab_live":   (0.578, 0.384),
    "tab_paper":  (0.668, 0.384),
    "username":   (0.720, 0.493),
    "password":   (0.720, 0.560),
    "btn_login":  (0.720, 0.714),
}

# ── Relative positions — IB Gateway / IBKR Gateway dialog ────────────────
# Measured from screenshot: window ~805 × 517 px.
# Trading-mode toggle buttons are in a 2-segment bar.
# Username / Password / Login button are centered in the dialog.
_GW_POS: dict[str, tuple[float, float]] = {
    "tab_live":   (0.393, 0.424),   # "Live Trading"  left segment
    "tab_paper":  (0.626, 0.424),   # "Paper Trading" right segment
    "username":   (0.513, 0.541),
    "password":   (0.513, 0.619),
    "btn_login":  (0.513, 0.756),   # "Log In" / "Paper Log In"
}

# ── Login-window detection ───────────────────────────────────────────────
# Gateway login: the window title is the product name and is NOT localized.
_GW_TITLES = {"IB Gateway", "IBKR Gateway"}

# TWS login: the window title IS localized ("Login" in English, "Anmelden" in
# German, ...). We match a set of known titles (case-insensitive) for a fast
# path and, as a language-independent fallback, accept the Java/Swing top-level
# window class of the TWS login frame — so autofill also works in languages
# whose title is not listed here.
_TWS_LOGIN_TITLES = {
    "login",      # English
    "anmelden",   # German
}
_JAVA_FRAME_CLASS_PREFIX = "SunAwt"   # e.g. SunAwtFrame / SunAwtDialog


def _window_class(hwnd: int) -> str:
    try:
        return win32gui.GetClassName(hwnd) or ""
    except Exception:
        return ""


def _is_login_window(hwnd: int, is_gateway: bool) -> bool:
    """Whether `hwnd` is the login dialog we launched, independent of UI language.

    We already know from the caller whether TWS or Gateway was started, so the
    localized title is only a hint — for TWS we also accept the Java frame class.
    """
    title = win32gui.GetWindowText(hwnd)
    if is_gateway:
        return title in _GW_TITLES
    # TWS: known localized title, or any Java/Swing frame (but never the Gateway).
    if title in _GW_TITLES:
        return False
    if title.strip().lower() in _TWS_LOGIN_TITLES:
        return True
    return _window_class(hwnd).startswith(_JAVA_FRAME_CLASS_PREFIX)


# ── Helpers ───────────────────────────────────────────────────────────────

def _win_size(hwnd: int) -> tuple[int, int]:
    rect = win32gui.GetWindowRect(hwnd)
    return rect[2] - rect[0], rect[3] - rect[1]


def _dump_visible_titles() -> None:
    """Log all visible top-level window titles (diagnostic)."""
    titles: list[str] = []

    def _cb(hwnd: int, _) -> None:
        if win32gui.IsWindowVisible(hwnd):
            t = win32gui.GetWindowText(hwnd)
            if t.strip():
                w, h = _win_size(hwnd)
                titles.append(f"'{t}' ({w}x{h})")

    win32gui.EnumWindows(_cb, None)
    _log("visible windows: " + " | ".join(titles))


def _find_login_window(is_gateway: bool, timeout: float) -> Optional[tuple[int, str]]:
    """Poll until a visible, sufficiently large TWS/Gateway login window appears.

    The install4j launcher (ibgateway.exe) shows a small splash that can briefly
    carry the same title, so we require a minimum window size before accepting
    it. Returns (hwnd, title) or None on timeout.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        candidates: list[tuple[int, str, int, int]] = []

        with _FILL_LOCK:
            claimed = set(_claimed_hwnds)

        def _cb(hwnd: int, _) -> None:
            if hwnd not in claimed and win32gui.IsWindowVisible(hwnd):
                if _is_login_window(hwnd, is_gateway):
                    title = win32gui.GetWindowText(hwnd)
                    w, h = _win_size(hwnd)
                    candidates.append((hwnd, title, w, h))

        win32gui.EnumWindows(_cb, None)

        for hwnd, title, w, h in candidates:
            if w >= _MIN_LOGIN_W and h >= _MIN_LOGIN_H:
                _log(f"login window accepted: '{title}' hwnd={hwnd} size={w}x{h}")
                return hwnd, title
            _log(f"login window too small (splash?): '{title}' size={w}x{h} — waiting")
        time.sleep(1.0)
    return None


def _ensure_foreground(hwnd: int) -> bool:
    """Bring window to front and report whether it actually is foreground now."""
    _bring_to_front(hwnd)
    time.sleep(0.15)
    fg = win32gui.GetForegroundWindow()
    return fg == hwnd


def _bring_to_front(hwnd: int) -> None:
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    except Exception:
        pass
    try:
        import ctypes
        fg_thread = ctypes.windll.user32.GetWindowThreadProcessId(
            win32gui.GetForegroundWindow(), None
        )
        our_thread = ctypes.windll.kernel32.GetCurrentThreadId()
        if fg_thread != our_thread:
            ctypes.windll.user32.AttachThreadInput(fg_thread, our_thread, True)
        win32gui.SetForegroundWindow(hwnd)
        if fg_thread != our_thread:
            ctypes.windll.user32.AttachThreadInput(fg_thread, our_thread, False)
    except Exception:
        pass


def _click_rel(rect: tuple[int, int, int, int], rx: float, ry: float) -> None:
    w = rect[2] - rect[0]
    h = rect[3] - rect[1]
    x = rect[0] + int(w * rx)
    y = rect[1] + int(h * ry)
    pyautogui.click(x, y)


def _paste(text: str) -> None:
    """Clear the focused field and paste text via clipboard (Unicode-safe)."""
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, text)
    finally:
        win32clipboard.CloseClipboard()
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.05)
    pyautogui.hotkey("ctrl", "v")


# ── Linux (X11 / XWayland) ────────────────────────────────────────────────
# Relative positions inside the client area (no window decoration), measured on
# the Linux TWS login dialog (990 × 513 px). Switching to Paper shifts the form
# down a few pixels; the username y lies inside the field in both modes.
_TWS_POS_X11: dict[str, tuple[float, float]] = {
    "tab_live":   (0.584, 0.326),
    "tab_paper":  (0.680, 0.326),
    "username":   (0.722, 0.435),
}

def _x11_is_login(w: "x11input.XWindow", pid: Optional[int]) -> bool:
    """TWS login dialog: the window of the launched process (if known), with a
    known localized title or the TWS client window class."""
    if pid is not None and w.pid is not None and w.pid != pid:
        return False
    if w.title in _GW_TITLES or "Interactive Brokers" in w.title:
        return False          # Gateway, or the logged-in TWS main window
    return (w.title.strip().lower() in _TWS_LOGIN_TITLES
            or "jclient" in w.wm_class.lower())


def _x11_find_login(pid: Optional[int], timeout: float) -> Optional["x11input.XWindow"]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        with _FILL_LOCK:
            claimed = set(_claimed_hwnds)
        for w in x11input.list_windows():
            if w.wid in claimed or not _x11_is_login(w, pid):
                continue
            if w.width >= _MIN_LOGIN_W and w.height >= _MIN_LOGIN_H:
                _log(f"login window accepted: '{w.title}' wid={w.wid} pid={w.pid} "
                     f"class={w.wm_class} size={w.width}x{w.height}")
                return w
        time.sleep(1.0)
    return None


def _x11_fill(w: "x11input.XWindow", username: str, password: str,
              paper_trading: bool) -> None:
    """Fill and submit one TWS login dialog. Caller must hold _FILL_LOCK.

    Clicks and keys are synthetic events addressed to this window only, so the
    window need not be visible or focused and nothing reaches other windows.
    """
    time.sleep(1.0)                       # let the dialog finish rendering
    w = x11input.get_window(w.wid) or w   # current size
    _log(f"window size={w.width}x{w.height}")

    tab_key = "tab_paper" if paper_trading else "tab_live"
    _log(f"click {tab_key}")
    x11input.click(w, *_TWS_POS_X11[tab_key])
    time.sleep(0.8)

    _log("click username; typing username")
    x11input.click(w, *_TWS_POS_X11["username"])
    time.sleep(0.3)
    x11input.press(w, "a", ctrl=True)
    x11input.type_text(w, username)
    time.sleep(0.3)

    _log("press Tab; typing password")
    x11input.press(w, "Tab")
    time.sleep(0.3)
    x11input.press(w, "a", ctrl=True)
    x11input.type_text(w, password)
    time.sleep(0.35)

    _log("press Enter (submit)")
    x11input.press(w, "Return")
    _log("=== autofill done ===")


def _x11_fill_login(username: str, password: str, paper_trading: bool,
                    timeout: int, pid: Optional[int]) -> str:
    """Linux flow of fill_login; returns the success message or raises."""
    deadline = time.monotonic() + timeout
    while True:
        w = _x11_find_login(pid, max(0.0, deadline - time.monotonic()))
        if w is None:
            raise TimeoutError(f"Login window not found (timeout after {timeout}s).")
        with _FILL_LOCK:
            live = {win.wid for win in x11input.list_windows()}
            _claimed_hwnds.intersection_update(live)
            if w.wid in _claimed_hwnds or w.wid not in live:
                _log(f"window wid={w.wid} already taken — searching again")
                continue
            _claimed_hwnds.add(w.wid)
            _x11_fill(w, username, password, paper_trading)
            time.sleep(_SUBMIT_GRACE)
        return f"Credentials submitted ({w.title})."


# ── Main autofill logic ────────────────────────────────────────────────────

def _fill_window(
    hwnd: int,
    title: str,
    username: str,
    password: str,
    paper_trading: bool,
    is_gateway: bool,
) -> None:
    """Fill and submit one login dialog. Caller must hold _FILL_LOCK."""
    pos = _GW_POS if is_gateway else _TWS_POS
    _log(f"matched '{title}' hwnd={hwnd} gateway={is_gateway}")

    # The install4j Gateway loader keeps rebuilding the dialog for a moment;
    # give it time to fully render before interacting.
    fg = _ensure_foreground(hwnd)
    settle = 2.5 if is_gateway else 1.0
    _log(f"foreground={fg}; settling {settle}s")
    time.sleep(settle)

    rect = win32gui.GetWindowRect(hwnd)
    w, h = rect[2] - rect[0], rect[3] - rect[1]
    _log(f"window rect={rect} size={w}x{h}")

    # ── 1. Select Live / Paper tab ─────────────────────────────────────
    _ensure_foreground(hwnd)
    tab_key = "tab_paper" if paper_trading else "tab_live"
    tx, ty = pos[tab_key]
    _log(f"click {tab_key} at rel=({tx},{ty})")
    _click_rel(rect, tx, ty)
    time.sleep(0.6)

    # ── 2. Username ────────────────────────────────────────────────────
    _ensure_foreground(hwnd)
    ux, uy = pos["username"]
    _log(f"click username at rel=({ux},{uy}); pasting username")
    _click_rel(rect, ux, uy)
    time.sleep(0.3)
    _paste(username)
    time.sleep(0.3)

    # ── 3. Password via Tab navigation ─────────────────────────────────
    # Tabbing from the username field is robust against layout shifts
    # (the Live/Paper toggle changes the dialog height, so a fixed
    # password coordinate may land on "More Options" instead).
    _log("press Tab; pasting password")
    pyautogui.press("tab")
    time.sleep(0.3)
    _paste(password)
    time.sleep(0.35)

    # ── 4. Submit with Enter ───────────────────────────────────────────
    _log("press Enter (submit)")
    pyautogui.press("enter")
    _log("=== autofill done ===")


def fill_login(
    username: str,
    password: str,
    paper_trading: bool,
    is_gateway: bool,
    timeout: int = 90,
    on_done: Optional[Callable[[bool, str], None]] = None,
    pid: Optional[int] = None,
    on_submitted: Optional[Callable[[int], None]] = None,
) -> None:
    """Wait for the login window and fill credentials. Runs in a daemon thread.

    `is_gateway` is passed by the caller (it knows whether TWS or Gateway was
    launched), so detection does not depend on the localized window title.
    `pid` (Linux) restricts detection to the windows of the launched process.
    `on_submitted` receives the PID of the filled login window, so the caller
    can verify which account that process logs into.
    """
    if not _WIN32:
        if is_gateway or not x11input.available():
            if on_done:
                on_done(False, "Autofill not supported here (Linux: TWS on X11/XWayland only).")
            return
        try:
            _log(f"=== autofill start (x11, paper={paper_trading}, pid={pid}, "
                 f"timeout={timeout}s) ===")
            msg = _x11_fill_login(username, password, paper_trading, timeout, pid)
            if on_done:
                on_done(True, msg)
        except Exception as exc:
            _log(f"ABORT: {exc!r}")
            if on_done:
                on_done(False, f"Autofill error: {exc}")
        return
    try:
        _log(f"=== autofill start (gateway={is_gateway}, paper={paper_trading}, "
             f"timeout={timeout}s) ===")
        # Give the launcher a moment, then snapshot what is on screen.
        time.sleep(3.0)
        _dump_visible_titles()
        deadline = time.monotonic() + timeout

        while True:
            result = _find_login_window(is_gateway, max(0.0, deadline - time.monotonic()))
            if not result:
                msg = f"Login window not found (timeout after {timeout}s)."
                _log("ABORT: " + msg)
                if on_done:
                    on_done(False, msg)
                return

            hwnd, title = result
            with _FILL_LOCK:
                # Drop handles of closed windows; another thread may have
                # claimed this window while we were waiting for the lock.
                _claimed_hwnds.intersection_update(
                    {h for h in _claimed_hwnds if win32gui.IsWindow(h)})
                if hwnd in _claimed_hwnds or not win32gui.IsWindow(hwnd):
                    _log(f"window hwnd={hwnd} already taken — searching again")
                    continue
                _claimed_hwnds.add(hwnd)
                _fill_window(hwnd, title, username, password, paper_trading, is_gateway)
                login_pid = win32process.GetWindowThreadProcessId(hwnd)[1]
                time.sleep(_SUBMIT_GRACE)
            break

        if on_submitted:
            on_submitted(login_pid)

        if on_done:
            on_done(True, f"Credentials submitted ({title}).")

    except Exception as exc:
        _log(f"ERROR: {exc!r}")
        logger.exception("Autofill error")
        if on_done:
            on_done(False, f"Autofill error: {exc}")


def start_thread(
    username: str,
    password: str,
    paper_trading: bool,
    is_gateway: bool,
    timeout: int = 90,
    on_done: Optional[Callable[[bool, str], None]] = None,
    pid: Optional[int] = None,
    on_submitted: Optional[Callable[[int], None]] = None,
) -> threading.Thread:
    """Start autofill in a background daemon thread and return it."""
    t = threading.Thread(
        target=fill_login,
        args=(username, password, paper_trading, is_gateway, timeout, on_done, pid,
              on_submitted),
        daemon=True,
        name="TWSAutofill",
    )
    t.start()
    return t
