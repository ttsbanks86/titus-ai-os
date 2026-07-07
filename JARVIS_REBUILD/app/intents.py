from __future__ import annotations

import re
from dataclasses import dataclass


NOISE = "noise"
SELF_SPEECH = "self_speech"
STOP = "stop"
EXIT = "exit"
GREETING = "greeting"
CAPABILITIES = "capabilities"
WEATHER = "weather"
OPENCLAW = "openclaw"
OBSIDIAN = "obsidian"
EMAIL = "email"
NOTION = "notion"
BROWSER = "browser"
CALENDAR = "calendar"
FILE_CREATE = "file_create"
FILE_APPEND = "file_append"
BRIEFING = "briefing"
SYSTEM_CONTROL = "system_control"
MEMORY_STORE = "memory_store"  # "remember this" - explicitly store a fact
MEMORY_QUERY = "memory_query"  # "what do you remember" - query stored memories
BASIC_CHAT = "basic_chat"
SYSTEM_QUESTION = "system_question"
UNKNOWN = "unknown"


BACKGROUND_NOISE_PHRASES = {
    "ill see you in the next one",
    "i'll see you in the next one",
    "see you in the next one",
}

# OpenClaw keywords that trigger the coding/agent route.
# These must match as whole words/phrases, not as substrings, to avoid
# misrouting words like "hard-coded" (contains "code") or "scoring" (contains "code").
OPENCLAW_KEYWORDS = {
    "code",
    "coding",
    "debug",
    "debugging",
    "python",
    "script",
    "app",
    "build",
    "automation",
    "agent",
    "system plan",
    "architecture",
}

# Phrases that should NOT trigger OpenClaw even if they contain a keyword.
# This catches conversational uses of keyword words that aren't coding tasks.
OPENCLAW_NEGATIVE_PHRASES = {
    "hard-coded",
    "hard coded",
    "hardcoded",
    "area code",
    "zip code",
    "country code",
    "passcode",
    "barcode",
    "decode",
    "encode",
    "area codes",
    "diagnostic code",
    "source of truth",
}

CAPABILITY_PHRASES = {
    "what are your capabilities",
    "what can you do",
    "what are you able to do",
    "what are your",
    "what can you",
    "what do you",
    "tell me your capabilities",
    "tell me what you can do",
}

# Phrases that should NOT trigger the capabilities intent even though they
# sound like they might be about capabilities. These should go to the LLM
# for a more natural, personality-driven response.
CAPABILITY_NEGATIVE_PHRASES = {
    "introduce yourself",
    "introduce you",
    "who are you",
    "what is your name",
    "what's your name",
    "tell me about yourself",
    "say hi to",
    "say hello to",
    "introduce yourself to my",
    "introduce yourself to the",
    "introduce yourself to our",
    "show off",
    "do a demo",
    "do a quick demo",
}


@dataclass(frozen=True)
class Intent:
    name: str
    text: str
    cleaned_text: str
    reason: str


