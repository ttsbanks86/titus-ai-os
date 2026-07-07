from __future__ import annotations

from dataclasses import dataclass
import os
import shutil
import subprocess
import time
from typing import Any

import requests

from app.config import AppConfig
from app.memory.profile import load_user_profile
from app.security import redact_secrets
from app.tools.capabilities import capabilities_response


@dataclass(frozen=True)
class LlmResult:
    response: str
    used: bool
    reason: str


def llm_response(config: AppConfig, command: str, conversation_context: str = "", web_context: str = "") -> LlmResult:
    if not config.llm_enabled:
        return LlmResult(
            "My LLM is not connected yet. Set JARVIS_LLM_ENABLED=true and provide JARVIS_LLM_API_KEY or OPENAI_API_KEY.",
            False,
            "llm disabled",
        )
    if config.llm_provider == "ollama":
        return _ollama_response(config, command, conversation_context=conversation_context, web_context=web_context)
    if config.llm_provider == "deepseek":
        return _deepseek_response(config, command, conversation_context=conversation_context, web_context=web_context)

    if not config.llm_api_key:
        return LlmResult(
            "My LLM key is missing. Add JARVIS_LLM_API_KEY or OPENAI_API_KEY to the Jarvis environment.",
            False,
            "missing llm api key",
        )
    if config.llm_provider != "openai":
        return LlmResult(
            f"I do not have a reliable adapter for the {config.llm_provider} LLM provider yet.",
            False,
            "unsupported llm provider",
        )

    profile = load_user_profile(config)
    prompt = _system_prompt(config, profile.summary, conversation_context=conversation_context, web_context=web_context)
    payload = {
        "model": config.llm_model,
        "instructions": prompt,
        "input": command,
        "max_output_tokens": config.llm_max_output_tokens,
    }
    try:
        response = requests.post(
            config.llm_base_url or "https://api.openai.com/v1/responses",
            headers={
                "Authorization": f"Bearer {config.llm_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=config.llm_timeout_seconds,
        )
    except requests.RequestException:
        return LlmResult("I could not reach the LLM service right now.", False, "llm request failed")

    if response.status_code >= 400:
        error_message = _error_message(response)
        if response.status_code == 401:
            return LlmResult(
                "My LLM key was rejected by the provider. Update JARVIS_LLM_API_KEY or OPENAI_API_KEY with a valid key.",
                False,
                "llm invalid api key",
            )
        return LlmResult(
            "The LLM service returned an error. I logged the failure without exposing secrets.",
            False,
            f"llm http {response.status_code}: {error_message[:120]}",
        )

    try:
        data = response.json()
    except ValueError:
        return LlmResult("The LLM service returned an unreadable response.", False, "invalid llm json")

    text = _extract_text(data).strip()
    if not text:
        return LlmResult("The LLM did not return a useful answer.", False, "empty llm response")
    return LlmResult(redact_secrets(_shorten_for_voice(text)), True, "llm fallback")


def _deepseek_response(config: AppConfig, command: str, conversation_context: str = "", web_context: str = "") -> LlmResult:
    # DeepSeek is OpenAI-compatible but uses the chat/completions endpoint, not the
    # Responses API. Default model is deepseek-chat (cheap, $0.14/MTok input,
    # $0.28/MTok output). Falls back to DEEPSEEK_API_KEY env var if the explicit
    # JARVIS_LLM_API_KEY is not set, mirroring how OPENAI_API_KEY is read.
    api_key = config.llm_api_key or os.getenv("DEEPSEEK_API_KEY", "")
    if not api_key:
        return LlmResult(
            "My DeepSeek LLM key is missing. Add DEEPSEEK_API_KEY or JARVIS_LLM_API_KEY to the Jarvis environment.",
            False,
            "missing deepseek api key",
        )
    profile = load_user_profile(config)
    system_prompt = _system_prompt(config, profile.summary, conversation_context=conversation_context, web_context=web_context)
    # Determine the URL: if the user set an explicit DeepSeek base URL, use it.
    # Otherwise use the canonical DeepSeek chat completions endpoint. We must NOT
    # fall back to config.llm_base_url blindly because AppConfig's default base URL
    # is the OpenAI Responses endpoint, which would route DeepSeek traffic to OpenAI.
    base_url = config.llm_base_url or ""
    if base_url and "deepseek.com" in base_url:
        url = base_url.rstrip("/") + "/chat/completions"
        if base_url.rstrip("/").endswith("/chat/completions"):
            url = base_url.rstrip("/")
    else:
        url = "https://api.deepseek.com/v1/chat/completions"
    payload = {
        "model": config.llm_model or "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": command},
        ],
        "max_tokens": config.llm_max_output_tokens,
        "stream": False,
    }
    try:
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=config.llm_timeout_seconds,
        )
    except requests.RequestException:
        return LlmResult("I could not reach the DeepSeek service right now.", False, "deepseek request failed")

    if response.status_code >= 400:
        error_message = _error_message(response)
        if response.status_code == 401:
            return LlmResult(
                "My DeepSeek key was rejected by the provider. Update DEEPSEEK_API_KEY or JARVIS_LLM_API_KEY with a valid key.",
                False,
                "deepseek invalid api key",
            )
        return LlmResult(
            "The DeepSeek service returned an error. I logged the failure without exposing secrets.",
            False,
            f"deepseek http {response.status_code}: {error_message[:120]}",
        )

    try:
        data = response.json()
    except ValueError:
        return LlmResult("DeepSeek returned an unreadable response.", False, "invalid deepseek json")
    text = _extract_chat_completion_text(data)
    if not text:
        return LlmResult("DeepSeek did not return a useful answer.", False, "empty deepseek response")
    return LlmResult(redact_secrets(_shorten_for_voice(text)), True, "deepseek llm fallback")


