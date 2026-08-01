# knowledge_engine/agents.py
# Phase H+I: Agent Integration — role-specific context loading for CEO, Engineer, QA

from __future__ import annotations

import time
from enum import Enum
from typing import Optional

from .access import AccessControl
from .assembler import ContextAssembler
from .cache import HotContextCache
from .config import KnowledgeEngineConfig
from .index import KnowledgeIndex
from .models import (
    AccessLevel,
    AuthorityRank,
    ContextRequest,
    ContextResponse,
    DocumentMetadata,
    DocumentType,
)
from .search import SearchEngine


class AgentRole(Enum):
    """Agent roles with different context priorities."""
    CEO = "ceo"
    ENGINEER = "engineer"
    QA = "qa"


class AgentContextProvider:
    """
    Provides role-specific context to agents.

    Each role receives different ranked context:
    - CEO: strategic overview, milestones, blockers, decisions
    - Engineer: architecture, implementation files, coding standards
    - QA: definition of done, acceptance criteria, test strategy
    """

    def __init__(
        self,
        index: KnowledgeIndex,
        search: SearchEngine,
        cache: Optional[HotContextCache] = None,
        config: Optional[KnowledgeEngineConfig] = None,
    ):
        self.index = index
        self.search = search
        self.cache = cache or HotContextCache(config)
        self.config = config or index.config
        self.assembler = ContextAssembler(index, search, self.cache, self.config)
        self.access = AccessControl(index, self.config)

    def get_ceo_context(
        self,
        project: str = "general",
        max_tokens: int = 4000,
        include_archived: bool = False,
    ) -> AgentContextResponse:
        """
        Load CEO startup context.

        Returns:
        - Project Source of Truth
        - Current milestone
        - Current project status
        - Definition of Done
        - Approved architecture decisions
        - Active blockers
        - Latest verified completion report
        - Current branch, commit, tag (when available)
        """
        # Check cache
        cache_key = f"ceo:{project}:{max_tokens}:{include_archived}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        start = time.time()
        evidence: list[str] = []

        # 1. Source of Truth (always first)
        sot = self.index.get_source_of_truth()
        sot = self.access.filter_by_access(sot, AccessLevel.PUBLIC)
        if not include_archived:
            sot = [d for d in sot if not d.is_archived]
        evidence.append(f"Source of Truth: {len(sot)} documents")

        # 2. Governing docs (SOPs, rules, goals)
        governing = self.index.get_governing()
        governing = self.access.filter_by_access(governing, AccessLevel.PUBLIC)
        if not include_archived:
            governing = [d for d in governing if not d.is_archived]
        evidence.append(f"Governing docs: {len(governing)} documents")

        # 3. Project-specific docs
        if project != "general":
            project_docs = self.index.get_by_project(project)
            project_docs = self.access.filter_by_access(project_docs, AccessLevel.PUBLIC)
            if not include_archived:
                project_docs = [d for d in project_docs if not d.is_archived]
        else:
            project_docs = []

        # 4. Search for milestones, status, blockers
        milestone_docs = self._search_filtered("milestone status progress", project, include_archived)
        architecture_docs = self._search_filtered("architecture decisions approved", project, include_archived)
        blocker_docs = self._search_filtered("blockers issues risks", project, include_archived)
        completion_docs = self._search_filtered("completion report verified", project, include_archived)

        evidence.append(f"Milestone docs: {len(milestone_docs)}")
        evidence.append(f"Architecture docs: {len(architecture_docs)}")
        evidence.append(f"Blocker docs: {len(blocker_docs)}")
        evidence.append(f"Completion docs: {len(completion_docs)}")

        # 5. Apply budget
        all_docs = sot + governing + project_docs + milestone_docs + architecture_docs + blocker_docs + completion_docs
        all_docs = self._deduplicate(all_docs)
        selected, total_tokens, truncated = self._apply_budget(all_docs, max_tokens)

        # Partition results
        selected_paths = {d.path for d in selected}
        response = AgentContextResponse(
            role=AgentRole.CEO,
            source_of_truth=[d for d in sot if d.path in selected_paths],
            governing=[d for d in governing if d.path in selected_paths],
            project_docs=[d for d in project_docs if d.path in selected_paths],
            milestone_docs=[d for d in milestone_docs if d.path in selected_paths],
            architecture_docs=[d for d in architecture_docs if d.path in selected_paths],
            blocker_docs=[d for d in blocker_docs if d.path in selected_paths],
            completion_docs=[d for d in completion_docs if d.path in selected_paths],
            total_tokens=total_tokens,
            truncated=truncated,
            retrieval_evidence=evidence,
            assembly_time_ms=time.time() - start,
        )
        self.cache.set(cache_key, response)
        return response

    def get_engineer_context(
        self,
        project: str = "general",
        max_tokens: int = 4000,
        include_archived: bool = False,
    ) -> AgentContextResponse:
        """
        Load Engineer implementation context.

        Prioritizes:
        - Source of Truth
        - Current milestone
        - Architecture
        - Relevant implementation files
        - Coding standards
        - Acceptance criteria
        - Active technical decisions
        """
        # Check cache
        cache_key = f"eng:{project}:{max_tokens}:{include_archived}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        start = time.time()
        evidence: list[str] = []

        # 1. Source of Truth
        sot = self.index.get_source_of_truth()
        sot = self.access.filter_by_access(sot, AccessLevel.PUBLIC)
        evidence.append(f"Source of Truth: {len(sot)} documents")

        # 2. Architecture docs (high priority for engineers)
        architecture_docs = self._search_filtered("architecture design system", project, include_archived)
        evidence.append(f"Architecture docs: {len(architecture_docs)}")

        # 3. Implementation-related docs
        implementation_docs = self._search_filtered("implementation code standards", project, include_archived)
        evidence.append(f"Implementation docs: {len(implementation_docs)}")

        # 4. Acceptance criteria
        criteria_docs = self._search_filtered("acceptance criteria definition done", project, include_archived)
        evidence.append(f"Criteria docs: {len(criteria_docs)}")

        # 5. Technical decisions
        decision_docs = self._search_filtered("technical decisions approved", project, include_archived)
        evidence.append(f"Decision docs: {len(decision_docs)}")

        # 6. Project-specific docs
        if project != "general":
            project_docs = self.index.get_by_project(project)
            project_docs = self.access.filter_by_access(project_docs, AccessLevel.PUBLIC)
        else:
            project_docs = []

        # Apply budget
        all_docs = sot + architecture_docs + implementation_docs + criteria_docs + decision_docs + project_docs
        all_docs = self._deduplicate(all_docs)
        selected, total_tokens, truncated = self._apply_budget(all_docs, max_tokens)

        selected_paths = {d.path for d in selected}
        response = AgentContextResponse(
            role=AgentRole.ENGINEER,
            source_of_truth=[d for d in sot if d.path in selected_paths],
            architecture_docs=[d for d in architecture_docs if d.path in selected_paths],
            implementation_docs=[d for d in implementation_docs if d.path in selected_paths],
            criteria_docs=[d for d in criteria_docs if d.path in selected_paths],
            decision_docs=[d for d in decision_docs if d.path in selected_paths],
            project_docs=[d for d in project_docs if d.path in selected_paths],
            total_tokens=total_tokens,
            truncated=truncated,
            retrieval_evidence=evidence,
            assembly_time_ms=time.time() - start,
        )
        self.cache.set(cache_key, response)
        return response

    def get_qa_context(
        self,
        project: str = "general",
        max_tokens: int = 4000,
        include_archived: bool = False,
    ) -> AgentContextResponse:
        """
        Load QA verification context.

        Prioritizes:
        - Source of Truth
        - Definition of Done
        - Acceptance criteria
        - Test strategy
        - Security requirements
        - Changed files
        - Prior defect reports
        - Verification evidence
        """
        # Check cache
        cache_key = f"qa:{project}:{max_tokens}:{include_archived}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        start = time.time()
        evidence: list[str] = []

        # 1. Source of Truth
        sot = self.index.get_source_of_truth()
        sot = self.access.filter_by_access(sot, AccessLevel.PUBLIC)
        evidence.append(f"Source of Truth: {len(sot)} documents")

        # 2. Definition of Done
        dod_docs = self._search_filtered("definition of done acceptance", project, include_archived)
        evidence.append(f"Definition of Done docs: {len(dod_docs)}")

        # 3. Test strategy
        test_docs = self._search_filtered("test strategy testing verification", project, include_archived)
        evidence.append(f"Test strategy docs: {len(test_docs)}")

        # 4. Security requirements
        security_docs = self._search_filtered("security requirements vulnerabilities", project, include_archived)
        evidence.append(f"Security docs: {len(security_docs)}")

        # 5. Defect reports
        defect_docs = self._search_filtered("defect bugs issues defects", project, include_archived)
        evidence.append(f"Defect docs: {len(defect_docs)}")

        # 6. Verification evidence
        evidence_docs = self._search_filtered("verification evidence test results", project, include_archived)
        evidence.append(f"Verification docs: {len(evidence_docs)}")

        # 7. Project-specific docs
        if project != "general":
            project_docs = self.index.get_by_project(project)
            project_docs = self.access.filter_by_access(project_docs, AccessLevel.PUBLIC)
        else:
            project_docs = []

        # Apply budget
        all_docs = sot + dod_docs + test_docs + security_docs + defect_docs + evidence_docs + project_docs
        all_docs = self._deduplicate(all_docs)
        selected, total_tokens, truncated = self._apply_budget(all_docs, max_tokens)

        selected_paths = {d.path for d in selected}
        response = AgentContextResponse(
            role=AgentRole.QA,
            source_of_truth=[d for d in sot if d.path in selected_paths],
            dod_docs=[d for d in dod_docs if d.path in selected_paths],
            test_docs=[d for d in test_docs if d.path in selected_paths],
            security_docs=[d for d in security_docs if d.path in selected_paths],
            defect_docs=[d for d in defect_docs if d.path in selected_paths],
            evidence_docs=[d for d in evidence_docs if d.path in selected_paths],
            project_docs=[d for d in project_docs if d.path in selected_paths],
            total_tokens=total_tokens,
            truncated=truncated,
            retrieval_evidence=evidence,
            assembly_time_ms=time.time() - start,
        )
        self.cache.set(cache_key, response)
        return response

    # ─── Internal Helpers ─────────────────────────────────────────────

    def _search_filtered(
        self,
        query: str,
        project: str,
        include_archived: bool,
        max_results: int = 10,
    ) -> list[DocumentMetadata]:
        """Search with access control and archive filtering."""
        results = self.search.search(
            query,
            project=project if project != "general" else None,
            max_results=max_results,
            include_archived=include_archived,
        )
        docs = [r.document for r in results]
        return self.access.filter_by_access(docs, AccessLevel.PUBLIC)

    @staticmethod
    def _deduplicate(docs: list[DocumentMetadata]) -> list[DocumentMetadata]:
        """Remove duplicate documents by path."""
        seen: set[str] = set()
        result: list[DocumentMetadata] = []
        for doc in docs:
            if doc.path not in seen:
                seen.add(doc.path)
                result.append(doc)
        return result

    def _apply_budget(
        self,
        docs: list[DocumentMetadata],
        max_tokens: int,
    ) -> tuple[list[DocumentMetadata], int, bool]:
        """Apply token budget."""
        selected: list[DocumentMetadata] = []
        total = 0
        truncated = False
        for doc in docs:
            tokens = doc.estimated_tokens if hasattr(doc, 'estimated_tokens') else len(doc.content_preview.split()) * 4
            if total + tokens <= max_tokens:
                selected.append(doc)
                total += tokens
            else:
                truncated = True
                break
        return selected, total, truncated


