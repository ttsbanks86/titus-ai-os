"""Web search tool with RAG augmentation for the LLM.

Design:
- Tiered search strategy (no single point of failure):
  1. DuckDuckGo lite (no key, sometimes rate-limited)
  2. NewsAPI (uses NEWS_API_KEY from env, reliable for news/current events)
  3. Wikipedia API (no key, reliable for factual/encyclopedic questions)
- Returns titles + snippets for the top results.
- When the user asks a current-events question, this tool searches the web,
  feeds the snippets into the LLM prompt as context, and the LLM composes
  a natural spoken answer using the retrieved facts (RAG pattern).
- Standalone mode: "Jarvis, search the web for X" returns raw result titles.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DUCKDUCKGO_LITE_URL = "https://lite.duckduckgo.com/lite/"
NEWSAPI_URL = "https://newsapi.org/v2/everything"
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
MAX_RESULTS = 6
MAX_SNIPPET_CHARS = 200
MAX_PAGE_FETCH_CHARS = 1500
REQUEST_TIMEOUT = 15


@dataclass(frozen=True)
class WebResult:
    title: str
    url: str
    snippet: str


def web_search(query: str, max_results: int = MAX_RESULTS) -> list[WebResult]:
    """Search the web using a tiered strategy. Returns empty list only if all
    tiers fail. Tries DuckDuckGo first (no key), then NewsAPI (key from env),
    then Wikipedia (no key, factual topics).
    """
    if not query or not query.strip():
        return []

    # Tier 1: DuckDuckGo (no key, sometimes rate-limited)
    results = _search_duckduckgo(query, max_results)
    if results:
        return results

    # Tier 2: NewsAPI (uses NEWS_API_KEY from env)
    results = _search_newsapi(query, max_results)
    if results and _has_recent_articles(results):
        return results
    # If NewsAPI returned stale results, try a refined query with the current date
    from datetime import date

    today_short = date.today().strftime("%B %d").replace(" 0", " ")
    refined_query = _refine_query_for_news(query, today_short)
    if refined_query and refined_query != query:
        results = _search_newsapi(refined_query, max_results, sort_by_published=True)
        if results:
            return results

    # Tier 3: Wikipedia (no key, good for factual/encyclopedic questions)
    results = _search_wikipedia(query, max_results)
    if results:
        return results

    return []


def _has_recent_articles(results: list[WebResult]) -> bool:
    """Check if any results have the current month in the title or snippet,
    as a heuristic for recency.
    """
    from datetime import date

    month_name = date.today().strftime("%B")
    for r in results:
        if month_name in r.title or month_name in r.snippet:
            return True
    return bool(results)


def _refine_query_for_news(query: str, today_short: str) -> str:
    """Build a shorter, more search-friendly query for NewsAPI.
    Strips conversational filler and appends the current date.
    Example: 'who is playing today on the World Cup' -> 'World Cup July 6'
    """
    import re

    cleaned = query.lower()
    cleaned = re.sub(r"\b(who is|who's|whos|what|when|where|how|why|tell me|can you|could you)\b", "", cleaned)
    cleaned = re.sub(r"\b(playing|play|today|tonight|right now|currently|this week|this morning)\b", "", cleaned)
    cleaned = re.sub(r"\b(on|in|at|for|the|a|an|about|of)\b", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        cleaned = query.strip()
    if len(cleaned) > 60:
        cleaned = cleaned[:60].strip()
    return f"{cleaned} {today_short}"


def _search_duckduckgo(query: str, max_results: int) -> list[WebResult]:
    try:
        response = requests.post(
            DUCKDUCKGO_LITE_URL,
            data={"q": query.strip(), "kl": "us-en"},
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException:
        return []
    if response.status_code != 200:
        return []
    return _parse_duckduckgo_lite_results(response.text, max_results)


def _search_newsapi(query: str, max_results: int, sort_by_published: bool = False) -> list[WebResult]:
    """Search NewsAPI. Requires NEWS_API_KEY in env.
    Uses top-headlines for short current-event queries (better for today's news)
    and everything for longer specific topic queries.
    When sort_by_published is True, sorts by publication date (most recent first).
    """
    api_key = os.getenv("NEWS_API_KEY", "")
    if not api_key:
        return []
    try:
        if not sort_by_published and len(query) < 60 and _looks_like_current_event_query_for_newsapi(query):
            response = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={
                    "q": query,
                    "apiKey": api_key,
                    "pageSize": max_results,
                    "country": "us",
                    "category": "sports" if any(s in query.lower() for s in ("world cup", "nba", "nfl", "mlb", "nhl", "sports", "game", "match", "score", "play")) else "general",
                },
                timeout=REQUEST_TIMEOUT,
            )
        else:
            params = {
                "q": query,
                "apiKey": api_key,
                "pageSize": max_results,
                "language": "en",
            }
            if sort_by_published:
                params["sortBy"] = "publishedAt"
            else:
                params["sortBy"] = "relevancy"
            response = requests.get(NEWSAPI_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.RequestException:
        return []
    if response.status_code != 200:
        return []
    try:
        data = response.json()
    except ValueError:
        return []
    results: list[WebResult] = []
    for article in data.get("articles", [])[:max_results]:
        title = article.get("title", "") or ""
        url = article.get("url", "") or ""
        snippet = article.get("description", "") or article.get("content", "") or ""
        source_name = article.get("source", {}).get("name", "")
        if source_name and snippet:
            snippet = f"[{source_name}] {snippet}"
        if len(snippet) > MAX_SNIPPET_CHARS:
            snippet = snippet[: MAX_SNIPPET_CHARS - 3].rstrip() + "..."
        if title and title != "[Removed]":
            results.append(WebResult(title=title, url=url, snippet=snippet))
    return results


def _looks_like_current_event_query_for_newsapi(query: str) -> bool:
    """Decide whether to use NewsAPI's top-headlines (today's news) vs everything
    (all articles). If the query mentions today, current, live, or a current
    sports topic, use top-headlines.
    """
    lowered = query.lower()
    indicators = ("today", "tonight", "current", "live", "right now", "this week", "latest", "breaking")
    if any(ind in lowered for ind in indicators):
        return True
    topics = ("world cup", "fifa", "nba", "nfl", "mlb", "nhl", "sports", "game", "match", "score", "play")
    if any(topic in lowered for topic in topics):
        return True
    return False


def _search_wikipedia(query: str, max_results: int) -> list[WebResult]:
    """Search Wikipedia's API. No key required. Good for factual questions."""
    try:
        response = requests.get(
            WIKIPEDIA_API_URL,
            params={
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": query,
                "srlimit": max_results,
            },
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
    except requests.RequestException:
        return []
    if response.status_code != 200:
        return []
    try:
        data = response.json()
    except ValueError:
        return []
    results: list[WebResult] = []
    for item in data.get("query", {}).get("search", [])[:max_results]:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        # Wikipedia snippets contain HTML tags; strip them
        snippet = re.sub(r"<[^>]+>", "", snippet)
        page_id = item.get("pageid", "")
        url = f"https://en.wikipedia.org/wiki?curid={page_id}" if page_id else ""
        if len(snippet) > MAX_SNIPPET_CHARS:
            snippet = snippet[: MAX_SNIPPET_CHARS - 3].rstrip() + "..."
        if title:
            results.append(WebResult(title=title, url=url, snippet=snippet))
    return results


def _parse_duckduckgo_lite_results(html: str, max_results: int) -> list[WebResult]:
    soup = BeautifulSoup(html, "html.parser")
    results: list[WebResult] = []
    for link in soup.find_all("a", class_="result-link"):
        if len(results) >= max_results:
            break
        title = link.get_text(strip=True)
        raw_url = link.get("href", "")
        url = raw_url if raw_url.startswith("http") else ""
        if not title or not url:
            continue
        # Snippets in lite are often in a nearby td; try to find one
        snippet = _extract_snippet_near_link(link)
        if len(snippet) > MAX_SNIPPET_CHARS:
            snippet = snippet[: MAX_SNIPPET_CHARS - 3].rstrip() + "..."
        results.append(WebResult(title=title, url=url, snippet=snippet))
    return results


def _extract_snippet_near_link(link) -> str:
    """Try to find a snippet near a result link in DuckDuckGo's lite HTML.
    The lite version uses tables, and snippets may be in adjacent rows or cells.
    """
    # Walk up to the parent tr, then look at sibling trs
    parent_tr = link.find_parent("tr")
    if not parent_tr:
        return ""
    # Check the next 2 sibling rows for text content
    for _ in range(2):
        parent_tr = parent_tr.find_next_sibling("tr")
        if not parent_tr:
            break
        for td in parent_tr.find_all("td"):
            text = td.get_text(strip=True)
            if text and len(text) > 30 and "duckduckgo" not in text.lower():
                return text
    return ""


def fetch_page_content(url: str, max_chars: int = MAX_PAGE_FETCH_CHARS) -> str:
    """Fetch a web page and extract its main text content.
    Used to get richer context from the top search result.
    Returns up to max_chars of plain text. Returns empty string on any error.
    """
    if not url or not url.startswith("http"):
        return ""
    try:
        response = requests.get(
            url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
            stream=True,
        )
    except requests.RequestException:
        return ""
    if response.status_code != 200:
        return ""
    # Read up to 500KB to avoid downloading huge pages
    content = response.raw.read(500_000)
    html = content.decode("utf-8", errors="ignore")
    return _extract_main_text(html, max_chars)


def _extract_main_text(html: str, max_chars: int) -> str:
    """Extract readable text from an HTML page using BeautifulSoup.
    Strips scripts, styles, nav, footer, and other non-content elements.
    """
    soup = BeautifulSoup(html, "html.parser")
    # Remove non-content elements
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]):
        tag.decompose()
    # Try to find the main content area
    main = soup.find("main") or soup.find("article") or soup.find("div", class_=re.compile(r"content|article|post|entry", re.I))
    text_source = main if main else soup
    # Get text, clean whitespace
    text = text_source.get_text(separator=" ", strip=True)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(".", 1)[0].strip() + "."
    return text


