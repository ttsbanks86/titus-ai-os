"""
Titus AI OS Agent Orchestration
Task routing, handoffs, approval gates, and evidence collection.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
import json
from pathlib import Path


class TaskStatus(Enum):
    """Task status states."""
    PLANNED = "planned"
    READY = "ready"
    RUNNING = "running"
    VERIFYING = "verifying"
    BLOCKED = "blocked"
    AWAITING_APPROVAL = "awaiting_approval"
    FAILED = "failed"
    COMPLETE = "complete"


class AgentRole(Enum):
    """Eight approved agent roles."""
    CEO = "ceo"
    ENGINEER = "engineer"
    QA = "qa"
    RESEARCH = "research"
    REASONING = "reasoning"
    BROWSER = "browser"
    AUTOMATION = "automation"
    DOCUMENTATION = "documentation"


@dataclass
class Task:
    """A unit of work assigned to an agent."""
    id: str
    title: str
    description: str
    assigned_to: AgentRole
    status: TaskStatus = TaskStatus.PLANNED
    dependencies: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    retry_count: int = 0
    max_retries: int = 3
    approval_required: bool = False
    approved: bool = False


@dataclass
class Handoff:
    """A task handoff between agents."""
    task_id: str
    from_agent: AgentRole
    to_agent: AgentRole
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""


class Orchestrator:
    """
    Agent orchestration layer.
    
    Manages task creation, routing, handoffs, approval gates,
    and evidence collection for the eight-agent team.
    """
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.handoffs: List[Handoff] = []
        self.agents = {role: {"status": "idle", "current_task": None} for role in AgentRole}
    
    def create_task(
        self,
        title: str,
        description: str,
        assigned_to: AgentRole,
        dependencies: Optional[List[str]] = None,
        approval_required: bool = False,
    ) -> Task:
        """Create a new task and assign it to an agent."""
        task_id = f"task-{len(self.tasks) + 1:04d}"
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            assigned_to=assigned_to,
            dependencies=dependencies or [],
            approval_required=approval_required,
        )
        
        self.tasks[task_id] = task
        return task
    
    def start_task(self, task_id: str) -> Task:
        """Start working on a task."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Check dependencies
        for dep_id in task.dependencies:
            dep = self.tasks.get(dep_id)
            if dep and dep.status != TaskStatus.COMPLETE:
                task.status = TaskStatus.BLOCKED
                return task
        
        task.status = TaskStatus.RUNNING
        task.updated_at = datetime.now().isoformat()
        
        # Update agent status
        agent = self.agents[task.assigned_to]
        agent["status"] = "working"
        agent["current_task"] = task_id
        
        return task
    
    def complete_task(self, task_id: str, evidence: Optional[List[str]] = None) -> Task:
        """Mark a task as complete."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.approval_required and not task.approved:
            task.status = TaskStatus.AWAITING_APPROVAL
            return task
        
        task.status = TaskStatus.COMPLETE
        task.evidence.extend(evidence or [])
        task.updated_at = datetime.now().isoformat()
        
        # Update agent status
        agent = self.agents[task.assigned_to]
        agent["status"] = "idle"
        agent["current_task"] = None
        
        return task
    
    def handoff_task(self, task_id: str, to_agent: AgentRole, notes: str = "") -> Handoff:
        """Hand off a task to another agent."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        handoff = Handoff(
            task_id=task_id,
            from_agent=task.assigned_to,
            to_agent=to_agent,
            notes=notes,
        )
        
        self.handoffs.append(handoff)
        
        # Update task assignment
        task.assigned_to = to_agent
        task.updated_at = datetime.now().isoformat()
        
        return handoff
    
    def approve_task(self, task_id: str) -> Task:
        """Approve a task that requires approval."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        task.approved = True
        if task.status == TaskStatus.AWAITING_APPROVAL:
            task.status = TaskStatus.COMPLETE
            task.updated_at = datetime.now().isoformat()
        
        return task
    
    def block_task(self, task_id: str, reason: str = "") -> Task:
        """Block a task."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        task.status = TaskStatus.BLOCKED
        task.updated_at = datetime.now().isoformat()
        
        return task
    
    def retry_task(self, task_id: str) -> Task:
        """Retry a failed task."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.retry_count >= task.max_retries:
            task.status = TaskStatus.FAILED
            return task
        
        task.retry_count += 1
        task.status = TaskStatus.READY
        task.updated_at = datetime.now().isoformat()
        
        return task
    
    def get_task_status(self) -> Dict[str, int]:
        """Get summary of task statuses."""
        status_counts = {status.value: 0 for status in TaskStatus}
        for task in self.tasks.values():
            status_counts[task.status.value] += 1
        return status_counts
    
    def get_agent_status(self) -> Dict[str, Dict]:
        """Get status of all agents."""
        return {
            role.value: {
                "status": info["status"],
                "current_task": info["current_task"],
            }
            for role, info in self.agents.items()
        }
    
    def get_queue(self) -> Dict[str, List[Dict]]:
        """Get tasks grouped by status."""
        queue = {status.value: [] for status in TaskStatus}
        for task in self.tasks.values():
            queue[task.status.value].append({
                "id": task.id,
                "title": task.title,
                "assigned_to": task.assigned_to.value,
                "status": task.status.value,
            })
        return queue
    
    def save_state(self, filepath: str):
        """Save orchestrator state to file."""
        state = {
            "tasks": {
                task_id: {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "assigned_to": task.assigned_to.value,
                    "status": task.status.value,
                    "dependencies": task.dependencies,
                    "evidence": task.evidence,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                    "retry_count": task.retry_count,
                    "approval_required": task.approval_required,
                    "approved": task.approved,
                }
                for task_id, task in self.tasks.items()
            },
            "handoffs": [
                {
                    "task_id": h.task_id,
                    "from_agent": h.from_agent.value,
                    "to_agent": h.to_agent.value,
                    "timestamp": h.timestamp,
                    "notes": h.notes,
                }
                for h in self.handoffs
            ],
        }
        
        Path(filepath).write_text(json.dumps(state, indent=2))
    
    def load_state(self, filepath: str):
        """Load orchestrator state from file."""
        if not Path(filepath).exists():
            return
        
        state = json.loads(Path(filepath).read_text())
        
        # Restore tasks
        for task_id, task_data in state.get("tasks", {}).items():
            task = Task(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                assigned_to=AgentRole(task_data["assigned_to"]),
                status=TaskStatus(task_data["status"]),
                dependencies=task_data.get("dependencies", []),
                evidence=task_data.get("evidence", []),
                created_at=task_data.get("created_at", ""),
                updated_at=task_data.get("updated_at", ""),
                retry_count=task_data.get("retry_count", 0),
                approval_required=task_data.get("approval_required", False),
                approved=task_data.get("approved", False),
            )
            self.tasks[task_id] = task
        
        # Restore handoffs
        for h_data in state.get("handoffs", []):
            handoff = Handoff(
                task_id=h_data["task_id"],
                from_agent=AgentRole(h_data["from_agent"]),
                to_agent=AgentRole(h_data["to_agent"]),
                timestamp=h_data.get("timestamp", ""),
                notes=h_data.get("notes", ""),
            )
            self.handoffs.append(handoff)
