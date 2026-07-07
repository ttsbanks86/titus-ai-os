from unittest.mock import patch

from app.config import AppConfig
from app.intents import BRIEFING, classify_intent
from app.router import Router
from app.tools.briefing import (
    BriefingSection,
    _extract_open_tasks,
    _clean_task_text,
    briefing_response,
    looks_like_briefing_request,
)


# ---------------------------------------------------------------------------
# Intent classification
# ---------------------------------------------------------------------------


def test_classify_intent_recognizes_morning_briefing_request():
    intent = classify_intent("Jarvis, give me my morning briefing")
    assert intent.name == BRIEFING


def test_classify_intent_recognizes_whats_happening_today():
    intent = classify_intent("Jarvis, what's happening today?")
    assert intent.name == BRIEFING


def test_classify_intent_recognizes_brief_me():
    intent = classify_intent("Jarvis, brief me")
    assert intent.name == BRIEFING


def test_classify_intent_recognizes_start_my_day():
    intent = classify_intent("Jarvis, start my day")
    assert intent.name == BRIEFING


def test_looks_like_briefing_request_handles_phrases():
    assert looks_like_briefing_request("what is happening today") is True
    assert looks_like_briefing_request("give me my daily briefing") is True
    assert looks_like_briefing_request("what does my day look like") is True
    assert looks_like_briefing_request("tell me a joke") is False


# ---------------------------------------------------------------------------
# Task extraction from Obsidian notes
# ---------------------------------------------------------------------------


def test_extract_open_tasks_finds_uncompleted_checkboxes():
    text = """
# 2026-07-06

- [ ] Finish Jarvis briefing tool
- [x] Ship push-to-talk fix
- [ ] Email Sam about the contract
- [ ] Review PR #42

Some other content.
"""
    tasks = _extract_open_tasks(text, limit=3)
    assert "Finish Jarvis briefing tool" in tasks
    assert "Email Sam about the contract" in tasks
    assert "Review PR #42" in tasks
    # The completed task should NOT appear
    assert all("push-to-talk" not in t for t in tasks)


def test_extract_open_tasks_respects_limit():
    text = """
- [ ] Task one
- [ ] Task two
- [ ] Task three
- [ ] Task four
- [ ] Task five
"""
    tasks = _extract_open_tasks(text, limit=3)
    assert len(tasks) == 3


def test_extract_open_tasks_handles_empty_text():
    tasks = _extract_open_tasks("", limit=3)
    assert tasks == []


def test_extract_open_tasks_ignores_completed_tasks():
    text = """
- [x] Done thing one
- [x] Done thing two
"""
    tasks = _extract_open_tasks(text, limit=3)
    assert tasks == []


def test_clean_task_text_strips_wikilinks():
    assert _clean_task_text("Review [[Project Notes]] for context") == "Review Project Notes for context"


def test_clean_task_text_strips_wikilinks_with_alias():
    assert _clean_task_text("See [[Project Notes|the project]]") == "See the project"


def test_clean_task_text_strips_bold_emphasis():
    assert _clean_task_text("Read **important** document") == "Read important document"


def test_clean_task_text_strips_italic_emphasis():
    assert _clean_task_text("Review *draft* proposal") == "Review draft proposal"


def test_clean_task_text_caps_long_text():
    long_task = "A" * 200
    cleaned = _clean_task_text(long_task)
    assert len(cleaned) <= 120
    assert cleaned.endswith("...")


# ---------------------------------------------------------------------------
# Briefing composition
# ---------------------------------------------------------------------------


def _make_config(tmp_path, **overrides) -> AppConfig:
    defaults = dict(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        obsidian_vault_path=tmp_path / "vault",
        obsidian_inbox_path=tmp_path / "vault" / "02-Daily-Notes",
        weather_provider="wttr",
        notion_api_token="ntn_test_token",
    )
    defaults.update(overrides)
    return AppConfig(**defaults)


def test_briefing_returns_greeting_and_closing_when_no_sources_available(tmp_path, monkeypatch):
    monkeypatch.delenv("NOTION_API_TOKEN", raising=False)
    monkeypatch.delenv("JARVIS_NOTION_API_TOKEN", raising=False)
    config = AppConfig(
        project_root=tmp_path,
        logs_dir=tmp_path / "logs",
        audit_log_path=tmp_path / "audit.jsonl",
        obsidian_vault_path=tmp_path / "vault",
        obsidian_inbox_path=tmp_path / "vault" / "inbox",
        weather_provider="",
        notion_api_token="",
    )
    # Mock all the source responses to return "not configured" so the briefing
    # has nothing to compose from.
    with patch("app.tools.briefing.weather_response", return_value="Weather is not configured. Set JARVIS_WEATHER_PROVIDER."):
        text = briefing_response(config)
    # No weather, no gmail, no calendar, no notion, no inbox. Should still produce
    # a polite "could not pull sources" message wrapped in greeting/closing.
    assert "Good morning" in text
    assert "could not pull any" in text.lower()
    assert "Have a focused day" in text


def test_briefing_includes_weather_when_configured(tmp_path, monkeypatch):
    config = _make_config(tmp_path)
    with patch("app.tools.briefing.weather_response", return_value="Sunny, 72 degrees."):
        text = briefing_response(config)
    assert "Weather:" in text
    assert "72 degrees" in text


