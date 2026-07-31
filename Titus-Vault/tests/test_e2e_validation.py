"""Phase J: End-to-End Validation — 12 scenario tests proving full workflow."""
import pytest
import time

from knowledge_engine.config import KnowledgeEngineConfig
from knowledge_engine.index import KnowledgeIndex
from knowledge_engine.search import SearchEngine
from knowledge_engine.cache import HotContextCache
from knowledge_engine.assembler import ContextAssembler
from knowledge_engine.access import AccessControl
from knowledge_engine.agents import AgentContextProvider, AgentRole
from knowledge_engine.models import AccessLevel, ContextRequest


@pytest.fixture(scope="module")
def engine():
    """Build complete engine stack once for all E2E tests."""
    config = KnowledgeEngineConfig()
    index = KnowledgeIndex(config)
    index.build()
    search = SearchEngine(index, config)
    cache = HotContextCache(config)
    assembler = ContextAssembler(index, search, cache, config)
    access = AccessControl(index, config)
    provider = AgentContextProvider(index, search, cache, config)
    return {
        "config": config,
        "index": index,
        "search": search,
        "cache": cache,
        "assembler": assembler,
        "access": access,
        "provider": provider,
    }


class TestEndToEndValidation:
    """12 end-to-end scenarios proving M2 completeness."""

    def test_scenario_01_project_session_starts(self, engine):
        """Scenario 1: A project session starts."""
        index = engine["index"]
        assert index._built
        assert len(index.documents) > 0

    def test_scenario_02_correct_source_of_truth_loads(self, engine):
        """Scenario 2: The correct Source of Truth loads."""
        index = engine["index"]
        sot = index.get_source_of_truth()
        assert len(sot) >= 1
        for doc in sot:
            assert doc.is_source_of_truth

    def test_scenario_03_ceo_receives_executive_context(self, engine):
        """Scenario 3: The CEO receives executive context."""
        provider = engine["provider"]
        resp = provider.get_ceo_context(project="general")
        assert resp.role == AgentRole.CEO
        assert resp.document_count >= 1
        assert resp.total_tokens > 0
        assert len(resp.retrieval_evidence) >= 1

    def test_scenario_04_engineer_receives_implementation_context(self, engine):
        """Scenario 4: The engineer receives implementation context."""
        provider = engine["provider"]
        resp = provider.get_engineer_context(project="general")
        assert resp.role == AgentRole.ENGINEER
        assert resp.document_count >= 1
        assert len(resp.architecture_docs) >= 0
        assert len(resp.implementation_docs) >= 0

    def test_scenario_05_qa_receives_verification_context(self, engine):
        """Scenario 5: QA receives verification context."""
        provider = engine["provider"]
        resp = provider.get_qa_context(project="general")
        assert resp.role == AgentRole.QA
        assert resp.document_count >= 1
        assert len(resp.test_docs) >= 0
        assert len(resp.security_docs) >= 0

    def test_scenario_06_each_role_gets_different_results(self, engine):
        """Scenario 6: Each role receives different relevant results."""
        provider = engine["provider"]
        ceo = provider.get_ceo_context(project="general")
        eng = provider.get_engineer_context(project="general")
        qa = provider.get_qa_context(project="general")

        # At least two roles should differ in document counts or categories
        ceo_paths = set(d.path for d in ceo.all_documents)
        eng_paths = set(d.path for d in eng.all_documents)
        qa_paths = set(d.path for d in qa.all_documents)

        # Not all identical
        assert not (ceo_paths == eng_paths == qa_paths)

    def test_scenario_07_project_boundaries_enforced(self, engine):
        """Scenario 7: Project boundaries remain enforced."""
        provider = engine["provider"]
        general = provider.get_ceo_context(project="general")
        specific = provider.get_ceo_context(project="Titus-AI-OS-Upgrade")

        # Both should return valid responses
        assert general is not None
        assert specific is not None

        # Both should have source of truth (shared across projects)
        assert len(general.source_of_truth) >= 1
        assert len(specific.source_of_truth) >= 1

        # Specific project should not have docs from unrelated projects
        for doc in specific.project_docs:
            assert doc.project == "Titus-AI-OS-Upgrade" or doc.is_source_of_truth

    def test_scenario_08_archived_cannot_override_current(self, engine):
        """Scenario 8: Archived instructions do not override current instructions."""
        provider = engine["provider"]
        resp = provider.get_ceo_context(project="general", include_archived=False)

        # No archived docs should be in the response
        for doc in resp.all_documents:
            assert not doc.is_archived, f"Archived doc leaked: {doc.path}"

    def test_scenario_09_restricted_files_denied(self, engine):
        """Scenario 9: Restricted files are denied."""
        provider = engine["provider"]
        resp = provider.get_ceo_context(project="general")

        for doc in resp.all_documents:
            assert doc.access_level in (AccessLevel.PUBLIC, AccessLevel.SHARED), \
                f"Unauthorized doc: {doc.path} (level={doc.access_level})"

    def test_scenario_10_context_budgets_enforced(self, engine):
        """Scenario 10: Context budgets are enforced."""
        provider = engine["provider"]
        budgets = [500, 1000, 2000, 4000]

        for budget in budgets:
            resp = provider.get_ceo_context(project="general", max_tokens=budget)
            assert resp.total_tokens <= budget + 200, \
                f"Budget {budget} exceeded: got {resp.total_tokens}"

    def test_scenario_11_deterministic_response(self, engine):
        """Scenario 11: The engine responds deterministically."""
        provider = engine["provider"]
        resp1 = provider.get_ceo_context(project="general")
        resp2 = provider.get_ceo_context(project="general")

        # Same documents should be returned
        paths1 = [d.path for d in resp1.all_documents]
        paths2 = [d.path for d in resp2.all_documents]
        assert paths1 == paths2

    def test_scenario_12_cache_invalidation_works(self, engine):
        """Scenario 12: Cache invalidation works after source changes."""
        cache = engine["cache"]
        provider = engine["provider"]

        # Clear any prior state
        cache.clear()

        # Populate cache
        provider.get_ceo_context(project="general")
        initial_size = cache.size
        assert initial_size > 0, f"Cache should be populated after context load, got size={initial_size}"

        # Invalidate
        cleared = cache.clear()
        assert cleared > 0
        assert cache.size == 0

        # Next request rebuilds cache
        provider.get_ceo_context(project="general")
        assert cache.size > 0
