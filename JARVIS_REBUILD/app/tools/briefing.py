"""Daily briefing aggregator.

Composes a single spoken response from:
- Today's weather (if configured)
- Latest unread/important emails (direct Gmail)
- Today's calendar events (if connected)
- Recent Notion pages (if direct token is configured)
- Top open tasks from the most recent daily note in Obsidian

Each section is best-effort. If a tool is not configured, the briefing
gracefully skips that section instead of failing the whole response.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Callable

from app.config import AppConfig
from app.tools.weather import weather_response
from app.tools.email import email_response, GmailReadOnlyClient
from app.tools.calendar import calendar_response, GoogleCalendarReadOnlyClient
from app.tools.notion import notion_response, NotionReadOnlyClient


@dataclass(frozen=True)
class BriefingSection:
    name: str
    text: str
    available: bool


def briefing_response(config: AppConfig) -> str:
    sections: list[BriefingSection] = []
    sections.append(_weather_section(config))
    sections.append(_calendar_section(config))
    sections.append(_email_section(config))
    sections.append(_notion_section(config))
    sections.append(_obsidian_tasks_section(config))

    # Compose the final spoken briefing. We include each available section
    # and skip the unavailable ones entirely (rather than saying "not available"
    # for each, which would be tedious in voice mode).
    parts: list[str] = []
    parts.append(f"Good morning. Here is your briefing for {date.today().strftime('%A, %B %d')}.")
    for section in sections:
        if section.available and section.text:
            parts.append(section.text)
    if len(parts) == 1:
        # Only the greeting — no sections were available.
        parts.append(
            "I could not pull any of your connected sources right now. "
            "Connect Gmail, Calendar, Notion, or weather to get a full briefing."
        )
    parts.append("That is your briefing. Have a focused day.")
    return " ".join(parts)


def _weather_section(config: AppConfig) -> BriefingSection:
    try:
        text = weather_response(config)
        # weather_response returns setup hints when not configured. Treat those
        # as unavailable so the briefing doesn't read setup hints out loud.
        if not text or "not configured" in text.lower() or "set " in text.lower() and "JARVIS_" in text:
            return BriefingSection("weather", "", False)
        return BriefingSection("weather", f"Weather: {text}", True)
    except Exception:
        return BriefingSection("weather", "", False)


def _calendar_section(config: AppConfig) -> BriefingSection:
    try:
        text = calendar_response(config, "what is on my schedule today")
        # The calendar response returns "not connected yet" or the Composio
        # auth-config-no-active-account message when calendar is unavailable.
        lowered = text.lower()
        if (
            "not connected" in lowered
            or "no active connected account" in lowered
            or "not completed" in lowered
            or "calendar access is not connected" in lowered
        ):
            return BriefingSection("calendar", "", False)
        if "no events listed" in lowered:
            return BriefingSection("calendar", "Calendar: no events scheduled for today.", True)
        return BriefingSection("calendar", f"Calendar: {text}", True)
    except Exception:
        return BriefingSection("calendar", "", False)


def _email_section(config: AppConfig) -> BriefingSection:
    try:
        # Use a targeted query rather than the full email_response so the briefing
        # stays concise. We pull the latest 3 inbox messages via the direct client
        # when available. If direct Gmail isn't configured, fall back to a
        # best-effort call to email_response which itself returns a clean
        # "not connected" message.
        client = GmailReadOnlyClient.from_config(config)
        if client is None:
            return BriefingSection("email", "", False)
        summaries = client.latest(max_results=3)
        if not summaries:
            return BriefingSection("email", "Email: your inbox has no recent messages.", True)
        parts = ["Email: latest inbox."]
        for summary in summaries:
            subject = summary.subject or "(no subject)"
            sender = summary.sender or "Unknown sender"
            # Trim sender to a friendly short form (just the name part if present)
            if "<" in sender:
                sender = sender.split("<", 1)[0].strip().strip('"')
            parts.append(f"{subject} from {sender}.")
        return BriefingSection("email", " ".join(parts), True)
    except Exception:
        return BriefingSection("email", "", False)


def _notion_section(config: AppConfig) -> BriefingSection:
    try:
        client = NotionReadOnlyClient.from_config(config)
        if client is None:
            return BriefingSection("notion", "", False)
        pages = client.recent(max_results=3)
        if not pages:
            return BriefingSection("notion", "", False)
        parts = ["Notion: recently edited pages."]
        for page in pages:
            title = page.title or "(untitled)"
            parts.append(f"{title}.")
        return BriefingSection("notion", " ".join(parts), True)
    except Exception:
        return BriefingSection("notion", "", False)


def _obsidian_tasks_section(config: AppConfig) -> BriefingSection:
    """Pull open tasks from the most recent daily note in the Obsidian inbox.

    Looks for lines starting with "- [ ]" (uncompleted Markdown checkboxes).
    Falls back gracefully if no daily note exists or no open tasks are found.
    """
    try:
        inbox = config.obsidian_inbox_path
        if not inbox.exists():
            return BriefingSection("tasks", "", False)
        # Find the most recent .md file in the inbox directory.
        # Sort by mtime first. On Windows, file mtime resolution can be coarse
        # (seconds, sometimes 2-second granularity on FAT-derived filesystems),
        # so files created back-to-back can share mtime. As a deterministic
        # tiebreaker, we sort by filename descending (which works for ISO-date
        # named daily notes like 2026-07-06.md).
        daily_notes = sorted(
            (p for p in inbox.glob("*.md") if p.is_file()),
            key=lambda p: (p.stat().st_mtime, p.name),
            reverse=True,
        )
        if not daily_notes:
            return BriefingSection("tasks", "", False)
        latest_note = daily_notes[0]
        text = latest_note.read_text(encoding="utf-8", errors="ignore")
        open_tasks = _extract_open_tasks(text, limit=3)
        if not open_tasks:
            return BriefingSection("tasks", "", False)
        parts = [f"Open tasks from {latest_note.stem}:"]
        for task in open_tasks:
            parts.append(task)
        return BriefingSection("tasks", " ".join(parts), True)
    except Exception:
        return BriefingSection("tasks", "", False)


def _extract_open_tasks(text: str, limit: int = 3) -> list[str]:
    """Extract uncompleted Markdown checklist items from a note's text."""
    tasks: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        # Match "- [ ] task text" (standard Obsidian/Markdown open task)
        if stripped.startswith("- [ ]"):
            task_text = stripped[len("- [ ]"):].strip()
            # Strip wikilinks and markdown emphasis for cleaner spoken output
            task_text = _clean_task_text(task_text)
            if task_text and len(tasks) < limit:
                tasks.append(task_text)
    return tasks


def _clean_task_text(text: str) -> str:
    # Remove Obsidian wikilinks [[Note Name]] -> Note Name
    # In Obsidian, [[Note Name|Alias]] displays as Alias, so we prefer the alias.
    import re

    def _wikilink_replacement(match: re.Match) -> str:
        inner = match.group(1)
        if "|" in inner:
            # Use the alias (the part after the pipe)
            return inner.split("|", 1)[1].split("#", 1)[0]
        return inner.split("#", 1)[0]

    text = re.sub(r"\[\[([^\]]+)\]\]", _wikilink_replacement, text)
    # Remove markdown emphasis markers
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Cap length for voice output
    if len(text) > 120:
        text = text[:117].rstrip() + "..."
    return text


def looks_like_briefing_request(text: str) -> bool:
    lowered = text.lower()
    return any(
        phrase in lowered
        for phrase in (
            "what's happening today",
            "what is happening today",
            "give me my briefing",
            "give me my daily briefing",
            "morning briefing",
            "daily briefing",
            "what's my day look like",
            "what does my day look like",
            "brief me",
            "start my day",
        )
    )