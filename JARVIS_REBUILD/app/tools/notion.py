from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any

import requests

from app.config import AppConfig
from app.tools.composio_tool import read_only_response


NOT_CONNECTED = "Notion access is not connected yet. Set NOTION_API_TOKEN in your environment."
NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"
WRITE_KEYWORDS = {"create", "add", "update", "edit", "delete", "archive", "trash", "move", "rename"}
MAX_PAGES = 5
MAX_BLOCK_TEXT_CHARS = 800


@dataclass(frozen=True)
class NotionPageSummary:
    id: str
    title: str
    url: str
    last_edited_time: str = ""


def notion_response(config: AppConfig, command: str) -> str:
    """Read-only Notion access. Tries the direct API token first (NOTION_API_TOKEN),
    falls back to Composio if direct is not configured. Write actions always
    require Jarvis approval.
    """
    # Composio first if the user has explicitly opted into composio connector mode
    # AND the direct token is unavailable. Direct wins when both are present,
    # because the direct token is already provisioned and requires no Composio
    # account connection step.
    api_token = config.notion_api_token or os.getenv("NOTION_API_TOKEN", "")
    if not api_token:
        # No direct token. Try Composio as the fallback path.
        if config.connector_mode == "composio":
            return read_only_response(config, "notion", command)
        return NOT_CONNECTED

    if _looks_like_write(command):
        return "Notion write actions require Jarvis approval first."

    query = _extract_search_query(command)
    try:
        if query:
            pages = _search_pages(api_token, query, max_results=MAX_PAGES)
            scope = f"matching {query}"
        else:
            pages = _recent_pages(api_token, max_results=MAX_PAGES)
            scope = "recently edited pages"
    except requests.RequestException:
        return "Notion access had a network error while reading."
    except Exception:
        return "Notion access had an error while reading pages."

    if not pages:
        return f"I did not find any Notion pages in the {scope}."

    # If the user explicitly asked to read/summarize a specific page, attempt to
    # fetch its block content too.
    if _asks_for_page_content(command) and pages:
        try:
            content = _fetch_page_text(api_token, pages[0].id)
            if content:
                title = pages[0].title or "(untitled)"
                snippet = content[:600].strip()
                return f"{title}: {snippet}"
        except Exception:
            # Fall back to the summary list if content fetch fails.
            pass

    return _format_summaries(pages, scope)


class NotionReadOnlyClient:
    """Thin wrapper for testing. Not used by the response function directly,
    but exposed so tests can construct a client with a stub token and verify
    behavior. The real HTTP calls happen in the module-level helpers.
    """

    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    @classmethod
    def from_config(cls, config: AppConfig) -> "NotionReadOnlyClient | None":
        token = config.notion_api_token or os.getenv("NOTION_API_TOKEN", "")
        if not token:
            return None
        return cls(token)

    def search(self, query: str, max_results: int = MAX_PAGES) -> list[NotionPageSummary]:
        return _search_pages(self.api_token, query, max_results=max_results)

    def recent(self, max_results: int = MAX_PAGES) -> list[NotionPageSummary]:
        return _recent_pages(self.api_token, max_results=max_results)


def _search_pages(api_token: str, query: str, max_results: int = MAX_PAGES) -> list[NotionPageSummary]:
    payload = {"query": query, "page_size": max_results}
    response = requests.post(
        f"{NOTION_API_BASE}/search",
        headers=_headers(api_token),
        json=payload,
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    return [_page_from_result(item) for item in data.get("results", []) if _is_page(item)]


def _recent_pages(api_token: str, max_results: int = MAX_PAGES) -> list[NotionPageSummary]:
    # Notion's search endpoint with an empty query sorts by last_edited_time
    # in descending order, which gives us the recently edited pages.
    payload = {"query": "", "page_size": max_results, "sort": {"direction": "descending", "timestamp": "last_edited_time"}}
    response = requests.post(
        f"{NOTION_API_BASE}/search",
        headers=_headers(api_token),
        json=payload,
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    return [_page_from_result(item) for item in data.get("results", []) if _is_page(item)]


def _fetch_page_text(api_token: str, page_id: str) -> str:
    """Fetch the block tree of a page and extract plain text from it.
    Only walks the top-level and one level of children to keep response size sane.
    """
    parts: list[str] = []
    response = requests.get(
        f"{NOTION_API_BASE}/blocks/{page_id}/children",
        headers=_headers(api_token),
        params={"page_size": 100},
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    for block in data.get("results", []):
        text = _text_from_block(block)
        if text:
            parts.append(text)
        if len(" ".join(parts)) >= MAX_BLOCK_TEXT_CHARS:
            break
    return "\n".join(parts).strip()


def _headers(api_token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _is_page(item: dict) -> bool:
    return item.get("object") == "page"


def _page_from_result(item: dict) -> NotionPageSummary:
    title = _extract_title_from_page(item)
    return NotionPageSummary(
        id=item.get("id", ""),
        title=title,
        url=item.get("url", ""),
        last_edited_time=item.get("last_edited_time", ""),
    )


def _extract_title_from_page(page: dict) -> str:
    properties = page.get("properties") or {}
    # Notion page titles live in a property whose type is "title".
    for prop in properties.values():
        if isinstance(prop, dict) and prop.get("type") == "title":
            title_array = prop.get("title") or []
            return _text_from_rich_text_array(title_array)
    return ""


def _text_from_block(block: dict) -> str:
    block_type = block.get("type")
    if not block_type:
        return ""
    payload = block.get(block_type) or {}
    rich_text = payload.get("rich_text") or payload.get("text") or []
    return _text_from_rich_text_array(rich_text)


def _text_from_rich_text_array(rich_text: list) -> str:
    if not isinstance(rich_text, list):
        return ""
    parts: list[str] = []
    for piece in rich_text:
        if isinstance(piece, dict):
            text = piece.get("plain_text") or piece.get("text", {}).get("content") if isinstance(piece.get("text"), dict) else piece.get("plain_text")
            if isinstance(text, str):
                parts.append(text)
    return "".join(parts).strip()


def _extract_search_query(command: str) -> str:
    text = command.lower().replace("jarvis,", "").strip()
    match = re.search(r"search notion for (.+)", text)
    if match:
        return match.group(1).strip(" .?")
    match = re.search(r"read my notion page about (.+)", text)
    if match:
        return match.group(1).strip(" .?")
    match = re.search(r"notion page about (.+)", text)
    if match:
        return match.group(1).strip(" .?")
    return ""


def _asks_for_page_content(command: str) -> bool:
    lowered = command.lower()
    return any(
        phrase in lowered
        for phrase in (
            "read my notion page",
            "summarize my notion page",
            "summarize my latest notion",
            "read my latest notion",
            "what does my notion page say",
        )
    )


def _looks_like_write(command: str) -> bool:
    lowered = command.lower()
    return any(keyword in lowered for keyword in WRITE_KEYWORDS)


def _format_summaries(pages: list[NotionPageSummary], scope: str) -> str:
    parts = [f"From the {scope}: "]
    for page in pages[:3]:
        title = page.title or "(untitled)"
        parts.append(f"{title}.")
    if len(pages) > 3:
        parts.append(f"And {len(pages) - 3} more.")
    return " ".join(parts)