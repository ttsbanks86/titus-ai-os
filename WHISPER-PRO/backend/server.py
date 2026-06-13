#!/usr/bin/env python3
"""Whisper My Idea Pro — Backend Server (Transcription + Intelligence)"""
import sys, json, os, uuid, tempfile, subprocess, signal, threading, time, ctypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# ─── Global Hotkey Listener ──────────────────────────────────────────────
toggle_requested = False
capture_mode = False
captured_key = None

def start_global_listener():
    """Background thread that listens for the configured hotkey (mouse + keyboard)."""
    try:
        from pynput import mouse, keyboard
        
        def on_click(x, y, button, pressed):
            global toggle_requested, capture_mode, captured_key
            if not pressed: return
            btn_name = str(button).replace('Button.', '')
            if capture_mode:
                captured_key = f"Mouse {btn_name}"
                return False  # Stop listener
            if btn_name == "middle":
                toggle_requested = True
        
        def on_press(key):
            global toggle_requested, capture_mode, captured_key
            try:
                k = key.char if hasattr(key, 'char') and key.char else str(key).replace('Key.', '')
            except:
                k = str(key).replace('Key.', '')
            if capture_mode:
                captured_key = k
                return False
            # Check keyboard hotkeys
            settings = load_json(os.path.join(DATA_DIR, "settings.json"), {})
            hk = settings.get("hotkey", "")
            if hk and hk == k:
                toggle_requested = True
        
        with mouse.Listener(on_click=on_click) as ml, keyboard.Listener(on_press=on_press) as kl:
            ml.join()
            kl.join()
    except:
        pass

# Start in a daemon thread
listener_thread = threading.Thread(target=start_global_listener, daemon=True)
listener_thread.start()

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
PORT = int(os.environ.get("WMIP_PORT", "18927"))
DATA_DIR = os.path.join(os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)), "..", "data")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
VOCAB_FILE = os.path.join(DATA_DIR, "vocabulary.json")
STATS_FILE = os.path.join(DATA_DIR, "stats.json")

# Ensure data dirs
os.makedirs(DATA_DIR, exist_ok=True)

# ─── Model ──────────────────────────────────────────────────────────────
model = None
model_load_attempted = False

def load_model(size="tiny", device="cpu"):
    global model, model_load_attempted
    if model_load_attempted and model is None:
        return False  # Don't retry if previously failed
    model_load_attempted = True
    try:
        from faster_whisper import WhisperModel
        print(f"[WMIP] Loading model '{size}' on {device}...")
        import sys; sys.stdout.flush()
        model = WhisperModel(size, device=device, compute_type="default", num_workers=1)
        print(f"[WMIP] Model loaded successfully")
        return True
    except Exception as e:
        print(f"[WMIP] Model error: {e}")
        return False

# ─── Data helpers ────────────────────────────────────────────────────────
def load_json(path, default=None):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f: return json.load(f)
        except: pass
    return default if default is not None else {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_stats():
    stats = load_json(STATS_FILE, {"session_words": 0, "total_words": 0, "sessions": 0, "history": []})
    stats.setdefault("weekly", {})
    return stats

def update_stats(text):
    stats = get_stats()
    words = len(text.split())
    stats["session_words"] = stats.get("session_words", 0) + words
    stats["total_words"] = stats.get("total_words", 0) + words
    stats["sessions"] = stats.get("sessions", 0) + 1
    save_json(STATS_FILE, stats)
    return stats

# ─── Vocabulary ──────────────────────────────────────────────────────────
def get_vocab():
    return load_json(VOCAB_FILE, {"words": [], "phrases": []})

def add_vocab(word, category="words"):
    v = get_vocab()
    if word not in v.get(category, []):
        v.setdefault(category, []).append(word)
        save_json(VOCAB_FILE, v)
    return v

# ─── History ─────────────────────────────────────────────────────────────
def get_history(limit=50):
    h = load_json(HISTORY_FILE, [])
    return h[-limit:][::-1]  # most recent first

def add_history(text, mode="Voice", duration=0):
    h = load_json(HISTORY_FILE, [])
    entry = {
        "id": str(uuid.uuid4())[:8],
        "text": text,
        "mode": mode,
        "duration": duration,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "words": len(text.split())
    }
    h.append(entry)
    # Keep last 500 entries
    if len(h) > 500: h = h[-500:]
    save_json(HISTORY_FILE, h)
    return entry

# ─── Transcription ────────────────────────────────────────────────────────
def transcribe_audio(audio_data, mode="Voice", hotwords=None):
    global model
    if model is None:
        if not load_model():
            return "Model not loaded"
    try:
        tmp_wav = os.path.join(tempfile.gettempdir(), f"wmi_{uuid.uuid4().hex}.wav")
        tmp_webm = tmp_wav + ".webm"
        with open(tmp_webm, "wb") as f: f.write(audio_data)
        
        if os.path.getsize(tmp_webm) == 0:
            os.remove(tmp_webm)
            return "No audio data"
        
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", tmp_webm, "-ar", "16000", "-ac", "1", tmp_wav],
            capture_output=True, timeout=30,
            creationflags=0x08000000 if sys.platform == "win32" else 0
        )
        os.remove(tmp_webm)
        
        if result.returncode != 0 or not os.path.exists(tmp_wav):
            return "Audio conversion failed"
        
        # Apply vocabulary as hotwords
        initial_prompt = None
        vocab = get_vocab()
        all_terms = vocab.get("words", []) + vocab.get("phrases", [])
        if all_terms:
            initial_prompt = ", ".join(all_terms)
        
        segs, _ = model.transcribe(tmp_wav, beam_size=3, initial_prompt=initial_prompt, language="en")
        text = " ".join(s.text.strip() for s in segs)
        
        if os.path.exists(tmp_wav): os.remove(tmp_wav)
        
        if not text: return "No speech detected"
        
        # Mode-based formatting
        if mode == "Email":
            text = text.strip()
        elif mode == "Bullets":
            lines = [f"• {s.strip()}" for s in text.split(". ") if s.strip()]
            text = "\n".join(lines)
        elif mode == "Meeting":
            text = f"[Meeting Notes]\n{text}"
        
        # Update stats and history
        update_stats(text)
        add_history(text, mode)
        
        return text
    except Exception as e:
        return f"Error: {e}"

