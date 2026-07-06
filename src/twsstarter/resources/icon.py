from __future__ import annotations
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QBrush, QPen, QFont, QLinearGradient, QPainterPath,
)
from PyQt6.QtCore import Qt, QRect, QPointF


def make_icon(size: int = 256) -> QPixmap:
    """Render the TWSStarter app icon at the given pixel size.

    A plain "launch" motif — a play triangle inside a soft ring — signalling
    "start something" (TWS/Gateway), with a small TWS wordmark. Deliberately
    understated: no chart imagery.
    """
    px = QPixmap(size, size)
    px.fill(Qt.GlobalColor.transparent)

    p = QPainter(px)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    # ── Background rounded rect ───────────────────────────────────────
    grad = QLinearGradient(0, 0, 0, size)
    grad.setColorAt(0.0, QColor("#1e3a8a"))
    grad.setColorAt(1.0, QColor("#0f172a"))
    p.setBrush(QBrush(grad))
    p.setPen(Qt.PenStyle.NoPen)
    radius = int(46 * size / 256)
    p.drawRoundedRect(0, 0, size, size, radius, radius)

    # ── Soft "start button" ring ──────────────────────────────────────
    cx, cy = size * 0.5, size * 0.44
    ring_r = size * 0.26
    ring = QPen(QColor(255, 255, 255, 60))
    ring.setWidth(max(2, int(size * 0.016)))
    p.setPen(ring)
    p.setBrush(QColor(255, 255, 255, 18))
    p.drawEllipse(QPointF(cx, cy), ring_r, ring_r)

    # ── Play / launch triangle ────────────────────────────────────────
    # Slightly right-shifted so the triangle looks optically centered.
    tri = QPainterPath()
    tri.moveTo(cx - size * 0.085, cy - size * 0.115)
    tri.lineTo(cx - size * 0.085, cy + size * 0.115)
    tri.lineTo(cx + size * 0.130, cy)
    tri.closeSubpath()

    white = QColor("#f8fafc")
    corner = QPen(white)
    corner.setWidth(max(2, int(size * 0.028)))
    corner.setJoinStyle(Qt.PenJoinStyle.RoundJoin)   # softened corners
    p.setPen(corner)
    p.setBrush(QBrush(white))
    p.drawPath(tri)

    # ── "TWS" wordmark ────────────────────────────────────────────────
    font = QFont("Arial", int(30 * size / 256), QFont.Weight.Bold)
    font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, size * 0.01)
    p.setFont(font)
    p.setPen(QPen(QColor("#cbd5e1")))
    p.setBrush(Qt.BrushStyle.NoBrush)
    text_rect = QRect(0, int(size * 0.72), size, int(size * 0.18))
    p.drawText(text_rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter, "TWS")

    p.end()
    return px
