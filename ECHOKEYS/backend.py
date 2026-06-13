#!/usr/bin/env python3
"""EchoKeys Backend — transcription server only, no browser"""
import sys, json, threading, ctypes, os, uuid, tempfile, subprocess, signal
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
PORT = int(os.environ.get("EK_PORT", "18924"))

model = None
try:
    from faster_whisper import WhisperModel
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
except Exception as e:
    print(f"[EchoKeys Backend] Model error: {e}")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if urlparse(self.path).path == "/status":
            self._json({"status": "ok", "model": model is not None})
        else:
            self.send_error(404)
    
    def do_POST(self):
        if urlparse(self.path).path == "/transcribe":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len)
            text = self._transcribe(body)
            self._json({"text": text})
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def _transcribe(self, audio_data):
        if not model: return "Model not loaded"
        try:
            tmp = os.path.join(tempfile.gettempdir(), f"ek_{uuid.uuid4().hex}.wav")
            webm_path = tmp + ".webm"
            with open(webm_path, "wb") as f: f.write(audio_data)
            if os.path.getsize(webm_path) == 0:
                os.remove(webm_path)
                return "No audio data received"
            result = subprocess.run(["ffmpeg", "-y", "-i", webm_path, "-ar", "16000", "-ac", "1", tmp],
                         capture_output=True, timeout=30)
            if result.returncode != 0:
                err = result.stderr.decode(errors='ignore')[-200:]
                os.remove(webm_path)
                return f"Audio conversion failed: {err}"
            if not os.path.exists(tmp) or os.path.getsize(tmp) == 0:
                os.remove(webm_path)
                return "Audio conversion produced empty file"
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
    
    def log_message(self, *args): pass

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    server.serve_forever()