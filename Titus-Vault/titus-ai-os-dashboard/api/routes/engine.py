"""Titus AI OS M5 Autonomous Engine API routes.

Reads engine runtime state (queue, approvals, checkpoints, safety, events,
memory context) from the engine state directory and exposes owner controls
(approve/deny, pause/resume/stop, rollback).

The engine itself runs inside OpenCode (via the M5 plugin). The dashboard
route is a stateless viewer + decision channel over the same state files,
so the plugin and the dashboard never disagree.
"""

from __future__ import annotations

from pathlib import Path
import json
import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..orchestration.engine import AutonomousEngine

router = APIRouter()

VAULT_ROOT = Path(__file__).parent.parent.parent.parent
PROJECT_DIR = VAULT_ROOT / "06-Projects" / "Titus-AI-OS-Upgrade"

# Runtime state lives OUTSIDE the repo (M4 hybrid pattern): user config dir.
ENGINE_STATE_DIR = Path(
    os.environ.get(
        "TITUS_ENGINE_STATE_DIR",
        str(Path.home() / ".config" / "opencode" / "engine-state"),
    )
)


def _engine() -> AutonomousEngine:
    """Fresh engine instance bound to the shared state dir. Stateless read
    of persistent files unless a mutating endpoint writes to them."""
    return AutonomousEngine(
        engine_state_dir=str(ENGINE_STATE_DIR),
        vault_project_dir=str(PROJECT_DIR),
    )


class DecideRequest(BaseModel):
    granted: bool = True
    by: str = "owner"


@router.get("/status")
async def engine_status():
    """Engine + milestone + queue + approvals + safety snapshot."""
    try:
        engine = _engine()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"engine init failed: {e}")
    return {
        "engine_state_dir": str(ENGINE_STATE_DIR),
        "engine_state_dir_exists": ENGINE_STATE_DIR.exists(),
        "current_milestone": engine.memory.current_milestone(),
        "queue_status": engine.queue.by_status(),
        "approvals_pending": [
            r.to_dict() for r in engine.approvals.pending()
        ],
        "approvals_total": len(engine.approvals.all()),
        "checkpoints": engine.checkpoints.list_checkpoints(),
        "safety": engine.safety.status(),
        "events": engine.events.to_dict_list(10),
        "source_of_truth": engine.memory.source_of_truth()[:400],
    }


@router.get("/report")
async def engine_report():
    """Full engine completion report (milestone, queue, approvals)."""
    try:
        engine = _engine()
        return engine.report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"report failed: {e}")


@router.get("/events")
async def engine_events(limit: int = 25):
    """Recent engine events."""
    try:
        engine = _engine()
        return {"events": engine.events.to_dict_list(limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"events failed: {e}")


@router.get("/checkpoints")
async def engine_checkpoints():
    """List all checkpoints (id, created_at, label)."""
    try:
        engine = _engine()
        return {"checkpoints": engine.checkpoints.list_checkpoints()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"checkpoints failed: {e}")


@router.post("/approvals/{item_id}/decide")
async def decide_approval(item_id: str, req: DecideRequest):
    """Owner decision on a pending HIGH/CRITICAL approval gate."""
    try:
        engine = _engine()
        engine.approvals.load_state()
        engine.approvals.decide(item_id, req.granted, req.by)
        engine.approvals.save_state()
        return {"status": "decided", "item_id": item_id,
                "granted": req.granted, "by": req.by}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"decide failed: {e}")


@router.post("/checkpoint/rollback")
async def rollback_checkpoint():
    """Roll engine back to the previous checkpoint."""
    try:
        engine = _engine()
        engine.approvals.load_state()
        engine.queue.load_state()
        snap = engine.rollback()
        if snap is None:
            return {"status": "no_rollback", "reason": "fewer than 2 checkpoints"}
        return {"status": "rolled_back", "checkpoint": snap.get("captured_at")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"rollback failed: {e}")


@router.post("/memory/snapshot")
async def memory_snapshot():
    """Capture a full context snapshot (knowledge + runtime state)."""
    try:
        engine = _engine()
        engine.memory.save_context(engine.memory.snapshot_context())
        return {"status": "snapshot_saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"snapshot failed: {e}")


@router.get("/memory/context")
async def memory_context():
    """Current memory context bundle (knowledge from vault)."""
    try:
        engine = _engine()
        return engine.memory.snapshot_context()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"memory failed: {e}")
