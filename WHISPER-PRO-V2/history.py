"""History Manager — Transcription history with search, copy, delete"""
import json
import uuid
import time
from pathlib import Path
from constants import HISTORY_FILE

MAX_HISTORY = 500

def load_history():
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return []

def save_history(history: list):
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"[History] Save error: {e}")

def add_history(text: str, mode: str = "Voice", duration: float = 0.0) -> dict:
    history = load_history()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "text": text,
        "mode": mode,
        "duration": round(duration, 1),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "words": len(text.split()) if text else 0
    }
    history.append(entry)
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    save_history(history)
    return entry

def get_history(limit: int = 50) -> list:
    history = load_history()
    return history[-limit:][::-1]  # Most recent first

def delete_history_item(entry_id: str) -> bool:
    history = load_history()
    original_len = len(history)
    history = [h for h in history if h["id"] != entry_id]
    if len(history) < len(history):
        save_history(history)
        return True
    return False

def clear_history():
    save_history([])

def search_history(query: str, limit: int = 50) -> list:
    history = load_history()
    query = query.lower()
    results = [h for h in history if query in h["text"].lower()]
    return results[:limit][::-1]

def clear_history():
    import json
    from constants import HISTORY_FILE
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)