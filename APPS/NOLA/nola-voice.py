#!/usr/bin/env python3
"""
NOLA Voice — Professional AI Voice Assistant
Open Door AI Systems | App Store Ready
"""

import sys, os, json, tempfile, time, threading, signal, ctypes, wave, io
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import keyboard, pyperclip

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# ─── NOLA BRAND ──────────────────────────────────────────────
BG = "#0b0f1a"
CARD = "#131827"
SURFACE = "rgba(255,255,255,0.04)"
BORDER = "rgba(255,255,255,0.06)"
BORDER_HOVER = "rgba(192,132,252,0.3)"
ACCENT = "#c084fc"
ACCENT2 = "#a78bfa"
ACCENT_GLOW = "rgba(192,132,252,0.15)"
TEXT = "#f1f5f9"
TEXT2 = "#94a3b8"
TEXT3 = "rgba(148,163,184,0.4)"
RED = "#f87171"
GREEN = "#34d399"

STYLE = f"""
QWidget {{ font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif; color: {TEXT}; }}
QMainWindow {{ background: transparent; }}
QTextEdit {{
    background: {SURFACE}; color: {TEXT}; border: 1px solid {BORDER};
    border-radius: 12px; padding: 16px; font-size: 14px; line-height: 1.6;
    selection-background-color: {ACCENT_GLOW};
}}
QTextEdit:focus {{ border-color: {ACCENT}; }}
QComboBox {{
    background: {SURFACE}; color: {TEXT2}; border: 1px solid {BORDER};
    border-radius: 8px; padding: 8px 14px; font-size: 12px; min-width: 110px;
}}
QComboBox:hover {{ border-color: {ACCENT}; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox::down-arrow {{ image: none; }}
QComboBox QAbstractItemView {{
    background: {CARD}; color: {TEXT}; border: 1px solid {BORDER};
    border-radius: 8px; selection-background-color: {ACCENT_GLOW};
}}
QPushButton {{ border: none; border-radius: 10px; padding: 10px 20px; font-size: 13px; font-weight: 600; }}
QToolTip {{ background: {CARD}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 8px; padding: 8px 12px; }}
QSlider::groove:horizontal {{ height: 4px; background: {BORDER}; border-radius: 2px; }}
QSlider::handle:horizontal {{ background: {ACCENT}; width: 16px; height: 16px; margin: -6px 0; border-radius: 8px; }}
QSlider::sub-page:horizontal {{ background: {ACCENT}; border-radius: 2px; }}
QCheckBox {{ spacing: 8px; font-size: 12px; color: {TEXT2}; }}
QCheckBox::indicator {{ width: 18px; height: 18px; border-radius: 5px; border: 1px solid {BORDER}; background: {SURFACE}; }}
QCheckBox::indicator:checked {{ background: {ACCENT}; border-color: {ACCENT}; }}
"""


class NOLA_transcriber(QThread):
    done = Signal(str)
    def __init__(self):
        super().__init__()
        self.path = None
        self.model = None
        QTimer.singleShot(100, self._load)
    def _load(self):
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel("tiny", device="auto", compute_type="int8")
        except: pass
    def run(self):
        if not self.model or not self.path: self.done.emit(""); return
        try:
            segs, _ = self.model.transcribe(self.path, beam_size=5)
            self.done.emit(" ".join(s.text.strip() for s in segs))
        except: self.done.emit("")