def test_briefing_skips_weather_section_when_not_configured(tmp_path, monkeypatch):
    config = _make_config(tmp_path, weather_provider="")
    with patch("app.tools.briefing.weather_response", return_value="Weather is not configured. Set JARVIS_WEATHER_PROVIDER to enable it."):
        text = briefing_response(config)
    # The weather setup hint should NOT appear in the briefing.
    assert "JARVIS_WEATHER_PROVIDER" not in text
    assert "Weather:" not in text


def test_briefing_includes_email_when_gmail_configured(tmp_path, monkeypatch):
    config = _make_config(tmp_path)
    monkeypatch.setattr(
        "app.tools.briefing.GmailReadOnlyClient.from_config",
        lambda _config: _StubGmailClient(),
    )
    text = briefing_response(config)
    assert "Email:" in text
    assert "Project update" in text


def test_briefing_skips_email_when_gmail_not_configured(tmp_path, monkeypatch):
    config = _make_config(tmp_path)
    monkeypatch.setattr("app.tools.briefing.GmailReadOnlyClient.from_config", lambda _config: None)
    with patch("app.tools.briefing.weather_response", return_value="Weather is not configured."):
        text = briefing_response(config)
    assert "Email:" not in text


def test_briefing_includes_notion_when_token_configured(tmp_path, monkeypatch):
    config = _make_config(tmp_path, notion_api_token="ntn_test_token")
    monkeypatch.setattr(
        "app.tools.briefing.NotionReadOnlyClient.from_config",
        lambda _config: _StubNotionClient(),
    )
    with patch("app.tools.briefing.weather_response", return_value="Weather is not configured."):
        text = briefing_response(config)
    assert "Notion:" in text
    assert "Marketing Plan" in text


def test_briefing_includes_open_tasks_from_latest_daily_note(tmp_path):
    inbox = tmp_path / "vault" / "02-Daily-Notes"
    inbox.mkdir(parents=True)
    (inbox / "2026-07-05.md").write_text(
        "- [x] Older completed task\n- [ ] Older open task",
        encoding="utf-8",
    )
    (inbox / "2026-07-06.md").write_text(
        "# Today\n\n- [ ] Finish Jarvis briefing\n- [ ] Email Sam\n- [x] Done already\n",
        encoding="utf-8",
    )
    config = _make_config(tmp_path, obsidian_inbox_path=inbox)
    with patch("app.tools.briefing.weather_response", return_value="Weather is not configured."):
        text = briefing_response(config)
    assert "Open tasks" in text
    assert "Finish Jarvis briefing" in text
    assert "Email Sam" in text
    # Older note's tasks should NOT appear
    assert "Older open task" not in text


def test_briefing_skips_tasks_section_when_no_open_tasks(tmp_path):
    inbox = tmp_path / "vault" / "02-Daily-Notes"
    inbox.mkdir(parents=True)
    (inbox / "2026-07-06.md").write_text(
        "# Today\n\n- [x] All done\n",
        encoding="utf-8",
    )
    config = _make_config(tmp_path, obsidian_inbox_path=inbox)
    with patch("app.tools.briefing.weather_response", return_value="Weather is not configured."):
        text = briefing_response(config)
    assert "Open tasks" not in text


# ---------------------------------------------------------------------------
# Router integration
# ---------------------------------------------------------------------------


def test_router_routes_briefing_command_to_briefing_tool(tmp_path):
    config = _make_config(tmp_path)
    router = Router(config)

    with patch("app.router.briefing_response") as mocked:
        mocked.return_value = "Good morning. Weather: Sunny. Have a focused day."
        result = router.handle("Jarvis, give me my morning briefing")

    assert result.intent == BRIEFING
    assert result.route == "briefing"
    assert "Sunny" in result.response
    mocked.assert_called_once()


def test_router_does_not_route_general_chat_to_briefing(tmp_path):
    config = _make_config(tmp_path)
    router = Router(config)

    with patch("app.router.briefing_response") as mocked:
        result = router.handle("Why is the sky blue?")

    assert result.route != "briefing"
    mocked.assert_not_called()


# ---------------------------------------------------------------------------
# Test stubs
# ---------------------------------------------------------------------------


class _StubGmailClient:
    def latest(self, max_results=5):
        from app.tools.email import EmailSummary

        return [
            EmailSummary(
                sender="Sam Rivera <sam@example.com>",
                subject="Project update",
                snippet="The build is green and ready for review.",
                date="2026-07-06T10:00:00Z",
            ),
            EmailSummary(
                sender="HR <hr@example.com>",
                subject="Payroll confirmation",
                snippet="Your July payroll is confirmed.",
                date="2026-07-06T08:00:00Z",
            ),
        ]


class _StubNotionClient:
    def recent(self, max_results=5):
        from app.tools.notion import NotionPageSummary

        return [
            NotionPageSummary(
                id="page-1",
                title="Marketing Plan",
                url="https://notion.so/page-1",
                last_edited_time="2026-07-05T10:00:00Z",
            ),
            NotionPageSummary(
                id="page-2",
                title="Engineering Roadmap",
                url="https://notion.so/page-2",
                last_edited_time="2026-07-04T10:00:00Z",
            ),
        ]