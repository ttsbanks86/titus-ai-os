"""HotkeyManager — Configurable global hotkeys using keyboard library"""
import keyboard
from constants import COMMON_HOTKEYS

class HotkeyManager:
    def __init__(self, settings):
        self.settings = settings
        self._current_hotkey = settings.get("hotkey", "alt+space")
        self._callback = None

    def set_callback(self, callback):
        """Set the function to call when hotkey is triggered."""
        self._callback = callback

    def register(self, hotkey: str = None):
        """Register the global hotkey."""
        if hotkey:
            self._current_hotkey = hotkey
        else:
            hotkey = self._current_hotkey

        try:
            keyboard.remove_hotkey(hotkey)
        except:
            pass

        try:
            keyboard.add_hotkey(hotkey, self._on_hotkey, suppress=True)
            print(f"[HotkeyManager] Registered: {hotkey}")
        except Exception as e:
            print(f"[HotkeyManager] Failed to register {hotkey}: {e}")

    def _on_hotkey(self):
        if self._callback:
            self._callback()

    def update_hotkey(self, new_hotkey: str):
        """Change the hotkey."""
        self._current_hotkey = new_hotkey
        self.settings.set("hotkey", hotkey)
        self.register(hotkey)