# M5 — Checkpoint System

**File:** `api/orchestration/checkpoint.py`
**Status:** COMPLETE

---

## Purpose

Checkpoints capture the full engine state so the autonomous runner can
pause, resume, roll back, and recover after interruption or failure. Every
checkpoint snapshot stores the complete engine state: milestones, sprints,
queue, approvals, recent events, and safety status.

## Layout

```
engine-state/checkpoints/
  checkpoint-<YYYYmmdd-HHMMSS>-<label>.json   immutable snapshots
  latest.json                                 pointer to most recent
```

`<label>` is sanitized (`_safe_filename`: only `[A-Za-z0-9._-]`), so
arbitrary labels cannot break paths.

## Operations

| Operation | Behavior |
|-----------|----------|
| `create(snapshot, label)` | Writes snapshot, updates `latest.json`, prunes old files (keep=50). Returns checkpoint id. |
| `latest()` | Snapshot from `latest.json` pointer (falls back to newest file). |
| `get(cp_id)` | Snapshot for a specific id. |
| `list_checkpoints()` | Ordered metadata list (id, created_at, label) for the dashboard. |
| `restore(cp_id)` | Returns snapshot AND repoints `latest.json` to it. |
| `rollback(to=None)` | Returns the previous snapshot (or an explicit one) and repoints latest. Requires >= 2 checkpoints. |

## Engine integration

- The engine checkpoints after every sprint
  (`checkpoint_every_sprint=True`), at stop conditions
  (`awaiting-approval`, `blocked`, `verification-failed`), and on
  milestone completion (`milestone-complete`).
- `engine.rollback()` / `engine.restore()` reload milestone, queue,
  approval, and safety state from the snapshot (`_restore_snapshot`).
- Dashboard: `POST /api/engine/checkpoint/rollback`; plugin shows the
  latest checkpoint in `titus_engine_status`.

## Recovery flow

1. Engine stops or crashes.
2. On resume, OpenCode calls `titus_engine_resume` which reports the
   latest checkpoint.
3. Owner (or the CEO) restores it: `engine.restore()` repoints to the
   last good state.
4. `run()` continues from the restored milestone/sprint.

## Verification

`test_m5_autonomous.py::TestCheckpoints` — create/latest/get, rollback to
previous, pruning (keep=3 -> 3 files), safe filename sanitization.
Engine-level rollback covered by `test_rollback_restores_previous_checkpoint`.
