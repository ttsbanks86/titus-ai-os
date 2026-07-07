from pathlib import Path
from unittest.mock import Mock, patch

from app.voice.transcribe import transcribe_audio_result


@patch("app.voice.transcribe._transcribe_speechrecognition")
def test_speechrecognition_provider(mock_speech):
    mock_speech.return_value = "hello jarvis"

    result = transcribe_audio_result(Path("test.wav"), provider="speechrecognition")

    assert result.text == "hello jarvis"
    assert result.provider_used == "speechrecognition"
    assert result.fallback_used is False


@patch("app.voice.transcribe._transcribe_speechrecognition")
@patch("app.voice.transcribe._try_transcribe_whisper")
def test_whisper_falls_back_to_speechrecognition(mock_whisper, mock_speech):
    mock_whisper.return_value = None
    mock_speech.return_value = "fallback transcript"

    result = transcribe_audio_result(Path("test.wav"), provider="whisper")

    assert result.text == "fallback transcript"
    assert result.provider_used == "speechrecognition"
    assert result.requested_provider == "whisper"
    assert result.fallback_used is True


@patch("app.voice.transcribe._try_transcribe_whisper")
def test_whisper_provider_when_available(mock_whisper):
    mock_whisper.return_value = "whisper transcript"

    result = transcribe_audio_result(Path("test.wav"), provider="whisper")

    assert result.text == "whisper transcript"
    assert result.provider_used == "whisper"
    assert result.fallback_used is False
