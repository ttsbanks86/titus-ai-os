"""
Titus AI OS Automation Boundaries
Safety controls for automated operations.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import json
from pathlib import Path


class OperationType(Enum):
    """Types of operations."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    NETWORK = "network"
    APPROVE = "approve"


class SafetyLevel(Enum):
    """Safety levels for operations."""
    SAFE = "safe"
    CAUTION = "caution"
    DANGEROUS = "dangerous"
    FORBIDDEN = "forbidden"


@dataclass
class Operation:
    """An operation to be executed."""
    id: str
    type: OperationType
    target: str
    description: str
    safety_level: SafetyLevel = SafetyLevel.SAFE
    requires_approval: bool = False
    requires_confirmation: bool = False
    reversible: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ApprovalRecord:
    """Record of an approval."""
    operation_id: str
    approved_by: str
    approved_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""


class AutomationGuardrails:
    """
    Safety controls for automated operations.
    
    Enforces approval gates, confirmation requirements,
    and operation restrictions.
    """
    
    # Forbidden operations (never auto-execute)
    FORBIDDEN_PATTERNS = [
        "rm -rf",
        "del /s",
        "format",
        "drop table",
        "drop database",
        "delete from",
        "truncate",
        "sudo",
        "chmod 777",
        "rm -r /",
    ]
    
    # Dangerous operations (require approval)
    DANGEROUS_PATTERNS = [
        "delete",
        "remove",
        "uninstall",
        "disable",
        "revoke",
        "revoke access",
        "change password",
        "reset",
    ]
    
    # Auto-approve patterns (safe operations)
    SAFE_PATTERNS = [
        "list",
        "get",
        "read",
        "search",
        "index",
        "query",
        "status",
        "health",
    ]
    
    def __init__(self):
        self.operations: Dict[str, Operation] = {}
        self.approvals: Dict[str, ApprovalRecord] = {}
        self.restricted_paths: List[str] = []
        self.restricted_commands: List[str] = []
    
    def classify_operation(self, operation_type: OperationType, target: str, description: str) -> SafetyLevel:
        """Classify the safety level of an operation."""
        desc_lower = description.lower()
        target_lower = target.lower()
        
        # Check forbidden patterns
        for pattern in self.FORBIDDEN_PATTERNS:
            if pattern in desc_lower or pattern in target_lower:
                return SafetyLevel.FORBIDDEN
        
        # Check dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern in desc_lower or pattern in target_lower:
                return SafetyLevel.DANGEROUS
        
        # Check safe patterns
        for pattern in self.SAFE_PATTERNS:
            if pattern in desc_lower:
                return SafetyLevel.SAFE
        
        # Default classification based on operation type
        if operation_type == OperationType.READ:
            return SafetyLevel.SAFE
        elif operation_type == OperationType.WRITE:
            return SafetyLevel.CAUTION
        elif operation_type == OperationType.DELETE:
            return SafetyLevel.DANGEROUS
        elif operation_type == OperationType.EXECUTE:
            return SafetyLevel.CAUTION
        elif operation_type == OperationType.NETWORK:
            return SafetyLevel.CAUTION
        elif operation_type == OperationType.APPROVE:
            return SafetyLevel.DANGEROUS
        
        return SafetyLevel.CAUTION
    
    def create_operation(
        self,
        operation_type: OperationType,
        target: str,
        description: str,
    ) -> Operation:
        """Create a new operation with safety classification."""
        op_id = f"op-{len(self.operations) + 1:04d}"
        
        safety_level = self.classify_operation(operation_type, target, description)
        
        operation = Operation(
            id=op_id,
            type=operation_type,
            target=target,
            description=description,
            safety_level=safety_level,
            requires_approval=safety_level in (SafetyLevel.DANGEROUS, SafetyLevel.FORBIDDEN),
            requires_confirmation=safety_level == SafetyLevel.CAUTION,
        )
        
        self.operations[op_id] = operation
        return operation
    
    def request_approval(self, operation_id: str, approver: str, notes: str = "") -> bool:
        """Request and record approval for an operation."""
        operation = self.operations.get(operation_id)
        if not operation:
            return False
        
        if operation.safety_level == SafetyLevel.FORBIDDEN:
            return False
        
        approval = ApprovalRecord(
            operation_id=operation_id,
            approved_by=approver,
            notes=notes,
        )
        
        self.approvals[operation_id] = approval
        return True
    
    def check_approval(self, operation_id: str) -> bool:
        """Check if an operation has been approved."""
        return operation_id in self.approvals
    
    def can_execute(self, operation_id: str) -> bool:
        """Check if an operation can be executed."""
        operation = self.operations.get(operation_id)
        if not operation:
            return False
        
        # Forbidden operations can never be executed
        if operation.safety_level == SafetyLevel.FORBIDDEN:
            return False
        
        # Dangerous operations require approval
        if operation.requires_approval and not self.check_approval(operation_id):
            return False
        
        # Check restricted paths
        for restricted in self.restricted_paths:
            if restricted in operation.target:
                return False
        
        # Check restricted commands
        for restricted in self.restricted_commands:
            if restricted in operation.description:
                return False
        
        return True
    
    def add_restricted_path(self, path: str):
        """Add a path to the restricted list."""
        if path not in self.restricted_paths:
            self.restricted_paths.append(path)
    
    def add_restricted_command(self, command: str):
        """Add a command to the restricted list."""
        if command not in self.restricted_commands:
            self.restricted_commands.append(command)
    
    def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """Get operations awaiting approval."""
        pending = []
        
        for op_id, operation in self.operations.items():
            if operation.requires_approval and not self.check_approval(op_id):
                pending.append({
                    "id": operation.id,
                    "type": operation.type.value,
                    "target": operation.target,
                    "description": operation.description,
                    "safety_level": operation.safety_level.value,
                    "created_at": operation.created_at,
                })
        
        return pending
    
    def get_operation_log(self) -> List[Dict[str, Any]]:
        """Get log of all operations."""
        log = []
        
        for op_id, operation in self.operations.items():
            entry = {
                "id": operation.id,
                "type": operation.type.value,
                "target": operation.target,
                "description": operation.description,
                "safety_level": operation.safety_level.value,
                "requires_approval": operation.requires_approval,
                "approved": self.check_approval(op_id),
                "created_at": operation.created_at,
            }
            
            if op_id in self.approvals:
                approval = self.approvals[op_id]
                entry["approved_by"] = approval.approved_by
                entry["approved_at"] = approval.approved_at
            
            log.append(entry)
        
        return log
    
    def save_state(self, filepath: str):
        """Save guardrails state to file."""
        state = {
            "operations": {
                op_id: {
                    "id": op.id,
                    "type": op.type.value,
                    "target": op.target,
                    "description": op.description,
                    "safety_level": op.safety_level.value,
                    "requires_approval": op.requires_approval,
                    "requires_confirmation": op.requires_confirmation,
                    "reversible": op.reversible,
                    "created_at": op.created_at,
                }
                for op_id, op in self.operations.items()
            },
            "approvals": {
                op_id: {
                    "operation_id": ap.operation_id,
                    "approved_by": ap.approved_by,
                    "approved_at": ap.approved_at,
                    "notes": ap.notes,
                }
                for op_id, ap in self.approvals.items()
            },
            "restricted_paths": self.restricted_paths,
            "restricted_commands": self.restricted_commands,
        }
        
        Path(filepath).write_text(json.dumps(state, indent=2))
    
    def load_state(self, filepath: str):
        """Load guardrails state from file."""
        if not Path(filepath).exists():
            return
        
        state = json.loads(Path(filepath).read_text())
        
        for op_id, op_data in state.get("operations", {}).items():
            operation = Operation(
                id=op_data["id"],
                type=OperationType(op_data["type"]),
                target=op_data["target"],
                description=op_data["description"],
                safety_level=SafetyLevel(op_data["safety_level"]),
                requires_approval=op_data.get("requires_approval", False),
                requires_confirmation=op_data.get("requires_confirmation", False),
                reversible=op_data.get("reversible", True),
                created_at=op_data.get("created_at", ""),
            )
            self.operations[op_id] = operation
        
        for op_id, ap_data in state.get("approvals", {}).items():
            approval = ApprovalRecord(
                operation_id=ap_data["operation_id"],
                approved_by=ap_data["approved_by"],
                approved_at=ap_data.get("approved_at", ""),
                notes=ap_data.get("notes", ""),
            )
            self.approvals[op_id] = approval
        
        self.restricted_paths = state.get("restricted_paths", [])
        self.restricted_commands = state.get("restricted_commands", [])
