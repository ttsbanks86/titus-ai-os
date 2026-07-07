from __future__ import annotations

import os

from app.config import AppConfig
from app.tools.composio_tool import composio_status


def system_status_response(config: AppConfig) -> str:
    composio = composio_status(config)
    connected = set(composio.connected_accounts)
    auth_configs = set(composio.auth_configs)
    parts = [
        "Jarvis core is running.",
        f"LLM: {_llm_label(config)}.",
        f"Profile context: {'enabled' if config.user_profile_enabled else 'disabled'}.",
        f"Weather: {'ready' if _weather_ready(config) else 'not configured'}.",
        f"OpenClaw: {'configured' if config.openclaw_enabled and config.openclaw_command else 'not configured'}.",
        f"Composio: {'configured' if composio.configured else 'not configured'}.",
    ]
    for slug, label in (
        ("gmail", "Gmail"),
        ("googlecalendar", "Google Calendar"),
        ("googledrive", "Google Drive"),
        ("notion", "Notion"),
    ):
        if slug == "gmail" and config.gmail_credentials_path and config.gmail_token_path:
            state = "direct read-only ready"
        elif slug == "notion" and (config.notion_api_token or os.getenv("NOTION_API_TOKEN")):
            state = "direct read-only ready"
        elif slug == "googlecalendar" and config.google_calendar_enabled and config.google_calendar_credentials_path and config.google_calendar_token_path:
            state = "direct read-only ready"
        elif slug in connected:
            state = "active"
        elif slug in auth_configs:
            state = "auth config enabled, no active account visible"
        else:
            state = "not connected"
        parts.append(f"{label}: {state}.")
    return " ".join(parts)


def looks_like_status_question(text: str) -> bool:
    lowered = text.lower()
    return any(
        phrase in lowered
        for phrase in (
            "what tools are connected",
            "what tools do you have",
            "what is your status",
            "are you connected",
            "is openclaw connected",
            "is composio connected",
            "how are you set up",
        )
    )


def _llm_label(config: AppConfig) -> str:
    if not config.llm_enabled:
        return "disabled"
    if config.llm_provider == "ollama":
        return f"local Ollama model {config.llm_model}"
    if config.llm_provider == "deepseek":
        if config.llm_api_key or os.getenv("DEEPSEEK_API_KEY"):
            return f"DeepSeek {config.llm_model or 'deepseek-chat'}"
        return "DeepSeek (missing API key)"
    if config.llm_api_key:
        return f"{config.llm_provider} configured"
    return "missing API key"


def _weather_ready(config: AppConfig) -> bool:
    provider = (config.weather_provider or "").lower()
    if provider in {"wttr", "wttr.in", "auto"}:
        return True
    return bool(config.weather_provider and config.weather_api_key and config.default_location)
