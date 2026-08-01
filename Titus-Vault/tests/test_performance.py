"""Phase K: Performance Validation — benchmarks and thresholds."""
import pytest
import time
import statistics

from knowledge_engine.config import KnowledgeEngineConfig
from knowledge_engine.index import KnowledgeIndex
from knowledge_engine.search import SearchEngine
from knowledge_engine.cache import HotContextCache
from knowledge_engine.assembler import ContextAssembler
from knowledge_engine.access import AccessControl
from knowledge_engine.agents import AgentContextProvider, AgentRole
from knowledge_engine.models import AccessLevel, ContextRequest


@pytest.fixture(scope="module")
def perf_engine():
    """Build engine for performance testing."""
    config = KnowledgeEngineConfig()
    index = KnowledgeIndex(config)
    index.build()
    search = SearchEngine(index, config)
    cache = HotContextCache(config)
    assembler = ContextAssembler(index, search, cache, config)
    provider = AgentContextProvider(index, search, cache, config)
    return {
        "config": config,
        "index": index,
        "search": search,
        "cache": cache,
        "assembler": assembler,
        "provider": provider,
    }


class TestPerformanceValidation:
    """Performance benchmarks with reasonable thresholds."""

    def test_initial_indexing_performance(self, perf_engine):
        """Initial indexing should complete within threshold."""
        index = KnowledgeIndex(perf_engine["config"])
        start = time.perf_counter()
        index.build()
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Threshold: full vault index in under 10 seconds
        assert elapsed_ms < 10000, f"Indexing too slow: {elapsed_ms:.0f}ms"
        print(f"  Initial indexing: {elapsed_ms:.0f}ms ({len(index.documents)} docs)")

    def test_incremental_indexing_performance(self, perf_engine):
        """Incremental indexing should be fast."""
        index = perf_engine["index"]
        start = time.perf_counter()
        changed = index.incremental_update()
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Threshold: incremental update in under 10 seconds
        assert elapsed_ms < 10000, f"Incremental update too slow: {elapsed_ms:.0f}ms"
        print(f"  Incremental indexing: {elapsed_ms:.0f}ms ({changed} changed)")

    def test_keyword_search_performance(self, perf_engine):
        """Keyword search should be fast."""
        search = perf_engine["search"]
        queries = ["AI", "architecture", "Titus", "sprint", "test", "career", "knowledge"]
        times = []

        for q in queries:
            start = time.perf_counter()
            results = search.search(q)
            elapsed_ms = (time.perf_counter() - start) * 1000
            times.append(elapsed_ms)

        avg_ms = statistics.mean(times)
        p95_ms = sorted(times)[int(len(times) * 0.95)]

        # Threshold: average search under 100ms, p95 under 200ms
        assert avg_ms < 100, f"Average search too slow: {avg_ms:.1f}ms"
        assert p95_ms < 200, f"P95 search too slow: {p95_ms:.1f}ms"
        print(f"  Search avg: {avg_ms:.1f}ms, p95: {p95_ms:.1f}ms")

    def test_authority_ranked_retrieval_performance(self, perf_engine):
        """Authority-ranked retrieval should be fast."""
        search = perf_engine["search"]
        start = time.perf_counter()
        results = search.search("architecture", max_results=20)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Verify results are sorted by score
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

        # Threshold: under 100ms
        assert elapsed_ms < 100, f"Authority retrieval too slow: {elapsed_ms:.1f}ms"
        print(f"  Authority retrieval: {elapsed_ms:.1f}ms")

    def test_cache_hit_performance(self, perf_engine):
        """Cache hit should be very fast."""
        cache = perf_engine["cache"]
        cache.set("perf_test", {"data": list(range(1000))})

        start = time.perf_counter()
        for _ in range(100):
            result = cache.get("perf_test")
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Threshold: 100 cache reads under 10ms
        assert elapsed_ms < 10, f"Cache hit too slow: {elapsed_ms:.1f}ms"
        assert result == {"data": list(range(1000))}
        print(f"  Cache hit (100 reads): {elapsed_ms:.1f}ms")

    def test_cache_miss_performance(self, perf_engine):
        """Cache miss should be fast (no blocking)."""
        cache = perf_engine["cache"]

        start = time.perf_counter()
        for i in range(100):
            result = cache.get(f"nonexistent_{i}")
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Threshold: 100 cache misses under 10ms
        assert elapsed_ms < 10, f"Cache miss too slow: {elapsed_ms:.1f}ms"
        assert result is None
        print(f"  Cache miss (100 reads): {elapsed_ms:.1f}ms")

    def test_ceo_context_assembly_performance(self, perf_engine):
        """CEO context assembly should be within threshold."""
        provider = perf_engine["provider"]

        start = time.perf_counter()
        resp = provider.get_ceo_context(project="general", max_tokens=4000)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Threshold: CEO context under 2 seconds
        assert elapsed_ms < 2000, f"CEO context too slow: {elapsed_ms:.0f}ms"
        print(f"  CEO context assembly: {elapsed_ms:.0f}ms ({resp.document_count} docs, {resp.total_tokens} tokens)")

    def test_engineer_context_assembly_performance(self, perf_engine):
        """Engineer context assembly should be within threshold."""
        provider = perf_engine["provider"]

        start = time.perf_counter()
        resp = provider.get_engineer_context(project="general", max_tokens=4000)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Threshold: Engineer context under 2 seconds
        assert elapsed_ms < 2000, f"Engineer context too slow: {elapsed_ms:.0f}ms"
        print(f"  Engineer context assembly: {elapsed_ms:.0f}ms ({resp.document_count} docs, {resp.total_tokens} tokens)")

    def test_qa_context_assembly_performance(self, perf_engine):
        """QA context assembly should be within threshold."""
        provider = perf_engine["provider"]

        start = time.perf_counter()
        resp = provider.get_qa_context(project="general", max_tokens=4000)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Threshold: QA context under 2 seconds
        assert elapsed_ms < 2000, f"QA context too slow: {elapsed_ms:.0f}ms"
        print(f"  QA context assembly: {elapsed_ms:.0f}ms ({resp.document_count} docs, {resp.total_tokens} tokens)")
