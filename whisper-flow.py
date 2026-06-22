#!/usr/bin/env python3
"""
Whisper Flow v2.0 — Local voice-to-text with settings panel
A free, local alternative to Super Whisper.

Modes:
  python whisper-flow.py               → Start engine (record hotkey)
  python whisper-flow.py --settings    → Open settings panel in browser
  python whisper-flow.py --help        → Full options
"""

import argparse
import json
import os
import queue
import sys
import threading
import time
import warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore", message=".*symlinks.*")
warnings.filterwarnings("ignore", message=".*torch.classes.*")

# ─── CONFIG ───────────────────────────────────────────────────

CONFIG_DIR = Path.home() / ".whisper-flow"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "hotkey": "ctrl+shift+space",
    "model": "small.en",
    "device": "cpu",
    "compute_type": "int8",
    "lm_studio_url": "http://localhost:1234/v1",
    "lm_studio_model": "qwen2.5-coder-7b-instruct",
    "smart_cleanup": True,
    "auto_paste": True,
    "sample_rate": 16000,
    "input_device": None,
    "output_device": None,
    "silence_timeout": 5.0,
}


def load_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    with open(CONFIG_FILE, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    return dict(DEFAULT_CONFIG)


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


# ─── DEVICE LISTING ──────────────────────────────────────────

def list_devices():
    """Return structured list of audio devices."""
    import sounddevice as sd
    devices = sd.query_devices()
    inputs = []
    outputs = []
    for i, d in enumerate(devices):
        entry = {
            "index": i,
            "name": d["name"].strip(),
            "channels": d["max_input_channels"] if d["max_input_channels"] > 0 else d["max_output_channels"],
            "sample_rate": int(d["default_samplerate"]),
        }
        if d["max_input_channels"] > 0:
            inputs.append(entry)
        if d["max_output_channels"] > 0:
            outputs.append(entry)

    default_in = sd.default.device[0]
    default_out = sd.default.device[1]

    # Resolve default to actual device
    if isinstance(default_in, int) and default_in < len(devices):
        default_in_name = devices[default_in]["name"].strip()
    else:
        default_in_name = "System Default"

    if isinstance(default_out, int) and default_out < len(devices):
        default_out_name = devices[default_out]["name"].strip()
    else:
        default_out_name = "System Default"

    return {
        "inputs": inputs,
        "outputs": outputs,
        "default_input": default_in_name,
        "default_output": default_out_name,
    }


# ─── AUDIO RECORDER ──────────────────────────────────────────

class AudioRecorder:
    def __init__(self, sample_rate=16000, input_device=None, output_device=None):
        self.sample_rate = sample_rate
        self.input_device = input_device
        self.output_device = output_device
        self.audio_queue = queue.Queue()
        self.recording = False
        self.stream = None

    def _callback(self, indata, frames, time_info, status):
        if status:
            print(f"[audio] {status}")
        if self.recording:
            self.audio_queue.put(indata.copy())

    def start_recording(self):
        import sounddevice as sd
        self.audio_queue = queue.Queue()
        self.recording = True
        kwargs = dict(
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32',
            callback=self._callback,
        )
        if self.input_device is not None:
            kwargs['device'] = self.input_device
        self.stream = sd.InputStream(**kwargs)
        self.stream.start()
        return True

    def stop_recording(self):
        if not self.recording:
            return None
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        chunks = []
        while not self.audio_queue.empty():
            chunks.append(self.audio_queue.get_nowait())
        if not chunks:
            return None
        return np.concatenate(chunks, axis=0).flatten()


# ─── TRANSCRIBER ─────────────────────────────────────────────

class Transcriber:
    def __init__(self, model_name="small.en", device="cpu", compute_type="int8"):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load(self):
        from faster_whisper import WhisperModel
        print(f"[whisper] Loading '{self.model_name}' ({self.device}/{self.compute_type})...")
        t = time.time()
        self.model = WhisperModel(self.model_name, device=self.device, compute_type=self.compute_type)
        print(f"[whisper] Loaded in {time.time()-t:.1f}s")

    def transcribe(self, audio):
        if self.model is None:
            self.load()
        if audio is None or len(audio) == 0:
            return "", []
        segments, info = self.model.transcribe(audio, beam_size=1, language="en")
        text = " ".join(seg.text.strip() for seg in segments if seg.text.strip())
        return text, segments


# ─── TEXT CLEANER ────────────────────────────────────────────

class TextCleaner:
    def __init__(self, api_url="http://localhost:1234/v1", model="qwen2.5-coder-7b-instruct"):
        self.api_url = api_url
        self.model = model
        self.available = self._check_api()

    def _check_api(self):
        try:
            import requests
            resp = requests.get(f"{self.api_url}/models", timeout=3)
            return resp.status_code == 200
        except Exception:
            return False

    def is_available(self):
        return self.available

    def clean(self, text):
        if not text or not self.available:
            return text
        import requests
        try:
            resp = requests.post(
                f"{self.api_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a voice transcription cleaner. "
                                "Clean up the user's speech-to-text output. Rules:\n"
                                "1. Add proper punctuation and capitalization\n"
                                "2. Fix grammar and word fragments\n"
                                "3. Remove filler words (um, uh, like, you know, sort of, kind of)\n"
                                "4. Keep the exact meaning and intent\n"
                                "5. Return ONLY the cleaned text - no explanations, no quotes"
                            ),
                        },
                        {"role": "user", "content": text},
                    ],
                    "temperature": 0.2,
                    "max_tokens": len(text) + 100,
                },
                timeout=30,
            )
            result = resp.json()
            cleaned = result["choices"][0]["message"]["content"].strip()
            return cleaned if cleaned else text
        except Exception as e:
            print(f"[cleaner] Error: {e}")
            return text


