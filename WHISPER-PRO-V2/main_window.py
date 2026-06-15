"""MainWindow — Hidden coordinator for SuperWhisper-style voice overlay."""

import time
import threading
import ctypes
from ctypes import wintypes
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon, QMenu, QDialog, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QCheckBox, QDialogButtonBox, QFormLayout,
    QLineEdit, QMessageBox, QTabWidget, QWidget, QSpinBox, QSlider
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QIcon, QAction, QPixmap, QPainter, QColor, QFont

from constants import AVAILABLE_MODES, AVAILABLE_MODELS, COMMON_HOTKEYS, APP_DIR, DATA_DIR
from settings import Settings
from transcriber import Transcriber
from hud_window import HUDWindow
from hotkey_manager import HotkeyManager
from stats import update_stats
from history import add_history


class SettingsDialog(QDialog):
    """Native settings panel for overlay, hotkeys, audio, and transcription."""

    def __init__(self, settings: Settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.setWindowTitle("Whisper My Idea Pro Settings")
        self.setMinimumWidth(560)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        tabs = QTabWidget()
        tabs.addTab(self._hotkey_tab(), "Hotkeys")
        tabs.addTab(self._appearance_tab(), "Appearance")
        tabs.addTab(self._audio_tab(), "Audio")
        tabs.addTab(self._transcription_tab(), "Transcription")
        tabs.addTab(self._behavior_tab(), "Behavior")
        root.addWidget(tabs)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

    def _hotkey_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        self.start_hotkey = self._hotkey_combo(self.settings.get("start_hotkey", self.settings.get("hotkey", "mouse_middle")))
        self.stop_hotkey = self._hotkey_combo(self.settings.get("stop_hotkey", "shift+z"))
        self.cancel_hotkey = self._hotkey_combo(self.settings.get("cancel_hotkey", "esc"))
        form.addRow("Start recording", self.start_hotkey)
        form.addRow("Stop recording", self.stop_hotkey)
        form.addRow("Cancel recording", self.cancel_hotkey)
        note = QLabel("Use mouse_middle for the middle mouse/track button. Custom keyboard combos like ctrl+shift+space also work.")
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748b;")
        form.addRow("", note)
        return page

    def _appearance_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        self.overlay_width = QSpinBox()
        self.overlay_width.setRange(600, 800)
        self.overlay_width.setSingleStep(20)
        self.overlay_width.setValue(int(self.settings.get("overlay_width", 680)))
        form.addRow("Overlay width", self.overlay_width)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(75, 100)
        self.opacity_slider.setValue(int(float(self.settings.get("overlay_opacity", 0.94)) * 100))
        form.addRow("Transparency", self.opacity_slider)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Glass Dark"])
        self.theme_combo.setCurrentText(self.settings.get("theme", "Glass Dark"))
        form.addRow("Theme", self.theme_combo)

        self.position_combo = QComboBox()
        self.position_combo.addItems(["center", "custom"])
        self.position_combo.setCurrentText(self.settings.get("overlay_position", "center"))
        form.addRow("Position", self.position_combo)
        note = QLabel("Tip: drag the floating overlay with the left mouse button to place it anywhere. The app remembers that position.")
        note.setWordWrap(True)
        note.setStyleSheet("color: #64748b;")
        form.addRow("", note)
        return page

    def _audio_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        self.microphone_combo = QComboBox()
        self.microphone_combo.addItem("System default", "")
        try:
            import sounddevice as sd
            for index, device in enumerate(sd.query_devices()):
                if device.get("max_input_channels", 0) > 0:
                    self.microphone_combo.addItem(f"{index}: {device['name']}", str(index))
        except Exception:
            pass
        self._set_combo_by_data(self.microphone_combo, str(self.settings.get("microphone", "")))
        form.addRow("Microphone", self.microphone_combo)

        self.noise_check = QCheckBox("Noise suppression")
        self.noise_check.setChecked(bool(self.settings.get("noise_suppression", True)))
        form.addRow("", self.noise_check)

        self.vad_check = QCheckBox("Voice activity detection")
        self.vad_check.setChecked(bool(self.settings.get("voice_activity_detection", True)))
        form.addRow("", self.vad_check)
        return page

    def _transcription_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Faster-Whisper", "Whisper", "OpenAI", "OpenRouter", "Local model"])
        self.engine_combo.setCurrentText(self.settings.get("engine", "Faster-Whisper"))
        form.addRow("Engine", self.engine_combo)

        self.model_combo = QComboBox()
        for model in AVAILABLE_MODELS:
            self.model_combo.addItem(f"{model['name']} ({model['size']})", model["id"])
        self._set_combo_by_data(self.model_combo, self.settings.get("model", "tiny"))
        form.addRow("Local model", self.model_combo)

        self.mode_combo = QComboBox()
        for mode in AVAILABLE_MODES:
            self.mode_combo.addItem(mode["label"], mode["id"])
        self._set_combo_by_data(self.mode_combo, self.settings.get("mode", "Dictation"))
        form.addRow("Mode", self.mode_combo)

        self.language_edit = QLineEdit(self.settings.get("language", "en"))
        form.addRow("Language", self.language_edit)
        return page

    def _behavior_tab(self):
        page = QWidget()
        form = QFormLayout(page)
        self.auto_paste = QCheckBox("Auto-insert text into active app")
        self.auto_paste.setChecked(bool(self.settings.get("auto_paste", True)))
        form.addRow("", self.auto_paste)

        self.push_to_talk = QCheckBox("Push-to-talk")
        self.push_to_talk.setChecked(bool(self.settings.get("push_to_talk", False)))
        form.addRow("", self.push_to_talk)

        self.toggle_recording = QCheckBox("Toggle recording")
        self.toggle_recording.setChecked(not bool(self.settings.get("push_to_talk", False)))
        form.addRow("", self.toggle_recording)

        self.continuous = QCheckBox("Continuous listening")
        self.continuous.setChecked(bool(self.settings.get("continuous_listening", False)))
        form.addRow("", self.continuous)

        self.save_history = QCheckBox("Save transcription history")
        self.save_history.setChecked(bool(self.settings.get("save_history", True)))
        form.addRow("", self.save_history)

        self.startup = QCheckBox("Launch when Windows starts")
        self.startup.setChecked(bool(self.settings.get("launch_at_startup", False)))
        form.addRow("", self.startup)
        return page

    def _hotkey_combo(self, value: str):
        combo = QComboBox()
        combo.setEditable(True)
        combo.addItems(COMMON_HOTKEYS)
        combo.setCurrentText(value)
        return combo

    def _set_combo_by_data(self, combo: QComboBox, value: str):
        idx = combo.findData(value)
        if idx >= 0:
            combo.setCurrentIndex(idx)

    def _save(self):
        start_hotkey = self.start_hotkey.currentText().strip().lower()
        if not start_hotkey:
            QMessageBox.warning(self, "Missing hotkey", "Choose a start recording hotkey before saving.")
            return
        values = {
            "hotkey": start_hotkey,
            "start_hotkey": start_hotkey,
            "stop_hotkey": self.stop_hotkey.currentText().strip().lower() or "shift+z",
            "cancel_hotkey": self.cancel_hotkey.currentText().strip().lower() or "esc",
            "overlay_width": self.overlay_width.value(),
            "overlay_opacity": self.opacity_slider.value() / 100,
            "theme": self.theme_combo.currentText(),
            "overlay_position": self.position_combo.currentText(),
            "overlay_x": None if self.position_combo.currentText() == "center" else self.settings.get("overlay_x", None),
            "overlay_y": None if self.position_combo.currentText() == "center" else self.settings.get("overlay_y", None),
            "microphone": self.microphone_combo.currentData(),
            "noise_suppression": self.noise_check.isChecked(),
            "voice_activity_detection": self.vad_check.isChecked(),
            "engine": self.engine_combo.currentText(),
            "model": self.model_combo.currentData(),
            "mode": self.mode_combo.currentData(),
            "language": self.language_edit.text().strip() or "en",
            "auto_paste": self.auto_paste.isChecked(),
            "push_to_talk": self.push_to_talk.isChecked() and not self.toggle_recording.isChecked(),
            "continuous_listening": self.continuous.isChecked(),
            "save_history": self.save_history.isChecked(),
            "launch_at_startup": self.startup.isChecked(),
        }
        self.settings.update(values)
        self._apply_startup(values["launch_at_startup"])
        self.accept()

    def _apply_startup(self, enabled: bool):
        try:
            import os
            startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
            startup_dir.mkdir(parents=True, exist_ok=True)
            launcher = startup_dir / "Whisper My Idea Pro.bat"
            vbs = APP_DIR / "Start-WhisperMyIdeaPro.vbs"
            if enabled:
                launcher.write_text(f'@echo off\r\nstart "" wscript.exe "{vbs}"\r\n', encoding="utf-8")
            elif launcher.exists():
                launcher.unlink()
        except Exception as exc:
            QMessageBox.warning(self, "Startup setting", f"Settings saved, but startup could not be updated:\n{exc}")


class MainWindow(QMainWindow):
    transcription_ready = Signal(str)
    status_update = Signal(str)
    recording_finished = Signal()
    toggle_requested = Signal()
    stop_requested = Signal()
    cancel_requested = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Whisper My Idea Pro")
        self.setFixedSize(1, 1)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.hide()

        self.settings = Settings()
        self.transcriber = Transcriber(self.settings)
        self.hud = HUDWindow(self.settings)
        self.hotkeys = HotkeyManager(self.settings)

        self._recording = False
        self._stopping = False
        self._cancelled = False
        self._current_mode = self.settings.get("mode", "Dictation")
        if not any(mode["id"] == self._current_mode for mode in AVAILABLE_MODES):
            self._current_mode = "Dictation"
            self.settings.set("mode", self._current_mode)
        self._record_start_time = 0.0
        self._target_window = None
        self._target_window_title = ""
        self._worker = None
        self._log_file = DATA_DIR / "app-debug.log"
        self._log("app initialized version=source-debug-voice-pipeline")

        self._level_timer = QTimer(self)
        self._level_timer.timeout.connect(self._update_hud_level)

        self._setup_tray()
        self._connect_signals()
        self._apply_overlay_settings()
        self._setup_hotkeys()

    def _setup_tray(self):
        px = QPixmap(32, 32)
        px.fill(Qt.transparent)
        painter = QPainter(px)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#8b5cf6"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(2, 2, 28, 28, 7, 7)
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Segoe UI", 14, QFont.Bold))
        painter.drawText(2, 2, 28, 28, Qt.AlignCenter, "W")
        painter.end()
        self.tray = QSystemTrayIcon(QIcon(px), self)
        self.tray.activated.connect(self._on_tray_activated)
        self._rebuild_tray()
        self.tray.show()

    def _connect_signals(self):
        self.transcription_ready.connect(self._on_transcription_ready)
        self.status_update.connect(self._on_status_update)
        self.recording_finished.connect(self._on_recording_done)
        self.toggle_requested.connect(self._toggle_recording)
        self.stop_requested.connect(self._stop_recording)
        self.cancel_requested.connect(self._cancel_recording)
        self.hud.mode_requested.connect(self._cycle_mode)
        self.hud.stop_requested.connect(self._stop_recording)
        self.hud.cancel_requested.connect(self._cancel_recording)

    def _setup_hotkeys(self):
        self.hotkeys.set_callbacks(
            start=lambda: self.toggle_requested.emit(),
            stop=lambda: self.stop_requested.emit(),
            cancel=lambda: self.cancel_requested.emit(),
        )
        self.hotkeys.register_all()
        self.hud.set_shortcuts(
            self.settings.get("start_hotkey", self.settings.get("hotkey", "mouse_middle")),
            self.settings.get("stop_hotkey", "shift+z"),
            self.settings.get("cancel_hotkey", "esc"),
        )
        self._rebuild_tray()

    def _apply_overlay_settings(self):
        position = self.settings.get("overlay_position", "center")
        self.hud.configure(
            width=self.settings.get("overlay_width", 680),
            opacity=self.settings.get("overlay_opacity", 0.94),
            position=position,
            x=self.settings.get("overlay_x", None) if position == "custom" else None,
            y=self.settings.get("overlay_y", None) if position == "custom" else None,
        )
        self.hud.set_mode(self._current_mode)
        self.hud.set_shortcuts(
            self.settings.get("start_hotkey", self.settings.get("hotkey", "mouse_middle")),
            self.settings.get("stop_hotkey", "shift+z"),
            self.settings.get("cancel_hotkey", "esc"),
        )

    def _rebuild_tray(self):
        menu = QMenu()
        toggle_action = QAction("Stop Recording" if self._recording else "Start Recording", self)
        toggle_action.triggered.connect(self._toggle_recording)
        menu.addAction(toggle_action)

        file_action = QAction("Transcribe File...", self)
        file_action.triggered.connect(self._transcribe_file)
        menu.addAction(file_action)
        menu.addSeparator()

        modes_menu = menu.addMenu("Mode")
        for mode in AVAILABLE_MODES:
            prefix = "✓ " if mode["id"] == self._current_mode else ""
            action = QAction(f"{prefix}{mode['label']}", self)
            action.triggered.connect(lambda checked=False, m=mode["id"]: self._set_mode(m))
            modes_menu.addAction(action)

        menu.addSeparator()
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self._show_settings)
        menu.addAction(settings_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)
        self.tray.setToolTip(f"Whisper My Idea Pro ({self.settings.get('start_hotkey', 'mouse_middle')})")

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self._toggle_recording()

    def _toggle_recording(self):
        if self._recording or self._stopping:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self):
        if self._recording:
            return
        self._target_window = self._get_foreground_window()
        self._target_window_title = self._get_window_title(self._target_window)
        self._log(
            f"recording start target_hwnd={self._target_window} "
            f"target_title={self._target_window_title!r} mode={self._current_mode}"
        )
        self._recording = True
        self._stopping = False
        self._cancelled = False
        self._record_start_time = time.time()
        self.transcriber.set_mode(self._current_mode)
        self.transcriber.set_language(self.settings.get("language", "en"))

        self.hud.start_recording(self._current_mode)
        self._level_timer.start(16)
        self._rebuild_tray()

        self._worker = threading.Thread(target=self._record_then_transcribe, daemon=True)
        self._worker.start()

    def _stop_recording(self):
        if not self._recording or self._stopping:
            return
        self._log(f"recording stop requested elapsed={time.time() - self._record_start_time:.2f}s")
        self._stopping = True
        self.status_update.emit("Processing...")
        self.hud.stop_recording()
        self._recording = False
        self._level_timer.stop()

    def _cancel_recording(self):
        if not self._recording and not self._stopping:
            self.hud.cancel()
            return
        self._cancelled = True
        self._recording = False
        self._stopping = True
        self._level_timer.stop()
        self.hud.cancel()
        self._rebuild_tray()

    def _record_then_transcribe(self):
        try:
            temp_path = self.transcriber.start_recording()
            if not temp_path:
                self._log("recording failed to start: no temp path")
                self.status_update.emit("Failed to start recording")
                return
            self._log(f"audio capture started temp_path={temp_path}")
            while self._recording:
                time.sleep(0.02)
            audio_path = self.transcriber.stop_recording()
            if self._cancelled:
                self._log("recording cancelled before transcription")
                return
            if not audio_path:
                self._log("audio save failed: recorder returned no path")
                self.status_update.emit("No audio recorded")
                return
            audio_file = Path(audio_path)
            audio_size = audio_file.stat().st_size if audio_file.exists() else -1
            self._log(
                f"audio saved path={audio_path} exists={audio_file.exists()} "
                f"size={audio_size} duration={time.time() - self._record_start_time:.2f}s"
            )
            self.status_update.emit("Transcribing...")
            self.transcriber.set_mode(self._current_mode)
            self.transcriber.set_language(self.settings.get("language", "en"))
            self._log(f"stt started audio_path={audio_path} model={self.settings.get('model', 'tiny')} language={self.settings.get('language', 'en')}")
            text = self.transcriber.transcribe_file(audio_path)
            self._log(f"stt completed transcription_len={len(text) if text else 0} preview={(text or '')[:120]!r}")
            if not self._cancelled:
                self.transcription_ready.emit(text)
        except Exception as exc:
            self._log(f"record/transcribe error: {type(exc).__name__}: {exc}")
            print(f"[MainWindow] Transcription error: {exc}")
            self.status_update.emit(f"Error: {exc}")
        finally:
            self._recording = False
            self._stopping = False
            self.recording_finished.emit()

    def _on_recording_done(self):
        self._level_timer.stop()
        if self._cancelled:
            self.hud.cancel()
        self._rebuild_tray()

    def _on_transcription_ready(self, text: str):
        self._log(f"transcription_ready len={len(text) if text else 0} preview={(text or '')[:80]!r}")
        if not text or text.startswith("Error") or text.startswith("No speech") or text.startswith("Model not loaded"):
            self.status_update.emit(text or "No text produced")
            QTimer.singleShot(700, self.hud.fade_out)
            return
        duration = time.time() - self._record_start_time if self._record_start_time else 0
        update_stats(text, duration)
        if self.settings.get("save_history", True):
            add_history(text, self._current_mode, duration)
        if self.settings.get("auto_paste", True):
            self._auto_paste(text)
        self.status_update.emit("Complete")
        self.hud.finish_and_hide()

    def _auto_paste(self, text: str):
        try:
            self._log(
                f"insert attempted len={len(text)} target_hwnd={self._target_window} "
                f"target_title={self._target_window_title!r}"
            )
            self._copy_text_to_clipboard(text)
            self.hud.hide()
            QApplication.processEvents()
            time.sleep(0.12)
            restored = self._restore_target_window()
            time.sleep(0.35)
            current_before_paste = self._get_foreground_window()
            pasted = self._send_ctrl_v()
            target_ready = not self._target_window or current_before_paste == self._target_window
            if pasted and target_ready:
                self._log(
                    f"insert successful method=clipboard-paste len={len(text)} "
                    f"focus_restored={restored} foreground={current_before_paste}"
                )
            else:
                self._log(
                    f"insert failed method=clipboard-paste len={len(text)} "
                    f"focus_restored={restored} foreground={current_before_paste} "
                    f"target={self._target_window} pasted_sent={pasted}"
                )
        except Exception as exc:
            self._log(f"insert failed exception={type(exc).__name__}: {exc}")
            print(f"[MainWindow] Auto-paste failed: {exc}")

    def _copy_text_to_clipboard(self, text: str):
        try:
            import pyperclip
            pyperclip.copy(text)
            if pyperclip.paste() == text:
                self._log(f"clipboard set by pyperclip {len(text)} chars")
                return
            self._log("pyperclip verification failed after copy")
        except Exception as exc:
            self._log(f"pyperclip failed: {type(exc).__name__}: {exc}")
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            finally:
                win32clipboard.CloseClipboard()
            self._log(f"clipboard set by win32clipboard {len(text)} chars")
            return
        except Exception as exc:
            self._log(f"win32clipboard failed: {type(exc).__name__}: {exc}")
        self._set_windows_clipboard(text)

    def _set_windows_clipboard(self, text: str):
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        kernel32.GlobalAlloc.restype = ctypes.c_void_p
        kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
        kernel32.GlobalLock.restype = ctypes.c_void_p
        kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
        kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
        user32.SetClipboardData.restype = ctypes.c_void_p
        user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
        CF_UNICODETEXT = 13
        GMEM_MOVEABLE = 0x0002
        GMEM_ZEROINIT = 0x0040

        data = ctypes.create_unicode_buffer(text)
        size = ctypes.sizeof(data)
        handle = kernel32.GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, size)
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        locked = kernel32.GlobalLock(handle)
        if not locked:
            raise ctypes.WinError(ctypes.get_last_error())
        ctypes.memmove(locked, ctypes.addressof(data), size)
        kernel32.GlobalUnlock(handle)

        if not user32.OpenClipboard(None):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            user32.EmptyClipboard()
            if not user32.SetClipboardData(CF_UNICODETEXT, handle):
                raise ctypes.WinError(ctypes.get_last_error())
            handle = None
        finally:
            user32.CloseClipboard()
        self._log(f"clipboard set {len(text)} chars")

    def _send_ctrl_v(self) -> bool:
        """Paste clipboard contents using SendInput, with keyboard-module fallback."""
        VK_CONTROL = 0x11
        VK_V = 0x56
        KEYEVENTF_KEYUP = 0x0002
        INPUT_KEYBOARD = 1
        ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong

        class KEYBDINPUT(ctypes.Structure):
            _fields_ = [
                ("wVk", wintypes.WORD),
                ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ULONG_PTR),
            ]

        class INPUT_UNION(ctypes.Union):
            _fields_ = [("ki", KEYBDINPUT)]

        class INPUT(ctypes.Structure):
            _fields_ = [("type", wintypes.DWORD), ("union", INPUT_UNION)]

        def key(vk, flags=0):
            return INPUT(type=INPUT_KEYBOARD, union=INPUT_UNION(ki=KEYBDINPUT(vk, 0, flags, 0, 0)))

        inputs = (INPUT * 4)(
            key(VK_CONTROL),
            key(VK_V),
            key(VK_V, KEYEVENTF_KEYUP),
            key(VK_CONTROL, KEYEVENTF_KEYUP),
        )
        user32 = ctypes.windll.user32
        user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
        user32.SendInput.restype = wintypes.UINT
        sent = user32.SendInput(len(inputs), inputs, ctypes.sizeof(INPUT))
        if sent == len(inputs):
            self._log("paste shortcut sent via SendInput")
            return True
        self._log(f"SendInput paste failed sent={sent} error={ctypes.get_last_error()}")
        try:
            user32.keybd_event(VK_CONTROL, 0, 0, 0)
            user32.keybd_event(VK_V, 0, 0, 0)
            user32.keybd_event(VK_V, 0, KEYEVENTF_KEYUP, 0)
            user32.keybd_event(VK_CONTROL, 0, KEYEVENTF_KEYUP, 0)
            self._log("paste shortcut sent via keybd_event fallback")
            return True
        except Exception as exc:
            self._log(f"keybd_event paste failed: {type(exc).__name__}: {exc}")
        try:
            import keyboard
            keyboard.press_and_release("ctrl+v")
            self._log("paste shortcut sent via keyboard fallback")
            return True
        except Exception as exc:
            self._log(f"keyboard fallback paste failed: {type(exc).__name__}: {exc}")
            return False

    def _get_foreground_window(self):
        try:
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            self._log(f"active window detected hwnd={hwnd} title={self._get_window_title(hwnd)!r}")
            return hwnd or None
        except Exception as exc:
            self._log(f"active window detection failed: {type(exc).__name__}: {exc}")
            return None

    def _get_window_title(self, hwnd) -> str:
        if not hwnd:
            return ""
        try:
            user32 = ctypes.windll.user32
            length = user32.GetWindowTextLengthW(hwnd)
            if length <= 0:
                return ""
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            return buffer.value
        except Exception:
            return ""

    def _restore_target_window(self) -> bool:
        hwnd = self._target_window
        if not hwnd:
            self._log("restore target skipped: no target window")
            return False
        try:
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            if user32.IsWindow(hwnd):
                current = user32.GetForegroundWindow()
                current_thread = user32.GetWindowThreadProcessId(current, None)
                target_thread = user32.GetWindowThreadProcessId(hwnd, None)
                this_thread = kernel32.GetCurrentThreadId()
                user32.AttachThreadInput(this_thread, target_thread, True)
                if current_thread:
                    user32.AttachThreadInput(this_thread, current_thread, True)
                # Windows foreground-lock workaround: a synthetic Alt press often
                # allows a background helper app to restore the user's prior app.
                VK_MENU = 0x12
                KEYEVENTF_KEYUP = 0x0002
                user32.keybd_event(VK_MENU, 0, 0, 0)
                user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
                user32.AllowSetForegroundWindow(-1)
                user32.ShowWindow(hwnd, 5)  # SW_SHOW
                user32.BringWindowToTop(hwnd)
                set_ok = bool(user32.SetForegroundWindow(hwnd))
                user32.SetActiveWindow(hwnd)
                user32.SetFocus(hwnd)
                user32.AttachThreadInput(this_thread, target_thread, False)
                if current_thread:
                    user32.AttachThreadInput(this_thread, current_thread, False)
                restored = user32.GetForegroundWindow()
                success = restored == hwnd
                self._log(
                    f"focus restored attempted target_hwnd={hwnd} current_before={current} "
                    f"current_after={restored} set_ok={set_ok} success={success} "
                    f"title={self._get_window_title(restored)!r}"
                )
                return success
            self._log(f"restore target failed: hwnd no longer valid {hwnd}")
        except Exception as exc:
            self._log(f"restore target window failed: {type(exc).__name__}: {exc}")
        return False

    def _on_status_update(self, msg: str):
        self.hud.set_status(msg)

    def _update_hud_level(self):
        if self._recording:
            self.hud.set_level(self.transcriber.get_audio_level())

    def _set_mode(self, mode: str):
        self._current_mode = mode
        self.settings.set("mode", mode)
        self.transcriber.set_mode(mode)
        self.hud.set_mode(mode)
        self._rebuild_tray()

    def _cycle_mode(self):
        mode_ids = [mode["id"] for mode in AVAILABLE_MODES]
        try:
            current_index = mode_ids.index(self._current_mode)
        except ValueError:
            current_index = 0
        self._set_mode(mode_ids[(current_index + 1) % len(mode_ids)])

    def _transcribe_file(self):
        from PySide6.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self, "Transcribe Audio File", "", "Audio Files (*.wav *.mp3 *.m4a *.ogg *.webm *.flac);;All Files (*.*)")
        if not path:
            return
        self.status_update.emit("Transcribing...")
        self.hud.show()

        def worker():
            try:
                self.transcriber.set_mode(self._current_mode)
                self.transcriber.set_language(self.settings.get("language", "en"))
                self.transcription_ready.emit(self.transcriber.transcribe_file(path))
            except Exception as exc:
                self.status_update.emit(f"Error: {exc}")
            finally:
                self.recording_finished.emit()
        threading.Thread(target=worker, daemon=True).start()

    def _show_settings(self):
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec():
            self._current_mode = self.settings.get("mode", "Dictation")
            if not any(mode["id"] == self._current_mode for mode in AVAILABLE_MODES):
                self._current_mode = "Dictation"
                self.settings.set("mode", self._current_mode)
            self.transcriber.set_mode(self._current_mode)
            self._apply_overlay_settings()
            self._setup_hotkeys()
            self._rebuild_tray()

    def _log(self, message: str):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(self._log_file, "a", encoding="utf-8") as file:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
        except Exception:
            pass

    def _quit(self):
        self.hotkeys.unregister_all()
        if self._recording:
            self._cancel_recording()
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
