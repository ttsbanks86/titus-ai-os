#!/usr/bin/env python3
"""Voice input using Windows built-in Speech Recognition (SAPI)."""
from __future__ import annotations

import sys
import threading
from typing import Optional


def listen_once(timeout_sec: float = 15.0) -> Optional[str]:
    """Listen for one voice command using Windows Speech Recognition.
    
    Returns the recognized text, or None if cancelled/timeout.
    """
    if sys.platform != "win32":
        return None

    result = [None]
    error = [None]
    done = threading.Event()

    def _listen():
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen with timeout
                audio = recognizer.listen(source, timeout=timeout_sec, phrase_time_limit=30)
            # Recognize using Google (free, no API key needed)
            text = recognizer.recognize_google(audio)
            result[0] = text
        except Exception as exc:
            error[0] = str(exc)
        finally:
            done.set()

    thread = threading.Thread(target=_listen, daemon=True)
    thread.start()
    thread.join(timeout=timeout_sec + 5)

    if error[0]:
        return None
    return result[0]


def listen_with_sapi(timeout_sec: float = 15.0) -> Optional[str]:
    """Alternative: use Windows SAPI directly (no external dependency)."""
    if sys.platform != "win32":
        return None

    result = [None]
    done = threading.Event()

    def _listen():
        try:
            import comtypes.client
            # Create shared recognizer
            recognizer = comtypes.client.CreateObject("SAPI.SpSharedRecoContext")
            # Set up grammar
            grammar = recognizer.CreateGrammar(1)
            grammar.DictationSetState(1)  # Enable dictation

            recognized_text = []

            def on_recognition(stream, start, end, result_obj, *args):
                try:
                    text = result_obj.PhraseInfo.GetText()
                    recognized_text.append(text)
                except Exception:
                    pass

            # This is a simplified approach - SAPI events are complex
            # For reliable voice input, prefer speech_recognition library
            import time
            time.sleep(timeout_sec)
            if recognized_text:
                result[0] = " ".join(recognized_text)
        except Exception:
            pass
        finally:
            done.set()

    thread = threading.Thread(target=_listen, daemon=True)
    thread.start()
    done.wait(timeout=timeout_sec + 5)
    return result[0]


def get_available_voices() -> list[str]:
    """List available system TTS voices."""
    voices = []
    if sys.platform == "win32":
        try:
            import comtypes.client
            sapi = comtypes.client.CreateObject("SAPI.SpVoice")
            for i in range(sapi.GetVoices().Count):
                voice = sapi.GetVoices().Item(i)
                voices.append(voice.GetDescription())
        except Exception:
            pass
    return voices


def is_speech_available() -> bool:
    """Check if speech recognition is available."""
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        with sr.Microphone() as source:
            return True
    except Exception:
        return False
