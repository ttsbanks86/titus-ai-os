"""
Titus AI OS M5 Checkpoint System

Persistent checkpoints capture the full engine state so the autonomous
runner can pause, resume, roll back, and recover after interruption.

A checkpoint snapshot stores:

- project, milestone, sprint
- completed tasks, pending tasks
- approvals, failures
- retry counts
- verification evidence

Supports pause / resume / rollback / recovery.
"""

from __future__ import annotations

import json
import logging
import re
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def _safe_filename(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", text)[:60]


class CheckpointSystem:
    """
    Checkpoint store on disk.

    Layout (checkpoint_dir):
        checkpoint-<timestamp>-<label>.json   immutable snapshots
        latest.json                           pointer to most recent snapshot

    create(snapshot, label) -> checkpoint id
    latest() / get(cp_id) / list()
    restore(cp_id) -> snapshot dict (rollback = restore older checkpoint)
    """

    def __init__(self, checkpoint_dir: Optional[str] = None, keep: int = 50):
        self.dir = Path(checkpoint_dir) if checkpoint_dir else None
        self.keep = keep
        self._lock = threading.Lock()
        if self.dir:
            self.dir.mkdir(parents=True, exist_ok=True)

    def create(self, snapshot: Dict, label: str = "auto") -> Optional[str]:
        """Write a checkpoint snapshot. Returns checkpoint id or None."""
        if not self.dir:
            return None
        with self._lock:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            safe_label = _safe_filename(label)
            cp_id = f"{ts}-{safe_label}"
            path = self.dir / f"checkpoint-{cp_id}.json"
            payload = {
                "checkpoint_id": cp_id,
                "created_at": datetime.now().isoformat(),
                "label": label,
                "snapshot": snapshot,
            }
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            self._write_latest(cp_id)
            self._prune()
            return cp_id

    def _write_latest(self, cp_id: str) -> None:
        if not self.dir:
            return
        (self.dir / "latest.json").write_text(
            json.dumps({"checkpoint_id": cp_id,
                        "updated_at": datetime.now().isoformat()}),
            encoding="utf-8",
        )

    def latest(self) -> Optional[Dict]:
        """Return the most recent snapshot dict, or None."""
        if not self.dir:
            return None
        latest_file = self.dir / "latest.json"
        if not latest_file.exists():
            files = sorted(self.dir.glob("checkpoint-*.json"))
            if not files:
                return None
            return json.loads(files[-1].read_text(encoding="utf-8")).get("snapshot")
        try:
            pointer = json.loads(latest_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
        return self.get(pointer.get("checkpoint_id", ""))

    def get(self, cp_id: str) -> Optional[Dict]:
        if not self.dir:
            return None
        path = self.dir / f"checkpoint-{cp_id}.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8")).get("snapshot")
        except (json.JSONDecodeError, OSError):
            return None

    def list_checkpoints(self) -> List[Dict]:
        if not self.dir:
            return []
        out = []
        for path in sorted(self.dir.glob("checkpoint-*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                out.append({
                    "checkpoint_id": data.get("checkpoint_id"),
                    "created_at": data.get("created_at"),
                    "label": data.get("label"),
                })
            except (json.JSONDecodeError, OSError):
                continue
        return out

    def restore(self, cp_id: str) -> Optional[Dict]:
        """Restore (recover) from a checkpoint. Also updates latest pointer."""
        snapshot = self.get(cp_id)
        if snapshot is not None:
            with self._lock:
                self._write_latest(cp_id)
        return snapshot

    def rollback(self, to: Optional[str] = None) -> Optional[Dict]:
        """
        Roll back to a previous checkpoint.
        Without `to`, rolls back to the checkpoint before the latest.
        """
        if not self.dir:
            return None
        checkpoints = sorted(self.dir.glob("checkpoint-*.json"))
        if len(checkpoints) < 2:
            return None
        if to:
            return self.restore(to)
        # previous = second-to-last
        prev = checkpoints[-2]
        data = json.loads(prev.read_text(encoding="utf-8"))
        cp_id = data.get("checkpoint_id")
        return self.restore(cp_id) if cp_id else None

    def _prune(self) -> None:
        if not self.dir or self.keep <= 0:
            return
        files = sorted(self.dir.glob("checkpoint-*.json"))
        while len(files) > self.keep:
            files[0].unlink(missing_ok=True)
            files = files[1:]
