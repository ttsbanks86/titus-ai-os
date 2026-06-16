#!/usr/bin/env python3
"""Floating AI Tutor — Phase 1: Floating Overlay Window.

A lightweight, always-on-top floating window that sits above any application.
Provides chat input, microphone button, screenshot selection, collapse/expand,
and chat history panel. Controlled by a global hotkey (default: Ctrl+Shift+T).
"""
import ctypes
import ctypes.wintypes
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, Signal, QObject,
    QThread,
)
from PySide6.QtGui import (
    QAction, QColor, QFont, QFontDatabase, QIcon, QPainter, QPainterPath,
    QKeySequence, QPalette, QShortcut,
)
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QScrollArea, QTextEdit, QVBoxLayout, QWidget,
    QSizePolicy, QMessageBox,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
APP_NAME = "Floating AI Tutor"
APP_VERSION = "0.1.0"
DATA_DIR = Path(os.path.expanduser("~")) / ".floating-ai-tutor"
HISTORY_FILE = DATA_DIR / "chat_history.json"
DEFAULT_HOTKEY_MOD = 0x0002 | 0x0004  # Ctrl + Shift
DEFAULT_HOTKEY_VK = 0x54  # T

# ---------------------------------------------------------------------------
# Windows global hotkey via RegisterHotKey
# ---------------------------------------------------------------------------
class GlobalHotkey(QObject):
    """Register a system-wide hotkey using Windows RegisterHotKey."""

    activated = Signal()

    def __init__(self, mod=DEFAULT_HOTKEY_MOD, vk=DEFAULT_HOTKEY_VK):
        super().__init__()
        self.mod = mod
        self.vk = vk
        self._hotkey_id = 0x9F01  # unique ID for this hotkey

    def register(self, hwnd):
        """Register the hotkey for the given window handle."""
        if sys.platform != "win32":
            return
        self._hwnd = int(hwnd)
        ctypes.windll.user32.RegisterHotKey(self._hwnd, self._hotkey_id, self.mod, self.vk)

    def unregister(self):
        if sys.platform != "win32" or not hasattr(self, "_hwnd"):
            return
        ctypes.windll.user32.UnregisterHotKey(self._hwnd, self._hotkey_id)

    def nativeEvent(self, event_type, message):
        if sys.platform == "win32" and event_type == "windows_generic_MSG":
            msg = ctypes.wintypes.MSG.from_address(message.__int__())
            if msg.message == 0x0312:  # WM_HOTKEY
                if msg.wParam == self._hotkey_id:
                    self.activated.emit()
                    return True, 0
        return False, 0

# ---------------------------------------------------------------------------
# Chat history manager
# ---------------------------------------------------------------------------
class ChatHistory:
    def __init__(self, path=HISTORY_FILE):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.sessions = []
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                self.sessions = json.loads(self.path.read_text(encoding="utf-8"))
            except Exception:
                self.sessions = []

    def save(self):
        self.path.write_text(json.dumps(self.sessions, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_message(self, role, content):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
        }
        self.sessions.append(entry)
        self.save()

    def clear(self):
        self.sessions = []
        self.save()

    def get_recent(self, limit=50):
        return self.sessions[-limit:]

# ---------------------------------------------------------------------------
# Background worker for OCR + AI explanation
# ---------------------------------------------------------------------------
class ExplainWorker(QObject):
    """Runs OCR + AI explanation on a background thread."""

    finished = Signal(str)  # explanation text
    error = Signal(str)     # error message

    def __init__(self, pixmap, question="", context=""):
        super().__init__()
        self._pixmap = pixmap
        self._question = question
        self._context = context

    def run(self):
        try:
            from ocr import extract_text, get_ocr_status
            from tutor import explain, check_ollama

            status = get_ocr_status()
            ollama = check_ollama()

            # OCR
            text = extract_text(self._pixmap)
            if not text:
                self.finished.emit(
                    "I couldn't extract any text from the selected area. "
                    "Try selecting a region with more visible text.\n\n"
                    f"OCR engines available: pytesseract={status['pytesseract']}, "
                    f"easyocr={status['easyocr']}, windows={status['windows']}"
                )
                return

            # AI explanation with context
            result = explain(text, self._question, context=self._context)
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))


