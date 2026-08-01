# M5 — Owner Approval Model

**File:** `api/orchestration/approval.py`
**Status:** COMPLETE

---

## Purpose

Every autonomous action carries an approval level. The model gates what the
engine may do on its own vs. what requires the owner. CRITICAL operations
also route through the existing guardrails module (`api/guardrails`,
`SafetyLevel`) for defense in depth.

## Levels

| Level | Requires owner | Policy |
|-------|---------------|--------|
| `LOW` | never | Fully automatic (docs, tests, formatting, safe refactoring). Granted immediately at `request()`. |
| `MEDIUM` | never | New modules, safe configuration. Waits, then auto-granted by `auto_approve()` after verification passes. |
| `HIGH` | yes | Architecture, security, database, breaking changes. Pending until owner decides. |
| `CRITICAL` | yes, always | Repo rewrite, credential changes, production deployment. Owner decision mandatory. |

`rank` orders levels: LOW(0) < MEDIUM(1) < HIGH(2) < CRITICAL(3).

## States

`PENDING` -> `GRANTED` | `DENIED` (owner) | `AUTO_GRANTED` (system, LOW or
verified MEDIUM).

## API

- `request(item_id, description, level, reason)` — idempotent per item.
- `requires_owner(item_id)` — true while a HIGH/CRITICAL request is pending.
- `auto_approve(item_id)` — grants LOW/MEDIUM after success + verification.
- `decide(item_id, granted, by)` — owner decision; persists decided_at/by.
- `is_approved(item_id)`, `pending()`, `all()`.
- `save_state()` / `load_state()` — approvals survive restarts.

## Engine integration

1. `plan()` registers an approval request per task at its level.
2. `_execute_sprint()` checks `requires_owner()` BEFORE executing: if
   pending, the task goes `AWAITING_APPROVAL`, the engine checkpoints and
   stops with `{"status": "awaiting_approval"}`.
3. Owner decides via `engine.approve(task, granted)` (or the dashboard
   `POST /api/engine/approvals/{item}/decide`, or the plugin
   `titus_engine_approve`).
4. `run()` resumes; the gate now passes and execution continues.

## Verification

`test_m5_autonomous.py::TestApprovals` — LOW auto-grant, MEDIUM
post-verification auto-grant, HIGH owner requirement + decision, DENIED
stays denied, rank ordering, persistence.
Engine-level: `test_approval_gate_stops_and_resumes`.
