"""HUD Window — Floating recording indicator with timer and level meter"""
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QFrame
)
from PySide6.QtCore import Qt, QTimer, QRect, QPoint
from PySide6.QtGui import QFont, QColor, QPainter, QPainterPath, QBrush

from constants import BG, BG2, BG3, SURFACE, BORDER, ACCENT, ACCENT2, TEXT, TEXT2, GREEN, RED, GLOW_ACCENT


class HUDWindow(QWidget):
    """Frameless, always-on-top floating HUD for recording feedback."""

    def __init__(self, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(360, 120)
        
        self._recording = False
        self._start_time = 0
        self._level = 0.0
        self._mode = "Voice"
        
        self._setup_ui()
        self._center_on_screen()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_timer)
        self._level_timer = QTimer(self)
        self._level_timer.timeout.connect(self._update_level)
        self._level_timer.start(50)  # 20 FPS for level meter

    def _setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{ background: transparent; }}
            QLabel {{ color: #f0f2f5; font-family: 'Segoe UI', sans-serif; }}
        """)

        # Main container with rounded corners and shadow
        container = QFrame(self)
        container.setGeometry(0, 0, 360, 120)
        container.setStyleSheet(f"""
            QFrame {{
                background: #0d111a;
                border: 1px solid #2a3147;
                border-radius: 16px;
            }}
        """)
        
        # Add drop shadow
        from PySide6.QtWidgets import QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 4)
        container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)

        # Top row: Mode badge + Recording indicator
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.mode_badge = QLabel("VOICE")
        self.mode_badge.setStyleSheet("""
            background: rgba(139,92,246,0.2);
            color: #a78bfa;
            border: 1px solid #3b4460;
            border-radius: 6px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
        """)
        top_row.addWidget(self.mode_badge)
        top_row.addStretch()

        self.rec_indicator = QLabel("●")
        self.rec_indicator.setStyleSheet("color: #ef4444; font-size: 14px;")
        self.rec_indicator.hide()
        top_row.addWidget(self.rec_indicator)

        layout.addLayout(top_row)

        # Timer display
        self.timer_label = QLabel("0:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: #f0f2f5;
            font-variant-numeric: tabular-nums;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
        """)
        layout.addWidget(self.timer_label)

        # Level meter
        self.level_bar = QProgressBar()
        self.level_bar.setRange(0, 100)
        self.level_bar.setValue(0)
        self.level_bar.setTextVisible(False)
        self.level_bar.setFixedHeight(6)
        self.level_bar.setStyleSheet("""
            QProgressBar {
                background: #131823;
                border: 1px solid #2a3147;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8b5cf6, stop:1 #a78bfa);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.level_bar)

        # Status label
        self.status_label = QLabel("Ready to record")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #64748b; font-size: 11px;")
        layout.addWidget(self.status_label)

    def _center_on_screen(self):
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            self.move(
                geo.width() // 2 - self.width() // 2,
                geo.height() // 2 - self.height() // 2
            )

    def start_recording(self, mode: str = "Voice"):
        self._recording = True
        self._mode = mode
        self._start_time = time.time()
        self.rec_indicator.show()
        self.status_label.setText("Recording...")
        self.rec_indicator.setStyleSheet("color: #ef4444; font-size: 14px;")
        self.timer_label.setStyleSheet(self.timer_label.styleSheet().replace("#f0f2f5", "#ef4444"))
        self._timer.start(1000)
        self._timer_single_shot = False

    def stop_recording(self):
        self._recording = False
        self._timer.stop()
        self.rec_indicator.hide()
        self.status_label.setText("Transcribing...")
        self.timer_label.setStyleSheet(self.timer_label.styleSheet().replace("#ef4444", "#f0f2f5"))

    def set_status(self, text: str):
        self.status_label.setText(text)

    def set_mode(self, mode: str):
        self._mode = mode
        self.mode_badge.setText(mode.upper())

    def _update_timer(self):
        if self._recording:
            elapsed = int(time.time() - self._start_time)
            m = elapsed // 60
            s = elapsed % 60
            self.timer_label.setText(f"{m}:{s:02d}")

    def _update_level(self):
        if self._recording:
            # This will be updated externally via set_level
            pass

    def set_level(self, level: float):
        """Set audio level (0.0 to 1.0)."""
        self._level = level
        self.level_bar.setValue(int(level * 100))

    def closeEvent(self, event):
        self._timer.stop()
        self._level_timer.stop()
        super().closeEvent(event)