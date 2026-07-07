from __future__ import annotations

import time
import threading
from collections.abc import Callable
from collections import deque
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MicrophoneDevice:
    index: int
    name: str
    channels: int
    sample_rate: int
    is_default: bool = False


class ShortRecordingError(RuntimeError):
    def __init__(self, duration_seconds: float, min_seconds: float) -> None:
        self.duration_seconds = duration_seconds
        self.min_seconds = min_seconds
        super().__init__(f"Recording was too short: {duration_seconds:.2f}s; minimum is {min_seconds:.2f}s.")


@dataclass(frozen=True)
class AudioStats:
    duration_seconds: float
    rms_level: float


def list_microphones() -> list[MicrophoneDevice]:
    try:
        import sounddevice as sd
    except ImportError as exc:
        raise RuntimeError("Microphone listing requires sounddevice. Install requirements.txt first.") from exc

    devices = sd.query_devices()
    default_input = sd.default.device[0] if isinstance(sd.default.device, (list, tuple)) else None
    microphones: list[MicrophoneDevice] = []
    for index, device in enumerate(devices):
        channels = int(device.get("max_input_channels", 0))
        if channels <= 0:
            continue
        microphones.append(
            MicrophoneDevice(
                index=index,
                name=str(device.get("name", "Unknown microphone")),
                channels=channels,
                sample_rate=int(float(device.get("default_samplerate", 16000))),
                is_default=index == default_input,
            )
        )
    return microphones


def format_microphones(devices: list[MicrophoneDevice]) -> str:
    if not devices:
        return "No input microphones were detected."
    lines = ["Input microphones:"]
    for device in devices:
        marker = " default" if device.is_default else ""
        lines.append(
            f"  [{device.index}] {device.name} - {device.channels} channel(s), "
            f"default {device.sample_rate} Hz{marker}"
        )
    return "\n".join(lines)