def format_search_results_for_user(results: list[WebResult], query: str) -> str:
    """Format search results as a spoken response for the user.
    Used when the user explicitly asks to search the web.
    """
    if not results:
        return f"I searched for {query} but did not find any results."
    parts = [f"Here is what I found for {query}."]
    for i, result in enumerate(results[:3], 1):
        parts.append(f"{i}. {result.title}.")
        if result.snippet:
            parts.append(result.snippet)
    if len(results) > 3:
        parts.append(f"And {len(results) - 3} more results.")
    return " ".join(parts)


def format_search_results_for_llm(results: list[WebResult], query: str, page_content: str = "") -> str:
    """Format search results as context for the LLM to compose a natural answer.
    Used in RAG mode: the LLM receives these facts and writes the spoken response.
    Optionally includes fetched page content from the top result for richer context.
    """
    if not results and not page_content:
        return ""
    parts = [f"Web search results for: {query}"]
    for i, result in enumerate(results, 1):
        parts.append(f"[{i}] {result.title}")
        if result.snippet:
            parts.append(f"Snippet: {result.snippet}")
    if page_content:
        parts.append(f"\nTop page content ({results[0].title if results else 'top result'}):\n{page_content}")
    parts.append("\nUse these search results to answer the user's question naturally. If the results do not contain the answer, say so honestly. Cite sources by name when the answer comes from a specific result.")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Trigger detection: when should Jarvis automatically search the web?
