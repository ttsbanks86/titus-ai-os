from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.config import AppConfig


READ_ONLY_TOOLKITS = {
    "gmail": ("gmail", "Gmail"),
    "googlecalendar": ("googlecalendar", "Google Calendar"),
    "googledrive": ("googledrive", "Google Drive"),
    "notion": ("notion", "Notion"),
}

WRITE_KEYWORDS = {
    "send",
    "create",
    "update",
    "edit",
    "delete",
    "remove",
    "archive",
    "trash",
    "label",
    "move",
}


@dataclass(frozen=True)
class ComposioStatus:
    configured: bool
    enabled: bool
    user_id_present: bool
    allowed_tools: tuple[str, ...]
    connected_accounts: tuple[str, ...] = ()
    auth_configs: tuple[str, ...] = ()
    error: str = ""


def composio_configured(config: AppConfig) -> bool:
    return bool(config.composio_enabled and config.composio_api_key and config.composio_user_id)


def composio_status(config: AppConfig) -> ComposioStatus:
    allowed = tuple(_normalize_tool(tool) for tool in config.composio_allowed_tools if _normalize_tool(tool))
    if not config.composio_enabled:
        return ComposioStatus(False, False, bool(config.composio_user_id), allowed)
    if not config.composio_api_key or not config.composio_user_id:
        return ComposioStatus(False, True, bool(config.composio_user_id), allowed, error="missing api key or user id")
    try:
        accounts = list_connected_toolkits(config)
        auth_configs = list_auth_config_toolkits(config)
    except Exception:
        return ComposioStatus(True, True, True, allowed, error="could not read connected accounts")
    return ComposioStatus(True, True, True, allowed, tuple(accounts), tuple(auth_configs))


def list_connected_toolkits(config: AppConfig) -> list[str]:
    client = _client(config)
    if client is None:
        return []
    accounts = client.connected_accounts.list(account_type="ALL", statuses=["ACTIVE"])
    names: list[str] = []
    for account in _iter_items(accounts):
        toolkit = getattr(account, "toolkit", None)
        slug = getattr(toolkit, "slug", None) or _dict_get(account, "toolkit.slug") or _dict_get(account, "toolkit", "slug")
        if slug:
            names.append(_normalize_tool(str(slug)))
    return sorted(set(names))


def list_auth_config_toolkits(config: AppConfig) -> list[str]:
    client = _client(config)
    if client is None or not hasattr(client, "auth_configs"):
        return []
    configs = client.auth_configs.list(limit=100)
    names: list[str] = []
    for auth_config in _iter_items(configs):
        status = str(getattr(auth_config, "status", "") or _dict_get(auth_config, "status")).upper()
        if status and status != "ENABLED":
            continue
        toolkit = getattr(auth_config, "toolkit", None)
        slug = (
            getattr(toolkit, "slug", None)
            or getattr(auth_config, "toolkit_slug", None)
            or _dict_get(auth_config, "toolkit.slug")
            or _dict_get(auth_config, "toolkit", "slug")
        )
        if slug:
            names.append(_normalize_tool(str(slug)))
    return sorted(set(names))


def read_only_response(config: AppConfig, toolkit: str, command: str) -> str:
    normalized = _normalize_tool(toolkit)
    label = READ_ONLY_TOOLKITS.get(normalized, (normalized, normalized))[1]
    if normalized not in {_normalize_tool(tool) for tool in config.composio_allowed_tools}:
        return f"{label} is not allowed through Composio yet."
    if not composio_configured(config):
        return "Composio is not connected yet. Set JARVIS_COMPOSIO_ENABLED, JARVIS_COMPOSIO_API_KEY, and JARVIS_COMPOSIO_USER_ID."
    if _looks_like_write(command):
        return f"{label} write actions require Jarvis approval first."
    try:
        connected = set(list_connected_toolkits(config))
    except Exception:
        return f"{label} access through Composio had a connection error."
    if normalized not in connected:
        try:
            auth_configs = set(list_auth_config_toolkits(config))
        except Exception:
            auth_configs = set()
        if normalized in auth_configs:
            return f"{label} has a Composio auth config, but no active connected account is visible to Jarvis yet."
        return f"{label} is not connected in Composio yet."
    return f"{label} is connected through Composio in read-only mode."


def _client(config: AppConfig) -> Any | None:
    try:
        from composio import Composio
    except Exception:
        return None
    return Composio(api_key=config.composio_api_key)


def _iter_items(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    items = getattr(value, "items", None)
    if isinstance(items, list):
        return items
    data = getattr(value, "data", None)
    if isinstance(data, list):
        return data
    if isinstance(value, dict):
        for key in ("items", "data", "connected_accounts"):
            if isinstance(value.get(key), list):
                return value[key]
    return []


def _dict_get(value: Any, *keys: str) -> Any:
    if not isinstance(value, dict):
        return None
    current: Any = value
    for key in keys:
        for part in key.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
    return current


def _normalize_tool(tool: str) -> str:
    return tool.lower().replace("_", "").replace("-", "").strip()


def _looks_like_write(command: str) -> bool:
    lowered = command.lower()
    return any(keyword in lowered for keyword in WRITE_KEYWORDS)
