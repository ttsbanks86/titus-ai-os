# Qwen3 TTS Setup for Goose

## Installation Complete ✅

- **Qwen3 TTS Engine:** Installed at `C:\Users\tbank\Desktop\qwen3-tts\.venv`
- **MCP Server:** Installed at `C:\Users\tbank\Desktop\qwen3-tts-mcp`
- **PyTorch:** 2.6.0+cu124 with CUDA support
- **GPU:** NVIDIA GeForce RTX 3080 Laptop GPU detected ✅
- **FastMCP:** Installed

## Add to Goose Desktop

### Step 1: Open Goose Desktop

Launch Goose from `C:\Users\tbank\Desktop\Goose.lnk`

### Step 2: Add Extension

1. Click **Extensions** in the left sidebar
2. Click **Add custom extension**
3. Fill in the form:
   - **Extension ID:** `qwen3-tts`
   - **Extension Name:** `Qwen3 TTS`
   - **Type:** `Standard IO`
   - **Command:** `C:\Users\tbank\Desktop\qwen3-tts\.venv\Scripts\python.exe`
   - **Arguments:** `C:\Users\tbank\Desktop\qwen3-tts-mcp\server.py`
   - **Timeout:** `600`
4. Click **Add**

### Step 3: Restart Goose

Close and reopen Goose Desktop for the extension to load.

## Test in Goose

Once restarted, try these prompts:

```
Use Qwen3 TTS to say "Hello, this is a test of the Qwen3 text to speech system"
```

Or:

```
Generate speech with a calm male voice saying "Welcome to the Titus Banks AI operating system"
```

## Available Tools

### `speak` - Voice Design
Generate speech with a custom voice persona.

**Parameters:**
- `text`: Text to speak
- `voice`: Voice description (e.g., "A deep male voice with a calm tone")
- `language`: English, Chinese, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian
- `seed`: Random seed for reproducible voices (0 = random)

### `clone_voice` - Voice Cloning
Clone a voice from reference audio.

**Parameters:**
- `text`: Text to speak
- `ref_audio`: Path to reference audio file (3+ seconds recommended)
- `ref_text`: Transcript of reference audio (optional, improves quality)
- `language`: Language of output speech

## Notes

- First run downloads the model (~3GB) - this may take a few minutes
- Requires NVIDIA GPU with CUDA (RTX 3080 ✅)
- SoX warning is harmless - audio playback uses PowerShell instead
- Audio files saved to `C:\Users\tbank\AppData\Local\Temp\qwen3tts\`

## Troubleshooting

### "IO error: program not found" Fix

If you see `IO error: program not found` when calling the qwen3-tts tools:

**Cause:** Goose can't resolve the Python executable path because `python` is not on the system PATH and Goose's subprocess context doesn't handle absolute paths the same way as PowerShell.

**Fix:** A batch wrapper script has been created at `C:\Users\tbank\Desktop\qwen3-tts-mcp\start-qwen3tts.bat` that sets the correct Python path. The Goose config has been updated to use this wrapper:

```yaml
qwen3tts:
    cmd: C:/Users/tbank/Desktop/qwen3-tts-mcp/start-qwen3tts.bat
    args: []
```

**Steps:**
1. Close and restart Goose Desktop
2. The extension should now load correctly
3. Test with: `Use Qwen3 TTS to say "Hello, this is a test"`

### General Troubleshooting

If the extension doesn't load:
1. Verify the paths are correct
2. Check that the virtual environment has all dependencies
3. Restart Goose Desktop
4. Check Goose logs for errors