def clean_transcript(text: str) -> str:
    text = text or ""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def normalize_text(text: str) -> str:
    cleaned = clean_transcript(text).lower()
    cleaned = cleaned.replace("jarvis,", "jarvis ")
    cleaned = cleaned.replace("jarvis.", "jarvis ")
    cleaned = re.sub(r"[^\w\s']", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def strip_assistant_name(text: str, assistant_name: str = "jarvis") -> str:
    normalized = normalize_text(text)
    name = assistant_name.lower()
    if normalized.startswith(name + " "):
        return normalized[len(name) + 1 :].strip()
    return normalized


def is_noise(text: str) -> bool:
    normalized = normalize_text(text)
    without_name = strip_assistant_name(normalized)
    return normalized in BACKGROUND_NOISE_PHRASES or without_name in BACKGROUND_NOISE_PHRASES


def is_self_speech(text: str, recent_assistant_speech: str | None = None, source: str = "user") -> bool:
    if source == "assistant":
        return True
    if not recent_assistant_speech:
        return False
    return normalize_text(text) == normalize_text(recent_assistant_speech)


def classify_intent(
    text: str,
    *,
    recent_assistant_speech: str | None = None,
    source: str = "user",
    assistant_name: str = "jarvis",
) -> Intent:
    cleaned = clean_transcript(text)
    normalized = normalize_text(cleaned)
    body = strip_assistant_name(normalized, assistant_name)

    if not normalized:
        return Intent(NOISE, cleaned, normalized, "empty transcript")
    if is_self_speech(cleaned, recent_assistant_speech, source):
        return Intent(SELF_SPEECH, cleaned, normalized, "matched recent assistant speech")
    if is_noise(cleaned):
        return Intent(NOISE, cleaned, normalized, "known background phrase")
    if body in {"stop", "cancel", "quiet", "silence"}:
        return Intent(STOP, cleaned, normalized, "system stop command")
    if body in {"exit", "quit", "shutdown", "close"}:
        return Intent(EXIT, cleaned, normalized, "system exit command")
    if body in {"hello", "hi", "hey", "hello jarvis", "hi jarvis", "hey jarvis"} or normalized in {
        "hello jarvis",
        "hi jarvis",
        "hey jarvis",
    }:
        return Intent(GREETING, cleaned, normalized, "greeting")
    if _looks_like_capability_question(body):
        return Intent(CAPABILITIES, cleaned, normalized, "capabilities request")
    if "weather" in body or "forecast" in body or "temperature" in body:
        return Intent(WEATHER, cleaned, normalized, "weather request")
    if _looks_like_obsidian_request(body):
        return Intent(OBSIDIAN, cleaned, normalized, "obsidian vault request")
    if _looks_like_email_request(body):
        return Intent(EMAIL, cleaned, normalized, "email read-only request")
    if _looks_like_notion_request(body):
        return Intent(NOTION, cleaned, normalized, "notion read-only request")
    if _looks_like_calendar_request(body):
        return Intent(CALENDAR, cleaned, normalized, "calendar read-only request")
    if _looks_like_file_create_request(body):
        return Intent(FILE_CREATE, cleaned, normalized, "file creation request")
    if _looks_like_file_append_request(body):
        return Intent(FILE_APPEND, cleaned, normalized, "file append request")
    if _looks_like_browser_request(body):
        return Intent(BROWSER, cleaned, normalized, "browser control request")
    if _looks_like_briefing_request(body):
        return Intent(BRIEFING, cleaned, normalized, "daily briefing request")
    if _looks_like_memory_store_request(body):
        return Intent(MEMORY_STORE, cleaned, normalized, "memory store request")
    if _looks_like_memory_query_request(body):
        return Intent(MEMORY_QUERY, cleaned, normalized, "memory query request")
    if _looks_like_system_control_request(body):
        return Intent(SYSTEM_CONTROL, cleaned, normalized, "system control request")
    if _looks_like_openclaw_task(body):
        return Intent(OPENCLAW, cleaned, normalized, "coding or agent task")
    if _looks_like_system_question(body):
        return Intent(SYSTEM_QUESTION, cleaned, normalized, "system or Jarvis question")
    if _looks_like_basic_chat(body):
        return Intent(BASIC_CHAT, cleaned, normalized, "basic chat or general question")
    return Intent(UNKNOWN, cleaned, normalized, "no local intent matched")


def _looks_like_openclaw_task(text: str) -> bool:
    # First, check if any negative phrase is present. If the text contains
    # "hard-coded", "area code", etc., it's NOT a coding task even though it
    # contains "code".
    for negative in OPENCLAW_NEGATIVE_PHRASES:
        if negative in text:
            return False
    # Use word-boundary matching for single-word keywords to avoid
    # "hard-coded" matching "code", "scoring" matching "code", etc.
    for keyword in OPENCLAW_KEYWORDS:
        if " " in keyword:
            # Multi-word keyword: simple substring match is fine
            if keyword in text:
                return True
        else:
            # Single-word keyword: match as a whole word using regex
            if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                return True
    return False


def _looks_like_capability_question(text: str) -> bool:
    # First, check if any negative phrase is present. "Introduce yourself"
    # should go to the LLM, not the capabilities list.
    for negative in CAPABILITY_NEGATIVE_PHRASES:
        if negative in text:
            return False
    if "capabilities" in text:
        return True
    if text in CAPABILITY_PHRASES:
        return True
    capability_phrases = CAPABILITY_PHRASES - {"what are your", "what can you", "what do you"}
    return any(phrase in text for phrase in capability_phrases)


def _looks_like_obsidian_request(text: str) -> bool:
    phrases = (
        "search obsidian for",
        "find my note about",
        "what do i have in my vault about",
        "summarize this note",
        "open the note about",
        "where is this information in my vault",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_email_request(text: str) -> bool:
    phrases = (
        "check my email",
        "new emails",
        "any new email",
        "summarize my latest emails",
        "search my email for",
        "what do i have on my email",
        "what's in my inbox",
        "whats in my inbox",
        "what is in my email",
        "read my email",
        "read my emails",
        "show me my email",
        "show me my inbox",
        "do i have new emails",
        "do i have any email",
        "do i have any emails",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_notion_request(text: str) -> bool:
    phrases = (
        "search notion for",
        "search my notion for",
        "find my notion page about",
        "read my notion page",
        "read my latest notion",
        "summarize my notion page",
        "summarize my latest notion",
        "what does my notion page say",
        "show me my notion",
        "notion page about",
        "recent notion pages",
        "what is in my notion",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_browser_request(text: str) -> bool:
    phrases = (
        "open chrome",
        "could you open chrome",
        "open browser",
        "close browser",
        "close chrome",
        "open website",
        "open this website",
        "open a new tab",
        "open a tab",
        "new tab in chrome",
        "search the web for",
        "use openclaw to open chrome",
        "try to open",
        "open again",
        "open the browser",
        "launch chrome",
        "start chrome",
        "open the web",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_calendar_request(text: str) -> bool:
    phrases = (
        "what am i working on today",
        "what is on my schedule today",
        "what's on my schedule today",
        "what do i have today",
        "what are my tasks today",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_file_create_request(text: str) -> bool:
    # If the user specified desktop or downloads, defer to system_control
    # which handles those locations with proper authorization.
    if "desktop" in text or "downloads" in text:
        return False
    phrases = (
        "create a file called",
        "create a file named",
        "create a file for the name",
        "create a file for",
        "create a file with the name",
        "create a new file",
        "create a new file called",
        "create a note about",
        "create an obsidian note about",
        "create a folder called",
        "create a folder named",
        "create a folder for the name",
        "create a folder for",
        "create a new folder",
        "create a new folder called",
        "create a new folder and call it",
        "create a new folder and name it",
        "make a file called",
        "make a file named",
        "make a file for",
        "make a folder called",
        "make a folder named",
        "make a new folder",
        "save this as a markdown file",
        "save this in my vault",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_file_append_request(text: str) -> bool:
    return "append this to my note" in text or "append this to" in text


def _looks_like_briefing_request(text: str) -> bool:
    phrases = (
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
    return any(phrase in text for phrase in phrases)


def _looks_like_system_control_request(text: str) -> bool:
    """Detect requests to control the computer: open/close apps, list files,
    create folders on desktop, take screenshots, list running apps.
    """
    from app.tools.system_control import (
        _looks_like_open_app,
        _looks_like_close_app,
        _looks_like_list_apps,
        _looks_like_screenshot,
        _looks_like_create_folder,
        _looks_like_list_files,
        _looks_like_read_file,
        _looks_like_move_file,
        _looks_like_rename_file,
    )

    return (
        _looks_like_open_app(text)
        or _looks_like_close_app(text)
        or _looks_like_list_apps(text)
        or _looks_like_screenshot(text)
        or _looks_like_create_folder(text)
        or _looks_like_list_files(text)
        or _looks_like_read_file(text)
        or _looks_like_move_file(text)
        or _looks_like_rename_file(text)
    )


def _looks_like_system_question(text: str) -> bool:
    phrases = (
        "what is your status",
        "are you connected",
        "what tools are connected",
        "what tools do you have",
        "what is my system",
        "how are you set up",
        "what do you know about me",
        "who am i",
        "what do you remember about me",
        "how does jarvis work",
        "what is mission control",
        "is openclaw connected",
        "is composio connected",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_basic_chat(text: str) -> bool:
    if text.endswith("?"):
        return True
    starters = (
        "tell me",
        "explain",
        "summarize",
        "why",
        "how",
        "what",
        "when",
        "where",
        "who",
        "can you",
        "could you",
        "i need advice",
        "help me think",
    )
    return any(text.startswith(starter) for starter in starters)


def _looks_like_memory_store_request(text: str) -> bool:
    """Detect requests to explicitly remember/store a fact or preference.
    
    Examples:
    - "remember that I prefer Sekuru voice"
    - "remember this: my interview is on Friday"
    - "don't forget that I'm working on Jarvis"
    - "keep in mind that I like dark mode"
    """
    phrases = (
        "remember that",
        "remember this",
        "remember the",
        "don't forget",
        "dont forget",
        "keep in mind",
        "keep this in mind",
        "note that",
        "make a note",
        "save this",
        "store this",
        "remember my",
        "remember i",
        "remember when",
    )
    return any(phrase in text for phrase in phrases)


def _looks_like_memory_query_request(text: str) -> bool:
    """Detect requests to query stored memories.
    
    Examples:
    - "what do you remember about me"
    - "what do you remember"
    - "do you remember when we did the mock interview"
    - "what have you learned about me"
    - "tell me what you know about my preferences"
    - "show me your memory"
    
    Note: "what do you know about me" is a SYSTEM_QUESTION (handled by the LLM
    with profile context), not a memory query. We exclude it here.
    """
    # First, check for the negative phrase - "what do you know about me" is a system question
    # that should be routed to the LLM with vault profile context, not to memory query.
    if text.strip() in ("what do you know about me", "what do you know about me?", 
                        "what do you know about my", "what do you know about my?"):
        return False
    
    phrases = (
        "what do you remember",
        "what have you learned",
        "what have we discussed",
        "what did we talk about",
        "show me your memory",
        "show your memory",
        "tell me what you remember",
        "do you remember",
    )
    return any(phrase in text for phrase in phrases)