# ─── HOTKEY PARSER ───────────────────────────────────────────

MOD_ALT = 0x0001
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

VK_MAP = {
    "space": 0x20, "enter": 0x0D, "tab": 0x09, "esc": 0x1B,
    "backspace": 0x08, "delete": 0x2E, "insert": 0x2D,
    "home": 0x24, "end": 0x23, "pageup": 0x21, "pagedown": 0x22,
    "up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
    "printscreen": 0x2C, "scrolllock": 0x91, "pause": 0x13,
    "capslock": 0x14, "numlock": 0x90,
    "`": 0xC0, "-": 0xBD, "=": 0xBB, "[": 0xDB,
    "]": 0xDD, "\\": 0xDC, ";": 0xBA, "'": 0xDE,
    ",": 0xBC, ".": 0xBE, "/": 0xBF,
}

# Add F1-F24 keys
for i in range(1, 25):
    VK_MAP[f"f{i}"] = 0x6F + i

# Add letters a-z
for c in "abcdefghijklmnopqrstuvwxyz":
    VK_MAP[c] = ord(c.upper())

# Add numbers 0-9
for i in range(10):
    VK_MAP[str(i)] = 0x30 + i


def parse_hotkey(hotkey_str):
    """
    Parse hotkey string like 'ctrl+shift+space' or 'f13' or 'scrolllock'.
    Returns (modifier_mask, virtual_key_code, is_single_key).
    """
    parts = hotkey_str.lower().split("+")
    modifier_mask = 0
    key = None

    for part in parts:
        part = part.strip()
        if part in ("ctrl", "control"):
            modifier_mask |= MOD_CONTROL
        elif part in ("alt",):
            modifier_mask |= MOD_ALT
        elif part in ("shift",):
            modifier_mask |= MOD_SHIFT
        elif part in ("win", "windows", "meta", "super"):
            modifier_mask |= MOD_WIN
        elif part in VK_MAP:
            key = VK_MAP[part]
        else:
            # Try to match as a single character
            if len(part) == 1:
                key = ord(part.upper())
            else:
                print(f"[hotkey] Unknown key: '{part}'")

    if key is None:
        print("[hotkey] No valid key found, defaulting to Space")
        key = 0x20

    is_single_key = (modifier_mask == 0)

    return modifier_mask, key, is_single_key


