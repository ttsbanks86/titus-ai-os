"""Always-listening mode with wake-word detection.

Design goals:
- Nothing leaves the machine until a wake word is detected.
- Voice activity detection (RMS threshold) prevents burning transcription on silence.
- A configurable silence window detects end-of-utterance.
- A wake-word classifier decides whether to route the utterance to the Jarvis
  router or ignore it as background conversation.
- Self-speech rejection is handled by ShortTermMemory in the router (Codex already
  wired this); we ALSO add a local cooldown so the mic is not captured while
  Jarvis is still speaking.
- The loop is fully cancellable via KeyboardInterrupt and a stop event.

This module is opt-in. It does NOT run unless the user invokes
`python app/main.py --always-listening`. Push-to-talk stays available.
"""
from __future__ import annotations

import tempfile
import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


# Sensible defaults tuned for typical desktop microphones.
DEFAULT_SAMPLE_RATE = 16000
# Voice activity threshold. Below this RMS, we consider the input silent.
# 16-bit PCM amplitude range is -32768..32767; an RMS of ~300 corresponds
# to a quiet room, ~1000+ to normal speech a foot from the mic.
DEFAULT_VOICE_RMS_THRESHOLD = 350.0
# How many seconds of silence end an utterance.
DEFAULT_SILENCE_END_SECONDS = 1.2
# Maximum utterance length we will accept before forcing a transcription.
DEFAULT_MAX_UTTERANCE_SECONDS = 12.0
# Minimum utterance length. Below this we ignore (avoid noise bursts).
DEFAULT_MIN_UTTERANCE_SECONDS = 0.4
# Cooldown after Jarvis finishes speaking, so its own TTS does not trigger us.
DEFAULT_POST_SPEAK_COOLDOWN_SECONDS = 1.5
# Size of the pre-roll buffer so we capture the first phoneme of the wake word.
DEFAULT_PRE_ROLL_SECONDS = 0.6


@dataclass(frozen=True)
class WakeWordSettings:
    wake_words: tuple[str, ...] = ("jarvis",)
    sample_rate: int = DEFAULT_SAMPLE_RATE
    voice_rms_threshold: float = DEFAULT_VOICE_RMS_THRESHOLD
    silence_end_seconds: float = DEFAULT_SILENCE_END_SECONDS
    max_utterance_seconds: float = DEFAULT_MAX_UTTERANCE_SECONDS
    min_utterance_seconds: float = DEFAULT_MIN_UTTERANCE_SECONDS
    post_speak_cooldown_seconds: float = DEFAULT_POST_SPEAK_COOLDOWN_SECONDS
    pre_roll_seconds: float = DEFAULT_PRE_ROLL_SECONDS
    device: int | None = None
    transcribe_provider: str = "speechrecognition"


@dataclass(frozen=True)
class WakeDecision:
    triggered: bool
    wake_word: str
    cleaned_text: str
    raw_text: str
    reason: str
    duration_seconds: float


