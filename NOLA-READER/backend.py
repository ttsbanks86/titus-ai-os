#!/usr/bin/env python3
"""NOLA Voice Reader Backend — Clipboard Monitor + TTS"""
import sys, json, threading, ctypes, os, uuid, tempfile, signal, time, re, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import pyperclip

# Suppress terminal windows when spawning processes from windowed EXE
if getattr(sys, 'frozen', False):
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0

def create_subprocess(args, **kwargs):
    """Spawn process without flashing a terminal window."""
    kwargs.setdefault('creationflags', CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
    return subprocess.run(args, **kwargs)

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
PORT = int(os.environ.get("NR_PORT", "18926"))

# TTS path
TTS_CLI = os.path.join("C:\\Users\\tbank\\Desktop\\Live Cowork\\video-automation", "tts-cli.js")
ALT_PATHS = [TTS_CLI,
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "video-automation", "tts-cli.js"),
    os.path.join(os.path.dirname(__file__), "tts-cli.js")]

# State
clipboard_history = [""]
current_text = ""
is_listening = True
current_voice = "af_sarah"
current_provider = "kokoro"
current_speed = "1.0"
last_clip = ""
listener_active = False

NODE_BIN = "C:\\Program Files\\nodejs\\node.exe"
if not os.path.exists(NODE_BIN):
    NODE_BIN = "node"  # fallback

def find_tts():
    for p in ALT_PATHS:
        if os.path.exists(p): return p
    return None

def generate_tts(text, voice, provider):
    tts = find_tts()
    if not tts: return None
    try:
        out_path = os.path.join(tempfile.gettempdir(), f"nola_{uuid.uuid4().hex}.wav")
        # TTS CLI creates files in working directory
        cwd = os.getcwd()
        result = create_subprocess([NODE_BIN, tts, text[:2000], voice, provider],
                                  capture_output=True, timeout=120, text=True, cwd=cwd)
        if result.returncode != 0: return None
        # Search for generated WAV in working dir and temp
        search_dirs = [cwd, tempfile.gettempdir(), os.path.dirname(tts)]
        for d in search_dirs:
            if not os.path.isdir(d): continue
            wavs = [f for f in os.listdir(d) if f.startswith("tts-output-") and f.endswith(".wav")]
            if wavs:
                latest = max([os.path.join(d, f) for f in wavs], key=os.path.getmtime)
                if latest != out_path:
                    if os.path.exists(out_path): os.remove(out_path)
                    os.rename(latest, out_path)
                return out_path
        return None
    except: return None

def clipboard_listener():
    global last_clip, current_text, is_listening, listener_active
    listener_active = True
    last_clip = pyperclip.paste()
    while listener_active:
        try:
            time.sleep(0.5)
            if not is_listening: continue
            new_clip = pyperclip.paste()
            if new_clip != last_clip and new_clip.strip():
                last_clip = new_clip
                current_text = new_clip
                # Auto-generate TTS when clipboard changes
                audio_path = generate_tts(new_clip, current_voice, current_provider)
                if audio_path:
                    clipboard_history.append(new_clip)
                    if len(clipboard_history) > 50:
                        clipboard_history.pop(0)
        except: pass

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/status":
            self._json({
                "status": "ok",
                "listening": is_listening,
                "tts_available": find_tts() is not None,
                "clipboard": current_text[:200] if current_text else "",
                "history_count": len(clipboard_history),
                "voice": current_voice,
                "provider": current_provider,
                "speed": current_speed
            })
        elif path == "/clipboard":
            self._json({"text": current_text, "last": last_clip})
        elif path == "/history":
            self._json({"history": clipboard_history[-20:]})
        elif path == "/voices":
            self._json({"voices": {
                "kokoro": ["af_sarah","af_alloy","af_bella","af_nova","af_sky","af_heart",
                          "am_adam","am_echo","am_eric","am_fenrir","am_liam","am_michael",
                          "am_onyx","am_puck","am_santa","jf_alpha","jf_gongbei","jf_nezumi",
                          "jm_kumo","pf_dora","pm_alex","pm_baba","pm_santa","zf_xiaobei"],
                "supertonic": ["F1","F2","F3","F4","F5","M1","M2","M3","M4","M5"],
                "edge": ["en-US-AriaNeural","en-US-JennyNeural","en-US-GuyNeural",
                        "en-US-EricNeural","en-US-DavisNeural","en-GB-SoniaNeural"]
            }})
        elif path == "/audio":
            qs = {k: v[0] for k, v in (p.split('=') for p in parsed.query.split('&') if '=' in p)}
            ap = qs.get("path", "")
            if ap and os.path.exists(ap):
                self.send_response(200)
                self.send_header("Content-Type", "audio/wav")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(os.path.getsize(ap)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                with open(ap, "rb") as f:
                    self.wfile.write(f.read())
            else: self.send_error(404)
        else: self.send_error(404)

    def do_POST(self):
        global is_listening, current_voice, current_provider, current_speed, current_text
        path = urlparse(self.path).path
        content_len = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_len)) if content_len else {}

        if path == "/toggle":
            is_listening = body.get("listening", not is_listening)
            self._json({"listening": is_listening})
        elif path == "/settings":
            current_voice = body.get("voice", current_voice)
            current_provider = body.get("provider", current_provider)
            current_speed = body.get("speed", current_speed)
            self._json({"voice": current_voice, "provider": current_provider, "speed": current_speed})
        elif path == "/speak":
            text = body.get("text", current_text)
            voice = body.get("voice", current_voice)
            provider = body.get("provider", current_provider)
            audio = generate_tts(text, voice, provider)
            if audio: self._json({"success": True, "audioPath": audio, "text": text[:80]})
            else: self._json({"error": "TTS generation failed"})
        elif path == "/test":
            voice = body.get("voice", current_voice)
            provider = body.get("provider", current_provider)
            audio = generate_tts("Hello, this is a voice test. I am the NOLA Voice Reader.", voice, provider)
            if audio: self._json({"success": True, "audioPath": audio})
            else: self._json({"error": "Voice test failed"})
        else: self.send_error(404)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, *args): pass

if __name__ == "__main__":
    # Start clipboard listener in background
    t = threading.Thread(target=clipboard_listener, daemon=True)
    t.start()
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"[NOLA Reader] Running on port {PORT}")
    server.serve_forever()
