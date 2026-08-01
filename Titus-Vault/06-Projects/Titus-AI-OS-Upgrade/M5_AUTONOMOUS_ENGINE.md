# M5 — Autonomous Execution Engine

**Milestone:** M5 — Autonomous Execution Engine
**Status:** IN PROGRESS (implementation complete; docs in progress)
**Date:** 2026-07-31

---

## Objective

Transform the Titus AI OS from a prompt-driven system into a long-running
autonomous executor. Given a single milestone prompt, the engine should:
plan -> execute sprints -> verify -> checkpoint -> commit -> continue ->
produce one final verified report. It stops ONLY at governance gates:

- destructive operations (guardrails, always CRITICAL)
- architecture decisions (HIGH approval)
- owner approval gates (HIGH / CRITICAL)
- failed verification after retries exhausted
- security concerns
- safety monitor limits (runtime, heartbeat, deadlock, shutdown)

## Design Principles (from M5_WORKFLOW_ANALYSIS.md)

1. **Extend, do not replace.** The existing `MilestoneRunner` /
   `Orchestrator` (M2/M3 era) is the base. M5 wraps it with runtime systems.
2. **Provider-independent.** Pure Python stdlib + vault markdown + the M4
   hybrid plugin pattern. No cloud API is required to run the engine.
3. **No complexity without payoff.** Every subsystem removes a manual step:
   approvals, checkpoints, queue, safety, events, connectors, memory.
4. **Every autonomous capability has:** rollback, logging, verification,
   checkpoint recovery, approval boundaries.

## Architecture

```
api/orchestration/
  __init__.py      Orchestrator, Task, TaskStatus, AgentRole (existing)
  runner.py        MilestoneRunner (existing, extended: _serialize_state)
  engine.py        AutonomousEngine  <- composition root (NEW, Phase B)
  events.py        EventEngine + EventType (NEW, Phase F)
  approval.py      ApprovalModel + ApprovalLevel (NEW, Phase E)
  queue.py         ExecutionQueue + QueueItem (NEW, Phase D)
  checkpoint.py    CheckpointSystem (NEW, Phase C)
  safety.py        SafetyMonitor (NEW, Phase H)
  connectors.py    EventOutbox + sinks (NEW, Phase G)
  memory.py        ProjectMemory (NEW, Phase J)
```

## Integration surfaces

| Surface | Mechanism |
|---------|-----------|
| Dashboard | `api/routes/engine.py` -> `/api/engine/*` (status, report, events, checkpoints, approvals, rollback, memory) |
| OpenCode | `~/.config/opencode/plugins/titus-m5-engine.ts` -> `titus_engine_status`, `titus_engine_resume`, `titus_engine_approve` |
| Shared state | `~/.config/opencode/engine-state/` (queue.json, approvals.json, events.log, checkpoints/, heartbeat.json, context.json) |

The dashboard and the plugin read/write the SAME state files, so they can
never disagree. Runtime state lives OUTSIDE the repo (M4 hybrid pattern).

## Engine workflow

1. `plan(project, milestone, sprints)` -> creates milestone, sprints, and
   enqueues each task with its approval level; LOW auto-granted, MEDIUM
   auto-granted after verification, HIGH/CRITICAL await owner.
2. `run()` -> executes sprints sequentially. Per task: approval gate ->
   execute with retries (max_retries) -> queue completion -> evidence.
   After each sprint: verify, checkpoint, (auto-commit hook), continue.
3. Stop conditions return a status dict; operator controls:
   `approve(task, granted)`, `pause()`, `resume()`, `rollback()`,
   `restore(checkpoint)`, `request_stop(reason)`.
4. `report()` -> one final verified report (milestone, queue status,
   pending approvals, checkpoints, events, memory context).

## Test coverage

`api/tests/test_m5_autonomous.py` — 35 tests covering every subsystem and
engine end-to-end (complete milestone, approval gate stop/resume, rollback,
state persistence). Full suite: 70/70 passing (35 M3 + 35 M5).

## Status

- [x] Phase A: workflow analysis (`M5_WORKFLOW_ANALYSIS.md`)
- [x] Phase B: engine composition (`engine.py`)
- [x] Phase C: checkpoints (`checkpoint.py`)
- [x] Phase D: queue (`queue.py`)
- [x] Phase E: approvals (`approval.py`)
- [x] Phase F: events (`events.py`)
- [x] Phase G: connectors (`connectors.py`)
- [x] Phase H: long-run safety (`safety.py`)
- [x] Phase I: OpenCode + dashboard integration
- [x] Phase J: project memory (`memory.py`)
- [x] Phase K: tests (35 new)
- [ ] Phase L: documentation + records + commit
