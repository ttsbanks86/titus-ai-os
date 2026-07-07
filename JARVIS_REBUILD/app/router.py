from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.config import AppConfig
from app.intents import (
    CAPABILITIES,
    EXIT,
    GREETING,
    NOISE,
    OPENCLAW,
    OBSIDIAN,
    EMAIL,
    NOTION,
    BROWSER,
    BASIC_CHAT,
    BRIEFING,
    SYSTEM_CONTROL,
    MEMORY_STORE,
    MEMORY_QUERY,
    CALENDAR,
    FILE_CREATE,
    FILE_APPEND,
    SELF_SPEECH,
    STOP,
    SYSTEM_QUESTION,
    UNKNOWN,
    WEATHER,
    Intent,
    classify_intent,
)
from app.memory.short_term import ShortTermMemory
from app.memory.persistent import get_memory
from app.tools.capabilities import capabilities_response
from app.tools.approval import (
    approval_prompt,
    approved_response,
    canceled_response,
    detect_pending_action,
    is_approval,
    is_cancel,
    PendingAction,
)
from app.tools.openclaw import handle_openclaw_task
from app.tools.llm import llm_response
from app.tools.status import looks_like_status_question, system_status_response
from app.tools.obsidian import obsidian_response
from app.tools.email import email_response
from app.tools.notion import notion_response
from app.tools.browser import browser_response
from app.tools.briefing import briefing_response
from app.tools.system_control import system_control_response
from app.tools.web_search import (
    looks_like_current_event_question,
    extract_search_query_from_text,
    web_search,
    format_search_results_for_llm,
)
from app.voice.sound_effects import SoundEffectPlayer
from app.tools.calendar import calendar_response
from app.tools.files import file_creation_response, file_append_response
from app.tools.system import exit_response, stop_response
from app.tools.weather import weather_response
from app.security import redact_secrets


@dataclass(frozen=True)
class RouteResult:
    intent: str
    route: str
    response: str
    speak: bool = True
    should_exit: bool = False
    rejected: bool = False
    used_openclaw: bool = False
    reason: str = ""


