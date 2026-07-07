from unittest.mock import Mock, patch

from app.config import AppConfig
from app.router import Router
from app.tools.email import EmailSummary, _clean_spoken_email_text, email_response


def test_gmail_not_configured():
    response = email_response(AppConfig(), "Jarvis, check my email")
    assert response == "Email access is not connected yet. I can add Gmail or Outlook next."


@patch("app.tools.email.GmailReadOnlyClient.from_config")
def test_gmail_configured_mock_latest(mock_from_config):
    client = Mock()
    client.latest.return_value = [
        EmailSummary(sender="sam@example.com", subject="Project update", snippet="The project is on track."),
    ]
    mock_from_config.return_value = client

    response = email_response(AppConfig(gmail_max_results=3), "Jarvis, summarize my latest emails")

    assert "Project update" in response
    assert "sam@example.com" in response
    client.latest.assert_called_once_with(max_results=3)


@patch("app.tools.email.GmailReadOnlyClient.from_config")
def test_gmail_search_email(mock_from_config):
    client = Mock()
    client.search.return_value = [
        EmailSummary(sender="recruiter@example.com", subject="Interview", snippet="Can you talk Tuesday?"),
    ]
    mock_from_config.return_value = client

    response = email_response(AppConfig(gmail_max_results=2), "Jarvis, search my email for recruiter")

    assert "Interview" in response
    client.search.assert_called_once_with("recruiter", max_results=2)


def test_search_email_intent_routes_to_email(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "logs" / "audit.jsonl",
        speech_enabled=False,
    )
    router = Router(config)

    result = router.handle("Jarvis, search my email for invoices")

    assert result.route == "email"
    assert "Email access is not connected yet" in result.response


def test_send_email_blocked_by_approval(tmp_path):
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "logs" / "audit.jsonl",
        speech_enabled=False,
    )
    router = Router(config)

    result = router.handle("Jarvis, send an email to Sam")

    assert result.route == "approval"
    assert result.intent == "approval_required"
    assert router.memory.pending_action is not None


def test_email_text_cleaning_for_voice():
    assert _clean_spoken_email_text("Hi &#39;Titus&#39; \U0001f349") == "Hi 'Titus'"
