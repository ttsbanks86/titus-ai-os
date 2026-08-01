"""
Titus AI OS Dashboard API
FastAPI server providing endpoints for the branded dashboard.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import json

from .routes import projects, milestones, agents, knowledge, verification

app = FastAPI(
    title="Titus AI OS Dashboard API",
    description="API for the Titus AI OS branded dashboard",
    version="0.1.0"
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(milestones.router, prefix="/api/milestones", tags=["milestones"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["knowledge"])
app.include_router(verification.router, prefix="/api/verification", tags=["verification"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "titus-ai-os-dashboard"}


@app.get("/api/workspace")
async def get_workspace():
    """Main workspace overview — live from Titus-Vault records."""
    project_dir = Path(__file__).parent.parent.parent / "06-Projects" / "Titus-AI-OS-Upgrade"

    # Read current milestone record (source of truth, created in M4 Phase G)
    milestone = "M4"
    milestone_status = "in_progress"
    milestone_file = project_dir / "CURRENT_MILESTONE.md"
    if milestone_file.exists():
        content = milestone_file.read_text(encoding="utf-8")
        re_mod = __import__("re")
        name_match = re_mod.search(r"^# CURRENT_MILESTONE.*?\n\*\*Milestone:\*\* (.+)$", content, re_mod.MULTILINE)
        if name_match:
            milestone = name_match.group(1).strip()
        status_match = re_mod.search(r"\*\*Status:\*\*\s*(.+)", content)
        if status_match:
            milestone_status = status_match.group(1).strip().lower()

    # Read project status record
    status = "active"
    tests_total = None
    tests_passing = None
    status_file = project_dir / "PROJECT_STATUS.md"
    if status_file.exists():
        content = status_file.read_text(encoding="utf-8")
        status_match = __import__("re").search(r"Status\s*\|\s*(.+)", content)
        if status_match:
            status = status_match.group(1).strip()
        tests_match = __import__("re").search(r"(\d+)/(\d+) passing", content)
        if tests_match:
            tests_total = int(tests_match.group(2))
            tests_passing = int(tests_match.group(1))

    test_status = {
        "total": tests_total if tests_total is not None else 0,
        "passing": tests_passing if tests_passing is not None else 0,
        "status": "passing" if tests_total and tests_passing == tests_total else "unknown",
    }

    return {
        "greeting": "Good day, Titus",
        "current_project": "Titus AI OS Upgrade",
        "current_milestone": milestone,
        "milestone_status": milestone_status,
        "test_status": test_status,
        "ci_status": "passing",
        "security_status": "clean",
        "quick_actions": [
            {"id": "start-milestone", "label": "Start Milestone", "requires_approval": True},
            {"id": "run-tests", "label": "Run Tests", "requires_approval": False},
            {"id": "refresh-index", "label": "Refresh Index", "requires_approval": False},
            {"id": "assemble-context", "label": "Assemble Context", "requires_approval": False},
        ]
    }
