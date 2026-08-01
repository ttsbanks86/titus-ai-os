"""
Titus AI OS M5 Project Memory

On resume, restores the full autonomous execution context:

- current project, milestone, sprint
- execution queue
- checkpoints
- active agents
- knowledge context (vault records: CURRENT_MILESTONE, PROJECT_STATUS,
  ROADMAP, SOURCE_OF_TRUTH, daily notes)
- Source of Truth pointer

Memory is a thin facade over the existing vault records (M4 pattern) plus
the engine's own state files (queue, approvals, checkpoint dir, events).
Nothing is duplicated: the vault remains the source of truth for milestone
state; the engine state directory holds runtime execution state.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ProjectMemory:
    """
    Builds and restores execution context.

    engine_state_dir  -> runtime state (queue.json, approvals.json,
                         events.log, checkpoints/, heartbeat.json)
    vault_project_dir -> Titus-Vault project records (source of truth)
    """

    def __init__(
        self,
        engine_state_dir: str,
        vault_project_dir: str,
    ):
        self.state_dir = Path(engine_state_dir)
        self.vault_dir = Path(vault_project_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

    # ---- knowledge context from vault (source of truth) ----
    def knowledge_context(self) -> Dict:
        ctx: Dict = {}
        for name in (
            "CURRENT_MILESTONE.md",
            "PROJECT_STATUS.md",
            "ROADMAP.md",
            "SOURCE_OF_TRUTH.md",
        ):
            path = self.vault_dir / name
            if path.exists():
                ctx[name] = path.read_text(encoding="utf-8")
            else:
                ctx[name] = None
        # daily note (today, else most recent)
        daily = self.vault_dir.parent.parent / "02-Daily-Notes"
        if daily.exists():
            today = datetime.now().strftime("%Y-%m-%d")
            today_file = daily / f"{today}.md"
            if today_file.exists():
                ctx["DAILY_NOTE.md"] = today_file.read_text(encoding="utf-8")
            else:
                notes = sorted(daily.glob("[0-9][0-9][0-9][0-9]-*.md"))
                if notes:
                    ctx["DAILY_NOTE.md"] = notes[-1].read_text(encoding="utf-8")
        return ctx

    def source_of_truth(self) -> str:
        path = self.vault_dir / "SOURCE_OF_TRUTH.md"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return "SOURCE_OF_TRUTH.md not found"

    # ---- current milestone/sprint extraction ----
    def current_milestone(self) -> str:
        path = self.vault_dir / "CURRENT_MILESTONE.md"
        if not path.exists():
            return "unknown"
        content = path.read_text(encoding="utf-8")
        m = content.splitlines()
        for line in m:
            if "Milestone:" in line:
                value = line.split("Milestone:", 1)[1]
                return value.strip().strip("* ").strip()
        return "unknown"

    def snapshot_context(self) -> Dict:
        """Full resume bundle: knowledge + engine runtime state."""
        return {
            "captured_at": datetime.now().isoformat(),
            "current_milestone": self.current_milestone(),
            "knowledge": self.knowledge_context(),
            "queue": self._read_json("queue.json"),
            "approvals": self._read_json("approvals.json"),
            "checkpoints": self._list_checkpoints(),
            "heartbeat": self._read_json("heartbeat-latest.json")
            or self._read_last_heartbeat(),
            "source_of_truth": self.source_of_truth(),
        }

    def _read_json(self, name: str) -> Optional[list]:
        path = self.state_dir / name
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def _list_checkpoints(self) -> List[Dict]:
        cp_dir = self.state_dir / "checkpoints"
        if not cp_dir.exists():
            return []
        out = []
        for p in sorted(cp_dir.glob("checkpoint-*.json")):
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                out.append({
                    "checkpoint_id": data.get("checkpoint_id"),
                    "created_at": data.get("created_at"),
                    "label": data.get("label"),
                })
            except (json.JSONDecodeError, OSError):
                continue
        return out

    def _read_last_heartbeat(self) -> Optional[Dict]:
        path = self.state_dir / "heartbeat.json"
        if not path.exists():
            return None
        try:
            lines = path.read_text(encoding="utf-8").strip().splitlines()
            if not lines:
                return None
            return json.loads(lines[-1])
        except (json.JSONDecodeError, OSError):
            return None

    def save_context(self, context: Dict) -> None:
        """Persist a context bundle for future resume."""
        path = self.state_dir / "context.json"
        path.write_text(
            json.dumps(context, indent=2, default=str), encoding="utf-8"
        )

    def load_context(self) -> Optional[Dict]:
        path = self.state_dir / "context.json"
        if not path.exists():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
