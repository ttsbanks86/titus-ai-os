#!/usr/bin/env python3
"""
Command Portal
A tiny local chatbot-style portal for sending plain-English commands into OpenCode.
"""

from __future__ import annotations

import json
import socketserver
import http.server
import urllib.parse
from datetime import datetime
from pathlib import Path

BASE = Path(r"C:\Users\tbank\Desktop\Live Cowork")
PROJECT_DIR = BASE / "PROJECTS" / "Command Portal"
INBOX = PROJECT_DIR / "INBOX.md"
PORT = 8787

PROJECTS = [
    "General Inbox",
    "Bible School",
    "EchoKey",
    "Personal Reader",
    "SkillVault",
    "AI App Dock",
    "iPhone Apps",
    "PKX Projects",
    "Photos and Assets",
    "NOLO Open Door",
    "Career Ops",
]

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Command Portal</title>
<style>
:root{--bg:#0d1117;--panel:#161b22;--panel2:#0f1623;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--blue:#58a6ff;--green:#3fb950;--yellow:#d29922;--red:#f85149}
*{box-sizing:border-box} body{margin:0;background:radial-gradient(circle at top,#172033 0,#0d1117 45%);color:var(--text);font-family:Segoe UI,system-ui,sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:18px}.app{width:min(760px,100%);background:rgba(22,27,34,.96);border:1px solid var(--border);border-radius:22px;box-shadow:0 20px 70px rgba(0,0,0,.45);overflow:hidden}.top{padding:22px 22px 14px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;gap:14px;align-items:center}.brand h1{font-size:22px;margin:0}.brand p{font-size:13px;color:var(--muted);margin:5px 0 0}.pill{border:1px solid rgba(88,166,255,.35);color:var(--blue);padding:5px 10px;border-radius:99px;font-size:12px;white-space:nowrap}.chat{padding:20px}.bubble{background:var(--panel2);border:1px solid var(--border);border-radius:16px;padding:15px;margin-bottom:16px;color:var(--muted);font-size:14px;line-height:1.45}.row{display:flex;gap:10px;margin-bottom:12px}select,input,textarea{width:100%;background:#0d1117;color:var(--text);border:1px solid var(--border);border-radius:12px;padding:12px 14px;font-size:15px;outline:none}textarea{min-height:150px;resize:vertical;line-height:1.45}select:focus,input:focus,textarea:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(88,166,255,.12)}.actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap}button{background:var(--blue);color:white;border:0;border-radius:12px;padding:12px 18px;font-size:15px;font-weight:700;cursor:pointer}button.secondary{background:#21262d;color:var(--text);border:1px solid var(--border)}button:hover{filter:brightness(1.08)}#status{font-size:13px;color:var(--muted)}.quick{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}.quick button{font-size:12px;padding:7px 10px;background:#21262d;border:1px solid var(--border);font-weight:500}.footer{padding:12px 20px;border-top:1px solid var(--border);font-size:12px;color:var(--muted);display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}@media(max-width:600px){body{padding:8px}.top{align-items:flex-start;flex-direction:column}.row{flex-direction:column}.chat{padding:14px}textarea{min-height:190px}}
</style>
</head>
<body>
<div class="app">
  <div class="top">
    <div class="brand"><h1>Command Portal</h1><p>Type plain English. No coding. OpenCode can process this inbox later.</p></div>
    <div class="pill">Local • Port 8787</div>
  </div>
  <div class="chat">
    <div class="bubble">Example: “Open Bible School and save this as a note for Rethinking the Church.”</div>
    <div class="row">
      <select id="project"></select>
      <input id="title" placeholder="Optional title, e.g. Bible quiz question">
    </div>
    <textarea id="message" placeholder="Type what you want me/OpenCode to do..."></textarea>
    <div class="actions">
      <button onclick="sendCommand()">Send to OpenCode Inbox</button>
      <button class="secondary" onclick="clearBox()">Clear</button>
      <span id="status">Ready</span>
    </div>
    <div class="quick">
      <button onclick="quick('Open Bible School and help me answer this quiz: ')" type="button">Bible School</button>
      <button onclick="quick('Open EchoKey and make this improvement: ')" type="button">EchoKey</button>
      <button onclick="quick('Add this to my project radar: ')" type="button">Project Radar</button>
      <button onclick="quick('Create a task for: ')" type="button">Task</button>
    </div>
  </div>
  <div class="footer"><span>Writes to PROJECTS\\Command Portal\\INBOX.md</span><span>Use VS Code Tunnel port forwarding to open from phone.</span></div>
</div>
<script>
const projects = __PROJECTS__;
const projectEl = document.getElementById('project');
projects.forEach(p => { const o=document.createElement('option'); o.value=p; o.textContent=p; projectEl.appendChild(o); });
function quick(text){ const m=document.getElementById('message'); m.value = text + m.value; m.focus(); }
function clearBox(){ document.getElementById('title').value=''; document.getElementById('message').value=''; document.getElementById('status').textContent='Cleared'; }
async function sendCommand(){
  const status=document.getElementById('status');
  const payload={project:projectEl.value,title:document.getElementById('title').value.trim(),message:document.getElementById('message').value.trim()};
  if(!payload.message){status.textContent='Type a message first.'; status.style.color='var(--yellow)'; return;}
  status.textContent='Sending...'; status.style.color='var(--muted)';
  try{
    const r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
    const j=await r.json();
    if(j.ok){status.textContent='Saved to inbox.'; status.style.color='var(--green)'; document.getElementById('message').value=''; document.getElementById('title').value='';}
    else{status.textContent='Error: '+j.error; status.style.color='var(--red)';}
  }catch(e){status.textContent='Connection error.'; status.style.color='var(--red)';}
}
document.getElementById('message').addEventListener('keydown', e=>{ if((e.ctrlKey||e.metaKey)&&e.key==='Enter') sendCommand(); });
</script>
</body>
</html>'''


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            html = HTML.replace("__PROJECTS__", json.dumps(PROJECTS))
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        elif self.path == "/api/status":
            self.send_json({"ok": True, "inbox": str(INBOX)})
        else:
            self.send_json({"ok": False, "error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/api/command":
            self.send_json({"ok": False, "error": "not found"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            project = data.get("project", "General Inbox")
            title = data.get("title", "").strip()
            message = data.get("message", "").strip()
            if not message:
                self.send_json({"ok": False, "error": "empty message"}, 400)
                return
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            heading = title or message.splitlines()[0][:70]
            entry = f"\n## {stamp} — {project}\n\n**Title:** {heading}\n\n{message}\n\n---\n"
            INBOX.parent.mkdir(parents=True, exist_ok=True)
            with INBOX.open("a", encoding="utf-8") as f:
                f.write(entry)
            self.send_json({"ok": True, "saved": True})
        except Exception as e:
            self.send_json({"ok": False, "error": str(e)}, 500)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def main():
    PROJECT_DIR.mkdir(parents=True, exist_ok=True)
    if not INBOX.exists():
        INBOX.write_text("# Command Portal Inbox\n\n---\n", encoding="utf-8")
    for port in range(PORT, PORT + 10):
        try:
            with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
                print(f"Command Portal running: http://127.0.0.1:{port}")
                httpd.serve_forever()
                return
        except OSError:
            continue
    raise RuntimeError("No available port found")


if __name__ == "__main__":
    main()
