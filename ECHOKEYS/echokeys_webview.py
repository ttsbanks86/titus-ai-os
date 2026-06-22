#!/usr/bin/env python3
"""EchoKeys Pro — WebView2 powered desktop dictation app"""
import webview, threading, json, os, sys, time, wave, tempfile, ctypes

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: #0c0c0e;
    color: #f0f2f5;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    user-select: none;
}
/* Title bar */
.title-bar {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    background: #0c0c0e;
    -webkit-app-region: drag;
    min-height: 44px;
}
.title-bar > * { -webkit-app-region: no-drag; }
.title-bar h1 { font-size: 14px; font-weight: 700; letter-spacing: -0.2px; }
.status { margin-left: auto; font-size: 11px; color: #22c55e; margin-right: 12px; }
.close-btn {
    width: 28px; height: 28px; border-radius: 8px;
    background: transparent; color: #6b7280; border: none;
    font-size: 16px; cursor: pointer; display: flex;
    align-items: center; justify-content: center;
}
.close-btn:hover { background: #ef4444; color: white; }
/* Recording bar */
.rec-bar { height: 3px; margin: 0 16px; border-radius: 2px; transition: all 0.2s; }
/* Content */
.content { flex: 1; padding: 12px 16px; display: flex; flex-direction: column; gap: 10px; }
.mode-row { display: flex; align-items: center; gap: 8px; }
.mode-row label { font-size: 12px; color: #8a9bb5; }
.mode-select {
    background: #1a1a1e; color: #8ab4f8; border: 1px solid #2a2a2e;
    border-radius: 8px; padding: 6px 12px; font-size: 12px; font-family: 'Inter', sans-serif;
    outline: none; cursor: pointer;
}
.mode-desc { font-size: 11px; color: #6b7280; }
textarea {
    flex: 1; background: #151517; color: #f0f2f5; border: 1px solid #2a2a2e;
    border-radius: 12px; padding: 16px; font-size: 14px; font-family: 'Inter', sans-serif;
    resize: none; outline: none; line-height: 1.6;
}
textarea:focus { border-color: #8ab4f8; }
.btn-row { display: flex; gap: 6px; }
.btn {
    background: #151517; color: #8a9bb5; border: 1px solid #2a2a2e;
    border-radius: 8px; padding: 8px 16px; font-size: 12px; font-family: 'Inter', sans-serif;
    cursor: pointer; transition: all 0.15s;
}
.btn:hover { background: #1f1f23; border-color: #3a3a3e; color: #f0f2f5; }
.btn-primary {
    background: linear-gradient(135deg, #8ab4f8, #6a94d8); color: #0c0c0e;
    border: none; font-weight: 600; font-size: 13px; padding: 10px 20px;
}
.btn-primary:hover { opacity: 0.9; }
.btn-primary.recording { background: #ef4444; color: white; }
.footer {
    display: flex; justify-content: space-between; padding: 8px 16px 14px;
    font-size: 10px; color: #4a5568;
}
</style>
</head>
<body>
<div class="title-bar">
    <h1>EchoKeys Pro</h1>
    <span class="status" id="status">Ready</span>
    <button class="close-btn" onclick="window.close()">✕</button>
</div>
<div class="rec-bar" id="recBar"></div>
<div class="content">
    <div class="mode-row">
        <label>Mode:</label>
        <select class="mode-select" id="modeSelect" onchange="onModeChange()">
            <option value="Voice">🎤 Voice</option>
            <option value="Message">💬 Message</option>
            <option value="Email">✉️ Email</option>
            <option value="Meeting">📋 Meeting</option>
            <option value="Note">📝 Note</option>
            <option value="Bullets">📋 Bullets</option>
            <option value="Super">✨ Super</option>
        </select>
        <span class="mode-desc" id="modeDesc">Raw transcription</span>
    </div>
    <textarea id="output" placeholder="Hold Alt+Space or click record to start speaking..."></textarea>
    <button class="btn btn-primary" id="recBtn" onmousedown="startRec()" onmouseup="stopRec()">🎤  Hold to Record</button>
    <div class="btn-row">
        <button class="btn" onclick="pasteText()">📋 Paste</button>
        <button class="btn" onclick="copyText()">📄 Copy</button>
        <button class="btn" onclick="clearText()">🗑 Clear</button>
        <button class="btn" onclick="openFile()">🎵 File</button>
    </div>
</div>
<div class="footer">
    <span>Alt+Space · Thumb button</span>
    <span>PROMPT-MINE v3</span>
</div>
<script>
let recording = false;
function onModeChange() {
    const descs = {
        Voice: 'Raw transcription', Message: 'Polished messages', Email: 'Formatted emails',
        Meeting: 'Meeting notes + actions', Note: 'Structured notes',
        Bullets: 'Bullet points', Super: 'Context-aware'
    };
    document.getElementById('modeDesc').textContent = descs[document.getElementById('modeSelect').value] || '';
}
function startRec() {
    if (recording) return;
    recording = true;
    document.getElementById('recBtn').textContent = '⏺ Recording...';
    document.getElementById('recBtn').className = 'btn btn-primary recording';
    document.getElementById('recBar').style.background = '#ef4444';
    document.getElementById('status').textContent = 'Recording';
    document.getElementById('status').style.color = '#ef4444';
    pywebview.api.start_recording();
}
function stopRec() {
    if (!recording) return;
    recording = false;
    document.getElementById('recBtn').textContent = '🎤  Hold to Record';
    document.getElementById('recBtn').className = 'btn btn-primary';
    document.getElementById('recBar').style.background = 'transparent';
    document.getElementById('status').textContent = 'Transcribing';
    document.getElementById('status').style.color = '#f59e0b';
    pywebview.api.stop_recording();
}
function updateOutput(text) {
    document.getElementById('output').value = text;
    document.getElementById('status').textContent = 'Ready';
    document.getElementById('status').style.color = '#22c55e';
}
function pasteText() {
    const t = document.getElementById('output').value;
    if (t) pywebview.api.paste_text(t);
}
function copyText() {
    const t = document.getElementById('output').value;
    if (t) { navigator.clipboard.writeText(t);
        document.getElementById('status').textContent = 'Copied!';
        document.getElementById('status').style.color = '#8ab4f8'; }
}
function clearText() { document.getElementById('output').value = ''; }
function openFile() { pywebview.api.open_file(); }
</script>
</body>
</html>"""

class Api:
    def __init__(self):
        self.model = None
        self.recording = False
        self.window = None
        threading.Thread(target=self._load_model, daemon=True).start()
    
    def _load_model(self):
        try:
            from faster_whisper import WhisperModel
            self.model = WhisperModel("tiny", device="auto", compute_type="int8")
        except:
            pass
    
    def start_recording(self):
        self.recording = True
        threading.Thread(target=self._capture, daemon=True).start()
    
    def stop_recording(self):
        self.recording = False
    
    def _capture(self):
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            s = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                      input=True, frames_per_buffer=1024)
            frames = []
            while self.recording:
                frames.append(s.read(1024, exception_on_overflow=False))
            s.stop_stream(); s.close(); p.terminate()
            path = os.path.join(tempfile.gettempdir(), "ek_capture.wav")
            wf = wave.open(path, 'wb')
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(16000)
            wf.writeframes(b''.join(frames)); wf.close()
            if os.path.getsize(path) > 1000 and self.model:
                segs, _ = self.model.transcribe(path, beam_size=5)
                text = " ".join(s.text.strip() for s in segs) or "No speech detected"
                self.window.evaluate_js(f'updateOutput({json.dumps(text)})')
            else:
                self.window.evaluate_js('updateOutput("No speech detected")')
        except Exception as e:
            self.window.evaluate_js(f'updateOutput("Error: {e}")')
    
    def paste_text(self, text):
        import pyperclip
        pyperclip.copy(text)
        import keyboard
        time.sleep(0.1)
        keyboard.send("ctrl+v")
    
    def open_file(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(title="Select audio file",
            filetypes=[("Audio/Video", "*.mp3 *.wav *.mp4 *.m4a *.ogg"), ("All files", "*.*")])
        if path:
            self.window.evaluate_js(f'document.getElementById("output").value = "Transcribing file..."')
            threading.Thread(target=self._transcribe_file, args=(path,), daemon=True).start()
    
    def _transcribe_file(self, path):
        try:
            import whisper
            model = whisper.load_model("tiny")
            result = model.transcribe(path)
            text = result["text"].strip() or "No speech detected"
            self.window.evaluate_js(f'updateOutput({json.dumps(text)})')
        except Exception as e:
            self.window.evaluate_js(f'updateOutput("File error: {e}")')

if __name__ == "__main__":
    api = Api()
    window = webview.create_window(
        "EchoKeys Pro",
        html=HTML,
        js_api=api,
        width=440,
        height=580,
        frameless=True,
        easy_drag=False,
        transparent=True,
        on_top=True
    )
    api.window = window
    webview.start()