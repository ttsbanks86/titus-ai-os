from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any

from app.config import AppConfig
from app.tools.composio_tool import read_only_response


NOT_CONNECTED = "Calendar access is not connected yet. I can add Google Calendar next."
READ_ONLY_SCOPE = ["https://www.googleapis.com/auth/calendar.readonly"]


@dataclass(frozen=True)
class CalendarEvent:
    summary: str
    start: str
    end: str = ""
    location: str = ""


def calendar_response(config: AppConfig, command: str) -> str:
    # Try Composio first (if it has an active connected account)
    if config.connector_mode == "composio":
        composio_message = read_only_response(config, "googlecalendar", command)
        if "no active connected account is visible" not in composio_message:
            return composio_message
    # Try direct Google Calendar OAuth (same pattern as Gmail direct adapter)
    client = GoogleCalendarReadOnlyClient.from_config(config)
    if client is None:
        return NOT_CONNECTED
    try:
        events = client.today()
    except Exception:
        return "Calendar access had an error while reading today's schedule."
    if not events:
        return "Your calendar has no events listed for today."
    return _format_events(events)


class GoogleCalendarReadOnlyClient:
    def __init__(self, service: Any) -> None:
        self.service = service

    @classmethod
    def from_config(cls, config: AppConfig) -> "GoogleCalendarReadOnlyClient | None":
        # First try the configured credentials file path (if set)
        if config.google_calendar_enabled and config.google_calendar_credentials_path and config.google_calendar_token_path:
            if config.google_calendar_credentials_path.exists():
                try:
                    service = _build_calendar_service_from_file(config.google_calendar_credentials_path, config.google_calendar_token_path)
                except Exception:
                    service = None
                if service is not None:
                    return cls(service)
        # Then try building from GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET env vars
        # ONLY if a token already exists (don't trigger OAuth flow in non-interactive contexts)
        client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
        if client_id and client_secret:
            token_path = config.google_calendar_token_path or (config.project_root / "secrets" / "google-calendar-token.json")
            # Only attempt to build from token if it already exists - avoid blocking on OAuth
            if token_path.exists():
                try:
                    service = _build_calendar_service_from_env(client_id, client_secret, token_path)
                except Exception:
                    service = None
                if service is not None:
                    return cls(service)
        return None

    def today(self) -> list[CalendarEvent]:
        now = datetime.now().astimezone()
        start = datetime.combine(now.date(), time.min, tzinfo=now.tzinfo)
        end = start + timedelta(days=1)
        result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=start.isoformat(),
                timeMax=end.isoformat(),
                singleEvents=True,
                orderBy="startTime",
                maxResults=10,
            )
            .execute()
        )
        return [_event_from_item(item) for item in result.get("items", [])]


def _build_calendar_service_from_file(credentials_path: Path, token_path: Path):
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(str(token_path), READ_ONLY_SCOPE)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), READ_ONLY_SCOPE)
        credentials = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(credentials.to_json(), encoding="utf-8")
    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request

            credentials.refresh(Request())
            token_path.write_text(credentials.to_json(), encoding="utf-8")
        else:
            return None
    return build("calendar", "v3", credentials=credentials)


def _build_calendar_service_from_env(client_id: str, client_secret: str, token_path: Path):
    """Build a Google Calendar service using client ID and secret from env vars.
    This bypasses the need for a credentials JSON file. Uses the same OAuth flow
    as the file-based approach but constructs the client config in memory.
    """
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    # Construct a client config that looks like a downloaded credentials JSON
    # but built from env vars. This uses the "installed" app type since
    # InstalledAppFlow expects it.
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost"],
        }
    }

    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(str(token_path), READ_ONLY_SCOPE)
    else:
        flow = InstalledAppFlow.from_client_config(client_config, READ_ONLY_SCOPE)
        credentials = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(credentials.to_json(), encoding="utf-8")
    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            from google.auth.transport.requests import Request

            credentials.refresh(Request())
            token_path.write_text(credentials.to_json(), encoding="utf-8")
        else:
            return None
    return build("calendar", "v3", credentials=credentials)


def _event_from_item(item: dict) -> CalendarEvent:
    start = item.get("start", {}).get("dateTime") or item.get("start", {}).get("date", "all day")
    end = item.get("end", {}).get("dateTime") or item.get("end", {}).get("date", "")
    return CalendarEvent(
        summary=item.get("summary", "(no title)"),
        start=_format_time(start),
        end=_format_time(end),
        location=item.get("location", ""),
    )


def _format_events(events: list[CalendarEvent]) -> str:
    parts = ["Today you have:"]
    for event in events[:4]:
        location = f" at {event.location}" if event.location else ""
        parts.append(f"{event.summary} at {event.start}{location}.")
    if len(events) > 4:
        parts.append(f"And {len(events) - 4} more.")
    return " ".join(parts)


def _format_time(value: str) -> str:
    if not value:
        return ""
    if value == "all day" or len(value) == 10:
        return "all day"
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone()
    except ValueError:
        return value
    return parsed.strftime("%I:%M %p").lstrip("0")
