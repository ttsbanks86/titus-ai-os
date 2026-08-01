# M5 — Automation Connectors

**File:** `api/orchestration/connectors.py`
**Status:** COMPLETE

---

## Purpose

Stable interfaces for external automation surfaces: OpenCode hooks
(state JSON files the M5 hybrid plugin reads), MCP outbox, n8n/cloud
webhooks, future schedulers. Design rule from the mission: do NOT depend
on external services. Connectors are sinks that write structured JSON to
known locations or POST to configured endpoints ONLY when enabled. If
nothing is configured they are no-ops and the engine runs fully standalone.

## Components

| Component | Behavior |
|-----------|----------|
| `ConnectorSink` | Base class: `emit(record) -> bool`, `describe()`. |
| `FileSink` | Writes each record as `out_dir/<name>-<ts>.json`. Used for OpenCode hooks / MCP outbox. |
| `WebhookSink` | POSTs JSON to a configured URL (n8n, cloud worker). Returns False (no-op) when no URL set — engine unaffected. 10s timeout, fail-soft. |
| `EventOutbox` | Fan-out: emits one record to every configured sink, returning per-sink success map. |

## Engine integration

The engine subscribes its `EventOutbox` to the event bus, so every event
is emitted to all configured sinks. Default deployment: the dashboard +
plugin read the shared state dir directly, so no extra sinks are required.

## Sink configuration

```python
from orchestration.connectors import FileSink, WebhookSink
engine.outbox.add(FileSink(out_dir=r"~/.config/opencode/engine-state/hooks", name="hooks"))
engine.outbox.add(WebhookSink(url=os.environ.get("TITUS_WEBHOOK_URL")))  # off unless set
```

## Verification

`test_m5_autonomous.py::TestConnectors` — FileSink writes valid JSON
records, WebhookSink no-ops without a URL, EventOutbox fan-out returns
per-sink results and describe().
