# NOLA Reader v2

Professional text-to-speech reader with Edge TTS neural voices.
Built for Titus Banks AI OS — Open Door AI Systems.

## Features

- 28+ neural voices (Aria, Jenny, Guy, Andrew, Christopher, etc.)
- Clipboard auto-read — copy text anywhere, it reads aloud
- Configurable global hotkey (default: Alt+Shift+R)
- Speed control (0.5x – 3.0x)
- High-contrast dark UI — all buttons visible on any background
- System tray with quick controls
- Load text from .txt files
- Persistent settings (voice, speed, hotkey, position)
- Single portable EXE build

## Launch

Double-click: `Start-NOLA-Reader.vbs` (no console window)

Or directly:

```powershell
python nola_reader_v2.py
```

## Build EXE

```powershell
.\Build-NOLA-EXE.ps1
```

Output: `dist\NOLA_Reader.exe`

## Configuration

Settings saved to: `%APPDATA%\NOLA\settings.json`

## Keyboard

| Action | Default |
|--------|---------|
| Toggle window | Alt+Shift+R (configurable) |
| Close window | Escape |
