"""
Titus AI OS M5 Owner Approval Model

Approval levels gate every autonomous action:

- LOW      -> automatic (documentation, tests, formatting, safe refactoring)
- MEDIUM   -> new modules, safe configuration; automatic after verification
- HIGH     -> architecture, security, database, breaking changes; owner required
- CRITICAL -> repository rewrite, credential changes, production deployment;
              owner approval mandatory, always

CRITICAL operations also route through the existing guardrails module
(api/guardrails) for defense in depth.
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


class ApprovalLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def requires_owner(self) -> bool:
        """HIGH and CRITICAL always require owner approval."""
        return self in (ApprovalLevel.HIGH, ApprovalLevel.CRITICAL)

    @property
    def automatic_after_verification(self) -> bool:
        """MEDIUM proceeds automatically once verification passes."""
        return self == ApprovalLevel.MEDIUM

    @property
    def fully_automatic(self) -> bool:
        return self == ApprovalLevel.LOW

    @property
    def rank(self) -> int:
        return {ApprovalLevel.LOW: 0, ApprovalLevel.MEDIUM: 1,
                ApprovalLevel.HIGH: 2, ApprovalLevel.CRITICAL: 3}[self]


class ApprovalStatus(Enum):
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    AUTO_GRANTED = "auto_granted"  # LOW, or MEDIUM after verification


class ApprovalRequest:
    """A single approval gate."""

    def __init__(
        self,
        item_id: str,
        description: str,
        level: ApprovalLevel,
        reason: str = "",
        created_at: Optional[str] = None,
    ):
        self.item_id = item_id
        self.description = description
        self.level = level
        self.reason = reason
        self.status = ApprovalStatus.PENDING
        self.created_at = created_at or datetime.now().isoformat()
        self.decided_at: Optional[str] = None
        self.decided_by: str = ""

    def to_dict(self) -> Dict:
        return {
            "item_id": self.item_id,
            "description": self.description,
            "level": self.level.value,
            "reason": self.reason,
            "status": self.status.value,
            "created_at": self.created_at,
            "decided_at": self.decided_at,
            "decided_by": self.decided_by,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ApprovalRequest":
        req = cls(
            item_id=data["item_id"],
            description=data.get("description", ""),
            level=ApprovalLevel(data.get("level", "medium")),
            reason=data.get("reason", ""),
            created_at=data.get("created_at"),
        )
        req.status = ApprovalStatus(data.get("status", "pending"))
        req.decided_at = data.get("decided_at")
        req.decided_by = data.get("decided_by", "")
        return req


class ApprovalModel:
    """
    Central approval authority.

    - request(item_id, description, level, reason) -> ApprovalRequest
    - decide(item_id, granted, by) -> owner decision on pending HIGH/CRITICAL
    - auto_approve(item_id) -> LOW, or MEDIUM after verification
    - pending() -> list of requests awaiting owner
    - persisted via save_state/load_state so approvals survive restarts
    """

    def __init__(self, state_path: Optional[str] = None):
        self._requests: Dict[str, ApprovalRequest] = {}
        self._lock = threading.Lock()
        self.state_path = Path(state_path) if state_path else None

    def request(
        self,
        item_id: str,
        description: str,
        level: ApprovalLevel,
        reason: str = "",
    ) -> ApprovalRequest:
        with self._lock:
            if item_id in self._requests:
                return self._requests[item_id]
            req = ApprovalRequest(item_id, description, level, reason)
            # LOW is auto-granted immediately; MEDIUM waits for verification
            if level.fully_automatic:
                req.status = ApprovalStatus.AUTO_GRANTED
                req.decided_at = datetime.now().isoformat()
                req.decided_by = "system"
            self._requests[item_id] = req
            return req

    def requires_owner(self, item_id: str) -> bool:
        with self._lock:
            req = self._requests.get(item_id)
            if not req:
                return False
            return req.level.requires_owner and req.status == ApprovalStatus.PENDING

    def auto_approve(self, item_id: str) -> Optional[ApprovalRequest]:
        """Grant a LOW or MEDIUM (post-verification) request automatically."""
        with self._lock:
            req = self._requests.get(item_id)
            if not req:
                return None
            if req.level in (ApprovalLevel.LOW, ApprovalLevel.MEDIUM):
                req.status = ApprovalStatus.AUTO_GRANTED
                req.decided_at = datetime.now().isoformat()
                req.decided_by = "system"
            return req

    def decide(self, item_id: str, granted: bool, by: str) -> Optional[ApprovalRequest]:
        with self._lock:
            req = self._requests.get(item_id)
            if not req or req.status != ApprovalStatus.PENDING:
                return req
            req.status = ApprovalStatus.GRANTED if granted else ApprovalStatus.DENIED
            req.decided_at = datetime.now().isoformat()
            req.decided_by = by
            return req

    def is_approved(self, item_id: str) -> bool:
        with self._lock:
            req = self._requests.get(item_id)
            if not req:
                return False
            return req.status in (ApprovalStatus.GRANTED, ApprovalStatus.AUTO_GRANTED)

    def pending(self) -> List[ApprovalRequest]:
        with self._lock:
            return [r for r in self._requests.values()
                    if r.status == ApprovalStatus.PENDING]

    def all(self) -> List[ApprovalRequest]:
        with self._lock:
            return list(self._requests.values())

    def save_state(self) -> None:
        if not self.state_path:
            return
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps([r.to_dict() for r in self.all()], indent=2), encoding="utf-8"
        )

    def load_state(self) -> None:
        if not self.state_path or not self.state_path.exists():
            return
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            logger.warning("Could not load approval state from %s", self.state_path)
            return
        with self._lock:
            for item in data:
                req = ApprovalRequest.from_dict(item)
                self._requests[req.item_id] = req
