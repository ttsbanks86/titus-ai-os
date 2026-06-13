# Titus AI OS — Production Apps

**Standard:** Compiled .EXE | Glass-morphism UI | Zero Terminal Flash

## Current Inventory

| App | Type | Status |
|-----|------|--------|
| Whisper My Idea | Voice-to-Text | Production EXE |
| Voice My Idea | Voice Assistant | Production EXE |
| Auto Hub | Automation Scheduler | Script Phase |
| Job Intel | Market Intelligence | Script Phase |

## Build Commands (For Future Apps)

- **Frontend (Electron):** `npx electron-packager . "AppName" --platform=win32 --arch=x64 --out=../dist --overwrite --icon=../../APPS/icon.ico`
- **Backend (Python):** `pyinstaller --noconfirm --onedir --windowed --name "Backend_Name" backend.py`
