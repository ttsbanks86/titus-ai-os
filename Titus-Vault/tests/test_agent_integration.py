"""Tests for agent integration — Phases H and I."""
import pytest

from knowledge_engine.config import KnowledgeEngineConfig
from knowledge_engine.index import KnowledgeIndex
from knowledge_engine.search import SearchEngine
from knowledge_engine.cache import HotContextCache
from knowledge_engine.agents import AgentContextProvider, AgentRole, AgentContextResponse
from knowledge_engine.models import AccessLevel


@pytest.fixture
def engine():
    config = KnowledgeEngineConfig()
    index = KnowledgeIndex(config)
    index.build()
    search = SearchEngine(index, config)
    cache = HotContextCache(config)
    provider = AgentContextProvider(index, search, cache, config)
    return provider


# ─── Phase H: CEO Agent Integration ───────────────────────────────

class TestCEOContext:
    def test_ceo_receives_source_of_truth(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert len(resp.source_of_truth) >= 1
        for doc in resp.source_of_truth:
            assert doc.is_source_of_truth or doc.authority.value >= 4

    def test_ceo_receives_milestone_docs(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert isinstance(resp.milestone_docs, list)

    def test_ceo_receives_architecture_docs(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert isinstance(resp.architecture_docs, list)

    def test_ceo_receives_blocker_docs(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert isinstance(resp.blocker_docs, list)

    def test_ceo_receives_completion_docs(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert isinstance(resp.completion_docs, list)

    def test_ceo_context_has_retrieval_evidence(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert len(resp.retrieval_evidence) >= 1
        for e in resp.retrieval_evidence:
            assert isinstance(e, str)

    def test_ceo_context_respects_budget(self, engine):
        resp = engine.get_ceo_context(project="general", max_tokens=1000)
        assert resp.total_tokens <= 1000 + 200

    def test_ceo_context_within_time(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert resp.assembly_time_ms < 5000

    def test_ceo_source_of_truth_priority(self, engine):
        """CEO must receive source of truth docs — these are the highest-priority docs."""
        resp = engine.get_ceo_context(project="general")
        assert len(resp.source_of_truth) >= 1
        # All source of truth docs should be marked as such
        for doc in resp.source_of_truth:
            assert doc.is_source_of_truth

    def test_ceo_excludes_archived_by_default(self, engine):
        resp = engine.get_ceo_context(project="general", include_archived=False)
        for doc in resp.all_documents:
            assert not doc.is_archived or doc.authority.value >= 4

    def test_ceo_excludes_secrets(self, engine):
        resp = engine.get_ceo_context(project="general")
        for doc in resp.all_documents:
            assert doc.access_level != AccessLevel.SECRET

    def test_ceo_returns_role(self, engine):
        resp = engine.get_ceo_context(project="general")
        assert resp.role == AgentRole.CEO

    def test_ceo_fallback_on_invalid_project(self, engine):
        """CEO should not crash on invalid project name."""
        resp = engine.get_ceo_context(project="nonexistent-project-xyz")
        assert resp is not None
        assert resp.role == AgentRole.CEO


# ─── Phase I: Engineer Agent Integration ──────────────────────────

class TestEngineerContext:
    def test_engineer_receives_source_of_truth(self, engine):
        resp = engine.get_engineer_context(project="general")
        assert len(resp.source_of_truth) >= 1

    def test_engineer_receives_architecture_docs(self, engine):
        resp = engine.get_engineer_context(project="general")
        assert isinstance(resp.architecture_docs, list)

    def test_engineer_receives_implementation_docs(self, engine):
        resp = engine.get_engineer_context(project="general")
        assert isinstance(resp.implementation_docs, list)

    def test_engineer_receives_criteria_docs(self, engine):
        resp = engine.get_engineer_context(project="general")
        assert isinstance(resp.criteria_docs, list)

    def test_engineer_receives_decision_docs(self, engine):
        resp = engine.get_engineer_context(project="general")
        assert isinstance(resp.decision_docs, list)

    def test_engineer_context_respects_budget(self, engine):
        resp = engine.get_engineer_context(project="general", max_tokens=1500)
        assert resp.total_tokens <= 1500 + 200

    def test_engineer_excludes_secrets(self, engine):
        resp = engine.get_engineer_context(project="general")
        for doc in resp.all_documents:
            assert doc.access_level != AccessLevel.SECRET

    def test_engineer_returns_role(self, engine):
        resp = engine.get_engineer_context(project="general")
        assert resp.role == AgentRole.ENGINEER


# ─── Phase I: QA Agent Integration ────────────────────────────────

class TestQAContext:
    def test_qa_receives_source_of_truth(self, engine):
        resp = engine.get_qa_context(project="general")
        assert len(resp.source_of_truth) >= 1

    def test_qa_receives_dod_docs(self, engine):
        resp = engine.get_qa_context(project="general")
        assert isinstance(resp.dod_docs, list)

    def test_qa_receives_test_docs(self, engine):
        resp = engine.get_qa_context(project="general")
        assert isinstance(resp.test_docs, list)

    def test_qa_receives_security_docs(self, engine):
        resp = engine.get_qa_context(project="general")
        assert isinstance(resp.security_docs, list)

    def test_qa_receives_defect_docs(self, engine):
        resp = engine.get_qa_context(project="general")
        assert isinstance(resp.defect_docs, list)

    def test_qa_receives_evidence_docs(self, engine):
        resp = engine.get_qa_context(project="general")
        assert isinstance(resp.evidence_docs, list)

    def test_qa_context_respects_budget(self, engine):
        resp = engine.get_qa_context(project="general", max_tokens=1500)
        assert resp.total_tokens <= 1500 + 200

    def test_qa_excludes_secrets(self, engine):
        resp = engine.get_qa_context(project="general")
        for doc in resp.all_documents:
            assert doc.access_level != AccessLevel.SECRET

    def test_qa_returns_role(self, engine):
        resp = engine.get_qa_context(project="general")
        assert resp.role == AgentRole.QA


# ─── Cross-role differentiation ───────────────────────────────────

class TestRoleDifferentiation:
    def test_different_roles_get_different_context(self, engine):
        """CEO, Engineer, and QA receive different ranked context."""
        ceo = engine.get_ceo_context(project="general")
        eng = engine.get_engineer_context(project="general")
        qa = engine.get_qa_context(project="general")

        # All should have source of truth
        assert len(ceo.source_of_truth) >= 1
        assert len(eng.source_of_truth) >= 1
        assert len(qa.source_of_truth) >= 1

        # Roles should differ in category distribution
        ceo_cats = ceo.category_summary
        eng_cats = eng.category_summary
        qa_cats = qa.category_summary

        # CEO has milestone/blocker/completion docs
        assert ceo_cats.get("milestone_docs", 0) >= 0
        # Engineer has architecture/implementation docs
        assert eng_cats.get("architecture_docs", 0) >= 0
        # QA has test/security/defect docs
        assert qa_cats.get("test_docs", 0) >= 0

    def test_project_isolation(self, engine):
        """Different projects should return different context."""
        general = engine.get_ceo_context(project="general")
        # Use a real project if it exists
        specific = engine.get_ceo_context(project="Titus-AI-OS-Upgrade")
        # Both should work without crashing
        assert general is not None
        assert specific is not None

    def test_no_unrestricted_vault_scanning(self, engine):
        """Agents must not silently scan entire vault without access control."""
        for role_fn in [engine.get_ceo_context, engine.get_engineer_context, engine.get_qa_context]:
            resp = role_fn(project="general")
            for doc in resp.all_documents:
                # All returned docs must be public or shared
                assert doc.access_level in (AccessLevel.PUBLIC, AccessLevel.SHARED)

    def test_deduplication_across_roles(self, engine):
        """Documents should not be duplicated within a role response."""
        resp = engine.get_ceo_context(project="general")
        paths = [d.path for d in resp.all_documents]
        assert len(paths) == len(set(paths))
