import json
from unittest.mock import patch

from app.config import AppConfig
from app.router import Router


def make_router(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "logs" / "audit.jsonl",
        speech_enabled=False,
    )
    return Router(config), config


def test_route_capabilities(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Jarvis, what are your capabilities?")
    assert result.route == "capabilities"
    assert "OpenClaw adapter" in result.response


def test_weather_fallback(tmp_path):
    router, _ = make_router(tmp_path)
    with patch("app.tools.weather.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "nearest_area": [{"areaName": [{"value": "Seattle"}], "region": [{"value": "Washington"}]}],
            "current_condition": [
                {"temp_F": "63", "FeelsLikeF": "63", "weatherDesc": [{"value": "Clear"}]}
            ],
        }
        result = router.handle("Jarvis, what's the weather today?")
        assert result.route == "weather"
        assert "Right now in Seattle, Washington" in result.response
        assert result.used_openclaw is False


def test_stop_command(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Stop")
    assert result.route == "system"
    assert result.intent == "stop"
    assert result.response == "Stopped."


def test_exit_command(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Exit")
    assert result.route == "system"
    assert result.intent == "exit"
    assert result.should_exit is True


def test_openclaw_not_used_for_basic_commands(tmp_path):
    router, _ = make_router(tmp_path)
    for command in ["Hello Jarvis", "Jarvis, what's the weather today?", "Jarvis, what are your capabilities?"]:
        result = router.handle(command)
        assert result.route != "openclaw"
        assert result.used_openclaw is False


def test_openclaw_route_is_restricted_to_coding_task(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Help me debug this Python script")
    assert result.route == "openclaw"
    assert result.used_openclaw is False
    assert "not configured yet" in result.response
    assert "selected OpenClaw boundary" in result.reason


def test_openclaw_delete_files_requires_approval(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Use OpenClaw to delete files")
    assert result.route == "approval"
    assert result.intent == "approval_required"
    assert result.used_openclaw is False


def test_browser_command_routes_safely(tmp_path):
    router, _ = make_router(tmp_path)
    with patch("app.tools.browser.subprocess.Popen"):
        result = router.handle("Jarvis, open Chrome")
        assert result.route == "browser"
        assert result.used_openclaw is False
        assert "Opening" in result.response


def test_browser_route_for_openclaw_open_chrome_stays_local(tmp_path):
    router, _ = make_router(tmp_path)
    with patch("app.tools.browser.subprocess.Popen"):
        result = router.handle("Jarvis, use OpenClaw to open Chrome")
        assert result.route == "browser"
        assert result.used_openclaw is False


def test_today_schedule_not_configured_response(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Jarvis, what am I working on today?")
    assert result.route == "calendar"
    assert result.response == "Calendar access is not connected yet. I can add Google Calendar next."


def test_system_status_question_stays_local(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Jarvis, what tools are connected?")
    assert result.route == "system_status"
    assert "Jarvis core is running" in result.response
    assert result.used_openclaw is False


def test_schedule_question_does_not_require_update_approval(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Jarvis, what is on my schedule today?")
    assert result.route == "calendar"
    assert result.intent == "calendar"


def test_email_placeholder(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Jarvis, check my email")
    assert result.route == "email"
    assert "Email access is not connected yet" in result.response


def test_weather_still_routes_locally(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Jarvis, what's the weather today?")
    assert result.route == "weather"
    assert result.used_openclaw is False


def test_gmail_still_routes_read_only(tmp_path):
    router, _ = make_router(tmp_path)
    result = router.handle("Jarvis, summarize my latest emails")
    assert result.route == "email"
    assert result.used_openclaw is False


def test_noise_is_silent_and_logged(tmp_path):
    router, config = make_router(tmp_path)
    result = router.handle("I'll see you in the next one.")
    assert result.rejected is True
    assert result.speak is False
    assert result.response == ""
    records = [json.loads(line) for line in config.audit_log_path.read_text(encoding="utf-8").splitlines()]
    assert records[-1]["result"]["route"] == "noise_rejection"


def test_self_speech_is_rejected(tmp_path):
    router, _ = make_router(tmp_path)
    first = router.handle("Hello Jarvis")
    second = router.handle(first.response)
    assert second.intent == "self_speech"
    assert second.rejected is True


def test_command_audit_logs(tmp_path):
    router, config = make_router(tmp_path)
    router.handle("Hello Jarvis")
    assert config.audit_log_path.exists()
    record = json.loads(config.audit_log_path.read_text(encoding="utf-8").splitlines()[-1])
    assert record["source"] == "user"
    assert record["raw_text"] == "Hello Jarvis"
    assert record["result"]["route"] == "greeting"


def test_command_audit_logs_metadata(tmp_path):
    router, config = make_router(tmp_path)
    router.handle("Hello Jarvis", source="microphone", metadata={"audio_path": "debug.wav"})
    record = json.loads(config.audit_log_path.read_text(encoding="utf-8").splitlines()[-1])
    assert record["source"] == "microphone"
    assert record["metadata"]["audio_path"] == "debug.wav"
