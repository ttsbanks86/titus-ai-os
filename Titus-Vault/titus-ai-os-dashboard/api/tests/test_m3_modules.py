"""
Titus AI OS Test Suite
Comprehensive tests for M3 modules.
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Import modules to test
from orchestration import Orchestrator, Task, TaskStatus, AgentRole, Handoff
from orchestration.runner import MilestoneRunner, Milestone, Sprint, MilestoneStatus
from search import SemanticSearch, SearchResult
from indexing import AutoIndexer, IndexEntry
from guardrails import AutomationGuardrails, Operation, OperationType, SafetyLevel


class TestOrchestrator:
    """Tests for the Orchestrator module."""
    
    def setup_method(self):
        self.orchestrator = Orchestrator()
    
    def test_create_task(self):
        """Test creating a task."""
        task = self.orchestrator.create_task(
            title="Test Task",
            description="A test task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        assert task.id.startswith("task-")
        assert task.title == "Test Task"
        assert task.status == TaskStatus.PLANNED
        assert task.assigned_to == AgentRole.ENGINEER
    
    def test_start_task(self):
        """Test starting a task."""
        task = self.orchestrator.create_task(
            title="Test Task",
            description="A test task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        started = self.orchestrator.start_task(task.id)
        assert started.status == TaskStatus.RUNNING
    
    def test_complete_task(self):
        """Test completing a task."""
        task = self.orchestrator.create_task(
            title="Test Task",
            description="A test task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        self.orchestrator.start_task(task.id)
        completed = self.orchestrator.complete_task(task.id, evidence=["test passed"])
        
        assert completed.status == TaskStatus.COMPLETE
        assert "test passed" in completed.evidence
    
    def test_handoff_task(self):
        """Test handing off a task."""
        task = self.orchestrator.create_task(
            title="Test Task",
            description="A test task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        handoff = self.orchestrator.handoff_task(
            task.id,
            to_agent=AgentRole.QA,
            notes="Ready for review",
        )
        
        assert handoff.from_agent == AgentRole.ENGINEER
        assert handoff.to_agent == AgentRole.QA
        assert task.assigned_to == AgentRole.QA
    
    def test_approval_gate(self):
        """Test approval gate functionality."""
        task = self.orchestrator.create_task(
            title="Deploy Task",
            description="Deploy to production",
            assigned_to=AgentRole.ENGINEER,
            approval_required=True,
        )
        
        self.orchestrator.start_task(task.id)
        completed = self.orchestrator.complete_task(task.id)
        
        # Should be awaiting approval
        assert completed.status == TaskStatus.AWAITING_APPROVAL
        
        # Approve
        approved = self.orchestrator.approve_task(task.id)
        assert approved.status == TaskStatus.COMPLETE
    
    def test_dependency_blocking(self):
        """Test task dependency blocking."""
        task1 = self.orchestrator.create_task(
            title="Task 1",
            description="First task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        task2 = self.orchestrator.create_task(
            title="Task 2",
            description="Second task",
            assigned_to=AgentRole.ENGINEER,
            dependencies=[task1.id],
        )
        
        # Task 2 should be blocked
        started = self.orchestrator.start_task(task2.id)
        assert started.status == TaskStatus.BLOCKED
    
    def test_task_status_summary(self):
        """Test task status summary."""
        self.orchestrator.create_task(
            title="Task 1",
            description="First task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        self.orchestrator.create_task(
            title="Task 2",
            description="Second task",
            assigned_to=AgentRole.QA,
        )
        
        status = self.orchestrator.get_task_status()
        assert status["planned"] == 2
        assert status["running"] == 0
    
    def test_agent_status(self):
        """Test agent status tracking."""
        task = self.orchestrator.create_task(
            title="Test Task",
            description="A test task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        self.orchestrator.start_task(task.id)
        
        agents = self.orchestrator.get_agent_status()
        assert agents["engineer"]["status"] == "working"
        assert agents["engineer"]["current_task"] == task.id


class TestMilestoneRunner:
    """Tests for the Milestone Runner module."""
    
    def setup_method(self):
        self.orchestrator = Orchestrator()
        self.runner = MilestoneRunner(self.orchestrator)
    
    def test_create_milestone(self):
        """Test creating a milestone."""
        milestone = self.runner.create_milestone(
            name="M3 Test",
            objective="Test milestone creation",
            sprints=[{"name": "Sprint 1"}],
        )
        
        assert milestone.id.startswith("milestone-")
        assert milestone.name == "M3 Test"
        assert len(milestone.sprints) == 1
    
    def test_start_milestone(self):
        """Test starting a milestone."""
        milestone = self.runner.create_milestone(
            name="M3 Test",
            objective="Test milestone",
        )
        
        started = self.runner.start_milestone(milestone.id)
        assert started.status == MilestoneStatus.RUNNING
    
    def test_safeguard_timeout(self):
        """Test timeout safeguard."""
        from datetime import timedelta
        
        self.runner.start_time = datetime.now() - timedelta(hours=25)
        violations = self.runner.check_safeguards()
        
        assert any("timeout" in v.lower() for v in violations)


class TestSemanticSearch:
    """Tests for the Semantic Search module."""
    
    def setup_method(self, tmp_path=None):
        # Create a temporary vault for testing
        self.tmp_dir = Path(tempfile.mkdtemp())
        (self.tmp_dir / "test-note.md").write_text("# Test Note\n\nThis is a test note with #tag1 #tag2")
        (self.tmp_dir / "project.md").write_text("# Project\n\nProject details here")
        
        self.search = SemanticSearch(str(self.tmp_dir))
    
    def test_search(self):
        """Test basic search."""
        results = self.search.search("test note")
        assert len(results) > 0
        assert results[0].title == "Test Note"
    
    def test_search_by_tag(self):
        """Test tag search."""
        results = self.search.search_by_tag("tag1")
        assert len(results) > 0
    
    def test_search_stats(self):
        """Test search statistics."""
        stats = self.search.get_stats()
        assert stats["total_documents"] == 2


class TestAutoIndexer:
    """Tests for the Auto-Indexer module."""
    
    def setup_method(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        (self.tmp_dir / "note.md").write_text("# Test Note\n\nContent here [[Other Note]]")
        (self.tmp_dir / "other.md").write_text("# Other Note\n\nReferenced content")
        
        self.indexer = AutoIndexer(str(self.tmp_dir))
    
    def test_index_all(self):
        """Test indexing all files."""
        stats = self.indexer.index_all()
        assert stats["indexed"] >= 2
    
    def test_compute_hash(self):
        """Test content hashing."""
        hash1 = self.indexer.compute_hash("hello world")
        hash2 = self.indexer.compute_hash("hello world")
        hash3 = self.indexer.compute_hash("different content")
        
        assert hash1 == hash2
        assert hash1 != hash3
    
    def test_extract_metadata(self):
        """Test metadata extraction."""
        content = "# Test Title\n\nSome content with #tag1 and [[Wiki Link]]"
        metadata = self.indexer.extract_metadata(content)
        
        assert metadata["title"] == "Test Title"
        assert "tag1" in metadata["tags"]
        assert "Wiki Link" in metadata["links"]


class TestAutomationGuardrails:
    """Tests for the Automation Guardrails module."""
    
    def setup_method(self):
        self.guardrails = AutomationGuardrails()
    
    def test_classify_safe_operation(self):
        """Test classifying safe operations."""
        level = self.guardrails.classify_operation(
            OperationType.READ,
            "/some/path",
            "list files in directory",
        )
        assert level == SafetyLevel.SAFE
    
    def test_classify_dangerous_operation(self):
        """Test classifying dangerous operations."""
        level = self.guardrails.classify_operation(
            OperationType.DELETE,
            "/some/path",
            "delete important files",
        )
        assert level == SafetyLevel.DANGEROUS
    
    def test_classify_forbidden_operation(self):
        """Test classifying forbidden operations."""
        level = self.guardrails.classify_operation(
            OperationType.EXECUTE,
            "/",
            "rm -rf /",
        )
        assert level == SafetyLevel.FORBIDDEN
    
    def test_approval_workflow(self):
        """Test approval workflow."""
        operation = self.guardrails.create_operation(
            OperationType.DELETE,
            "/data",
            "delete old logs",
        )
        
        # Should require approval
        assert operation.requires_approval
        assert not self.guardrails.can_execute(operation.id)
        
        # Approve
        self.guardrails.request_approval(operation.id, "admin", "Approved for cleanup")
        
        # Now can execute
        assert self.guardrails.can_execute(operation.id)
    
    def test_restricted_paths(self):
        """Test restricted paths."""
        self.guardrails.add_restricted_path("/etc")
        
        operation = self.guardrails.create_operation(
            OperationType.WRITE,
            "/etc/passwd",
            "modify system file",
        )
        
        assert not self.guardrails.can_execute(operation.id)
    
    def test_pending_approvals(self):
        """Test pending approvals list."""
        self.guardrails.create_operation(
            OperationType.DELETE,
            "/data",
            "delete old logs",
        )
        
        pending = self.guardrails.get_pending_approvals()
        assert len(pending) == 1


class TestIntegration:
    """Integration tests for combined modules."""
    
    def test_orchestrator_with_runner(self):
        """Test orchestrator working with milestone runner."""
        orchestrator = Orchestrator()
        runner = MilestoneRunner(orchestrator)
        
        # Create milestone
        milestone = runner.create_milestone(
            name="Integration Test",
            objective="Test integration",
            sprints=[{"name": "Sprint 1"}],
        )
        
        # Create and add tasks
        task = orchestrator.create_task(
            title="Test Task",
            description="A test task",
            assigned_to=AgentRole.ENGINEER,
        )
        
        runner.add_task_to_sprint(milestone.id, 0, task)
        
        # Start milestone
        runner.start_milestone(milestone.id)
        
        # Verify
        assert milestone.status == MilestoneStatus.RUNNING
        assert task.id in milestone.sprints[0].tasks
