from __future__ import annotations

import base64
import html
import re
from dataclasses import dataclass
from email.message import Message
from email.parser import Parser
from pathlib import Path
from typing import Any

from app.config import AppConfig
from app.tools.composio_tool import read_only_response


READ_ONLY_SCOPE = ["https://www.googleapis.com/auth/gmail.readonly"]
NOT_CONNECTED = "Email access is not connected yet. I can add Gmail or Outlook next."


@dataclass(frozen=True)
class EmailSummary:
    sender: str
    subject: str
    snippet: str
    date: str = ""


def email_response(config: AppConfig, command: str) -> str:
    if config.connector_mode == "composio":
        composio_message = read_only_response(config, "gmail", command)
        if "no active connected account is visible" not in composio_message:
            return composio_message
    client = GmailReadOnlyClient.from_config(config)
    if client is None:
        return NOT_CONNECTED

    query = _extract_search_query(command)
    try:
        if query:
            summaries = client.search(query, max_results=config.gmail_max_results)
            scope = f"matching {query}"
        else:
            summaries = client.latest(max_results=config.gmail_max_results)
            scope = "latest inbox messages"
    except Exception:
        return "Gmail access had an error while reading messages."

    if not summaries:
        return f"I did not find any emails in the {scope}."
    return _format_summaries(summaries, scope)


class GmailReadOnlyClient:
    def __init__(self, service: Any) -> None:
        self.service = service

    @classmethod
    def from_config(cls, config: AppConfig) -> "GmailReadOnlyClient | None":
        if not config.gmail_credentials_path or not config.gmail_token_path:
            return None
        if not config.gmail_credentials_path.exists():
            return None
        try:
            service = _build_gmail_service(config.gmail_credentials_path, config.gmail_token_path)
        except Exception:
            return None
        if service is None:
            return None
        return cls(service)

    def latest(self, max_results: int = 5) -> list[EmailSummary]:
        return self.search("in:inbox newer_than:30d", max_results=max_results)

    def search(self, query: str, max_results: int = 5) -> list[EmailSummary]:
        listed = (
            self.service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )
        messages = listed.get("messages", [])
        summaries: list[EmailSummary] = []
        for item in messages:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=item["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"])
                .execute()
            )
            summaries.append(_summary_from_message(message))
        return summaries


def _build_gmail_service(credentials_path: Path, token_path: Path):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(str(token_path), READ_ONLY_SCOPE)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), READ_ONLY_SCOPE)
        credentials = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(credentials.to_json(), encoding="utf-8")
    if not credentials.valid and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        token_path.write_text(credentials.to_json(), encoding="utf-8")
    if not credentials.valid:
        return None
    return build("gmail", "v1", credentials=credentials)


def _summary_from_message(message: dict) -> EmailSummary:
    headers = {header["name"].lower(): header["value"] for header in message.get("payload", {}).get("headers", [])}
    snippet = message.get("snippet", "")
    if not snippet and "payload" in message:
        snippet = _payload_text(message["payload"])
    return EmailSummary(
        sender=headers.get("from", "Unknown sender"),
        subject=headers.get("subject", "(no subject)"),
        date=headers.get("date", ""),
        snippet=snippet,
    )


def _payload_text(payload: dict) -> str:
    data = payload.get("body", {}).get("data")
    if not data:
        return ""
    decoded = base64.urlsafe_b64decode(data + "===")
    parsed: Message = Parser().parsestr(decoded.decode("utf-8", errors="ignore"))
    return parsed.get_payload() if isinstance(parsed.get_payload(), str) else ""


def _extract_search_query(command: str) -> str:
    text = command.lower().replace("jarvis,", "").strip()
    match = re.search(r"search my email for (.+)", text)
    if match:
        return match.group(1).strip(" .?")
    return ""


def _format_summaries(summaries: list[EmailSummary], scope: str) -> str:
    parts = [f"From the {scope}: "]
    for summary in summaries[:3]:
        subject = _clean_spoken_email_text(summary.subject) or "(no subject)"
        sender = _clean_spoken_email_text(summary.sender) or "Unknown sender"
        snippet = _clean_spoken_email_text(summary.snippet)
        if len(snippet) > 100:
            snippet = snippet[:97].rstrip() + "..."
        parts.append(f"{subject} from {sender}: {snippet}")
    return " ".join(parts)


def _clean_spoken_email_text(text: str) -> str:
    text = html.unescape(text or "")
    text = text.encode("ascii", errors="ignore").decode("ascii")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -:\t\r\n")
