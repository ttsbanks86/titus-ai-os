"""Transcriber — Orchestrates recording → transcription → formatting"""
import time
import threading
from audio_recorder import AudioRecorder
from model_manager import ModelManager
from constants import AVAILABLE_MODES

class Transcriber:
    def __init__(self, settings):
        self.settings = settings
        self.model_manager = ModelManager()
        self.recorder = AudioRecorder()
        self._current_mode = "Voice"
        self._current_language = "en"

    def set_mode(self, mode: str):
        if any(m["id"] == mode for m in AVAILABLE_MODES):
            self._current_mode = mode

    def set_language(self, lang: str):
        self._current_language = lang

    def record_and_transcribe(self, progress_callback=None) -> str:
        """Record until stop() called, then transcribe. Returns text."""
        # Start recording
        temp_path = self.recorder.start()
        if not temp_path:
            return "Failed to start recording"

        # Wait for stop signal (handled externally via recorder.stop())
        # This method blocks until stop() is called externally
        while self.recorder.is_recording:
            if progress_callback:
                level = self.recorder.get_level()
                duration = self.recorder.duration
                progress_callback(duration, level)
            time.sleep(0.1)

        # Recording stopped, get the file path
        audio_path = self.recorder.stop()
        if not audio_path:
            return "No audio recorded"

        # Transcribe
        if progress_callback:
            progress_callback(0, 0, "Transcribing...")

        # Load model with current settings
        model_size = self.settings.get("model", "tiny")
        language = self.settings.get("language", "en")

        # Get vocabulary for initial_prompt
        initial_prompt = self._build_initial_prompt()

        # Transcribe
        text = self.model_manager.transcribe(
            audio_path,
            language=language,
            beam_size=3,
            initial_prompt=self._get_initial_prompt()
        )

        # Apply mode formatting
        text = self._format_text(text)

        return text

    def _get_initial_prompt(self):
        """Build initial_prompt from vocabulary for better accuracy."""
        # Import here to avoid circular dependency
        from vocab import get_vocab
        vocab = get_vocab()
        all_terms = vocab.get("words", []) + vocab.get("phrases", [])
        if all_terms:
            return ", ".join(all_terms)
        return None

    def _format_text(self, text: str) -> str:
        """Apply mode-based formatting."""
        if not text:
            return text
        mode = self._current_mode
        if mode == "Email":
            return text.strip()
        elif mode == "Bullets":
            lines = [f"• {s.strip()}" for s in text.split(". ") if s.strip()]
            return "\n".join(lines)
        elif mode == "Meeting":
            return f"[Meeting Notes]\n{text}"
        elif mode == "Message":
            return text.strip()
        return text

    def transcribe_file(self, audio_path: str) -> str:
        """Transcribe an existing audio file."""
        text = self.model_manager.transcribe(
            audio_path,
            language=self.settings.get("language", "en"),
            initial_prompt=self._get_initial_prompt()
        )
        return self._format_text(text)

    def get_audio_level(self) -> float:
        return self.recorder.get_level()

    def get_duration(self) -> float:
        return self.recorder.duration

    def is_recording(self) -> bool:
        return self.recorder.is_recording

    def start_recording(self) -> str:
        return self.recorder.start()

    def stop_recording(self) -> str:
        return self.recorder.stop()