#!/usr/bin/env python3
"""
EchoKey v1.3
Always-on-top floating local dictation app with dropdown settings,
hard-key hotkey capture, mic selection, recording buffer, smart cleanup,
and auto-paste.
"""

from __future__ import annotations

import json
import math
import queue
import threading
import time
import warnings
from pathlib import Path

import numpy as np
import pyperclip
import sounddevice as sd

warnings.filterwarnings("ignore", message=".*symlinks.*")

CONFIG_DIR = Path.home() / ".whisper-flow"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "hotkey": "ctrl+shift+space",
    "mode": "Clean dictation",
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
}

HOTKEY_PRESETS = [
    "ctrl+shift+space", "ctrl+alt+v", "ctrl+shift+v",
    "middlemouse", "mouse3", "f13", "f14", "f15", "f16", "scrolllock", "pause", "printscreen",
    "enter", "space"
]

MOD_NAMES = {"ctrl", "control", "shift", "alt", "win", "cmd", "super", "meta"}


def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            return {**DEFAULT_CONFIG, **json.loads(CONFIG_FILE.read_text(encoding="utf-8"))}
        except Exception:
            pass
    save_config(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")


def device_label(index: int, d: dict) -> str:
    name = str(d["name"]).replace("\r", " ").replace("\n", " ").strip()
    return f"[{index}] {name} ({int(d['default_samplerate'])}Hz)"


def parse_device_index(label: str | None):
    if not label or label.startswith("System Default"):
        return None
    if label.startswith("[") and "]" in label:
        try:
            return int(label[1:label.index("]")])
        except Exception:
            return None
    try:
        return int(label)
    except Exception:
        return None


def list_audio_devices():
    devices = sd.query_devices()
    inputs, outputs = [], []
    for i, d in enumerate(devices):
        if d["max_input_channels"] > 0:
            inputs.append((i, device_label(i, d)))
        if d["max_output_channels"] > 0:
            outputs.append((i, device_label(i, d)))
    return inputs, outputs


class AudioRecorder:
    def __init__(self, sample_rate=16000, input_device=None):
        self.sample_rate = sample_rate
        self.input_device = input_device
        self.q = queue.Queue()
        self.stream = None
        self.recording = False
        self.started_at = None

    def _callback(self, indata, frames, time_info, status):
        if self.recording:
            self.q.put(indata.copy())

    def start(self):
        self.q = queue.Queue()
        self.recording = True
        self.started_at = time.time()
        kwargs = {
            "samplerate": self.sample_rate,
            "channels": 1,
            "dtype": "float32",
            "callback": self._callback,
        }
        if self.input_device is not None:
            kwargs["device"] = self.input_device
        self.stream = sd.InputStream(**kwargs)
        self.stream.start()

    def stop(self):
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        chunks = []
        while not self.q.empty():
            chunks.append(self.q.get_nowait())
        if not chunks:
            return None
        return np.concatenate(chunks, axis=0).flatten()


class Transcriber:
    def __init__(self, model_name="small.en", device="cpu", compute_type="int8"):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.model = None

    def load(self):
        if self.model is not None:
            return
        from faster_whisper import WhisperModel
        self.model = WhisperModel(self.model_name, device=self.device, compute_type=self.compute_type)

    def transcribe(self, audio):
        self.load()
        segments, info = self.model.transcribe(audio, beam_size=1, language="en")
        return " ".join(s.text.strip() for s in segments if s.text.strip())


class TextCleaner:
    def __init__(self, api_url, model):
        self.api_url = api_url.rstrip("/")
        self.model = model
        self.available = self._check()

    def _check(self):
        try:
            import requests
            return requests.get(f"{self.api_url}/models", timeout=3).status_code == 200
        except Exception:
            return False

    def clean(self, text, mode="Clean dictation"):
        if not self.available or not text.strip():
            return text
        import requests

        mode = mode or "Clean dictation"
        prompts = {
            "Clean dictation": "Clean this speech transcript. Add punctuation/capitalization, fix obvious speech-to-text errors, remove filler words, preserve meaning. Return only the cleaned text.",
            "Quick note": "Turn this transcript into a concise quick note. Preserve useful details. Use short, clear phrasing. Return only the note.",
            "Professional": "Polish this transcript into professional, clear language. Preserve meaning and tone, remove filler words, improve flow. Return only the polished text.",
            "Rewrite": "Rewrite this transcript for clarity and readability while preserving the original intent. Return only the rewritten text.",
            "Prompt": "Convert this transcript into a clear prompt for an AI assistant. Include the user's goal, constraints, and desired output if implied. Return only the prompt.",
            "Text message": "Turn this transcript into a natural text message. Keep it brief, conversational, and clear. Return only the message.",
            "Email": "Turn this transcript into a clear email. Add a subject line if obvious, then a concise email body. Return only the email text.",
            "Command mode": "Convert this transcript into a concise instruction/command. Return only the final command text.",
            "Raw transcript paste": "Return the transcript unchanged.",
            "Clipboard only": "Clean this speech transcript. Add punctuation/capitalization and preserve meaning. Return only the cleaned text.",
        }
        instruction = prompts.get(mode, prompts["Clean dictation"])

        # Faster cleanup for short dictation: fewer tokens, lower timeout.
        max_tokens = min(700, max(80, int(len(text) * 1.4) + 60))
        try:
            r = requests.post(
                f"{self.api_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": instruction},
                        {"role": "user", "content": text},
                    ],
                    "temperature": 0.15,
                    "max_tokens": max_tokens,
                },
                timeout=18,
            )
            return r.json()["choices"][0]["message"]["content"].strip() or text
        except Exception:
            return text


