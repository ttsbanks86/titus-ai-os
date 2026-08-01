# M5 — Long-Running Execution (Safety Monitor)

**File:** `api/orchestration/safety.py`
**Status:** COMPLETE

---

## Purpose

Guards for long-running autonomous execution. The engine is designed to run
for up to 12 hours on a single milestone prompt; the safety monitor ensures
it cannot silently hang, overrun, or keep working after the owner asks it
to stop.

## Guards

| Guard | Default | Behavior |
|-------|---------|----------|
| Max runtime | 12h | Violation if `now - start > max_runtime_seconds`. |
| Heartbeat timeout | 600s | Violation if no heartbeat within the window (watchdog). |
| Deadlock | 5 stagnant heartbeats | `heartbeat(progress)` resets the counter when progress text changes; no change for N heartbeats = deadlock. |
| Retry limits | 3 | Exhausted retries = stop condition (engine-level, from queue). |
| Resources | CPU/MEM 90% warn | Via psutil if installed; degrades with a one-time warning when absent (stdlib-only). |
| Pause | — | `pause()` stops the run loop; `resume()` resets deadlock counter. |
| Shutdown | — | `request_shutdown(reason)` / `shutdown(reason)` halt the engine. |

## Usage pattern

```python
mon = SafetyMonitor(state_dir=..., max_runtime_hours=12)
mon.heartbeat("sprint 3/10")          # after each unit of work
stop, reason = mon.should_stop(progress)
if stop: ...                          # checkpoint + stop with reason
mon.shutdown("milestone_completed")   # clean end
```

Heartbeats are appended to `engine-state/heartbeat.json` (JSONL) so the
dashboard and the OpenCode plugin can show liveness externally.

## Engine integration

`AutonomousEngine.run()` calls `should_stop()` before every sprint and
publishes `SAFETY_SHUTDOWN` when a guard trips. `pause()`/`resume()`/
`request_stop()` are exposed as engine + dashboard controls. Restoring a
checkpoint resets the safety monitor (`_restore_snapshot` rebuilds it) so
a resumed run gets fresh timers.

## Verification

`test_m5_autonomous.py::TestSafety` — deadlock detection after N stagnant
heartbeats, progress resets the counter, max-runtime violation via clock
manipulation, pause/resume, shutdown request, heartbeat file with correct
JSONL entries. All checks avoid real sleeps (compressed timers).
