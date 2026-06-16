#!/usr/bin/env python3
"""Memory System — save and resume learning sessions."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

DATA_DIR = Path.home() / ".floating-ai-tutor"
SESSIONS_DIR = DATA_DIR / "sessions"


class SessionMemory:
    """Save and resume learning sessions."""

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)

    def save_session(self, name: str, data: dict) -> str:
        """Save a session to disk. Returns the session ID."""
        session_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session = {
            "id": session_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "data": data,
        }
        path = SESSIONS_DIR / f"{session_id}.json"
        path.write_text(json.dumps(session, indent=2, ensure_ascii=False), encoding="utf-8")
        return session_id

    def load_session(self, session_id: str) -> Optional[dict]:
        """Load a session by ID."""
        path = SESSIONS_DIR / f"{session_id}.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return None

    def list_sessions(self) -> list[dict]:
        """List all saved sessions, newest first."""
        sessions = []
        for file in sorted(SESSIONS_DIR.glob("*.json"), reverse=True):
            try:
                data = json.loads(file.read_text(encoding="utf-8"))
                sessions.append({
                    "id": data.get("id", file.stem),
                    "name": data.get("name", "Unknown"),
                    "created_at": data.get("created_at", ""),
                })
            except Exception:
                pass
        return sessions

    def get_latest_session(self) -> Optional[dict]:
        """Get the most recent session."""
        sessions = self.list_sessions()
        if sessions:
            return self.load_session(sessions[0]["id"])
        return None

    def delete_session(self, session_id: str):
        """Delete a session."""
        path = SESSIONS_DIR / f"{session_id}.json"
        if path.exists():
            path.unlink()

    def save_current_state(self, conversation, lesson_progress, captured_text=""):
        """Save the current tutor state as a session."""
        return self.save_session("tutor_session", {
            "conversation": conversation.messages[-20:] if conversation else [],
            "current_topic": conversation.current_topic if conversation else "",
            "last_captured_text": captured_text,
            "lesson_progress": lesson_progress,
            "saved_at": datetime.now().isoformat(),
        })

    def resume_session(self, session_id: str) -> Optional[dict]:
        """Load session data for resuming."""
        session = self.load_session(session_id)
        if session:
            return session.get("data", {})
        return None