class Router:
    def __init__(self, config: AppConfig, memory: ShortTermMemory | None = None) -> None:
        self.config = config
        self.memory = memory or ShortTermMemory()
        self.persistent_memory = get_memory()
        self.config.logs_dir.mkdir(parents=True, exist_ok=True)
        self.sound_player = SoundEffectPlayer.from_config(config)

    def handle(self, text: str, *, source: str = "user", metadata: dict | None = None) -> RouteResult:
        recent_speech = self.memory.recent_assistant_speech(self.config.self_speech_window_seconds)
        # Remember the user's input for multi-turn conversation context.
        # Skip noise and self-speech so the conversation history stays clean.
        if source == "user" and text.strip():
            self.memory.remember_user_input(text)
            # Log to persistent memory
            self.persistent_memory.log_turn("user", text, metadata=metadata)
        intent = classify_intent(
            text,
            recent_assistant_speech=recent_speech,
            source=source,
            assistant_name=self.config.assistant_name,
        )
        result = self._approval_gate(text, intent)
        if result is None:
            result = self._route_intent(intent)
        self._audit(text, intent, result, source=source, metadata=metadata)
        if result.speak and result.response:
            self.memory.remember_assistant_speech(result.response)
            # Log assistant response to persistent memory
            self.persistent_memory.log_turn("assistant", result.response)
        return result

    def _approval_gate(self, text: str, intent: Intent) -> RouteResult | None:
        if intent.name in {NOISE, SELF_SPEECH}:
            return None

        if self.memory.pending_action is not None:
            if is_approval(text):
                action = self.memory.clear_pending_action()
                if action is not None:
                    return RouteResult(
                        intent="approval_confirmed",
                        route="approval",
                        response=approved_response(action),
                        reason="pending action approved",
                    )
            if is_cancel(text):
                action = self.memory.clear_pending_action()
                if action is not None:
                    return RouteResult(
                        intent="approval_canceled",
                        route="approval",
                        response=canceled_response(action),
                        reason="pending action canceled",
                    )
            return RouteResult(
                intent="approval_pending",
                route="approval",
                response="Approval is still pending. Say 'yes, approve' to approve, or 'cancel' to discard.",
                reason="pending action awaiting approval",
            )

        action = detect_pending_action(text)
        if action is None:
            return None
        self.memory.set_pending_action(action)
        return RouteResult(
            intent="approval_required",
            route="approval",
            response=approval_prompt(action),
            reason="risky action requires approval",
        )

    def _route_intent(self, intent: Intent) -> RouteResult:
        if intent.name in {NOISE, SELF_SPEECH}:
            return RouteResult(
                intent=intent.name,
                route="noise_rejection",
                response="",
                speak=False,
                rejected=True,
                reason=intent.reason,
            )
        if intent.name == STOP:
            return RouteResult(STOP, "system", stop_response(), reason=intent.reason)
        if intent.name == EXIT:
            return RouteResult(EXIT, "system", exit_response(), should_exit=True, reason=intent.reason)
        if intent.name == CAPABILITIES:
            return RouteResult(CAPABILITIES, "capabilities", capabilities_response(self.config), reason=intent.reason)
        if intent.name == WEATHER:
            return RouteResult(WEATHER, "weather", weather_response(self.config), reason=intent.reason)
        if intent.name == OBSIDIAN:
            return RouteResult(OBSIDIAN, "obsidian", obsidian_response(self.config, intent.text), reason=intent.reason)
        if intent.name == EMAIL:
            return RouteResult(EMAIL, "email", email_response(self.config, intent.text), reason=intent.reason)
        if intent.name == NOTION:
            return RouteResult(NOTION, "notion", notion_response(self.config, intent.text), reason=intent.reason)
        if intent.name == CALENDAR:
            return RouteResult(CALENDAR, "calendar", calendar_response(self.config, intent.text), reason=intent.reason)
        if intent.name == FILE_CREATE:
            file_result = file_creation_response(self.config, intent.text)
            if file_result.approval_required:
                self.memory.set_pending_action(PendingAction(file_result.action_type, file_result.response, intent.text))
            return RouteResult(
                FILE_CREATE,
                "approval" if file_result.approval_required else "files",
                file_result.response,
                speak=True,
                rejected=file_result.blocked,
                reason="file creation requires approval" if file_result.approval_required else intent.reason,
            )
        if intent.name == FILE_APPEND:
            file_result = file_append_response(self.config, intent.text)
            if file_result.approval_required:
                self.memory.set_pending_action(PendingAction(file_result.action_type, file_result.response, intent.text))
            return RouteResult(
                FILE_APPEND,
                "approval" if file_result.approval_required else "files",
                file_result.response,
                speak=True,
                rejected=file_result.blocked,
                reason="file append requires approval" if file_result.approval_required else intent.reason,
            )
        if intent.name == BROWSER:
            return RouteResult(BROWSER, "browser", browser_response(self.config, intent.text), reason=intent.reason)
        if intent.name == BRIEFING:
            return RouteResult(BRIEFING, "briefing", briefing_response(self.config), reason=intent.reason)
        if intent.name == MEMORY_STORE:
            # Extract the fact to remember from the command
            fact_content = self._extract_memory_fact(intent.text)
            if fact_content:
                self.persistent_memory.add_key_fact(
                    category="user_note",
                    content=fact_content,
                    source="explicit_remember_command"
                )
                response = f"I'll remember that. {fact_content}"
            else:
                response = "What would you like me to remember?"
            return RouteResult(MEMORY_STORE, "memory_store", response, reason=intent.reason)
        if intent.name == MEMORY_QUERY:
            # Re-load key facts from file to get the latest data
            self.persistent_memory.key_facts = self.persistent_memory._load_key_facts()
            
            # Extract the actual query from the text
            import re
            query = intent.text.strip().lower()
            # Remove assistant name prefixes
            query = re.sub(r'^(jarvis|hey jarvis|okay jarvis|ok jarvis|please)[,\s]+', '', query)
            # Remove the trigger phrases themselves
            query = query.replace('what do you remember', '')
            query = query.replace('do you remember', '')
            query = query.replace('tell me what you remember', '')
            # Remove trailing question marks and punctuation
            query = query.rstrip('?.!,').strip()
            
            # Determine what to show
            if not query or len(query) <= 3:
                # Broad query, no specifics - return all memories
                facts = list(self.persistent_memory.key_facts)
            else:
                # Search for specific topic
                facts = self.persistent_memory.search_key_facts(query)
                # If no direct matches but query has meaningful keywords, 
                # return all memories as fallback (user is asking broadly)
                if not facts:
                    query_words = [w for w in re.findall(r'\w+', query) if len(w) > 3]
                    if any(w in ['memory', 'memories', 'remember', 'everything', 'all'] for w in query_words):
                        facts = list(self.persistent_memory.key_facts)
            
            if facts:
                if len(facts) == 1:
                    response = f"I remember: {facts[0].content}"
                else:
                    response_parts = [f"I remember {len(facts)} things:"]
                    for fact in facts[-10:]:  # Show last 10 at most
                        response_parts.append(f"- {fact.content}")
                    response = " ".join(response_parts)
            else:
                # Check if there are any memories at all
                all_facts = self.persistent_memory.key_facts
                if all_facts:
                    response = f"I have {len(all_facts)} memories total but none specifically match '{query}'. Available memories: " + "; ".join(f.content for f in all_facts[-5:])
                else:
                    response = "I don't have any memories stored yet. You can tell me to remember things by saying 'remember that...' or 'don't forget that...'"
            return RouteResult(MEMORY_QUERY, "memory_query", response, reason=intent.reason)
        if intent.name == SYSTEM_CONTROL:
            sc_result = system_control_response(self.config, intent.text)
            if sc_result.approval_required:
                self.memory.set_pending_action(PendingAction(sc_result.action_type, sc_result.response, intent.text))
            return RouteResult(
                SYSTEM_CONTROL,
                "approval" if sc_result.approval_required else "system_control",
                sc_result.response,
                speak=True,
                rejected=sc_result.blocked,
                reason="system control requires approval" if sc_result.approval_required else intent.reason,
            )
        if intent.name == GREETING:
            return RouteResult(GREETING, "greeting", "Hello. I'm here.", reason=intent.reason)
        if intent.name == OPENCLAW:
            selection_reason = f"{intent.reason}; selected OpenClaw boundary for coding/debugging/build/planning task"
            self.sound_player.play_thinking_sound()
            openclaw_result = handle_openclaw_task(intent.text, self.config, selection_reason=selection_reason)
            return RouteResult(
                OPENCLAW,
                "openclaw",
                openclaw_result.response,
                used_openclaw=openclaw_result.used,
                reason=openclaw_result.selection_reason or selection_reason,
            )
        if intent.name == SYSTEM_QUESTION and looks_like_status_question(intent.cleaned_text):
            return RouteResult(
                SYSTEM_QUESTION,
                "system_status",
                system_status_response(self.config),
                reason=intent.reason,
            )
        if intent.name in {BASIC_CHAT, SYSTEM_QUESTION, UNKNOWN}:
            # Play the thinking sound effect while processing (non-blocking,
            # plays in background while the LLM generates the response)
            self.sound_player.play_thinking_sound()
            # RAG: if the question needs current data, search the web first
            # and feed the results into the LLM prompt as context.
            web_context = ""
            if looks_like_current_event_question(intent.text):
                search_query = extract_search_query_from_text(intent.text)
                if search_query:
                    try:
                        results = web_search(search_query)
                        if results:
                            web_context = format_search_results_for_llm(results, search_query)
                    except Exception:
                        pass  # Web search is best-effort; don't fail the LLM call

            conversation_context = self.memory.conversation_summary()
            llm_result = llm_response(
                self.config,
                intent.text,
                conversation_context=conversation_context,
                web_context=web_context,
            )
            route = "llm" if llm_result.used else "fallback"
            response = llm_result.response
            if web_context and llm_result.used:
                reason = f"{intent.reason}; {llm_result.reason}; web_rag"
            else:
                reason = f"{intent.reason}; {llm_result.reason}"
            return RouteResult(
                intent.name,
                route,
                response,
                reason=reason,
            )
        if intent.name == UNKNOWN:
            return RouteResult(
                UNKNOWN,
                "fallback",
                "I heard you, but I do not have a reliable handler for that yet.",
                reason=intent.reason,
            )
        return RouteResult(UNKNOWN, "fallback", "I do not know how to handle that yet.", reason=intent.reason)

    def _audit(
        self,
        raw_text: str,
        intent: Intent,
        result: RouteResult,
        *,
        source: str,
        metadata: dict | None,
    ) -> None:
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": source,
            "raw_text": redact_secrets(raw_text),
            "metadata": redact_secrets(metadata or {}),
            "intent": redact_secrets(asdict(intent)),
            "result": redact_secrets(asdict(result)),
        }
        _append_jsonl(self.config.audit_log_path, record)

    def _extract_memory_fact(self, text: str) -> str | None:
        """Extract the fact content from a 'remember that...' command.
        
        Examples:
        - "remember that I prefer the Sekuru voice" -> "I prefer the Sekuru voice"
        - "Jarvis, remember this: my interview is Friday" -> "My interview is Friday"
        - "don't forget I like dark mode" -> "I like dark mode"
        """
        text = text.strip()
        # Remove common prefixes
        prefixes = [
            "jarvis,",
            "okay jarvis,",
            "hey jarvis,",
            "ok jarvis,",
            "please",
        ]
        for prefix in prefixes:
            if text.lower().startswith(prefix):
                text = text[len(prefix):].strip()
                break

        # Remove "remember that" / "remember this:" etc.
        patterns = [
            r"^remember\s+that\s+",
            r"^remember\s+this[:\s]+",
            r"^remember\s+the\s+",
            r"^don't\s+forget\s+(that\s+)?",
            r"^dont\s+forget\s+(that\s+)?",
            r"^keep\s+in\s+mind\s+(that\s+)?",
            r"^keep\s+this\s+in\s+mind\s*[:\s]*",
            r"^note\s+that\s+",
            r"^make\s+a\s+note[:\s]+",
            r"^save\s+this[:\s]+",
            r"^store\s+this[:\s]+",
            r"^remember\s+my\s+",
            r"^remember\s+i\s+",
            r"^remember\s+when\s+",
        ]
        for pattern in patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                text = text[match.end():].strip()
                break

        return text if text else None


def _append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")
