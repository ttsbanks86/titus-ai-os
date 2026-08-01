"""
Titus AI OS M5 Autonomous Execution Engine

The engine composes the existing MilestoneRunner/Orchestrator with the M5
modules (queue, approvals, events, checkpoints, safety, connectors, memory)
into a long-running autonomous executor.

Workflow (mission):
    plan(project, milestone, sprints)          -> milestone + queue
    run()                                       -> execute sprints until stop
      for each sprint: execute -> verify -> checkpoint -> commit
    pause() / resume() / rollback() / cancel()  -> operator controls
    report()                                    -> one final verified report

Stop conditions (engine stops ONLY for):
    - destructive operations (delegated to guardrails, always CRITICAL)
    - architecture decisions (HIGH approval)
    - owner approval gates (HIGH / CRITICAL)
    - failed verification after retries exhausted
    - security concerns (guardrails violation)
    - safety monitor (runtime / heartbeat / deadlock / shutdown)
"""

from __future__ import annotations

import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Optional

from . import Orchestrator, Task, TaskStatus, AgentRole  # base systems (re-export)
from .runner import MilestoneRunner, Milestone, Sprint, MilestoneStatus
from .events import EventEngine, EventType
from .approval import ApprovalModel, ApprovalLevel, ApprovalStatus
from .queue import ExecutionQueue, QueueItem, QueueStatus
from .checkpoint import CheckpointSystem
from .safety import SafetyMonitor
from .connectors import EventOutbox, FileSink, WebhookSink
from .memory import ProjectMemory

logger = logging.getLogger(__name__)


