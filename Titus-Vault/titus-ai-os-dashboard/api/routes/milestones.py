"""Milestones API routes."""

from fastapi import APIRouter
from pathlib import Path

router = APIRouter()

VAULT_ROOT = Path(__file__).parent.parent.parent.parent


@router.get("/")
async def list_milestones():
    """List all milestones for current project."""
    project_dir = VAULT_ROOT / "06-Projects" / "Titus-AI-OS-Upgrade"
    
    milestones = []
    
    # Find M2 and M3 completion reports
    for md_file in project_dir.glob("M*_COMPLETION_REPORT.md"):
        content = md_file.read_text(encoding="utf-8")
        
        # Parse milestone info
        name = md_file.stem.replace("_COMPLETION_REPORT", "").replace("_", " ")
        status = "complete" if "VERIFIED_COMPLETE" in content else "in_progress"
        
        milestones.append({
            "id": md_file.stem,
            "name": name,
            "status": status,
            "file": md_file.name,
        })
    
    # Add M3 as current
    milestones.append({
        "id": "M3",
        "name": "M3: Orchestration & Interface",
        "status": "in_progress",
        "progress": 45,
    })
    
    return {"milestones": milestones, "current": "M3"}


@router.get("/{milestone_id}")
async def get_milestone(milestone_id: str):
    """Get milestone details."""
    project_dir = VAULT_ROOT / "06-Projects" / "Titus-AI-OS-Upgrade"
    
    # Find matching file
    for md_file in project_dir.glob(f"{milestone_id}*_COMPLETION_REPORT.md"):
        content = md_file.read_text(encoding="utf-8")
        return {
            "id": milestone_id,
            "name": md_file.stem.replace("_COMPLETION_REPORT", "").replace("_", " "),
            "content": content,
            "status": "complete" if "VERIFIED_COMPLETE" in content else "in_progress",
        }
    
    return {"error": "Milestone not found"}