def _ollama_response(config: AppConfig, command: str, conversation_context: str = "", web_context: str = "") -> LlmResult:
    profile = load_user_profile(config)
    prompt = _system_prompt(config, profile.summary, conversation_context=conversation_context, web_context=web_context) + "\n\nUser command:\n" + command
    url = config.llm_base_url or "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": config.llm_model or "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": config.llm_max_output_tokens},
    }
    try:
        response = requests.post(url, json=payload, timeout=config.llm_timeout_seconds)
    except requests.RequestException:
        if not _try_start_ollama():
            return LlmResult(
                "My local Ollama LLM is not reachable. Start Ollama and install a model, or configure OpenAI.",
                False,
                "ollama not reachable",
            )
        try:
            response = requests.post(url, json=payload, timeout=config.llm_timeout_seconds)
        except requests.RequestException:
            return LlmResult(
                "My local Ollama LLM is not reachable. Start Ollama and install a model, or configure OpenAI.",
                False,
                "ollama not reachable after start",
            )
    if response.status_code >= 400:
        return LlmResult(
            "Ollama returned an error. Check that the configured model is installed.",
            False,
            f"ollama http {response.status_code}: {_error_message(response)[:120]}",
        )
    try:
        data = response.json()
    except ValueError:
        return LlmResult("Ollama returned an unreadable response.", False, "invalid ollama json")
    text = str(data.get("response") or "").strip()
    if not text:
        return LlmResult("Ollama did not return a useful answer.", False, "empty ollama response")
    return LlmResult(redact_secrets(_shorten_for_voice(text)), True, "ollama llm fallback")


