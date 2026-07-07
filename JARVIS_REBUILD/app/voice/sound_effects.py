"""Sound effect player for Jarvis.

Plays sound effects in a background thread so they don't block processing.
Used for the 'thinking' sound that plays while Jarvis is generating a response,
and can be extended later for funny sound effects, confirmation sounds, etc.

The sound is played using the same sounddevice/soundfile stack already used
for TTS playback, so no new dependencies are needed. Falls back to pygame
if sounddevice has issues, then to the OS default player.
"""
from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Optional


def play_sound_effect(path: str, blocking: bool = False, volume: float = 0.5) -> bool:
    """Play a sound effect from a file path.

    Args:
        path: Path to the audio file (mp3, wav, ogg, etc.)
        blocking: If True, wait for the sound to finish before returning.
                  If False (default), play in a background thread.
        volume: 0.0 to 1.0 volume scaling

    Returns:
        True if playback started successfully, False otherwise.
    """
    if not path or not os.path.exists(path):
        return False

    if blocking:
        return _play_audio_file(path, volume)
    # Non-blocking: play in a daemon thread so it doesn't prevent shutdown
    thread = threading.Thread(
        target=_play_audio_file,
        args=(path, volume),
        daemon=True,
    )
    thread.start()
    return True


def _play_audio_file(path: str, volume: float) -> bool:
    """Play an audio file using sounddevice/soundfile, falling back to pygame."""
    # Try sounddevice + soundfile first (already installed)
    try:
        import soundfile as sf
        import sounddevice as sd
        import numpy as np

        data, sample_rate = sf.read(path, dtype="float32")
        if data.ndim > 1:
            data = data[:, 0]  # mono
        data = data * float(volume)
        sd.play(data, sample_rate)
        sd.wait()
        return True
    except Exception:
        pass

    # Fallback: pygame
    try:
        import pygame

        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(float(volume))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(30)
        return True
    except Exception:
        pass

    # Last resort: os.startfile (Windows only, may show a player window)
    try:
        os.startfile(path)  # type: ignore[attr-defined]
        return True
    except Exception:
        return False


class SoundEffectPlayer:
    """Manages sound effects for Jarvis. Plays the thinking sound when
    Jarvis starts processing, and can be extended for other sound effects.

    Usage:
        player = SoundEffectPlayer(config)
        player.play_thinking_sound()  # plays in background while Jarvis thinks
        # ... Jarvis processes and responds ...
        # The sound stops automatically when it finishes, or can be stopped early
    """

    def __init__(self, sound_path: str = "", enabled: bool = False, volume: float = 0.5) -> None:
        self.sound_path = sound_path
        self.enabled = enabled
        self.volume = volume
        self._current_thread: Optional[threading.Thread] = None

    def play_thinking_sound(self) -> bool:
        """Play the thinking sound in the background. Returns True if started."""
        if not self.enabled or not self.sound_path:
            return False
        if not os.path.exists(self.sound_path):
            return False
        # Stop any currently playing sound
        self.stop()
        self._current_thread = threading.Thread(
            target=_play_audio_file,
            args=(self.sound_path, self.volume),
            daemon=True,
        )
        self._current_thread.start()
        return True

    def stop(self) -> None:
        """Stop any currently playing sound effect."""
        try:
            import sounddevice as sd

            sd.stop()
        except Exception:
            pass
        self._current_thread = None

    @classmethod
    def from_config(cls, config) -> "SoundEffectPlayer":
        """Create a SoundEffectPlayer from an AppConfig."""
        return cls(
            sound_path=config.thinking_sound_path,
            enabled=config.thinking_sound_enabled,
            volume=0.5,
        )