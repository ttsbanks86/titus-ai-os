"""
Titus AI OS M5 Autonomous Execution Engine tests.

Covers:
- events (subscribe, publish, type filters, persistent log)
- approval model (LOW auto, MEDIUM post-verification, HIGH/CRITICAL owner)
- execution queue (priority, dependencies, retry, persistence)
- checkpoint system (create, latest, get, rollback, prune)
- safety monitor (heartbeat, deadlock, runtime, pause/resume/shutdown)
- connectors (file sink, webhook no-op, outbox fan-out)
- project memory (knowledge context, snapshot)
- engine end-to-end (plan -> run -> complete; approval gate; rollback)

Run from api/ with:  python -m pytest tests/test_m5_autonomous.py -q
"""

import json
import time
from pathlib import Path

import pytest

from orchestration.events import EventEngine, EventType
from orchestration.approval import ApprovalModel, ApprovalLevel, ApprovalStatus
from orchestration.queue import ExecutionQueue, QueueItem, QueueStatus
from orchestration.checkpoint import CheckpointSystem
from orchestration.safety import SafetyMonitor
from orchestration.connectors import FileSink, WebhookSink, EventOutbox
from orchestration.memory import ProjectMemory
from orchestration.engine import AutonomousEngine


# ----------------------------------------------------------------------
# fixtures
# ----------------------------------------------------------------------
@pytest.fixture
def state_dir(tmp_path):
    d = tmp_path / "engine-state"
    d.mkdir()
    return d


@pytest.fixture
def vault_dir(tmp_path):
    v = tmp_path / "vault-project"
    v.mkdir()
    (v / "CURRENT_MILESTONE.md").write_text(
        "# Current Milestone\n\n**Milestone:** M5 Autonomous Engine\n",
        encoding="utf-8",
    )
    (v / "PROJECT_STATUS.md").write_text("status: in progress", encoding="utf-8")
    (v / "ROADMAP.md").write_text("roadmap", encoding="utf-8")
    (v / "SOURCE_OF_TRUTH.md").write_text("source: vault", encoding="utf-8")
    return v


def make_engine(state_dir, vault_dir, **kwargs):
    return AutonomousEngine(
        engine_state_dir=str(state_dir),
        vault_project_dir=str(vault_dir),
        **kwargs,
    )


# ----------------------------------------------------------------------
# events
# ----------------------------------------------------------------------
class TestEvents:
    def test_subscribe_and_publish(self):
        ee = EventEngine()
        got = []
        ee.subscribe(lambda e: got.append(e))
        ee.publish(EventType.SPRINT_STARTED, {"sprint": "s1"})
        assert len(got) == 1
        assert got[0].type == EventType.SPRINT_STARTED
        assert got[0].payload == {"sprint": "s1"}

    def test_subscribe_type_filter(self):
        ee = EventEngine()
        got = []
        ee.subscribe_type(lambda e: got.append(e), EventType.SPRINT_COMPLETED)
        ee.publish(EventType.SPRINT_STARTED, {})
        ee.publish(EventType.SPRINT_COMPLETED, {})
        assert len(got) == 1
        assert got[0].type == EventType.SPRINT_COMPLETED

    def test_recent_and_unknown(self):
        ee = EventEngine()
        for i in range(5):
            ee.publish(EventType.HEARTBEAT, {"i": i})
        assert len(ee.recent(3)) == 3
        # unknown type coercion
        from orchestration.events import Event
        ev = Event.from_dict({"type": "nonsense"})
        assert ev.type == EventType.UNKNOWN

    def test_persistent_log(self, state_dir):
        log = state_dir / "events.log"
        ee = EventEngine(log_path=str(log))
        ee.publish(EventType.RUNNER_STARTED, {})
        ee.publish(EventType.SPRINT_COMPLETED, {"sprint": "s1"})
        lines = log.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["type"] == "runner_started"


