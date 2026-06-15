"""ModelManager — Lazy-load faster-whisper models"""
import sys
import time
from constants import AVAILABLE_MODELS, DATA_DIR

class ModelManager:
    def __init__(self):
        self._model = None
        self._current_size = None
        self._load_attempted = False
        self._last_error = ""
        self._log_file = DATA_DIR / "model-debug.log"

    def _safe_console(self, message: str):
        """Write to console only when launched with a real stdout.

        pythonw.exe sets sys.stdout/sys.stderr to None. Calling print()/flush()
        in that mode crashes model loading before Faster-Whisper can run.
        """
        try:
            if sys.stdout is not None:
                sys.stdout.write(message + "\n")
                sys.stdout.flush()
        except Exception:
            pass

    def load(self, size: str = "tiny", device: str = "cpu") -> bool:
        """Load faster-whisper model. Returns True if successful."""
        if self._model is not None and self._current_size == size:
            return True  # Already loaded

        self._load_attempted = True
        try:
            from faster_whisper import WhisperModel
            self._safe_console(f"[ModelManager] Loading model '{size}' on {device}...")
            self._log(f"model load started size={size} device={device}")
            self._model = WhisperModel(size, device=device, compute_type="default", num_workers=1)
            self._current_size = size
            self._last_error = ""
            self._safe_console(f"[ModelManager] Model '{size}' loaded successfully")
            self._log(f"model load completed size={size} device={device}")
            return True
        except Exception as e:
            self._safe_console(f"[ModelManager] Model load error: {e}")
            self._last_error = f"{type(e).__name__}: {e}"
            self._log(f"model load failed size={size} device={device} error={self._last_error}")
            self._model = None
            self._current_size = None
            return False

    def transcribe(self, audio_path: str, language: str = "en", beam_size: int = 3, initial_prompt: str = None, model_size: str = "tiny") -> str:
        """Transcribe audio file. Returns transcribed text."""
        if self._model is None or self._current_size != model_size:
            if not self.load(size=model_size):
                detail = f": {self._last_error}" if self._last_error else ""
                return f"Model not loaded{detail}"
        try:
            self._log(f"transcribe started audio_path={audio_path} model={model_size} language={language}")
            segs, _ = self._model.transcribe(
                audio_path,
                beam_size=beam_size,
                initial_prompt=initial_prompt,
                language=language or "en"
            )
            text = " ".join(s.text.strip() for s in segs)
            self._log(f"transcribe completed text_len={len(text)}")
            return text if text else "No speech detected"
        except Exception as e:
            self._log(f"transcribe failed error={type(e).__name__}: {e}")
            return f"Error: {e}"

    def _log(self, message: str):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(self._log_file, "a", encoding="utf-8") as file:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
        except Exception:
            pass

    @property
    def is_loaded(self) -> bool:
        return self._model is not None

    @property
    def current_size(self):
        return self._current_size