def normalize_key(key) -> str | None:
    """Map pynput key/keycode to simple hotkey token."""
    from pynput.keyboard import Key, KeyCode
    special = {
        Key.space: "space", Key.enter: "enter", Key.tab: "tab", Key.esc: "esc",
        Key.backspace: "backspace", Key.delete: "delete", Key.insert: "insert",
        Key.home: "home", Key.end: "end", Key.page_up: "pageup", Key.page_down: "pagedown",
        Key.up: "up", Key.down: "down", Key.left: "left", Key.right: "right",
        Key.ctrl: "ctrl", Key.ctrl_l: "ctrl", Key.ctrl_r: "ctrl",
        Key.shift: "shift", Key.shift_l: "shift", Key.shift_r: "shift",
        Key.alt: "alt", Key.alt_l: "alt", Key.alt_r: "alt",
        Key.cmd: "win", Key.cmd_l: "win", Key.cmd_r: "win",
        Key.caps_lock: "capslock", Key.num_lock: "numlock",
        Key.scroll_lock: "scrolllock", Key.pause: "pause", Key.print_screen: "printscreen",
        Key.f1: "f1", Key.f2: "f2", Key.f3: "f3", Key.f4: "f4", Key.f5: "f5", Key.f6: "f6",
        Key.f7: "f7", Key.f8: "f8", Key.f9: "f9", Key.f10: "f10", Key.f11: "f11", Key.f12: "f12",
        Key.f13: "f13", Key.f14: "f14", Key.f15: "f15", Key.f16: "f16", Key.f17: "f17", Key.f18: "f18",
        Key.f19: "f19", Key.f20: "f20",
    }
    if key in special:
        return special[key]
    if isinstance(key, KeyCode):
        if key.char:
            return key.char.lower()
        if key.vk:
            return f"vk{key.vk}"
    return None


def normalize_mouse_button(button) -> str | None:
    """Map pynput mouse button to hotkey token."""
    try:
        from pynput.mouse import Button
        mapping = {
            Button.left: "leftmouse",
            Button.right: "rightmouse",
            Button.middle: "middlemouse",
        }
        return mapping.get(button, str(button).replace("Button.", "").lower())
    except Exception:
        return None


def parse_hotkey_tokens(hotkey: str) -> set[str]:
    return {p.strip().lower() for p in hotkey.split("+") if p.strip()}