# ─── HTTP Handler ────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/status":
            self._json({
                "status": "ok", "model": model is not None,
                "stats": get_stats(), "vocab_size": len(get_vocab().get("words", [])),
                "history_count": len(load_json(HISTORY_FILE, [])),
                "mode": "Voice"
            })
        elif path == "/history":
            self._json(get_history())
        elif path == "/vocabulary":
            self._json(get_vocab())
        elif path == "/stats":
            self._json(get_stats())
        elif path == "/models":
            self._json({"available": ["tiny", "base", "small", "medium"], "current": "tiny"})
        elif path == "/capture-status":
            global capture_mode, captured_key
            ck = captured_key
            captured_key = None
            self._json({"capturing": capture_mode, "key": ck})
        elif path == "/toggle-event":
            global toggle_requested
            if toggle_requested:
                toggle_requested = False
                self._json({"toggle": True})
            else:
                self._json({"toggle": False})
        elif path == "/settings":
            self._json(load_json(os.path.join(DATA_DIR, "settings.json"), {"hotkey": "Alt+Space"}))
        else:
            self.send_error(404)

    def do_POST(self):
        global capture_mode, captured_key
        path = urlparse(self.path).path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len)
        
        if path == "/transcribe":
            import json as j
            try:
                data = j.loads(body)
                audio_path = data.get("audio_path", "")
                mode = data.get("mode", "Voice")
                text = transcribe_audio_raw_path(audio_path, mode)
                self._json({"text": text})
            except Exception as e:
                self._json({"text": f"Error: {e}"})
        elif path == "/transcribe-blob":
            import json as j
            ct = self.headers.get("Content-Type", "")
            if "multipart" in ct or "octet-stream" in ct:
                text = transcribe_audio(body, "Voice")
                self._json({"text": text})
            else:
                self._json({"text": "Use blob upload"})
        elif path == "/vocabulary/add":
            data = json.loads(body)
            w = data.get("word", "")
            cat = data.get("category", "words")
            self._json(add_vocab(w, cat))
        elif path == "/vocabulary/remove":
            data = json.loads(body)
            w = data.get("word", "")
            cat = data.get("category", "words")
            v = get_vocab()
            if w in v.get(cat, []):
                v[cat].remove(w)
                save_json(VOCAB_FILE, v)
            self._json(v)
        elif path == "/history/clear":
            save_json(HISTORY_FILE, [])
            self._json({"status": "cleared"})
        elif path == "/history/save":
            data = json.loads(body)
            save_json(HISTORY_FILE, data.get("history", []))
            self._json({"status": "saved"})
        elif path == "/stats/reset":
            save_json(STATS_FILE, {"session_words": 0, "total_words": 0, "sessions": 0, "weekly": {}})
            self._json({"status": "reset"})
        elif path == "/model/switch":
            data = json.loads(body)
            size = data.get("size", "tiny")
            ok = load_model(size)
            self._json({"status": "ok" if ok else "failed", "model": size})
        elif path == "/capture-start":
            capture_mode = True
            captured_key = None
            self._json({"capturing": True})
        elif path == "/set-hotkey":
            data = json.loads(body)
            hk = data.get("hotkey", "Alt+Space")
            settings = load_json(os.path.join(DATA_DIR, "settings.json"), {})
            settings["hotkey"] = hk
            save_json(os.path.join(DATA_DIR, "settings.json"), settings)
            self._json({"hotkey": hk})
        else:
            self.send_error(404)

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

def transcribe_audio_raw_path(audio_path, mode="Voice", hotwords=None):
    """Transcribe from raw file path (for Electron frontend)"""
    global model
    if model is None and not load_model():
        return "Model not loaded"
    try:
        import json as j
        initial_prompt = None
        vocab = get_vocab()
        all_terms = vocab.get("words", []) + vocab.get("phrases", [])
        if all_terms:
            initial_prompt = ", ".join(all_terms)
        
        segs, _ = model.transcribe(audio_path, beam_size=3, initial_prompt=initial_prompt, language="en")
        text = " ".join(s.text.strip() for s in segs)
        if not text: return "No speech detected"
        
        if mode == "Bullets":
            lines = [f"• {s.strip()}" for s in text.split(". ") if s.strip()]
            text = "\n".join(lines)
        
        update_stats(text)
        add_history(text, mode)
        return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # Don't load model at startup - lazy load on first request
    print(f"[WMIP] Server starting on port {PORT}")
    sys.stdout.flush()
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    server.serve_forever()
