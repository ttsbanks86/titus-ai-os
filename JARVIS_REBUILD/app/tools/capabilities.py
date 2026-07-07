from __future__ import annotations

from app.config import AppConfig


def capabilities_response(config: AppConfig | None = None) -> str:
    base = (
        "I can answer core Jarvis commands, open or search the browser, search Titus's Obsidian vault read-only, "
        "report weather when configured, check email read-only, search Notion read-only when configured, "
        "prepare read-only calendar access, give a daily briefing combining connected sources, "
        "create files inside the approved workspace, open and close apps on the computer, "
        "list running apps, take screenshots, create folders on the desktop, list files, read files, "
        "route coding tasks through the safe OpenClaw adapter boundary, and protect risky "
        "actions with approval"
    )
    if config is None:
        return base + "."

    extras: list[str] = []
    if config.llm_enabled and (config.llm_api_key or config.llm_provider == "ollama"):
        extras.append("answer general questions through the connected LLM")
    if config.user_profile_enabled:
        extras.append("use approved Titus profile notes for more natural context")
    if config.connector_mode == "composio" and config.composio_enabled:
        extras.append("use Composio as the external app connector when active accounts are visible")
    if extras:
        return base + ". I can also " + "; ".join(extras) + "."
    return base + "."
