#!/usr/bin/env python3
"""EchoKeys Pro Launcher — serves app.html, handles transcription"""
import sys, json, threading, ctypes, os, io, signal, uuid, tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
PORT = 18924
APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(APP_DIR, "app.html")

model = None
try:
    from faster_whisper import WhisperModel
    model = WhisperModel("tiny", device="auto", compute_type="int8")
    print(f"[EchoKeys] Model loaded: tiny (GPU)")
except Exception as e:
    print(f"[EchoKeys] Model load: {e}")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/status":
            self._json({"status": "ok", "model": model is not None})
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if os.path.exists(HTML_PATH):
            with open(HTML_PATH, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.wfile.write(b"<h1>EchoKeys</h1><p>app.html not found</p>")
    
    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/transcribe":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len)
            text = self._transcribe(body)
            self._json({"text": text})
            return
        self.send_response(404); self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def _transcribe(self, audio_data):
        if not model:
            return "Transcription model not loaded. Check console."
        try:
            tmp = os.path.join(tempfile.gettempdir(), f"ek_{uuid.uuid4().hex}.wav")
            # Convert webm to wav with ffmpeg
            import subprocess
            webm_path = tmp + ".webm"
            with open(webm_path, "wb") as f:
                f.write(audio_data)
            subprocess.run(["ffmpeg", "-y", "-i", webm_path, "-ar", "16000", "-ac", "1", tmp],
                         capture_output=True, timeout=30)
            segs, _ = model.transcribe(tmp, beam_size=5)
            text = " ".join(s.text.strip() for s in segs)
            os.remove(webm_path)
            if os.path.exists(tmp): os.remove(tmp)
            return text or "No speech detected"
        except Exception as e:
            return f"Error: {e}"
    
    def _json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def log_message(self, format, *args):
        pass  # silence logs

def main():
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"[EchoKeys] Server on http://127.0.0.1:{PORT}")
    print(f"[EchoKeys] Open in browser or use Edge app mode")
    import webbrowser
    webbrowser.open(f"http://127.0.0.1:{PORT}")
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    server.serve_forever()

if __name__ == "__main__":
    main()