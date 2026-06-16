#!/usr/bin/env python3
"""Conversation context manager for AI Tutor."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

DATA_DIR = Path.home() / ".floating-ai-tutor"
CONTEXT_FILE = DATA_DIR / "conversation_context.json"


class ConversationContext:
    """Manages the current conversation thread."""

    def __init__(self, max_history: int = 20):
        self.max_history = max_history
        self.messages = []
        self.current_topic = ""
        self.last_captured_text = ""
        self._load()

    def _load(self):
        """Load conversation context from disk."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if CONTEXT_FILE.exists():
            try:
                data = json.loads(CONTEXT_FILE.read_text(encoding="utf-8"))
                self.messages = data.get("messages", [])
                self.current_topic = data.get("current_topic", "")
                self.last_captured_text = data.get("last_captured_text", "")
            except Exception:
                self.messages = []

    def save(self):
        """Save conversation context to disk."""
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = {
            "messages": self.messages[-self.max_history:],
            "current_topic": self.current_topic,
            "last_captured_text": self.last_captured_text,
            "updated_at": datetime.now().isoformat(),
        }
        CONTEXT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_message(self, role: str, content: str):
        """Add a message to the conversation."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        # Keep only recent history
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
        self.save()

    def set_topic(self, topic: str):
        """Set the current discussion topic."""
        self.current_topic = topic
        self.save()

    def set_captured_text(self, text: str):
        """Store the last captured screen text."""
        self.last_captured_text = text
        self.save()

    def get_context_for_prompt(self) -> str:
        """Format conversation history for AI prompt context."""
        if not self.messages:
            return ""

        context_lines = []
        for msg in self.messages[-10:]:  # Last 10 messages
            role = "User" if msg["role"] == "user" else "Tutor"
            content = msg["content"][:200]  # Truncate long messages
            context_lines.append(f"{role}: {content}")

        return "\n".join(context_lines)

    def get_follow_up_prompt(self, question: str) -> str:
        """Build a prompt that includes conversation context."""
        context = self.get_context_for_prompt()
        prompt_parts = []

        if self.last_captured_text:
            prompt_parts.append(f"Previously captured screen content:\n{self.last_captured_text[:500]}")

        if context:
            prompt_parts.append(f"Conversation history:\n{context}")

        prompt_parts.append(f"User's follow-up question: {question}")
        prompt_parts.append("Answer the question based on the captured content and conversation history. Be concise and helpful.")

        return "\n\n".join(prompt_parts)

    def clear(self):
        """Clear conversation context."""
        self.messages = []
        self.current_topic = ""
        self.last_captured_text = ""
        self.save()

    def get_summary(self) -> str:
        """Get a summary of the current conversation."""
        if not self.messages:
            return "No conversation history."

        topics = set()
        for msg in self.messages:
            if msg["role"] == "user":
                # Extract potential topic from first few words
                words = msg["content"][:50].split()
                if len(words) > 2:
                    topics.add(" ".join(words[:4]))

        return f"Conversation: {len(self.messages)} messages. Topics: {', '.join(list(topics)[:3]) or 'general'}"