def record_push_to_talk(
    output_path: Path,
    seconds: float = 5.0,
    sample_rate: int = 16000,
    device: int | None = None,
    end_padding_ms: int = 500,
) -> tuple[Path, AudioStats]:
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write
    except ImportError as exc:
        raise RuntimeError(
            "Push-to-talk recording requires sounddevice and scipy. Install requirements.txt first."
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames = int((seconds + (end_padding_ms / 1000.0)) * sample_rate)
    try:
        audio = sd.rec(frames, samplerate=sample_rate, channels=1, dtype="int16", device=device)
        sd.wait()
    except sd.PortAudioError as exc:
        device_hint = f" device {device}" if device is not None else " the default input device"
        raise RuntimeError(f"Could not record from{device_hint}: {exc}") from exc
    write(str(output_path), sample_rate, audio)
    return output_path, AudioStats(duration_seconds=_audio_duration(audio, sample_rate), rms_level=_rms_level(audio))


def record_hold_to_talk(
    output_path: Path,
    key: str = "right ctrl",
    min_seconds: float = 0.35,
    sample_rate: int = 16000,
    start_padding_ms: int = 250,
    end_padding_ms: int = 500,
    device: int | None = None,
    on_recording_start: Callable[[], None] | None = None,
    debug_keys: bool = False,
) -> tuple[Path, AudioStats]:
    try:
        import numpy as np
        from pynput import keyboard
        import sounddevice as sd
        from scipy.io.wavfile import write
    except ImportError as exc:
        raise RuntimeError(
            "Hold-to-talk recording requires pynput, sounddevice, numpy, and scipy. Install requirements.txt first."
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    target_key = _parse_hold_key(key, keyboard)
    pressed = threading.Event()
    released = threading.Event()

    chunks = []
    pre_roll = deque()
    state = {"recording": False, "started_at": 0.0, "released_at": 0.0}
    start_padding_seconds = start_padding_ms / 1000.0
    end_padding_seconds = end_padding_ms / 1000.0

    def on_audio(indata, _frames, _time_info, _status) -> None:
        now = time.monotonic()
        audio_chunk = indata.copy()
        if state["recording"]:
            chunks.append(audio_chunk)
            return
        pre_roll.append((now, audio_chunk))
        while pre_roll and now - pre_roll[0][0] > start_padding_seconds:
            pre_roll.popleft()

    def on_press(pressed_key) -> None:
        matched = _keys_match(pressed_key, target_key)
        already_held = pressed.is_set()
        if debug_keys and (not matched or not already_held):
            print(f"Key pressed: {pressed_key}", flush=True)
            print(f"Matched push-to-talk key: {str(matched).lower()}", flush=True)
        if matched and not already_held:
            chunks.extend(chunk for _timestamp, chunk in pre_roll)
            pre_roll.clear()
            state["recording"] = True
            state["started_at"] = time.monotonic()
            pressed.set()

    def on_release(released_key) -> bool | None:
        matched = _keys_match(released_key, target_key)
        if debug_keys:
            print(f"Key released: {released_key}", flush=True)
            print(f"Matched push-to-talk key: {str(matched).lower()}", flush=True)
        if matched and pressed.is_set():
            state["released_at"] = time.monotonic()
            released.set()
            return False
        return None

    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            with sd.InputStream(
                samplerate=sample_rate,
                channels=1,
                dtype="int16",
                device=device,
                callback=on_audio,
            ):
                pressed.wait()
                if on_recording_start is not None:
                    on_recording_start()
                released.wait()
                time.sleep(end_padding_seconds)
                state["recording"] = False
            listener.stop()
    except sd.PortAudioError as exc:
        device_hint = f" device {device}" if device is not None else " the default input device"
        raise RuntimeError(f"Could not record from{device_hint}: {exc}") from exc

    held_duration = state["released_at"] - state["started_at"]
    if held_duration < min_seconds:
        raise ShortRecordingError(held_duration, min_seconds)
    if not chunks:
        raise RuntimeError("No audio frames were captured.")

    audio = np.concatenate(chunks, axis=0)
    write(str(output_path), sample_rate, audio)
    return output_path, AudioStats(duration_seconds=_audio_duration(audio, sample_rate), rms_level=_rms_level(audio))


def check_audio_dependencies(device: int | None = None) -> list[str]:
    errors: list[str] = []
    try:
        import pynput  # noqa: F401
    except Exception as exc:
        errors.append(f"pynput failed: {type(exc).__name__}: {exc}")
    try:
        import sounddevice as sd
    except Exception as exc:
        errors.append(f"sounddevice failed: {type(exc).__name__}: {exc}")
        return errors
    try:
        sd.check_input_settings(device=device, samplerate=16000, channels=1, dtype="int16")
    except Exception as exc:
        device_label = f"device {device}" if device is not None else "default input device"
        errors.append(f"microphone access failed for {device_label}: {type(exc).__name__}: {exc}")
    return errors


def _parse_hold_key(key_name: str, keyboard_module):
    normalized = key_name.strip().lower().replace("_", " ")
    mapping = {
        "right ctrl": keyboard_module.Key.ctrl_r,
        "right control": keyboard_module.Key.ctrl_r,
        "ctrl r": keyboard_module.Key.ctrl_r,
        "left ctrl": keyboard_module.Key.ctrl_l,
        "left control": keyboard_module.Key.ctrl_l,
        "ctrl l": keyboard_module.Key.ctrl_l,
        "space": keyboard_module.Key.space,
        "shift": keyboard_module.Key.shift,
        "right shift": keyboard_module.Key.shift_r,
        "left shift": keyboard_module.Key.shift_l,
        "alt": keyboard_module.Key.alt,
        "right alt": keyboard_module.Key.alt_r,
        "left alt": keyboard_module.Key.alt_l,
    }
    if normalized in mapping:
        return mapping[normalized]
    if len(normalized) == 1:
        return keyboard_module.KeyCode.from_char(normalized)
    raise RuntimeError(f"Unsupported push-to-talk key: {key_name}")


def _keys_match(observed_key, target_key) -> bool:
    observed_name = str(observed_key)
    target_name = str(target_key)
    if target_name == "Key.ctrl_r" and observed_name in {"Key.ctrl", "Key.ctrl_r"}:
        return True
    if target_name == "Key.ctrl_l" and observed_name in {"Key.ctrl", "Key.ctrl_l"}:
        return True
    return observed_key == target_key


def _rms_level(audio) -> float:
    try:
        import numpy as np
    except ImportError:
        return 0.0
    values = audio.astype("float64")
    if values.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(values * values)))


def _audio_duration(audio, sample_rate: int) -> float:
    if sample_rate <= 0:
        return 0.0
    return float(len(audio) / sample_rate)
