#!/usr/bin/env python3
"""EchoKeys Pro v3 — Superwhisper-inspired dictation app"""
import sys, os, threading, time, wave, tempfile, ctypes, json, re
from tkinter import Tk, Frame, Label, Button, Text, Entry, OptionMenu, StringVar, BooleanVar, Checkbutton, filedialog, messagebox, Toplevel
import pyperclip
import keyboard

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

# ─── CONFIG ──────────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "ek_config.json")

DEFAULT_CONFIG = {
    "mode": "Voice",
    "hotkey": "alt+space",
    "auto_paste": True,
    "context_aware": False,
    "vocabulary": {},
    "theme": "dark"
}

# ─── MODES (Superwhisper-inspired) ───────────────────────────
MODES = {
    "Voice": {
        "desc": "Raw transcription, minimal processing",
        "prompt": "Transcribe the audio exactly as spoken."
    },
    "Message": {
        "desc": "Polished, ready-to-send messages",
        "prompt": "Format as a clean, professional message. Fix grammar and flow."
    },
    "Email": {
        "desc": "Properly structured emails",
        "prompt": "Format as a professional email with greeting, body, and closing."
    },
    "Meeting": {
        "desc": "Meeting notes with action items",
        "prompt": "Format as meeting notes with key points, decisions, and action items."
    },
    "Note": {
        "desc": "Structured notes with hierarchy",
        "prompt": "Format as organized notes with clear structure."
    },
    "Bullets": {
        "desc": "Clean bullet-point summary",
        "prompt": "Convert to clean bullet points, grouped by topic."
    },
    "Super": {
        "desc": "Context-aware smart processing",
        "prompt": "Process intelligently based on context."
    }
}

recording = False
transcriber_model = None
config = {}
ek_window = None

def load_config():
    global config
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f: config = json.load(f)
        else:
            config = dict(DEFAULT_CONFIG)
    except:
        config = dict(DEFAULT_CONFIG)

def save_config():
    with open(CONFIG_FILE, 'w') as f: json.dump(config, f, indent=2)

def load_model():
    global transcriber_model
    try:
        from faster_whisper import WhisperModel
        transcriber_model = WhisperModel("tiny", device="auto", compute_type="int8")
    except: pass

# ─── VOCABULARY ──────────────────────────────────────────────
def apply_vocabulary(text):
    for word, replacement in config.get("vocabulary", {}).items():
        text = re.sub(re.escape(word), replacement, text, flags=re.IGNORECASE)
    return text

def transcribe_file(filepath, output_widget, status_label):
    global transcriber_model
    if not transcriber_model:
        status_label.config(text="Model not loaded", fg="#f59e0b")
        return
    status_label.config(text="Transcribing file...", fg="#8ab4f8")
    def do_transcribe():
        try:
            import whisper
            model = whisper.load_model("tiny")
            result = model.transcribe(filepath)
            text = result["text"].strip()
            output_widget.delete(1.0, "end")
            output_widget.insert(1.0, text if text else "No speech detected")
        except Exception as e:
            output_widget.delete(1.0, "end")
            output_widget.insert(1.0, f"File transcription error: {e}")
        finally:
            status_label.config(text="Ready", fg="#22c55e")
    threading.Thread(target=do_transcribe, daemon=True).start()

