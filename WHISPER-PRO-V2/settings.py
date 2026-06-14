"""Settings Manager — JSON persistence with defaults"""
import json
from pathlib import Path
from constants import SETTINGS_FILE, DEFAULT_SETTINGS

class Settings:
    def __init__(self):
        self._data = dict(DEFAULT_SETTINGS)
        self._load()

    def _load(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data.update(loaded)
        except Exception as e:
            print(f"[Settings] Load error: {e}")

    def save(self):
        try:
            SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2)
        except Exception as e:
            print(f"[Settings] Save error: {e}")

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def update(self, mapping: dict):
        self._data.update(mapping)
        self.save()

    @property
    def all(self) -> dict:
        return dict(self._data)