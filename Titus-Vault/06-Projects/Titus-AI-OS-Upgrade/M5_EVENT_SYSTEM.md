# M5 — Event System

**File:** `api/orchestration/events.py`
**Status:** COMPLETE

---

## Purpose

Internal event bus for the autonomous engine. Every meaningful transition
(milestone started, sprint completed, verification passed/failed, approval
required/granted/denied, retries, checkpoints, queue items, heartbeats,
safety events, memory save/restore) is published as an event. Consumers
subscribe in-process; a persistent JSONL log keeps a durable trail for the
dashboard and for resume.

## Event types

`EventType` enum (36 types), including:
- Milestone: `MILESTONE_STARTED`, `MILESTONE_COMPLETED`
- Sprint: `SPRINT_STARTED`, `SPRINT_COMPLETED`
- Verification: `VERIFICATION_PASSED`, `VERIFICATION_FAILED`
- Approval: `APPROVAL_REQUIRED`, `APPROVAL_GRANTED`, `APPROVAL_DENIED`
- Retry: `RETRY_STARTED`, `RETRY_SUCCEEDED`, `RETRY_EXHAUSTED`
- Checkpoint: `CHECKPOINT_CREATED`, `CHECKPOINT_RESTORED`
- Queue: `QUEUE_ITEM_ADDED/STARTED/COMPLETED/FAILED/BLOCKED/CANCELLED`
- Safety: `SAFETY_PAUSED/RESUMED/SHUTDOWN`, `DEADLOCK_DETECTED`,
  `RESOURCE_WARNING`, `HEARTBEAT`
- Runtime: `RUNNER_STARTED/STOPPED`, `MEMORY_SAVED/RESTORED`
- Fallback: `UNKNOWN` (safe coercion on unknown type strings)

## API

- `subscribe(handler)` — receives every event.
- `subscribe_type(handler, *types)` — filtered subscription.
- `publish(type, payload)` — fans out, appends to JSONL log (max 1000
  in-memory entries kept).
- `recent(n)` / `to_dict_list(n)` — last n events for dashboard/resume.
- Event shape: `{"type", "payload", "timestamp"}`.

## Engine integration

- The engine subscribes its outbox to the bus, so every event also fans
  out to configured connectors (Phase G) — dashboard hooks, webhooks, MCP.
- Stop conditions and checkpoints publish their events; the dashboard
  `GET /api/engine/events` and the plugin `titus_engine_status` both read
  the same `events.log`.

## Verification

`test_m5_autonomous.py::TestEvents` — subscribe + publish, type filter,
recent + unknown coercion, persistent log with correct JSON lines.
