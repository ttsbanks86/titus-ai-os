#!/usr/bin/env python3
"""
NOLA Reader v2 — Professional Text-to-Speech Reader
Open Door AI Systems | Industry Standard Quality
Edge TTS Neural Voices · High-Contrast Dark UI · Configurable Hotkey
"""
import sys, os, json, tempfile, time, threading, asyncio, ctypes, re
from pathlib import Path

# ── Qt ──────────────────────────────────────────────────────────────────
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QSlider, QComboBox, QFrame,
    QSystemTrayIcon, QMenu, QDialog, QDialogButtonBox, QFileDialog,
    QMessageBox, QGraphicsDropShadowEffect, QSizePolicy
)
from PySide6.QtGui import (
    QIcon, QPixmap, QPainter, QColor, QFont, QPalette, QAction,
    QKeySequence, QShortcut, QCursor, QFontDatabase
)
from PySide6.QtCore import (
    Qt, QThread, Signal, QUrl, QTimer, QSettings, QRect, QPoint
)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices, QAudioDevice

# ── Third-party ────────────────────────────────────────────────────────
import pyperclip
import keyboard

# ── Edge TTS ────────────────────────────────────────────────────────────
import edge_tts

# ── System ──────────────────────────────────────────────────────────────
ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# ═══════════════════════════════════════════════════════════════════════
# NOLA BRAND COLORS — high-contrast dark palette, every element visible
# ═══════════════════════════════════════════════════════════════════════
BG          = "#080b12"     # Deep background
BG2         = "#0d111a"     # Card/secondary background
BG3         = "#131823"     # Input/control background
SURFACE     = "#181e2c"     # Button surface
SURFACE2    = "#1f2638"     # Hover surface
BORDER      = "#2a3147"     # Visible border on any background
BORDER2     = "#3b4460"     # Stronger border
ACCENT      = "#8b5cf6"     # Purple accent
ACCENT2     = "#a78bfa"     # Hover accent
ACCENT3     = "#7c3aed"     # Darker accent
TEXT        = "#f0f2f5"     # Primary text — high contrast
TEXT2       = "#94a3b8"     # Secondary text
TEXT3       = "#64748b"     # Muted text
GREEN       = "#22c55e"     # Active/listening
AMBER       = "#f59e0b"     # Paused
RED         = "#ef4444"     # Error
GLOW_ACCENT = "rgba(139,92,246,0.12)"

