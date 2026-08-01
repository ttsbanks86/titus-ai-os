"""
Titus AI OS M5 Event Engine

Internal event system for the autonomous execution engine.
Events are emitted by the runner, queue, checkpoint system, and safety
monitor. Consumers (dashboard, connectors, logging) subscribe via handlers.

Provider-independent: pure stdlib, no external services.
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class EventType(Enum):
    """All internal event types (M5 Phase F)."""

    MILESTONE_STARTED = "milestone_started"
    SPRINT_STARTED = "sprint_started"
    SPRINT_COMPLETED = "sprint_completed"
    VERIFICATION_PASSED = "verification_passed"
    VERIFICATION_FAILED = "verification_failed"
    APPROVAL_REQUIRED = "approval_required"
    APPROVAL_GRANTED = "approval_granted"
    APPROVAL_DENIED = "approval_denied"
    RETRY_STARTED = "retry_started"
    RETRY_SUCCEEDED = "retry_succeeded"
    RETRY_EXHAUSTED = "retry_exhausted"
    MILESTONE_COMPLETED = "milestone_completed"
    CHECKPOINT_CREATED = "checkpoint_created"
    CHECKPOINT_RESTORED = "checkpoint_restored"
    QUEUE_ITEM_ADDED = "queue_item_added"
    QUEUE_ITEM_STARTED = "queue_item_started"
    QUEUE_ITEM_COMPLETED = "queue_item_completed"
    QUEUE_ITEM_FAILED = "queue_item_failed"
    QUEUE_ITEM_BLOCKED = "queue_item_blocked"
    QUEUE_ITEM_CANCELLED = "queue_item_cancelled"
    HEARTBEAT = "heartbeat"
    SAFETY_PAUSED = "safety_paused"
    SAFETY_RESUMED = "safety_resumed"
    SAFETY_SHUTDOWN = "safety_shutdown"
    DEADLOCK_DETECTED = "deadlock_detected"
    RESOURCE_WARNING = "resource_warning"
    RUNNER_STARTED = "runner_started"
    RUNNER_STOPPED = "runner_stopped"
    MEMORY_RESTORED = "memory_restored"
    MEMORY_SAVED = "memory_saved"
    UNKNOWN = "unknown"


class Event:
    """A single event with a type, payload, and timestamp."""

    def __init__(
        self,
        type: EventType,
        payload: Optional[Dict] = None,
        timestamp: Optional[str] = None,
    ):
        self.type = type if isinstance(type, EventType) else EventType.UNKNOWN
        self.payload = payload or {}
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "type": self.type.value,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Event":
        try:
            etype = EventType(data.get("type", "unknown"))
        except ValueError:
            etype = EventType.UNKNOWN
        return cls(
            type=etype,
            payload=data.get("payload", {}),
            timestamp=data.get("timestamp"),
        )


class EventEngine:
    """
    In-memory event bus with optional persistent log.

    - publish(event_type, payload) -> fans out to subscribers and appends to log
    - subscribe(handler) -> handler receives every event
    - subscribe_type(handler, *types) -> handler receives only listed types
    - recent(n) -> last n events (for dashboard / resume)
    """

    def __init__(self, log_path: Optional[str] = None, max_log_entries: int = 1000):
        self._handlers: List[Callable[[Event], None]] = []
        self._type_handlers: Dict[EventType, List[Callable[[Event], None]]] = {}
        self._recent: List[Event] = []
        self.max_log_entries = max_log_entries
        self._lock = threading.Lock()
        self.log_path = Path(log_path) if log_path else None
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def subscribe(self, handler: Callable[[Event], None]) -> None:
        with self._lock:
            self._handlers.append(handler)

    def subscribe_type(
        self, handler: Callable[[Event], None], *types: EventType
    ) -> None:
        with self._lock:
            for t in types:
                self._type_handlers.setdefault(t, []).append(handler)

    def publish(
        self, type: EventType, payload: Optional[Dict] = None
    ) -> Event:
        event = Event(type=type, payload=payload)
        with self._lock:
            self._recent.append(event)
            if len(self._recent) > self.max_log_entries:
                self._recent = self._recent[-self.max_log_entries:]
            handlers = list(self._handlers)
            type_handlers = list(self._type_handlers.get(type, []))
        for h in handlers:
            try:
                h(event)
            except Exception:
                logger.exception("Event handler %s failed", h)
        for h in type_handlers:
            try:
                h(event)
            except Exception:
                logger.exception("Type handler %s failed", h)
        self._append_log(event)
        return event

    def _append_log(self, event: Event) -> None:
        if not self.log_path:
            return
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event.to_dict()) + "\n")
        except OSError:
            logger.warning("Could not append to event log %s", self.log_path)

    def recent(self, n: int = 50) -> List[Event]:
        with self._lock:
            return list(self._recent[-n:])

    def to_dict_list(self, n: int = 50) -> List[Dict]:
        return [e.to_dict() for e in self.recent(n)]
