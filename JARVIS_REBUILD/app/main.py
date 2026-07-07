from __future__ import annotations

import argparse
import dataclasses
import tempfile
import sys
from datetime import datetime
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import load_config
from app.doctor import doctor_report
from app.intents import clean_transcript
from app.router import Router
from app.api_server import run_api_server
from app.voice.capture import ShortRecordingError, check_audio_dependencies, format_microphones, list_microphones
from app.voice.speak import Speaker
from app.voice.turn_manager import TurnManager, VoiceTurnResult
from app.voice.wake_word import AlwaysListeningLoop, WakeDecision, WakeWordSettings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean Jarvis rebuild")
    parser.add_argument("--command", help="Run one command and exit.")
    parser.add_argument("--list-mics", action="store_true", help="List detected input microphones and exit.")
    parser.add_argument("--test-mic", action="store_true", help="Record one debug turn, transcribe, route, speak, and exit.")
    parser.add_argument("--push-to-talk", action="store_true", help="Run push-to-talk loop.")
    parser.add_argument("--mode", choices=["hold", "enter"], default="hold", help="Push-to-talk mode.")
    parser.add_argument("--record-seconds", type=float, default=5.0, help="Seconds to record per turn.")
    parser.add_argument("--push-key", help="Hold-to-talk key name. Default comes from config.")
    parser.add_argument("--min-record-seconds", type=float, help="Reject hold recordings shorter than this.")
    parser.add_argument("--input-device", type=int, help="sounddevice input device index.")
    parser.add_argument("--debug-audio", action="store_true", help="Keep debug WAV files in app/logs/audio_debug/.")
    parser.add_argument("--no-speech", action="store_true", help="Print responses without text-to-speech.")
    parser.add_argument("--api", action="store_true", help="Run the local Jarvis API for Mission Control.")
    parser.add_argument("--doctor", action="store_true", help="Check Jarvis configuration without printing secrets.")
    parser.add_argument(
        "--always-listening",
        action="store_true",
        help="Run always-listening mode with wake-word detection. Push-to-talk stays available via --push-to-talk.",
    )
    parser.add_argument(
        "--wake-words",
        help="Override the wake words (semicolon-separated) for always-listening mode. Default is 'jarvis'.",
    )
    parser.add_argument("--briefing", action="store_true", help="Run the daily briefing aggregator and exit.")
    parser.add_argument(
        "--persona",
        choices=["companion", "host"],
        default=None,
        help="Override Jarvis's persona. 'companion' is the default (personal assistant). 'host' is for live show/audience mode.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config()
    # CLI persona override (host mode for live shows)
    if args.persona:
        config = _override_persona(config, args.persona)
    # Initialize persistent memory so Jarvis remembers across sessions
    from app.memory.persistent import init_memory
    init_memory()
    router = Router(config)
    voice_cli = args.push_to_talk or args.test_mic
    speaker = Speaker(
        enabled=config.speech_enabled and not args.no_speech,
        echo=not voice_cli,
        engine=config.tts_engine,
        voice=config.tts_voice,
        rate=config.tts_rate,
        volume=config.tts_volume,
        pitch=config.tts_pitch,
        playback_mode=config.tts_playback_mode,
        elevenlabs_api_key=config.elevenlabs_api_key,
        elevenlabs_voice_id=config.elevenlabs_voice_id,
        elevenlabs_model=config.elevenlabs_model,
        elevenlabs_stability=config.elevenlabs_stability,
        elevenlabs_similarity_boost=config.elevenlabs_similarity_boost,
    )
    turns = TurnManager(router, speaker, auto_speak=not voice_cli)
    push_key = args.push_key or config.push_to_talk_key
    min_record_seconds = args.min_record_seconds or config.min_record_seconds
    debug_audio = args.debug_audio or config.debug_audio_enabled

    if args.doctor:
        exit_code, report = doctor_report(config)
        print(report, flush=True)
        return exit_code

    if args.briefing:
        from app.tools.briefing import briefing_response

        text = briefing_response(config)
        print(_console_safe(f"Jarvis: {text}"), flush=True)
        if speaker.enabled:
            speaker.speak(text)
        return 0

    if args.api:
        run_api_server(config, router)
        return 0

    if args.list_mics:
        print(format_microphones(list_microphones()))
        return 0

    if args.command is not None:
        result = router.handle(args.command)
        if result.speak and result.response:
            speaker.speak(result.response)
        return 0

    if args.test_mic:
        audio_path, keep_audio = _recording_path(config.logs_dir, config.audio_debug_dir, debug_audio)
        result = None
        if args.mode == "enter":
            print("Recording...", flush=True)
        try:
            result = _run_voice_turn(
                turns,
                router,
                audio_path,
                mode=args.mode,
                push_key=push_key,
                min_record_seconds=min_record_seconds,
                record_seconds=args.record_seconds,
                sample_rate=config.sample_rate,
                end_padding_ms=config.record_end_padding_ms,
                transcribe_provider=config.transcribe_provider,
                input_device=args.input_device,
            )
        except RuntimeError as exc:
            _cleanup_audio(audio_path, keep_audio)
            print(f"Microphone test failed: {exc}", flush=True)
            return 1
        finally:
            if result is not None:
                _cleanup_audio(audio_path, keep_audio)
        print(f"Transcript: {result.transcript or '(no speech recognized)'}", flush=True)
        print(f"Route: {result.route_result.route}", flush=True)
        print(f"Intent: {result.route_result.intent}", flush=True)
        if keep_audio:
            print(f"Audio: \"{result.audio_path}\"", flush=True)
        _speak_jarvis_response(result, speaker)
        return 0

    if args.push_to_talk:
        if args.mode == "hold":
            print(f"Hold {_display_key(push_key)} to talk", flush=True)
            dependency_errors = check_audio_dependencies(device=args.input_device)
            if dependency_errors:
                for error in dependency_errors:
                    print(error, flush=True)
                print("Hold mode failed. Try: python app/main.py --push-to-talk --mode enter --debug-audio", flush=True)
                return 1
        else:
            print("Enter push-to-talk fallback. Press Enter to record one turn, or type exit to quit.", flush=True)

        while True:
            if args.mode == "enter":
                value = input("> ").strip().lower()
                if value == "exit":
                    break
            audio_path, keep_audio = _recording_path(config.logs_dir, config.audio_debug_dir, debug_audio)
            try:
                if args.mode == "hold":
                    turn = _run_hold_loop_turn(
                        turns,
                        router,
                        audio_path,
                        push_key=push_key,
                        min_record_seconds=min_record_seconds,
                        sample_rate=config.sample_rate,
                        start_padding_ms=config.record_start_padding_ms,
                        end_padding_ms=config.record_end_padding_ms,
                        transcribe_provider=config.transcribe_provider,
                        input_device=args.input_device,
                        debug_keys=debug_audio,
                    )
                else:
                    print("Recording...", flush=True)
                    turn = turns.run_push_to_talk_turn(
                        audio_path,
                        seconds=args.record_seconds,
                        sample_rate=config.sample_rate,
                        end_padding_ms=config.record_end_padding_ms,
                        transcribe_provider=config.transcribe_provider,
                        device=args.input_device,
                        on_processing=lambda: print("Processing...", flush=True),
                    )
            except ShortRecordingError as exc:
                router.handle(
                    "",
                    source="microphone",
                    metadata={
                        "mode": args.mode,
                        "rejected_reason": "recording_too_short",
                        "duration_seconds": exc.duration_seconds,
                        "min_record_seconds": exc.min_seconds,
                        "push_to_talk_key": push_key,
                        "input_device": args.input_device,
                    },
                )
                print(f"Recording too short ({exc.duration_seconds:.2f}s). Ignored.", flush=True)
                _cleanup_audio(audio_path, keep_audio)
                continue
            except RuntimeError as exc:
                print(f"Recording failed: {exc}", flush=True)
                _cleanup_audio(audio_path, keep_audio)
                continue
            except KeyboardInterrupt:
                print()
                break

            _cleanup_audio(audio_path, keep_audio)
            if debug_audio:
                _print_debug_turn(turn)
            if keep_audio:
                _print_audio_path(turn.audio_path)
            if turn.duration_seconds is not None:
                print(f"Duration: {turn.duration_seconds:.2f}s", flush=True)
            if turn.rms_level is not None:
                print(f"RMS level: {turn.rms_level:.2f}", flush=True)
            _speak_jarvis_response(turn, speaker)
            if turn.route_result.should_exit:
                break
        return 0

    if args.always_listening:
        return _run_always_listening(args, config, router, speaker)

    print("Jarvis text mode. Type exit to quit.")
    while True:
        try:
            text = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        should_exit = turns.handle_text_turn(text)
        if should_exit:
            return 0


def _audio_debug_path(audio_debug_dir: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return audio_debug_dir / f"push_to_talk_{stamp}.wav"


def _recording_path(logs_dir: Path, audio_debug_dir: Path, debug_audio: bool) -> tuple[Path, bool]:
    if debug_audio:
        return _audio_debug_path(audio_debug_dir), True
    logs_dir.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(prefix="jarvis_ptt_", suffix=".wav", dir=logs_dir, delete=False)
    path = Path(handle.name)
    handle.close()
    return path, False


def _cleanup_audio(path: Path, keep_audio: bool) -> None:
    if keep_audio:
        return
    try:
        path.unlink(missing_ok=True)
    except OSError:
        pass


def _run_voice_turn(
    turns: TurnManager,
    router: Router,
    audio_path: Path,
    *,
    mode: str,
    push_key: str,
    min_record_seconds: float,
    record_seconds: float,
    sample_rate: int,
    end_padding_ms: int,
    transcribe_provider: str,
    input_device: int | None,
) -> VoiceTurnResult:
    if mode == "hold":
        return _run_hold_loop_turn(
            turns,
            router,
            audio_path,
            push_key=push_key,
            min_record_seconds=min_record_seconds,
            sample_rate=sample_rate,
            start_padding_ms=250,
            end_padding_ms=end_padding_ms,
            transcribe_provider=transcribe_provider,
            input_device=input_device,
        )
    return turns.run_push_to_talk_turn(
        audio_path,
        seconds=record_seconds,
        sample_rate=sample_rate,
        end_padding_ms=end_padding_ms,
        transcribe_provider=transcribe_provider,
        device=input_device,
        on_processing=lambda: print("Processing...", flush=True),
    )


def _run_hold_loop_turn(
    turns: TurnManager,
    _router: Router,
    audio_path: Path,
    *,
    push_key: str,
    min_record_seconds: float,
    sample_rate: int,
    start_padding_ms: int,
    end_padding_ms: int,
    transcribe_provider: str,
    input_device: int | None,
    debug_keys: bool = False,
) -> VoiceTurnResult:
    turn = turns.run_hold_to_talk_turn(
        audio_path,
        key=push_key,
        min_seconds=min_record_seconds,
        sample_rate=sample_rate,
        start_padding_ms=start_padding_ms,
        end_padding_ms=end_padding_ms,
        transcribe_provider=transcribe_provider,
        device=input_device,
        on_recording_start=lambda: print("Recording...", flush=True),
        on_processing=lambda: print("Processing...", flush=True),
        debug_keys=debug_keys,
    )
    return turn


def _speak_jarvis_response(turn: VoiceTurnResult, speaker: Speaker) -> None:
    if turn.route_result.speak and turn.route_result.response:
        print(_console_safe(f"Jarvis: {turn.route_result.response}"), flush=True)
        speaker.speak(turn.route_result.response)


def _run_always_listening(args, config, router: Router, speaker: Speaker) -> int:
    # Always-listening mode runs continuously until the user presses Ctrl+C
    # or says the sleep phrase ("Jarvis, go to sleep"). Push-to-talk stays
    # available as a separate flag.
    wake_words = tuple(w.strip() for w in (args.wake_words or "").split(";") if w.strip()) or config.wake_words
    settings = WakeWordSettings(
        wake_words=wake_words,
        sample_rate=config.sample_rate,
        voice_rms_threshold=config.wake_word_voice_rms_threshold,
        silence_end_seconds=config.wake_word_silence_end_seconds,
        max_utterance_seconds=config.wake_word_max_utterance_seconds,
        min_utterance_seconds=config.wake_word_min_utterance_seconds,
        post_speak_cooldown_seconds=config.wake_word_post_speak_cooldown_seconds,
        pre_roll_seconds=config.wake_word_pre_roll_seconds,
        device=args.input_device,
        transcribe_provider=config.transcribe_provider,
    )
    sleep_phrase = config.wake_word_sleep_phrase

    def on_state_change(state: str) -> None:
        # Minimal, single-line state output so the user can see what's happening
        # without flooding the console. States: ready, listening, processing,
        # responding, stopped.
        if state == "listening":
            print("Listening...", flush=True)
        elif state == "stopped":
            print("Always-listening stopped.", flush=True)

    def on_wake_utterance(decision: WakeDecision) -> None:
        # Strip the wake word and route the remaining text through the router.
        cleaned = decision.cleaned_text.strip()
        if not cleaned:
            # User said just "Jarvis" with no follow-up. Acknowledge briefly
            # and return to listening.
            print("Jarvis: Yes?", flush=True)
            if speaker.enabled:
                speaker.speak("Yes?")
                loop.paused_for_speaking()
            return
        # Sleep phrase handling: returns Jarvis to push-to-talk mode cleanly.
        if cleaned.lower() == sleep_phrase or cleaned.lower().rstrip(".?") == sleep_phrase:
            print("Jarvis: Going to sleep. Use push-to-talk or restart to wake me.", flush=True)
            if speaker.enabled:
                speaker.speak("Going to sleep.")
            loop.stop()
            return
        result = router.handle(
            cleaned,
            source="microphone",
            metadata={
                "mode": "always_listening",
                "wake_word": decision.wake_word,
                "raw_transcript": decision.raw_text,
                "duration_seconds": decision.duration_seconds,
                "transcribe_provider": settings.transcribe_provider,
                "input_device": settings.device,
            },
        )
        if result.speak and result.response:
            print(_console_safe(f"Jarvis: {result.response}"), flush=True)
            if speaker.enabled:
                # Pause the mic during Jarvis's speech so his TTS doesn't trigger
                # another wake-word turn. The router's existing self-speech
                # rejection in ShortTermMemory is the backstop.
                loop.paused_for_speaking()
                speaker.speak(result.response)
                loop.paused_for_speaking()
        if result.should_exit:
            loop.stop()

    def on_error(msg: str) -> None:
        print(f"[always-listening error] {msg}", flush=True)

    loop = AlwaysListeningLoop(
        settings=settings,
        on_wake_utterance=on_wake_utterance,
        on_state_change=on_state_change,
        on_error=on_error,
    )

    wake_display = ", ".join(w.upper() + ("..." if w == "jarvis" else "") for w in wake_words)
    print(f"Always-listening. Say {wake_display} to address Jarvis. Ctrl+C to stop.", flush=True)
    dependency_errors = check_audio_dependencies(device=args.input_device)
    if dependency_errors:
        for error in dependency_errors:
            print(error, flush=True)
        return 1

    try:
        loop.run()
        return 0
    except KeyboardInterrupt:
        print()
        loop.stop()
        return 0
    except RuntimeError as exc:
        print(f"Always-listening failed: {exc}", flush=True)
        return 1


def _print_debug_turn(turn: VoiceTurnResult) -> None:
    raw = turn.transcript or ""
    cleaned = clean_transcript(raw)
    print(f"Raw transcript: {raw or '(no speech recognized)'}", flush=True)
    print(f"Cleaned transcript: {cleaned or '(empty)'}", flush=True)
    print(f"Transcription provider: {turn.transcribe_provider}", flush=True)
    if turn.transcribe_fallback_used:
        print(f"Transcription fallback: {turn.requested_transcribe_provider} -> {turn.transcribe_provider}", flush=True)
    print(f"Intent: {turn.route_result.intent}", flush=True)
    print(f"Route: {turn.route_result.route}", flush=True)
    print(f"Confidence: {_route_confidence(turn):.2f}", flush=True)


def _print_audio_path(path: Path) -> None:
    print(f"Audio path: {repr(path.as_posix())}", flush=True)
    print(f"Audio file: {path.name}", flush=True)


def _route_confidence(turn: VoiceTurnResult) -> float:
    if not turn.transcript:
        return 0.0
    if turn.route_result.rejected:
        return 0.2
    if turn.route_result.route in {"capabilities", "weather", "system", "greeting"}:
        return 0.9
    if turn.route_result.route == "fallback":
        return 0.35
    return 0.6


def _display_key(key: str) -> str:
    labels = {"right ctrl": "Right Ctrl", "left ctrl": "Left Ctrl", "space": "Space"}
    return labels.get(key.lower(), key)


def _override_persona(config: AppConfig, persona: str) -> AppConfig:
    """Return a new AppConfig with the persona overridden. Used for the --persona CLI flag."""
    return dataclasses.replace(config, jarvis_persona=persona)


def _console_safe(text: str) -> str:
    return text.encode("ascii", errors="replace").decode("ascii")


if __name__ == "__main__":
    raise SystemExit(main())
