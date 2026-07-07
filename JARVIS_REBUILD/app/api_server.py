from __future__ import annotations

import json
import os
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from app.config import AppConfig
from app.router import Router
from app.security import redact_secrets
from app.tools.composio_tool import composio_status


def run_api_server(config: AppConfig, router: Router) -> None:
    # The Mission Control API key gates /command, /approval, /audit/latest.
    # /health stays open so Mission Control can probe whether Jarvis is alive
    # without needing to know the key. The key is read from
    # JARVIS_MISSION_CONTROL_API_KEY (system env var or .env). If the key is
    # empty, enforcement is disabled (localhost-only development mode).
    expected_key = (config.mission_control_api_key or "").strip()

    class JarvisHandler(BaseHTTPRequestHandler):
        server_version = "JarvisLocalAPI/1.0"

        def do_GET(self) -> None:
            path = urlparse(self.path).path
            if path == "/health":
                self._json({"ok": True, "service": "jarvis", "mode": "local"})
                return
            # /status, /audit/latest require the key when one is configured.
            if path == "/status":
                if not self._authorized():
                    self._json({"error": "unauthorized"}, HTTPStatus.UNAUTHORIZED)
                    return
                self._json(jarvis_status(config, router))
                return
            if path == "/audit/latest":
                if not self._authorized():
                    self._json({"error": "unauthorized"}, HTTPStatus.UNAUTHORIZED)
                    return
                self._json({"latest": latest_audit(config.audit_log_path)})
                return
            self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)

        def do_POST(self) -> None:
            path = urlparse(self.path).path
            body = self._body()
            if path == "/command":
                if not self._authorized():
                    self._json({"error": "unauthorized"}, HTTPStatus.UNAUTHORIZED)
                    return
                command = str(body.get("command") or "").strip()
                if not command:
                    self._json({"error": "command is required"}, HTTPStatus.BAD_REQUEST)
                    return
                result = router.handle(command, source="mission_control", metadata={"api": "local"})
                self._json({"result": redact_secrets(asdict(result)), "status": jarvis_status(config, router)})
                return
            if path == "/approval":
                if not self._authorized():
                    self._json({"error": "unauthorized"}, HTTPStatus.UNAUTHORIZED)
                    return
                decision = str(body.get("decision") or "").strip().lower()
                if decision not in {"approve", "cancel"}:
                    self._json({"error": "decision must be approve or cancel"}, HTTPStatus.BAD_REQUEST)
                    return
                text = "yes, approve" if decision == "approve" else "cancel"
                result = router.handle(text, source="mission_control", metadata={"api": "approval"})
                self._json({"result": redact_secrets(asdict(result)), "status": jarvis_status(config, router)})
                return
            self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)

        def _authorized(self) -> bool:
            # If no key is configured, allow all requests (localhost-only dev mode).
            if not expected_key:
                return True
            supplied = self.headers.get("X-Jarvis-Key") or self.headers.get("x-jarvis-key") or ""
            return supplied.strip() == expected_key

        def log_message(self, _format: str, *_args: Any) -> None:
            return

        def _body(self) -> dict[str, Any]:
            length = int(self.headers.get("content-length", "0") or "0")
            if length <= 0:
                return {}
            raw = self.rfile.read(length).decode("utf-8", errors="ignore")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                return {}
            return data if isinstance(data, dict) else {}

        def _json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
            data = json.dumps(redact_secrets(payload), ensure_ascii=True).encode("utf-8")
            self.send_response(int(status))
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    server = ThreadingHTTPServer((config.api_host, config.api_port), JarvisHandler)
    print(f"Jarvis local API listening on http://{config.api_host}:{config.api_port}", flush=True)
    server.serve_forever()


