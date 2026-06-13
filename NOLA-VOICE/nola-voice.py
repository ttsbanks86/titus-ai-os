#!/usr/bin/env python3
"""NOLA Voice - working build from scratch"""
import sys, os, threading, time, wave, tempfile, ctypes
from tkinter import Tk, Frame, Label, Button, Text, Entry, OptionMenu, StringVar
import pyperclip
import keyboard

ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)

recording = False
model = None

def load_model():
    global model
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("tiny", device="auto", compute_type="int8")
    except:
        pass

def record(output, status):
    global recording
    if recording: return
    recording = True
    status.config(text="Recording...", fg="#ef4444")
    output.delete(1.0, "end")
    output.insert(1.0, "Listening...")
    
    def capture():
        try:
            import pyaudio
            p = pyaudio.PyAudio()
            s = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
            frames = []
            while recording:
                frames.append(s.read(1024, exception_on_overflow=False))
            s.stop_stream(); s.close(); p.terminate()
            path = os.path.join(tempfile.gettempdir(), "nola.wav")
            wf = wave.open(path, 'wb')
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(16000)
            wf.writeframes(b''.join(frames)); wf.close()
            if os.path.getsize(path) > 1000 and model:
                segs, _ = model.transcribe(path, beam_size=5)
                text = " ".join(s.text.strip() for s in segs)
                output.delete(1.0, "end")
                output.insert(1.0, text if text else "No speech detected")
        except Exception as e:
            output.delete(1.0, "end")
            output.insert(1.0, f"Error: {e}")
        finally:
            status.config(text="Ready", fg="#c084fc")
    
    threading.Thread(target=capture, daemon=True).start()

def stop_rec():
    global recording
    recording = False

def paste_text(output, root):
    t = output.get(1.0, "end-1c")
    if t.strip():
        pyperclip.copy(t)
        root.after(100, lambda: keyboard.send("ctrl+v"))
        root.after(200, root.iconify)

def build_app():
    root = Tk()
    root.title("NOLA Voice")
    root.geometry("420x520+{}+{}".format(root.winfo_screenwidth()-460, root.winfo_screenheight()-570))
    root.configure(bg="#0b0f1a")
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    
    # Dragging
    def sm(e): root._drag = (e.x_root - root.winfo_x(), e.y_root - root.winfo_y())
    def mv(e):
        if hasattr(root,'_drag'): root.geometry(f"+{e.x_root - root._drag[0]}+{e.y_root - root._drag[1]}")
    title = Frame(root, bg="#0b0f1a", height=40, cursor="fleur")
    title.pack(fill="x")
    title.bind("<Button-1>", sm)
    title.bind("<B1-Motion>", mv)
    
    Label(title, text="  NOLA Voice", font=("Segoe UI", 13, "bold"),
          fg="#f1f5f9", bg="#0b0f1a").pack(side="left")
    Label(title, text="Open Door AI Systems", font=("Segoe UI", 8),
          fg="#6b7280", bg="#0b0f1a").pack(side="left", padx=4)
    
    status = Label(title, text="Ready", font=("Segoe UI", 10),
                   fg="#c084fc", bg="#0b0f1a")
    status.pack(side="right", padx=10)
    
    # Mode
    mode_f = Frame(root, bg="#0b0f1a")
    mode_f.pack(fill="x", padx=16, pady=(0, 8))
    Label(mode_f, text="Mode:", fg="#94a3b8", bg="#0b0f1a",
          font=("Segoe UI", 10)).pack(side="left")
    mv = StringVar(root); mv.set("Voice")
    m = OptionMenu(mode_f, mv, "Voice", "Message", "Email", "Bullets")
    m.configure(bg="#15182a", fg="#c084fc", bd=0, highlightthickness=0,
                font=("Segoe UI", 10), activebackground="#15182a", activeforeground="#c084fc")
    m.pack(side="left", padx=8)
    
    # Output
    out = Text(root, bg="#131827", fg="#f1f5f9", insertbackground="#f1f5f9",
               font=("Segoe UI", 13), padx=16, pady=16, relief="flat",
               highlightthickness=1, height=12, wrap="word")
    out.pack(fill="both", expand=True, padx=16, pady=(0, 8))
    out.insert(1.0, "Press Ctrl+Shift+N or click Record to speak...")
    
    # Record
    bf = Frame(root, bg="#0b0f1a")
    bf.pack(fill="x", padx=16, pady=(0, 8))
    rec = Button(bf, text="Hold to Record", font=("Segoe UI", 12, "bold"),
                 bg="#c084fc", fg="#0b0f1a", relief="flat", cursor="hand2",
                 activebackground="#d8b4fe", bd=0, padx=20, pady=10)
    rec.pack(fill="x")
    rec.bind("<Button-1>", lambda e: record(out, status))
    rec.bind("<ButtonRelease-1>", lambda e: stop_rec())
    
    # Actions
    af = Frame(root, bg="#0b0f1a")
    af.pack(fill="x", padx=16)
    for t, c in [("Paste", lambda: paste_text(out, root)),
                 ("Copy", lambda: (pyperclip.copy(out.get(1.0,"end-1c")), status.config(text="Copied!"))),
                 ("Clear", lambda: out.delete(1.0, "end"))]:
        Button(af, text=t, font=("Segoe UI", 10), bg="#131827", fg="#94a3b8",
               relief="flat", cursor="hand2", activebackground="#1a1e30",
               bd=0, padx=16, pady=6, command=c).pack(side="left", padx=2)
    
    # Footer
    ft = Frame(root, bg="#0b0f1a")
    ft.pack(fill="x", padx=16, pady=(8, 12))
    Label(ft, text="Ctrl+Shift+N to record", font=("Segoe UI", 8),
          fg="#6b7280", bg="#0b0f1a").pack(side="left")
    Label(ft, text="Open Door AI Systems", font=("Segoe UI", 8),
          fg="#6b7280", bg="#0b0f1a").pack(side="right")
    
    keyboard.add_hotkey("ctrl+shift+n", lambda: record(out, status), suppress=True)
    threading.Thread(target=load_model, daemon=True).start()
    
    return root

if __name__ == "__main__":
    r = build_app()
    r.mainloop()