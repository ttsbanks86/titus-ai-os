# Titus Banks Production Standard v2.0
## Industry-Grade Desktop Application Quality Framework

> Compiled from: VS Code (Microsoft), Slack, Discord, WhatsApp Desktop, Notion, Obsidian,
> Apple Human Interface Guidelines, Microsoft Fluent Design, Material Design 3,
> Electron Security Best Practices, PySide6/Qt6 Industry Patterns

---

## 1. Architecture Standards

### 1.1 Process Model
```
┌─────────────────────────────────────────────┐
│              Main Process                    │
│  • Window management    • Tray/ menubar      │
│  • Global hotkeys       • Auto-updater       │
│  • IPC hub              • Native menus       │
├─────────────────────────────────────────────┤
│              Renderer Process                │
│  • UI rendering          • User interaction  │
│  • Local state           • Animations        │
├─────────────────────────────────────────────┤
│              Backend Process                 │
│  • Heavy computation     • AI/ML inference   │
│  • File I/O              • Network requests  │
└─────────────────────────────────────────────┘
```
- **Main process** must be lean — no UI rendering logic
- **Backend process** must be crash-isolated (restart without losing app state)
- **IPC** must be typed, validated, and authenticated
- **Never** use `nodeIntegration: true` in production

### 1.2 Technology Selection
| Layer | Recommended | Avoid |
|-------|-------------|-------|
| Desktop shell | Electron 35+ or Tauri | Raw Chromium |
| UI framework | React 19, Vue 3, or Svelte 5 | jQuery, vanilla JS for complex apps |
| Python backends | PySide6 (bundled with PyInstaller) | Running raw `python.exe` |
| Styling | Tailwind CSS v4, CSS Modules | Global CSS files >1000 lines |
| State management | Zustand, Pinia, or Jotai | Redux for small apps |
| Packaging | electron-builder (NSIS for Windows) | electron-packager alone |
| Installer | NSIS or WiX with auto-update | Manual folder copy |

### 1.3 Project Structure
```
project/
├── src/
│   ├── main/           # Electron main process
│   │   ├── index.js
│   │   ├── menu.js
│   │   ├── tray.js
│   │   ├── updater.js
│   │   └── ipc/
│   ├── renderer/       # UI code
│   │   ├── index.html
│   │   ├── styles/
│   │   ├── components/
│   │   └── pages/
│   ├── backend/        # Python/compiled backend
│   │   ├── server.py
│   │   └── dist/       # Compiled EXE
│   └── preload.js
├── assets/             # Icons, images
├── build/              # Build configuration
├── tests/
└── package.json
```

---

## 2. UI/UX Standards

### 2.1 Window Behavior
- **System tray app** (like Superwhisper): Starts minimized to tray. No window on launch.
- **Utility app** (like Calculator): Small fixed-size window. No resize handle.
- **Full app** (like VS Code): Restorable position/size. Session restore on crash.

**Golden rule:** The app should stay out of the user's way until requested.

### 2.2 Visual Design
| Element | Standard |
|---------|----------|
| Window frame | Custom frameless (`frame: false`) with 10px drag region |
| Title bar height | 32–38px for utility apps, 38–48px for full apps |
| Title bar buttons | Custom minimize/maximize/close, 24x24px |
| Border radius | 8px for cards, 6px for buttons, 12px for modals |
| Background | `#0a0c10` (dark) or `#f8f9fa` (light) |
| Text primary | `#f0f2f5` (dark) or `#1a1d23` (light) |
| Text secondary | `#6b7280` (both themes) |
| Accent color | One accent color used consistently for all interactive elements |
| Font stack | `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif` |
| Font sizes | 13px body, 11px labels, 9px secondary, 15px headings |
| Spacing | 16px base unit, 8px half, 24px double |

### 2.3 Responsiveness
- App must never freeze during any operation
- Heavy operations (transcription, TTS) must run on a **background thread**
- Show loading states (spinner, skeleton, or progress bar) for operations >500ms
- Handle errors gracefully — never show raw error messages to users

### 2.4 Accessibility (Minimum)
- All interactive elements must be keyboard-navigable
- Tab order must follow visual order
- Buttons must have visible focus states
- Minimum contrast ratio: 4.5:1 for text

---

## 3. Code Quality Standards

### 3.1 Error Handling
```python
# ✅ GOOD: Specific, recoverable, user-friendly
try:
    result = transcribe(audio)
    if not result:
        return {"error": "No speech detected. Try speaking closer to the mic."}
except MicrophoneError:
    return {"error": "Microphone not found. Check your device settings."}
except ModelLoadError:
    return {"error": "AI model failed to load. Restart the app to retry."}

# ❌ BAD: Generic, silent, crash-prone
try:
    result = transcribe(audio)
except:
    pass
```

