"""Minimal X11 window + input layer for Linux autofill (ctypes, libX11).

TWS and IB Gateway are Java/Swing applications and run as X11 clients — under a
Wayland desktop via XWayland — so they can be found through the EWMH client list.
libX11 is used directly instead of python-xlib: python-xlib rejects the
Xauthority entry Mutter writes for XWayland (it has an empty display number),
libX11 treats it as a wildcard.

Input is sent as synthetic X events (XSendEvent) straight to the target window,
not as global fake input (XTEST). GNOME routes XTEST through its remote-control
portal, which needs an interactive approval and replays events that were not
yet allowed. Synthetic events stay inside the X server, need no approval, reach
only the addressed window (a password can never land elsewhere) and work even
when the window is covered. Java/AWT accepts them.

Text is typed key by key with the keycode and modifier state the current
keyboard layout assigns to each character. No clipboard is involved and the
keyboard mapping is never changed.

Every public function opens its own short-lived display connection, so callers
in different threads never share Xlib state.
"""
from __future__ import annotations

import ctypes
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, Optional

_c = ctypes
_Display = _c.c_void_p
_Window = _c.c_ulong
_Atom = _c.c_ulong
_KeySym = _c.c_ulong

_XA_CARDINAL = 6
_XA_STRING = 31
_XA_WINDOW = 33
_IS_VIEWABLE = 2

# Event types / masks / modifier state bits (X.h)
_KEY_PRESS, _KEY_RELEASE, _BUTTON_PRESS, _BUTTON_RELEASE = 2, 3, 4, 5
_KEY_PRESS_MASK, _KEY_RELEASE_MASK = 1 << 0, 1 << 1
_BUTTON_PRESS_MASK, _BUTTON_RELEASE_MASK = 1 << 2, 1 << 3
_SHIFT_MASK, _CONTROL_MASK, _BUTTON1_MASK = 1 << 0, 1 << 2, 1 << 8


class _XWindowAttributes(_c.Structure):
    _fields_ = [
        ("x", _c.c_int), ("y", _c.c_int), ("width", _c.c_int), ("height", _c.c_int),
        ("border_width", _c.c_int), ("depth", _c.c_int), ("visual", _c.c_void_p),
        ("root", _Window), ("class_", _c.c_int), ("bit_gravity", _c.c_int),
        ("win_gravity", _c.c_int), ("backing_store", _c.c_int),
        ("backing_planes", _c.c_ulong), ("backing_pixel", _c.c_ulong),
        ("save_under", _c.c_int), ("colormap", _c.c_ulong),
        ("map_installed", _c.c_int), ("map_state", _c.c_int),
        ("all_event_masks", _c.c_long), ("your_event_mask", _c.c_long),
        ("do_not_propagate_mask", _c.c_long), ("override_redirect", _c.c_int),
        ("screen", _c.c_void_p),
    ]


class _XInputEvent(_c.Structure):
    """Common layout of XKeyEvent and XButtonEvent (last field differs only by name)."""
    _fields_ = [
        ("type", _c.c_int), ("serial", _c.c_ulong), ("send_event", _c.c_int),
        ("display", _Display), ("window", _Window), ("root", _Window),
        ("subwindow", _Window), ("time", _c.c_ulong),
        ("x", _c.c_int), ("y", _c.c_int), ("x_root", _c.c_int), ("y_root", _c.c_int),
        ("state", _c.c_uint), ("detail", _c.c_uint),   # keycode / button
        ("same_screen", _c.c_int),
    ]


class _XEvent(_c.Union):
    _fields_ = [("input", _XInputEvent), ("pad", _c.c_long * 24)]


class _XClassHint(_c.Structure):
    _fields_ = [("res_name", _c.c_char_p), ("res_class", _c.c_char_p)]


class _XModifierKeymap(_c.Structure):
    _fields_ = [("max_keypermod", _c.c_int), ("modifiermap", _c.POINTER(_c.c_ubyte))]


_x11 = None