def send_paste():
    """Send Ctrl+V to paste into active window."""
    try:
        from pynput.keyboard import Controller, Key
        kb = Controller()
        with kb.pressed(Key.ctrl):
            kb.press('v')
            kb.release('v')
    except Exception as e:
        print(f"[paste] Error: {e}")


# ─── HOTKEY MANAGER (pynput-based, no admin needed) ──────────

class HotkeyManager:
    """Global hotkey listener using pynput (no admin required)."""

    def __init__(self, hotkey_str, on_activate):
        self.hotkey_str = hotkey_str
        self.on_activate = on_activate
        self.modifier_mask, self.vk_code, self.is_single_key = parse_hotkey(hotkey_str)
        self.listener = None
        self.running = False
        self._pressed_mods = set()
        self._activated = False  # debounce
        self._last_activation = 0

        # Map modifier bits to pynput key objects
        self._mod_keys = {}
        if self.modifier_mask & MOD_CONTROL:
            self._mod_keys['ctrl'] = None  # resolved dynamically
        if self.modifier_mask & MOD_ALT:
            self._mod_keys['alt'] = None
        if self.modifier_mask & MOD_SHIFT:
            self._mod_keys['shift'] = None
        if self.modifier_mask & MOD_WIN:
            self._mod_keys['win'] = None

        # Map VK code to key name for single-key detection
        import pynput.keyboard as kb
        self._target_key = self._vk_to_pynput(self.vk_code)

    def _vk_to_pynput(self, vk):
        """Convert virtual key code to pynput key or key code."""
        from pynput.keyboard import Key, KeyCode

        # Special keys
        special = {
            0x20: Key.space, 0x0D: Key.enter, 0x09: Key.tab,
            0x1B: Key.esc, 0x08: Key.backspace, 0x2E: Key.delete,
            0x2D: Key.insert, 0x24: Key.home, 0x23: Key.end,
            0x21: Key.page_up, 0x22: Key.page_down,
            0x26: Key.up, 0x28: Key.down, 0x25: Key.left, 0x27: Key.right,
            0x70: Key.f1, 0x71: Key.f2, 0x72: Key.f3, 0x73: Key.f4,
            0x74: Key.f5, 0x75: Key.f6, 0x76: Key.f7, 0x77: Key.f8,
            0x78: Key.f9, 0x79: Key.f10, 0x7A: Key.f11, 0x7B: Key.f12,
            0x7C: Key.f13, 0x7D: Key.f14, 0x7E: Key.f15, 0x7F: Key.f16,
            0x80: Key.f17, 0x81: Key.f18, 0x82: Key.f19, 0x83: Key.f20,
            0x2C: Key.print_screen, 0x91: Key.scroll_lock, 0x13: Key.pause,
            0x14: Key.caps_lock, 0x90: Key.num_lock,
        }
        if vk in special:
            return special[vk]

        # Letters and numbers
        if 0x30 <= vk <= 0x39:  # 0-9
            return KeyCode.from_char(chr(0x30 + (vk - 0x30)))
        if 0x41 <= vk <= 0x5A:  # A-Z
            return KeyCode.from_char(chr(vk).lower())

        return KeyCode.from_vk(vk)

    def _on_press(self, key):
        """Handle key press event."""
        from pynput.keyboard import Key, KeyCode
        import pynput.keyboard as kb

        # Track modifier keys
        try:
            if key in (Key.ctrl, Key.ctrl_l, Key.ctrl_r):
                self._pressed_mods.add('ctrl')
            elif key in (Key.alt, Key.alt_l, Key.alt_r):
                self._pressed_mods.add('alt')
            elif key in (Key.shift, Key.shift_l, Key.shift_r):
                self._pressed_mods.add('shift')
            elif key in (Key.cmd, Key.cmd_l, Key.cmd_r):
                self._pressed_mods.add('win')
        except:
            pass

        # Check if this is the target key
        is_target = False
        if isinstance(key, KeyCode):
            if self.is_single_key:
                # Single key mode: just match the key
                if key.vk == self.vk_code or key == self._target_key:
                    is_target = True
            else:
                # Modifier combo mode
                if key.vk == self.vk_code or key == self._target_key:
                    is_target = True

        if is_target:
            # Check modifiers are correct
            mods_held = self._pressed_mods.copy()
            needed_mods = set(self._mod_keys.keys())

            if self.is_single_key or mods_held == needed_mods:
                now = time.time()
                if now - self._last_activation > 0.3:  # debounce 300ms
                    self._last_activation = now
                    self.on_activate()

    def _on_release(self, key):
        """Handle key release event."""
        from pynput.keyboard import Key
        try:
            if key in (Key.ctrl, Key.ctrl_l, Key.ctrl_r):
                self._pressed_mods.discard('ctrl')
            elif key in (Key.alt, Key.alt_l, Key.alt_r):
                self._pressed_mods.discard('alt')
            elif key in (Key.shift, Key.shift_l, Key.shift_r):
                self._pressed_mods.discard('shift')
            elif key in (Key.cmd, Key.cmd_l, Key.cmd_r):
                self._pressed_mods.discard('win')
        except:
            pass

    def start(self):
        """Start listening for hotkey."""
        if self.running:
            return
        self.running = True
        from pynput.keyboard import Listener
        self.listener = Listener(on_press=self._on_press, on_release=self._on_release)
        self.listener.daemon = True
        self.listener.start()

    def stop(self):
        """Stop listening."""
        self.running = False
        if self.listener:
            self.listener.stop()
            self.listener = None


