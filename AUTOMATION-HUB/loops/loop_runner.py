#!/usr/bin/env python3
"""Titus AI OS — Autonomous Loop Runner
Loops run agents iteratively: set goal → execute → check → repeat until done → notify.
"""
import sys, json, os, time, subprocess, datetime, logging
from pathlib import Path

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

LOOPS_DIR = Path.home() / "Desktop" / "Live Cowork" / "AUTOMATION-HUB" / "loops"
LOOPS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOOPS_DIR / "runner.log"
STATUS_FILE = LOOPS_DIR / "status.json"

logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_status():
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text())
    return {"loops": {}}

def save_status(data):
    STATUS_FILE.write_text(json.dumps(data, indent=2))

# ─── Loop Definitions ─────────────────────────────────────────────────────
LOOPS = {
    "job-search": {
        "goal": "Find and apply to BA roles daily until employed",
        "tasks": [
            {"action": "Check Indeed for new BA postings", "command": "hub.ps1 -Command check-messages"},
            {"action": "Check LinkedIn for recruiter messages", "command": "hub.ps1 -Command check-messages"},
            {"action": "Review job tracker for follow-ups", "file": "JOB-TRACKER.md"},
            {"action": "Apply to 1-2 new BA roles if open", "manual": True}
        ],
        "success_criteria": "5+ applications submitted per week",
        "schedule": "daily"
    },
    "skill-upgrade": {
        "goal": "Identify and close skill gaps for BA roles",
        "tasks": [
            {"action": "Run self-growth scan for new tools", "command": "self-growth.ps1"},
            {"action": "Check tracked repos for updates", "command": "goldmine.ps1 -Command goldmine"},
            {"action": "Review design inspiration trends", "command": "design-inspiration.ps1"}
        ],
        "success_criteria": "1 new skill or tool identified per week",
        "schedule": "daily"
    },
    "app-maintenance": {
        "goal": "Keep all apps running, updated, and bug-free",
        "tasks": [
            {"action": "Check system health", "command": "hub.ps1 -Command status"},
            {"action": "Verify all EXEs exist and run", "manual": True},
            {"action": "Check for process leaks (stale EXEs)", "command": "powershell Get-Process | Where-Object { $_.ProcessName -match 'Whisper|NOLA|Voice' }"}
        ],
        "success_criteria": "All apps functional with <500MB total memory",
        "schedule": "daily"
    }
}

def run_loop(loop_name):
    loop = LOOPS.get(loop_name)
    if not loop:
        logging.error(f"Unknown loop: {loop_name}")
        return

    status = load_status()
    loop_state = status["loops"].get(loop_name, {"runs": 0, "last_result": None})
    loop_state["runs"] += 1
    loop_state["last_run"] = datetime.datetime.now().isoformat()
    
    logging.info(f"=== Running loop: {loop_name} (run #{loop_state['runs']}) ===")
    print(f"\n{'='*50}")
    print(f"  LOOP: {loop_name}")
    print(f"  Goal: {loop['goal']}")
    print(f"  Run:  #{loop_state['runs']}")
    print(f"{'='*50}")
    
    results = []
    for task in loop["tasks"]:
        action = task["action"]
        print(f"\n  -> {action}...")
        
        if "command" in task:
            try:
                hub_path = Path.home() / "Desktop" / "Live Cowork" / "AUTOMATION-HUB"
                result = subprocess.run(
                    ["powershell", "-NoProfile", "-File", str(hub_path / task["command"].split()[0])] + task["command"].split()[1:],
                    capture_output=True, text=True, timeout=120, cwd=str(hub_path)
                )
                if result.returncode == 0:
                    print(f"    ✓ Done")
                    results.append({"action": action, "status": "ok", "output": result.stdout[:200]})
                else:
                    print(f"    ⚠ Failed (code {result.returncode})")
                    results.append({"action": action, "status": "failed", "error": result.stderr[:200]})
            except Exception as e:
                print(f"    ✗ Error: {e}")
                results.append({"action": action, "status": "error", "error": str(e)})
        
        elif "manual" in task and task["manual"]:
            print(f"    ⏳ Requires manual action: {action}")
            results.append({"action": action, "status": "manual"})
        
        elif "file" in task:
            fp = Path.home() / "Desktop" / "Live Cowork" / task["file"]
            if fp.exists():
                print(f"    ✓ File found")
                results.append({"action": action, "status": "ok"})
            else:
                print(f"    ⚠ File not found")
                results.append({"action": action, "status": "missing"})
    
    # Determine overall status
    errors = [r for r in results if r["status"] in ("failed", "error")]
    manual = [r for r in results if r["status"] == "manual"]
    
    if errors:
        loop_state["last_result"] = "partial"
        print(f"\n  🟡 Loop completed with {len(errors)} error(s)")
    elif manual:
        loop_state["last_result"] = "needs-attention"
        print(f"\n  🟠 Loop needs manual attention ({len(manual)} tasks)")
    else:
        loop_state["last_result"] = "success"
        print(f"\n  🟢 Loop completed successfully!")
    
    loop_state["results"] = results
    status["loops"][loop_name] = loop_state
    save_status(status)
    
    print(f"{'='*50}\n")

def run_all_loops():
    logging.info("=== Running ALL loops ===")
    for name in LOOPS:
        run_loop(name)
    logging.info("=== All loops complete ===")

def status_summary():
    status = load_status()
    print(f"\n{'='*50}")
    print(f"  LOOP STATUS SUMMARY")
    print(f"{'='*50}")
    for name, state in status["loops"].items():
        last = state.get("last_result", "never")
        icon = {"success": "🟢", "partial": "🟡", "needs-attention": "🟠", "never": "⚪"}
        print(f"  {icon.get(last, '⚪')} {name}: run #{state['runs']} — {last}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            run_all_loops()
        elif sys.argv[1] == "status":
            status_summary()
        elif sys.argv[1] in LOOPS:
            run_loop(sys.argv[1])
        else:
            print(f"Unknown loop. Available: {list(LOOPS.keys())} ['all', 'status']")
    else:
        run_all_loops()
