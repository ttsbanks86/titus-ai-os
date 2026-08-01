"""Integration tests for the knowledge_engine — end-to-end workflows."""
import pytest
from pathlib import Path

from knowledge_engine.config import KnowledgeEngineConfig
from knowledge_engine.index import KnowledgeIndex
from knowledge_engine.search import SearchEngine
from knowledge_engine.cache import HotContextCache
from knowledge_engine.assembler import ContextAssembler
from knowledge_engine.access import AccessControl
from knowledge_engine.models import AccessLevel, ContextRequest


@pytest.fixture
def engine():
    """Build a complete knowledge engine stack."""
    config = KnowledgeEngineConfig()
    index = KnowledgeIndex(config)
    index.build()
    search = SearchEngine(index, config)
    cache = HotContextCache(config)
    assembler = ContextAssembler(index, search, cache, config)
    access = AccessControl(index, config)
    return {
        "config": config,
        "index": index,
        "search": search,
        "cache": cache,
        "assembler": assembler,
        "access": access,
    }


class TestEndToEndWorkflow:
    """Full workflow integration tests."""

    def test_session_startup_workflow(self, engine):
        """Simulate session startup: scan, index, search for context."""
        index = engine["index"]
        search = engine["search"]

        # 1. Build index
        assert len(index.documents) > 0

        # 2. Search for session context
        dashboards = index.get_by_type("dashboard")
        assert len(dashboards) >= 1

        # 3. Search for goals
        goals = search.search_by_title("Goals")
        assert len(goals) >= 1

        # 4. Search for rules
        rules = search.search_by_title("Rules")
        assert len(rules) >= 1

    def test_context_assembly_workflow(self, engine):
        """Test full context assembly with budget."""
        assembler = engine["assembler"]

        request = ContextRequest(
            project="general",
            agent_role="engineer",
            task="implement new feature for Titus AI OS",
            context_budget=2000,
            permissions=[AccessLevel.PUBLIC, AccessLevel.SHARED],
        )

        response = assembler.assemble(request)
        assert response.token_estimate <= 2000 + 200
        assert len(response.source_of_truth_docs) >= 1
        assert len(response.citations) >= 1

    def test_search_with_multiple_filters(self, engine):
        """Test search with combined filters."""
        search = engine["search"]

        results = search.search(
            "AI",
            project="general",
            tag=None,
            max_results=5,
        )
        assert len(results) <= 5
        for r in results:
            assert r.score >= 0.0

    def test_cache_invalidation_on_project_change(self, engine):
        """Test cache invalidation when a project changes."""
        cache = engine["cache"]
        assembler = engine["assembler"]

        # Populate cache
        req = ContextRequest(
            project="general",
            agent_role="engineer",
            task="cache invalidation test",
            context_budget=4000,
            permissions=[AccessLevel.PUBLIC],
        )
        assembler.assemble(req)
        assert cache.size > 0

        # Invalidate
        removed = cache.invalidate_prefix("ctx:")
        assert removed >= 1

    def test_access_control_enforcement(self, engine):
        """Test that access control properly filters documents."""
        access = engine["access"]
        index = engine["index"]

        # Public access should not include secret docs
        public_docs = access.get_accessible_documents(AccessLevel.PUBLIC)
        for doc in public_docs:
            assert doc.access_level == AccessLevel.PUBLIC

        # All docs include everything up to the allowed level
        all_docs = access.get_accessible_documents(AccessLevel.SECRET)
        assert len(all_docs) >= len(public_docs)

    def test_incremental_update_preserves_state(self, engine):
        """Test that incremental update preserves index state."""
        index = engine["index"]
        initial_count = len(index.documents)

        changed = index.incremental_update()
        assert len(index.documents) == initial_count or changed > 0

    def test_authority_ranking(self, engine):
        """Test that authority ranking works correctly."""
        index = engine["index"]
        search = engine["search"]

        results = search.search("architecture")
        if len(results) >= 2:
            # Higher authority docs should rank higher (all else equal)
            scores = [r.score for r in results]
            assert scores == sorted(scores, reverse=True)

    def test_full_lifecycle(self, engine):
        """Test complete lifecycle: build -> search -> assemble -> cache -> invalidate."""
        index = engine["index"]
        search = engine["search"]
        cache = engine["cache"]
        assembler = engine["assembler"]

        # 1. Build
        assert index._built

        # 2. Search
        results = search.search("Titus AI OS")
        assert len(results) > 0

        # 3. Assemble
        req = ContextRequest(
            project="general",
            agent_role="engineer",
            task="lifecycle test",
            context_budget=3000,
            permissions=[AccessLevel.PUBLIC],
        )
        resp = assembler.assemble(req)
        assert resp.token_estimate > 0

        # 4. Cache hit
        resp2 = assembler.assemble(req)
        assert resp2 is not None

        # 5. Invalidate
        cache.clear()
        assert cache.size == 0
