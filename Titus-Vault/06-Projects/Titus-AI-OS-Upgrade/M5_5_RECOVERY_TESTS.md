# M5.5 Recovery Tests — Titus AI OS

**Milestone:** M5.5 — Platform Validation, Hardening, and Production Readiness
**Date:** 2026-07-31
**Scope:** Prove the platform recovers from crashes, shutdowns, runtime violations, and failed starts — and that recovery is lossless.

## Test 1 — Crash / Restart / Resume (process boundary)

- Scenario: engine planned 3 sprints, ran sprint 1, stopped at a HIGH approval gate. Simulated crash = discard the process entirely; new process, same state dir + vault project dir.
- Action: `restore()` from latest checkpoint.
- Result: PASS — milestone id, queue (2 completed / 3 queued), pending approval, and memory context all restored identically. Approved the gated task, run resumed and completed all 3 sprints → `VERIFIED_COMPLETE`, report `verified_complete`, 5 checkpoints on disk.

## Test 2 — Runtime limit guard (safety monitor)

- Scenario: engine with `max_runtime_hours = 0.001` (3.6s budget) on a 60-sprint milestone.
- Result: PASS — engine stopped at 4.56s with reason `MAX_RUNTIME exceeded (3.6s)`. Guard fires and returns a clean stop reason; state remains restorable.

## Test 3 — Sustained run, no false stops

- Scenario: 40-sprint / 80-task run with 1-minute runtime budget.
- Result: PASS — ran to `VERIFIED_COMPLETE` in 20.32s with 41 checkpoints; heartbeat advanced to "sprint 40/40"; no false shutdown, no stagnation.

## Test 4 — Dashboard cold-start failure → repair → recovery

- Scenario: fresh boot through `Start-TitusAIOS.ps1` failed (API never healthy). Root cause: `main:app` launch string vs package-relative imports (`ImportError: attempted relative import with no known parent package`).
- Action: repaired launcher + `start.ps1` + README to `api.main:app` from the dashboard root.
- Result: PASS — subsequent cold start healthy; port 8000 listening; `/api/health` 200; `/api/engine/status` returns milestone + state dir; `/api/workspace` returns milestone + 70/70 tests.

## Test 5 — State-file integrity across sessions

- Scenario: session 1 and session 2 (separate engine instances) against the same state dir.
- Result: PASS — queue.json, approvals.json, checkpoint files, and events.log written by session 1 were read and restored by session 2 without corruption; no partial writes observed (atomic file writes per module).

## Regression

- 70/70 tests pass after all repairs (no code changes were required for recovery — the defect was in launch configuration, not engine logic).

## Verdict

PASS — recovery is lossless at process boundaries, the runtime guard fires correctly, sustained runs do not false-stop, and failed starts are diagnosable and repairable.