def _lib():
    """Load libX11 once and declare the signatures used."""
    global _x11
    if _x11 is None:
        x = _c.CDLL("libX11.so.6")
        x.XInitThreads()
        x.XOpenDisplay.restype = _Display
        x.XOpenDisplay.argtypes = [_c.c_char_p]
        x.XCloseDisplay.argtypes = [_Display]
        x.XDefaultRootWindow.restype = _Window
        x.XDefaultRootWindow.argtypes = [_Display]
        x.XInternAtom.restype = _Atom
        x.XInternAtom.argtypes = [_Display, _c.c_char_p, _c.c_int]
        x.XGetWindowProperty.argtypes = [
            _Display, _Window, _Atom, _c.c_long, _c.c_long, _c.c_int, _Atom,
            _c.POINTER(_Atom), _c.POINTER(_c.c_int), _c.POINTER(_c.c_ulong),
            _c.POINTER(_c.c_ulong), _c.POINTER(_c.c_void_p)]
        x.XFree.argtypes = [_c.c_void_p]
        x.XGetWindowAttributes.argtypes = [_Display, _Window, _c.POINTER(_XWindowAttributes)]
        x.XTranslateCoordinates.argtypes = [
            _Display, _Window, _Window, _c.c_int, _c.c_int,
            _c.POINTER(_c.c_int), _c.POINTER(_c.c_int), _c.POINTER(_Window)]
        x.XGetClassHint.argtypes = [_Display, _Window, _c.POINTER(_XClassHint)]
        x.XSendEvent.argtypes = [_Display, _Window, _c.c_int, _c.c_long, _c.POINTER(_XEvent)]
        x.XSync.argtypes = [_Display, _c.c_int]
        x.XStringToKeysym.restype = _KeySym
        x.XStringToKeysym.argtypes = [_c.c_char_p]
        x.XKeysymToKeycode.restype = _c.c_ubyte
        x.XKeysymToKeycode.argtypes = [_Display, _KeySym]
        x.XDisplayKeycodes.argtypes = [_Display, _c.POINTER(_c.c_int), _c.POINTER(_c.c_int)]
        x.XGetKeyboardMapping.restype = _c.POINTER(_KeySym)
        x.XGetKeyboardMapping.argtypes = [_Display, _c.c_ubyte, _c.c_int, _c.POINTER(_c.c_int)]
        x.XGetModifierMapping.restype = _c.POINTER(_XModifierKeymap)
        x.XGetModifierMapping.argtypes = [_Display]
        x.XFreeModifiermap.argtypes = [_c.POINTER(_XModifierKeymap)]
        _x11 = x
    return _x11


def available() -> bool:
    """Whether an X11 display (e.g. XWayland) can be opened."""
    try:
        with _display():
            return True
    except Exception:
        return False


@contextmanager
def _display() -> Iterator[int]:
    x = _lib()
    d = x.XOpenDisplay(None)
    if not d:
        raise RuntimeError("Cannot open X11 display (is DISPLAY set?)")
    try:
        yield d
    finally:
        x.XCloseDisplay(d)


# ── Windows ────────────────────────────────────────────────────────────────

@dataclass
class XWindow:
    wid: int
    title: str
    wm_class: str    # "res_name.res_class", e.g. "install4j-jclient-Launcher.install4j-jclient-Launcher"
    pid: Optional[int]
    x: int           # absolute position of the client area (without decoration)
    y: int
    width: int
    height: int


def _prop(d, wid: int, name: bytes, typ: int) -> Optional[bytes]:
    """Raw value of a window property (all items concatenated), or None."""
    x = _lib()
    atom = x.XInternAtom(d, name, False)
    rtype, fmt = _Atom(), _c.c_int()
    n, after, data = _c.c_ulong(), _c.c_ulong(), _c.c_void_p()
    if x.XGetWindowProperty(d, wid, atom, 0, 1 << 16, False, typ, _c.byref(rtype),
                            _c.byref(fmt), _c.byref(n), _c.byref(after),
                            _c.byref(data)) != 0 or not data.value:
        return None
    try:
        # 32-bit format items are stored as C longs by Xlib.
        size = {8: 1, 16: 2, 32: _c.sizeof(_c.c_long)}.get(fmt.value, 1) * n.value
        return _c.string_at(data.value, size)
    finally:
        x.XFree(data)