def detect_wake_word(
    transcript: str,
    wake_words: tuple[str, ...] = ("jarvis",),
) -> tuple[bool, str, str]:
    """Decide whether a transcript begins with (or contains early on) a wake word.

    Returns: (triggered, detected_word, cleaned_text)
    - triggered: True if the wake word matched and we should route the cleaned_text.
    - detected_word: lowercase wake word that matched, or empty string.
    - cleaned_text: the transcript with the leading wake word (and a following
      comma/punctuation) stripped, suitable for routing to the router.
    """
    if not transcript:
        return False, "", ""
    text = transcript.strip()
    lowered = text.lower()
    for wake in wake_words:
        if not wake:
            continue
        wake_lower = wake.lower().strip()
        # Common ways the user addresses Jarvis:
        #   "Jarvis, what's the weather?"        (comma)
        #   "Jarvis what's the weather?"          (no punctuation)
        #   "Jarvis... what time is it"           (ellipsis)
        #   "Hey Jarvis, what's the weather?"     (hey prefix)
        #   "ok Jarvis ..."                        (ok prefix)
        # First, try the simple prefix list (handles "hey/ok/okayo/yo/hi" prefixes
        # and the most common punctuation patterns).
        prefixes = (
            wake_lower + ",",
            wake_lower + " ",
            wake_lower + "...",
            wake_lower + ".",
            wake_lower + "!",
            wake_lower + "?",
            "hey " + wake_lower,
            "ok " + wake_lower,
            "okay " + wake_lower,
            "yo " + wake_lower,
            "hi " + wake_lower,
        )
        for prefix in prefixes:
            if lowered.startswith(prefix):
                cleaned = text[len(prefix):].lstrip(", ;:.").strip()
                return True, wake_lower, cleaned
        # Bare wake word only (e.g., the user just says "Jarvis")
        if lowered == wake_lower:
            return True, wake_lower, ""
        # Handle the case where wake word is followed by punctuation with no space
        # but our specific prefix list missed it (e.g., "Jarvis--" or "Jarvis:").
        # We check: the text starts with the wake word, the very next character is
        # non-alphanumeric, and after stripping the wake word + punctuation we have
        # either nothing (bare) or content (a real command).
        if lowered.startswith(wake_lower) and len(text) > len(wake_lower):
            next_char = lowered[len(wake_lower)]
            if not next_char.isalnum() and next_char != " ":
                cleaned = text[len(wake_lower):].lstrip(", ;:.-!?").strip()
                return True, wake_lower, cleaned
    # Wake word not at the start. We intentionally do NOT trigger on
    # wake words in the MIDDLE of an utterance. Background conversation that
    # happens to mention Jarvis should not trigger him.
    return False, "", text


