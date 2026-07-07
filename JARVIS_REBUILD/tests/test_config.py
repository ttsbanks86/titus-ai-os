import os

from app.config import AppConfig, load_dotenv


def test_push_to_talk_defaults():
    config = AppConfig()
    assert config.push_to_talk_key == "right ctrl"
    assert config.min_record_seconds > 0
    assert config.sample_rate == 16000
    assert config.record_end_padding_ms == 500
    assert config.transcribe_provider == "speechrecognition"
    assert config.openclaw_timeout_seconds == 30
    assert config.default_browser == "chrome"
    assert config.google_calendar_enabled is False
    assert config.tts_engine == "edge-tts"
    assert config.tts_voice == "en-GB-RyanNeural"
    assert config.tts_rate == "+10%"
    assert config.tts_pitch == "-20Hz"
    assert config.obsidian_inbox_path.name == "02-Daily-Notes"
    assert config.file_editing_enabled is True
    assert config.debug_audio_enabled is False


def test_dotenv_overrides_stale_process_env(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("JARVIS_COMPOSIO_ENABLED=true\n", encoding="utf-8")
    monkeypatch.setenv("JARVIS_COMPOSIO_ENABLED", "false")

    load_dotenv(env_file)

    assert os.environ["JARVIS_COMPOSIO_ENABLED"] == "true"