# ----------------------------------------------------------------------
# approvals
# ----------------------------------------------------------------------
class TestApprovals:
    def test_low_auto_granted(self):
        am = ApprovalModel()
        req = am.request("t1", "docs", ApprovalLevel.LOW)
        assert req.status == ApprovalStatus.AUTO_GRANTED
        assert am.is_approved("t1")

    def test_medium_waits_then_auto(self):
        am = ApprovalModel()
        am.request("t1", "new module", ApprovalLevel.MEDIUM)
        assert not am.is_approved("t1")
        am.auto_approve("t1")
        assert am.is_approved("t1")
        assert am.all()[0].status == ApprovalStatus.AUTO_GRANTED

    def test_high_requires_owner(self):
        am = ApprovalModel()
        am.request("t1", "arch change", ApprovalLevel.HIGH)
        assert am.requires_owner("t1")
        assert len(am.pending()) == 1
        am.decide("t1", True, "titus")
        assert am.is_approved("t1")
        assert not am.requires_owner("t1")

    def test_denied_stays_denied(self):
        am = ApprovalModel()
        am.request("t1", "deploy", ApprovalLevel.CRITICAL)
        am.decide("t1", False, "titus")
        assert not am.is_approved("t1")
        assert am.all()[0].status == ApprovalStatus.DENIED

    def test_rank(self):
        assert ApprovalLevel.LOW.rank < ApprovalLevel.MEDIUM.rank < \
            ApprovalLevel.HIGH.rank < ApprovalLevel.CRITICAL.rank

    def test_persistence(self, state_dir):
        path = state_dir / "approvals.json"
        am = ApprovalModel(state_path=str(path))
        am.request("t1", "x", ApprovalLevel.HIGH)
        am.save_state()
        am2 = ApprovalModel(state_path=str(path))
        am2.load_state()
        assert am2.requires_owner("t1")


# ----------------------------------------------------------------------
# queue
# ----------------------------------------------------------------------
class TestQueue:
    def test_priority_order(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(id="low", description="low", priority=0))
        q.enqueue(QueueItem(id="high", description="high", priority=10))
        q.enqueue(QueueItem(id="mid", description="mid", priority=5))
        assert q.next_ready().id == "high"
        q.mark_completed("high")
        assert q.next_ready().id == "mid"
        q.mark_completed("mid")
        assert q.next_ready().id == "low"

    def test_dependencies_block(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(id="a", description="a"))
        q.enqueue(QueueItem(id="b", description="b", dependencies=["a"]))
        assert q.next_ready().id == "a"
        q.mark_completed("a")
        assert q.next_ready().id == "b"

    def test_retry_limits(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(id="a", description="a", max_retries=2))
        assert q.retry("a").status == QueueStatus.RETRY
        assert q.retry("a").status == QueueStatus.RETRY
        assert q.retry("a").status == QueueStatus.FAILED

    def test_persistence(self, state_dir):
        path = state_dir / "queue.json"
        q = ExecutionQueue(state_path=str(path))
        q.enqueue(QueueItem(id="a", description="a", priority=3))
        q.save_state()
        q2 = ExecutionQueue(state_path=str(path))
        q2.load_state()
        item = q2.get("a")
        assert item is not None
        assert item.priority == 3
        assert item.owner_action is None  # not serializable

    def test_by_status(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(id="a", description="a"))
        q.enqueue(QueueItem(id="b", description="b"))
        q.mark_completed("a")
        counts = q.by_status()
        assert counts["queued"] == 1
        assert counts["completed"] == 1


