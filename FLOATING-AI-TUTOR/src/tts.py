#!/usr/bin/env python3
"""Text-to-speech using Windows built-in SAPI5."""
from __future__ import annotations

import sys
import threading
from typing import Optional


def speak(text: str, voice_name: str = "") -> bool:
    """Speak text using Windows SAPI5 TTS.
    
    Returns True if speech started, False if unavailable.
    """
    if sys.platform != "win32":
        return False

    def _speak():
        try:
            import comtypes.client
            sapi = comtypes.client.CreateObject("SAPI.SpVoice")
            if voice_name:
                voices = sapi.GetVoices()
                for i in range(voices.Count):
                    if voice_name.lower() in voices.Item(i).GetDescription().lower():
                        sapi.Voice = voices.Item(i)
                        break
            sapi.Speak(text)
        except Exception:
            pass

    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()
    return True


def get_available_voices() -> list[str]:
    """List available TTS voices."""
    voices = []
    if sys.platform == "win32":
        try:
            import comtypes.client
            sapi = comtypes.client.CreateObject("SAPI.SpVoice")
            for i in range(sapi.GetVoices().Count):
                voices.append(sapi.GetVoices().Item(i).GetDescription())
        except Exception:
            # Fallback: try pyttsx3
            try:
                import pyttsx3
                engine = pyttsx3.init()
                for voice in engine.getProperty('voices'):
                    voices.append(voice.name)
            except Exception:
                pass
    return voices


def speak_pyttsx3(text: str) -> bool:
    """Alternative TTS using pyttsx3."""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        return True
    except Exception:
        return False
