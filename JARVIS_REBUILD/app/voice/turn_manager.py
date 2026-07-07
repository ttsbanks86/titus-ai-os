from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from app.router import RouteResult
from app.router import Router
from app.voice.capture import record_hold_to_talk, record_push_to_talk
from app.voice.speak import Speaker
from app.voice.transcribe import transcribe_audio_result


@dataclass(frozen=True)
class VoiceTurnResult:
    audio_path: Path
    transcript: str
    route_result: RouteResult
    duration_seconds: float | None = None
    rms_level: float | None = None
    transcribe_provider: str = "speechrecognition"
    requested_transcribe_provider: str = "speechrecognition"
    transcribe_fallback_used: bool = False


class TurnManager:
    def __init__(self, router: Router, speaker: Speaker, auto_speak: bool = True) -> None:
        self.router = router
        self.speaker = speaker
        self.auto_speak = auto_speak

    def handle_text_turn(self, text: str) -> bool:
        result = self.router.handle(text)
        if result.intent == "stop":
            self.speaker.stop()
        if self.auto_speak and result.speak:
            self.speaker.speak(result.response)
        return result.should_exit

    def run_push_to_talk_turn(
        self,
        audio_path: Path,
        seconds: float = 5.0,
        sample_rate: int = 16000,
        end_padding_ms: int = 500,
        transcribe_provider: str = "speechrecognition",
        device: int | None = None,
        on_processing: Callable[[], None] | None = None,
    ) -> VoiceTurnResult:
        _, audio_stats = record_push_to_talk(
            audio_path,
            seconds=seconds,
            sample_rate=sample_rate,
            end_padding_ms=end_padding_ms,
            device=device,
        )
        if on_processing is not None:
            on_processing()
        transcription = transcribe_audio_result(audio_path, provider=transcribe_provider)
        route_result = self.router.handle(
            transcription.text,
            source="microphone",
            metadata={
                "audio_path": str(audio_path),
                "mode": "enter",
                "record_seconds": seconds,
                "sample_rate": sample_rate,
                "record_end_padding_ms": end_padding_ms,
                "transcribe_provider": transcription.provider_used,
                "requested_transcribe_provider": transcription.requested_provider,
                "transcribe_fallback_used": transcription.fallback_used,
                "input_device": device,
            },
        )
        if route_result.intent == "stop":
            self.speaker.stop()
        if self.auto_speak and route_result.speak:
            self.speaker.speak(route_result.response)
        return VoiceTurnResult(
            audio_path=audio_path,
            transcript=transcription.text,
            route_result=route_result,
            duration_seconds=audio_stats.duration_seconds,
            rms_level=audio_stats.rms_level,
            transcribe_provider=transcription.provider_used,
            requested_transcribe_provider=transcription.requested_provider,
            transcribe_fallback_used=transcription.fallback_used,
        )

    def run_hold_to_talk_turn(
        self,
        audio_path: Path,
        key: str = "right ctrl",
        min_seconds: float = 0.35,
        sample_rate: int = 16000,
        start_padding_ms: int = 250,
        end_padding_ms: int = 500,
        transcribe_provider: str = "speechrecognition",
        device: int | None = None,
        on_recording_start: Callable[[], None] | None = None,
        on_processing: Callable[[], None] | None = None,
        debug_keys: bool = False,
    ) -> VoiceTurnResult:
        _, audio_stats = record_hold_to_talk(
            audio_path,
            key=key,
            min_seconds=min_seconds,
            sample_rate=sample_rate,
            start_padding_ms=start_padding_ms,
            end_padding_ms=end_padding_ms,
            device=device,
            on_recording_start=on_recording_start,
            debug_keys=debug_keys,
        )
        if on_processing is not None:
            on_processing()
        transcription = transcribe_audio_result(audio_path, provider=transcribe_provider)
        route_result = self.router.handle(
            transcription.text,
            source="microphone",
            metadata={
                "audio_path": str(audio_path),
                "mode": "hold",
                "duration_seconds": audio_stats.duration_seconds,
                "rms_level": audio_stats.rms_level,
                "sample_rate": sample_rate,
                "record_start_padding_ms": start_padding_ms,
                "record_end_padding_ms": end_padding_ms,
                "transcribe_provider": transcription.provider_used,
                "requested_transcribe_provider": transcription.requested_provider,
                "transcribe_fallback_used": transcription.fallback_used,
                "push_to_talk_key": key,
                "input_device": device,
            },
        )
        if route_result.intent == "stop":
            self.speaker.stop()
        if self.auto_speak and route_result.speak:
            self.speaker.speak(route_result.response)
        return VoiceTurnResult(
            audio_path=audio_path,
            transcript=transcription.text,
            route_result=route_result,
            duration_seconds=audio_stats.duration_seconds,
            rms_level=audio_stats.rms_level,
            transcribe_provider=transcription.provider_used,
            requested_transcribe_provider=transcription.requested_provider,
            transcribe_fallback_used=transcription.fallback_used,
        )

    def handle_push_to_talk_turn(
        self,
        audio_path: Path,
        seconds: float = 5.0,
        device: int | None = None,
    ) -> bool:
        result = self.run_push_to_talk_turn(audio_path, seconds=seconds, device=device)
        return result.route_result.should_exit