# ---------------------------------------------------------------------------
# Floating overlay window
# ---------------------------------------------------------------------------
RESIZE_MARGIN = 8

class FloatingWindow(QMainWindow):
    """Phase 1 floating overlay window."""

    def __init__(self):
        super().__init__()
        self._collapsed = False
        self._dragging = False
        self._drag_pos = None
        self._resizing = False
        self._resize_edge = None
        self._resize_start_pos = None
        self._resize_start_rect = None
        self.history = ChatHistory()
        from context import ConversationContext
        self.conversation = ConversationContext()
        from memory import SessionMemory
        self.session_memory = SessionMemory()
        self._lesson = None
        self._lesson_step = 0
        self._setup_ui()
        self._load_history_ui()
        self._apply_style()

    # -- UI setup -----------------------------------------------------------
    def _setup_ui(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(340, 260)
        self.resize(420, 520)
        self.move(200, 120)
        self.setWindowTitle(APP_NAME)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Title bar
        root.addWidget(self._build_titlebar())

        # Content area
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(12, 10, 12, 10)
        content_layout.setSpacing(8)

        # Chat display
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setObjectName("chatScroll")
        self.chat_area = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_area)
        self.chat_layout.setContentsMargins(4, 4, 4, 4)
        self.chat_layout.setSpacing(6)
        self.chat_layout.addStretch()
        self.chat_scroll.setWidget(self.chat_area)
        content_layout.addWidget(self.chat_scroll)

        # Action bar (mic, screenshot, history)
        content_layout.addWidget(self._build_actionbar())

        # Input bar
        content_layout.addWidget(self._build_inputbar())

        root.addWidget(self.content_frame)

        # Welcome message
        self._add_bubble("tutor", "Hi! I'm your AI tutor. Drag me anywhere, resize from the edges, or press Ctrl+Shift+T to toggle. Select something on screen and ask me to explain it.")

    def _build_titlebar(self):
        bar = QFrame()
        bar.setObjectName("titlebar")
        bar.setFixedHeight(36)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(6)

        # App label
        self.title_label = QLabel("🧠 AI Tutor")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(self.title_label)

        layout.addStretch()

        # History button
        self.btn_history = QPushButton("📋")
        self.btn_history.setObjectName("toolBtn")
        self.btn_history.setFixedSize(28, 28)
        self.btn_history.setToolTip("Chat History")
        self.btn_history.clicked.connect(self._toggle_history)
        layout.addWidget(self.btn_history)

        # Collapse button
        self.btn_collapse = QPushButton("─")
        self.btn_collapse.setObjectName("toolBtn")
        self.btn_collapse.setFixedSize(28, 28)
        self.btn_collapse.setToolTip("Collapse")
        self.btn_collapse.clicked.connect(self._toggle_collapse)
        layout.addWidget(self.btn_collapse)

        # Close button
        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("closeBtn")
        self.btn_close.setFixedSize(28, 28)
        self.btn_close.setToolTip("Close")
        self.btn_close.clicked.connect(self.close)
        layout.addWidget(self.btn_close)

        return bar

    def _build_actionbar(self):
        bar = QFrame()
        bar.setObjectName("actionbar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(6)

        self.btn_mic = QPushButton("🎤 Mic")
        self.btn_mic.setObjectName("actionBtn")
        self.btn_mic.setToolTip("Voice input (Phase 4)")
        self.btn_mic.clicked.connect(self._on_mic)
        layout.addWidget(self.btn_mic)

        self.btn_screenshot = QPushButton("📸 Capture")
        self.btn_screenshot.setObjectName("actionBtn")
        self.btn_screenshot.setToolTip("Capture screen region (Phase 2)")
        self.btn_screenshot.clicked.connect(self._on_screenshot)
        layout.addWidget(self.btn_screenshot)

        self.btn_explain = QPushButton("💡 Explain")
        self.btn_explain.setObjectName("actionBtn primary")
        self.btn_explain.setToolTip("Explain what's on screen (Phase 3)")
        self.btn_explain.clicked.connect(self._on_explain)
        layout.addWidget(self.btn_explain)

        self.btn_teach = QPushButton("📚 Teach")
        self.btn_teach.setObjectName("actionBtn")
        self.btn_teach.setToolTip("Start a lesson (Phase 5)")
        self.btn_teach.clicked.connect(self._on_teach)
        layout.addWidget(self.btn_teach)

        layout.addStretch()
        return bar

    def _build_inputbar(self):
        bar = QFrame()
        bar.setObjectName("inputbar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(6)

        self.input = QLineEdit()
        self.input.setObjectName("chatInput")
        self.input.setPlaceholderText("Ask anything about what you see…")
        self.input.returnPressed.connect(self._send_message)
        layout.addWidget(self.input)

        self.btn_send = QPushButton("Send")
        self.btn_send.setObjectName("sendBtn")
        self.btn_send.setFixedWidth(56)
        self.btn_send.clicked.connect(self._send_message)
        layout.addWidget(self.btn_send)

        return bar

    # -- Styling ------------------------------------------------------------
    def _apply_style(self):
        self.setStyleSheet("""
            QMainWindow { background: transparent; }
            QWidget { font-family: 'Segoe UI', 'Inter', Arial, sans-serif; font-size: 13px; color: #e5e7eb; }
            #titlebar {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #1e1b4b, stop:0.5 #312e81, stop:1 #1e1b4b);
                border-radius: 16px 16px 0 0;
                border: 1px solid rgba(99,102,241,0.3);
                border-bottom: none;
            }
            #titleLabel { color: #e0e7ff; }
            #toolBtn {
                background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
                border-radius: 8px; color: #c7d2fe; font-size: 14px;
            }
            #toolBtn:hover { background: rgba(99,102,241,0.25); border-color: rgba(99,102,241,0.5); color: #fff; }
            #closeBtn {
                background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3);
                border-radius: 8px; color: #fca5a5; font-size: 13px; font-weight: 600;
            }
            #closeBtn:hover { background: rgba(239,68,68,0.35); color: #fff; }
            #contentFrame {
                background: rgba(15,15,35,0.92);
                border: 1px solid rgba(99,102,241,0.25);
                border-top: none;
                border-radius: 0 0 16px 16px;
            }
            #chatScroll {
                background: transparent; border: none;
            }
            #chatScroll > QWidget { background: transparent; }
            #actionbar { background: transparent; }
            #actionBtn {
                background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
                border-radius: 10px; color: #c7d2fe; padding: 6px 10px; font-size: 12px; font-weight: 500;
            }
            #actionBtn:hover { background: rgba(99,102,241,0.2); border-color: rgba(99,102,241,0.45); }
            #actionBtn.primary {
                background: rgba(99,102,241,0.25); border-color: rgba(99,102,241,0.5);
                color: #e0e7ff; font-weight: 600;
            }
            #inputbar { background: transparent; }
            #chatInput {
                background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
                border-radius: 12px; padding: 10px 14px; color: #e5e7eb; font-size: 13px;
            }
            #chatInput:focus { border-color: rgba(99,102,241,0.6); background: rgba(255,255,255,0.08); }
            #chatInput::placeholder { color: #6b7280; }
            #sendBtn {
                background: #4f46e5; border: 1px solid #6366f1; border-radius: 12px;
                color: #fff; font-weight: 600; font-size: 13px;
            }
            #sendBtn:hover { background: #6366f1; }
        """)

    # -- Chat bubbles -------------------------------------------------------
    def _add_bubble(self, role, text):
        bubble = QFrame()
        bubble.setObjectName("bubble")
        is_user = role == "user"
        bubble.setProperty("role", role)
        bubble.setStyleSheet(f"""
            #bubble {{
                background: {'rgba(99,102,241,0.2)' if is_user else 'rgba(255,255,255,0.06)'};
                border: 1px solid {'rgba(99,102,241,0.3)' if is_user else 'rgba(255,255,255,0.1)'};
                border-radius: 14px; padding: 10px 12px;
            }}
            QLabel {{ color: #e5e7eb; font-size: 13px; line-height: 1.5; }}
        """)
        layout = QVBoxLayout(bubble)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        label = QLabel(text)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(label)

        # Insert before stretch
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

        # Scroll to bottom
        QTimer.singleShot(50, lambda: self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        ))

    def _load_history_ui(self):
        for msg in self.history.get_recent(30):
            self._add_bubble(msg["role"], msg["content"])

    # -- Actions ------------------------------------------------------------
    def _send_message(self):
        text = self.input.text().strip()
        if not text:
            return
        self.input.clear()
        self._add_bubble("user", text)
        self.history.add_message("user", text)
        self.conversation.add_message("user", text)

        # Check for teach mode commands
        if self._handle_teach_command(text):
            return

        # Check if we have captured context for follow-up
        if self.conversation.last_captured_text:
            # Send as follow-up question with context
            self._add_bubble("tutor", "💡 Thinking about your question…")
            self.btn_explain.setText("⏳ Working…")
            self.btn_explain.setEnabled(False)

            self._thread = QThread()
            context = self.conversation.get_context_for_prompt()
            self._worker = ExplainWorker(None, text, context=context)
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._worker.finished.connect(self._on_explain_done)
            self._worker.error.connect(self._on_explain_error)
            self._worker.finished.connect(self._thread.quit)
            self._worker.error.connect(self._thread.quit)
            self._thread.finished.connect(self._thread.deleteLater)
            self._thread.start()
        else:
            # Placeholder response
            self._add_bubble("tutor", "I received your question. Click 💡 Explain to capture something on screen first, then ask follow-up questions.")
            self.history.add_message("tutor", "I received your question. Click 💡 Explain to capture something on screen first, then ask follow-up questions.")
            self.conversation.add_message("tutor", "I received your question. Click 💡 Explain to capture something on screen first, then ask follow-up questions.")

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        if self._collapsed:
            self.content_frame.hide()
            self.btn_collapse.setText("⊞")
            self.btn_collapse.setToolTip("Expand")
            self.setMinimumHeight(36)
            self.resize(self.width(), 36)
        else:
            self.content_frame.show()
            self.btn_collapse.setText("─")
            self.btn_collapse.setToolTip("Collapse")
            self.setMinimumHeight(260)
            self.resize(self.width(), 520)

    def _toggle_history(self):
        # Simple: show/hide last 10 messages as a quick peek
        recent = self.history.get_recent(10)
        if not recent:
            self._add_bubble("tutor", "No chat history yet. Start asking questions!")
            return
        self._add_bubble("tutor", f"📋 Showing {len(recent)} recent messages. Full history panel coming in Phase 1 refinement.")
        for msg in recent[-5:]:
            prefix = "You" if msg["role"] == "user" else "Tutor"
            self._add_bubble("tutor", f"{prefix}: {msg['content'][:120]}")

    def _on_mic(self):
        """Listen for voice input and add to chat."""
        self.btn_mic.setText("🎤 Listening…")
        self.btn_mic.setEnabled(False)

        def _listen():
            from voice import listen_once
            text = listen_once(timeout_sec=10)
            return text

        self._mic_thread = QThread()
        self._mic_worker = type('MicWorker', (QObject,), {
            'finished': Signal(str),
            'run': lambda self: self.finished.emit(_listen())
        })()
        self._mic_worker.moveToThread(self._mic_thread)
        self._mic_thread.started.connect(self._mic_worker.run)
        self._mic_worker.finished.connect(self._on_voice_input)
        self._mic_worker.finished.connect(self._mic_thread.quit)
        self._mic_thread.finished.connect(self._mic_thread.deleteLater)
        self._mic_thread.start()

    def _on_voice_input(self, text):
        """Handle voice input result."""
        self.btn_mic.setText("🎤 Mic")
        self.btn_mic.setEnabled(True)
        if text:
            self._add_bubble("user", f"🎤 {text}")
            self.input.setText(text)
            self.history.add_message("user", text)
            self.conversation.add_message("user", text)
            # Auto-send if there's captured context
            if self.conversation.last_captured_text:
                self._send_voice_question(text)
            else:
                self._add_bubble("tutor", "I heard you! Type a question or click 💡 Explain to capture something on screen first.")
        else:
            self._add_bubble("tutor", "🎤 Couldn't hear anything. Try again or type your question.")

    def _send_voice_question(self, question):
        """Send a voice question with existing captured context."""
        self._add_bubble("tutor", "💡 Thinking about your question…")
        self.btn_explain.setText("⏳ Working…")
        self.btn_explain.setEnabled(False)

        self._thread = QThread()
        self._worker = ExplainWorker(None, question, self.conversation.get_context_for_prompt())
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_explain_done)
        self._worker.error.connect(self._on_explain_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _on_screenshot(self):
        """Capture a screen region and show extracted text."""
        self.hide()
        QTimer.singleShot(200, self._do_capture)

    def _do_capture(self):
        from capture import capture_region
        pixmap = capture_region()
        self.show()
        self.activateWindow()
        self.raise_()
        if pixmap is None:
            self._add_bubble("tutor", "📸 Capture cancelled.")
            return
        # Save and show preview
        from ocr import extract_text, get_ocr_status
        text = extract_text(pixmap)
        status = get_ocr_status()
        if text:
            # Save to conversation context
            self.conversation.set_captured_text(text)
            preview = text[:300] + ("…" if len(text) > 300 else "")
            self._add_bubble("tutor", f"📸 Captured {len(text)} characters:\n\n```\n{preview}\n```")
            self.history.add_message("tutor", f"📸 Captured {len(text)} characters: {preview}")
            self.conversation.add_message("tutor", f"Captured {len(text)} characters from screen.")
        else:
            engines = ", ".join(k for k, v in status.items() if v)
            self._add_bubble("tutor", f"📸 Image captured but no text found. Available OCR: {engines or 'none'}")

    def _on_explain(self):
        """Capture screen region, run OCR, and generate AI explanation."""
        self.hide()
        QTimer.singleShot(200, self._do_explain)

    def _do_explain(self):
        from capture import capture_region
        pixmap = capture_region()
        self.show()
        self.activateWindow()
        self.raise_()
        if pixmap is None:
            self._add_bubble("tutor", "💡 Explain cancelled.")
            return

        # Show processing
        self._add_bubble("tutor", "💡 Analyzing screen content…")
        self.btn_explain.setText("⏳ Working…")
        self.btn_explain.setEnabled(False)

        # Get conversation context for follow-up awareness
        context = self.conversation.get_context_for_prompt()

        # Start background worker
        self._thread = QThread()
        self._worker = ExplainWorker(pixmap, context=context)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(self._on_explain_done)
        self._worker.error.connect(self._on_explain_error)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._thread.deleteLater)
        self._thread.start()

    def _on_explain_done(self, explanation):
        self.btn_explain.setText("💡 Explain")
        self.btn_explain.setEnabled(True)
        self._add_bubble("user", "[Screen capture]")
        self._add_bubble("tutor", explanation)
        self.history.add_message("user", "[Screen capture]")
        self.history.add_message("tutor", explanation)
        self.conversation.add_message("user", "[Screen capture]")
        self.conversation.add_message("tutor", explanation)

        # Read explanation aloud (TTS)
        try:
            from tts import speak
            # Clean markdown for speech
            clean = explanation.replace("**", "").replace("*", "").replace("#", "").replace("`", "")
            speak(clean[:500])  # Speak first 500 chars to avoid long waits
        except Exception:
            pass

    def _on_explain_error(self, error_msg):
        self.btn_explain.setText("💡 Explain")
        self.btn_explain.setEnabled(True)
        self._add_bubble("tutor", f"❌ Error: {error_msg}")

    def _on_teach(self):
        """Start or continue a structured lesson."""
        from teach import detect_topic, create_lesson_plan, get_saved_lessons, get_lesson_summary

        # Check for saved lessons
        saved = get_saved_lessons()
        if saved:
            latest = saved[0]
            summary = get_lesson_summary(latest)
            self._add_bubble("tutor", f"📚 Found saved lesson:\n\n{summary}\n\nType 'resume' to continue, or capture new content to start a fresh lesson.")
            self._lesson = latest
            return

        # Check if we have captured content to detect topic
        if self.conversation.last_captured_text:
            topic = detect_topic(self.conversation.last_captured_text)
            self._lesson = create_lesson_plan(topic, "beginner")
            self._lesson_step = 0
            self._show_lesson_intro()
        else:
            self._add_bubble("tutor", "📚 To start a lesson, first click 💡 Explain to capture something on screen (code, spreadsheet, diagram, etc.), then click 📚 Teach again.")

    def _show_lesson_intro(self):
        """Show the lesson introduction."""
        if not self._lesson:
            return
        steps = self._lesson["steps"]
        total = len(steps)
        step_list = "\n".join(f"{s['number']}. {s['title']}" for s in steps)
        self._add_bubble("tutor",
            f"📚 **{self._lesson['title']}** — Beginner Level\n\n"
            f"{total} steps:\n{step_list}\n\n"
            f"Type 'start' to begin step 1, or 'quiz' to test your knowledge."
        )
        self.conversation.set_topic(self._lesson["title"])
        from teach import save_lesson
        save_lesson(self._lesson)

    def _handle_teach_command(self, text: str):
        """Handle teach mode commands."""
        cmd = text.lower().strip()

        if cmd == "start" and self._lesson:
            self._start_lesson_step()
            return True

        if cmd == "next" and self._lesson:
            self._advance_lesson()
            return True

        if cmd == "quiz" and self._lesson:
            self._run_quiz()
            return True

        if cmd == "resume" and self._lesson:
            self._resume_lesson()
            return True

        if cmd == "progress":
            self._show_progress()
            return True

        if cmd == "save":
            self._save_session()
            return True

        if cmd == "load":
            self._load_session()
            return True

        return False

    def _start_lesson_step(self):
        """Start the current lesson step."""
        if not self._lesson:
            return
        steps = self._lesson["steps"]
        if self._lesson_step >= len(steps):
            self._add_bubble("tutor", "🎉 You've completed all steps! Type 'quiz' for a final review, or 'save' to save your progress.")
            return

        step = steps[self._lesson_step]
        step["status"] = "in_progress"
        self._add_bubble("tutor",
            f"📖 **Step {step['number']}: {step['title']}**\n\n"
            f"Let's learn about {step['title']}. I'll explain the key concepts.\n\n"
            f"When you're ready, type 'quiz' to test your understanding, or 'next' to move on."
        )

        # Auto-explain if we have captured content
        if self.conversation.last_captured_text:
            self._add_bubble("tutor", f"💡 I see you have captured content. Let me explain {step['title']} based on what's on your screen…")
            self.btn_explain.setText("⏳ Working…")
            self.btn_explain.setEnabled(False)

            self._thread = QThread()
            context = self.conversation.get_context_for_prompt()
            question = f"Teach me about {step['title']}. Explain the key concepts step by step with examples."
            self._worker = ExplainWorker(None, question, context=context)
            self._worker.moveToThread(self._thread)
            self._thread.started.connect(self._worker.run)
            self._worker.finished.connect(self._on_explain_done)
            self._worker.error.connect(self._on_explain_error)
            self._worker.finished.connect(self._thread.quit)
            self._worker.error.connect(self._thread.quit)
            self._thread.finished.connect(self._thread.deleteLater)
            self._thread.start()

    def _advance_lesson(self):
        """Mark current step complete and move to next."""
        if not self._lesson:
            return
        steps = self._lesson["steps"]
        if self._lesson_step < len(steps):
            steps[self._lesson_step]["status"] = "completed"
            self._add_bubble("tutor", f"✅ Step {steps[self._lesson_step]['number']} completed!")
        self._lesson_step += 1
        from teach import save_lesson
        save_lesson(self._lesson)
        self._start_lesson_step()

    def _run_quiz(self):
        """Run a quiz for the current step."""
        if not self._lesson:
            return
        from teach import generate_quiz
        steps = self._lesson["steps"]
        if self._lesson_step >= len(steps):
            self._add_bubble("tutor", "🎉 All steps complete! Great work.")
            return

        step = steps[self._lesson_step]
        quiz = generate_quiz(self._lesson["topic"], step["title"])

        quiz_text = f"📝 **Quiz: {step['title']}**\n\n"
        for i, q in enumerate(quiz):
            quiz_text += f"{i+1}. {q['q']}\n"
            if q.get("choices"):
                quiz_text += f"   A) {q['choices'][0]}  B) {q['choices'][1]}  C) {q['choices'][2]}  D) {q['choices'][3]}\n"
            quiz_text += f"   Answer: ||{q['a']}||\n\n"

        self._add_bubble("tutor", quiz_text)
        step["quiz_score"] = "attempted"
        from teach import save_lesson
        save_lesson(self._lesson)

    def _resume_lesson(self):
        """Resume from the first incomplete step."""
        if not self._lesson:
            return
        steps = self._lesson["steps"]
        for i, step in enumerate(steps):
            if step["status"] != "completed":
                self._lesson_step = i
                self._add_bubble("tutor", f"📚 Resuming at Step {i+1}: {step['title']}")
                self._start_lesson_step()
                return
        self._add_bubble("tutor", "🎉 All steps completed! Type 'quiz' for review.")

    def _show_progress(self):
        """Show learning progress."""
        from teach import load_progress, get_saved_lessons, get_lesson_summary
        saved = get_saved_lessons()
        if not saved:
            self._add_bubble("tutor", "📊 No saved lessons yet. Start a lesson with 📚 Teach!")
            return

        progress_text = "📊 **Your Learning Progress**\n\n"
        for lesson in saved[:5]:
            progress_text += get_lesson_summary(lesson) + "\n\n"
        self._add_bubble("tutor", progress_text)

    def _save_session(self):
        """Save the current session."""
        from teach import load_progress
        progress = load_progress()
        session_id = self.session_memory.save_current_state(
            self.conversation, progress, self.conversation.last_captured_text
        )
        self._add_bubble("tutor", f"💾 Session saved! ID: {session_id}\n\nType 'load' later to resume where you left off.")

    def _load_session(self):
        """Load the most recent session."""
        sessions = self.session_memory.list_sessions()
        if not sessions:
            self._add_bubble("tutor", "📂 No saved sessions found. Start learning and type 'save' to create one!")
            return

        latest = sessions[0]
        data = self.session_memory.resume_session(latest["id"])
        if data:
            self._add_bubble("tutor",
                f"📂 Resumed session: **{latest['name']}**\n"
                f"Saved: {latest['created_at'][:16]}\n\n"
                f"Your previous conversation and progress have been restored."
            )
            # Restore conversation
            for msg in data.get("conversation", []):
                self.conversation.add_message(msg["role"], msg["content"])
            if data.get("last_captured_text"):
                self.conversation.set_captured_text(data["last_captured_text"])

    # -- Drag / Resize ------------------------------------------------------
    def _get_resize_edge(self, pos):
        """Determine which resize edge/corner the cursor is near."""
        r = self.rect()
        x, y = pos.x(), pos.y()
        left = x < RESIZE_MARGIN
        right = x > r.width() - RESIZE_MARGIN
        top = y < RESIZE_MARGIN
        bottom = y > r.height() - RESIZE_MARGIN

        if top and left: return "top-left"
        if top and right: return "top-right"
        if bottom and left: return "bottom-left"
        if bottom and right: return "bottom-right"
        if top: return "top"
        if bottom: return "bottom"
        if left: return "left"
        if right: return "right"
        return None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            edge = self._get_resize_edge(event.pos())
            if edge:
                self._resizing = True
                self._resize_edge = edge
                self._resize_start_pos = event.globalPosition().toPoint()
                self._resize_start_rect = self.geometry()
                self.setCursor(self._resize_cursor(edge))
            else:
                self._dragging = True
                self._drag_pos = event.globalPosition().toPoint() - self.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resizing and self._resize_start_rect:
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            r = self._resize_start_rect
            edge = self._resize_edge
            if "right" in edge:
                r.setRight(r.right() + delta.x())
            if "left" in edge:
                r.setLeft(r.left() + delta.x())
            if "bottom" in edge:
                r.setBottom(r.bottom() + delta.y())
            if "top" in edge:
                r.setTop(r.top() + delta.y())
            self.setGeometry(r)
        elif self._dragging:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
        else:
            edge = self._get_resize_edge(event.pos())
            self.setCursor(self._resize_cursor(edge) if edge else Qt.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._resizing = False
        self._resize_edge = None
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def _resize_cursor(self, edge):
        cursors = {
            "top-left": Qt.SizeFDiagCursor,
            "top-right": Qt.SizeBDiagCursor,
            "bottom-left": Qt.SizeBDiagCursor,
            "bottom-right": Qt.SizeFDiagCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
        }
        return cursors.get(edge, Qt.ArrowCursor)

    # -- Global hotkey via native event -------------------------------------
    def nativeEvent(self, event_type, message):
        if hasattr(self, "_hotkey"):
            handled, result = self._hotkey.nativeEvent(event_type, message)
            if handled:
                self._on_hotkey()
                return True, result
        return super().nativeEvent(event_type, message)

    def _on_hotkey(self):
        """Toggle window visibility on Ctrl+Shift+T."""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.activateWindow()
            self.raise_()
            self.input.setFocus()

    # -- Setup hotkey after show --------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        if not hasattr(self, "_hotkey"):
            self._hotkey = GlobalHotkey()
            hwnd = self.winId()
            self._hotkey.register(hwnd)

    def closeEvent(self, event):
        if hasattr(self, "_hotkey"):
            self._hotkey.unregister()
        self.history.save()
        super().closeEvent(event)

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setStyle("Fusion")

    # Dark palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(15, 15, 35))
    palette.setColor(QPalette.WindowText, QColor(229, 231, 235))
    palette.setColor(QPalette.Base, QColor(30, 30, 50))
    palette.setColor(QPalette.AlternateBase, QColor(25, 25, 45))
    palette.setColor(QPalette.ToolTipBase, QColor(229, 231, 235))
    palette.setColor(QPalette.ToolTipText, QColor(15, 15, 35))
    palette.setColor(QPalette.Text, QColor(229, 231, 235))
    palette.setColor(QPalette.Button, QColor(30, 30, 50))
    palette.setColor(QPalette.ButtonText, QColor(229, 231, 235))
    app.setPalette(palette)

    window = FloatingWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
