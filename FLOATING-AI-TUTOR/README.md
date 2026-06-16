# Floating AI Tutor — Phase 1

## What It Is

A lightweight, always-on-top floating window that sits above any application on your desktop. This is Phase 1 of a multi-phase AI tutor that will eventually explain, teach, and answer questions about anything visible on your screen.

## Phase 1 Features

- **Always on top** — stays visible over VS Code, browsers, PDFs, spreadsheets, terminals, and any other app
- **Movable** — click and drag the title bar to reposition
- **Resizable** — drag from any edge or corner to resize
- **Collapse / Expand** — minimize to title bar only, or expand to full chat
- **Chat interface** — type questions and see responses
- **Action buttons** — Mic, Capture, Explain, Teach (placeholders for future phases)
- **Chat history** — persists between sessions in `~/.floating-ai-tutor/chat_history.json`
- **Global hotkey** — press `Ctrl+Shift+T` to show or hide the window from anywhere

## How to Run

### From source
```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\FLOATING-AI-TUTOR"
pip install -r requirements.txt
python src\main.py
```

### From EXE
```
C:\Users\tbank\Desktop\Live Cowork\FLOATING-AI-TUTOR\dist\AI Tutor.exe
```

### From shortcut
Double-click `launch.bat`

## Controls

| Control | Action |
|---------|--------|
| Drag title bar | Move window |
| Drag edges/corners | Resize window |
| `─` button | Collapse to title bar |
| `⊞` button | Expand from collapsed |
| `✕` button | Close |
| `Ctrl+Shift+T` | Global hotkey: show/hide |
| Enter in input | Send message |

## File Structure

```
FLOATING-AI-TUTOR/
├── src/
│   └── main.py          # Phase 1: Floating overlay + chat
├── dist/
│   └── AI Tutor.exe     # Built executable
├── AI Tutor.spec        # PyInstaller build spec
├── requirements.txt     # Python dependencies
├── launch.bat           # Quick launcher
└── README.md            # This file
```

## Data Storage

Chat history persists at:
```
%USERPROFILE%\.floating-ai-tutor\chat_history.json
```

## Next Phases

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Floating overlay window | ✅ Complete |
| 2 | Screen understanding (capture + OCR) | Planned |
| 3 | Explain mode | Planned |
| 4 | Ask Anything (voice + text Q&A) | Planned |
| 5 | Teach mode (structured lessons) | Planned |
| 6 | Memory system (session resume) | Planned |
| 7 | Model routing (local → cloud) | Planned |
| 8 | Agent actions (notes, flashcards, quizzes) | Planned |

## Tech Stack

- **Python 3.13**
- **PySide6** — Qt6 bindings for the floating window
- **pynput** — (reserved for future keyboard/mouse capture)
- **pyperclip** — (reserved for future clipboard integration)
- **Windows RegisterHotKey** — native global hotkey (no extra dependency)
