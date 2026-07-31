"""Projects API routes."""

from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter()

VAULT_ROOT = Path(__file__).parent.parent.parent.parent / "Titus-Vault"


@router.get("/")
async def list_projects():
    """List all projects with status."""
    projects_dir = VAULT_ROOT / "06-Projects"
    projects = []
    
    for item in projects_dir.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Read project info if available
            readme = item / "README.md"
            status = "active"
            phase = "unknown"
            progress = 0
            
            if readme.exists():
                content = readme.read_text(encoding="utf-8")
                # Simple parsing for status
                if "Status:" in content:
                    for line in content.split("\n"):
                        if "Status:" in line:
                            status = line.split("Status:")[-1].strip()
            
            projects.append({
                "id": item.name,
                "name": item.name.replace("-", " ").replace("_", " "),
                "path": str(item),
                "status": status,
                "phase": phase,
                "progress": progress,
            })
    
    return {"projects": projects, "total": len(projects)}


@router.get("/{project_id}")
async def get_project(project_id: str):
    """Get project details."""
    project_dir = VAULT_ROOT / "06-Projects" / project_id
    
    if not project_dir.exists():
        return {"error": "Project not found"}
    
    # Read all markdown files in project
    docs = []
    for md_file in project_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        docs.append({
            "name": md_file.name,
            "content": content[:500],  # Preview
            "size": len(content),
        })
    
    return {
        "id": project_id,
        "name": project_id.replace("-", " ").replace("_", " "),
        "path": str(project_dir),
        "documents": docs,
        "document_count": len(docs),
    }
