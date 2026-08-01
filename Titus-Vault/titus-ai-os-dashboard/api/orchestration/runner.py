"""
Titus AI OS Milestone Runner
Autonomous multi-sprint milestone execution with safeguards.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
import json
from pathlib import Path

from . import Orchestrator, Task, TaskStatus, AgentRole


class MilestoneStatus(Enum):
    """Milestone execution status."""
    PLANNED = "planned"
    READY = "ready"
    RUNNING = "running"
    VERIFYING = "verifying"
    BLOCKED = "blocked"
    AWAITING_APPROVAL = "awaiting_approval"
    FAILED = "failed"
    COMPLETE_WITH_GAPS = "complete_with_gaps"
    VERIFIED_COMPLETE = "verified_complete"


@dataclass
class Sprint:
    """A sprint within a milestone."""
    id: str
    name: str
    tasks: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PLANNED
    evidence: List[str] = field(default_factory=list)


@dataclass
class Milestone:
    """A milestone containing sprints."""
    id: str
    name: str
    objective: str
    sprints: List[Sprint] = field(default_factory=list)
    status: MilestoneStatus = MilestoneStatus.PLANNED
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    blockers: List[str] = field(default_factory=list)
    deferred: List[str] = field(default_factory=list)


class MilestoneRunner:
    """
    Autonomous milestone execution engine.
    
    Runs sprints sequentially, collecting evidence and stopping
    only at approval gates or blockers.
    """
    
    # Safeguards
    MAX_RETRIES = 3
    MAX_SPRINTS = 20
    TIMEOUT_HOURS = 24
    
    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.milestones: Dict[str, Milestone] = {}
        self.current_milestone: Optional[str] = None
        self.start_time: Optional[datetime] = None
    
    def create_milestone(
        self,
        name: str,
        objective: str,
        sprints: Optional[List[Dict]] = None,
    ) -> Milestone:
        """Create a new milestone with sprints."""
        milestone_id = f"milestone-{len(self.milestones) + 1:04d}"
        
        sprint_list = []
        for i, sprint_data in enumerate(sprints or []):
            sprint = Sprint(
                id=f"{milestone_id}-sprint-{i+1:02d}",
                name=sprint_data.get("name", f"Sprint {i+1}"),
                tasks=[],
            )
            sprint_list.append(sprint)
        
        milestone = Milestone(
            id=milestone_id,
            name=name,
            objective=objective,
            sprints=sprint_list,
        )
        
        self.milestones[milestone_id] = milestone
        return milestone
    
    def add_task_to_sprint(self, milestone_id: str, sprint_index: int, task: Task):
        """Add a task to a sprint."""
        milestone = self.milestones.get(milestone_id)
        if not milestone:
            raise ValueError(f"Milestone {milestone_id} not found")
        
        if sprint_index >= len(milestone.sprints):
            raise ValueError(f"Sprint index {sprint_index} out of range")
        
        milestone.sprints[sprint_index].tasks.append(task.id)
        self.orchestrator.tasks[task.id] = task
    
    def start_milestone(self, milestone_id: str) -> Milestone:
        """Start executing a milestone."""
        milestone = self.milestones.get(milestone_id)
        if not milestone:
            raise ValueError(f"Milestone {milestone_id} not found")
        
        # Validate prerequisites
        if milestone.status not in (MilestoneStatus.PLANNED, MilestoneStatus.READY):
            raise ValueError(f"Milestone cannot be started from status {milestone.status}")
        
        milestone.status = MilestoneStatus.RUNNING
        milestone.updated_at = datetime.now().isoformat()
        self.current_milestone = milestone_id
        self.start_time = datetime.now()
        
        return milestone
    
    def run_sprint(self, milestone_id: str, sprint_index: int) -> Sprint:
        """Execute a single sprint."""
        milestone = self.milestones.get(milestone_id)
        if not milestone:
            raise ValueError(f"Milestone {milestone_id} not found")
        
        if sprint_index >= len(milestone.sprints):
            raise ValueError(f"Sprint index {sprint_index} out of range")
        
        sprint = milestone.sprints[sprint_index]
        sprint.status = TaskStatus.RUNNING
        
        # Execute each task in the sprint
        for task_id in sprint.tasks:
            task = self.orchestrator.tasks.get(task_id)
            if not task:
                continue
            
            # Check if task is blocked
            if task.status == TaskStatus.BLOCKED:
                sprint.status = TaskStatus.BLOCKED
                milestone.blockers.append(f"Task {task_id} blocked")
                return sprint
            
            # Check if task requires approval
            if task.approval_required and not task.approved:
                task.status = TaskStatus.AWAITING_APPROVAL
                sprint.status = TaskStatus.AWAITING_APPROVAL
                milestone.status = MilestoneStatus.AWAITING_APPROVAL
                return sprint
            
            # Start and complete task
            self.orchestrator.start_task(task_id)
            
            # Simulate task execution (in real implementation, this would call the agent)
            task.status = TaskStatus.VERIFYING
        
        # All tasks verified
        sprint.status = TaskStatus.COMPLETE
        sprint.evidence.append(f"Sprint {sprint_index + 1} completed")
        
        return sprint
    
    def verify_sprint(self, milestone_id: str, sprint_index: int) -> bool:
        """Verify a sprint's completion."""
        milestone = self.milestones.get(milestone_id)
        if not milestone:
            return False
        
        sprint = milestone.sprints[sprint_index]
        
        # Check all tasks are complete
        for task_id in sprint.tasks:
            task = self.orchestrator.tasks.get(task_id)
            if task and task.status != TaskStatus.COMPLETE:
                return False
        
        sprint.evidence.append(f"Sprint {sprint_index + 1} verified")
        return True
    
    def complete_milestone(self, milestone_id: str, verified: bool = False) -> Milestone:
        """Complete a milestone."""
        milestone = self.milestones.get(milestone_id)
        if not milestone:
            raise ValueError(f"Milestone {milestone_id} not found")
        
        if verified:
            milestone.status = MilestoneStatus.VERIFIED_COMPLETE
        else:
            # Check if there are gaps
            incomplete_tasks = []
            for sprint in milestone.sprints:
                for task_id in sprint.tasks:
                    task = self.orchestrator.tasks.get(task_id)
                    if task and task.status != TaskStatus.COMPLETE:
                        incomplete_tasks.append(task_id)
            
            if incomplete_tasks:
                milestone.status = MilestoneStatus.COMPLETE_WITH_GAPS
                milestone.deferred.extend(incomplete_tasks)
            else:
                milestone.status = MilestoneStatus.VERIFIED_COMPLETE
        
        milestone.updated_at = datetime.now().isoformat()
        
        # Generate final report
        report = self.generate_report(milestone_id)
        
        return milestone
    
    def generate_report(self, milestone_id: str) -> Dict:
        """Generate a milestone completion report."""
        milestone = self.milestones.get(milestone_id)
        if not milestone:
            return {"error": "Milestone not found"}
        
        total_tasks = sum(len(sprint.tasks) for sprint in milestone.sprints)
        completed_tasks = 0
        for sprint in milestone.sprints:
            for task_id in sprint.tasks:
                task = self.orchestrator.tasks.get(task_id)
                if task and task.status == TaskStatus.COMPLETE:
                    completed_tasks += 1
        
        return {
            "milestone_id": milestone.id,
            "name": milestone.name,
            "objective": milestone.objective,
            "status": milestone.status.value,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "sprints": len(milestone.sprints),
            "blockers": milestone.blockers,
            "deferred": milestone.deferred,
            "created_at": milestone.created_at,
            "updated_at": milestone.updated_at,
        }
    
    def check_safeguards(self) -> List[str]:
        """Check all safeguards and return any violations."""
        violations = []
        
        # Check retry limit
        for task in self.orchestrator.tasks.values():
            if task.retry_count >= self.MAX_RETRIES:
                violations.append(f"Task {task.id} exceeded max retries")
        
        # Check timeout
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds() / 3600
            if elapsed > self.TIMEOUT_HOURS:
                violations.append(f"Milestone exceeded timeout of {self.TIMEOUT_HOURS} hours")
        
        # Check sprint limit
        if self.current_milestone:
            milestone = self.milestones.get(self.current_milestone)
            if milestone and len(milestone.sprints) > self.MAX_SPRINTS:
                violations.append(f"Milestone exceeded max sprints of {self.MAX_SPRINTS}")
        
        return violations
    
    def save_state(self, filepath: str):
        """Save runner state to file."""
        state = {
            "milestones": {
                mid: {
                    "id": m.id,
                    "name": m.name,
                    "objective": m.objective,
                    "status": m.status.value,
                    "created_at": m.created_at,
                    "updated_at": m.updated_at,
                    "blockers": m.blockers,
                    "deferred": m.deferred,
                    "sprints": [
                        {
                            "id": s.id,
                            "name": s.name,
                            "tasks": s.tasks,
                            "status": s.status.value,
                            "evidence": s.evidence,
                        }
                        for s in m.sprints
                    ],
                }
                for mid, m in self.milestones.items()
            },
            "current_milestone": self.current_milestone,
            "start_time": self.start_time.isoformat() if self.start_time else None,
        }
        
        Path(filepath).write_text(json.dumps(state, indent=2))
    
    def load_state(self, filepath: str):
        """Load runner state from file."""
        if not Path(filepath).exists():
            return
        
        state = json.loads(Path(filepath).read_text())
        
        for mid, m_data in state.get("milestones", {}).items():
            sprints = [
                Sprint(
                    id=s["id"],
                    name=s["name"],
                    tasks=s["tasks"],
                    status=TaskStatus(s["status"]),
                    evidence=s.get("evidence", []),
                )
                for s in m_data.get("sprints", [])
            ]
            
            milestone = Milestone(
                id=m_data["id"],
                name=m_data["name"],
                objective=m_data["objective"],
                sprints=sprints,
                status=MilestoneStatus(m_data["status"]),
                created_at=m_data.get("created_at", ""),
                updated_at=m_data.get("updated_at", ""),
                blockers=m_data.get("blockers", []),
                deferred=m_data.get("deferred", []),
            )
            self.milestones[mid] = milestone
        
        self.current_milestone = state.get("current_milestone")
        start_time = state.get("start_time")
        if start_time:
            self.start_time = datetime.fromisoformat(start_time)
