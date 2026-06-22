#!/usr/bin/env python3
"""Generate high-quality app icons for Titus AI OS"""
import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import (QPixmap, QPainter, QColor, QFont, QLinearGradient,
                            QBrush, QPen, QPainterPath)
from PySide6.QtCore import Qt, QRect

app = QApplication(sys.argv)

apps = [
    ("EchoKeys", "#0a1628", "#1a2a4a", "#8ab4f8", "#a8c8ff"),
    ("Auto Hub", "#0a0f1a", "#111827", "#c084fc", "#d8b4fe"),
    ("Job Intel", "#0a1a0f", "#112820", "#34d399", "#6ee7b7"),
    ("Monitor", "#1a0a0a", "#2a1111", "#f87171", "#fca5a5"),
    ("Portfolio", "#0f0a1a", "#1a1128", "#60a5fa", "#93c5fd"),
]

output_dir = "C:\\Users\\tbank\\Desktop\\Live Cowork\\APPS"
os.makedirs(output_dir, exist_ok=True)

for name, c1, c2, accent, accent2 in apps:
    for size in [256]:
        px = QPixmap(size, size)
        px.fill(Qt.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.TextAntialiasing)

        # Background with rounded rect
        grad = QLinearGradient(0, 0, size, size)
        grad.setColorAt(0, QColor(c1))
        grad.setColorAt(1, QColor(c2))
        p.setBrush(QBrush(grad))
        p.setPen(QPen(QColor(accent), 2))
        p.drawRoundedRect(2, 2, size-4, size-4, size//5, size//5)

        # Glass reflection
        rg = QLinearGradient(0, 0, 0, size//2)
        rg.setColorAt(0, QColor(255, 255, 255, 20))
        rg.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(rg))
        p.setPen(Qt.NoPen)
        rp = QPainterPath()
        rp.addRoundedRect(4, 4, size-8, (size-8)//2, size//8, size//8)
        p.drawPath(rp)

        # Bottom bar
        bg = QLinearGradient(0, size - size//5.5, 0, size)
        bg.setColorAt(0, QColor(accent))
        bg.setColorAt(1, QColor(accent2))
        p.setBrush(QBrush(bg))
        p.setPen(Qt.NoPen)
        bm = size//8
        bp = QPainterPath()
        bp.addRoundedRect(bm, size - size//5.5, size - 2*bm, size//7.5, size//14, size//14)
        p.drawPath(bp)

        # App name
        f = QFont("Segoe UI", size//15, QFont.DemiBold)
        p.setFont(f)
        p.setPen(QColor(c1))
        p.drawText(QRect(bm, size - size//5.5, size - 2*bm, size//7.5), Qt.AlignCenter, name)

        # Icon shapes
        ac = QColor(accent2)
        p.setPen(QPen(ac, max(3, size//10)))
        p.setBrush(Qt.NoBrush)

        if name == "EchoKeys":
            # Microphone
            p.drawRoundedRect(size//2 - size//10, size//3, size//5, size//3, 4, 4)
            p.drawChord(size//2 - size//6, size//2 + size//12, size//3, size//4, 0, 180*16)
            p.drawLine(size//2, size//2 + size//4, size//2, size//2 + size//3)
            p.drawLine(size//2 - size//8, size//2 + size//3, size//2 + size//8, size//2 + size//3)
        elif name == "Auto Hub":
            # Bolt/lightning
            pts = [(size//2, size//6), (size//3, size//2), (size//2 - size//12, size//2), 
                   (size//2, size*5//6), (size*2//3, size//2), (size//2 + size//12, size//2)]
            bp = QPainterPath()
            bp.moveTo(pts[0][0], pts[0][1])
            for pt in pts[1:]: bp.lineTo(pt[0], pt[1])
            bp.closeSubpath()
            p.setBrush(QBrush(ac))
            p.setPen(Qt.NoPen)
            p.drawPath(bp)
        elif name == "Job Intel":
            # Bar chart
            p.setPen(QPen(ac, max(3, size//14)))
            p.drawLine(size//4, size*3//4, size//4, size//3)
            p.drawLine(size//2, size*3//4, size//2, size//4)
            p.drawLine(size*3//4, size*3//4, size*3//4, size//2)
            p.drawLine(size//4, size*3//4, size*3//4, size*3//4)
            p.setBrush(QBrush(ac))
            p.setPen(Qt.NoPen)
            p.drawRect(size//4 - size//14, size//3, size//7, size*5//12)
            p.drawRect(size//2 - size//14, size//4, size//7, size//2)
            p.drawRect(size*3//4 - size//14, size//2, size//7, size//3)
        elif name == "Monitor":
            # Magnifying glass
            p.setPen(QPen(ac, max(4, size//10)))
            p.drawEllipse(size//3, size//4, size//3, size//3)
            p.drawLine(size//2 + size//10, size//2 + size//10, size*2//3 + size//10, size*2//3 + size//10)
        elif name == "Portfolio":
            # Globe
            p.setPen(QPen(ac, max(2, size//18)))
            p.drawEllipse(size//5, size//5, size*3//5, size*3//5)
            p.drawLine(size//5, size//2, size*4//5, size//2)
            p.drawArc(size//5, size//5, size*3//5, size*3//5, -60*16, 120*16)
            p.drawArc(size//5, size//5, size*3//5, size*3//5, 120*16, 120*16)

        p.end()
        filepath = os.path.join(output_dir, f"{name.replace(' ', '')}.png")
        px.save(filepath)
        print(f"Created: {name}.png")

print(f"\nAll icons in: {output_dir}")
app.quit()
