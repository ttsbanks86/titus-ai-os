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
    
    # Find all completion reports
    for md_file in sorted(project_dir.glob("M*_COMPLETION_REPORT.md")):
        content = md_file.read_text(encoding="utf-8")
        
        # Parse milestone info
        name = md_file.stem.replace("_COMPLETION_REPORT", "").replace("_", " ")
        upper = content.upper()
        status_line = next((l for l in content.split("\n") if l.strip().lower().startswith("**status**") or l.strip().startswith("Status:")), "")
        status = (
            "complete"
            if ("VERIFIED_COMPLETE" in upper or "MERGED TO MAIN" in upper or "COMPLETE" in status_line.upper())
            else "in_progress"
        )
        
        milestones.append({
            "id": md_file.stem,
            "name": name,
            "status": status,
            "file": md_file.name,
        })
    
    # Current milestone from CURRENT_MILESTONE.md (M4 record, source of truth)
    current = "M4"
    current_file = project_dir / "CURRENT_MILESTONE.md"
    if current_file.exists():
        content = current_file.read_text(encoding="utf-8")
        id_match = __import__("re").search(r"^# CURRENT_MILESTONE\s*—\s*(.+)$", content)
        if id_match:
            current = id_match.group(1).strip()
    
    return {"milestones": milestones, "current": current}


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