def canonical_hotkey(tokens: set[str]) -> str:
    order = ["ctrl", "shift", "alt", "win"]
    mods = [m for m in order if m in tokens]
    keys = sorted([t for t in tokens if t not in order])
    return "+".join(mods + keys)


class GlobalHotkey:
    def __init__(self, hotkey, callback, ui_queue=None):
        self.hotkey = hotkey
        self.callback = callback
        self.ui_queue = ui_queue
        self.tokens = parse_hotkey_tokens(hotkey)
        self.pressed = set()
        self.listener = None
        self.mouse_listener = None
        self.last_fire = 0

    def start(self):
        from pynput.keyboard import Listener as KeyboardListener
        from pynput.mouse import Listener as MouseListener
        self.listener = KeyboardListener(on_press=self.on_press, on_release=self.on_release)
        self.listener.daemon = True
        self.listener.start()
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.mouse_listener.daemon = True
        self.mouse_listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

    def update(self, hotkey):
        self.hotkey = hotkey
        self.tokens = parse_hotkey_tokens(hotkey)
        self.pressed.clear()

    def maybe_fire(self):
        if self.tokens and self.tokens.issubset(self.pressed):
            now = time.time()
            if now - self.last_fire > 0.45:
                self.last_fire = now
                self.callback()

    def on_press(self, key):
        name = normalize_key(key)
        if not name:
            return
        self.pressed.add(name)
        self.maybe_fire()

    def on_release(self, key):
        name = normalize_key(key)
        if name:
            self.pressed.discard(name)

    def on_mouse_click(self, x, y, button, pressed):
        name = normalize_mouse_button(button)
        if not name:
            return
        # Treat mouse3 as alias for middlemouse
        aliases = {"mouse3": "middlemouse"}
        name = aliases.get(name, name)
        if pressed:
            self.pressed.add(name)
            self.maybe_fire()
        else:
            self.pressed.discard(name)


def paste_text(text):
    from pynput.keyboard import Controller, Key
    pyperclip.copy(text)
    time.sleep(0.08)
    kb = Controller()
    with kb.pressed(Key.ctrl):
        kb.press("v")
        kb.release("v")