# ─── WHISPER FLOW ENGINE ─────────────────────────────────────

class WhisperFlowEngine:
    """Core engine: hotkey → record → transcribe → clean → paste."""

    def __init__(self, config=None):
        self.config = config or load_config()
        self.recorder = AudioRecorder(
            sample_rate=self.config["sample_rate"],
            input_device=self.config.get("input_device"),
            output_device=self.config.get("output_device"),
        )
        self.transcriber = Transcriber(
            model_name=self.config["model"],
            device=self.config["device"],
            compute_type=self.config["compute_type"],
        )
        self.cleaner = TextCleaner(
            api_url=self.config["lm_studio_url"],
            model=self.config["lm_studio_model"],
        )
        self.recording = False
        self.processing = False
        self.running = False
        self.hotkey_mgr = None

    def _beep(self, high=True):
        try:
            import winsound
            winsound.Beep(880 if high else 440, 150)
        except Exception:
            pass

    def _paste_text(self, text):
        if not text:
            print("[output] No text to paste")
            return
        import pyperclip
        pyperclip.copy(text)
        time.sleep(0.1)
        if self.config.get("auto_paste", True):
            send_paste()
            print(f"[output] Pasted ({len(text)} chars)")
        else:
            print(f"[output] Copied to clipboard ({len(text)} chars)")

    def _process_audio(self, audio):
        if audio is None or len(audio) < 4000:
            print("[flow] Audio too short, ignored")
            self.processing = False
            return
        self._beep(False)
        print("[flow] Transcribing...")
        t = time.time()
        raw_text, segments = self.transcriber.transcribe(audio)
        t_time = time.time() - t
        if not raw_text:
            print("[flow] No speech detected")
            self._beep(True)
            self.processing = False
            return
        print(f"[whisper] ({t_time:.1f}s) {raw_text[:100]}")
        if self.config.get("smart_cleanup", True) and self.cleaner.is_available():
            print("[flow] Cleaning...")
            t = time.time()
            final_text = self.cleaner.clean(raw_text)
            c_time = time.time() - t
            print(f"[cleaner] ({c_time:.1f}s) {final_text[:100]}")
        else:
            final_text = raw_text
        self._paste_text(final_text)
        self._beep(True)
        self.processing = False

    def toggle_recording(self):
        if self.processing:
            print("[flow] Still processing...")
            return
        if self.recording:
            print("[flow] Stopped")
            audio = self.recorder.stop_recording()
            self.recording = False
            if audio is not None:
                self.processing = True
                threading.Thread(target=self._process_audio, args=(audio,), daemon=True).start()
        else:
            print("[flow] Recording...")
            self.recorder.start_recording()
            self.recording = True
            self._beep(True)

    def start(self):
        """Start the engine in background mode."""
        self.running = True

        # Pre-load whisper
        print("[flow] Loading whisper model...")
        self.transcriber.load()

        # Start hotkey listener
        hotkey_str = self.config["hotkey"]
        self.hotkey_mgr = HotkeyManager(hotkey_str, self.toggle_recording)
        self.hotkey_mgr.start()

        # Show info
        lm_status = f"Available ({self.config['lm_studio_model']})" if self.cleaner.is_available() else "OFFLINE"
        print(f"\n{'='*50}")
        print(f"  Whisper Flow v2.0 — RUNNING")
        print(f"{'='*50}")
        print(f"  Hotkey:      {hotkey_str}")
        print(f"  Microphone:  {self.config.get('input_device', 'System Default')}")
        print(f"  Model:       {self.config['model']}")
        print(f"  Cleanup:     {lm_status}")
        print(f"  Auto-paste:  {self.config.get('auto_paste', True)}")
        print(f"{'='*50}")
        print(f"  Press hotkey to record, press again to transcribe")
        print(f"  Ctrl+C to stop")
        print(f"{'='*50}\n")

        # Keep alive
        try:
            while self.running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n[flow] Shutting down...")
        finally:
            self.stop()

    def stop(self):
        self.running = False
        if self.hotkey_mgr:
            self.hotkey_mgr.stop()
        if self.recording:
            self.recorder.stop_recording()
        print("[flow] Stopped.")


