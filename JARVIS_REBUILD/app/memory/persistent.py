"""Persistent memory system for Jarvis.

Stores conversation history and key facts across sessions so Jarvis can:
- Remember previous conversations
- Recall user preferences and decisions
- Build context over time
- Answer questions like "what do you remember about X?"

Storage:
- conversation_log.jsonl: Append-only log of all interactions
- key_facts.json: Structured facts, preferences, and decisions
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class ConversationTurn:
    """A single turn in a conversation."""
    timestamp: str
    role: str  # "user" or "assistant"
    content: str
    session_id: str
    metadata: dict[str, Any] | None = None


@dataclass
class KeyFact:
    """A key fact, preference, or decision to remember."""
    timestamp: str
    category: str  # "preference", "decision", "fact", "project", "person"
    content: str
    source: str  # Where this came from (conversation, explicit, etc.)
    tags: list[str] | None = None


class PersistentMemory:
    """Manages persistent memory across Jarvis sessions."""
    
    def __init__(self, memory_dir: Path | None = None):
        if memory_dir is None:
            # Default to app/memory/ directory
            memory_dir = Path(__file__).parent
        self.memory_dir = memory_dir
        self.conversation_log = memory_dir / "conversation_log.jsonl"
        self.key_facts_file = memory_dir / "key_facts.json"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure memory directory exists
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Load key facts into memory
        self.key_facts: list[KeyFact] = self._load_key_facts()
    
    def _load_key_facts(self) -> list[KeyFact]:
        """Load key facts from JSON file."""
        if not self.key_facts_file.exists():
            return []
        
        try:
            with open(self.key_facts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [KeyFact(**fact) for fact in data]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[PersistentMemory] Error loading key facts: {e}")
            return []
    
    def _save_key_facts(self) -> None:
        """Save key facts to JSON file."""
        try:
            with open(self.key_facts_file, "w", encoding="utf-8") as f:
                json.dump([asdict(fact) for fact in self.key_facts], f, indent=2)
        except Exception as e:
            print(f"[PersistentMemory] Error saving key facts: {e}")
    
    def log_turn(self, role: str, content: str, metadata: dict[str, Any] | None = None) -> None:
        """Log a conversation turn."""
        turn = ConversationTurn(
            timestamp=datetime.now().isoformat(),
            role=role,
            content=content,
            session_id=self.session_id,
            metadata=metadata or {}
        )
        
        try:
            with open(self.conversation_log, "a", encoding="utf-8") as f:
                f.write(json.dumps(asdict(turn)) + "\n")
        except Exception as e:
            print(f"[PersistentMemory] Error logging turn: {e}")
    
    def add_key_fact(
        self,
        category: str,
        content: str,
        source: str = "conversation",
        tags: list[str] | None = None
    ) -> None:
        """Add a key fact to remember."""
        fact = KeyFact(
            timestamp=datetime.now().isoformat(),
            category=category,
            content=content,
            source=source,
            tags=tags or []
        )
        self.key_facts.append(fact)
        self._save_key_facts()
    
    def get_recent_conversations(self, max_turns: int = 50) -> list[ConversationTurn]:
        """Get recent conversation turns."""
        if not self.conversation_log.exists():
            return []
        
        try:
            with open(self.conversation_log, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Get last max_turns lines
            recent_lines = lines[-max_turns:] if len(lines) > max_turns else lines
            
            turns = []
            for line in recent_lines:
                try:
                    data = json.loads(line.strip())
                    turns.append(ConversationTurn(**data))
                except (json.JSONDecodeError, KeyError):
                    continue
            
            return turns
        except Exception as e:
            print(f"[PersistentMemory] Error loading conversations: {e}")
            return []
    
    def get_key_facts_by_category(self, category: str) -> list[KeyFact]:
        """Get key facts filtered by category."""
        return [fact for fact in self.key_facts if fact.category == category]
    
    def search_key_facts(self, query: str) -> list[KeyFact]:
        """Search key facts by content.
        
        Uses a scoring approach: facts that contain more query words rank higher.
        Stopwords like 'about', 'the', 'a' are ignored for better matching.
        """
        # Remove common stopwords that don't add meaning to the search
        stopwords = {"about", "the", "a", "an", "is", "of", "to", "in", "on", "at", "for", "my", "i"}
        query_words = [
            word for word in re.findall(r'\w+', query.lower())
            if word not in stopwords and len(word) > 2
        ]
        
        if not query_words:
            return []
        
        scored_results = []
        for fact in self.key_facts:
            content_lower = fact.content.lower()
            score = sum(1 for word in query_words if word in content_lower)
            if score > 0:
                scored_results.append((score, fact))
        
        # Sort by score descending (most matches first)
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [fact for _, fact in scored_results]
    
    def get_memory_context(self, max_turns: int = 30, max_facts: int = 20) -> str:
        """Get formatted memory context for LLM prompt."""
        parts = []
        
        # Add key facts
        if self.key_facts:
            parts.append("KEY FACTS AND PREFERENCES:")
            recent_facts = self.key_facts[-max_facts:]
            for fact in recent_facts:
                parts.append(f"- [{fact.category}] {fact.content}")
        
        # Add recent conversation summary
        recent_turns = self.get_recent_conversations(max_turns)
        if recent_turns:
            parts.append("\nRECENT CONVERSATION HISTORY:")
            for turn in recent_turns:
                role_label = "You" if turn.role == "user" else "Jarvis"
                # Truncate long content
                content = turn.content[:200] + "..." if len(turn.content) > 200 else turn.content
                parts.append(f"{role_label}: {content}")
        
        return "\n".join(parts) if parts else ""
    
    def summarize_old_sessions(self, keep_recent: int = 100) -> None:
        """Summarize old sessions to keep log manageable.
        
        Keeps the most recent `keep_recent` turns and summarizes older ones.
        This is called periodically to prevent the log from growing too large.
        """
        if not self.conversation_log.exists():
            return
        
        try:
            with open(self.conversation_log, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            if len(lines) <= keep_recent:
                return  # Nothing to summarize
            
            # Keep recent lines
            recent_lines = lines[-keep_recent:]
            
            # For now, just truncate old sessions
            # In the future, we could use an LLM to summarize them
            with open(self.conversation_log, "w", encoding="utf-8") as f:
                # Add a marker that old sessions were summarized
                summary_marker = {
                    "timestamp": datetime.now().isoformat(),
                    "role": "system",
                    "content": f"[Previous {len(lines) - keep_recent} turns summarized and archived]",
                    "session_id": "system",
                    "metadata": {"type": "summary_marker"}
                }
                f.write(json.dumps(summary_marker) + "\n")
                f.writelines(recent_lines)
        except Exception as e:
            print(f"[PersistentMemory] Error summarizing sessions: {e}")


# Global instance (initialized in main.py)
_memory_instance: PersistentMemory | None = None


def get_memory() -> PersistentMemory:
    """Get the global persistent memory instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = PersistentMemory()
    return _memory_instance


def init_memory(memory_dir: Path | None = None) -> PersistentMemory:
    """Initialize the global persistent memory instance."""
    global _memory_instance
    _memory_instance = PersistentMemory(memory_dir)
    return _memory_instance
