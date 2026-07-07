from __future__ import annotations

import os

from app.config import AppConfig
from app.tools.composio_tool import READ_ONLY_TOOLKITS, composio_status


def doctor_report(config: AppConfig) -> tuple[int, str]:
    lines = ["Jarvis doctor"]
    lines.append(f"Connector mode: {config.connector_mode}")
    lines.append(f"LLM enabled: {_yes_no(config.llm_enabled)}")
    lines.append(f"LLM provider: {config.llm_provider}")
    if config.llm_provider == "ollama":
        lines.append("LLM key present: not required for Ollama")
    elif config.llm_provider == "deepseek":
        deepseek_key = config.llm_api_key or os.getenv("DEEPSEEK_API_KEY", "")
        lines.append(f"LLM key present: {_yes_no(bool(deepseek_key))}")
    else:
        lines.append(f"LLM key present: {_yes_no(bool(config.llm_api_key))}")
    lines.append(f"Titus profile enabled: {_yes_no(config.user_profile_enabled)}")
    lines.append(f"Direct Gmail read-only configured: {_yes_no(bool(config.gmail_credentials_path and config.gmail_token_path))}")
    lines.append(
        "Direct Notion read-only configured: "
        f"{_yes_no(bool(config.notion_api_token or os.getenv('NOTION_API_TOKEN')))}"
    )
    lines.append(
        "Direct Google Calendar read-only configured: "
        f"{_yes_no(bool(config.google_calendar_enabled and config.google_calendar_credentials_path and config.google_calendar_token_path))}"
    )
    lines.append(f"Composio enabled: {_yes_no(config.composio_enabled)}")
    lines.append(f"Composio API key present: {_yes_no(bool(config.composio_api_key))}")
    lines.append(f"Composio user id present: {_yes_no(bool(config.composio_user_id))}")
    lines.append(f"Composio allowed tools: {', '.join(config.composio_allowed_tools) or '(none)'}")

    status = composio_status(config)
    lines.append(f"Composio configured: {_yes_no(status.configured)}")
    if status.error:
        lines.append(f"Composio status note: {status.error}")

    connected = set(status.connected_accounts)
    auth_configs = set(status.auth_configs)
    for slug, label in READ_ONLY_TOOLKITS.values():
        if not status.configured:
            state = "not checked"
        elif slug in connected:
            state = "connected account active"
        elif slug in auth_configs:
            state = "auth config enabled, no active connected account visible"
        else:
            state = "not configured in this project"
        lines.append(f"{label}: {state}")

    exit_code = 0 if status.configured else 1
    return exit_code, "\n".join(lines)


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"