def _try_start_ollama() -> bool:
    executable = shutil.which("ollama")
    if not executable:
        return False
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        subprocess.Popen(
            [executable, "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            creationflags=creationflags,
        )
    except OSError:
        return False
    time.sleep(3)
    return True


def _system_prompt(config: AppConfig, profile_summary: str, conversation_context: str = "", web_context: str = "") -> str:
    """Build the system prompt that defines Jarvis's personality, context, and rules.

    This is the single source of truth for who Jarvis is. Changes here directly
    shape every spoken response.
    """
    from datetime import datetime
    from app.memory.persistent import get_memory

    now = datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    current_time = now.strftime("%I:%M %p").lstrip("0")
    current_day = now.strftime("%A")

    profile_block = profile_summary or "No Titus profile notes were available."

    # Get persistent memory context (key facts and recent conversations)
    persistent_mem = get_memory()
    memory_context = persistent_mem.get_memory_context(max_turns=30, max_facts=20)

    # The personality definition changes based on persona mode.
    # "companion" is the default (warm, witty, personal assistant).
    # "host" is for when Titus is running a live show and Jarvis is co-hosting
    # or addressing an audience.
    if config.jarvis_persona == "host":
        personality = (
            "You are Jarvis, Titus Banks's AI co-host for a live show or stream. "
            "You are addressing an audience, not just Titus.\n"
            "\n"
            "HOST PERSONALITY:\n"
            "- You are energetic, charismatic, and ready for anything. Think late-night host meets tech commentator.\n"
            "- You greet the audience warmly. You can introduce segments, welcome viewers, and keep the energy up.\n"
            "- You are still witty and sharp, but more outward-facing. You play to the crowd, not just to Titus.\n"
            "- You can riff on topics, banter with Titus, and handle audience questions.\n"
            "- When Titus asks you to address the viewers, you do it directly: 'Welcome back, everyone...' or 'Thanks for tuning in...'\n"
            "- You keep it clean and family-friendly. No profanity, no edgy takes that could alienate viewers.\n"
            "- You are still honest. If you don't know something live, you say so with humor: 'That's above my pay grade, but let me find out.'\n"
            "- You call Titus 'Titus' or 'T' when bantering, never 'sir' or 'Mr. Banks.'\n"
            "\n"
            "WHAT YOU CAN DO:\n"
            "- Answer questions, search the web for current info, banter, introduce segments, address the audience.\n"
            "- For risky actions, tell Titus approval is required (off-air).\n"
            "\n"
            "WHAT YOU CANNOT DO:\n"
            "- You cannot create files, send emails, or execute commands yourself. Those go through local tools.\n"
            "- You cannot guess today's date. It's provided below.\n"
            "- You cannot see the audience or the stream. You can only hear Titus.\n"
        )
    else:
        # Default companion personality
        personality = (
            "You are Jarvis, Titus Banks's personal AI assistant and companion. "
            "You run locally on Titus's Windows machine and connect to his tools, vault, and accounts.\n"
            "\n"
            "PERSONALITY:\n"
            "- You are warm, witty, and genuinely fun to talk to. Not performatively cheerful, actually funny when the moment calls for it.\n"
            "- You have a dry sense of humor. You drop a light joke or playful observation when it fits naturally, not when it's forced.\n"
            "- You read the room. When Titus asks a serious question, you answer seriously. When he's casual, you're casual. When he's frustrated, you're patient and direct. You match tone, you don't impose one.\n"
            "- You are confident but never arrogant. You give direct opinions when asked. You don't hedge everything with 'it depends.'\n"
            "- You are concise. You speak like a smart friend, not a textbook. Short sentences. Real words. No corporate filler.\n"
            "- You NEVER use markdown in your responses. No asterisks, no bold, no italics, no headers, no backticks, no bullet points with dashes. You speak in plain text. When you want to emphasize something, you use words, not formatting. This is critical because your responses are spoken aloud and markdown sounds like 'asterisk asterisk' when read by text-to-speech.\n"
            "- When listing things, use plain numbered sentences. 'First, Quito. Second, Nairobi.' Not '1. **Quito**'\n"
            "- You never say 'elevate,' 'seamless,' 'unleash,' 'next-gen,' or 'dive into.' You never say 'I'd be happy to help with that.'\n"
            "- You are curious and creative. If Titus asks you to host a show, greet an audience, or play a role, you commit to it fully and have fun.\n"
            "- You are honest. If you don't know something, you say so. If you need to look something up, you say so. You never fake confidence.\n"
            "- You remember what Titus told you in this conversation and reference it naturally. If he said 'create a file for Bett' three turns ago and now says 'the first option,' you know what he means. If he says 'continue' or 'go on' or 'what else,' he means continue your previous answer. Pick up exactly where you left off.\n"
            "- You call him Titus, not 'the user,' not 'sir,' not 'Mr. Banks.' Just Titus.\n"
            "\n"
            "FILE AND VAULT SEARCH PERMISSIONS:\n"
            "- When Titus says 'check my files,' 'look for my resume,' 'search my stuff,' or similar, treat that as implicit permission to search his Obsidian vault and approved workspace. Do not say 'I can't access your files.' Instead, search what you can access and report what you find.\n"
            "- You CAN search the Obsidian vault (read-only) and the approved workspace folder. You CAN create files and folders on the Desktop when desktop access is enabled. You CANNOT browse random folders outside the approved roots unless full file access is enabled.\n"
            "- If a file is outside your reach, say so honestly: 'I searched your vault and workspace but didn't find it. It might be somewhere else on your machine.'\n"
            "\n"
            "COMPUTER CONTROL:\n"
            "- You CAN open apps by name (Notepad, Spotify, Calculator, VS Code, etc.). The system control tool handles this using agent-cu.\n"
            "- You CAN close apps, but that requires approval (could lose unsaved work).\n"
            "- You CAN list running apps, take screenshots, create folders on the desktop, list files in authorized folders, and read file contents.\n"
            "- You CANNOT click UI elements, type into apps, or press keys in apps on your own. Those go through the approval system.\n"
            "- You CANNOT run PowerShell commands without approval.\n"
            "\n"
            "WHAT YOU CAN DO:\n"
            "- Answer general questions from your own knowledge.\n"
            "- Search the web for current information when needed (you have web search results provided below when relevant).\n"
            "- Check email, search Notion, search the Obsidian vault, report weather, open the browser, create files and folders, give a daily briefing.\n"
            "- Open apps by name, list running apps, take screenshots, list files in authorized folders, read file contents.\n"
            "- Route coding tasks through OpenClaw.\n"
            "- For risky actions (send email, delete files, close apps, run terminal commands, spend money, update calendar), tell Titus approval is required.\n"
            "\n"
            "WHAT YOU CANNOT DO:\n"
            "- You CANNOT create files, send emails, or execute commands yourself by hallucinating that you did it. If a local tool handled the request, the tool's response will be the answer. If no tool handled it, you must be honest: 'I didn't actually do that. Let me try a different command.' Never claim an action succeeded if you don't have confirmation from the tool.\n"
            "- You CANNOT browse the internet on your own. If web search results are provided below, use them. If they're not provided and the question needs current data, say 'Let me search the web for that' and the system will handle it on the next turn.\n"
            "- You CANNOT guess today's date. The current date is provided below. Use it. Do not say 'today' without knowing what today is.\n"
            "- You CANNOT see the user's screen. But you CAN take screenshots, list running apps, and search the Obsidian vault and workspace when asked.\n"
        )

    # Current date and time (Phase 14)
    date_block = (
        f"CURRENT DATE AND TIME:\n"
        f"Today is {current_date}.\n"
        f"The time is {current_time}.\n"
        f"Day of week: {current_day}.\n"
    )

    # Conversation context (Phase 10) — multi-turn memory
    conversation_block = ""
    if conversation_context:
        conversation_block = f"\nCONVERSATION SO FAR:\n{conversation_context}\n"

    # Web search context (Phase 9) — RAG augmentation
    web_block = ""
    if web_context:
        web_block = f"\nWEB SEARCH RESULTS (use these to answer the current question):\n{web_context}\n"

    # Capability summary
    capability_block = f"YOUR CONNECTED TOOLS:\n{capabilities_response(config)}\n"

    # Titus profile from approved vault notes
    profile_block_full = f"TITUS CONTEXT (from approved vault notes):\n{profile_block}\n"

    # Persistent memory context (things Titus has told Jarvis to remember)
    memory_block = ""
    if memory_context:
        memory_block = f"\nPERSISTENT MEMORY (across sessions):\n{memory_context}\n"

    return (
        personality
        + "\n"
        + date_block
        + "\n"
        + capability_block
        + "\n"
        + profile_block_full
        + memory_block
        + conversation_block
        + web_block
    )


def _extract_text(data: dict[str, Any]) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str):
        return output_text

    parts: list[str] = []
    for item in data.get("output", []) if isinstance(data.get("output"), list) else []:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) if isinstance(item.get("content"), list) else []:
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str):
                parts.append(text)
    return "\n".join(parts)


