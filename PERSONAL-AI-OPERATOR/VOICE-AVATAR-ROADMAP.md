# Voice and Avatar Roadmap

## Goal

Add a face, voice, and reactive presence to the Personal AI Operator without compromising safety or privacy.

## Recommended Build Order

### 1. Push-to-Talk Voice Input
- Use a hotkey or button to record a short command.
- Transcribe locally if possible.
- Do not run always-on recording by default.

Options to research later:
- Whisper local
- Windows Speech Recognition
- faster-whisper

### 2. Text-to-Speech Output
- Read short responses aloud.
- Keep long reports as text.

Options to research later:
- Windows built-in SAPI voice
- Kokoro TTS
- Edge TTS

### 3. Local Dashboard
- Simple HTML or Electron-style dashboard.
- Show state: idle, listening, thinking, acting, waiting for approval.
- Buttons: Morning Briefing, Open Browser, Business Ops, Screenshot, Ask Local Model.

### 4. Avatar
- Start with simple animated face/status card.
- Add lip-sync only if useful.
- Avoid heavy GPU or cloud services unless approved.

## Safety

- No always-on microphone until explicitly approved.
- No camera/vision monitoring until explicitly approved.
- No customer messages sent without approval.
- Log voice commands locally.