# ─── MAIN APP ────────────────────────────────────────────────
def build_app():
    global ek_window
    load_config()
    
    root = Tk()
    ek_window = root
    root.title("EchoKeys Pro")
    root.geometry(f"440x560+{root.winfo_screenwidth()-480}+{root.winfo_screenheight()-610}")
    root.configure(bg="#0c0c0e")
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    
    # ── Dragging ──
    def sm(e): root._drag = (e.x_root - root.winfo_x(), e.y_root - root.winfo_y())
    def mv(e):
        if hasattr(root,'_drag'): root.geometry(f"+{e.x_root - root._drag[0]}+{e.y_root - root._drag[1]}")
    
    def quit_app():
        try: keyboard.unhook_all()
        except: pass
        root.destroy()
    
    # ── Title bar ──
    tb = Frame(root, bg="#0c0c0e", height=44, cursor="fleur")
    tb.pack(fill="x")
    tb.bind("<Button-1>", sm)
    tb.bind("<B1-Motion>", mv)
    
    Label(tb, text="  EchoKeys Pro", font=("Segoe UI", 13, "bold"),
          fg="#f0f2f5", bg="#0c0c0e").pack(side="left")
    
    status_lbl = Label(tb, text="Ready", font=("Segoe UI", 10), fg="#22c55e", bg="#0c0c0e")
    status_lbl.pack(side="right", padx=6)
    
    # Settings button
    def open_settings():
        sw = Toplevel(root)
        sw.title("EchoKeys Settings")
        sw.geometry(f"360x320+{root.winfo_x()+40}+{root.winfo_y()+80}")
        sw.configure(bg="#151517")
        sw.attributes('-topmost', True)
        sw.overrideredirect(True)
        
        # Dragging for settings
        def ssm(e): sw._drag = (e.x_root - sw.winfo_x(), e.y_root - sw.winfo_y())
        def smv(e):
            if hasattr(sw,'_drag'): sw.geometry(f"+{e.x_root - sw._drag[0]}+{e.y_root - sw._drag[1]}")
        stb = Frame(sw, bg="#151517", height=36, cursor="fleur")
        stb.pack(fill="x")
        stb.bind("<Button-1>", ssm); stb.bind("<B1-Motion>", smv)
        Label(stb, text="  Settings", font=("Segoe UI", 12, "bold"),
              fg="#f0f2f5", bg="#151517").pack(side="left")
        Button(stb, text="✕", font=("Segoe UI", 10), bg="#151517", fg="#8a9bb5",
               relief="flat", bd=0, command=sw.destroy).pack(side="right", padx=8)
        
        sf = Frame(sw, bg="#151517", padx=20, pady=16)
        sf.pack(fill="both", expand=True)
        
        # Hotkey
        Label(sf, text="Hotkey:", fg="#8a9bb5", bg="#151517",
              font=("Segoe UI", 10)).pack(anchor="w")
        hk_var = StringVar(sf, value=config.get("hotkey", "alt+space"))
        hk_entry = Entry(sf, textvariable=hk_var, bg="#1a1a1e", fg="#f0f2f5",
                         font=("Segoe UI", 10), relief="flat", bd=0, highlightthickness=1,
                         highlightcolor="#2a2a2e")
        hk_entry.pack(fill="x", pady=(4, 12))
        
        # Auto-paste
        ap_var = BooleanVar(sf, value=config.get("auto_paste", True))
        Checkbutton(sf, text="Auto-paste after transcription", variable=ap_var,
                    bg="#151517", fg="#8a9bb5", activebackground="#151517",
                    activeforeground="#f0f2f5", font=("Segoe UI", 10),
                    selectcolor="#0c0c0e", relief="flat", bd=0).pack(anchor="w", pady=4)
        
        # Context awareness
        ca_var = BooleanVar(sf, value=config.get("context_aware", False))
        Checkbutton(sf, text="Context-aware processing (Super Mode)",
                    variable=ca_var, bg="#151517", fg="#8a9bb5",
                    activebackground="#151517", activeforeground="#f0f2f5",
                    font=("Segoe UI", 10), selectcolor="#0c0c0e",
                    relief="flat", bd=0).pack(anchor="w", pady=4)
        
        # Save button
        def save_settings():
            config["hotkey"] = hk_var.get()
            config["auto_paste"] = ap_var.get()
            config["context_aware"] = ca_var.get()
            save_config()
            status_lbl.config(text="Settings saved", fg="#22c55e")
            sw.destroy()
        
        Button(sf, text="Save", font=("Segoe UI", 11, "bold"),
               bg="#8ab4f8", fg="#0c0c0e", relief="flat", bd=0,
               padx=20, pady=8, cursor="hand2", command=save_settings).pack(pady=16)
    
    Button(tb, text="⚙", font=("Segoe UI", 11), bg="#0c0c0e", fg="#8a9bb5",
           relief="flat", bd=0, cursor="hand2", padx=8, command=open_settings).pack(side="right")
    
    Button(tb, text="✕", font=("Segoe UI", 11, "bold"), bg="#0c0c0e", fg="#8a9bb5",
           activebackground="#ef4444", activeforeground="#fff", relief="flat",
           bd=0, cursor="hand2", padx=12, command=quit_app).pack(side="right")
    
    # ── Recording indicator bar ──
    indicator = Frame(root, bg="#0c0c0e", height=3)
    indicator.pack(fill="x", padx=16)
    ind_bar = Frame(indicator, bg="#0c0c0e", height=3)
    ind_bar.pack(fill="x")
    
    # ── Mode selector ──
    mf = Frame(root, bg="#0c0c0e")
    mf.pack(fill="x", padx=16, pady=(8, 6))
    Label(mf, text="Mode:", fg="#8a9bb5", bg="#0c0c0e",
          font=("Segoe UI", 10)).pack(side="left")
    mode_var = StringVar(root, value=config.get("mode", "Voice"))
    
    def on_mode_change(*args):
        config["mode"] = mode_var.get()
        save_config()
        mode_desc = MODES[mode_var.get()]["desc"]
        status_lbl.config(text=f"Mode: {mode_desc}", fg="#8ab4f8")
    
    mode_var.trace_add("write", on_mode_change)
    mm = OptionMenu(mf, mode_var, *MODES.keys())
    mm.configure(bg="#1a1a1e", fg="#8ab4f8", bd=0, highlightthickness=0,
                 font=("Segoe UI", 10), activebackground="#1a1a1e", activeforeground="#8ab4f8")
    mm.pack(side="left", padx=8)
    
    # Mode description
    mode_desc_lbl = Label(mf, text=MODES[config.get("mode", "Voice")]["desc"],
                          fg="#6b7280", bg="#0c0c0e", font=("Segoe UI", 8))
    mode_desc_lbl.pack(side="left", padx=4)
    
    # ── Output area ──
    output = Text(root, bg="#151517", fg="#f0f2f5", insertbackground="#f0f2f5",
                  font=("Segoe UI", 13), padx=18, pady=18, relief="flat",
                  highlightthickness=1, highlightcolor="#2a2a2e",
                  height=11, wrap="word")
    output.pack(fill="both", expand=True, padx=16, pady=(0, 8))
    output.insert(1.0, f"Hold {config.get('hotkey','Alt+Space')} or click Record to start speaking...")
    
    # ── Record button ──
    bf = Frame(root, bg="#0c0c0e")
    bf.pack(fill="x", padx=16, pady=(0, 8))
    
    rec_var = StringVar(bf, value="Hold to Record")
    
    def on_press():
        global recording
        if recording: return
        recording = True
        status_lbl.config(text="Recording...", fg="#ef4444")
        ind_bar.configure(bg="#ef4444")
        rec_btn.configure(text="⏺ Recording...", bg="#ef4444", fg="white")
        output.delete(1.0, "end")
        output.insert(1.0, "Listening...")
        
        def capture():
            try:
                import pyaudio
                p = pyaudio.PyAudio()
                s = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                          input=True, frames_per_buffer=1024)
                frames = []
                while recording:
                    frames.append(s.read(1024, exception_on_overflow=False))
                s.stop_stream(); s.close(); p.terminate()
                path = os.path.join(tempfile.gettempdir(), "ek_capture.wav")
                wf = wave.open(path, 'wb')
                wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(16000)
                wf.writeframes(b''.join(frames)); wf.close()
                
                if os.path.getsize(path) > 1000 and transcriber_model:
                    segs, _ = transcriber_model.transcribe(path, beam_size=5)
                    raw = " ".join(s.text.strip() for s in segs)
                    text = apply_vocabulary(raw) if raw else "No speech detected"
                    output.delete(1.0, "end")
                    output.insert(1.0, text)
                    
                    if text.strip() and config.get("auto_paste", True):
                        root.after(200, lambda: paste_text(text, root, status_lbl))
                else:
                    output.delete(1.0, "end")
                    output.insert(1.0, "No speech detected")
            except Exception as e:
                output.delete(1.0, "end")
                output.insert(1.0, f"Error: {e}")
            finally:
                recording = False
                root.after(0, lambda: (status_lbl.config(text="Ready", fg="#22c55e"),
                                       ind_bar.configure(bg="#0c0c0e"),
                                       rec_btn.configure(text="Hold to Record", bg="#8ab4f8", fg="#0c0c0e")))
        
        threading.Thread(target=capture, daemon=True).start()
    
    def on_release():
        global recording
        if recording:
            recording = False
    
    rec_btn = Button(bf, text="Hold to Record", font=("Segoe UI", 12, "bold"),
                     bg="#8ab4f8", fg="#0c0c0e", relief="flat", cursor="hand2",
                     activebackground="#a8c8ff", bd=0, padx=20, pady=10)
    rec_btn.pack(fill="x")
    rec_btn.bind("<Button-1>", lambda e: on_press())
    rec_btn.bind("<ButtonRelease-1>", lambda e: on_release())
    
    # ── Action buttons ──
    af = Frame(root, bg="#0c0c0e")
    af.pack(fill="x", padx=16)
    
    def paste(t, root_widget, status):
        if t.strip():
            pyperclip.copy(t)
            root_widget.after(80, lambda: keyboard.send("ctrl+v"))
            root_widget.after(200, root_widget.iconify)
    
    def paste_current():
        t = output.get(1.0, "end-1c")
        if t.strip():
            pyperclip.copy(t)
            root.after(80, lambda: keyboard.send("ctrl+v"))
            root.after(200, root.iconify)
    
    def copy_current():
        t = output.get(1.0, "end-1c")
        if t.strip():
            pyperclip.copy(t)
            status_lbl.config(text="Copied!", fg="#8ab4f8")
    
    # File transcription button
    def transcribe_file_dialog():
        path = filedialog.askopenfilename(
            title="Select audio/video file",
            filetypes=[("Audio/Video", "*.mp3 *.wav *.mp4 *.m4a *.ogg"), ("All files", "*.*")])
        if path:
            transcribe_file(path, output, status_lbl)
    
    for text, cmd in [("📋 Paste", paste_current), ("📄 Copy", copy_current),
                      ("🗑 Clear", lambda: output.delete(1.0, "end")),
                      ("🎵 File", transcribe_file_dialog)]:
        Button(af, text=text, font=("Segoe UI", 10), bg="#151517", fg="#8a9bb5",
               relief="flat", cursor="hand2", activebackground="#1a1a1e",
               bd=0, padx=14, pady=6, command=cmd).pack(side="left", padx=2)
    
    # ── Footer ──
    ft = Frame(root, bg="#0c0c0e")
    ft.pack(fill="x", padx=16, pady=(8, 14))
    Label(ft, text=f"{config.get('hotkey','Alt+Space')}  ·  Modes: Voice/Message/Email/Meeting/Note/Super",
          font=("Segoe UI", 8), fg="#4a5568", bg="#0c0c0e").pack(side="left")
    Label(ft, text=f"PROMPT-MINE v3", font=("Segoe UI", 8),
          fg="#4a5568", bg="#0c0c0e").pack(side="right")
    
    # ── Hotkey ──
    try:
        keyboard.add_hotkey(config.get("hotkey", "alt+space"),
                           lambda: (on_press() if not recording else on_release()))
    except Exception:
        status_lbl.config(text="Hotkey unavailable", fg="#f59e0b")
    
    root.bind("<Escape>", lambda e: quit_app())
    
    # Load model in background
    threading.Thread(target=load_model, daemon=True).start()
    
    return root

if __name__ == "__main__":
    r = build_app()
    r.mainloop()