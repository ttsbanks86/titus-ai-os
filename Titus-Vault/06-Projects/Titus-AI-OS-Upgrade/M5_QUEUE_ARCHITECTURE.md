# M5 — Execution Queue Architecture

**File:** `api/orchestration/queue.py`
**Status:** COMPLETE

---

## Purpose

The queue is the single source of truth for what the engine should do next.
Tasks are enqueued at `plan()` time with a priority and dependency list;
the engine pulls the next ready item, executes it, and records the outcome.

## States

| State | Meaning |
|-------|---------|
| `queued` | Enqueued, waiting to run |
| `running` | Currently executing |
| `waiting` | Held (dependency not complete or manually held) |
| `blocked` | Permanently blocked (error recorded) |
| `failed` | Retries exhausted |
| `completed` | Done (result recorded) |
| `retry` | Failed once; eligible for re-run |
| `cancelled` | Removed from execution |

## Selection rule

`next_ready()` returns the highest-priority item whose status is
`queued` or `retry` AND whose dependencies are all `completed`. Priority
is `int` (higher wins). This gives deterministic execution order with
dependency safety.

## Retry semantics

`retry(item_id)` increments `retry_count`; when `retry_count >= max_retries`
(engine default 3), the item is marked `failed` and the sprint stops.

## Persistence

`save_state()` / `load_state()` write the item list to `queue.json` in the
engine state dir (`~/.config/opencode/engine-state/`). `owner_action`
callables are NOT serialized (load re-injects `None`); the engine re-binds
work at execution time, so resume after restart is safe.

## Engine integration

- `plan()` enqueues one `QueueItem` per task with its priority.
- `_execute_sprint()` marks running -> executes -> marks completed/failed.
- Queue state is included in every checkpoint snapshot and in `report()`.

## Verification

`test_m5_autonomous.py::TestQueue` — priority order, dependency blocking,
retry limits, persistence (owner_action not serialized), status counts.