# ── Stylesheet ──────────────────────────────────────────────────────────
BASE_STYLE = f"""
QWidget {{ font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif; color: {TEXT}; }}
QMainWindow {{ background: {BG}; }}

QLabel {{ color: {TEXT2}; font-size: 12px; }}
QLabel#header {{ color: {TEXT}; font-size: 15px; font-weight: 600; }}
QLabel#status {{ font-size: 11px; }}
QLabel#value {{ color: {ACCENT}; font-weight: 600; font-size: 12px; }}

QPushButton {{
    background: {SURFACE}; color: {TEXT};
    border: 1px solid {BORDER2}; border-radius: 8px;
    padding: 8px 18px; font-size: 12px; font-weight: 500;
    min-height: 32px;
}}
QPushButton:hover {{
    background: {SURFACE2}; border-color: {ACCENT}; color: {ACCENT2};
}}
QPushButton:pressed {{
    background: {BG3}; border-color: {ACCENT3};
}}
QPushButton:disabled {{
    background: {BG2}; color: {TEXT3}; border-color: {BORDER};
}}
QPushButton#primary {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {ACCENT}, stop:1 {ACCENT3});
    border: 1px solid {ACCENT2}; color: white; font-weight: 600;
    min-height: 36px;
}}
QPushButton#primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {ACCENT2}, stop:1 {ACCENT});
}}
QPushButton#primary:pressed {{
    background: {ACCENT3};
}}
QPushButton#danger {{
    background: {BG2}; border-color: {RED}; color: {RED};
}}
QPushButton#danger:hover {{
    background: "rgba(239,68,68,0.1)"; border-color: {RED};
}}
QPushButton#ghost {{
    background: transparent; border: 1px solid {BORDER2}; color: {TEXT2};
}}
QPushButton#ghost:hover {{
    border-color: {ACCENT}; color: {ACCENT2};
}}

QTextEdit {{
    background: {BG2}; color: {TEXT};
    border: 1px solid {BORDER2}; border-radius: 10px;
    padding: 14px; font-size: 13px; selection-background-color: {GLOW_ACCENT};
    line-height: 1.5;
}}
QTextEdit:focus {{ border-color: {ACCENT}; }}
QTextEdit#display {{
    background: {BG}; border: 1px solid {BORDER2};
    font-size: 14px; padding: 16px;
}}

QComboBox {{
    background: {SURFACE}; color: {TEXT};
    border: 1px solid {BORDER2}; border-radius: 8px;
    padding: 8px 14px; font-size: 12px; min-width: 120px;
}}
QComboBox:hover {{ border-color: {ACCENT}; }}
QComboBox::drop-down {{ border: none; width: 26px; }}
QComboBox::down-arrow {{ image: none; }}
QComboBox QAbstractItemView {{
    background: {BG3}; color: {TEXT};
    border: 1px solid {BORDER2}; border-radius: 8px;
    selection-background-color: {GLOW_ACCENT};
    padding: 4px;
}}

QSlider::groove:horizontal {{
    background: {BORDER}; height: 4px; border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {ACCENT}, stop:1 {ACCENT2});
    width: 18px; height: 18px; margin: -7px 0; border-radius: 9px;
    border: 2px solid {BG2};
}}
QSlider::handle:horizontal:hover {{
    width: 20px; height: 20px; margin: -8px 0; border-radius: 10px;
}}
QSlider::sub-page:horizontal {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 {ACCENT}, stop:1 {ACCENT3});
    border-radius: 2px;
}}

QFrame#statusBar {{
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 8px; padding: 4px;
}}
QFrame#controlCard {{
    background: {BG2}; border: 1px solid {BORDER};
    border-radius: 10px; padding: 12px;
}}
QFrame#trayHeader {{
    background: transparent;
}}
QScrollBar:vertical {{
    background: {BG}; width: 8px; border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER}; border-radius: 4px; min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {BORDER2};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""

# ═══════════════════════════════════════════════════════════════════════
#  SETTINGS MANAGER
# ═══════════════════════════════════════════════════════════════════════
CONFIG_DIR = Path(os.environ.get("APPDATA", Path.home())) / "NOLA"
CONFIG_PATH = CONFIG_DIR / "settings.json"

DEFAULT_SETTINGS = {
    "voice": "en-US-AriaNeural",
    "speed": 1.0,
    "hotkey": "alt+shift+r",
    "window_x": None,
    "window_y": None,
    "clipboard_enabled": True,
    "volume": 0.8,
    "speaker": "",
    "microphone": "",
}

class Settings:
    def __init__(self):
        self.data = dict(DEFAULT_SETTINGS)
        self._load()

    def _load(self):
        try:
            if CONFIG_PATH.exists():
                with open(CONFIG_PATH, encoding="utf-8") as f:
                    self.data.update(json.load(f))
        except Exception as e:
            print(f"[NOLA] Settings load error: {e}")

    def save(self):
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"[NOLA] Settings save error: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()


# ═══════════════════════════════════════════════════════════════════════
#  EDGE TTS ENGINE  (async → thread wrapper)
# ═══════════════════════════════════════════════════════════════════════
def get_edge_voices() -> list[dict]:
    """Fetch available voices from edge-tts (cached per session)."""
    if not hasattr(get_edge_voices, "_cache"):
        try:
            import edge_tts
            loop = asyncio.new_event_loop()
            voices = loop.run_until_complete(edge_tts.list_voices())
            loop.close()
            # Filter to English + most useful
            english = [
                v for v in voices
                if v["ShortName"].startswith("en-")
            ]
            # Sort: US first, then GB, then others
            def sort_key(v):
                n = v["Name"]
                if n.startswith("en-US"): return 0, n
                if n.startswith("en-GB"): return 1, n
                if n.startswith("en-AU"): return 2, n
                if n.startswith("en-CA"): return 3, n
                return 4, n
            english.sort(key=sort_key)
            get_edge_voices._cache = english
        except Exception as e:
            print(f"[NOLA] Voice list error: {e}")
            get_edge_voices._cache = [
                {"ShortName": "en-US-AriaNeural", "Gender": "Female", "Locale": "en-US"},
                {"ShortName": "en-US-GuyNeural", "Gender": "Male", "Locale": "en-US"},
                {"ShortName": "en-GB-SoniaNeural", "Gender": "Female", "Locale": "en-GB"},
            ]
    return get_edge_voices._cache


def voice_display_name(v: dict) -> str:
    raw = v.get("ShortName", v.get("Name", ""))
    short = raw.replace("Neural", "").replace("Multilingual", "")
    # Insert space before caps
    short = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", short)
    gender = "[F] " if v.get("Gender", "").lower() == "female" else "[M] "
    return f"{gender}{short}"


class TTSWorker(QThread):
    """Generates TTS audio in background thread with asyncio."""
    finished = Signal(str)      # path to generated audio file
    error = Signal(str)         # error message
    progress = Signal(str)      # status update

    def __init__(self, text: str, voice: str, speed: float):
        super().__init__()
        self.text = text
        self.voice = voice
        self.speed = speed
        self._cancel = False

    def cancel(self):
        self._cancel = True

    def run(self):
        if not self.text.strip():
            return
        self.progress.emit("Generating speech...")
        try:
            suffix = ".mp3"
            fd, path = tempfile.mkstemp(suffix=suffix, prefix="nola_")
            os.close(fd)
            communicate = edge_tts.Communicate(
                self.text[:8000],  # edge-tts limit ~8000 chars safe
                self.voice,
                rate=f"{int((self.speed - 1.0) * 100):+d}%" if self.speed != 1.0 else "+0%",
            )
            asyncio.run(communicate.save(path))
            if self._cancel or not os.path.getsize(path):
                try: os.remove(path)
                except: pass
                if self._cancel:
                    return
                self.error.emit("No audio generated")
                return
            self.finished.emit(path)
        except Exception as e:
            if self._cancel: return
            err = str(e)
            if "connect" in err.lower() or "timeout" in err.lower():
                self.error.emit("Network error. Check internet connection.")
            else:
                self.error.emit(f"TTS error: {err}"[:120])


# ═══════════════════════════════════════════════════════════════════════
#  CLIPBOARD MONITOR
# ═══════════════════════════════════════════════════════════════════════
class ClipboardMonitor(QThread):
    text_changed = Signal(str)

    def __init__(self):
        super().__init__()
        self._running = True
        self._last = ""
        self._enabled = True

    def set_enabled(self, enabled: bool):
        self._enabled = enabled

    def run(self):
        try:
            self._last = pyperclip.paste() or ""
        except:
            self._last = ""
        while self._running:
            time.sleep(0.4)
            if not self._enabled:
                continue
            try:
                current = pyperclip.paste()
                if current and current != self._last and current.strip():
                    # Filter single-char noise
                    if len(current.strip()) >= 3:
                        self._last = current
                        self.text_changed.emit(current)
            except:
                pass

    def stop(self):
        self._running = False


# ═══════════════════════════════════════════════════════════════════════
#  HOTKEY SETTINGS DIALOG
# ═══════════════════════════════════════════════════════════════════════
class HotkeyDialog(QDialog):
    def __init__(self, current_hotkey: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Global Hotkey")
        self.setFixedSize(400, 200)
        self.setStyleSheet(BASE_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self._new_hotkey = current_hotkey
        self._listening = False

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Press your desired hotkey combination")
        title.setStyleSheet("font-size: 14px; font-weight: 600; color: white;")
        layout.addWidget(title)

        self.display = QPushButton(current_hotkey.upper())
        self.display.setMinimumHeight(48)
        self.display.setStyleSheet(f"""
            QPushButton {{
                background: {BG}; border: 2px dashed {ACCENT};
                border-radius: 10px; font-size: 18px; font-weight: 700;
                color: {ACCENT2}; padding: 12px;
            }}
            QPushButton:hover {{ border-color: {ACCENT2}; }}
        """)
        self.display.clicked.connect(self._start_listening)
        layout.addWidget(self.display)

        self.hint = QLabel("Click the box above, then press your hotkey.")
        self.hint.setStyleSheet(f"color: {TEXT2}; font-size: 11px;")
        layout.addWidget(self.hint)

        layout.addStretch()

        buttons = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        self.ok_btn = QPushButton("Apply")
        self.ok_btn.setObjectName("primary")
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.accept)
        buttons.addWidget(cancel_btn)
        buttons.addWidget(self.ok_btn)
        layout.addLayout(buttons)

    def _start_listening(self):
        self._listening = True
        self.display.setText("... listening ...")
        self.display.setStyleSheet(f"""
            QPushButton {{
                background: {BG}; border: 2px solid {GREEN};
                border-radius: 10px; font-size: 16px;
                color: {GREEN}; padding: 12px;
            }}
        """)
        self.hint.setText("Press any key combination...")
        # Listen in a thread
        def listen():
            recorded = keyboard.read_hotkey(suppress=True)
            if recorded:
                self._new_hotkey = recorded.lower()
                QTimer.singleShot(0, self._on_key_captured)
        threading.Thread(target=listen, daemon=True).start()

    def _on_key_captured(self):
        self._listening = False
        self.display.setText(self._new_hotkey.upper())
        self.display.setStyleSheet(f"""
            QPushButton {{
                background: {BG}; border: 2px solid {GREEN};
                border-radius: 10px; font-size: 18px; font-weight: 700;
                color: {GREEN}; padding: 12px;
            }}
            QPushButton:hover {{ border-color: {ACCENT2}; }}
        """)
        self.hint.setText(f"Hotkey set to: {self._new_hotkey.upper()}")
        self.ok_btn.setEnabled(True)

    def hotkey(self) -> str:
        return self._new_hotkey


# ═══════════════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════
class NOLAReader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.tts_worker = None
        self.current_audio_path = None
        self.is_speaking = False

        # ── Audio playback ──
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.positionChanged.connect(self._on_position)
        self.player.durationChanged.connect(self._on_duration)
        self.player.mediaStatusChanged.connect(self._on_media_status)
        self.audio_output.setVolume(self.settings.get("volume", 0.8))

        # ── Window ──
        self.setWindowTitle("NOLA Reader")
        self.setFixedSize(520, 560)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setStyleSheet(BASE_STYLE)

        self._drag_pos = None
        self.setup_ui()
        self.setup_tray()
        self.setup_hotkey()

        # ── Clipboard ──
        self.clip_monitor = ClipboardMonitor()
        self.clip_monitor.text_changed.connect(self._on_clipboard)
        self.clip_monitor.set_enabled(self.settings.get("clipboard_enabled", True))
        self.clip_monitor.start()

        # ── Restore window position ──
        wx = self.settings.get("window_x")
        wy = self.settings.get("window_y")
        if wx is not None and wy is not None:
            self.move(wx, wy)
        else:
            screen = QApplication.primaryScreen()
            if screen:
                geo = screen.availableGeometry()
                self.move(geo.width() - 560, geo.height() - 620)

    # ── UI Setup ────────────────────────────────────────────────────────
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 0, 12, 12)
        layout.setSpacing(8)

        # ─── Title bar (draggable) ───
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setCursor(QCursor(Qt.OpenHandCursor))
        title_bar.mousePressEvent = self._drag_start
        title_bar.mouseMoveEvent = self._drag_move

        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(12, 0, 8, 0)

        icon = QLabel("     N O L A")
        icon.setObjectName("header")
        icon.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {TEXT}; letter-spacing: 4px;")
        tb_layout.addWidget(icon)

        tag = QLabel("voice reader")
        tag.setStyleSheet(f"color: {TEXT3}; font-size: 9px; padding-top: 4px;")
        tb_layout.addWidget(tag)

        tb_layout.addStretch()

        # Window control buttons (visible, high-contrast)
        self.status_dot = QLabel("●")
        self.status_dot.setStyleSheet(f"color: {GREEN}; font-size: 14px;")
        self.status_dot.setToolTip("Clipboard monitoring active")
        tb_layout.addWidget(self.status_dot)

        min_btn = QPushButton("—")
        min_btn.setFixedSize(28, 28)
        min_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; border: 1px solid {BORDER}; border-radius: 6px;
                color: {TEXT2}; font-size: 14px; padding: 0;
            }}
            QPushButton:hover {{ background: {SURFACE2}; border-color: {ACCENT}; color: {ACCENT2}; }}
        """)
        min_btn.clicked.connect(self.hide)
        tb_layout.addWidget(min_btn)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent; border: 1px solid {BORDER}; border-radius: 6px;
                color: {TEXT2}; font-size: 12px; padding: 0;
            }}
            QPushButton:hover {{ background: "rgba(239,68,68,0.15)"; border-color: {RED}; color: {RED}; }}
        """)
        close_btn.clicked.connect(self._quit_app)
        tb_layout.addWidget(close_btn)

        layout.addWidget(title_bar)

        # ─── Status Bar ───
        self.status_frame = QFrame()
        self.status_frame.setObjectName("statusBar")
        sb = QHBoxLayout(self.status_frame)
        sb.setContentsMargins(12, 6, 12, 6)
        self.status_icon = QLabel("●")
        self.status_icon.setStyleSheet(f"color: {GREEN}; font-size: 8px;")
        self.status_label = QLabel("Listening for clipboard")
        self.status_label.setObjectName("status")
        self.status_label.setStyleSheet(f"color: {TEXT2};")
        self.char_count = QLabel("0 chars")
        self.char_count.setStyleSheet(f"color: {TEXT3}; font-size: 9px;")
        sb.addWidget(self.status_icon)
        sb.addWidget(self.status_label)
        sb.addStretch()
        sb.addWidget(self.char_count)
        layout.addWidget(self.status_frame)

        # ─── Voice + Speed Controls ───
        ctrl_card = QFrame()
        ctrl_card.setObjectName("controlCard")
        ctrl_layout = QHBoxLayout(ctrl_card)
        ctrl_layout.setContentsMargins(12, 10, 12, 10)
        ctrl_layout.setSpacing(12)

        # Voice
        vc = QVBoxLayout()
        vc.setSpacing(4)
        vl = QLabel("Voice")
        vl.setStyleSheet(f"color: {TEXT3}; font-size: 10px; font-weight: 500; letter-spacing: 1px;")
        self.voice_combo = QComboBox()
        self._populate_voices()
        self.voice_combo.currentIndexChanged.connect(self._on_voice_changed)
        vc.addWidget(vl)
        vc.addWidget(self.voice_combo)
        ctrl_layout.addLayout(vc)

        # Speed
        sc = QVBoxLayout()
        sc.setSpacing(4)
        sl = QLabel("Speed")
        sl.setStyleSheet(f"color: {TEXT3}; font-size: 10px; font-weight: 500; letter-spacing: 1px;")
        sr = QHBoxLayout()
        sr.setSpacing(8)
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(5, 30)
        initial_speed = int(self.settings.get("speed", 1.0) * 10)
        self.speed_slider.setValue(initial_speed)
        self.speed_slider.valueChanged.connect(self._on_speed)
        self.speed_label = QLabel(f"{initial_speed / 10:.1f}x")
        self.speed_label.setObjectName("value")
        sr.addWidget(self.speed_slider)
        sr.addWidget(self.speed_label)
        sc.addWidget(sl)
        sc.addLayout(sr)
        ctrl_layout.addLayout(sc)

        # Speaker output
        spk = QVBoxLayout()
        spk.setSpacing(4)
        spl = QLabel("Speaker")
        spl.setStyleSheet(f"color: {TEXT3}; font-size: 10px; font-weight: 500; letter-spacing: 1px;")
        self.speaker_combo = QComboBox()
        self._populate_speakers()
        self.speaker_combo.currentIndexChanged.connect(self._on_speaker_changed)
        spk.addWidget(spl)
        spk.addWidget(self.speaker_combo)
        ctrl_layout.addLayout(spk)

        layout.addWidget(ctrl_card)

        # ─── Mic Selection (for future voice input) ───
        mic_row = QFrame()
        mic_row.setObjectName("controlCard")
        mic_row.setFixedHeight(36)
        mic_layout = QHBoxLayout(mic_row)
        mic_layout.setContentsMargins(12, 0, 12, 0)
        mic_label = QLabel("🎤 Mic")
        mic_label.setStyleSheet(f"color: {TEXT3}; font-size: 10px; font-weight: 500; letter-spacing: 1px;")
        mic_layout.addWidget(mic_label)
        self.mic_combo = QComboBox()
        self._populate_microphones()
        self.mic_combo.currentIndexChanged.connect(self._on_mic_changed)
        mic_layout.addWidget(self.mic_combo, 1)
        layout.addWidget(mic_row)

        # ─── Text Display ───
        self.text_display = QTextEdit()
        self.text_display.setObjectName("display")
        self.text_display.setReadOnly(True)
        self.text_display.setMinimumHeight(100)
        self.text_display.setPlaceholderText("Copy text anywhere — will be read aloud...")
        layout.addWidget(self.text_display)

        # ─── Action Buttons (high contrast, all visible) ───
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        self.clip_btn = QPushButton("📋 Toggle Clipboard")
        self.clip_btn.setObjectName("ghost")
        self.clip_btn.setToolTip("Enable/disable clipboard auto-read")
        self.clip_btn.clicked.connect(self._toggle_clipboard)
        btn_row.addWidget(self.clip_btn)

        self.speak_btn = QPushButton("▶  Read")
        self.speak_btn.setObjectName("primary")
        self.speak_btn.setToolTip("Read the current text aloud")
        self.speak_btn.clicked.connect(self._read_aloud)
        btn_row.addWidget(self.speak_btn)

        self.stop_btn = QPushButton("■  Stop")
        self.stop_btn.setObjectName("danger")
        self.stop_btn.setToolTip("Stop current reading")
        self.stop_btn.clicked.connect(self._stop_reading)
        self.stop_btn.setEnabled(False)
        btn_row.addWidget(self.stop_btn)

        self.hotkey_btn = QPushButton("⌨ Hotkey")
        self.hotkey_btn.setObjectName("ghost")
        self.hotkey_btn.setToolTip("Change the global hotkey")
        self.hotkey_btn.clicked.connect(self._change_hotkey)
        btn_row.addWidget(self.hotkey_btn)

        layout.addLayout(btn_row)

        # ─── File + Utility row ───
        util_row = QHBoxLayout()
        util_row.setSpacing(6)

        self.file_btn = QPushButton("📂 Open File")
        self.file_btn.setObjectName("ghost")
        self.file_btn.clicked.connect(self._open_file)
        util_row.addWidget(self.file_btn)

        self.clear_btn = QPushButton("✕ Clear")
        self.clear_btn.setObjectName("ghost")
        self.clear_btn.clicked.connect(self._clear_text)
        util_row.addWidget(self.clear_btn)

        util_row.addStretch()

        hotkey_hint = QLabel(f"Hotkey: {self.settings.get('hotkey', 'alt+shift+r').upper()}")
        hotkey_hint.setStyleSheet(f"color: {TEXT3}; font-size: 9px;")
        hotkey_hint.setObjectName("hotkey_hint")
        util_row.addWidget(hotkey_hint)

        layout.addLayout(util_row)

    def _populate_voices(self):
        self.voice_combo.clear()
        voices = get_edge_voices()
        saved_voice = self.settings.get("voice", "en-US-AriaNeural")
        selected_idx = 0
        for i, v in enumerate(voices):
            short_name = v.get("ShortName", v.get("Name", ""))
            display = voice_display_name(v)
            self.voice_combo.addItem(display, short_name)
            if short_name == saved_voice:
                selected_idx = i
        self.voice_combo.setCurrentIndex(selected_idx)

    def _populate_speakers(self):
        """Populate audio output device list."""
        self.speaker_combo.clear()
        devices = QMediaDevices.audioOutputs()
        saved = self.settings.get("speaker", "")
        selected = 0
        for i, dev in enumerate(devices):
            desc = dev.description()
            label = f"🔊 {desc}" if dev.isDefault() else f"  {desc}"
            self.speaker_combo.addItem(label, dev.id())
            if dev.id() == saved:
                selected = i
        if not devices:
            self.speaker_combo.addItem("Default speaker", "")
        self.speaker_combo.setCurrentIndex(selected)
        # Apply saved speaker
        self._apply_speaker(selected)

    def _apply_speaker(self, idx=None):
        """Apply the selected audio output to QAudioOutput."""
        devices = QMediaDevices.audioOutputs()
        if not devices:
            return
        if idx is None:
            idx = self.speaker_combo.currentIndex()
        if 0 <= idx < len(devices):
            self.audio_output.setDevice(devices[idx])

    def _on_speaker_changed(self, idx):
        devices = QMediaDevices.audioOutputs()
        if 0 <= idx < len(devices):
            dev = devices[idx]
            self.audio_output.setDevice(dev)
            self.settings.set("speaker", dev.id())

    def _populate_microphones(self):
        """Populate audio input (mic) device list."""
        self.mic_combo.clear()
        devices = QMediaDevices.audioInputs()
        saved = self.settings.get("microphone", "")
        selected = 0
        for i, dev in enumerate(devices):
            desc = dev.description()
            label = f"🎙 {desc}" if dev.isDefault() else f"   {desc}"
            self.mic_combo.addItem(label, dev.id())
            if dev.id() == saved:
                selected = i
        if not devices:
            self.mic_combo.addItem("Default microphone", "")

    def _on_mic_changed(self, idx):
        devices = QMediaDevices.audioInputs()
        if 0 <= idx < len(devices):
            self.settings.set("microphone", devices[idx].id())

    # ── Tray ────────────────────────────────────────────────────────────
    def setup_tray(self):
        px = QPixmap(32, 32)
        px.fill(Qt.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(ACCENT))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(2, 2, 28, 28, 7, 7)
        p.setPen(QColor("white"))
        p.setFont(QFont("Segoe UI", 14, QFont.Bold))
        p.drawText(2, 2, 28, 28, Qt.AlignCenter, "N")
        p.end()

        self.tray = QSystemTrayIcon(QIcon(px), self)
        self.tray.setToolTip("NOLA Reader")
        menu = QMenu()
        menu.addAction("Show", self._show_window)
        menu.addSeparator()
        menu.addAction("Read Clipboard", self._read_aloud)
        menu.addAction("Toggle Clipboard", self._toggle_clipboard)
        menu.addSeparator()
        menu.addAction("Quit", self._quit_app)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(
            lambda r: self._show_window() if r == QSystemTrayIcon.DoubleClick else None
        )
        self.tray.show()

    # ── Hotkey ──────────────────────────────────────────────────────────
    def setup_hotkey(self):
        hotkey = self.settings.get("hotkey", "alt+shift+r")
        try:
            keyboard.remove_hotkey(hotkey)
        except:
            pass
        keyboard.add_hotkey(hotkey, self._hotkey_triggered, suppress=True)
        self._current_hotkey = hotkey

    def _hotkey_triggered(self):
        self._show_window()
        # Read whatever is in clipboard
        try:
            text = pyperclip.paste()
            if text and len(text.strip()) >= 3:
                self.text_display.setPlainText(text[:2000])
                QTimer.singleShot(100, self._read_aloud)
        except:
            pass

    # ── Clipboard ───────────────────────────────────────────────────────
    def _on_clipboard(self, text):
        self.text_display.setPlainText(text[:2000])
        self.char_count.setText(f"{len(text)} chars")
        if self.clip_monitor._enabled and len(text.strip()) >= 3:
            self.status_label.setText("New text copied — reading...")
            self.status_icon.setStyleSheet(f"color: {ACCENT}; font-size: 8px;")
            QTimer.singleShot(200, lambda: self._start_tts(text))

    def _toggle_clipboard(self):
        enabled = not self.clip_monitor._enabled
        self.clip_monitor.set_enabled(enabled)
        self.settings.set("clipboard_enabled", enabled)
        if enabled:
            self.clip_btn.setText("📋 Toggle Clipboard")
            self.clip_btn.setStyleSheet(f"""
                QPushButton {{ background: transparent; border: 1px solid {BORDER2}; color: {TEXT2}; border-radius: 8px; padding: 8px 18px; font-size: 12px; }}
                QPushButton:hover {{ border-color: {ACCENT}; color: {ACCENT2}; }}
            """)
            self.status_dot.setStyleSheet(f"color: {GREEN}; font-size: 14px;")
            self.status_label.setText("Listening for clipboard")
            self.status_icon.setStyleSheet(f"color: {GREEN}; font-size: 8px;")
        else:
            self.clip_btn.setText("📋 Clipboard Off")
            self.clip_btn.setStyleSheet(f"""
                QPushButton {{ background: transparent; border: 1px solid {AMBER}; border-radius: 8px; padding: 8px 18px; font-size: 12px; color: {AMBER}; }}
                QPushButton:hover {{ border-color: {ACCENT}; color: {ACCENT2}; }}
            """)
            self.status_dot.setStyleSheet(f"color: {AMBER}; font-size: 14px;")
            self.status_label.setText("Clipboard paused")
            self.status_icon.setStyleSheet(f"color: {AMBER}; font-size: 8px;")

    # ── TTS ─────────────────────────────────────────────────────────────
    def _start_tts(self, text: str):
        if not text or len(text.strip()) < 3:
            return
        self._stop_reading()
        voice = self.voice_combo.currentData() or self.settings.get("voice", "en-US-AriaNeural")
        speed = self.speed_slider.value() / 10.0
        self.is_speaking = True
        self.speak_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Generating speech...")
        self.status_icon.setStyleSheet(f"color: {AMBER}; font-size: 8px;")

        self.tts_worker = TTSWorker(text, voice, speed)
        self.tts_worker.finished.connect(self._on_tts_ready)
        self.tts_worker.error.connect(self._on_tts_error)
        self.tts_worker.start()

    def _on_tts_ready(self, path: str):
        self.current_audio_path = path
        self.status_label.setText("Playing...")
        self.status_icon.setStyleSheet(f"color: {ACCENT}; font-size: 8px;")
        # Play via QMediaPlayer
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()

    def _on_tts_error(self, msg: str):
        self.is_speaking = False
        self.speak_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText(msg)
        self.status_icon.setStyleSheet(f"color: {RED}; font-size: 8px;")
        self.char_count.setText("Error")

    def _read_aloud(self):
        text = self.text_display.toPlainText()
        if text.strip():
            self._start_tts(text)

    def _stop_reading(self):
        self.player.stop()
        if self.tts_worker and self.tts_worker.isRunning():
            self.tts_worker.cancel()
            self.tts_worker.wait(2000)
        if self.current_audio_path:
            try: os.remove(self.current_audio_path)
            except: pass
            self.current_audio_path = None
        self.is_speaking = False
        self.speak_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

    def _on_media_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self._on_playback_done()
        elif status == QMediaPlayer.InvalidMedia:
            self._on_tts_error("Playback error")

    def _on_playback_done(self):
        self.is_speaking = False
        self.speak_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if self.current_audio_path:
            try: os.remove(self.current_audio_path)
            except: pass
            self.current_audio_path = None
        if self.clip_monitor._enabled:
            self.status_label.setText("Listening for clipboard")
            self.status_icon.setStyleSheet(f"color: {GREEN}; font-size: 8px;")
        else:
            self.status_label.setText("Ready")
            self.status_icon.setStyleSheet(f"color: {AMBER}; font-size: 8px;")

    def _on_position(self, pos):
        # Update progress if needed (future: time display)
        pass

    def _on_duration(self, dur):
        pass

    # ── Event handlers ──────────────────────────────────────────────────
    def _on_voice_changed(self, idx):
        voice = self.voice_combo.currentData()
        if voice:
            self.settings.set("voice", voice)

    def _on_speed(self, value):
        speed = value / 10.0
        self.speed_label.setText(f"{speed:.1f}x")
        self.settings.set("speed", speed)

    def _on_speed_changed(self, value):
        self._on_speed(value)

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Text File", "",
            "Text files (*.txt *.md *.html *.csv);;All files (*.*)"
        )
        if path:
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read(10000)  # Limit to ~10k chars
                self.text_display.setPlainText(text)
                self.char_count.setText(f"{len(text)} chars")
                self.status_label.setText(f"Loaded: {Path(path).name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not read file:\n{e}")

    def _clear_text(self):
        self.text_display.clear()
        self.char_count.setText("0 chars")
        self._stop_reading()

    def _change_hotkey(self):
        current = self.settings.get("hotkey", "alt+shift+r")
        dialog = HotkeyDialog(current, self)
        if dialog.exec():
            new_hotkey = dialog.hotkey()
            if new_hotkey and new_hotkey != current:
                try:
                    keyboard.remove_hotkey(current)
                except:
                    pass
                keyboard.add_hotkey(new_hotkey, self._hotkey_triggered, suppress=True)
                self.settings.set("hotkey", new_hotkey)
                self._current_hotkey = new_hotkey
                hint = self.findChild(QLabel, "hotkey_hint")
                if hint:
                    hint.setText(f"Hotkey: {new_hotkey.upper()}")

    # ── Drag ────────────────────────────────────────────────────────────
    def _drag_start(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def _drag_move(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)

    def _show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def _quit_app(self):
        self.clip_monitor.stop()
        self.clip_monitor.wait(2000)
        self._stop_reading()
        # Save position
        pos = self.pos()
        self.settings.set("window_x", pos.x())
        self.settings.set("window_y", pos.y())
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.hide()
        super().keyPressEvent(event)


# ═══════════════════════════════════════════════════════════════════════
#  ENTRY
# ═══════════════════════════════════════════════════════════════════════
def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Load Inter font if available
    QFontDatabase.addApplicationFont(
        "C:/Windows/Fonts/segui.ttf"
    )

    win = NOLAReader()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