def jarvis_status(config: AppConfig, router: Router) -> dict[str, Any]:
    pending = router.memory.pending_action
    latest = latest_audit(config.audit_log_path)
    last_result = latest.get("result", {}) if isinstance(latest, dict) else {}
    composio = composio_status(config)
    composio_connected = set(composio.connected_accounts)
    composio_auth_configs = set(composio.auth_configs)
    notion_direct_ready = bool(config.notion_api_token or os.getenv("NOTION_API_TOKEN"))
    gmail_connected = "gmail" in composio_connected or bool(config.gmail_credentials_path and config.gmail_token_path)
    calendar_connected = "googlecalendar" in composio_connected or config.google_calendar_enabled
    drive_connected = "googledrive" in composio_connected
    notion_connected = "notion" in composio_connected or notion_direct_ready
    tool_status = {
        "browser": "ready",
        "weather": "ready" if _weather_ready(config) else "not configured",
        "gmail": "direct read-only ready" if bool(config.gmail_credentials_path and config.gmail_token_path) else _connector_status("gmail", gmail_connected, composio_auth_configs, composio),
        "google_calendar": "direct read-only ready" if bool(config.google_calendar_enabled and config.google_calendar_credentials_path and config.google_calendar_token_path) else _connector_status("googlecalendar", calendar_connected, composio_auth_configs, composio),
        "google_drive": _connector_status("googledrive", drive_connected, composio_auth_configs, composio),
        "notion": "direct read-only ready" if notion_direct_ready else _connector_status("notion", notion_connected, composio_auth_configs, composio),
        "obsidian": "ready" if config.obsidian_vault_path.exists() else "not configured",
        "openclaw": "ready" if config.openclaw_enabled and bool(config.openclaw_command) else "not configured",
        "composio": "configured" if composio.configured else "not configured",
        "llm": _llm_status(config),
        "profile": "ready" if config.user_profile_enabled else "disabled",
        "mission_control_api_key": "enforced" if config.mission_control_api_key else "open (localhost dev mode)",
    }
    return {
        "health": "ok",
        "mode": "voice_local",
        "connector_mode": config.connector_mode,
        "connected_tools": {
            "browser": True,
            "weather": _weather_ready(config),
            "gmail": gmail_connected,
            "google_calendar": calendar_connected,
            "google_drive": drive_connected,
            "notion": notion_connected,
            "obsidian": config.obsidian_vault_path.exists(),
            "openclaw": config.openclaw_enabled and bool(config.openclaw_command),
            "composio": composio.configured,
            "llm": config.llm_enabled and _llm_ready(config),
            "profile": config.user_profile_enabled,
        },
        "tool_status": tool_status,
        "pending_approval": asdict(pending) if pending else None,
        "last_response": last_result.get("response", ""),
        "latest_command": latest,
    }


def _connector_status(toolkit: str, connected: bool, auth_configs: set[str], composio: Any) -> str:
    if connected:
        return "ready"
    if toolkit in auth_configs:
        return "auth config enabled, no active account visible"
    if composio.enabled and not composio.configured:
        return "missing Composio config"
    return "not configured"


def _llm_status(config: AppConfig) -> str:
    if not config.llm_enabled:
        return "disabled"
    if config.llm_provider == "ollama":
        return "configured for Ollama"
    if config.llm_provider == "deepseek":
        if config.llm_api_key or os.getenv("DEEPSEEK_API_KEY"):
            return f"configured for DeepSeek ({config.llm_model or 'deepseek-chat'})"
        return "DeepSeek (missing api key)"
    if config.llm_api_key:
        return f"configured for {config.llm_provider}"
    return "missing api key"


def _llm_ready(config: AppConfig) -> bool:
    if not config.llm_enabled:
        return False
    if config.llm_provider == "ollama":
        return True
    if config.llm_provider == "deepseek":
        return bool(config.llm_api_key or os.getenv("DEEPSEEK_API_KEY"))
    return bool(config.llm_api_key)


def _weather_ready(config: AppConfig) -> bool:
    provider = (config.weather_provider or "").lower()
    if provider in {"wttr", "wttr.in", "auto"}:
        return True
    return bool(config.weather_provider and config.weather_api_key and config.default_location)


def latest_audit(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        lines = [line for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()]
    except OSError:
        return {}
    if not lines:
        return {}
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError:
        return {}
