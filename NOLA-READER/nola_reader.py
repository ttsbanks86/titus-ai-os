#!/usr/bin/env python3
"""NOLA Voice Reader — Pure Native Desktop (PySide6 + Windows TTS)"""
import sys, os, threading, time, ctypes, pyttsx3
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QTextEdit, QLabel, QSlider, QComboBox, QFrame,
    QSystemTrayIcon, QMenu)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QPalette, QAction
from PySide6.QtCore import Qt, QThread, Signal

# Keep PC awake
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# ─── TTS Engine (pytts3 - Windows SAPI5) ─────────────────────────────────
class TTSEngine:
    def __init__(self):
        self.engine = None
        self.voices = []
        self._init()

    def _init(self):
        try:
            self.engine = pyttsx3.init()
            self.voices = self.engine.getProperty('voices')
        except Exception as e:
            print(f"[NOLA] TTS init error: {e}")

    def get_voice_list(self):
        return [(v.name.replace('Microsoft ','').split(' - ')[0], i) for i, v in enumerate(self.voices)]

    def speak(self, text, voice_idx=0, speed=1.0):
        if not self.engine: return
        try:
            self.engine.setProperty('voice', self.voices[voice_idx].id)
            self.engine.setProperty('rate', int(150 * speed))
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"[NOLA] TTS error: {e}")

    def speak_async(self, text, voice_idx=0, speed=1.0, callback=None):
        def _run():
            self.speak(text, voice_idx, speed)
            if callback: callback()
        threading.Thread(target=_run, daemon=True).start()

# ─── Clipboard Monitor ────────────────────────────────────────────────────
import pyperclip

class ClipboardThread(QThread):
    text_captured = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.last = ""

    def run(self):
        try: self.last = pyperclip.paste() or ""
        except: self.last = ""
        while self.running:
            try:
                time.sleep(0.5)
                current = pyperclip.paste()
                if current and current != self.last and current.strip():
                    self.last = current
                    self.text_captured.emit(current)
            except:
                time.sleep(1.0)

    def stop(self):
        self.running = False