class FloatingApp:
    def __init__(self):
        import tkinter as tk
        from tkinter import ttk

        self.tk = tk
        self.ttk = ttk
        self.root = tk.Tk()
        self.root.title("EchoKey")
        self.root.geometry("460x118+1120+110")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#0d1117")
        self.root.minsize(440, 118)

        self.config = load_config()
        self.uiq = queue.Queue()
        self.drag_start = None
        self.expanded = False
        self.capture_mode = False
        self.capture_tokens = set()
        self.recording = False
        self.processing = False
        self.recorder = None
        self.transcriber = None
        self.cleaner = None
        self.started_at = None
        self.meter_phase = 0
        self.inputs, self.outputs = list_audio_devices()

        self.hotkey = GlobalHotkey(self.config["hotkey"], self.toggle_recording, self.uiq)
        self.hotkey.start()

        self.build_ui()
        self.root.after(120, self.process_uiq)
        self.root.after(120, self.animate)
        self.root.protocol("WM_DELETE_WINDOW", self.shutdown)
        threading.Thread(target=self.preload_model, daemon=True).start()


    def preload_model(self):
        """Load Whisper model in background so first transcription is faster."""
        try:
            self.uiq.put(("status", "Loading model…", "#d29922"))
            self.transcriber = Transcriber(self.config["model"], self.config.get("device", "cpu"), self.config.get("compute_type", "int8"))
            self.transcriber.load()
            self.uiq.put(("status", "Ready", "#3fb950"))
        except Exception:
            self.uiq.put(("status", "Model load delayed", "#d29922"))

    def build_ui(self):
        tk, ttk = self.tk, self.ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground="#161b22", background="#161b22", foreground="#e6edf3")
        style.configure("TCheckbutton", background="#161b22", foreground="#e6edf3")

        self.shell = tk.Frame(self.root, bg="#0d1117", bd=1, relief="solid")
        self.shell.pack(fill="both", expand=True, padx=2, pady=2)

        top = tk.Frame(self.shell, bg="#161b22", height=50)
        top.pack(fill="x")
        top.bind("<ButtonPress-1>", self.start_drag)
        top.bind("<B1-Motion>", self.do_drag)

        self.status_dot = tk.Label(top, text="●", fg="#3fb950", bg="#161b22", font=("Segoe UI", 16))
        self.status_dot.pack(side="left", padx=(12, 4))
        self.title = tk.Label(top, text="EchoKey", fg="#e6edf3", bg="#161b22", font=("Segoe UI", 14, "bold"))
        self.title.pack(side="left")
        self.status = tk.Label(top, text="Ready", fg="#8b949e", bg="#161b22", font=("Segoe UI", 10))
        self.status.pack(side="left", padx=10)

        self.record_btn = tk.Button(top, text="🎙  Record", command=self.toggle_recording, bg="#238636", fg="white", relief="flat", padx=16, pady=4, font=("Segoe UI", 10, "bold"))
        self.record_btn.pack(side="right", padx=(4, 8), pady=10)
        self.menu_btn = tk.Button(top, text="⚙", command=self.toggle_settings, bg="#30363d", fg="#e6edf3", relief="flat", width=3)
        self.menu_btn.pack(side="right", padx=4, pady=10)
        self.close_btn = tk.Button(top, text="×", command=self.shutdown, bg="#30363d", fg="#e6edf3", relief="flat", width=3)
        self.close_btn.pack(side="right", padx=4, pady=10)

        self.canvas = tk.Canvas(self.shell, height=48, bg="#0d1117", highlightthickness=0)
        self.canvas.pack(fill="x")
        self.canvas.create_text(16, 24, anchor="w", fill="#8b949e", text=f"Click where you want text → press {self.config['hotkey']} → speak", tags="hint", font=("Segoe UI", 10))

        self.panel = tk.Frame(self.shell, bg="#161b22")
        # hidden by default

        self.mode_var = tk.StringVar(value=self.config.get("mode", "Clean dictation"))
        self.hotkey_var = tk.StringVar(value=self.config.get("hotkey", "ctrl+shift+space"))
        self.mic_var = tk.StringVar(value=self.label_for_device(self.config.get("input_device"), self.inputs))
        self.spk_var = tk.StringVar(value=self.label_for_device(self.config.get("output_device"), self.outputs))
        self.model_var = tk.StringVar(value=self.config.get("model", "small.en"))
        self.cleanup_var = tk.BooleanVar(value=bool(self.config.get("smart_cleanup", True)))
        self.paste_var = tk.BooleanVar(value=bool(self.config.get("auto_paste", True)))

        self.section("Dictation Mode", "Choose how EchoKey transforms what you say before pasting.")
        self.row("Output style", ttk.Combobox(self.panel, textvariable=self.mode_var, values=[
            "Clean dictation", "Quick note", "Professional", "Rewrite", "Prompt", "Text message", "Email", "Command mode", "Raw transcript paste", "Clipboard only"
        ], state="readonly"))

        self.section("Activation", "Use the scroll-wheel/middle mouse button, a function key, or a keyboard combo.")
        self.row("Hard key", ttk.Combobox(self.panel, textvariable=self.hotkey_var, values=HOTKEY_PRESETS))
        self.button_row([
            ("Capture key/button", self.begin_capture, True),
            ("Middle mouse", lambda: self.set_hotkey("middlemouse"), False),
            ("F13", lambda: self.set_hotkey("f13"), False),
            ("ScrollLock", lambda: self.set_hotkey("scrolllock"), False),
        ])

        self.section("Audio Devices", "Pick the exact microphone and output device EchoKey should use.")
        self.row("Microphone", ttk.Combobox(self.panel, textvariable=self.mic_var, values=["System Default"] + [x[1] for x in self.inputs], state="readonly"))
        self.row("Speaker", ttk.Combobox(self.panel, textvariable=self.spk_var, values=["System Default"] + [x[1] for x in self.outputs], state="readonly"))

        self.section("Performance", "Small is usually the best balance. Tiny/Base are faster; Medium is more accurate.")
        self.row("Whisper model", ttk.Combobox(self.panel, textvariable=self.model_var, values=["tiny.en", "base.en", "small.en", "medium"], state="readonly"))
        checks = tk.Frame(self.panel, bg="#161b22")
        checks.pack(fill="x", padx=18, pady=8)
        ttk.Checkbutton(checks, text="Smart cleanup", variable=self.cleanup_var).pack(side="left")
        ttk.Checkbutton(checks, text="Auto-paste", variable=self.paste_var).pack(side="left", padx=22)

        self.section("Actions")
        actions = tk.Frame(self.panel, bg="#161b22")
        actions.pack(fill="x", padx=18, pady=(4, 18))
        tk.Button(actions, text="Save Settings", command=self.save_settings, bg="#238636", fg="white", relief="flat", padx=18, pady=8, font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Button(actions, text="Test Microphone", command=self.test_mic, bg="#21262d", fg="#e6edf3", relief="flat", padx=18, pady=8, font=("Segoe UI", 10)).pack(side="left", padx=10)
        self.save_label = tk.Label(actions, text="", fg="#8b949e", bg="#161b22", font=("Segoe UI", 9))
        self.save_label.pack(side="left", padx=8)

        self.root.bind_all("<KeyPress>", self.capture_keypress)
        self.root.bind_all("<KeyRelease>", self.capture_keyrelease)
        self.root.bind_all("<ButtonPress>", self.capture_mousepress)


    def section(self, title, subtitle=None):
        tk = self.tk
        frame = tk.Frame(self.panel, bg="#161b22")
        frame.pack(fill="x", padx=18, pady=(18, 6))
        tk.Label(frame, text=title, fg="#58a6ff", bg="#161b22", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        if subtitle:
            tk.Label(frame, text=subtitle, fg="#8b949e", bg="#161b22", font=("Segoe UI", 9)).pack(anchor="w", pady=(2,0))
        return frame

    def button_row(self, items):
        tk = self.tk
        frame = tk.Frame(self.panel, bg="#161b22")
        frame.pack(fill="x", padx=18, pady=(4, 10))
        for label, command, primary in items:
            bg = "#238636" if primary else "#21262d"
            fg = "white" if primary else "#e6edf3"
            tk.Button(frame, text=label, command=command, bg=bg, fg=fg, relief="flat", padx=14, pady=7, font=("Segoe UI", 9, "bold" if primary else "normal")).pack(side="left", padx=(0,8))
        return frame

    def row(self, label, widget):
        tk = self.tk
        frame = tk.Frame(self.panel, bg="#161b22")
        frame.pack(fill="x", padx=18, pady=7)
        tk.Label(frame, text=label, fg="#8b949e", bg="#161b22", width=15, anchor="w", font=("Segoe UI", 10)).pack(side="left")
        widget.pack(side="left", fill="x", expand=True)
        return widget

    def label_for_device(self, value, entries):
        if value is None or value == "":
            return "System Default"
        try:
            idx = int(value)
        except Exception:
            return str(value)
        for i, label in entries:
            if i == idx:
                return label
        return "System Default"

    def start_drag(self, event):
        self.drag_start = (event.x_root, event.y_root, self.root.winfo_x(), self.root.winfo_y())

    def do_drag(self, event):
        if not self.drag_start:
            return
        sx, sy, wx, wy = self.drag_start
        self.root.geometry(f"+{wx + event.x_root - sx}+{wy + event.y_root - sy}")

    def toggle_settings(self):
        self.expanded = not self.expanded
        if self.expanded:
            self.panel.pack(fill="both")
            self.root.geometry("540x720")
            self.menu_btn.config(text="⌃")
        else:
            self.panel.forget()
            self.root.geometry("460x118")
            self.menu_btn.config(text="⚙")

    def set_hotkey(self, h):
        self.hotkey_var.set(h)
        self.save_settings()

    def begin_capture(self):
        self.capture_mode = True
        self.capture_tokens.clear()
        self.save_label.config(text="Press desired key/combo now…", fg="#d29922")

    def capture_keypress(self, event):
        if not self.capture_mode:
            return
        # Tkinter key names normalize
        key = event.keysym.lower()
        aliases = {"return": "enter", "prior": "pageup", "next": "pagedown", "control_l": "ctrl", "control_r": "ctrl", "shift_l": "shift", "shift_r": "shift", "alt_l": "alt", "alt_r": "alt"}
        key = aliases.get(key, key)
        self.capture_tokens.add(key)

    def capture_keyrelease(self, event):
        if not self.capture_mode:
            return
        if self.capture_tokens:
            hk = canonical_hotkey(self.capture_tokens)
            self.hotkey_var.set(hk)
            self.capture_mode = False
            self.save_settings()


    def capture_mousepress(self, event):
        if not self.capture_mode:
            return
        mapping = {1: "leftmouse", 2: "middlemouse", 3: "rightmouse"}
        token = mapping.get(getattr(event, "num", None))
        if token:
            self.hotkey_var.set(token)
            self.capture_mode = False
            self.save_settings()

    def save_settings(self):
        cfg = load_config()
        cfg.update({
            "hotkey": self.hotkey_var.get().strip().lower(),
            "mode": self.mode_var.get(),
            "model": self.model_var.get(),
            "smart_cleanup": bool(self.cleanup_var.get()),
            "auto_paste": bool(self.paste_var.get()),
            "input_device": parse_device_index(self.mic_var.get()),
            "output_device": parse_device_index(self.spk_var.get()),
        })
        # Clipboard-only mode overrides auto-paste but doesn't destroy checkbox state permanently
        if cfg["mode"] == "Clipboard only":
            cfg["auto_paste"] = False
        save_config(cfg)
        self.config = cfg
        self.hotkey.update(cfg["hotkey"])
        self.save_label.config(text="Saved", fg="#3fb950")
        self.canvas.itemconfigure("hint", text=f"Hotkey: {cfg['hotkey']}")

    def test_mic(self):
        self.save_settings()
        self.set_status("Testing mic…", "#d29922")
        def run():
            try:
                dev = self.config.get("input_device")
                audio = sd.rec(int(1.2 * 16000), samplerate=16000, channels=1, dtype="float32", device=dev)
                sd.wait()
                rms = float(np.sqrt(np.mean(audio ** 2)))
                level = min(100, int(rms * 500))
                self.uiq.put(("status", f"Mic level: {level}%", "#3fb950" if level > 5 else "#d29922"))
            except Exception as e:
                self.uiq.put(("status", "Mic test failed", "#f85149"))
        threading.Thread(target=run, daemon=True).start()

    def set_status(self, text, color="#8b949e"):
        self.status.config(text=text, fg=color)

    def selected_output_device(self):
        return self.config.get("output_device")

    def beep(self, high=True):
        try:
            freq = 880 if high else 440
            sr = 16000
            t = np.linspace(0, 0.12, int(sr * 0.12), False)
            tone = 0.15 * np.sin(freq * t * 2 * math.pi)
            sd.play(tone, samplerate=sr, device=self.selected_output_device())
            sd.wait()
        except Exception:
            try:
                import winsound
                winsound.Beep(880 if high else 440, 120)
            except Exception:
                pass

    def toggle_recording(self):
        if self.processing:
            self.uiq.put(("status", "Processing…", "#d29922"))
            return
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.recording = True
        self.started_at = time.time()
        self.status_dot.config(fg="#f85149")
        self.record_btn.config(text="■ Stop", bg="#f85149")
        self.set_status("Recording…", "#f85149")
        self.recorder = AudioRecorder(self.config.get("sample_rate", 16000), self.config.get("input_device"))
        try:
            self.recorder.start()
            threading.Thread(target=self.beep, args=(True,), daemon=True).start()
        except Exception as e:
            self.recording = False
            self.set_status(f"Mic error", "#f85149")
            self.save_label.config(text=str(e)[:38], fg="#f85149")

    def stop_recording(self):
        self.recording = False
        self.processing = True
        self.status_dot.config(fg="#d29922")
        self.record_btn.config(text="…", bg="#d29922")
        self.set_status("Processing…", "#d29922")
        audio = self.recorder.stop() if self.recorder else None
        threading.Thread(target=self.process_audio, args=(audio,), daemon=True).start()

    def process_audio(self, audio):
        try:
            if audio is None or len(audio) < 4000:
                self.uiq.put(("status", "Too short", "#d29922"))
                return
            self.beep(False)
            if self.transcriber is None or self.transcriber.model_name != self.config.get("model"):
                self.uiq.put(("status", "Loading model…", "#d29922"))
                self.transcriber = Transcriber(self.config["model"], self.config.get("device", "cpu"), self.config.get("compute_type", "int8"))
            self.uiq.put(("status", "Transcribing…", "#d29922"))
            raw = self.transcriber.transcribe(audio)
            if not raw.strip():
                self.uiq.put(("status", "No speech", "#d29922"))
                return
            mode = self.config.get("mode", "Clean dictation")
            final = raw
            if mode != "Raw transcript paste" and self.config.get("smart_cleanup", True):
                self.uiq.put(("status", "Cleaning…", "#d29922"))
                self.cleaner = TextCleaner(self.config["lm_studio_url"], self.config["lm_studio_model"])
                final = self.cleaner.clean(raw, mode)
            if self.config.get("auto_paste", True) and mode != "Clipboard only":
                paste_text(final)
                self.uiq.put(("status", "Pasted", "#3fb950"))
            else:
                pyperclip.copy(final)
                self.uiq.put(("status", "Copied", "#3fb950"))
            self.uiq.put(("buffer", final))
            self.beep(True)
        except Exception as e:
            self.uiq.put(("status", f"Error: {str(e)[:24]}", "#f85149"))
        finally:
            self.uiq.put(("done", None))

    def process_uiq(self):
        while not self.uiq.empty():
            item = self.uiq.get()
            if item[0] == "status":
                _, text, color = item
                self.set_status(text, color)
            elif item[0] == "buffer":
                self.canvas.itemconfigure("hint", text=item[1][:60])
            elif item[0] == "done":
                self.processing = False
                self.status_dot.config(fg="#3fb950")
                self.record_btn.config(text="🎙 Record", bg="#238636")
        self.root.after(120, self.process_uiq)

    def animate(self):
        self.canvas.delete("bars")
        w = max(self.canvas.winfo_width(), 200)
        if self.recording:
            elapsed = int(time.time() - self.started_at) if self.started_at else 0
            self.canvas.itemconfigure("hint", text=f"Recording buffer… {elapsed}s")
            for i in range(24):
                x = 120 + i * 10
                amp = 6 + 10 * abs(math.sin(self.meter_phase + i * 0.45))
                self.canvas.create_rectangle(x, 17 - amp, x + 5, 17 + amp, fill="#f85149", outline="", tags="bars")
            self.meter_phase += 0.25
        elif self.processing:
            self.canvas.itemconfigure("hint", text="Processing buffer…")
            for i in range(24):
                x = 130 + i * 9
                y = 17 + 7 * math.sin(self.meter_phase + i * 0.55)
                self.canvas.create_oval(x, y, x + 4, y + 4, fill="#d29922", outline="", tags="bars")
            self.meter_phase += 0.2
        self.root.after(80, self.animate)

    def shutdown(self):
        try:
            self.hotkey.stop()
        except Exception:
            pass
        try:
            if self.recording and self.recorder:
                self.recorder.stop()
        except Exception:
            pass
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    FloatingApp().run()
