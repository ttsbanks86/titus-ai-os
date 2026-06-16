# Floating AI Tutor — Complete System

An always-on-top desktop AI tutor that teaches anything visible on your screen.

## All 8 Phases — Complete

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Floating overlay window (always-on-top, movable, resizable, hotkey) | ✅ |
| 2 | Screen capture (region selection, full screen, OCR text extraction) | ✅ |
| 3 | Explain mode (AI-powered explanations of screen content) | ✅ |
| 4 | Ask Anything (voice input, text-to-speech, conversation context) | ✅ |
| 5 | Teach mode (structured lessons, quizzes, progress tracking) | ✅ |
| 6 | Memory system (save/resume sessions, learning history) | ✅ |
| 7 | Model router (local Ollama → DeepSeek → Claude/GPT by complexity) | ✅ |
| 8 | Agent actions (study notes, flashcards, guides, practice exams) | ✅ |

## How to Run

### From source
```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\FLOATING-AI-TUTOR"
pip install -r requirements.txt
python src\main.py
```

### From Command Center
Click **Open AI Tutor** in the Command Center desktop app.

### Global hotkey
Press **Ctrl+Shift+T** to show/hide the tutor from anywhere.

## Quick Start

1. **Capture**: Click 💡 Explain → drag to select screen region
2. **Learn**: Click 📚 Teach → type `start` → `next` → `quiz`
3. **Ask**: Type or speak (🎤 Mic) follow-up questions
4. **Create**: Type `notes`, `flashcards`, `guide`, or `exam`
5. **Save**: Type `save` to preserve your session
6. **Resume**: Type `load` to continue later

## Commands

| Command | Action |
|---------|--------|
| `start` | Begin current lesson step |
| `next` | Complete step and advance |
| `quiz` | Take a quiz on current step |
| `resume` | Continue from last incomplete step |
| `progress` | Show learning progress |
| `save` | Save current session |
| `load` | Resume last saved session |
| `notes` | Generate study notes |
| `flashcards` | Create flashcard deck |
| `guide` | Build study guide |
| `exam` | Generate practice exam |
| `materials` | List all study files |

## File Structure

```
FLOATING-AI-TUTOR/
├── src/
│   ├── main.py          # Main window + all integrations
│   ├── capture.py       # Region selection overlay
│   ├── ocr.py           # Text extraction (pytesseract + Windows)
│   ├── tutor.py         # AI explanation engine
│   ├── voice.py         # Speech recognition
│   ├── tts.py           # Text-to-speech
│   ├── context.py       # Conversation context manager
│   ├── teach.py         # Lesson plans + quizzes
│   ├── memory.py        # Session save/resume
│   ├── router.py        # Model routing by complexity
│   └── actions.py       # Notes, flashcards, guides, exams
├── dist/
│   └── AI Tutor.exe     # Built executable
├── AI Tutor.spec        # PyInstaller build spec
├── requirements.txt     # Python dependencies
├── launch.bat           # Quick launcher
└── README.md            # This file
```

## Data Storage

All data persists at:
```
%USERPROFILE%\.floating-ai-tutor\
├── chat_history.json
├── conversation_context.json
├── tutor_config.json
├── router_config.json
├── learning_progress.json
├── lessons/
├── sessions/
├── notes/
├── flashcards/
├── study_guides/
└── quizzes/
```

## AI Models

- **Local**: Ollama (llama3.2) — free, always available
- **Mid**: DeepSeek — cheap, for code/technical explanations
- **High**: Claude/GPT — for complex reasoning (requires API key)

Configure in `~/.floating-ai-tutor/router_config.json`

## Tech Stack

- Python 3.13 + PySide6 (Qt6)
- pytesseract + Pillow (OCR)
- speech_recognition (voice input)
- Windows SAPI5 (text-to-speech)
- Ollama (local AI)
- PyInstaller (EXE packaging)