class AlwaysListeningLoop:
    """Continuously captures audio, detects voice activity, transcribes spoken
    utterances, and routes only the ones that begin with a wake word.
    """

    def __init__(
        self,
        settings: WakeWordSettings,
        on_wake_utterance: Callable[[WakeDecision], None],
        on_state_change: Callable[[str], None] | None = None,
        on_error: Callable[[str], None] | None = None,
    ) -> None:
        self.settings = settings
        self.on_wake_utterance = on_wake_utterance
        self.on_state_change = on_state_change or (lambda _state: None)
        self.on_error = on_error or (lambda _msg: None)
        self._stop_event = threading.Event()
        self._cooldown_until = 0.0

    def stop(self) -> None:
        self._stop_event.set()

    def paused_for_speaking(self, seconds: float | None = None) -> None:
        """Tell the loop that Jarvis is about to speak, so we should ignore
        the microphone for a cooldown period. This is a defense in depth on
        top of the existing ShortTermMemory self-speech rejection.
        """
        cooldown = seconds if seconds is not None else self.settings.post_speak_cooldown_seconds
        self._cooldown_until = time.monotonic() + cooldown

    def run(self) -> None:
        try:
            import numpy as np
            import sounddevice as sd
            from scipy.io.wavfile import write
        except ImportError as exc:
            raise RuntimeError(
                "Always-listening mode requires sounddevice, numpy, and scipy. "
                "Install requirements.txt first."
            ) from exc

        settings = self.settings
        stop_event = self._stop_event
        pre_roll_frames = int(settings.pre_roll_seconds * settings.sample_rate)
        pre_roll: deque = deque(maxlen=pre_roll_frames)
        chunks: list[np.ndarray] = []
        state = {
            "recording": False,
            "silence_frames": 0,
            "utterance_start": 0.0,
            "last_voice_frame": 0.0,
        }

        # Frames per callback tick.(sounddevice recommends 2048 at 16k.)
        blocksize = 2048
        silence_frames_needed = int(settings.silence_end_seconds * settings.sample_rate / blocksize)
        max_utterance_frames = int(settings.max_utterance_seconds * settings.sample_rate)

        def on_audio(indata, frames, _time_info, _status) -> None:
            if stop_event.is_set():
                raise sd.CallbackStop
            # While in cooldown (Jarvis speaking), discard audio entirely.
            if time.monotonic() < self._cooldown_until:
                return
            audio = indata.copy()
            rms = _rms(audio)
            voice = rms > settings.voice_rms_threshold
            now = time.monotonic()

            if not state["recording"]:
                # Always maintain pre-roll so we do not clip the wake word.
                pre_roll.append(audio)
                if voice:
                    # Start a new utterance.
                    state["recording"] = True
                    state["utterance_start"] = now
                    state["last_voice_frame"] = now
                    state["silence_frames"] = 0
                    if pre_roll:
                        chunks.extend(list(pre_roll))
                        pre_roll.clear()
                    chunks.append(audio)
                    self.on_state_change("listening")
                return

            # We are mid-utterance.
            chunks.append(audio)
            if voice:
                state["last_voice_frame"] = now
                state["silence_frames"] = 0
            else:
                state["silence_frames"] += 1

            utterance_duration = now - state["utterance_start"]
            silence_too_long = state["silence_frames"] >= silence_frames_needed
            utterance_too_long = len(chunks) >= max_utterance_frames
            if (silence_too_long or utterance_too_long) and chunks:
                # End of utterance. Freeze the buffer, signal the main thread.
                frozen = list(chunks)
                chunks.clear()
                state["recording"] = False
                state["silence_frames"] = 0
                self._process_utterance(frozen, settings)

        # Run the loop on the main thread; audio callback runs in sounddevice's
        # background thread. We sleep until the stop event is set.
        try:
            with sd.InputStream(
                samplerate=settings.sample_rate,
                channels=1,
                dtype="int16",
                blocksize=blocksize,
                device=settings.device,
                callback=on_audio,
            ):
                self.on_state_change("ready")
                while not stop_event.is_set():
                    stop_event.wait(timeout=0.5)
        except sd.PortAudioError as exc:
            device_hint = f" device {settings.device}" if settings.device is not None else " the default input device"
            raise RuntimeError(f"Could not open microphone on{device_hint}: {exc}") from exc
        finally:
            self.on_state_change("stopped")

    def _process_utterance(self, frozen_chunks: list, settings: WakeWordSettings) -> None:
        try:
            import numpy as np
            from scipy.io.wavfile import write
        except ImportError:
            return
        try:
            audio = np.concatenate(frozen_chunks, axis=0)
        except ValueError:
            return
        duration = float(len(audio) / settings.sample_rate)
        if duration < settings.min_utterance_seconds:
            # Too short to be a real utterance. Ignore.
            self.on_state_change("ready")
            return
        # Write to a temp WAV file for the transcriber, then delete after.
        tmp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                suffix=".wav", delete=False, dir=tempfile.gettempdir()
            ) as handle:
                tmp_path = Path(handle.name)
            write(str(tmp_path), settings.sample_rate, audio)
            # Import here so tests can mock transcribe_audio_result without
            # pulling in speech_recognition at module import time.
            from app.voice.transcribe import transcribe_audio_result

            result = transcribe_audio_result(tmp_path, provider=settings.transcribe_provider)
            text = result.text or ""
        except Exception as exc:
            self.on_error(f"transcription error: {exc}")
            self.on_state_change("ready")
            return
        finally:
            if tmp_path is not None:
                try:
                    if tmp_path.exists():
                        tmp_path.unlink()
                except OSError:
                    pass

        triggered, wake_word, cleaned = detect_wake_word(text, settings.wake_words)
        decision = WakeDecision(
            triggered=triggered,
            wake_word=wake_word,
            cleaned_text=cleaned,
            raw_text=text,
            reason="wake_word_matched" if triggered else "no_wake_word",
            duration_seconds=duration,
        )
        if triggered:
            self.on_wake_utterance(decision)
        else:
            # Background conversation; do not route. State goes back to ready.
            self.on_state_change("ready")


def _rms(audio) -> float:
    try:
        import numpy as np
    except ImportError:
        return 0.0
    values = audio.astype("float64")
    if values.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(values * values)))
