"""AudioRecorder — Low-latency audio capture using sounddevice"""
import sys
import tempfile
import threading
import time
import wave
from pathlib import Path

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
        
        self._stream = sd.InputStream(
            device=self._device_id,
            samplerate=16000,
            channels=1,
            dtype='int16',
            callback=callback,
            blocksize=1024
        )
        self._stream.start()
        return self._temp_path

    def stop(self) -> str:
        """Stop recording and save WAV. Returns path to WAV file."""
        if not self._recording:
            return ""
        
        self._recording = False
        self._stream.stop()
        self._stream.close()
        
        # Concatenate frames
        if self._frames:
            audio_data = np.concatenate(self._frames, axis=0)
        else:
            audio_data = np.array([], dtype=np.int16)
        
        # Write WAV
        with wave.open(self._temp_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit = 2 bytes
            wf.setframerate(16000)
            wf.writeframes(audio_data.tobytes())
        
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