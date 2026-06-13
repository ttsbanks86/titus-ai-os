#!/usr/bin/env python3
"""NOLA Voice Launcher"""
import sys, os, json, threading, ctypes, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
PORT = 18925
APP_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(APP_DIR, "app.html")

model = None
try:
    from faster_whisper import WhisperModel
    model = WhisperModel("tiny", device="auto", compute_type="int8")
except: pass

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if os.path.exists(HTML_PATH):
            with open(HTML_PATH, "rb") as f: self.wfile.write(f.read())
        else:
            self.wfile.write(b"<h1>NOLA Voice</h1><p>app.html not found</p>")
    
    def do_POST(self):
        import tempfile, uuid, subprocess
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len)
        text = ""
        if model:
            try:
                tmp = os.path.join(tempfile.gettempdir(), f"nola_{uuid.uuid4().hex}.wav")
                webm_path = tmp + ".webm"
                with open(webm_path, "wb") as f: f.write(body)
                subprocess.run(["ffmpeg", "-y", "-i", webm_path, "-ar", "16000", "-ac", "1", tmp], capture_output=True, timeout=30)
                segs, _ = model.transcribe(tmp, beam_size=5)
                text = " ".join(s.text.strip() for s in segs)
                os.remove(webm_path)
                if os.path.exists(tmp): os.remove(tmp)
            except: text = "Error processing audio"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"text": text or "No speech detected"}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, *args): pass

server = HTTPServer(("127.0.0.1", PORT), Handler)
print(f"[NOLA Voice] http://127.0.0.1:{PORT}")
webbrowser.open(f"http://127.0.0.1:{PORT}")
server.serve_forever()