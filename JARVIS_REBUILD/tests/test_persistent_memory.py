"""Tests for the persistent memory system."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from app.memory.persistent import (
    ConversationTurn,
    KeyFact,
    PersistentMemory,
    get_memory,
    init_memory,
)


def test_persistent_memory_initialization(tmp_path):
    """Test that PersistentMemory initializes and creates storage directory."""
    mem = PersistentMemory(memory_dir=tmp_path)
    assert mem.memory_dir == tmp_path
    assert mem.memory_dir.exists()
    assert mem.conversation_log.parent == tmp_path


def test_log_turn_creates_file(tmp_path):
    """Test that logging a turn creates the JSONL file."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.log_turn("user", "Hello Jarvis")
    assert mem.conversation_log.exists()
    content = mem.conversation_log.read_text(encoding="utf-8")
    assert "Hello Jarvis" in content
    assert "user" in content


def test_log_multiple_turns(tmp_path):
    """Test logging multiple conversation turns."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.log_turn("user", "What's the weather?")
    mem.log_turn("assistant", "It's sunny.")
    mem.log_turn("user", "Thanks!")
    
    content = mem.conversation_log.read_text(encoding="utf-8")
    lines = content.strip().split("\n")
    assert len(lines) == 3
    for line in lines:
        data = json.loads(line)
        assert "timestamp" in data
        assert "role" in data
        assert "content" in data


def test_add_key_fact(tmp_path):
    """Test adding a key fact to memory."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.add_key_fact(
        category="preference",
        content="User prefers dark mode",
        source="conversation"
    )
    assert len(mem.key_facts) == 1
    assert mem.key_facts[0].content == "User prefers dark mode"
    assert mem.key_facts[0].category == "preference"
    assert mem.key_facts_file.exists()


def test_key_facts_persistence(tmp_path):
    """Test that key facts are persisted to file and can be reloaded."""
    mem1 = PersistentMemory(memory_dir=tmp_path)
    mem1.add_key_fact("decision", "User chose Sekuru voice", "explicit")
    
    # Create a new instance and verify it loads the fact
    mem2 = PersistentMemory(memory_dir=tmp_path)
    assert len(mem2.key_facts) == 1
    assert mem2.key_facts[0].content == "User chose Sekuru voice"


def test_get_recent_conversations(tmp_path):
    """Test retrieving recent conversation turns."""
    mem = PersistentMemory(memory_dir=tmp_path)
    for i in range(5):
        mem.log_turn("user", f"Message {i}")
    
    recent = mem.get_recent_conversations(max_turns=10)
    assert len(recent) == 5
    assert recent[0].content == "Message 0"
    assert recent[4].content == "Message 4"


def test_get_recent_conversations_limit(tmp_path):
    """Test that get_recent_conversations respects the max_turns limit."""
    mem = PersistentMemory(memory_dir=tmp_path)
    for i in range(20):
        mem.log_turn("user", f"Message {i}")
    
    recent = mem.get_recent_conversations(max_turns=5)
    assert len(recent) == 5
    # Should return the LAST 5 messages
    assert recent[0].content == "Message 15"
    assert recent[4].content == "Message 19"


def test_search_key_facts(tmp_path):
    """Test searching key facts by content."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.add_key_fact("preference", "User likes dark mode", "conversation")
    mem.add_key_fact("preference", "User prefers Sekuru voice", "conversation")
    mem.add_key_fact("fact", "Project is in WGU", "conversation")
    
    # Search for "voice"
    results = mem.search_key_facts("voice")
    assert len(results) == 1
    assert "Sekuru" in results[0].content
    
    # Search for "dark"
    results = mem.search_key_facts("dark")
    assert len(results) == 1
    assert "dark mode" in results[0].content


def test_search_key_facts_with_stopwords(tmp_path):
    """Test that searches ignore stopwords for better matching."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.add_key_fact("decision", "we did a mock interview on Friday", "conversation")
    mem.add_key_fact("preference", "I prefer using the Sekuru voice", "conversation")
    
    # Search with stopwords like "about the"
    results = mem.search_key_facts("about the mock interview")
    assert len(results) == 1
    assert "mock interview" in results[0].content
    
    # Search with just "interview"
    results = mem.search_key_facts("interview")
    assert len(results) == 1
    
    # Search should rank more matches first
    mem.add_key_fact("fact", "The interview went well and I got good feedback", "conversation")
    results = mem.search_key_facts("interview feedback")
    assert len(results) >= 2
    # The fact with both "interview" and "feedback" should rank first
    assert "feedback" in results[0].content


