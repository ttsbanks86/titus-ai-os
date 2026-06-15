"""AudioRecorder — Low-latency audio capture using sounddevice"""
import sys
import tempfile
import threading
import time
import wave
from pathlib import Path
from constants import DATA_DIR

try:
    import sounddevice as sd
    import numpy as np
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    print("[AudioRecorder] sounddevice not available")

class AudioRecorder:
    """Captures audio from microphone to a temporary WAV file."""
    
    def __init__(self, device_id: int = None, sample_rate: int = 16000, channels: int = 1):
        self._device_id = device_id
        self._sample_rate = sample_rate
        self._channels = channels
        self._recording = False
        self._thread = None
        self._frames = []
        self._temp_path = None
        self._start_time = None
        self._stream = None
        self._last_error = ""
        self._log_file = DATA_DIR / "audio-debug.log"

    def start(self) -> str:
        """Start recording. Returns temp file path when stopped."""
        if self._recording:
            return ""
        
        if not SOUNDDEVICE_AVAILABLE:
            raise RuntimeError("sounddevice not installed")
        
        self._recording = True
        self._frames = []
        self._start_time = time.time()
        
        # Create temp file
        self._temp_path = Path(tempfile.gettempdir()) / f"wmi_{int(time.time()*1000)}.wav"
        
        def callback(indata, frames, time_info, status):
            if self._recording:
                self._frames.append(indata.copy())
        
        try:
            device_info = sd.query_devices(self._device_id, "input") if self._device_id is not None else sd.query_devices(kind="input")
        except Exception as exc:
            device_info = f"device query failed: {type(exc).__name__}: {exc}"
        self._log(f"recording start requested device_id={self._device_id} device_info={device_info}")

        try:
            self._stream = sd.InputStream(
                device=self._device_id,
                samplerate=self._sample_rate,
                channels=self._channels,
                dtype='int16',
                callback=callback,
                blocksize=1024
            )
            self._stream.start()
            self._log(f"recording stream started path={self._temp_path} sample_rate={self._sample_rate} channels={self._channels}")
        except Exception as exc:
            self._recording = False
            self._last_error = f"{type(exc).__name__}: {exc}"
            self._log(f"recording stream failed error={self._last_error}")
            raise
        return self._temp_path

    def stop(self) -> str:
        """Stop recording and save WAV. Returns path to WAV file."""
        if not self._recording:
            return ""
        
        self._recording = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
        
        # Concatenate frames
        if self._frames:
            audio_data = np.concatenate(self._frames, axis=0)
        else:
            audio_data = np.array([], dtype=np.int16)

        duration = time.time() - self._start_time if self._start_time else 0.0
        sample_count = int(audio_data.size)
        peak = int(np.max(np.abs(audio_data))) if sample_count else 0
        rms = float(np.sqrt(np.mean(audio_data.astype(np.float32) ** 2))) if sample_count else 0.0
        
        # Write WAV
        with wave.open(str(self._temp_path), 'wb') as wf:
            wf.setnchannels(self._channels)
            wf.setsampwidth(2)  # 16-bit = 2 bytes
            wf.setframerate(self._sample_rate)
            wf.writeframes(audio_data.tobytes())

        size = self._temp_path.stat().st_size if self._temp_path.exists() else -1
        self._log(
            f"recording saved path={self._temp_path} frames={len(self._frames)} "
            f"samples={sample_count} duration={duration:.2f}s size={size} rms={rms:.2f} peak={peak}"
        )
        return str(self._temp_path) if self._temp_path.exists() else ""

    @property
    def is_recording(self) -> bool:
        return self._recording

    @property
    def duration(self) -> float:
        if self._start_time and self._recording:
            return time.time() - self._start_time
        return 0.0

    def get_level(self) -> float:
        """Get current audio level (0.0 to 1.0) for level meter."""
        if not self._frames:
            return 0.0
        # Get last frame's RMS
        last_frame = self._frames[-1]
        if len(last_frame) == 0:
            return 0.0
        rms = np.sqrt(np.mean(last_frame.astype(np.float32) ** 2))
        return min(rms / 32768.0, 1.0)  # Normalize to 0-1

    def _log(self, message: str):
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            with open(self._log_file, "a", encoding="utf-8") as file:
                file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
        except Exception:
            pass
