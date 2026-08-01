"""
Titus AI OS M5 Execution Queue

Structured task queue supporting:

- states: queued, running, waiting, blocked, failed, completed, retry, cancelled
- priority (higher = first)
- dependencies (by item id)

The queue is the single source of truth for what the engine should do next.
Persisted to disk so it survives restarts.
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class QueueStatus(Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING = "waiting"
    BLOCKED = "blocked"
    FAILED = "failed"
    COMPLETED = "completed"
    RETRY = "retry"
    CANCELLED = "cancelled"


class QueueItem:
    """A unit of work in the execution queue."""

    def __init__(
        self,
        id: str,
        description: str,
        priority: int = 0,
        dependencies: Optional[List[str]] = None,
        max_retries: int = 3,
        owner_action: Optional[callable] = None,
        created_at: Optional[str] = None,
    ):
        self.id = id
        self.description = description
        self.priority = priority
        self.dependencies = dependencies or []
        self.status = QueueStatus.QUEUED
        self.retry_count = 0
        self.max_retries = max_retries
        self.owner_action = owner_action  # the actual work, injected by runner
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = self.created_at
        self.result: Optional[str] = None
        self.error: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "result": self.result,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "QueueItem":
        item = cls(
            id=data["id"],
            description=data.get("description", ""),
            priority=data.get("priority", 0),
            dependencies=data.get("dependencies", []),
            max_retries=data.get("max_retries", 3),
            created_at=data.get("created_at"),
        )
        item.status = QueueStatus(data.get("status", "queued"))
        item.retry_count = data.get("retry_count", 0)
        item.updated_at = data.get("updated_at", item.created_at)
        item.result = data.get("result")
        item.error = data.get("error")
        return item


class ExecutionQueue:
    """
    Thread-safe priority queue with dependency ordering.

    - enqueue(item) -> add or replace
    - next_ready() -> highest-priority item whose dependencies are completed
    - mark_running / mark_completed / mark_failed / retry / cancel / block
    - save_state / load_state -> persistent across restarts
    """

    def __init__(self, state_path: Optional[str] = None):
        self._items: Dict[str, QueueItem] = {}
        self._lock = threading.Lock()
        self.state_path = Path(state_path) if state_path else None

    def enqueue(self, item: QueueItem) -> QueueItem:
        with self._lock:
            item.status = QueueStatus.QUEUED
            item.updated_at = datetime.now().isoformat()
            self._items[item.id] = item
            return item

    def get(self, item_id: str) -> Optional[QueueItem]:
        with self._lock:
            return self._items.get(item_id)

    def next_ready(self) -> Optional[QueueItem]:
        """Return the next runnable item: queued/retry, deps completed."""
        with self._lock:
            candidates = []
            for item in self._items.values():
                if item.status not in (QueueStatus.QUEUED, QueueStatus.RETRY):
                    continue
                deps_ok = all(
                    dep in self._items
                    and self._items[dep].status == QueueStatus.COMPLETED
                    for dep in item.dependencies
                )
                if deps_ok:
                    candidates.append(item)
            if not candidates:
                return None
            return max(candidates, key=lambda i: i.priority)

    def mark_running(self, item_id: str) -> Optional[QueueItem]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            item.status = QueueStatus.RUNNING
            item.updated_at = datetime.now().isoformat()
            return item

    def mark_completed(self, item_id: str, result: str = "") -> Optional[QueueItem]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            item.status = QueueStatus.COMPLETED
            item.result = result
            item.updated_at = datetime.now().isoformat()
            return item

    def mark_failed(self, item_id: str, error: str = "") -> Optional[QueueItem]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            item.status = QueueStatus.FAILED
            item.error = error
            item.updated_at = datetime.now().isoformat()
            return item

    def retry(self, item_id: str) -> Optional[QueueItem]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            if item.retry_count >= item.max_retries:
                item.status = QueueStatus.FAILED
                return item
            item.retry_count += 1
            item.status = QueueStatus.RETRY
            item.updated_at = datetime.now().isoformat()
            return item

    def block(self, item_id: str, reason: str = "") -> Optional[QueueItem]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            item.status = QueueStatus.BLOCKED
            item.error = reason
            item.updated_at = datetime.now().isoformat()
            return item

    def cancel(self, item_id: str) -> Optional[QueueItem]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            item.status = QueueStatus.CANCELLED
            item.updated_at = datetime.now().isoformat()
            return item

    def wait(self, item_id: str) -> Optional[QueueItem]:
        with self._lock:
            item = self._items.get(item_id)
            if not item:
                return None
            item.status = QueueStatus.WAITING
            item.updated_at = datetime.now().isoformat()
            return item

    def all(self) -> List[QueueItem]:
        with self._lock:
            return list(self._items.values())

    def by_status(self) -> Dict[str, int]:
        counts = {s.value: 0 for s in QueueStatus}
        for item in self._items.values():
            counts[item.status.value] += 1
        return counts

    def save_state(self) -> None:
        if not self.state_path:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        data = [i.to_dict() for i in self.all()]
        self.state_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load_state(self) -> None:
        if not self.state_path or not self.state_path.exists():
            return
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            logger.warning("Could not load queue state from %s", self.state_path)
            return
        with self._lock:
            for item_data in data:
                item = QueueItem.from_dict(item_data)
                item.owner_action = None  # actions cannot be serialized; runner re-injects
                self._items[item.id] = item
