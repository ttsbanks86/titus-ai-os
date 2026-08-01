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
    """Main workspace overview."""
    return {
        "greeting": "Good day, Titus",
        "current_project": "Titus AI OS Upgrade",
        "current_milestone": "M3: Orchestration & Interface",
        "milestone_progress": 45,
        "test_status": {"total": 131, "passing": 131, "status": "passing"},
        "ci_status": "passing",
        "security_status": "clean",
        "quick_actions": [
            {"id": "start-milestone", "label": "Start Milestone", "requires_approval": True},
            {"id": "run-tests", "label": "Run Tests", "requires_approval": False},
            {"id": "refresh-index", "label": "Refresh Index", "requires_approval": False},
            {"id": "assemble-context", "label": "Assemble Context", "requires_approval": False},
        ]
    }
