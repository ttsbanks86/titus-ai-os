from unittest.mock import Mock, patch

from app.config import AppConfig
from app.intents import classify_intent, NOTION
from app.router import Router
from app.tools.notion import (
    NOT_CONNECTED,
    NotionPageSummary,
    NotionReadOnlyClient,
    notion_response,
)


# ---------------------------------------------------------------------------
# Intent classification for Notion
# ---------------------------------------------------------------------------


def test_classify_intent_recovers_search_notion_phrase():
    intent = classify_intent("Jarvis, search Notion for project notes")
    assert intent.name == NOTION


def test_classify_intent_recovers_read_my_notion_page():
    intent = classify_intent("Jarvis, read my Notion page about marketing")
    assert intent.name == NOTION


def test_classify_intent_recovers_recent_notion_pages():
    intent = classify_intent("Jarvis, show me my recent Notion pages")
    assert intent.name == NOTION


def test_classify_intent_recovers_notion_page_about():
    intent = classify_intent("Jarvis, find my Notion page about Q3 goals")
    assert intent.name == NOTION


# ---------------------------------------------------------------------------
# notion_response — direct token path
# ---------------------------------------------------------------------------


def _config_with_notion_token(tmp_path, token: str = "ntn_test_token") -> AppConfig:
    return AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token=token,
        obsidian_vault_path=tmp_path / "vault",
    )


def test_notion_response_says_not_connected_when_no_token(tmp_path, monkeypatch):
    monkeypatch.delenv("NOTION_API_TOKEN", raising=False)
    monkeypatch.delenv("JARVIS_NOTION_API_TOKEN", raising=False)
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token="",
        obsidian_vault_path=tmp_path / "vault",
    )
    result = notion_response(config, "Jarvis, search Notion for project notes")
    assert "not connected" in result.lower()


def test_notion_response_search_returns_formatted_titles(tmp_path):
    config = _config_with_notion_token(tmp_path)
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "results": [
            {
                "object": "page",
                "id": "page-1",
                "url": "https://notion.so/page-1",
                "last_edited_time": "2026-07-01T10:00:00.000Z",
                "properties": {
                    "Name": {
                        "type": "title",
                        "title": [{"plain_text": "Q3 Marketing Plan"}],
                    }
                },
            },
            {
                "object": "page",
                "id": "page-2",
                "url": "https://notion.so/page-2",
                "last_edited_time": "2026-07-02T11:00:00.000Z",
                "properties": {
                    "Title": {
                        "type": "title",
                        "title": [{"plain_text": "Engineering Roadmap"}],
                    }
                },
            },
        ]
    }
    with patch("app.tools.notion.requests.post", return_value=response) as post:
        result = notion_response(config, "Jarvis, search Notion for marketing")

    assert "Q3 Marketing Plan" in result
    assert "Engineering Roadmap" in result
    assert post.call_args.args[0].endswith("/search")
    assert post.call_args.kwargs["headers"]["Notion-Version"] == "2022-06-28"
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer ntn_test_token"
    # The query should be extracted from the command
    payload = post.call_args.kwargs["json"]
    assert payload["query"] == "marketing"


def test_notion_response_recent_pages_uses_descending_sort(tmp_path):
    config = _config_with_notion_token(tmp_path)
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "results": [
            {
                "object": "page",
                "id": "page-1",
                "url": "https://notion.so/page-1",
                "last_edited_time": "2026-07-03T10:00:00.000Z",
                "properties": {
                    "Name": {
                        "type": "title",
                        "title": [{"plain_text": "Recently edited"}],
                    }
                },
            }
        ]
    }
    with patch("app.tools.notion.requests.post", return_value=response) as post:
        result = notion_response(config, "Jarvis, show me my recent Notion pages")

    assert "Recently edited" in result
    payload = post.call_args.kwargs["json"]
    assert payload["query"] == ""
    assert payload["sort"]["direction"] == "descending"
    assert payload["sort"]["timestamp"] == "last_edited_time"


def test_notion_response_handles_empty_results(tmp_path):
    config = _config_with_notion_token(tmp_path)
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"results": []}

    with patch("app.tools.notion.requests.post", return_value=response):
        result = notion_response(config, "Jarvis, search Notion for nonexistent topic")

    assert "did not find" in result.lower()


def test_notion_response_handles_request_exception(tmp_path):
    config = _config_with_notion_token(tmp_path)
    import requests as _requests

    with patch("app.tools.notion.requests.post", side_effect=_requests.RequestException("network down")):
        result = notion_response(config, "Jarvis, search Notion for project notes")

    assert "network error" in result.lower()


def test_notion_response_blocks_write_actions(tmp_path):
    config = _config_with_notion_token(tmp_path)
    result = notion_response(config, "Jarvis, create a new Notion page about lunch")
    assert "approval" in result.lower()
    assert "write" in result.lower()