# ─── Main Window ──────────────────────────────────────────────────────────
class NOLAReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tts = TTSEngine()
        self.is_listening = True
        self.current_text = ""
        self.is_speaking = False
        self.setWindowTitle("NOLA Voice Reader")
        self.setFixedSize(480, 380)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setup_ui()
        self.setup_tray()
        self.start_clipboard_monitor()

    def setup_ui(self):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0a0c10"))
        palette.setColor(QPalette.WindowText, QColor("#f0f2f5"))
        palette.setColor(QPalette.Base, QColor("#14161c"))
        palette.setColor(QPalette.Text, QColor("#f0f2f5"))
        palette.setColor(QPalette.Button, QColor("#1e2030"))
        palette.setColor(QPalette.ButtonText, QColor("#f0f2f5"))
        self.setPalette(palette)
        self.setStyleSheet("""
            QMainWindow { background: #0a0c10; }
            QLabel { color: #f0f2f5; font-family: Segoe UI, sans-serif; }
            QPushButton {
                background: #1e2030; border: 1px solid #2a2d3e; border-radius: 8px;
                padding: 8px 16px; color: #c8ced6; font-family: Segoe UI, sans-serif; font-size: 12px;
            }
            QPushButton:hover { background: #2a2d3e; border-color: #a78bfa; color: #a78bfa; }
            QPushButton#primaryBtn {
                background: #7c3aed; border: none; color: white; font-weight: 600; font-size: 13px; padding: 10px;
            }
            QPushButton#primaryBtn:hover { background: #8b5cf6; }
            QComboBox {
                background: #14161c; border: 1px solid #2a2d3e; border-radius: 6px;
                padding: 6px 10px; color: #c8ced6; font-family: Segoe UI, sans-serif; font-size: 11px;
            }
            QComboBox:hover { border-color: #a78bfa; }
            QComboBox QAbstractItemView { background: #1e2030; color: #c8ced6; selection-background: #7c3aed; }
            QSlider::groove:horizontal { height: 4px; background: #2a2d3e; border-radius: 2px; }
            QSlider::handle:horizontal { background: #a78bfa; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }
            QSlider::sub-page:horizontal { background: #a78bfa; border-radius: 2px; }
            QTextEdit { background: #0f1117; border: 1px solid #2a2d3e; border-radius: 8px; padding: 10px; color: #d1d5db; font-family: Segoe UI, sans-serif; font-size: 13px; }
            QTextEdit:focus { border-color: #a78bfa; }
            QFrame#statusBar { background: rgba(255,255,255,0.02); border-radius: 6px; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        # Header
        hdr = QHBoxLayout()
        icon_lbl = QLabel("R")
        icon_lbl.setFixedSize(28, 28)
        icon_lbl.setStyleSheet("background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #a78bfa,stop:1 #7c3aed);border-radius:7px;font-weight:bold;font-size:14px;color:white;qproperty-alignment:AlignCenter;")
        title = QLabel("<b>NOLA Voice Reader</b>  <span style='color:#6b7280;font-size:9px'>Clipboard TTS</span>")
        title.setTextFormat(Qt.RichText)
        hdr.addWidget(icon_lbl)
        hdr.addWidget(title)
        hdr.addStretch()
        layout.addLayout(hdr)

        # Status
        self.status_frame = QFrame()
        self.status_frame.setObjectName("statusBar")
        self.status_frame.setFixedHeight(28)
        sb = QHBoxLayout(self.status_frame)
        sb.setContentsMargins(10, 0, 10, 0)
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet("color: #22c55e; font-size: 10px;")
        self.status_text = QLabel("Listening for clipboard...")
        self.status_text.setStyleSheet("color: #6b7280; font-size: 10px;")
        sb.addWidget(self.status_dot)
        sb.addWidget(self.status_text)
        sb.addStretch()
        self.char_count = QLabel("0 chars")
        self.char_count.setStyleSheet("color: #4a5568; font-size: 9px;")
        sb.addWidget(self.char_count)
        layout.addWidget(self.status_frame)

        # Controls row
        ctrl = QHBoxLayout()
        ctrl.setSpacing(8)
        vc = QVBoxLayout()
        vc.setSpacing(2)
        vc.addWidget(QLabel("Voice"))
        self.voice_combo = QComboBox()
        voices = self.tts.get_voice_list()
        for name, idx in voices:
            self.voice_combo.addItem(name, idx)
        if not voices:
            self.voice_combo.addItem("Default", 0)
        self.voice_combo.setMinimumWidth(130)
        vc.addWidget(self.voice_combo)
        ctrl.addLayout(vc)

        sc = QVBoxLayout()
        sc.setSpacing(2)
        sc.addWidget(QLabel("Speed"))
        sr = QHBoxLayout()
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(5, 25)
        self.speed_slider.setValue(10)
        self.speed_slider.valueChanged.connect(self._on_speed)
        self.speed_label = QLabel("1.0x")
        self.speed_label.setStyleSheet("color: #a78bfa; font-weight: 600; min-width: 32px;")
        sr.addWidget(self.speed_slider)
        sr.addWidget(self.speed_label)
        sc.addLayout(sr)
        ctrl.addLayout(sc)
        layout.addLayout(ctrl)

        # Clipboard display
        self.clip_display = QTextEdit()
        self.clip_display.setReadOnly(True)
        self.clip_display.setMaximumHeight(100)
        self.clip_display.setPlaceholderText("Copy text anywhere — it will be read aloud...")
        layout.addWidget(self.clip_display)

        # Buttons
        btns = QHBoxLayout()
        self.listen_btn = QPushButton("⏸ Pause")
        self.listen_btn.clicked.connect(self._toggle)
        btns.addWidget(self.listen_btn)

        self.test_btn = QPushButton("🎤 Test Voice")
        self.test_btn.clicked.connect(self._test_voice)
        btns.addWidget(self.test_btn)

        self.speak_btn = QPushButton("🔊 Speak Last")
        self.speak_btn.setObjectName("primaryBtn")
        self.speak_btn.clicked.connect(self._speak_last)
        btns.addWidget(self.speak_btn)
        layout.addLayout(btns)

        # Footer
        footer = QLabel("<span style='color:#4a5568;font-size:8px'>Alt+Shift+R · Windows TTS</span>")
        footer.setTextFormat(Qt.RichText)
        layout.addWidget(footer)

    def setup_tray(self):
        px = QPixmap(28, 28)
        px.fill(Qt.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor("#7c3aed"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(2, 2, 24, 24, 6, 6)
        p.setPen(QColor("white"))
        p.setFont(QFont("Segoe UI", 12, QFont.Bold))
        p.drawText(2, 2, 24, 24, Qt.AlignCenter, "R")
        p.end()
        self.tray = QSystemTrayIcon(QIcon(px), self)
        self.tray.setToolTip("NOLA Voice Reader")
        menu = QMenu()
        menu.addAction("Show", self._show_window)
        menu.addSeparator()
        menu.addAction("Quit", self._quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(lambda r: self._show_window() if r == QSystemTrayIcon.DoubleClick else None)
        self.tray.show()

    def start_clipboard_monitor(self):
        self.clip_thread = ClipboardThread()
        self.clip_thread.text_captured.connect(self._on_clip)
        self.clip_thread.start()

    def _on_clip(self, text):
        self.current_text = text
        self.clip_display.setPlainText(text[:500])
        self.char_count.setText(f"{len(text)} chars")
        if self.is_listening and len(text) > 2:
            self.status_text.setText("Speaking...")
            self.status_dot.setStyleSheet("color: #a78bfa; font-size: 10px;")
            vi = self.voice_combo.currentData()
            sp = self.speed_slider.value() / 10.0
            self.is_speaking = True
            self.tts.speak_async(text, vi, sp, self._on_done)

    def _on_done(self):
        self.is_speaking = False
        if self.is_listening:
            self.status_text.setText("Listening for clipboard...")
            self.status_dot.setStyleSheet("color: #22c55e; font-size: 10px;")
        else:
            self.status_text.setText("Paused")
            self.status_dot.setStyleSheet("color: #6b7280; font-size: 10px;")

    def _toggle(self):
        self.is_listening = not self.is_listening
        t = "⏸ Pause" if self.is_listening else "▶ Resume"
        self.listen_btn.setText(t)
        self._on_done()

    def _test_voice(self):
        vi = self.voice_combo.currentData()
        sp = self.speed_slider.value() / 10.0
        self.status_text.setText("Testing voice...")
        self.status_dot.setStyleSheet("color: #a78bfa; font-size: 10px;")
        self.tts.speak_async("Hello, this is a voice test from NOLA Voice Reader.", vi, sp, self._on_done)

    def _speak_last(self):
        if self.current_text and len(self.current_text) > 2:
            vi = self.voice_combo.currentData()
            sp = self.speed_slider.value() / 10.0
            self.status_text.setText("Speaking...")
            self.is_speaking = True
            self.tts.speak_async(self.current_text, vi, sp, self._on_done)

    def _on_speed(self):
        self.speed_label.setText(f"{self.speed_slider.value() / 10.0:.1f}x")

    def _show_window(self):
        self.show(); self.raise_(); self.activateWindow()

    def _quit(self):
        if hasattr(self, 'clip_thread'): self.clip_thread.stop()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = NOLAReader()
    win.show()
    sys.exit(app.exec())
