from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path


# Playback modes:
#   "hidden"  - in-process playback through sounddevice (no visible window, file deleted)
#   "pygame"  - in-process playback through pygame.mixer (fallback if sounddevice has issues)
#   "startfile" - legacy behavior: os.startfile launches default media player (may show window)
DEFAULT_PLAYBACK_MODE = "hidden"


class Speaker:
    def __init__(
        self,
        enabled: bool = True,
        echo: bool = True,
        engine: str = "edge-tts",
        voice: str = "en-GB-RyanNeural",
        rate: str = "+10%",
        volume: float = 1.0,
        pitch: str = "-20Hz",
        playback_mode: str = DEFAULT_PLAYBACK_MODE,
        elevenlabs_api_key: str = "",
        elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM",
        elevenlabs_model: str = "eleven_multilingual_v2",
        elevenlabs_stability: float = 0.5,
        elevenlabs_similarity_boost: float = 0.75,
    ) -> None:
        self.enabled = enabled
        self.echo = echo
        self.engine = engine
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch
        self.playback_mode = (playback_mode or DEFAULT_PLAYBACK_MODE).strip().lower()
        if self.playback_mode not in {"hidden", "pygame", "startfile"}:
            self.playback_mode = DEFAULT_PLAYBACK_MODE
        self._engine = None
        self._pygame_initialized = False
        # ElevenLabs settings
        self.elevenlabs_api_key = elevenlabs_api_key
        self.elevenlabs_voice_id = elevenlabs_voice_id
        self.elevenlabs_model = elevenlabs_model
        self.elevenlabs_stability = elevenlabs_stability
        self.elevenlabs_similarity_boost = elevenlabs_similarity_boost

    def speak(self, text: str) -> None:
        if not text:
            return
        if self.echo:
            print(_console_safe(text))
        if not self.enabled:
            return
        try:
            if self.engine == "edge-tts":
                self._speak_with_edge_tts(text)
            elif self.engine == "elevenlabs":
                self._speak_with_elevenlabs(text)
            else:
                self._speak_with_pyttsx3(text)
        except Exception:
            self._speak_with_pyttsx3(text)

    def stop(self) -> None:
        if self._engine is not None:
            self._engine.stop()
        # Stop pygame playback if it is running
        try:
            if self._pygame_initialized:
                import pygame

                pygame.mixer.music.stop()
        except Exception:
            pass

    def _speak_with_pyttsx3(self, text: str) -> None:
        try:
            import pyttsx3
        except ImportError:
            return
        if self._engine is None:
            self._engine = pyttsx3.init()
            self._engine.setProperty("volume", self.volume)
            if self.rate.isdigit():
                self._engine.setProperty("rate", int(self.rate))
            for candidate in self._engine.getProperty("voices"):
                if self.voice.lower() in (candidate.name or "").lower() or self.voice.lower() in (candidate.id or "").lower():
                    self._engine.setProperty("voice", candidate.id)
                    break
        self._engine.say(text)
        self._engine.runAndWait()

    def _speak_with_edge_tts(self, text: str) -> None:
        # Use NamedTemporaryFile in a directory we control so deletion is reliable
        # on Windows. The delete=False + finally cleanup pattern prevents the
        # "audio file pops up on screen" bug and the "replay on next push-to-talk"
        # bug, because the file is always removed after playback completes.
        output = None
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False, dir=tempfile.gettempdir()
            ) as handle:
                output = Path(handle.name)
            subprocess.run(
                [
                    "edge-tts",
                    "--voice",
                    self.voice,
                    "--rate",
                    self.rate,
                    f"--pitch={self.pitch}",
                    "--text",
                    text,
                    "--write-media",
                    str(output),
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )
            self._play_file(str(output))
        finally:
            # Always clean up the temp file so the next push-to-talk doesn't replay it.
            if output is not None:
                try:
                    if output.exists():
                        output.unlink()
                except OSError:
                    pass

    def _speak_with_elevenlabs(self, text: str) -> None:
        """Generate speech using ElevenLabs API for high-quality, natural-sounding voice."""
        if not self.elevenlabs_api_key:
            # Fall back to edge-tts if no API key is configured
            self._speak_with_edge_tts(text)
            return

        import requests

        output = None
        try:
            # Call ElevenLabs text-to-speech API
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}"
            headers = {
                "xi-api-key": self.elevenlabs_api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            }
            payload = {
                "text": text,
                "model_id": self.elevenlabs_model,
                "voice_settings": {
                    "stability": self.elevenlabs_stability,
                    "similarity_boost": self.elevenlabs_similarity_boost,
                },
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            # Save the audio to a temp file
            with tempfile.NamedTemporaryFile(
                suffix=".mp3", delete=False, dir=tempfile.gettempdir()
            ) as handle:
                output = Path(handle.name)
                handle.write(response.content)

            self._play_file(str(output))
        except Exception as e:
            # If ElevenLabs fails, fall back to edge-tts
            print(f"ElevenLabs TTS failed: {e}, falling back to edge-tts")
            self._speak_with_edge_tts(text)
        finally:
            # Always clean up the temp file
            if output is not None:
                try:
                    if output.exists():
                        output.unlink()
                except OSError:
                    pass

    def _play_file(self, path: str) -> None:
        mode = self.playback_mode
        if mode == "startfile":
            self._play_with_startfile(path)
            return
        if mode == "pygame":
            if self._play_with_pygame(path):
                return
            # fall through to hidden
        if self._play_with_sounddevice(path):
            return
        # Last-resort fallbacks in order of safety
        if self._play_with_pygame(path):
            return
        self._play_with_startfile(path)

    def _play_with_sounddevice(self, path: str) -> bool:
        try:
            import soundfile as sf
            import sounddevice as sd
            import numpy as np
        except ImportError:
            return False
        try:
            data, sample_rate = sf.read(path, dtype="float32")
            if data.ndim > 1:
                data = data[:, 0]
            # Apply volume scaling
            data = data * float(self.volume)
            sd.play(data, sample_rate)
            sd.wait()
            return True
        except Exception:
            return False

    def _play_with_pygame(self, path: str) -> bool:
        try:
            import pygame
        except ImportError:
            return False
        try:
            if not self._pygame_initialized:
                pygame.mixer.init()
                self._pygame_initialized = True
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(float(self.volume))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(30)
            return True
        except Exception:
            self._pygame_initialized = False
            return False

    def _play_with_startfile(self, path: str) -> None:
        try:
            os.startfile(str(path))  # type: ignore[attr-defined]
        except Exception:
            pass


def _console_safe(text: str) -> str:
    return text.encode("ascii", errors="replace").decode("ascii")
