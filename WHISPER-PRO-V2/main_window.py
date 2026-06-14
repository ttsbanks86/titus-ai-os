"""MainWindow — Hidden coordinator managing HUD, Tray, Hotkeys, Transcriber"""
import sys
import time
import threading
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon, QMenu, QWidget
)
from PySide6.QtCore import Qt, QTimer, QUrl, Signal, QObject
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont

from constants import (
    BG, ACCENT, ACCENT2, TEXT, TEXT2, GREEN, RED, AMBER,
    AVAILABLE_MODES, COMMON_HOTKEYS, DATA_DIR
)
from settings import Settings
from model_manager import ModelManager
from transcriber import Transcriber
from hud_window import HUDWindow
from hotkey_manager import HotkeyManager
from vocab import get_vocab, add_word, remove_word, get_all_terms
from history import add_history, get_history, delete_history_item, clear_history, search_history
from stats import update_stats

class MainWindow(QMainWindow):
    """Hidden main window — manages tray, HUD, hotkeys, and transcription."""
    
    transcription_ready = Signal(str)
    status_update = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Whisper My Idea Pro")
        self.setFixedSize(1, 1)  # Minimal, hidden
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.hide()
        
        # Core components
        self.settings = Settings()
        self.transcriber = Transcriber(self.settings)
        self.hud = HUDWindow()
        self.settings_obj = Settings()  # For hotkey manager
        
        # State
        self._recording = False
        self._current_mode = self.settings.get("mode", "Voice")
        self._current_hotkey = self.settings.get("hotkey", "alt+space")
        
        # Initialize components
        self._setup_tray()
        self._setup_hotkeys()
        self._connect_signals()
        
        # Transcription thread
        self._transcribe_thread = None
        self._record_start_time = 0
        
        # Restore window position
        self._restore_geometry()

    def _setup_tray(self):
        """Create system tray icon with menu."""
        # Create icon
        px = QPixmap(32, 32)
        px.fill(Qt.transparent)
        p = QPainter(px)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor("#8b5cf6"))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(2, 2, 28, 28, 7, 7)
        p.setPen(QColor("white"))
        p.setFont(QFont("Segoe UI", 14, QFont.Bold))
        p.drawText(2, 2, 28, 28, Qt.AlignCenter, "W")
        p.end()
        
        self.tray = QSystemTrayIcon(QIcon(px), self)
        self.tray.setToolTip("Whisper My Idea Pro (Alt+Space)")
        
        # Build menu
        self._rebuild_tray()
        
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _rebuild_tray(self):
        """Rebuild tray menu with current settings."""
        s = self.settings
        menu = QMenu()
        
        # Toggle recording
        toggle_action = QAction("🎤  Start Recording" if not self._recording else "⏹  Stop Recording", self)
        toggle_action.triggered.connect(self._toggle_recording)
        menu.addAction(toggle_action)
        
        # Transcribe file
        transcribe_file_action = QAction("📂  Transcribe File...", self)
        transcribe_file_action.triggered.connect(self._transcribe_file)
        menu.addAction(transcribe_file_action)
        
        menu.addSeparator()
        
        # Modes submenu
        modes_menu = menu.addMenu("Mode")
        for mode in AVAILABLE_MODES:
            action = QAction(f"{'✓ ' if mode['id'] == self._current_mode else ''}{mode['icon']} {mode['label']}", self)
            action.triggered.connect(lambda checked, m=mode['id']: self._set_mode(m))
            modes_menu.addAction(action)
        
        menu.addSeparator()
        
        # Settings
        settings_action = QAction("⚙️ Settings", self)
        settings_action.triggered.connect(self._show_settings)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # Quit
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)
        
        self.tray.setContextMenu(menu)

    def _setup_hotkeys(self):
        """Register global hotkey."""
        import keyboard
        hotkey = self.settings.get("hotkey", "alt+space")
        self._current_hotkey = hotkey
        
        try:
            keyboard.remove_hotkey(hotkey)
        except:
            pass
        
        try:
            keyboard.add_hotkey(hotkey, self._on_hotkey, suppress=True)
            print(f"[MainWindow] Hotkey registered: {hotkey}")
        except Exception as e:
            print(f"[MainWindow] Hotkey register failed: {e}")

    def _connect_signals(self):
        self.transcription_ready.connect(self._on_transcription_ready)
        self.status_update.connect(self._on_status_update)

    def _on_hotkey(self):
        """Global hotkey triggered."""
        self._toggle_recording()

    def _toggle_recording(self):
        if not self._recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        """Start recording via HUD."""
        if self._recording:
            return
        
        self._recording = True
        self._record_start_time = time.time()
        
        # Start HUD
        self.hud.set_mode(self._current_mode)
        self.hud.start_recording(self._current_mode)
        self.hud.show()
        
        # Start recording in background thread
        self._transcribe_thread = threading.Thread(target=self._record_and_transcribe, daemon=True)
        self._transcribe_thread.start()
        
        # Update tray
        self._rebuild_tray()

    def _stop_recording(self):
        self.status_update.emit("Transcribing...")
        
        # Stop the recorder
        # (The actual stop is handled by the recording thread)

    def _record_and_transcribe(self):
        """Background thread: record audio, then transcribe."""
        try:
            # Start audio capture
            temp_path = self.transcriber.start_recording()
            if not temp_path:
                self.status_update.emit("Failed to start recording")
                self._recording = False
                return
            
            # Wait for stop signal
            while self._recording:
                time.sleep(0.1)
            
            # Stop recording
            audio_path = self.transcriber.stop_recording()
            if not audio_path:
                self.status_update.emit("No audio recorded")
                self._recording = False
                self._on_recording_done()
                return
            
            # Transcribe
            self.status_update.emit("Transcribing...")
            
            # Get model and language
            model_size = self.settings.get("model", "tiny")
            language = self.settings.get("language", "en")
            
            # Transcribe
            from transcriber import Transcriber
            transcriber = Transcriber(self.settings)
            transcriber.set_mode(self._current_mode)
            text = transcriber.transcribe_file(self._record_temp_path)
            
            # Apply mode formatting
            text = self._format_text(text)
            
            # Emit result
            self.transcription_ready.emit(text)
            
        except Exception as e:
            print(f"[MainWindow] Transcription error: {e}")
            self.status_update.emit(f"Error: {e}")
        finally:
            self._recording = False
            self._on_recording_done()

    def _on_recording_done(self):
        """Called when recording/transcription completes."""
        self.hud.stop_recording()
        self.hud.hide()
        self._recording = False
        self._rebuild_tray()

    def _on_transcription_ready(self, text: str):
        """Handle completed transcription."""
        if not text or text.startswith("Error") or text.startswith("No speech"):
            self.status_update.emit(text)
            return
        
        # Apply mode formatting
        text = self._format_text(text)
        
        # Update stats and history
        duration = time.time() - self._record_start_time if self._record_start_time else 0
        update_stats(text, duration)
        add_history(text, self._current_mode, time.time() - self._record_start_time)
        
        # Auto-paste
        if self.settings.get("auto_paste", True):
            self._auto_paste(text)
        
        # Update HUD
        self.hud.set_status("Done!")
        self.status_update.emit("Done!")

    def _format_text(self, text: str) -> str:
        """Apply mode-based formatting."""
        if not text:
            return text
        mode = self._current_mode
        if mode == "Email":
            return text.strip()
        elif mode == "Bullets":
            lines = [f"• {s.strip()}" for s in text.split(". ") if s.strip()]
            return "\n".join(lines)
        elif mode == "Meeting":
            return f"[Meeting Notes]\n{text}"
        elif mode == "Message":
            return text.strip()
        return text

    def _on_status_update(self, msg: str):
        self.hud.set_status(msg)

    def _format_text(self, text: str) -> str:
        return self._format_text(text)

    def _set_mode(self, mode: str):
        self._current_mode = mode
        self.settings.set("mode", mode)
        self.hud.set_mode(mode)
        self._rebuild_tray()

    def _transcribe_file(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(
            self, "Transcribe Audio File", "",
            "Audio Files (*.wav *.mp3 *.m4a *.ogg *.webm *.flac);;All Files (*.*)"
        )
        if not path:
            return
        
        self.status_update.emit("Transcribing file...")
        
        def transcribe():
            from transcriber import Transcriber
            transcriber = Transcriber(self.settings)
            transcriber.set_mode(self._current_mode)
            text = transcriber.transcribe_file(path)
            text = self._format_text(text)
            self.transcription_ready.emit(text)
        
        threading.Thread(target=lambda: self.transcription_ready.emit(self._format_text(
            Transcriber(self.settings).transcribe_file(self._get_selected_file_path())
        )), daemon=True).start()

    def _get_selected_file_path(self):
        # Would be stored from file dialog
        return ""

    def _show_settings(self):
        # Show settings window (TODO: implement settings dialog)
        pass

    def _quit(self):
        QApplication.quit()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._toggle_recording()

    def _restore_geometry(self):
        # Could save/restore window position
        pass

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def closeEvent(self, event):
        # Override to prevent closing
        event.ignore()
        self.hide()