def test_search_key_facts_no_matches(tmp_path):
    """Test that search returns empty when no matches."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.add_key_fact("decision", "I chose Sekuru voice", "conversation")
    
    results = mem.search_key_facts("kubernetes deployment")
    assert results == []


def test_get_key_facts_by_category(tmp_path):
    """Test filtering key facts by category."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.add_key_fact("preference", "User likes dark mode", "conversation")
    mem.add_key_fact("decision", "Chose Sekuru voice", "conversation")
    mem.add_key_fact("preference", "User wants ElevenLabs", "conversation")
    
    preferences = mem.get_key_facts_by_category("preference")
    assert len(preferences) == 2
    
    decisions = mem.get_key_facts_by_category("decision")
    assert len(decisions) == 1


def test_get_memory_context(tmp_path):
    """Test formatting memory context for LLM."""
    mem = PersistentMemory(memory_dir=tmp_path)
    mem.log_turn("user", "Hello")
    mem.log_turn("assistant", "Hi there!")
    mem.add_key_fact("preference", "User likes concise responses", "conversation")
    
    context = mem.get_memory_context(max_turns=10, max_facts=5)
    assert "KEY FACTS AND PREFERENCES" in context
    assert "User likes concise responses" in context
    assert "RECENT CONVERSATION HISTORY" in context
    assert "Hello" in context


def test_get_memory_context_empty(tmp_path):
    """Test memory context when there's nothing stored."""
    mem = PersistentMemory(memory_dir=tmp_path)
    context = mem.get_memory_context()
    assert context == ""


def test_global_memory_singleton(tmp_path, monkeypatch):
    """Test the global memory singleton pattern."""
    # Reset the singleton
    import app.memory.persistent as persistent_module
    persistent_module._memory_instance = None
    
    mem1 = init_memory(memory_dir=tmp_path)
    mem2 = get_memory()
    
    # Both should be the same instance
    assert mem1 is mem2
    assert persistent_module._memory_instance is mem1


def test_summarize_old_sessions(tmp_path):
    """Test that old sessions can be summarized to manage log size."""
    mem = PersistentMemory(memory_dir=tmp_path)
    for i in range(150):
        mem.log_turn("user", f"Message {i}")
    
    # Keep only the most recent 100
    mem.summarize_old_sessions(keep_recent=100)
    
    # Read the log and verify it has the marker + 100 recent lines
    lines = mem.conversation_log.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 101  # marker + 100 turns
    # First line should be the summary marker
    first_line = json.loads(lines[0])
    assert first_line["role"] == "system"
    assert "summarized" in first_line["content"].lower()


def test_memory_survives_router_restart(tmp_path, monkeypatch):
    """Integration test: memory survives a router restart (simulates session restart)."""
    import app.memory.persistent as persistent_module
    persistent_module._memory_instance = None
    
    # Session 1: store a fact
    mem1 = init_memory(memory_dir=tmp_path)
    mem1.add_key_fact("decision", "User picked Sekuru voice", "conversation")
    mem1.log_turn("user", "Remember my voice choice")
    
    # Session 2: reset singleton and create new instance (simulates process restart)
    persistent_module._memory_instance = None
    mem2 = init_memory(memory_dir=tmp_path)
    
    # Memory should persist across sessions
    assert len(mem2.key_facts) == 1
    assert mem2.key_facts[0].content == "User picked Sekuru voice"
    
    recent = mem2.get_recent_conversations()
    assert len(recent) == 1
    assert recent[0].content == "Remember my voice choice"