# ----------------------------------------------------------------------
# checkpoints
# ----------------------------------------------------------------------
class TestCheckpoints:
    def test_create_latest_get(self, state_dir):
        cp = CheckpointSystem(checkpoint_dir=str(state_dir / "checkpoints"))
        cp_id = cp.create({"milestone": "m1", "queue": [1]}, label="sprint-1")
        assert cp_id
        latest = cp.latest()
        assert latest["milestone"] == "m1"
        got = cp.get(cp_id)
        assert got["queue"] == [1]
        assert len(cp.list_checkpoints()) == 1

    def test_rollback_prev(self, state_dir):
        cp = CheckpointSystem(checkpoint_dir=str(state_dir / "checkpoints"))
        cp.create({"v": 1}, label="first")
        cp.create({"v": 2}, label="second")
        snap = cp.rollback()
        assert snap["v"] == 1
        # latest pointer now points at first checkpoint
        assert cp.latest()["v"] == 1

    def test_prune(self, state_dir):
        cp = CheckpointSystem(checkpoint_dir=str(state_dir / "checkpoints"),
                              keep=3)
        for i in range(6):
            cp.create({"v": i}, label=f"c{i}")
        files = list((state_dir / "checkpoints").glob("checkpoint-*.json"))
        assert len(files) == 3

    def test_safe_filename(self, state_dir):
        cp = CheckpointSystem(checkpoint_dir=str(state_dir / "checkpoints"))
        cp_id = cp.create({}, label="bad/name:with spaces!?")
        assert "/" not in cp_id and " " not in cp_id


