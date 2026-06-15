"""Transcriber — Orchestrates recording → transcription → formatting"""
import time
import threading
import json
import urllib.request
from audio_recorder import AudioRecorder
from model_manager import ModelManager
from constants import AVAILABLE_MODES, DATA_DIR

OLLAMA_ENDPOINT = "http://127.0.0.1:11434/api/generate"
SMART_MODEL = "llama3.2:3b"

SMART_PROMPT_TEMPLATE = """[INST] You are a smart dictation fixer. Rewrite the raw speech below into clear, well-formed text.

Rules:
- Fix run-on sentences and fragments.
- Remove repeated words, stutters, and verbal fillers.
- Keep the original meaning and tone. Do NOT add information.
- Output ONLY the polished text. No commentary, no prefixes, no quotes.

Raw speech: {raw_text}

Polished text: [/INST]"""

class Transcriber:
    def __init__(self, settings):
        self.settings = settings
        self.model_manager = ModelManager()
        self.recorder = AudioRecorder()
        self._current_mode = "Dictation"
        self._current_language = "en"
        self._log_file = DATA_DIR / "transcriber-debug.log"

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

        model_size = self.settings.get("model", "tiny")
        language = self.settings.get("language", self._current_language or "en")

        text = self.model_manager.transcribe(
            audio_path,
            language=language,
            beam_size=3,
            initial_prompt=self._get_initial_prompt(),
            model_size=model_size,
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

    def _smart_polish(self, raw_text: str) -> str:
        """Send raw text to local Ollama for smart rewording."""
        if not raw_text or raw_text.strip() in ("No speech detected", "Model not loaded", ""):
            return raw_text
        prompt = SMART_PROMPT_TEMPLATE.format(raw_text=raw_text.strip()[:2000])
        payload = json.dumps({
            "model": SMART_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3, "num_predict": 1024}
        }).encode()
        self._log(f"smart_polish start text_len={len(raw_text)} model={SMART_MODEL}")
        try:
            req = urllib.request.Request(OLLAMA_ENDPOINT, data=payload,
                                          headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
            polished = result.get("response", "").strip()
            # Clean up any quotes the LLM wraps around the output
            if polished.startswith('"') and polished.endswith('"'):
                polished = polished[1:-1]
            if polished.startswith("'") and polished.endswith("'"):
                polished = polished[1:-1]
            if not polished:
                polished = raw_text  # fallback
            self._log(f"smart_polish done raw_len={len(raw_text)} polished_len={len(polished)}")
            return polished
        except Exception as exc:
            self._log(f"smart_polish failed error={type(exc).__name__}: {exc}")
            return raw_text  # fallback to raw transcription

    def transcribe_file(self, audio_path: str) -> str:
        """Transcribe an existing audio file."""
        self._log(f"transcribe_file called audio_path={audio_path} mode={self._current_mode} language={self.settings.get('language', self._current_language or 'en')} model={self.settings.get('model', 'tiny')}")
        text = self.model_manager.transcribe(
            audio_path,
            language=self.settings.get("language", self._current_language or "en"),
            initial_prompt=self._get_initial_prompt(),
            model_size=self.settings.get("model", "tiny"),
        )
        # Apply Smart Prompt polish for the special mode
        if self._current_mode == "Smart Prompt":
            text = self._smart_polish(text)
        formatted = self._format_text(text)
        self._log(f"transcribe_file result raw_len={len(text) if text else 0} formatted_len={len(formatted) if formatted else 0} preview={(formatted or '')[:120]!r}")
        return formatted

    def get_audio_level(self) -> float:
        return self.recorder.get_level()

    def get_duration(self) -> float:
        return self.recorder.duration

    def is_recording(self) -> bool:
        return self.recorder.is_recording

    def start_recording(self) -> str:
        microphone = self.settings.get("microphone", "")
        try:
            self.recorder._device_id = int(microphone) if microphone not in (None, "") else None
        except (TypeError, ValueError):
            self.recorder._device_id = None
        self._log(f"start_recording microphone_setting={microphone!r} resolved_device_id={self.recorder._device_id}")
        return self.recorder.start()

    def stop_recording(self) -> str:
        path = self.recorder.stop()
        self._log(f"stop_recording path={path}")
        return path

    def _log(self, message: str):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(self._log_file, "a", encoding="utf-8") as file:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
        except Exception:
            pass