### 3.2 State Management
- All app state must be in one place (zustand store, Pinia store, or class)
- No scattered `let` variables at module scope
- Settings must persist to disk (JSON file) and load on startup

### 3.3 Logging
- Log all errors with context (what action, what input, what went wrong)
- Never log sensitive data (passwords, API keys, personal info)
- Rotate logs — don't let them grow unbounded

---

## 4. Build & Release Standards

### 4.1 Packaging
| Requirement | Standard |
|------------|----------|
| Installer | NSIS or WiX with proper uninstall |
| Auto-update | electron-updater or Squirrel |
| Code signing | Required for production releases |
| Single instance | App must enforce single instance |
| Startup | Windows Registry `Run` key (optional) |

### 4.2 Executable Quality
- EXE must have proper **file version**, **product name**, **description**
- Icon must be a proper `.ico` file (256x256, multiple resolutions)
- All DLL dependencies must be bundled or verified at startup
- `--windowed` flag for PyInstaller (no console window)

### 4.3 Binary Size Budget
| Type | Max Size |
|------|----------|
| Pure Electron app (no ML) | <200MB |
| Electron + Python backend | <400MB |
| Pure PySide6 app | <100MB |
| Pure PySide6 app (no ML) | <30MB |

---

## 5. Performance Standards

| Metric | Target |
|--------|--------|
| Cold startup time | <3 seconds |
| Tray icon appear | <1 second |
| Recording start latency | <200ms |
| Transcription latency (tiny model) | <5 seconds per 30s audio |
| Memory (idle) | <150MB for utility apps |
| Memory (during recording) | <300MB |
| CPU (idle) | <1% |
| CPU (during transcription) | <50% on one core |
| Disk space (app only) | <500MB |
| Disk space (with models) | <2GB |

---

## 6. Security Standards

- **`nodeIntegration: false`** and **`contextIsolation: true`** in ALL BrowserWindows
- **`preload.js`** exposes only specific functions via `contextBridge`
- No shell commands with user input (sanitize or avoid)
- Validate all IPC input on the receiving end
- No storing secrets in source code (use environment variables or system keychain)
- Python backends: no `shell=True` in subprocess calls
- Python backends: `CREATE_NO_WINDOW` flag on Windows subprocesses

---

## 7. User Experience Checklist

- [ ] App starts without showing a window (tray-based)
- [ ] Tray icon is visible and distinguishable
- [ ] Right-click tray shows context menu with all options
- [ ] Global hotkey works from any app
- [ ] Recording starts within 200ms of hotkey press
- [ ] Floating HUD is minimal, draggable, always-on-top
- [ ] HUD shows waveform/timer/mode/stop button
- [ ] Transcription appears within 5 seconds of stopping
- [ ] Text is pasted into the previously active app
- [ ] App returns to tray state after completion
- [ ] No error dialogs reach the user (handled internally)
- [ ] App recovers from backend crash (restart)
- [ ] Settings persist across restarts
- [ ] Hotkey is adjustable from Settings
- [ ] Can transcribe files (not just live mic)
- [ ] History saves and is browsable
- [ ] Per-item copy/delete in history
- [ ] Launch at startup option works
- [ ] No duplicate processes or tray icons
- [ ] Windows key combos don't conflict with other apps

---

## 8. Source Standards (GitHub Stars Reference)

| App | Stars | Key Lessons |
|-----|-------|-------------|
| **VS Code** | 165k+ | Lean main process, extension isolation, startup perf |
| **Electron** | 115k+ | Security model, context isolation, sandboxing |
| **awesome-electron** | 26k+ | Curated best practices, boilerplates, tools |
| **Notable** | 9k+ | Clean markdown editor, minimal UI |
| **Beekeeper Studio** | 16k+ | Professional SQL client, native menus |

---

## 9. Quality Gates (Before Ship)

1. **Startup test** — App launches clean, no errors in console
2. **Hotkey test** — Global hotkey registers and unregisters
3. **Recording test** — Record + transcribe + paste works end-to-end
4. **Crash test** — Kill backend, app recovers gracefully
5. **Idle test** — App sits in tray for 1 hour, memory stable
6. **Multiple instance test** — Second launch focuses existing instance
7. **Shutdown test** — App shuts down clean, no orphaned processes
8. **Reinstall test** — Uninstall old, install new, settings preserved

---

*This standard is living. Update as new patterns emerge.*
*Filed under: [[Titus AI OS]] · [[PROMPT-MINE]]*