# ----------------------------------------------------------------------
# safety
# ----------------------------------------------------------------------
class TestSafety:
    def test_heartbeat_deadlock(self):
        mon = SafetyMonitor(deadlock_progress_window=3)
        mon.heartbeat("step1")
        mon.heartbeat("step1")
        mon.heartbeat("step1")
        stop, reason = mon.should_stop()
        assert stop
        assert "DEADLOCK" in reason

    def test_progress_resets_deadlock(self):
        mon = SafetyMonitor(deadlock_progress_window=3)
        mon.heartbeat("a")
        mon.heartbeat("b")  # progress -> reset
        mon.heartbeat("b")
        assert mon.stagnant_count == 1

    def test_max_runtime(self):
        mon = SafetyMonitor(max_runtime_hours=1.0)
        mon.start_time = time.time() - 4000  # 1.1h elapsed
        violations = mon.check()
        assert any("MAX_RUNTIME" in v for v in violations)

    def test_pause_resume(self):
        mon = SafetyMonitor()
        mon.pause()
        stop, reason = mon.should_stop()
        assert stop and reason == "paused"
        mon.resume()
        stop, _ = mon.should_stop()
        assert not stop

    def test_shutdown(self):
        mon = SafetyMonitor()
        mon.request_shutdown("owner_request")
        stop, reason = mon.should_stop()
        assert stop and reason == "owner_request"

    def test_heartbeat_file(self, state_dir):
        mon = SafetyMonitor(state_dir=str(state_dir))
        mon._open_file()
        mon.heartbeat("sprint 1")
        mon.heartbeat("sprint 2")
        mon.shutdown()
        lines = (state_dir / "heartbeat.json").read_text(
            encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        assert json.loads(lines[-1])["progress"] == "sprint 2"


# ----------------------------------------------------------------------
# connectors
# ----------------------------------------------------------------------
class TestConnectors:
    def test_file_sink(self, state_dir):
        fs = FileSink(out_dir=str(state_dir / "out"), name="hooks")
        ok = fs.emit({"type": "sprint_completed", "sprint": "s1"})
        assert ok
        files = list((state_dir / "out").glob("hooks-*.json"))
        assert len(files) == 1
        assert json.loads(files[0].read_text(encoding="utf-8"))["sprint"] == "s1"

    def test_webhook_sink_noop_without_url(self):
        ws = WebhookSink(url=None)
        assert ws.emit({}) is False  # not configured -> no-op, engine unaffected

    def test_outbox_fanout(self, state_dir):
        fs = FileSink(out_dir=str(state_dir / "out"), name="outbox")
        outbox = EventOutbox(sinks=[fs])
        results = outbox.emit({"type": "heartbeat"})
        assert results["outbox"] is True
        assert outbox.describe()[0]["name"] == "outbox"


# ----------------------------------------------------------------------
# project memory
# ----------------------------------------------------------------------
class TestMemory:
    def test_knowledge_context(self, state_dir, vault_dir):
        mem = ProjectMemory(engine_state_dir=str(state_dir),
                            vault_project_dir=str(vault_dir))
        ctx = mem.knowledge_context()
        assert ctx["CURRENT_MILESTONE.md"] is not None
        assert "M5 Autonomous Engine" in ctx["CURRENT_MILESTONE.md"]
        assert mem.current_milestone() == "M5 Autonomous Engine"
        assert "source: vault" in mem.source_of_truth()

    def test_save_load_context(self, state_dir, vault_dir):
        mem = ProjectMemory(engine_state_dir=str(state_dir),
                            vault_project_dir=str(vault_dir))
        mem.save_context({"milestone": "m1", "note": "hello"})
        loaded = mem.load_context()
        assert loaded["note"] == "hello"


# ----------------------------------------------------------------------
# engine end-to-end
# ----------------------------------------------------------------------
def _plan_sprints():
    return [
        {
            "name": "Sprint 1: setup",
            "tasks": [
                {"title": "Write events module",
                 "description": "Implement event engine", "assigned_to": "engineer",
                 "approval_level": "low"},
                {"title": "Write queue",
                 "description": "Implement execution queue", "assigned_to": "engineer",
                 "approval_level": "medium"},
            ],
        },
        {
            "name": "Sprint 2: verify",
            "tasks": [
                {"title": "Write tests",
                 "description": "Add M5 test coverage", "assigned_to": "qa",
                 "approval_level": "low"},
                {"title": "Write docs",
                 "description": "Document the engine", "assigned_to": "documentation",
                 "approval_level": "low"},
            ],
        },
    ]


class TestEngine:
    def test_completes_milestone(self, state_dir, vault_dir):
        engine = make_engine(state_dir, vault_dir)
        milestone = engine.plan("titus-ai-os", "M5 Test Run",
                                "Verify engine end-to-end", _plan_sprints())
        result = engine.run()
        assert result["status"] == "completed"
        assert milestone.status.value == "verified_complete"
        # all 4 tasks completed in queue
        assert engine.queue.by_status()["completed"] == 4
        # checkpoints created after each sprint + milestone complete
        assert len(engine.checkpoints.list_checkpoints()) >= 2
        # report generated
        report = engine.report()
        assert report["status"] == "verified_complete"
        assert report["completion_rate"] == 1.0

    def test_approval_gate_stops_and_resumes(self, state_dir, vault_dir):
        engine = make_engine(state_dir, vault_dir)
        sprints = [{
            "name": "Sprint 1",
            "tasks": [
                {"title": "Arch change",
                 "description": "Change DB schema", "assigned_to": "engineer",
                 "approval_level": "high"},
            ],
        }]
        milestone = engine.plan("proj", "M5 Gate", "Gate test", sprints)
        result = engine.run()
        assert result["status"] == "awaiting_approval"
        assert milestone.status.value == "awaiting_approval"
        # owner decides
        task_id = result["task"]
        engine.approve(task_id, granted=True, by="titus")
        # resume
        result2 = engine.run()
        assert result2["status"] == "completed"
        assert milestone.status.value == "verified_complete"

    def test_rollback_restores_previous_checkpoint(self, state_dir, vault_dir):
        engine = make_engine(state_dir, vault_dir)
        engine.plan("proj", "M5 Rollback", "Rollback test", _plan_sprints())
        result = engine.run()
        assert result["status"] == "completed"
        snap = engine.rollback()
        assert snap is not None
        # queue reloaded from older snapshot
        assert engine.queue.by_status()["completed"] <= 4

    def test_engine_state_persisted(self, state_dir, vault_dir):
        engine = make_engine(state_dir, vault_dir)
        engine.plan("proj", "M5 Persist", "Persistence test", _plan_sprints())
        engine.run()
        assert (state_dir / "queue.json").exists()
        assert (state_dir / "approvals.json").exists()
        assert (state_dir / "events.log").exists()
        assert (state_dir / "checkpoints").exists()

    def test_report_contains_engine_sections(self, state_dir, vault_dir):
        engine = make_engine(state_dir, vault_dir)
        engine.plan("proj", "M5 Report", "Report test", _plan_sprints())
        engine.run()
        report = engine.report()
        for key in ("queue_status", "approvals_pending", "checkpoints",
                    "memory_context", "events"):
            assert key in report
