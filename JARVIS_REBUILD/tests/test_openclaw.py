import subprocess
from unittest.mock import Mock, patch

from app.config import AppConfig
from app.tools.openclaw import handle_openclaw_task


def test_openclaw_not_configured_boundary():
    result = handle_openclaw_task("Help me debug this Python script", AppConfig(), "coding task")
    assert result.used is False
    assert "not configured yet" in result.response
    assert result.selection_reason == "coding task"


@patch("app.tools.openclaw.subprocess.run")
def test_openclaw_success(mock_run):
    completed = Mock()
    completed.returncode = 0
    completed.stdout = "debug summary"
    completed.stderr = ""
    mock_run.return_value = completed
    config = AppConfig(openclaw_enabled=True, openclaw_command="openclaw", openclaw_timeout_seconds=12)

    result = handle_openclaw_task("Help me debug", config, "coding task")

    assert result.used is True
    assert result.response == "debug summary"
    mock_run.assert_called_once()
    assert mock_run.call_args.kwargs["timeout"] == 12


@patch("app.tools.openclaw.subprocess.run")
def test_openclaw_timeout(mock_run):
    mock_run.side_effect = subprocess.TimeoutExpired(cmd=["openclaw"], timeout=1)
    config = AppConfig(openclaw_enabled=True, openclaw_command="openclaw", openclaw_timeout_seconds=1)

    result = handle_openclaw_task("Help me debug", config, "coding task")

    assert result.used is True
    assert result.response == "OpenClaw was routed correctly, but the local model did not finish before the timeout."
    assert result.error == "timeout"


@patch("app.tools.openclaw.subprocess.run")
def test_openclaw_nonzero_error(mock_run):
    completed = Mock()
    completed.returncode = 2
    completed.stdout = ""
    completed.stderr = "bad command"
    mock_run.return_value = completed
    config = AppConfig(openclaw_enabled=True, openclaw_command="openclaw")

    result = handle_openclaw_task("Help me debug", config, "coding task")

    assert result.used is True
    assert result.response == "OpenClaw returned an error."
    assert result.error == "bad command"


@patch("app.tools.openclaw.subprocess.run")
def test_openclaw_auth_error_is_actionable(mock_run):
    completed = Mock()
    completed.returncode = 1
    completed.stdout = ""
    completed.stderr = "Authentication failed invalid_api_key"
    mock_run.return_value = completed
    config = AppConfig(openclaw_enabled=True, openclaw_command="openclaw agent --agent main --message")

    result = handle_openclaw_task("Help me debug", config, "coding task")

    assert result.used is True
    assert "provider authentication is failing" in result.response


@patch("app.tools.openclaw.subprocess.run")
def test_openclaw_output_removes_provider_diagnostics(mock_run):
    completed = Mock()
    completed.returncode = 0
    completed.stdout = "[provider-transport-fetch] noisy\nUseful answer\n[agent] noisy"
    completed.stderr = ""
    mock_run.return_value = completed
    config = AppConfig(openclaw_enabled=True, openclaw_command="openclaw agent --agent main --message")

    result = handle_openclaw_task("Help me debug", config, "coding task")

    assert result.response == "Useful answer"