# ---------------------------------------------------------------------------

CURRENT_EVENT_INDICATORS = (
    "today",
    "tonight",
    "this morning",
    "this afternoon",
    "this evening",
    "right now",
    "currently",
    "latest",
    "recent",
    "this week",
    "this month",
    "this year",
    "yesterday",
    "breaking",
    "live",
    "score",
    "scores",
    "who is playing",
    "whos playing",
    "who's playing",
    "what happened",
    "what's happening",
    "whats happening",
    "news",
    "update",
    "results",
    "fixture",
    "fixtures",
    "schedule",
    "lineup",
    "standings",
    "bracket",
    "rankings",
    "stock price",
    "election",
    "release date",
    "came out",
    "released",
    "announced",
)

# Topics that almost always need current data
CURRENT_TOPIC_INDICATORS = (
    "world cup",
    "fifa",
    "nba",
    "nfl",
    "mlb",
    "nhl",
    "premier league",
    "champions league",
    "super bowl",
    "olympics",
    "formula 1",
    "f1",
    "ufc",
    "boxing",
    "tennis",
    "golf",
    "esports",
    "stock market",
    "crypto",
    "bitcoin",
    "exchange rate",
    "movie showtime",
    "box office",
    "charts",
    "billboard",
    "trending",
    "viral",
    "tweet",
)


def looks_like_current_event_question(text: str) -> bool:
    """Decide whether a question needs live web data before the LLM answers."""
    if not text:
        return False
    lowered = text.lower()
    for indicator in CURRENT_EVENT_INDICATORS:
        if indicator in lowered:
            return True
    for topic in CURRENT_TOPIC_INDICATORS:
        if topic in lowered:
            return True
    if re.search(r"\b(who\s+is|who's|whos|what\s+teams|what\s+time)\b", lowered):
        return True
    return False


def extract_search_query_from_text(text: str) -> str:
    """Extract a clean search query from a user's natural-language question."""
    if not text:
        return ""
    cleaned = text.strip()
    cleaned = re.sub(r"^(jarvis|hey jarvis|ok jarvis|okay jarvis|hi jarvis)[,\.]?\s*", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^(can you|could you|please|would you|just|quick question)\s+", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^(google|search|look up|find out|tell me|let me know)\s+(for|about|the|on|what|who|when|where|how|why)\s+", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^(google|search|look up|find out|tell me|let me know)\s+", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = cleaned.rstrip("?").strip()
    if not cleaned:
        return text.strip()
    return cleaned