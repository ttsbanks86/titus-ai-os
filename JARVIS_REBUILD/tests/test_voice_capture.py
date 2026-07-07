from app.voice.capture import MicrophoneDevice, ShortRecordingError, format_microphones


def test_format_microphones_empty():
    assert format_microphones([]) == "No input microphones were detected."


def test_format_microphones_marks_default():
    text = format_microphones(
        [
            MicrophoneDevice(index=2, name="USB Mic", channels=1, sample_rate=48000, is_default=True),
        ]
    )
    assert "[2] USB Mic" in text
    assert "48000 Hz default" in text


def test_short_recording_error_message():
    error = ShortRecordingError(0.1, 0.35)
    assert error.duration_seconds == 0.1
    assert error.min_seconds == 0.35
    assert "too short" in str(error)
