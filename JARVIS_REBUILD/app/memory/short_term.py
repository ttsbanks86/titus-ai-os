from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field

from app.tools.approval import PendingAction


@dataclass
class ConversationTurn:
    role: str  # "user" or "assistant"
    text: str
    timestamp: float = field(default_factory=time.time)


@dataclass
class ShortTermMemory:
    last_assistant_speech: str | None = None
    last_assistant_speech_at: float = 0.0
    pending_action: PendingAction | None = None
    # Conversation history for multi-turn context. We keep a bounded deque so
    # old turns roll off automatically. The LLM sees recent turns as context.
    conversation_history: deque = field(default_factory=lambda: deque(maxlen=20))

    def remember_assistant_speech(self, text: str) -> None:
        self.last_assistant_speech = text
        self.last_assistant_speech_at = time.time()
        if text:
            self.conversation_history.append(ConversationTurn(role="assistant", text=text))

    def remember_user_input(self, text: str) -> None:
        if text:
            self.conversation_history.append(ConversationTurn(role="user", text=text))

    def recent_assistant_speech(self, window_seconds: float) -> str | None:
        if not self.last_assistant_speech:
            return None
        if time.time() - self.last_assistant_speech_at > window_seconds:
            return None
        return self.last_assistant_speech

    def conversation_summary(self, max_turns: int = 10) -> str:
        """Return a formatted string of recent conversation turns for the LLM.
        Used to give the LLM multi-turn context so it can reference things the
        user said earlier without forgetting.
        """
        if not self.conversation_history:
            return ""
        turns = list(self.conversation_history)[-max_turns:]
        if len(turns) < 2:
            return ""
        parts: list[str] = ["Recent conversation:"]
        for turn in turns:
            label = "Titus" if turn.role == "user" else "Jarvis"
            # Cap each turn to keep the prompt size reasonable
            text = turn.text
            if len(text) > 200:
                text = text[:197].rstrip() + "..."
            parts.append(f"{label}: {text}")
        return "\n".join(parts)

    def set_pending_action(self, action: PendingAction) -> None:
        self.pending_action = action

    def clear_pending_action(self) -> PendingAction | None:
        action = self.pending_action
        self.pending_action = None
        return action