def _longs(raw: Optional[bytes]) -> list[int]:
    if not raw:
        return []
    arr = (_c.c_ulong * (len(raw) // _c.sizeof(_c.c_ulong))).from_buffer_copy(raw)
    return list(arr)


def _describe(d, wid: int) -> Optional[XWindow]:
    x = _lib()
    attrs = _XWindowAttributes()
    if not x.XGetWindowAttributes(d, wid, _c.byref(attrs)) or attrs.map_state != _IS_VIEWABLE:
        return None
    utf8 = x.XInternAtom(d, b"UTF8_STRING", False)
    raw = _prop(d, wid, b"_NET_WM_NAME", utf8) or _prop(d, wid, b"WM_NAME", _XA_STRING)
    title = raw.decode("utf-8", "replace") if raw else ""
    hint = _XClassHint()
    wm_class = ""
    if x.XGetClassHint(d, wid, _c.byref(hint)):
        wm_class = f"{(hint.res_name or b'').decode()}.{(hint.res_class or b'').decode()}"
    pid = (_longs(_prop(d, wid, b"_NET_WM_PID", _XA_CARDINAL)) or [None])[0]
    ax, ay, child = _c.c_int(), _c.c_int(), _Window()
    x.XTranslateCoordinates(d, wid, x.XDefaultRootWindow(d), 0, 0,
                            _c.byref(ax), _c.byref(ay), _c.byref(child))
    return XWindow(wid, title, wm_class, pid, ax.value, ay.value, attrs.width, attrs.height)


def _client_ids(d) -> list[int]:
    x = _lib()
    return _longs(_prop(d, x.XDefaultRootWindow(d), b"_NET_CLIENT_LIST", _XA_WINDOW))


def list_windows() -> list[XWindow]:
    """Visible top-level client windows (EWMH _NET_CLIENT_LIST)."""
    with _display() as d:
        return [w for w in (_describe(d, wid) for wid in _client_ids(d)) if w is not None]


def get_window(wid: int) -> Optional[XWindow]:
    """Current state of one window, or None if it is gone / unmapped."""
    with _display() as d:
        return _describe(d, wid) if wid in _client_ids(d) else None


# ── Input (synthetic events) ──────────────────────────────────────────────

def _deepest(d, wid: int, px: int, py: int) -> tuple[int, int, int]:
    """Innermost child window of `wid` under (px, py) and the point in its
    coordinates. Java/AWT handles input on its inner content window, not on the
    top-level frame."""
    x = _lib()
    cur = wid
    while True:
        ox, oy, child = _c.c_int(), _c.c_int(), _Window()
        x.XTranslateCoordinates(d, cur, cur, px, py, _c.byref(ox), _c.byref(oy), _c.byref(child))
        if not child.value:
            return cur, px, py
        x.XTranslateCoordinates(d, cur, child.value, px, py,
                                _c.byref(ox), _c.byref(oy), _c.byref(_Window()))
        cur, px, py = child.value, ox.value, oy.value


def _send(d, target: int, typ: int, mask: int, detail: int, state: int,
          xy: tuple[int, int] = (0, 0), root_xy: tuple[int, int] = (0, 0)) -> None:
    x = _lib()
    ev = _XEvent()
    e = ev.input
    e.type, e.send_event, e.window = typ, True, target
    e.root = x.XDefaultRootWindow(d)
    e.x, e.y = xy
    e.x_root, e.y_root = root_xy
    e.state, e.detail, e.same_screen = state, detail, True
    x.XSendEvent(d, target, True, mask, _c.byref(ev))


def click(w: XWindow, rx: float, ry: float) -> None:
    """Left click at a point given relative to the window's client area."""
    x = _lib()
    px, py = int(w.width * rx), int(w.height * ry)
    with _display() as d:
        target, tx, ty = _deepest(d, w.wid, px, py)
        root_xy = (w.x + px, w.y + py)
        _send(d, target, _BUTTON_PRESS, _BUTTON_PRESS_MASK, 1, 0, (tx, ty), root_xy)
        x.XSync(d, False)
        time.sleep(0.05)
        _send(d, target, _BUTTON_RELEASE, _BUTTON_RELEASE_MASK, 1, _BUTTON1_MASK,
              (tx, ty), root_xy)
        x.XSync(d, False)


def _key_target(d, w: XWindow) -> int:
    # Java routes keys from its inner content window to the focused component.
    return _deepest(d, w.wid, w.width // 2, w.height // 2)[0]


def _tap(d, target: int, keycode: int, state: int) -> None:
    x = _lib()
    _send(d, target, _KEY_PRESS, _KEY_PRESS_MASK, keycode, state)
    _send(d, target, _KEY_RELEASE, _KEY_RELEASE_MASK, keycode, state)
    x.XSync(d, False)
    time.sleep(0.02)


def press(w: XWindow, key: str, ctrl: bool = False) -> None:
    """Press a key by X keysym name (e.g. "Tab", "Return", or "a" with ctrl)."""
    x = _lib()
    with _display() as d:
        kc = x.XKeysymToKeycode(d, x.XStringToKeysym(key.encode()))
        if not kc:
            raise ValueError(f"No keycode for {key!r}")
        _tap(d, _key_target(d, w), kc, _CONTROL_MASK if ctrl else 0)


def _level3_mask(d) -> int:
    """Modifier bit carrying ISO_Level3_Shift (AltGr), usually Mod5."""
    x = _lib()
    altgr = x.XKeysymToKeycode(d, x.XStringToKeysym(b"ISO_Level3_Shift"))
    mm = x.XGetModifierMapping(d)
    try:
        per = mm.contents.max_keypermod
        for mod in range(8):
            if altgr and any(mm.contents.modifiermap[mod * per + i] == altgr
                             for i in range(per)):
                return 1 << mod
        return 0
    finally:
        x.XFreeModifiermap(mm)


def type_text(w: XWindow, text: str) -> None:
    """Type `text` into the focused component of `w`, layout-independently.

    Only characters reachable in the current layout (plain, Shift, AltGr,
    Shift+AltGr) can be typed — this covers ASCII on common layouts, which is all
    the TWS/Gateway login fields accept. Anything else raises ValueError before a
    single key is sent.
    """
    x = _lib()
    with _display() as d:
        lo, hi = _c.c_int(), _c.c_int()
        x.XDisplayKeycodes(d, _c.byref(lo), _c.byref(hi))
        per = _c.c_int()
        kmap = x.XGetKeyboardMapping(d, lo.value, hi.value - lo.value + 1, _c.byref(per))
        try:
            table = {kc: [kmap[(kc - lo.value) * per.value + i] for i in range(per.value)]
                     for kc in range(lo.value, hi.value + 1)}
        finally:
            x.XFree(kmap)
        l3 = _level3_mask(d)
        # Core-mapping columns: 0 plain, 1 Shift, 4 AltGr, 5 Shift+AltGr (XKB group 1).
        levels = [(0, 0), (1, _SHIFT_MASK)]
        if l3:
            levels += [(4, l3), (5, _SHIFT_MASK | l3)]

        def lookup(ch: str) -> Optional[tuple[int, int]]:
            o = ord(ch)
            # Latin-1 keysyms equal the code point; others use the Unicode range.
            syms = {0x01000000 | o} | ({o} if o <= 0xFF else set())
            return next(((kc, state) for col, state in levels
                         for kc, ks in table.items()
                         if col < len(ks) and ks[col] in syms), None)

        keys = [lookup(ch) for ch in text]
        missing = sorted({ch for ch, k in zip(text, keys) if k is None})
        if missing:
            raise ValueError("Characters not typeable in the current keyboard layout: "
                             + ", ".join(f"U+{ord(ch):04X}" for ch in missing))
        target = _key_target(d, w)
        for kc, state in keys:
            _tap(d, target, kc, state)
