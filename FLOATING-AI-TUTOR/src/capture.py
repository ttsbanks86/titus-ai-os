#!/usr/bin/env python3
"""Screen capture with region selection overlay (Snipping Tool style)."""
import sys
from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QScreen, QPixmap, QCursor
from PySide6.QtWidgets import QApplication, QWidget


class RegionSelector(QWidget):
    """Full-screen transparent overlay for region selection."""

    region_selected = Signal(QRect)
    cancelled = Signal()

    def __init__(self, screenshot: QPixmap):
        super().__init__(None)
        self._screenshot = screenshot
        self._start = None
        self._current = None
        self._selecting = False

        # Full-screen overlay on primary monitor
        screen = QApplication.primaryScreen()
        geo = screen.geometry()
        self.setGeometry(geo)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Dim everything
        painter.fillRect(self.rect(), QColor(0, 0, 0, 120))
        # Restore the selected region
        if self._start and self._current:
            rect = QRect(self._start, self._current).normalized()
            painter.drawPixmap(rect, self._screenshot, rect)
            # Draw selection border
            pen = QPen(QColor(99, 102, 241), 2)
            painter.setPen(pen)
            painter.drawRect(rect)
            # Draw size label
            painter.setPen(QColor(224, 231, 255))
            painter.setFont(self.font())
            label = f"{rect.width()} x {rect.height()}"
            painter.drawText(rect.left() + 6, rect.top() + 18, label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start = event.pos()
            self._current = event.pos()
            self._selecting = True

    def mouseMoveEvent(self, event):
        if self._selecting:
            self._current = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._selecting:
            self._selecting = False
            rect = QRect(self._start, self._current).normalized()
            if rect.width() > 10 and rect.height() > 10:
                self.region_selected.emit(rect)
            else:
                self.cancelled.emit()
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._selecting = False
            self.cancelled.emit()
            self.close()


def capture_region() -> QPixmap | None:
    """Show region selector and return the captured pixmap, or None if cancelled."""
    app = QApplication.instance()
    was_none = app is None
    if was_none:
        app = QApplication(sys.argv)

    screen = QApplication.primaryScreen()
    full = screen.grabWindow(0)

    selector = RegionSelector(full)
    result = [None]

    def on_selected(rect: QRect):
        result[0] = full.copy(rect)

    selector.region_selected.connect(on_selected)
    selector.show()
    selector.activateWindow()
    selector.raise_()

    # Wait for selection
    while selector.isVisible():
        app.processEvents()

    if was_none:
        # Don't quit if we didn't create the app
        pass

    return result[0]


def capture_full_screen() -> QPixmap:
    """Capture the entire primary screen."""
    screen = QApplication.primaryScreen()
    return screen.grabWindow(0)