def test_notion_response_does_not_expose_token_in_error(tmp_path):
    config = _config_with_notion_token(tmp_path, token="ntn_secret_value_123")
    response = Mock()
    response.status_code = 401
    response.json.return_value = {"message": "Invalid token ntn_secret_value_123"}

    with patch("app.tools.notion.requests.post", return_value=response):
        result = notion_response(config, "Jarvis, search Notion for marketing")

    # The function catches non-2xx via raise_for_status -> RequestException path
    # OR via the generic Exception path. Either way, no token leak.
    assert "ntn_secret_value_123" not in result


# ---------------------------------------------------------------------------
# NotionReadOnlyClient
# ---------------------------------------------------------------------------


def test_notion_client_from_config_returns_none_when_no_token(tmp_path, monkeypatch):
    monkeypatch.delenv("NOTION_API_TOKEN", raising=False)
    monkeypatch.delenv("JARVIS_NOTION_API_TOKEN", raising=False)
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token="",
        obsidian_vault_path=tmp_path / "vault",
    )
    assert NotionReadOnlyClient.from_config(config) is None


def test_notion_client_from_config_returns_client_when_token_present(tmp_path):
    config = _config_with_notion_token(tmp_path)
    client = NotionReadOnlyClient.from_config(config)
    assert client is not None
    assert client.api_token == "ntn_test_token"


def test_notion_client_search_calls_search_endpoint(tmp_path):
    client = NotionReadOnlyClient("ntn_test_token")
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"results": []}

    with patch("app.tools.notion.requests.post", return_value=response) as post:
        client.search("marketing")

    assert post.call_args.args[0].endswith("/search")
    assert post.call_args.kwargs["json"]["query"] == "marketing"


# ---------------------------------------------------------------------------
# Router integration — Notion route fires for Notion commands
# ---------------------------------------------------------------------------


def test_router_routes_notion_command_to_notion_tool(tmp_path):
    config = _config_with_notion_token(tmp_path)
    router = Router(config)

    with patch("app.router.notion_response") as mocked:
        mocked.return_value = "From the recently edited pages: Marketing Plan."
        result = router.handle("Jarvis, show me my recent Notion pages")

    assert result.intent == NOTION
    assert result.route == "notion"
    assert "Marketing Plan" in result.response
    mocked.assert_called_once()


def test_router_does_not_route_general_chat_to_notion(tmp_path):
    config = _config_with_notion_token(tmp_path)
    router = Router(config)

    with patch("app.router.notion_response") as mocked:
        result = router.handle("Why is the sky blue?")

    assert result.route != "notion"
    mocked.assert_not_called()


def test_router_notion_write_command_blocked_before_api_call(tmp_path):
    config = _config_with_notion_token(tmp_path)
    router = Router(config)

    # "create a Notion page" looks like a write, should be blocked at the tool layer.
    result = router.handle("Jarvis, create a Notion page about lunch plans")
    assert result.route == "notion"
    assert "approval" in result.response.lower()


# ---------------------------------------------------------------------------
# Status and doctor reflect Notion direct readiness
# ---------------------------------------------------------------------------


def test_status_reports_notion_direct_read_only_ready(tmp_path):
    from app.tools.status import system_status_response

    config = _config_with_notion_token(tmp_path)
    status = system_status_response(config)
    assert "Notion: direct read-only ready" in status


def test_status_reports_notion_not_connected_when_no_token(tmp_path, monkeypatch):
    from app.tools.status import system_status_response

    monkeypatch.delenv("NOTION_API_TOKEN", raising=False)
    monkeypatch.delenv("JARVIS_NOTION_API_TOKEN", raising=False)
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token="",
        obsidian_vault_path=tmp_path / "vault",
    )
    status = system_status_response(config)
    assert "Notion: not connected" in status


def test_doctor_reports_notion_direct_configured(tmp_path):
    from app.doctor import doctor_report

    config = _config_with_notion_token(tmp_path)
    _, report = doctor_report(config)
    assert "Direct Notion read-only configured: yes" in report


def test_doctor_reports_notion_not_configured_when_no_token(tmp_path, monkeypatch):
    from app.doctor import doctor_report

    monkeypatch.delenv("NOTION_API_TOKEN", raising=False)
    monkeypatch.delenv("JARVIS_NOTION_API_TOKEN", raising=False)
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token="",
        obsidian_vault_path=tmp_path / "vault",
    )
    _, report = doctor_report(config)
    assert "Direct Notion read-only configured: no" in report


# ---------------------------------------------------------------------------
# Env var fallback: NOTION_API_TOKEN read from env if config field is empty
# ---------------------------------------------------------------------------


def test_notion_response_uses_env_token_when_config_empty(tmp_path, monkeypatch):
    monkeypatch.setenv("NOTION_API_TOKEN", "ntn_env_fallback_token")
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        notion_api_token="",
        obsidian_vault_path=tmp_path / "vault",
    )
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "results": [
            {
                "object": "page",
                "id": "page-1",
                "url": "https://notion.so/page-1",
                "properties": {
                    "Name": {"type": "title", "title": [{"plain_text": "Env page"}]}
                },
            }
        ]
    }
    with patch("app.tools.notion.requests.post", return_value=response) as post:
        result = notion_response(config, "Jarvis, search Notion for env")

    assert "Env page" in result
    assert post.call_args.kwargs["headers"]["Authorization"] == "Bearer ntn_env_fallback_token"