from dataclasses import dataclass, field


@dataclass
class AgentContextResponse:
    """Response from agent context loading."""
    role: AgentRole
    source_of_truth: list[DocumentMetadata] = field(default_factory=list)
    governing: list[DocumentMetadata] = field(default_factory=list)
    project_docs: list[DocumentMetadata] = field(default_factory=list)
    milestone_docs: list[DocumentMetadata] = field(default_factory=list)
    architecture_docs: list[DocumentMetadata] = field(default_factory=list)
    blocker_docs: list[DocumentMetadata] = field(default_factory=list)
    completion_docs: list[DocumentMetadata] = field(default_factory=list)
    implementation_docs: list[DocumentMetadata] = field(default_factory=list)
    criteria_docs: list[DocumentMetadata] = field(default_factory=list)
    decision_docs: list[DocumentMetadata] = field(default_factory=list)
    dod_docs: list[DocumentMetadata] = field(default_factory=list)
    test_docs: list[DocumentMetadata] = field(default_factory=list)
    security_docs: list[DocumentMetadata] = field(default_factory=list)
    defect_docs: list[DocumentMetadata] = field(default_factory=list)
    evidence_docs: list[DocumentMetadata] = field(default_factory=list)
    total_tokens: int = 0
    truncated: bool = False
    retrieval_evidence: list[str] = field(default_factory=list)
    assembly_time_ms: float = 0.0

    @property
    def all_documents(self) -> list[DocumentMetadata]:
        """Get all documents across all categories, deduplicated."""
        seen: set[str] = set()
        result: list[DocumentMetadata] = []
        for attr in [
            self.source_of_truth, self.governing, self.project_docs,
            self.milestone_docs, self.architecture_docs, self.blocker_docs,
            self.completion_docs, self.implementation_docs, self.criteria_docs,
            self.decision_docs, self.dod_docs, self.test_docs,
            self.security_docs, self.defect_docs, self.evidence_docs,
        ]:
            for doc in attr:
                if doc.path not in seen:
                    seen.add(doc.path)
                    result.append(doc)
        return result

    @property
    def document_count(self) -> int:
        return len(self.all_documents)

    @property
    def category_summary(self) -> dict[str, int]:
        """Summary of documents per category."""
        return {
            "source_of_truth": len(self.source_of_truth),
            "governing": len(self.governing),
            "project_docs": len(self.project_docs),
            "milestone_docs": len(self.milestone_docs),
            "architecture_docs": len(self.architecture_docs),
            "blocker_docs": len(self.blocker_docs),
            "completion_docs": len(self.completion_docs),
            "implementation_docs": len(self.implementation_docs),
            "criteria_docs": len(self.criteria_docs),
            "decision_docs": len(self.decision_docs),
            "dod_docs": len(self.dod_docs),
            "test_docs": len(self.test_docs),
            "security_docs": len(self.security_docs),
            "defect_docs": len(self.defect_docs),
            "evidence_docs": len(self.evidence_docs),
        }
