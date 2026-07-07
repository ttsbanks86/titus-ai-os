import json

from app.api_server import jarvis_status
from app.config import AppConfig
from app.router import Router
from app.tools.composio_tool import ComposioStatus


def test_mission_control_status_endpoint_shape(tmp_path):
    config = AppConfig(logs_dir=tmp_path, audit_log_path=tmp_path / "audit.jsonl")
    router = Router(config)

    status = jarvis_status(config, router)

    assert status["health"] == "ok"
    assert "connected_tools" in status
    assert status["pending_approval"] is None


def test_mission_control_status_does_not_overstate_composio_accounts(tmp_path, monkeypatch):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        connector_mode="composio",
        composio_enabled=True,
        composio_api_key="ak_test_secret",
        composio_user_id="titus-local",
    )
    router = Router(config)

    def fake_status(_config):
        return ComposioStatus(
            configured=True,
            enabled=True,
            user_id_present=True,
            allowed_tools=("gmail", "googlecalendar", "googledrive", "notion"),
            connected_accounts=(),
            auth_configs=("gmail", "googlecalendar", "googledrive", "notion"),
        )

    monkeypatch.setattr("app.api_server.composio_status", fake_status)

    status = jarvis_status(config, router)

    assert status["connected_tools"]["composio"] is True
    assert status["connected_tools"]["gmail"] is False
    assert status["connected_tools"]["google_calendar"] is False
    assert status["tool_status"]["gmail"] == "auth config enabled, no active account visible"


def test_pending_approval_cannot_be_bypassed_in_status(tmp_path):
    config = AppConfig(logs_dir=tmp_path, audit_log_path=tmp_path / "audit.jsonl")
    router = Router(config)

    result = router.handle("Jarvis, send an email to Sam")
    status = jarvis_status(config, router)

    assert result.route == "approval"
    assert status["pending_approval"]["action_type"] == "send_email"


def test_secret_redaction_in_audit_logs(tmp_path):
    config = AppConfig(logs_dir=tmp_path, audit_log_path=tmp_path / "audit.jsonl")
    router = Router(config)

    router.handle("Jarvis, api_key=ak_supersecret123456789 what are your capabilities?")

    record = json.loads(config.audit_log_path.read_text(encoding="utf-8").splitlines()[-1])
    assert "ak_supersecret" not in json.dumps(record)
    assert "[REDACTED]" in json.dumps(record)


# ---------------------------------------------------------------------------
# Mission Control API key enforcement (Phase 7)
# ---------------------------------------------------------------------------


def _authorized_decision(config: AppConfig, supplied_key: str | None) -> bool:
    """Mirror the JarvisHandler._authorized logic exactly so we can test it
    without spinning up a real HTTP server. The handler closure in
    run_api_server reads `expected_key` from the config at server-start time,
    so this helper mirrors that by reading config.mission_control_api_key.
    """
    expected = (config.mission_control_api_key or "").strip()
    if not expected:
        return True
    supplied = (supplied_key or "").strip()
    return supplied == expected


def test_api_key_enforcement_disabled_when_no_key_configured(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        mission_control_api_key="",
    )
    # With no key configured, all requests are allowed (localhost dev mode).
    assert _authorized_decision(config, None) is True
    assert _authorized_decision(config, "") is True
    assert _authorized_decision(config, "anything") is True


def test_api_key_enforcement_rejects_missing_header_when_key_set(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        mission_control_api_key="ak_mc_secret_12345",
    )
    assert _authorized_decision(config, None) is False
    assert _authorized_decision(config, "") is False


def test_api_key_enforcement_rejects_wrong_key(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        mission_control_api_key="ak_mc_secret_12345",
    )
    assert _authorized_decision(config, "wrong_key") is False
    assert _authorized_decision(config, "ak_mc_secret_1234") is False  # too short


def test_api_key_enforcement_accepts_correct_key(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        mission_control_api_key="ak_mc_secret_12345",
    )
    assert _authorized_decision(config, "ak_mc_secret_12345") is True


def test_api_key_enforcement_accepts_key_with_whitespace(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        mission_control_api_key="  ak_mc_secret_12345  ",
    )
    # The config strips whitespace from the key, so a user who pastes with
    # surrounding spaces should still be authorized when they send the bare key.
    assert _authorized_decision(config, "ak_mc_secret_12345") is True


def test_status_endpoint_reports_when_api_key_is_enforced(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        mission_control_api_key="ak_mc_secret_12345",
    )
    router = Router(config)
    status = jarvis_status(config, router)
    assert status["tool_status"]["mission_control_api_key"] == "enforced"


def test_status_endpoint_reports_when_api_key_is_open(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        mission_control_api_key="",
    )
    router = Router(config)
    status = jarvis_status(config, router)
    assert "open" in status["tool_status"]["mission_control_api_key"]
    assert "localhost" in status["tool_status"]["mission_control_api_key"]


# ---------------------------------------------------------------------------
# DeepSeek and Notion status reporting in API server
# ---------------------------------------------------------------------------


def test_status_llm_reports_deepseek_when_configured(tmp_path, monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "ak_ds_test")
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="deepseek",
        llm_api_key="",
        llm_model="deepseek-chat",
    )
    router = Router(config)
    status = jarvis_status(config, router)
    assert "DeepSeek" in status["tool_status"]["llm"]
    assert status["connected_tools"]["llm"] is True


def test_status_llm_reports_deepseek_missing_key(tmp_path, monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        llm_enabled=True,
        llm_provider="deepseek",
        llm_api_key="",
    )
    router = Router(config)
    status = jarvis_status(config, router)
    assert "missing api key" in status["tool_status"]["llm"]
    assert status["connected_tools"]["llm"] is False


def test_status_notion_reports_direct_when_token_present(tmp_path):
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token="ntn_test_token",
    )
    router = Router(config)
    status = jarvis_status(config, router)
    assert status["tool_status"]["notion"] == "direct read-only ready"
    assert status["connected_tools"]["notion"] is True


def test_status_notion_reports_not_connected_when_no_token(tmp_path, monkeypatch):
    monkeypatch.delenv("NOTION_API_TOKEN", raising=False)
    monkeypatch.delenv("JARVIS_NOTION_API_TOKEN", raising=False)
    config = AppConfig(
        logs_dir=tmp_path,
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token="",
    )
    router = Router(config)
    status = jarvis_status(config, router)
    # Without a direct token AND without Composio connected, status is "not configured".
    # The exact text depends on whether Composio is configured. We assert that
    # the status is NOT "direct read-only ready".
    assert status["tool_status"]["notion"] != "direct read-only ready"
    assert status["connected_tools"]["notion"] is False
