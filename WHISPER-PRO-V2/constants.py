"""Whisper My Idea Pro v2 — Constants & Brand Colors"""
from pathlib import Path

# ─── Paths ──────────────────────────────────────────────────────────────────
APP_DIR = Path(__file__).parent
DATA_DIR = Path.home() / "AppData" / "Roaming" / "WhisperMyIdeaPro"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SETTINGS_FILE = DATA_DIR / "settings.json"
HISTORY_FILE = DATA_DIR / "history.json"
VOCAB_FILE = DATA_DIR / "vocabulary.json"
STATS_FILE = DATA_DIR / "stats.json"

# ─── Brand Colors (TBPS Dark) ──────────────────────────────────────────────
BG          = "#080b12"
BG2         = "#0d111a"
BG3         = "#131823"
SURFACE     = "#181e2c"
SURFACE2    = "#1f2638"
BORDER      = "#2a3147"
BORDER2     = "#3b4460"
ACCENT      = "#8b5cf6"
ACCENT2     = "#a78bfa"
ACCENT3     = "#7c3aed"
TEXT        = "#f0f2f5"
TEXT2       = "#94a3b8"
TEXT3       = "#64748b"
GREEN       = "#22c55e"
AMBER       = "#f59e0b"
RED         = "#ef4444"
GLOW_ACCENT = "rgba(139,92,246,0.12)"

# ─── Defaults ───────────────────────────────────────────────────────────────
DEFAULT_SETTINGS = {
    "hotkey": "mouse_middle",
    "start_hotkey": "mouse_middle",
    "stop_hotkey": "shift+z",
    "cancel_hotkey": "esc",
    "model": "tiny",
    "mode": "Dictation",
    "auto_paste": True,
    "save_history": True,
    "launch_at_startup": False,
    "language": "en",
    "overlay_width": 680,
    "overlay_opacity": 0.94,
    "overlay_position": "center",
    "overlay_x": None,
    "overlay_y": None,
    "theme": "Glass Dark",
    "noise_suppression": True,
    "voice_activity_detection": True,
    "push_to_talk": False,
    "continuous_listening": False,
    "speaker": "",
    "microphone": "",
}

# ─── Available Models ───────────────────────────────────────────────────────
AVAILABLE_MODELS = [
    {"id": "tiny",   "name": "Tiny",   "desc": "Fastest, ~1GB RAM",   "size": "75 MB"},
    {"id": "base",   "name": "Base",   "desc": "Balanced speed/accuracy", "size": "150 MB"},
    {"id": "small",  "name": "Small",  "desc": "Good accuracy",       "size": "500 MB"},
    {"id": "medium", "name": "Medium", "desc": "High accuracy",       "size": "1.5 GB"},
]

# ─── Available Modes ───────────────────────────────────────────────────────
AVAILABLE_MODES = [
    {"id": "Dictation", "icon": "", "label": "Dictation", "desc": "Clean dictation"},
    {"id": "Smart Prompt", "icon": "", "label": "Smart Prompt", "desc": "AI-polished from raw voice"},
    {"id": "AI Assistant", "icon": "", "label": "AI Assistant", "desc": "Assistant-style capture"},
    {"id": "Command Mode", "icon": "", "label": "Command Mode", "desc": "Voice commands"},
    {"id": "Message",  "icon": "", "label": "Message",  "desc": "Clean message format"},
    {"id": "Email",    "icon": "", "label": "Email",    "desc": "Formatted for email"},
    {"id": "Meeting",  "icon": "", "label": "Meeting",  "desc": "Meeting notes format"},
    {"id": "Bullets",  "icon": "", "label": "Bullets",  "desc": "Bullet point list"},
]

# ─── Common Hotkeys ───────────────────────────────────────────────────────
COMMON_HOTKEYS = [
    "mouse_middle", "alt+space", "ctrl+shift+space", "ctrl+space", "shift+z", "esc",
    "alt+q", "alt+`", "alt+x", "ctrl+alt+space", "ctrl+shift+r", "alt+shift+r", "win+shift+r", "ctrl+shift+q",
]