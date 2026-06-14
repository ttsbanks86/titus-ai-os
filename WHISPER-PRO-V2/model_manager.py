"""ModelManager — Lazy-load faster-whisper models"""
import sys
from constants import AVAILABLE_MODELS

class ModelManager:
    def __init__(self):
        self._model = None
        self._current_size = None
        self._load_attempted = False

    def load(self, size: str = "tiny", device: str = "cpu") -> bool:
        """Load faster-whisper model. Returns True if successful."""
        if self._load_attempted and self._model is None:
            return False  # Don't retry if previously failed

        if self._model is not None and self._current_size == size:
            return True  # Already loaded

        self._load_attempted = True
        try:
            from faster_whisper import WhisperModel
            print(f"[ModelManager] Loading model '{size}' on {device}...")
            sys.stdout.flush()
            self._model = WhisperModel(size, device=device, compute_type="default", num_workers=1)
            self._current_size = size
            print(f"[ModelManager] Model '{size}' loaded successfully")
            return True
        except Exception as e:
            print(f"[ModelManager] Model load error: {e}")
            self._model = None
            self._current_size = None
            return False

    def transcribe(self, audio_path: str, language: str = "en", beam_size: int = 3, initial_prompt: str = None) -> str:
        """Transcribe audio file. Returns transcribed text."""
        if self._model is None:
            if not self.load():
                return "Model not loaded"
        try:
            segs, _ = self._model.transcribe(
                audio_path,
                beam_size=3,
                initial_prompt=initial_prompt,
                language="en"
            )
            text = " ".join(s.text.strip() for s in segs)
            return text if text else "No speech detected"
        except Exception as e:
            return f"Error: {e}"

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def current_size(self):
        return self._current_size