# ─── SETTINGS SERVER ─────────────────────────────────────────

def run_settings_server():
    """Start a local web server for the settings panel."""
    import http.server
    import socketserver
    import urllib.parse

    PORT = 18923  # Random high port

    class SettingsHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass  # Suppress logs

        def _send_json(self, data, status=200):
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        def _send_html(self, html):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())

        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            if path == "/":
                self._send_html(SETTINGS_HTML)
            elif path == "/api/devices":
                self._send_json(list_devices())
            elif path == "/api/config":
                self._send_json(load_config())
            elif path == "/api/status":
                cfg = load_config()
                self._send_json({"ok": True, "config": cfg})
            else:
                self._send_json({"error": "not found"}, 404)

        def do_POST(self):
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path

            if path == "/api/config":
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                try:
                    new_config = json.loads(body)
                    save_config(new_config)
                    self._send_json({"ok": True, "message": "Config saved"})
                except Exception as e:
                    self._send_json({"ok": False, "error": str(e)}, 400)

            elif path == "/api/test-mic":
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                data = json.loads(body) if body else {}
                device_idx = data.get("device", None)
                try:
                    import sounddevice as sd
                    duration = 2  # Record 2 seconds
                    print(f"[settings] Testing mic (device={device_idx}, {duration}s)...")
                    audio = sd.rec(
                        int(duration * 16000),
                        samplerate=16000,
                        channels=1,
                        dtype='float32',
                        device=device_idx if device_idx is not None else None,
                    )
                    sd.wait()
                    # Calculate RMS level
                    rms = float(np.sqrt(np.mean(audio ** 2)))
                    level = min(100, int(rms * 500))
                    self._send_json({
                        "ok": True,
                        "level": level,
                        "message": f"Mic test: level={level}%",
                    })
                except Exception as e:
                    self._send_json({"ok": False, "error": str(e)}, 500)

            else:
                self._send_json({"error": "not found"}, 404)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

    # Find available port
    for port in range(PORT, PORT + 10):
        try:
            httpd = socketserver.TCPServer(("127.0.0.1", port), SettingsHandler)
            break
        except OSError:
            continue
    else:
        print("[settings] Could not find available port")
        return

    url = f"http://127.0.0.1:{port}"
    print(f"\n{'='*50}")
    print(f"  Whisper Flow Settings")
    print(f"{'='*50}")
    print(f"  Open in browser: {url}")
    print(f"  Close this window to stop settings server")
    print(f"{'='*50}\n")

    # Open browser
    import webbrowser
    webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[settings] Closed.")
        httpd.shutdown()