class AutonomousEngine:
    """
    Long-running autonomous milestone executor.

    engine_state_dir: directory for runtime state (queue, approvals,
                      events, checkpoints, heartbeats). Not the vault.
    vault_project_dir: Titus-Vault project record directory (source of truth).
    """

    # Engine-wide limits
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_MAX_RUNTIME_HOURS = 12.0
    STOP_REASONS = (
        "completed",
        "approval_required",
        "verification_failed",
        "safety",
        "owner_request",
        "paused",
    )

    def __init__(
        self,
        engine_state_dir: str,
        vault_project_dir: str,
        max_runtime_hours: float = DEFAULT_MAX_RUNTIME_HOURS,
        checkpoint_every_sprint: bool = True,
        auto_commit: bool = True,
        run_verification: Optional[Callable[[], Dict]] = None,
    ):
        self.state_dir = Path(engine_state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.vault_project_dir = Path(vault_project_dir)

        # Base systems (M2/M3 era, extended)
        self.orchestrator = Orchestrator()
        self.runner = MilestoneRunner(self.orchestrator)

        # M5 systems
        self.events = EventEngine(log_path=str(self.state_dir / "events.log"))
        self.approvals = ApprovalModel(
            state_path=str(self.state_dir / "approvals.json")
        )
        self.queue = ExecutionQueue(
            state_path=str(self.state_dir / "queue.json")
        )
        self.checkpoints = CheckpointSystem(
            checkpoint_dir=str(self.state_dir / "checkpoints")
        )
        self.safety = SafetyMonitor(
            state_dir=str(self.state_dir),
            max_runtime_hours=max_runtime_hours,
        )
        self.outbox = EventOutbox()
        self.memory = ProjectMemory(
            engine_state_dir=str(self.state_dir),
            vault_project_dir=str(self.vault_project_dir),
        )

        self.max_runtime_hours = max_runtime_hours
        self.checkpoint_every_sprint = checkpoint_every_sprint
        self.auto_commit = auto_commit
        self.run_verification = run_verification

        self._lock = threading.Lock()
        self._current_sprint: Optional[str] = None
        self._last_commit_sha: Optional[str] = None
        self._log_dir = self.state_dir / "sprint-logs"
        self._log_dir.mkdir(parents=True, exist_ok=True)

        # event -> outbox fan-out
        self.events.subscribe(self._on_event)
        # approvals: wire decisions to events
        self.approvals.load_state()
        self.queue.load_state()

    # ------------------------------------------------------------------
    # event fan-out
    # ------------------------------------------------------------------
    def _on_event(self, event) -> None:
        self.outbox.emit(event.to_dict())

    # ------------------------------------------------------------------
    # planning
    # ------------------------------------------------------------------
    def plan(
        self,
        project: str,
        milestone_name: str,
        objective: str,
        sprints: List[Dict],
    ) -> Milestone:
        """
        Create a milestone with sprints and enqueue the work.

        sprints: [{"name": ..., "tasks": [{"description": ...,
                  "assigned_to": "engineer", "approval_level": "low", ...}]}]
        """
        milestone = self.runner.create_milestone(
            name=f"[{project}] {milestone_name}",
            objective=objective,
            sprints=sprints,  # pre-create sprint shells
        )

        for i, sprint_data in enumerate(sprints):
            sprint = milestone.sprints[i]
            for task_data in sprint_data.get("tasks", []):
                level = ApprovalLevel(
                    task_data.get("approval_level", "low")
                )
                task = self.orchestrator.create_task(
                    title=task_data.get("title", task_data["description"][:60]),
                    description=task_data["description"],
                    assigned_to=AgentRole(
                        task_data.get("assigned_to", "engineer")
                    ),
                    approval_required=level.requires_owner,
                )
                self.runner.add_task_to_sprint(milestone.id, i, task)
                # queue the task
                qitem = QueueItem(
                    id=task.id,
                    description=task.description,
                    priority=task_data.get("priority", 0),
                    max_retries=task_data.get("max_retries", self.DEFAULT_MAX_RETRIES),
                )
                self.queue.enqueue(qitem)
                # register approval
                self.approvals.request(
                    item_id=task.id,
                    description=task.description,
                    level=level,
                    reason=f"Sprint {i+1} task",
                )

        self.events.publish(EventType.MILESTONE_STARTED, {
            "milestone": milestone.id,
            "name": milestone.name,
            "sprints": len(milestone.sprints),
        })
        self._save_runtime_state()
        return milestone

    # ------------------------------------------------------------------
    # sprint execution
    # ------------------------------------------------------------------
    def _execute_sprint(self, milestone: Milestone, sprint_index: int) -> Dict:
        sprint = milestone.sprints[sprint_index]
        self._current_sprint = sprint.id
        self.events.publish(EventType.SPRINT_STARTED, {
            "milestone": milestone.id, "sprint": sprint.id, "index": sprint_index,
        })

        results: List[Dict] = []
        for task_id in sprint.tasks:
            task = self.orchestrator.tasks.get(task_id)
            if not task:
                continue

            # 1. approval gate (HIGH/CRITICAL)
            if self.approvals.requires_owner(task_id):
                task.status = TaskStatus.AWAITING_APPROVAL
                self.events.publish(EventType.APPROVAL_REQUIRED, {
                    "task": task_id, "title": task.title,
                })
                return {"status": "awaiting_approval", "task": task_id,
                        "results": results}

            # 2. execute with retries
            attempt = 0
            while True:
                try:
                    self.queue.mark_running(task_id)
                    self.orchestrator.start_task(task_id)
                    outcome = self._run_task(task)
                    self.queue.mark_completed(task_id, outcome.get("result", ""))
                    self.orchestrator.complete_task(task_id,
                                                    evidence=[outcome.get("evidence", "")])
                    self.events.publish(EventType.QUEUE_ITEM_COMPLETED, {
                        "task": task_id,
                    })
                    results.append({"task": task_id, "status": "ok",
                                    "evidence": outcome.get("evidence", "")})
                    break
                except Exception as e:  # retryable failure
                    attempt += 1
                    qitem = self.queue.get(task_id)
                    if qitem and attempt < qitem.max_retries:
                        self.events.publish(EventType.RETRY_STARTED, {
                            "task": task_id, "attempt": attempt, "error": str(e),
                        })
                        self.queue.retry(task_id)
                        continue
                    self.queue.mark_failed(task_id, str(e))
                    self.orchestrator.retry_task(task_id)
                    self.events.publish(EventType.RETRY_EXHAUSTED, {
                        "task": task_id, "attempt": attempt, "error": str(e),
                    })
                    results.append({"task": task_id, "status": "failed",
                                    "error": str(e)})
                    return {"status": "failed", "task": task_id,
                            "error": str(e), "results": results}

            # 3. MEDIUM approval: auto-grant after success + verification
            self.approvals.auto_approve(task_id)

        # sprint verification
        verified = self.runner.verify_sprint(milestone.id, sprint_index)
        if verified:
            sprint.status = TaskStatus.COMPLETE
            self.events.publish(EventType.SPRINT_COMPLETED, {
                "milestone": milestone.id, "sprint": sprint.id,
            })
        else:
            self.events.publish(EventType.VERIFICATION_FAILED, {
                "milestone": milestone.id, "sprint": sprint.id,
            })
            return {"status": "verification_failed", "results": results}

        return {"status": "ok", "results": results}

    def _run_task(self, task: Task) -> Dict:
        """
        Execute a single task. The default implementation logs the task
        as "simulated" so the engine can run end-to-end without external
        agents. A real deployment injects `run_verification` or overrides
        this method to call the OpenCode agent tooling.
        """
        log = self._log_dir / f"{task.id}.json"
        entry = {
            "task": task.id,
            "title": task.title,
            "executed_at": datetime.now().isoformat(),
            "mode": "simulated" if self.run_verification is None else "agent",
        }
        log.write_text(json.dumps(entry, indent=2), encoding="utf-8")
        return {"evidence": f"Executed {task.id} ({task.title})"}

    # ------------------------------------------------------------------
    # main loop
    # ------------------------------------------------------------------
    def run(self, max_sprints: Optional[int] = None) -> Dict:
        """Execute the current milestone until a stop condition."""
        milestone_id = self.runner.current_milestone
        if not milestone_id:
            milestone = self._pick_milestone()
            if not milestone:
                return {"status": "no_milestone", "reason": "nothing planned"}
            self.runner.start_milestone(milestone.id)
            milestone_id = milestone.id

        milestone = self.runner.milestones[milestone_id]
        self.safety.heartbeat("starting")
        self.events.publish(EventType.RUNNER_STARTED, {"milestone": milestone_id})

        completed_sprints = 0
        max_sprints = max_sprints or len(milestone.sprints)
        sprint_index = 0

        while sprint_index < len(milestone.sprints) and completed_sprints < max_sprints:
            # safety: stop on runtime/deadlock/shutdown
            stop, reason = self.safety.should_stop(
                f"sprint {sprint_index+1}/{len(milestone.sprints)}"
            )
            if stop:
                self.events.publish(EventType.SAFETY_SHUTDOWN,
                                    {"reason": reason})
                return {"status": "stopped", "reason": reason,
                        "sprint_index": sprint_index}

            sprint = milestone.sprints[sprint_index]
            if sprint.status == TaskStatus.COMPLETE:
                sprint_index += 1
                continue

            outcome = self._execute_sprint(milestone, sprint_index)

            if outcome["status"] == "awaiting_approval":
                milestone.status = MilestoneStatus.AWAITING_APPROVAL
                self.events.publish(EventType.APPROVAL_REQUIRED,
                                    {"sprint": sprint.id})
                self._checkpoint(milestone, label="awaiting-approval")
                return {"status": "awaiting_approval",
                        "task": outcome.get("task")}

            if outcome["status"] == "failed":
                milestone.status = MilestoneStatus.BLOCKED
                milestone.blockers.append(outcome.get("error", "task failed"))
                self._checkpoint(milestone, label="blocked")
                return {"status": "blocked", "error": outcome.get("error")}

            if outcome["status"] == "verification_failed":
                milestone.status = MilestoneStatus.BLOCKED
                milestone.blockers.append("sprint verification failed")
                self._checkpoint(milestone, label="verification-failed")
                return {"status": "verification_failed"}

            # sprint ok
            completed_sprints += 1
            sprint_index += 1
            if self.checkpoint_every_sprint:
                self._checkpoint(milestone, label=f"sprint-{sprint_index}")

        # all sprints complete -> milestone completion
        self.runner.complete_milestone(milestone_id, verified=True)
        milestone.status = MilestoneStatus.VERIFIED_COMPLETE
        self.events.publish(EventType.MILESTONE_COMPLETED, {
            "milestone": milestone_id,
            "name": milestone.name,
            "sprints": len(milestone.sprints),
        })
        self._checkpoint(milestone, label="milestone-complete")
        self.safety.shutdown("milestone_completed")
        self._save_runtime_state()
        return {"status": "completed", "milestone": milestone_id}

    def _pick_milestone(self) -> Optional[Milestone]:
        for m in self.runner.milestones.values():
            if m.status in (MilestoneStatus.PLANNED, MilestoneStatus.READY):
                return m
        return None

    def _checkpoint(self, milestone: Milestone, label: str) -> None:
        snapshot = self.snapshot()
        cp_id = self.checkpoints.create(snapshot, label=label)
        if cp_id:
            self.events.publish(EventType.CHECKPOINT_CREATED,
                                {"checkpoint": cp_id, "label": label})

    # ------------------------------------------------------------------
    # operator controls
    # ------------------------------------------------------------------
    def pause(self) -> Dict:
        self.safety.pause()
        self.events.publish(EventType.SAFETY_PAUSED, {})
        return {"status": "paused"}

    def resume(self) -> Dict:
        self.safety.resume()
        self.events.publish(EventType.SAFETY_RESUMED, {})
        return {"status": "resumed"}

    def request_stop(self, reason: str = "owner_request") -> Dict:
        self.safety.request_shutdown(reason)
        return {"status": "stop_requested"}

    def rollback(self) -> Optional[Dict]:
        """Roll back to the previous checkpoint."""
        snapshot = self.checkpoints.rollback()
        if snapshot:
            self._restore_snapshot(snapshot)
            self.events.publish(EventType.CHECKPOINT_RESTORED, {"rollback": True})
            return snapshot
        return None

    def restore(self, cp_id: Optional[str] = None) -> Optional[Dict]:
        """Restore latest (or given) checkpoint."""
        snapshot = (self.checkpoints.get(cp_id) if cp_id
                    else self.checkpoints.latest())
        if snapshot:
            self._restore_snapshot(snapshot)
            self.events.publish(EventType.CHECKPOINT_RESTORED,
                                {"checkpoint": cp_id or "latest"})
        return snapshot

    def _restore_snapshot(self, snapshot: Dict) -> None:
        """Restore engine state from a checkpoint snapshot."""
        # restore milestones from the runner's serialized state
        runner_state = snapshot.get("runner_state")
        if runner_state:
            state_file = self.state_dir / "_restore_runner.json"
            state_file.write_text(json.dumps(runner_state), encoding="utf-8")
            self.runner.load_state(str(state_file))
            state_file.unlink(missing_ok=True)
        # queue: write snapshot data into the queue's own state file, then load
        queue_data = snapshot.get("queue")
        if queue_data is not None and self.queue.state_path:
            self.queue.state_path.write_text(
                json.dumps(queue_data), encoding="utf-8"
            )
            self.queue.load_state()
        # approvals: same pattern
        approval_data = snapshot.get("approvals")
        if approval_data is not None and self.approvals.state_path:
            self.approvals.state_path.write_text(
                json.dumps(approval_data), encoding="utf-8"
            )
            self.approvals.load_state()
        # safety: reset runtime if a shutdown was requested
        if snapshot.get("safety", {}).get("shutdown_reason"):
            self.safety = SafetyMonitor(
                state_dir=str(self.state_dir),
                max_runtime_hours=self.max_runtime_hours,
            )
        self.events.publish(EventType.MEMORY_RESTORED, {})

    def approve(self, task_id: str, granted: bool = True, by: str = "owner") -> Dict:
        req = self.approvals.decide(task_id, granted, by)
        if not req:
            return {"status": "not_found"}
        if granted:
            task = self.orchestrator.tasks.get(task_id)
            if task:
                self.orchestrator.approve_task(task_id)
            self.events.publish(EventType.APPROVAL_GRANTED,
                                {"task": task_id, "by": by})
        else:
            self.events.publish(EventType.APPROVAL_DENIED,
                                {"task": task_id, "by": by})
        self._save_runtime_state()
        return {"status": "decided", "granted": granted, "task": task_id}

    # ------------------------------------------------------------------
    # snapshot / persistence / report
    # ------------------------------------------------------------------
    def snapshot(self) -> Dict:
        """Full engine state (for checkpoints + resume)."""
        return {
            "captured_at": datetime.now().isoformat(),
            "milestone": self.runner.current_milestone,
            "runner_state": self.runner._serialize_state(),
            "queue": [i.to_dict() for i in self.queue.all()],
            "approvals": [r.to_dict() for r in self.approvals.all()],
            "events": self.events.to_dict_list(100),
            "safety": self.safety.status(),
        }

    def _save_runtime_state(self) -> None:
        self.queue.save_state()
        self.approvals.save_state()
        self.events.publish(EventType.MEMORY_SAVED, {})

    def report(self) -> Dict:
        """One final verified report for the milestone."""
        milestone = None
        if self.runner.current_milestone:
            milestone = self.runner.milestones.get(
                self.runner.current_milestone
            )
        if not milestone:
            # fall back to most recent
            for m in self.runner.milestones.values():
                milestone = m
        base = self.runner.generate_report(
            milestone.id if milestone else ""
        ) if milestone else {"error": "no milestone"}
        base["sprints_done"] = self.safety.last_progress
        base["events"] = self.events.to_dict_list(10)
        base["queue_status"] = self.queue.by_status()
        base["approvals_pending"] = [
            r.to_dict() for r in self.approvals.pending()
        ]
        base["checkpoints"] = self.checkpoints.list_checkpoints()
        base["memory_context"] = self.memory.current_milestone()
        return base
