"""Tiny national-flag icons for the language menu, painted with QPainter.

Each supported language code maps to the flag of the country whose language it
is. The flags are drawn from primitives (colour bands, a disc, stars, crosses)
rather than shipped as image assets, so there are no binary dependencies and the
icons scale crisply to the menu's icon size.

Windows does not render Unicode flag emoji (🇩🇪) as flags — it shows the two
region letters — which is why we paint real pixmaps instead.

Public API:
    flag_icon(code) -> QIcon | None   # None for unknown codes
"""
from __future__ import annotations

import math

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QIcon, QPainter, QPen, QPixmap, QPolygonF

# Render size (px). A 3:2 ratio reads well and matches most European flags; the
# menu scales the icon down as needed, and rendering larger keeps it crisp.
_W, _H = 30, 20

# Equal-width colour bands, either horizontal ('h') or vertical ('v'). Colours
# are the commonly used official values.
_TRICOLOUR: dict[str, tuple[str, list[str]]] = {
    "de": ("h", ["#000000", "#DD0000", "#FFCE00"]),  # Germany
    "nl": ("h", ["#AE1C28", "#FFFFFF", "#21468B"]),  # Netherlands
    "ru": ("h", ["#FFFFFF", "#0039A6", "#D52B1E"]),  # Russia
    "fr": ("v", ["#0055A4", "#FFFFFF", "#EF4135"]),  # France
    "it": ("v", ["#009246", "#FFFFFF", "#CE2B37"]),  # Italy
}


def _bands(p: QPainter, rect: QRectF, orient: str, colours: list[str],
           weights: list[float] | None = None) -> None:
    """Fill `rect` with proportional colour bands along one axis."""
    weights = weights or [1.0] * len(colours)
    total = sum(weights)
    span = rect.height() if orient == "h" else rect.width()
    pos = rect.top() if orient == "h" else rect.left()
    for colour, weight in zip(colours, weights):
        length = span * weight / total
        band = (
            QRectF(rect.left(), pos, rect.width(), length)
            if orient == "h"
            else QRectF(pos, rect.top(), length, rect.height())
        )
        p.fillRect(band, QColor(colour))
        pos += length


def _star(cx: float, cy: float, r: float, rotation_deg: float = -90.0) -> QPolygonF:
    """Return a five-pointed star polygon centred on (cx, cy)."""
    inner = r * 0.382  # golden-ratio inner radius of a regular 5-point star
    poly = QPolygonF()
    for i in range(10):
        radius = r if i % 2 == 0 else inner
        angle = math.radians(rotation_deg + i * 36.0)
        poly.append(QPointF(cx + radius * math.cos(angle),
                            cy + radius * math.sin(angle)))
    return poly


def _draw_japan(p: QPainter, rect: QRectF) -> None:
    p.fillRect(rect, QColor("#FFFFFF"))
    d = rect.height() * 0.6
    p.setBrush(QColor("#BC002D"))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(QPointF(rect.center()), d / 2, d / 2)


def _draw_spain(p: QPainter, rect: QRectF) -> None:
    # Red–yellow–red with a double-height yellow band (arms omitted at this size).
    _bands(p, rect, "h", ["#AA151B", "#F1BF00", "#AA151B"], [1, 2, 1])


def _draw_portugal(p: QPainter, rect: QRectF) -> None:
    _bands(p, rect, "v", ["#006600", "#FF0000"], [2, 3])
    # Yellow disc at the band boundary hints at the armillary sphere.
    cx = rect.left() + rect.width() * 0.4
    cy = rect.center().y()
    r = rect.height() * 0.22
    p.setBrush(QColor("#FFE400"))
    p.setPen(QPen(QColor("#8C5A00"), 0.6))
    p.drawEllipse(QPointF(cx, cy), r, r)


def _draw_china(p: QPainter, rect: QRectF) -> None:
    p.fillRect(rect, QColor("#DE2910"))
    p.setBrush(QColor("#FFDE00"))
    p.setPen(Qt.PenStyle.NoPen)
    big_r = rect.height() * 0.22
    bx, by = rect.left() + rect.width() * 0.16, rect.top() + rect.height() * 0.28
    p.drawPolygon(_star(bx, by, big_r))
    # Four small stars arcing around the big one.
    small_r = rect.height() * 0.09
    for fx, fy in [(0.32, 0.12), (0.40, 0.26), (0.40, 0.46), (0.32, 0.60)]:
        p.drawPolygon(_star(rect.left() + rect.width() * fx,
                            rect.top() + rect.height() * fy, small_r))


def _draw_union_jack(p: QPainter, rect: QRectF) -> None:
    """Simplified Union Jack (used for English)."""
    p.fillRect(rect, QColor("#012169"))
    p.setClipRect(rect)
    w, h = rect.width(), rect.height()
    tl, tr = rect.topLeft(), rect.topRight()
    bl, br = rect.bottomLeft(), rect.bottomRight()
    # White diagonals (St Andrew), then narrower red diagonals (St Patrick).
    p.setPen(QPen(QColor("#FFFFFF"), h * 0.28))
    p.drawLine(tl, br)
    p.drawLine(tr, bl)
    p.setPen(QPen(QColor("#C8102E"), h * 0.12))
    p.drawLine(tl, br)
    p.drawLine(tr, bl)
    # White cross (St George border), then narrower red cross on top.
    cx, cy = rect.center().x(), rect.center().y()
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor("#FFFFFF"))
    p.drawRect(QRectF(cx - w * 0.16, rect.top(), w * 0.32, h))
    p.drawRect(QRectF(rect.left(), cy - h * 0.22, w, h * 0.44))
    p.setBrush(QColor("#C8102E"))
    p.drawRect(QRectF(cx - w * 0.09, rect.top(), w * 0.18, h))
    p.drawRect(QRectF(rect.left(), cy - h * 0.13, w, h * 0.26))
    p.setClipping(False)


_SPECIAL = {
    "ja": _draw_japan,
    "es": _draw_spain,
    "pt": _draw_portugal,
    "zh": _draw_china,
    "en": _draw_union_jack,
}


def flag_icon(code: str) -> QIcon | None:
    """Return a small flag QIcon for a language code, or None if unsupported."""
    if code not in _TRICOLOUR and code not in _SPECIAL:
        return None

    px = QPixmap(_W, _H)
    px.fill(Qt.GlobalColor.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    rect = QRectF(0.5, 0.5, _W - 1, _H - 1)
    if code in _TRICOLOUR:
        orient, colours = _TRICOLOUR[code]
        _bands(p, rect, orient, colours)
    else:
        _SPECIAL[code](p, rect)

    # Subtle border so light flags (Japan, Netherlands) stay visible on the
    # dark menu background.
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.setPen(QPen(QColor(0, 0, 0, 90), 1))
    p.drawRect(rect)
    p.end()
    return QIcon(px)
