#!/usr/bin/env python3
"""
EchoKeys Pro — AI Voice-to-Text for Windows
Matches Super Whisper design & functionality
"""

import sys, os, json, tempfile, time, threading, signal, ctypes, wave
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import keyboard, pyperclip
from pynput import mouse

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# ─── SUPER WHISPER INSPIRED DESIGN ─────────────────────────
BG = "#0c0c0e"
CARD = "#151517"
SURFACE = "rgba(255,255,255,0.04)"
BORDER = "rgba(255,255,255,0.07)"
BORDER_HOVER = "rgba(138,180,248,0.35)"
ACCENT = "#8ab4f8" 
ACCENT2 = "#6a94d8"
ACCENT_GLOW = "rgba(138,180,248,0.12)"
TEXT = "#f0f2f5"
TEXT2 = "#8a9bb5"
TEXT3 = "rgba(138,155,181,0.35)"
RED = "#ef4444"
GREEN = "#22c55e"

STYLE = f"""
QWidget {{ font-family: -apple-system, 'Inter', 'Segoe UI', sans-serif; color: {TEXT}; }}
QMainWindow {{ background: transparent; }}
QTextEdit {{
    background: {SURFACE}; color: {TEXT}; border: 1px solid {BORDER};
    border-radius: 14px; padding: 18px; font-size: 14px; line-height: 1.6;
    selection-background-color: {ACCENT_GLOW};
}}
QTextEdit:focus {{ border-color: {ACCENT}; }}
QComboBox {{
    background: {SURFACE}; color: {TEXT2}; border: 1px solid {BORDER};
    border-radius: 8px; padding: 8px 16px; font-size: 12px; min-width: 120px;
}}
QComboBox:hover {{ border-color: {ACCENT}; }}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox::down-arrow {{ image: none; }}
QComboBox QAbstractItemView {{
    background: {CARD}; color: {TEXT}; border: 1px solid {BORDER};
    border-radius: 8px; selection-background-color: {ACCENT_GLOW}; padding: 4px;
}}
QPushButton {{ border: none; border-radius: 10px; padding: 10px 20px; font-size: 13px; font-weight: 600; }}
QToolTip {{ background: {CARD}; color: {TEXT}; border: 1px solid {BORDER}; border-radius: 8px; padding: 8px 12px; }}
"""

MODES = [
    ("🎤 Voice", "Clean transcription, natural"),
    ("💬 Message", "Casual professional, brief"),
    ("✉️ Email", "Formal with structure"),
    ("📋 Bullets", "Clean bullet points"),
    ("📱 Social", "Short, engaging"),
]


class Transcriber(QThread):
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


class EchoKeysWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        app.setStyleSheet(STYLE)
        
        self.recording = False
        self.transcriber = Transcriber()
        self.transcriber.done.connect(self._on_transcribed)
        
        self._build_ui()
        self._build_tray()
        self._setup_hotkeys()
    
    def _build_ui(self):
        self.setWindowTitle("EchoKeys Pro")
        flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(420, 540)
        
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 460, screen.height() - 590)
        
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
        lo.setContentsMargins(20, 18, 20, 18)
        lo.setSpacing(10)
        
        # ── Header ──
        hdr = QHBoxLayout()
        icon_lbl = QLabel("🎙")
        icon_lbl.setStyleSheet("font-size: 20px; background: transparent;")
        hdr.addWidget(icon_lbl)
        
        title_block = QVBoxLayout()
        title = QLabel("EchoKeys Pro")
        title.setStyleSheet(f"font-size: 16px; font-weight: 700; color: {TEXT}; background: transparent; letter-spacing: -0.3px;")
        title_block.addWidget(title)
        subtitle = QLabel("Voice to text · Press to speak")
        subtitle.setStyleSheet(f"font-size: 10px; color: {TEXT3}; background: transparent; margin-top: -2px;")
        title_block.addWidget(subtitle)
        hdr.addLayout(title_block)
        hdr.addStretch()
        
        self.dot = QLabel("●")
        self.dot.setStyleSheet(f"font-size: 9px; color: {TEXT3}; background: transparent;")
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
        
        # ── Recording indicator bar ──
        self.indicator = QFrame()
        self.indicator.setFixedHeight(3)
        self.indicator.setStyleSheet(f"background: transparent; border-radius: 2px;")
        lo.addWidget(self.indicator)
        
        # ── Mode selector ──
        mode_row = QHBoxLayout()
        self.mode_cb = QComboBox()
        for name, desc in MODES: self.mode_cb.addItem(name)
        mode_row.addWidget(QLabel("Mode:"))
        mode_row.addWidget(self.mode_cb)
        mode_row.addStretch()
        lo.addLayout(mode_row)
        
        # ── Transcription ──
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Hold Alt+Space or your mouse thumb button to start speaking...\nRelease to transcribe and paste.")
        self.output.setMinimumHeight(170)
        lo.addWidget(self.output)
        
        # ── Record ──
        self.rec_btn = QPushButton("🎤  Hold to Record")
        self.rec_btn.setCursor(Qt.PointingHandCursor)
        self.rec_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {ACCENT}, stop:1 {ACCENT2});
                color: {BG}; font-weight: 700; font-size: 14px; letter-spacing: 0.3px;
                border: none; border-radius: 12px; padding: 14px 24px;
            }}
            QPushButton:hover {{ opacity: 0.9; }}
        """)
        self.rec_btn.pressed.connect(self._start_rec)
        self.rec_btn.released.connect(self._stop_rec)
        lo.addWidget(self.rec_btn)
        
        # ── Actions ──
        acts = QHBoxLayout(); acts.setSpacing(8)
        for text, cb in [("📋  Paste", self._paste), ("📄  Copy", self._copy), ("🗑  Clear", lambda: self.output.clear())]:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"QPushButton{{background:{SURFACE};color:{TEXT2};border:1px solid {BORDER};padding:8px 14px;font-size:12px;}}QPushButton:hover{{background:{ACCENT_GLOW};color:{ACCENT};border-color:{ACCENT};}}")
            btn.clicked.connect(cb)
            acts.addWidget(btn)
        lo.addLayout(acts)
        
        # ── Footer ──
        foot = QHBoxLayout()
        self.mic_icon = QLabel("○")
        self.mic_icon.setStyleSheet(f"font-size: 14px; color: {TEXT3}; background: transparent;")
        foot.addWidget(self.mic_icon)
        foot.addStretch()
        version = QLabel("PROMPT-MINE  ·  v2.0")
        version.setStyleSheet(f"font-size: 9px; color: {TEXT3}; background: transparent;")
        foot.addWidget(version)
        lo.addLayout(foot)
        
        self.setCentralWidget(root)
        
        # Dragging
        self.drag_pos = None
        root.mousePressEvent = self._drag_start
        root.mouseMoveEvent = self._drag_move
    
    def _drag_start(self, e):
        if e.button() == Qt.LeftButton and e.position().y() < 60:
            self.drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
    def _drag_move(self, e):
        if e.buttons() == Qt.LeftButton and self.drag_pos:
            self.move(e.globalPosition().toPoint() - self.drag_pos)
    
    def _build_tray(self):
        self.tray = QSystemTrayIcon(self)
        m = QMenu()
        m.setStyleSheet(f"QMenu{{background:{CARD};border:1px solid {BORDER};border-radius:8px;padding:4px;}}QMenu::item{{padding:8px 20px;border-radius:4px;font-size:12px;}}QMenu::item:selected{{background:{ACCENT_GLOW};}}")
        m.addAction("🎙  Show EchoKeys").triggered.connect(lambda: (self.show(), self.raise_(), self.activateWindow()))
        m.addSeparator()
        m.addAction("Quit").triggered.connect(self._quit)
        self.tray.setContextMenu(m)
        self.tray.setToolTip("EchoKeys Pro — Alt+Space to record")
        self.tray.show()
    
    def _setup_hotkeys(self):
        keyboard.add_hotkey("alt+space", self._toggle_rec, suppress=True)
        mouse_listener = mouse.Listener(on_click=lambda x, y, btn, pressed: self._toggle_rec() if btn == mouse.Button.x1 and pressed else None)
        mouse_listener.daemon = True; mouse_listener.start()
    
    def _toggle_rec(self):
        if self.recording: self._stop_rec()
        else: self._start_rec()
    
    def _start_rec(self):
        if self.recording: return
        self.recording = True
        self.rec_btn.setText("⏺  Recording...")
        self.rec_btn.setStyleSheet(f"QPushButton{{background:{RED};color:white;font-weight:700;font-size:14px;border:none;border-radius:12px;padding:14px 24px;}}")
        self.indicator.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {RED}, stop:0.5 transparent, stop:1 {RED}); border-radius: 2px;")
        self.dot.setStyleSheet(f"font-size:9px;color:{RED};background:transparent;")
        self.stat.setText("Recording"); self.mic_icon.setText("●")
        self.mic_icon.setStyleSheet(f"font-size:14px;color:{RED};background:transparent;")
        threading.Thread(target=self._capture, daemon=True).start()
    
    def _stop_rec(self):
        if not self.recording: return
        self.recording = False
        self.rec_btn.setText("⏳  Transcribing...")
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
            path = os.path.join(tempfile.gettempdir(), "ek_capture.wav")
            wf = wave.open(path, 'wb')
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(16000)
            wf.writeframes(b''.join(frames)); wf.close()
            if os.path.getsize(path) > 1000:
                self.transcriber.path = path; self.transcriber.start()
        except Exception as e:
            self.output.setText(f"Mic error: {e}"); self._reset_ui()
    
    def _on_transcribed(self, text):
        if text.strip(): self.output.setText(text)
        self._reset_ui()
        if text.strip(): QTimer.singleShot(200, self._paste)
    
    def _reset_ui(self):
        self.rec_btn.setText("🎤  Hold to Record")
        self.rec_btn.setStyleSheet(f"QPushButton{{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {ACCENT},stop:1 {ACCENT2});color:{BG};font-weight:700;font-size:14px;border:none;border-radius:12px;padding:14px 24px;}}")
        self.indicator.setStyleSheet("background: transparent; border-radius: 2px;")
        self.dot.setStyleSheet(f"font-size:9px;color:{TEXT3};background:transparent;")
        self.stat.setText("Ready"); self.mic_icon.setText("○")
        self.mic_icon.setStyleSheet(f"font-size:14px;color:{TEXT3};background:transparent;")
    
    def _paste(self):
        t = self.output.toPlainText()
        if t.strip(): pyperclip.copy(t); QTimer.singleShot(80, lambda: keyboard.send("ctrl+v")); QTimer.singleShot(300, self.hide)
    def _copy(self):
        t = self.output.toPlainText()
        if t.strip(): pyperclip.copy(t); self.stat.setText("Copied!")
    def _quit(self):
        keyboard.unhook_all(); ctypes.windll.kernel32.SetThreadExecutionState(0x80000000); self.app.quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setApplicationName("EchoKeys Pro")
    app.setQuitOnLastWindowClosed(False)
    
    w = EchoKeysWindow(app)
    QTimer.singleShot(500, lambda: (w.show(), w.raise_(), w.activateWindow()))
    sys.exit(app.exec())