# ─── SETTINGS HTML (embedded) ────────────────────────────────

SETTINGS_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Whisper Flow Settings</title>
<style>
:root {
    --bg: #0d1117; --surface: #161b22; --border: #30363d;
    --text: #e6edf3; --muted: #8b949e;
    --green: #3fb950; --blue: #58a6ff; --red: #f85149;
    --yellow: #d29922;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
    background:var(--bg); color:var(--text);
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
    max-width:800px; margin:0 auto; padding:40px 20px;
}
h1 { font-size:26px; margin-bottom:4px; }
.sub { color:var(--muted); margin-bottom:28px; font-size:14px; }
.card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:12px; padding:24px; margin-bottom:20px;
}
.card h2 { font-size:16px; margin-bottom:16px; color:var(--blue); }
.row { display:flex; gap:12px; margin-bottom:16px; flex-wrap:wrap; }
.field { flex:1; min-width:200px; }
.field label { display:block; font-size:13px; color:var(--muted); margin-bottom:6px; }
.field select, .field input {
    width:100%; background:var(--bg); color:var(--text);
    border:1px solid var(--border); border-radius:6px;
    padding:10px 12px; font-size:14px; outline:none;
}
.field select:focus, .field input:focus { border-color:var(--blue); }
.field select option { background:var(--surface); }
.hint { font-size:12px; color:var(--muted); margin-top:4px; }
.btn {
    background:var(--blue); color:#fff; border:none;
    border-radius:6px; padding:10px 20px; font-size:14px;
    cursor:pointer; transition:.15s;
}
.btn:hover { background:#4c8ed9; }
.btn.green { background:#238636; }
.btn.green:hover { background:#2ea043; }
.btn.red { background:var(--red); }
.btn.red:hover { background:#da3633; }
.btn:disabled { opacity:0.5; cursor:default; }
.status-badge {
    display:inline-block; padding:3px 10px; border-radius:8px;
    font-size:12px; font-weight:500;
}
.status-badge.ok { background:rgba(63,185,80,0.12); color:var(--green); }
.status-badge.warn { background:rgba(210,153,34,0.12); color:var(--yellow); }
.status-badge.err { background:rgba(248,81,73,0.12); color:var(--red); }
.actions { display:flex; gap:12px; flex-wrap:wrap; margin-top:16px; }
.mic-test {
    display:flex; align-items:center; gap:12px; margin-top:12px;
}
.mic-level {
    flex:1; height:8px; background:var(--bg); border-radius:4px; overflow:hidden;
}
.mic-level-bar {
    height:100%; border-radius:4px; transition:width .2s, background .2s;
    width:0%; background:var(--green);
}
.mic-level-bar.low { background:var(--green); }
.mic-level-bar.mid { background:var(--yellow); }
.mic-level-bar.high { background:var(--red); }
#toast {
    position:fixed; bottom:24px; right:24px;
    background:var(--surface); border:1px solid var(--border);
    border-radius:8px; padding:12px 20px; font-size:14px;
    box-shadow:0 8px 24px rgba(0,0,0,.4);
    opacity:0; transform:translateY(10px);
    transition:.3s; pointer-events:none;
}
#toast.show { opacity:1; transform:translateY(0); }
@media(max-width:600px) { .row { flex-direction:column; } }
</style>
</head>
<body>
<h1>🎤 Whisper Flow</h1>
<p class="sub">Configure your microphone, hotkey, and transcription settings</p>

<div class="card">
  <h2>🎯 Hotkey</h2>
  <div class="row">
    <div class="field">
      <label>Activation key</label>
      <input type="text" id="hotkey" placeholder="ctrl+shift+space" value="ctrl+shift+space">
      <div class="hint">Examples: ctrl+shift+space, f13, scrolllock, ctrl+alt+v</div>
    </div>
  </div>
</div>

<div class="card">
  <h2>🎙️ Microphone</h2>
  <div class="row">
    <div class="field">
      <label>Input device</label>
      <select id="inputDevice"></select>
      <div class="hint">Select your microphone</div>
    </div>
  </div>
  <button class="btn" id="testMicBtn" onclick="testMic()">🎤 Test Microphone</button>
  <div class="mic-test" id="micTestResult" style="display:none">
    <span id="micLevelText" style="font-size:13px;min-width:60px;">Level: 0%</span>
    <div class="mic-level"><div class="mic-level-bar" id="micLevelBar"></div></div>
  </div>
</div>

<div class="card">
  <h2>🔊 Speaker (for confirmation beeps)</h2>
  <div class="row">
    <div class="field">
      <label>Output device</label>
      <select id="outputDevice"></select>
      <div class="hint">Where you hear the beep sounds</div>
    </div>
  </div>
</div>

<div class="card">
  <h2>⚙️ Transcription</h2>
  <div class="row">
    <div class="field">
      <label>Whisper model</label>
      <select id="model">
        <option value="tiny.en">Tiny (fastest, least accurate)</option>
        <option value="base.en">Base (fast)</option>
        <option value="small.en" selected>Small (balanced) ✅</option>
        <option value="medium">Medium (accurate, slower)</option>
      </select>
    </div>
    <div class="field">
      <label>Smart cleanup (LM Studio)</label>
      <select id="smartCleanup">
        <option value="true">ON — fixes grammar, punctuation, fillers</option>
        <option value="false">OFF — raw transcription only</option>
      </select>
    </div>
  </div>
  <div class="row">
    <div class="field">
      <label>Output mode</label>
      <select id="autoPaste">
        <option value="true">Auto-paste into active window</option>
        <option value="false">Copy to clipboard only</option>
      </select>
    </div>
  </div>
</div>

<div class="actions">
  <button class="btn green" onclick="saveSettings()">💾 Save Settings</button>
  <button class="btn" onclick="loadSettings()">🔄 Reload</button>
  <span id="saveStatus"></span>
</div>

<div id="toast"></div>

<script>
async function api(path, opts={}) {
    const resp = await fetch(path, {
        ...opts,
        headers: {'Content-Type': 'application/json', ...opts.headers}
    });
    return resp.json();
}

async function loadSettings() {
    const cfg = await api('/api/config');
    const devices = await api('/api/devices');

    document.getElementById('hotkey').value = cfg.hotkey || 'ctrl+shift+space';
    document.getElementById('model').value = cfg.model || 'small.en';
    document.getElementById('smartCleanup').value = String(cfg.smart_cleanup);
    document.getElementById('autoPaste').value = String(cfg.auto_paste);

    // Populate input devices
    const inSel = document.getElementById('inputDevice');
    inSel.innerHTML = '<option value="">System Default</option>';
    devices.inputs.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.index;
        opt.textContent = `${d.name} (${d.channels}ch, ${d.sample_rate}Hz)`;
        if (d.name === cfg.input_device || String(d.index) === String(cfg.input_device)) opt.selected = true;
        inSel.appendChild(opt);
    });

    // Populate output devices
    const outSel = document.getElementById('outputDevice');
    outSel.innerHTML = '<option value="">System Default</option>';
    devices.outputs.forEach(d => {
        const opt = document.createElement('option');
        opt.value = d.index;
        opt.textContent = `${d.name} (${d.channels}ch, ${d.sample_rate}Hz)`;
        if (d.name === cfg.output_device || String(d.index) === String(cfg.output_device)) opt.selected = true;
        outSel.appendChild(opt);
    });
}

async function saveSettings() {
    const btn = document.querySelector('.btn.green');
    btn.disabled = true;
    btn.textContent = 'Saving...';
    
    const config = {
        hotkey: document.getElementById('hotkey').value.trim(),
        model: document.getElementById('model').value,
        smart_cleanup: document.getElementById('smartCleanup').value === 'true',
        auto_paste: document.getElementById('autoPaste').value === 'true',
        input_device: document.getElementById('inputDevice').value || null,
        output_device: document.getElementById('outputDevice').value || null,
    };

    const result = await api('/api/config', {
        method: 'POST',
        body: JSON.stringify(config)
    });

    btn.disabled = false;
    btn.textContent = '💾 Save Settings';

    if (result.ok) {
        showToast('Settings saved! Restart Whisper Flow to apply.');
    } else {
        showToast('Error: ' + (result.error || 'Unknown'), true);
    }
}

let micTestTimer = null;

async function testMic() {
    const btn = document.getElementById('testMicBtn');
    const resultDiv = document.getElementById('micTestResult');
    const bar = document.getElementById('micLevelBar');
    const text = document.getElementById('micLevelText');
    const device = document.getElementById('inputDevice').value || null;

    btn.disabled = true;
    btn.textContent = '🎤 Testing... (2s)';
    resultDiv.style.display = 'flex';

    for (let i = 0; i < 4; i++) {
        const result = await api('/api/test-mic', {
            method: 'POST',
            body: JSON.stringify({ device: device ? parseInt(device) : null })
        });
        if (result.ok) {
            const level = result.level;
            bar.style.width = level + '%';
            bar.className = 'mic-level-bar ' + (level > 70 ? 'high' : level > 40 ? 'mid' : 'low');
            text.textContent = 'Level: ' + level + '%';
        }
    }

    btn.disabled = false;
    btn.textContent = '🎤 Test Microphone';
}

function showToast(msg, isError) {
    const t = document.getElementById('toast');
    t.textContent = '✓ ' + msg;
    t.style.color = isError ? 'var(--red)' : 'var(--green)';
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}

// Load on page open
loadSettings();
</script>
</body>
</html>"""

# ─── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Whisper Flow — Local voice-to-text")
    parser.add_argument("--settings", action="store_true", help="Open settings panel in browser")
    parser.add_argument("--hotkey", help="Set hotkey (e.g., 'ctrl+shift+space', 'f13', 'scrolllock')")
    parser.add_argument("--model", help="Whisper model (tiny.en, base.en, small.en, medium)")
    parser.add_argument("--no-cleanup", action="store_true", help="Disable smart cleanup")
    parser.add_argument("--clipboard-only", action="store_true", help="Copy only, don't paste")
    parser.add_argument("--list-devices", action="store_true", help="List audio devices and exit")
    parser.add_argument("--config", action="store_true", help="Show current config and exit")
    args = parser.parse_args()

    if args.list_devices:
        import sounddevice as sd
        print("\n=== Microphones (Input Devices) ===\n")
        for d in list_devices()["inputs"]:
            print(f'  [{d["index"]}] {d["name"]} ({d["channels"]}ch, {d["sample_rate"]}Hz)')
        print("\n=== Speakers (Output Devices) ===\n")
        for d in list_devices()["outputs"]:
            print(f'  [{d["index"]}] {d["name"]} ({d["channels"]}ch, {d["sample_rate"]}Hz)')
        return

    if args.config:
        print(json.dumps(load_config(), indent=2))
        return

    if args.settings:
        run_settings_server()
        return

    # Apply CLI overrides
    config = load_config()
    if args.hotkey:
        config["hotkey"] = args.hotkey
    if args.model:
        config["model"] = args.model
    if args.no_cleanup:
        config["smart_cleanup"] = False
    if args.clipboard_only:
        config["auto_paste"] = False

    save_config(config)

    # Launch engine
    engine = WhisperFlowEngine(config)
    engine.start()


if __name__ == "__main__":
    main()
