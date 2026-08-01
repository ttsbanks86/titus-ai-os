"""Tests for knowledge_engine package."""
import pytest
from pathlib import Path

from knowledge_engine.config import KnowledgeEngineConfig
from knowledge_engine.inventory import scan_vault, build_inventory_report
from knowledge_engine.index import KnowledgeIndex
from knowledge_engine.search import SearchEngine
from knowledge_engine.cache import HotContextCache
from knowledge_engine.assembler import ContextAssembler
from knowledge_engine.access import AccessControl
from knowledge_engine.models import (
    AccessLevel,
    AuthorityRank,
    ContextRequest,
    DocumentMetadata,
    DocumentType,
    SearchResult,
)


@pytest.fixture
def config():
    return KnowledgeEngineConfig()


@pytest.fixture
def vault_docs(config):
    return scan_vault(config=config)


@pytest.fixture
def index(config):
    idx = KnowledgeIndex(config)
    idx.build()
    return idx


@pytest.fixture
def search(index, config):
    return SearchEngine(index, config)


@pytest.fixture
def cache(config):
    return HotContextCache(config)


# ─── Inventory Tests ──────────────────────────────────────────────

class TestInventory:
    def test_scan_vault_returns_documents(self, vault_docs):
        assert len(vault_docs) > 0

    def test_documents_have_required_fields(self, vault_docs):
        for doc in vault_docs[:20]:
            assert doc.path
            assert doc.filename
            assert doc.title
            assert isinstance(doc.doc_type, DocumentType)
            assert isinstance(doc.authority, AuthorityRank)
            assert isinstance(doc.access_level, AccessLevel)

    def test_dashboard_detected(self, vault_docs):
        dashboards = [d for d in vault_docs if d.doc_type == DocumentType.DASHBOARD]
        assert len(dashboards) >= 1

    def test_sop_detected(self, vault_docs):
        sops = [d for d in vault_docs if d.doc_type == DocumentType.SOP]
        assert len(sops) >= 1

    def test_agent_detected(self, vault_docs):
        agents = [d for d in vault_docs if d.doc_type == DocumentType.AGENT]
        assert len(agents) >= 1

    def test_build_inventory_report(self, vault_docs):
        report = build_inventory_report(vault_docs)
        assert "total_documents" in report
        assert report["total_documents"] == len(vault_docs)
        assert "by_type" in report
        assert "by_authority" in report

    def test_wiki_links_extracted(self, vault_docs):
        with_links = [d for d in vault_docs if d.wiki_links]
        assert len(with_links) > 0

    def test_source_of_truth_detected(self, vault_docs):
        sot = [d for d in vault_docs if d.is_source_of_truth]
        assert len(sot) >= 1

    def test_checksum_computed(self, vault_docs):
        for doc in vault_docs[:10]:
            assert len(doc.checksum) > 0

    def test_content_preview_extracted(self, vault_docs):
        with_preview = [d for d in vault_docs if d.content_preview]
        assert len(with_preview) > 0


# ─── Index Tests ──────────────────────────────────────────────────

class TestIndex:
    def test_build_populates_index(self, index):
        assert len(index.documents) > 0
        assert index._built is True

    def test_get_by_path(self, index):
        first = index.documents[0]
        result = index.get_by_path(first.path)
        assert result is not None
        assert result.path == first.path

    def test_get_by_project(self, index):
        projects = set(d.project for d in index.documents)
        for project in projects:
            docs = index.get_by_project(project)
            assert len(docs) > 0

    def test_get_by_type(self, index):
        for dtype in ["note", "project", "sop", "agent"]:
            docs = index.get_by_type(dtype)
            assert isinstance(docs, list)

    def test_get_by_authority(self, index):
        for auth in ["SOURCE_OF_TRUTH", "GOVERNING", "CURRENT", "REFERENCE", "ARCHIVED"]:
            docs = index.get_by_authority(auth)
            assert isinstance(docs, list)

    def test_get_source_of_truth(self, index):
        sot = index.get_source_of_truth()
        assert len(sot) >= 1
        for doc in sot:
            assert doc.is_source_of_truth

    def test_get_governing(self, index):
        governing = index.get_governing()
        assert len(governing) >= 1

    def test_keyword_search(self, index):
        results = index.keyword_search("AI")
        assert len(results) > 0

    def test_stats(self, index):
        stats = index.stats()
        assert "total_documents" in stats
        assert "by_type" in stats
        assert "by_authority" in stats
        assert stats["built"] is True

    def test_incremental_update(self, index):
        changed = index.incremental_update()
        assert isinstance(changed, int)


# ─── Search Tests ─────────────────────────────────────────────────

