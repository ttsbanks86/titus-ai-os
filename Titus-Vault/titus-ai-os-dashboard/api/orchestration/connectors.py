"""
Titus AI OS M5 Automation Connectors

Stable interfaces for external automation surfaces:

- n8n webhook sink
- OpenCode hooks (state JSON files the M4 hybrid plugin / hooks read)
- MCP (outbox JSON the MCP server picks up)
- future schedulers / cloud workers

Design rule (mission): do NOT depend on external services. All connectors
are sinks that write structured JSON to known locations or POST to
configured endpoints only when enabled. If nothing is configured, the
connectors are no-ops and the engine runs fully standalone.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConnectorSink:
    """Base class: all sinks implement emit(record)."""

    name = "base"

    def emit(self, record: Dict) -> bool:
        raise NotImplementedError

    def describe(self) -> Dict:
        return {"name": self.name, "enabled": True}


class FileSink(ConnectorSink):
    """Write JSON records to a directory (OpenCode hooks, MCP outbox)."""

    def __init__(self, out_dir: str, name: str = "file"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.name = name

    def emit(self, record: Dict) -> bool:
        try:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            path = self.out_dir / f"{self.name}-{ts}.json"
            path.write_text(
                json.dumps(record, indent=2, default=str), encoding="utf-8"
            )
            return True
        except OSError as e:
            logger.warning("FileSink(%s) write failed: %s", self.name, e)
            return False


class WebhookSink(ConnectorSink):
    """POST JSON to a configured endpoint (n8n, cloud worker). Off unless URL set."""

    def __init__(self, url: Optional[str] = None, name: str = "webhook"):
        self.url = url
        self.name = name

    def emit(self, record: Dict) -> bool:
        if not self.url:
            return False  # not configured -> no-op, engine still works
        try:
            import urllib.request

            req = urllib.request.Request(
                self.url,
                data=json.dumps(record, default=str).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return 200 <= resp.status < 300
        except Exception as e:
            logger.warning("WebhookSink(%s) failed: %s", self.url, e)
            return False


class EventOutbox:
    """
    Fan-out event records to all configured sinks.
    Sinks are created by the engine from config; default = one FileSink
    for the OpenCode hybrid integration (state/events dir).
    """

    def __init__(self, sinks: Optional[list] = None):
        self.sinks: list = sinks or []

    def add(self, sink: ConnectorSink) -> None:
        self.sinks.append(sink)

    def emit(self, record: Dict) -> Dict[str, bool]:
        results = {}
        for sink in self.sinks:
            results[sink.name] = sink.emit(record)
        return results

    def describe(self) -> list:
        return [s.describe() for s in self.sinks]
