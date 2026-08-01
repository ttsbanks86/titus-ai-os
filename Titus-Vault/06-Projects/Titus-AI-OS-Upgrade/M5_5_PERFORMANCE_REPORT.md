# M5.5 Performance Report — Titus AI OS

**Milestone:** M5.5 — Platform Validation, Hardening, and Production Readiness
**Date:** 2026-07-31
**Method:** Stopwatch-measured runs on the local machine (Windows, Python 3.13). All engine numbers use the real `AutonomousEngine`; test numbers use the committed suite.

## Measured Numbers

| Benchmark | Result | Notes |
|-----------|--------|-------|
| Test suite (70 tests) | 8.28s | `pytest tests\test_m3_modules.py tests\test_m5_autonomous.py`; ~119ms/test |
| Plan milestone (3 sprints, 5 tasks) | part of 1.04s | includes milestone creation + queue + approvals + first run to gate |
| Run to approval gate (sprint 1) | 1.04s total (plan + run) | engine stops at HIGH approval gate |
| Restore from checkpoint + approve + finish (3 sprints) | 1.60s | fresh process → restore → approve → complete |
| Sustained execution | 20.32s for 40 sprints / 80 tasks | ~0.5s per sprint incl. verification + checkpoint write |
| Checkpoint write throughput | 41 checkpoints in 20.32s | ~0.5s per checkpoint incl. sprint work |
| Dashboard cold start | < 20s (launcher health window) | uvicorn boot ~2–4s after import fix; launcher completes with no warnings |
| Dashboard health poll | 200 OK | `/api/health` |
| Context assembly (Source of Truth read) | instant (in-memory file read) | `ProjectMemory.source_of_truth()` |

## Resource Footprint

- Engine state per run: queue.json + approvals.json + events.log + N checkpoint files under `checkpoints/` in the state dir (5 files + 1 per sprint + milestone-complete).
- Dashboard: single uvicorn process on :8000; frontend static server on :3000.
- No background daemons; no scheduled jobs; no auto-spend.

## Observations (non-blocking)

- Checkpoint size grows with milestone scope (one snapshot per sprint). `CheckpointSystem` prunes to `keep` (default 50) — retention capped by design.
- Queue items retain terminal `queued` markers after milestone completion because the queue is an execution ledger; completion truth is the milestone status (`VERIFIED_COMPLETE`). Cosmetic, no fix required.
- All measured times are on local hardware with simulated task execution (`_run_task`); real agent-invoked tasks will add tool-call latency proportional to the tools used, not to the platform itself.

## Verdict

PASS — platform overhead is negligible (sub-second plan/restore, ~0.5s/sprint, ~3s dashboard boot). No performance blockers for daily use.
