from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.intents import clean_transcript


@dataclass(frozen=True)
class TranscriptionResult:
    text: str
    provider_used: str
    requested_provider: str
    fallback_used: bool = False


def transcribe_audio(audio_path: Path, provider: str = "speechrecognition") -> str:
    return transcribe_audio_result(audio_path, provider=provider).text


def transcribe_audio_result(audio_path: Path, provider: str = "speechrecognition") -> TranscriptionResult:
    requested = (provider or "speechrecognition").strip().lower()
    if requested == "whisper":
        whisper_result = _try_transcribe_whisper(audio_path)
        if whisper_result is not None:
            return TranscriptionResult(
                text=whisper_result,
                provider_used="whisper",
                requested_provider=requested,
                fallback_used=False,
            )
        text = _transcribe_speechrecognition(audio_path)
        return TranscriptionResult(
            text=text,
            provider_used="speechrecognition",
            requested_provider=requested,
            fallback_used=True,
        )
    text = _transcribe_speechrecognition(audio_path)
    return TranscriptionResult(
        text=text,
        provider_used="speechrecognition",
        requested_provider=requested,
        fallback_used=False,
    )


def _try_transcribe_whisper(audio_path: Path) -> str | None:
    try:
        import whisper
    except ImportError:
        return None
    model = whisper.load_model("base")
    result = model.transcribe(str(audio_path), fp16=False)
    return clean_transcript(str(result.get("text", "")))


def _transcribe_speechrecognition(audio_path: Path) -> str:
    try:
        import speech_recognition as sr
    except ImportError as exc:
        raise RuntimeError("Transcription requires SpeechRecognition. Install requirements.txt first.") from exc

    recognizer = sr.Recognizer()
    with sr.AudioFile(str(audio_path)) as source:
        audio = recognizer.record(source)
    try:
        return clean_transcript(recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""