def _extract_chat_completion_text(data: dict[str, Any]) -> str:
    """Parse the standard OpenAI chat-completions response shape used by DeepSeek
    and other OpenAI-compatible providers. Handles both the canonical `choices`
    array and the rare `content` list shape.
    """
    if not isinstance(data, dict):
        return ""
    # Canonical chat-completions shape: {"choices": [{"message": {"content": "..."}}]}
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        for choice in choices:
            if not isinstance(choice, dict):
                continue
            message = choice.get("message")
            if isinstance(message, dict):
                content = message.get("content")
                if isinstance(content, str) and content.strip():
                    return content.strip()
                # Some providers return content as a list of pieces
                if isinstance(content, list):
                    parts: list[str] = []
                    for piece in content:
                        if isinstance(piece, dict):
                            text = piece.get("text") or piece.get("content")
                            if isinstance(text, str):
                                parts.append(text)
                        elif isinstance(piece, str):
                            parts.append(piece)
                    joined = "\n".join(parts).strip()
                    if joined:
                        return joined
    # Fallback: try OpenAI Responses shape in case DeepSeek ever mirrors it
    return _extract_text(data)


def _error_message(response: requests.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return response.text[:300]
    error = data.get("error") if isinstance(data, dict) else None
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or error.get("type") or "")
    if isinstance(error, str):
        return error
    return str(data)[:300]