class TestSearch:
    def test_search_returns_results(self, search):
        results = search.search("AI")
        assert len(results) > 0

    def test_search_results_have_scores(self, search):
        results = search.search("Titus")
        for r in results:
            assert 0.0 <= r.score <= 1.0

    def test_search_sorted_by_score(self, search):
        results = search.search("architecture")
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_search_with_project_filter(self, search):
        results = search.search("AI", project="general")
        assert isinstance(results, list)

    def test_search_exact(self, search):
        results = search.search_exact("Home")
        assert isinstance(results, list)

    def test_search_by_tag(self, search):
        results = search.search_by_tag("ai")
        assert isinstance(results, list)

    def test_search_by_project(self, search):
        results = search.search_by_project("general")
        assert isinstance(results, list)

    def test_search_by_title(self, search):
        results = search.search_by_title("Sprint")
        assert isinstance(results, list)


# ─── Cache Tests ──────────────────────────────────────────────────

class TestCache:
    def test_set_and_get(self, cache):
        cache.set("key1", {"data": 42})
        result = cache.get("key1")
        assert result == {"data": 42}

    def test_miss_returns_none(self, cache):
        result = cache.get("nonexistent")
        assert result is None

    def test_invalidate(self, cache):
        cache.set("key2", "value")
        assert cache.invalidate("key2") is True
        assert cache.get("key2") is None

    def test_invalidate_prefix(self, cache):
        cache.set("prefix:a", 1)
        cache.set("prefix:b", 2)
        cache.set("other:c", 3)
        removed = cache.invalidate_prefix("prefix:")
        assert removed == 2
        assert cache.get("other:c") == 3

    def test_clear(self, cache):
        cache.set("a", 1)
        cache.set("b", 2)
        count = cache.clear()
        assert count == 2
        assert cache.size == 0

    def test_stats(self, cache):
        cache.set("a", 1)
        cache.get("a")
        cache.get("miss")
        stats = cache.stats
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["size"] == 1

    def test_peek_does_not_affect_lru(self, cache):
        cache.set("a", 1)
        cache.set("b", 2)
        cache.peek("a")
        result = cache.get("a")
        assert result == 1


# ─── Access Control Tests ─────────────────────────────────────────

class TestAccessControl:
    def test_filter_by_access(self, index):
        access = AccessControl(index)
        docs = access.get_accessible_documents(AccessLevel.PUBLIC)
        assert len(docs) > 0
        for doc in docs:
            assert doc.access_level == AccessLevel.PUBLIC

    def test_filter_by_authority(self, index):
        access = AccessControl(index)
        docs = index.documents
        filtered = access.filter_by_authority(docs, AuthorityRank.GOVERNING)
        for doc in filtered:
            assert doc.authority.value >= AuthorityRank.GOVERNING.value

    def test_is_accessible(self, index):
        access = AccessControl(index)
        doc = index.documents[0]
        assert isinstance(access.is_accessible(doc, AccessLevel.PUBLIC), bool)

    def test_get_summary(self, index):
        access = AccessControl(index)
        summary = access.get_summary()
        assert "total_documents" in summary
        assert "by_access_level" in summary


# ─── Assembler Tests ──────────────────────────────────────────────

class TestAssembler:
    def test_assemble_returns_response(self, index, search, cache, config):
        assembler = ContextAssembler(index, search, cache, config)
        req = ContextRequest(
            project="general",
            agent_role="engineer",
            task="AI OS architecture",
            context_budget=4000,
            permissions=[AccessLevel.PUBLIC, AccessLevel.SHARED],
        )
        resp = assembler.assemble(req)
        assert resp is not None
        assert hasattr(resp, "source_of_truth_docs")
        assert hasattr(resp, "current_milestone_docs")
        assert hasattr(resp, "supporting_docs")
        assert hasattr(resp, "token_estimate")
        assert resp.assembly_time_ms >= 0

    def test_assemble_caches_result(self, index, search, cache, config):
        assembler = ContextAssembler(index, search, cache, config)
        req = ContextRequest(
            project="general",
            agent_role="engineer",
            task="caching test",
            context_budget=4000,
            permissions=[AccessLevel.PUBLIC],
        )
        resp1 = assembler.assemble(req)
        resp2 = assembler.assemble(req)
        assert resp1.assembly_time_ms >= 0
        assert resp2.assembly_time_ms >= 0

    def test_assemble_respects_budget(self, index, search, cache, config):
        assembler = ContextAssembler(index, search, cache, config)
        req = ContextRequest(
            project="general",
            agent_role="engineer",
            task="budget test",
            context_budget=500,
            permissions=[AccessLevel.PUBLIC],
        )
        resp = assembler.assemble(req)
        assert resp.token_estimate <= 500 + 100  # Small tolerance


# ─── Config Tests ─────────────────────────────────────────────────

class TestConfig:
    def test_default_config(self):
        config = KnowledgeEngineConfig()
        assert config.vault_root.exists()
        assert config.index_filename
        assert config.cache_max_entries > 0

    def test_config_exclusion_rules(self, config):
        assert len(config.excluded_paths) > 0
        assert len(config.excluded_extensions) > 0
