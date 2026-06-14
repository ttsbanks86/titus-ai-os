"""Stats Manager — Session and lifetime transcription statistics"""
import json
import time
from pathlib import Path
from constants import STATS_FILE

DEFAULT_STATS = {
    "session_words": 0,
    "total_words": 0,
    "sessions": 0,
    "weekly": {},
    "total_duration": 0.0
}

def load_stats():
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return dict(DEFAULT_STATS)

def save_stats(stats: dict):
    try:
        STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        print(f"[Stats] Save error: {e}")

def get_stats() -> dict:
    return load_stats()

def update_stats(text: str, duration: float = 0.0):
    stats = load_stats()
    words = len(text.split()) if text else 0
    stats["session_words"] = stats.get("session_words", 0) + words
    stats["total_words"] = stats.get("total_words", 0) + words
    stats["sessions"] = stats.get("sessions", 0) + 1
    stats["total_duration"] = stats.get("total_duration", 0.0) + duration
    # Weekly tracking
    week = time.strftime("%Y-W%U")
    stats.setdefault("weekly", {})
    stats["weekly"][week] = stats["weekly"].get(week, 0) + words
    save_stats(stats)
    return stats

def reset_session():
    stats = load_stats()
    stats["session_words"] = 0
    save_stats(stats)

def reset_all():
    save_stats(dict(DEFAULT_STATS))