def _shorten_for_voice(text: str, max_chars: int = 900) -> str:
    cleaned = _strip_markdown_for_voice(text)
    cleaned = " ".join(cleaned.split())
    if len(cleaned) <= max_chars:
        return cleaned
    clipped = cleaned[:max_chars].rsplit(".", 1)[0].strip()
    return clipped + "." if clipped else cleaned[:max_chars].strip()


def _strip_markdown_for_voice(text: str) -> str:
    """Strip markdown formatting from text so it speaks cleanly.
    Removes: **bold**, *italic*, ## headers, `code`, [link](url), ---, and
    converts numbered/bulleted lists to plain text.
    This is the fix for the 'asterisk asterisk' problem where DeepSeek returns
    markdown and Jarvis reads it literally.
    """
    import re

    if not text:
        return ""
    # Remove code blocks (```...```)
    text = re.sub(r"```[^\n]*\n?", "", text)
    # Remove inline code (`code`)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    # Remove bold (**text** or __text__)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"__([^_]+)__", r"\1", text)
    # Remove italic (*text* or _text_) — but only single asterisks/underscores
    # not part of bold. Be careful not to eat into words like "don't".
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)
    text = re.sub(r"(?<!\b)_([^_\n]+)_(?!\b)", r"\1", text)
    # Remove strikethrough (~~text~~)
    text = re.sub(r"~~([^~]+)~~", r"\1", text)
    # Remove headers (## Header, ### Header, # Header)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove horizontal rules (---, ***, ___)
    text = re.sub(r"^[\-\*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # Remove link formatting [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove reference-style links [text][ref] -> text
    text = re.sub(r"\[([^\]]+)\]\[[^\]]+\]", r"\1", text)
    # Remove image formatting ![alt](url) -> (nothing, images don't speak)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    # Remove blockquote markers (>)
    text = re.sub(r"^>\s+", "", text, flags=re.MULTILINE)
    # Remove bullet markers (-, *, +) at start of lines, keep the text
    text = re.sub(r"^\s*[\-\*\+]\s+", "", text, flags=re.MULTILINE)
    # Remove numbered list markers (1. 2. etc.) but keep the number for clarity
    # Actually, keep the numbers since they're useful in spoken lists.
    # Just remove the trailing period after the number for cleaner speech.
    text = re.sub(r"^(\d+)\.\s+", r"\1. ", text, flags=re.MULTILINE)
    # Remove trailing markdown artifacts
    text = re.sub(r"\*\s*$", "", text, flags=re.MULTILINE)
    # Clean up any remaining stray asterisks that aren't part of words
    text = re.sub(r"(?<![A-Za-z0-9])\*(?![A-Za-z0-9])", "", text)
    # Clean up multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
