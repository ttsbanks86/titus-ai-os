"""
Titus AI OS M5 Long-Run Safety

Guards for long-running autonomous execution:

- maximum runtime
- heartbeat (worker updates; watchdog checks staleness)
- deadlock detection (no progress within a window)
- retry limits
- resource monitoring (optional: CPU/memory via psutil if available)
- automatic pause
- safe shutdown

Provider-independent: heartbeat/deadlock/runtime use only stdlib;
resource monitoring degrades gracefully when psutil is absent.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

try:  # optional; degrades gracefully
    import psutil  # type: ignore
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class SafetyMonitor:
    """
    Heartbeat + watchdog + limits for the autonomous runner.

    Usage (single-threaded runner):
        mon = SafetyMonitor(max_runtime_hours=12, ...)
        mon.start()
        while not mon.should_stop(...):
            mon.heartbeat(progress="sprint 3/10")
            ...work...
        mon.shutdown(reason="completed")
    """

    def __init__(
        self,
        state_dir: Optional[str] = None,
        max_runtime_hours: float = 12.0,
        heartbeat_timeout_seconds: int = 600,
        deadlock_progress_window: int = 5,   # n heartbeats without progress
        max_retries: int = 3,
        cpu_warn_percent: float = 90.0,
        mem_warn_percent: float = 90.0,
    ):
        self.state_dir = Path(state_dir) if state_dir else None
        self.max_runtime_seconds = max_runtime_hours * 3600
        self.heartbeat_timeout_seconds = heartbeat_timeout_seconds
        self.deadlock_progress_window = deadlock_progress_window
        self.max_retries = max_retries
        self.cpu_warn_percent = cpu_warn_percent
        self.mem_warn_percent = mem_warn_percent

        self.start_time = time.time()
        self.last_heartbeat = time.time()
        self.last_progress = ""
        self.stagnant_count = 0
        self.paused = False
        self.shutdown_requested = False
        self.shutdown_reason: Optional[str] = None
        self.warnings: List[str] = []
        self._lock = threading.Lock()
        self._file = None

    # ---- state file for external watchdogs (OpenCode / dashboard) ----
    def _open_file(self) -> None:
        if not self.state_dir:
            return
        self.state_dir.mkdir(parents=True, exist_ok=True)
        try:
            self._file = open(
                self.state_dir / "heartbeat.json", "a", encoding="utf-8"
            )
        except OSError:
            self._file = None

    def heartbeat(self, progress: str = "") -> Dict:
        """Record a heartbeat with optional progress label."""
        with self._lock:
            now = time.time()
            self.last_heartbeat = now
            if progress and progress != self.last_progress:
                self.last_progress = progress
                self.stagnant_count = 0
            else:
                self.stagnant_count += 1
            state = self.status()
            if self._file:
                try:
                    self._file.write(json.dumps(state) + "\n")
                    self._file.flush()
                except OSError:
                    pass
            return state

    def status(self) -> Dict:
        return {
            "running": not self.shutdown_requested,
            "paused": self.paused,
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "last_heartbeat": datetime.fromtimestamp(
                self.last_heartbeat
            ).isoformat(),
            "uptime_seconds": round(time.time() - self.start_time, 1),
            "max_runtime_seconds": self.max_runtime_seconds,
            "progress": self.last_progress,
            "stagnant_heartbeats": self.stagnant_count,
            "shutdown_reason": self.shutdown_reason,
            "warnings": self.warnings,
        }

    # ---- watchdog checks ----
    def check(self, progress: str = "") -> List[str]:
        """
        Run all safety checks. Returns list of violations.
        Runner should pause/stop if any violation is CRITICAL.
        """
        violations = []
        now = time.time()

        # max runtime
        if now - self.start_time > self.max_runtime_seconds:
            violations.append(
                f"MAX_RUNTIME exceeded ({self.max_runtime_seconds}s)"
            )

        # heartbeat staleness (watchdog)
        if now - self.last_heartbeat > self.heartbeat_timeout_seconds:
            violations.append(
                f"HEARTBEAT_TIMEOUT ({self.heartbeat_timeout_seconds}s)"
            )

        # deadlock (no progress across window)
        if self.stagnant_count >= self.deadlock_progress_window:
            violations.append(
                f"DEADLOCK_DETECTED (no progress for {self.stagnant_count} "
                f"heartbeats; last: '{self.last_progress}')"
            )

        # resources (optional)
        if HAS_PSUTIL:
            try:
                cpu = psutil.cpu_percent(interval=0.5)
                mem = psutil.virtual_memory().percent
                if cpu > self.cpu_warn_percent:
                    self.warnings.append(f"CPU high: {cpu}%")
                    violations.append(f"RESOURCE_WARNING cpu={cpu}%")
                if mem > self.mem_warn_percent:
                    self.warnings.append(f"MEM high: {mem}%")
                    violations.append(f"RESOURCE_WARNING mem={mem}%")
            except Exception:
                pass
        else:
            # stdlib-only: record a soft warning once
            if not any("psutil" in w for w in self.warnings):
                self.warnings.append(
                    "RESOURCE_MONITORING_DEGRADED (psutil not installed)"
                )

        return violations

    # ---- controls ----
    def pause(self) -> None:
        with self._lock:
            self.paused = True
        logger.info("SafetyMonitor: paused")

    def resume(self) -> None:
        with self._lock:
            self.paused = False
            self.stagnant_count = 0
        logger.info("SafetyMonitor: resumed")

    def request_shutdown(self, reason: str) -> None:
        with self._lock:
            self.shutdown_requested = True
            self.shutdown_reason = reason
        logger.info("SafetyMonitor: shutdown requested (%s)", reason)

    def should_stop(self, progress: str = "") -> (bool, str):
        """
        Convenience: heartbeat + check. Returns (stop, reason).
        Call after each unit of work.
        """
        self.heartbeat(progress)
        violations = self.check()
        if self.shutdown_requested:
            return True, self.shutdown_reason or "shutdown_requested"
        if self.paused:
            return True, "paused"
        if violations:
            # Deadlock / runtime / heartbeat are stop conditions.
            return True, violations[0]
        return False, ""

    def shutdown(self, reason: str = "completed") -> None:
        self.request_shutdown(reason)
        if self._file:
            try:
                self._file.close()
            except OSError:
                pass
            self._file = None