class NOLAVoiceWindow(QMainWindow):
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        app.setStyleSheet(STYLE)
        
        self.recording = False
        self.transcriber = NOLA_transcriber()
        self.transcriber.done.connect(self._on_transcribed)
        
        self._build_ui()
        self._build_tray()
        keyboard.add_hotkey("ctrl+shift+n", self._toggle_rec, suppress=True)
    
    def _build_ui(self):
        self.setWindowTitle("NOLA Voice")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(440, 560)
        
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 480, screen.height() - 610)
        
        root = QWidget()
        root.setObjectName("root")
        root.setStyleSheet(f"""
            QWidget#root {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {BG}, stop:1 {CARD});
                border-radius: 20px;
                border: 1px solid {BORDER};
            }}
        """)
        lo = QVBoxLayout(root)
        lo.setContentsMargins(24, 20, 24, 20)
        lo.setSpacing(12)
        
        # ── Header ──
        hdr = QHBoxLayout()
        logo = QLabel("◈")
        logo.setStyleSheet(f"font-size: 24px; color: {ACCENT}; background: transparent; font-weight: 300;")
        hdr.addWidget(logo)
        
        title = QVBoxLayout()
        t = QLabel("NOLA")
        t.setStyleSheet(f"font-size: 17px; font-weight: 800; color: {TEXT}; background: transparent; letter-spacing: 0.5px;")
        title.addWidget(t)
        sub = QLabel("Voice Assistant · Open Door AI")
        sub.setStyleSheet(f"font-size: 10px; color: {TEXT3}; background: transparent; letter-spacing: 1px; margin-top: -2px;")
        title.addWidget(sub)
        hdr.addLayout(title)
        hdr.addStretch()
        
        self.dot = QLabel("●")
        self.dot.setStyleSheet(f"font-size: 10px; color: {TEXT3}; background: transparent;")
        hdr.addWidget(self.dot)
        self.stat = QLabel("Ready")
        self.stat.setStyleSheet(f"font-size: 11px; color: {TEXT2}; background: transparent;")
        hdr.addWidget(self.stat)
        
        close = QPushButton("✕")
        close.setFixedSize(24, 24)
        close.setCursor(Qt.PointingHandCursor)
        close.setStyleSheet(f"QPushButton{{background:transparent;color:{TEXT3};font-size:14px;border:none;border-radius:12px;}}QPushButton:hover{{background:rgba(255,255,255,0.06);color:{TEXT};}}")
        close.clicked.connect(self.hide)
        hdr.addWidget(close)
        lo.addLayout(hdr)
        
        # ── Glow bar ──
        self.glow = QFrame()
        self.glow.setFixedHeight(3)
        self.glow.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {ACCENT}, stop:0.5 transparent, stop:1 {ACCENT}); border-radius: 2px;")
        lo.addWidget(self.glow)
        
        # ── Mode selector ──
        modes = QHBoxLayout()
        self.mode_cb = QComboBox()
        for m in ["🎤 Voice", "💬 Message", "✉️ Email", "📋 Bullets", "📱 Social"]:
            self.mode_cb.addItem(m)
        modes.addWidget(QLabel("Mode:"))
        modes.addWidget(self.mode_cb)
        modes.addStretch()
        lo.addLayout(modes)
        
        # ── Output area ──
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Press Ctrl+Shift+N or click Record to start speaking...")
        self.output.setMinimumHeight(180)
        lo.addWidget(self.output)
        
        # ── Record button ──
        self.rec_btn = QPushButton("●  Hold to Record")
        self.rec_btn.setCursor(Qt.PointingHandCursor)
        self.rec_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {ACCENT2});
                color: {BG}; font-weight: 700; font-size: 14px;
                border: none; border-radius: 12px; padding: 14px 24px;
            }}
            QPushButton:hover {{ opacity: 0.9; }}
        """)
        self.rec_btn.pressed.connect(self._start_rec)
        self.rec_btn.released.connect(self._stop_rec)
        lo.addWidget(self.rec_btn)
        
        # ── Action buttons ──
        acts = QHBoxLayout(); acts.setSpacing(8)
        for text, cb in [("📋 Paste", self._paste), ("📄 Copy", self._copy), ("🗑 Clear", lambda: self.output.clear())]:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"QPushButton{{background:{SURFACE};color:{TEXT2};border:1px solid {BORDER};padding:8px 14px;font-size:12px;}}QPushButton:hover{{background:{ACCENT_GLOW};color:{ACCENT};border-color:{ACCENT};}}")
            btn.clicked.connect(cb)
            acts.addWidget(btn)
        lo.addLayout(acts)
        
        # ── Footer ──
        foot = QHBoxLayout()
        self.mic = QLabel("○")
        self.mic.setStyleSheet(f"font-size: 14px; color: {TEXT3}; background: transparent;")
        foot.addWidget(self.mic)
        foot.addStretch()
        foot.addWidget(QLabel(f"<span style='color:{TEXT3};font-size:9px;'>Open Door AI Systems  ·  v2.0</span>"))
        lo.addLayout(foot)
        
        self.setCentralWidget(root)
        
        # Dragging
        self.drag_pos = None
        root.mousePressEvent = lambda e: setattr(self, 'drag_pos', e.globalPosition().toPoint() - self.frameGeometry().topLeft()) if e.button() == Qt.LeftButton and e.position().y() < 60 else None
        root.mouseMoveEvent = lambda e: self.move(e.globalPosition().toPoint() - self.drag_pos) if e.buttons() == Qt.LeftButton and self.drag_pos else None
    
    def _build_tray(self):
        self.tray = QSystemTrayIcon(self)
        m = QMenu()
        m.setStyleSheet(f"QMenu{{background:{CARD};border:1px solid {BORDER};border-radius:8px;padding:4px;}}QMenu::item{{padding:8px 20px;border-radius:4px;font-size:12px;}}QMenu::item:selected{{background:{ACCENT_GLOW};}}")
        m.addAction("◈  Show NOLA").triggered.connect(lambda: (self.show(), self.raise_(), self.activateWindow()))
        m.addSeparator()
        m.addAction("Quit").triggered.connect(self._quit)
        self.tray.setContextMenu(m)
        self.tray.setToolTip("NOLA Voice — Ctrl+Shift+N to record")
        self.tray.show()
    
    def _toggle_rec(self):
        if self.recording: self._stop_rec()
        else: self._start_rec()
    
    def _start_rec(self):
        if self.recording: return
        self.recording = True
        self.rec_btn.setText("⏺  Recording...")
        self.rec_btn.setStyleSheet(f"QPushButton{{background:{RED};color:white;font-weight:700;font-size:14px;border:none;border-radius:12px;padding:14px 24px;}}")
        self.dot.setStyleSheet(f"font-size:10px;color:{RED};background:transparent;")
        self.stat.setText("Recording"); self.mic.setText("●"); self.mic.setStyleSheet(f"font-size:14px;color:{RED};background:transparent;")
        self.glow.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {RED},stop:0.5 transparent,stop:1 {RED});border-radius:2px;")
        threading.Thread(target=self._capture, daemon=True).start()
    
    def _stop_rec(self):
        if not self.recording: return
        self.recording = False
        self.rec_btn.setText("⏳  Processing...")
        self.stat.setText("Transcribing")
    
    def _capture(self):
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            s = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
            frames = []
            while self.recording:
                frames.append(s.read(1024, exception_on_overflow=False))
            s.stop_stream(); s.close(); p.terminate()
            path = os.path.join(tempfile.gettempdir(), "nola_capture.wav")
            wf = wave.open(path, 'wb')
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(16000)
            wf.writeframes(b''.join(frames)); wf.close()
            if os.path.getsize(path) > 1000:
                self.transcriber.path = path
                self.transcriber.start()
        except Exception as e:
            self.output.setText(f"Mic error: {e}")
            self._reset_ui()
    
    def _on_transcribed(self, text):
        if text.strip(): self.output.setText(text)
        self._reset_ui()
        if text.strip(): QTimer.singleShot(300, self._paste)
    
    def _reset_ui(self):
        self.rec_btn.setText("●  Hold to Record")
        self.rec_btn.setStyleSheet(f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {ACCENT},stop:1 {ACCENT2});color:{BG};font-weight:700;font-size:14px;border:none;border-radius:12px;padding:14px 24px;}}")
        self.dot.setStyleSheet(f"font-size:10px;color:{TEXT3};background:transparent;")
        self.stat.setText("Ready"); self.mic.setText("○")
        self.mic.setStyleSheet(f"font-size:14px;color:{TEXT3};background:transparent;")
        self.glow.setStyleSheet(f"background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {ACCENT},stop:0.5 transparent,stop:1 {ACCENT});border-radius:2px;")
    
    def _paste(self):
        t = self.output.toPlainText()
        if t.strip():
            pyperclip.copy(t)
            QTimer.singleShot(100, lambda: keyboard.send("ctrl+v"))
            QTimer.singleShot(300, self.hide)
    
    def _copy(self):
        t = self.output.toPlainText()
        if t.strip(): pyperclip.copy(t); self.stat.setText("Copied!")
    
    def _quit(self):
        keyboard.unhook_all(); ctypes.windll.kernel32.SetThreadExecutionState(0x80000000); self.app.quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setApplicationName("NOLA Voice")
    app.setQuitOnLastWindowClosed(False)
    
    # Generate app icon
    px = QPixmap(256, 256); px.fill(Qt.transparent)
    pa = QPainter(px); pa.setRenderHint(QPainter.Antialiasing)
    grad = QLinearGradient(0, 0, 256, 256)
    grad.setColorAt(0, QColor("#0b0f1a")); grad.setColorAt(1, QColor("#131827"))
    pa.setBrush(QBrush(grad)); pa.setPen(QPen(QColor(ACCENT), 2))
    pa.drawRoundedRect(2, 2, 252, 252, 50, 50)
    pa.setPen(QPen(QColor(ACCENT2), 6))
    pa.drawRoundedRect(120, 60, 16, 60, 4, 4)
    pa.drawChord(105, 100, 45, 35, 0, 180*16)
    pa.drawLine(128, 115, 128, 135)
    pa.drawLine(113, 135, 143, 135)
    # N letter
    f = QFont("Segoe UI", 80, QFont.Bold); pa.setFont(f); pa.setPen(QColor(ACCENT2))
    pa.drawText(QRect(0, 130, 256, 100), Qt.AlignCenter, "N")
    pa.end()
    icon_path = os.path.join(os.path.dirname(__file__), "nola_icon.png")
    px.save(icon_path)
    
    w = NOLAVoiceWindow(app)
    QTimer.singleShot(500, lambda: (w.show(), w.raise_(), w.activateWindow()))
    sys.exit(app.exec())