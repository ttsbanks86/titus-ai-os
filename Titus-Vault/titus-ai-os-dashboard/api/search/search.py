"""
Titus AI OS Search — Provider-based implementation.

Gate D: Reclassified from "SemanticSearch" to "KeywordSearch".
Added SemanticSearchProvider ABC and HybridSearch for future vector integration.

Classification: KEYWORD_SEARCH_ONLY with SEMANTIC_PROVIDER_BOUNDARY.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class SearchResult:
    """A single search result."""
    id: str
    title: str
    content: str
    score: float
    source: str
    file_path: str
    line_number: Optional[int] = None
    context: str = ""


@dataclass
class SearchQuery:
    """A search query with metadata."""
    query: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    results_count: int = 0
    execution_time_ms: float = 0


# ---------------------------------------------------------------------------
# Provider interface
# ---------------------------------------------------------------------------

class SemanticSearchProvider(ABC):
    """
    Abstract base class for semantic search providers.

    Implementations should use embeddings and cosine similarity (or similar)
    to rank documents by semantic relevance, not just keyword overlap.

    This boundary exists so the system can swap between:
    - KeywordSearchProvider (default, no external dependencies)
    - A real vector/embedding provider when one becomes available
    """

    @abstractmethod
    def search(
        self,
        query: str,
        index: Dict[str, Dict],
        max_results: int = 10,
    ) -> List[SearchResult]:
        """Search the index using semantic similarity."""
        ...

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this provider's backend is reachable."""
        ...


# ---------------------------------------------------------------------------
# Keyword provider (current implementation — no embeddings)
# ---------------------------------------------------------------------------

class KeywordSearchProvider(SemanticSearchProvider):
    """
    Keyword-based search provider.

    Uses substring matching and word frequency scoring.
    No embeddings, no vectors, no cosine similarity.

    Classification: KEYWORD_SEARCH_ONLY
    """

    def search(
        self,
        query: str,
        index: Dict[str, Dict],
        max_results: int = 10,
    ) -> List[SearchResult]:
        query_lower = query.lower()
        query_words = set(re.findall(r"\w+", query_lower))

        results: List[SearchResult] = []

        for path, doc in index.items():
            content_lower = doc["content"].lower()
            title_lower = doc["title"].lower()

            score = 0.0

            # Title match (highest weight)
            if query_lower in title_lower:
                score += 1.0
            for word in query_words:
                if word in title_lower:
                    score += 0.3

            # Content match
            if query_lower in content_lower:
                score += 0.5
            for word in query_words:
                if word in content_lower:
                    score += 0.1

            # Frequency bonus
            for word in query_words:
                count = content_lower.count(word)
                score += min(count * 0.05, 0.3)

            if score >= 0.1:
                context = self._extract_context(content_lower, query_lower)
                results.append(
                    SearchResult(
                        id=path,
                        title=doc["title"],
                        content=doc["content"][:500] + "..." if len(doc["content"]) > 500 else doc["content"],
                        score=min(score, 1.0),
                        source=doc["path"],
                        file_path=path,
                        context=context,
                    )
                )

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:max_results]

    def is_available(self) -> bool:
        return True  # Always available — no external dependencies

    @staticmethod
    def _extract_context(content: str, query: str, chars: int = 200) -> str:
        idx = content.find(query)
        if idx == -1:
            return ""
        start = max(0, idx - chars // 2)
        end = min(len(content), idx + len(query) + chars // 2)
        return content[start:end].strip()


# ---------------------------------------------------------------------------
# High-level search class (backwards-compatible rename)
# ---------------------------------------------------------------------------

class KeywordSearch:
    """
    Keyword search engine for the knowledge base.

    Uses substring matching and relevance scoring.
    No embeddings, no vectors, no cosine similarity.

    Gate D: Renamed from SemanticSearch to KeywordSearch.
    """

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.index: Dict[str, Dict] = {}
        self.provider: SemanticSearchProvider = KeywordSearchProvider()
        self.build_index()

    def build_index(self):
        """Build search index from vault files."""
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                relative_path = md_file.relative_to(self.vault_path)

                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = title_match.group(1) if title_match else md_file.stem

                self.index[str(relative_path)] = {
                    "title": title,
                    "content": content,
                    "path": str(relative_path),
                    "size": len(content),
                    "modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat(),
                }
            except Exception:
                continue

    def search(
        self,
        query: str,
        max_results: int = 10,
        min_score: float = 0.1,
    ) -> List[SearchResult]:
        """
        Search the knowledge base.

        Uses keyword matching via the configured provider.
        Default provider is KeywordSearchProvider (no embeddings).
        """
        return self.provider.search(query, self.index, max_results)

    def search_by_tag(self, tag: str) -> List[SearchResult]:
        """Search for files with a specific tag."""
        results = []
        for path, doc in self.index.items():
            if f"#{tag}" in doc["content"] or f"tags: {tag}" in doc["content"].lower():
                results.append(
                    SearchResult(
                        id=path,
                        title=doc["title"],
                        content=doc["content"][:200],
                        score=1.0,
                        source=doc["path"],
                        file_path=path,
                    )
                )
        return results

    def search_by_folder(self, folder: str) -> List[SearchResult]:
        """Search for files in a specific folder."""
        results = []
        for path, doc in self.index.items():
            if folder.lower() in path.lower():
                results.append(
                    SearchResult(
                        id=path,
                        title=doc["title"],
                        content=doc["content"][:200],
                        score=0.8,
                        source=doc["path"],
                        file_path=path,
                    )
                )
        return results

    def get_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions based on partial query."""
        suggestions = []
        partial_lower = partial_query.lower()

        for doc in self.index.values():
            if partial_lower in doc["title"].lower():
                suggestions.append(doc["title"])

        common_terms = [
            "project", "milestone", "task", "agent", "knowledge",
            "verification", "test", "security", "performance",
        ]
        for term in common_terms:
            if partial_lower in term:
                suggestions.append(term)

        return list(set(suggestions))[:10]

    def get_stats(self) -> Dict[str, Any]:
        """Get search index statistics."""
        total_size = sum(doc["size"] for doc in self.index.values())

        folder_counts: Dict[str, int] = {}
        for path in self.index.keys():
            folder = path.split("/")[0] if "/" in path else "root"
            folder_counts[folder] = folder_counts.get(folder, 0) + 1

        return {
            "total_documents": len(self.index),
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2),
            "folders": folder_counts,
            "last_indexed": datetime.now().isoformat(),
        }


# ---------------------------------------------------------------------------
# Hybrid search — routes to best available provider
# ---------------------------------------------------------------------------

class HybridSearch:
    """
    Hybrid search that uses a semantic provider when available,
    falling back to keyword search.

    Provider priority:
    1. Injected SemanticSearchProvider (if is_available() == True)
    2. KeywordSearchProvider (always available)
    """

    def __init__(
        self,
        vault_path: str,
        semantic_provider: Optional[SemanticSearchProvider] = None,
    ):
        self.vault_path = Path(vault_path)
        self.keyword = KeywordSearch(vault_path)
        self.semantic_provider = semantic_provider

    def search(
        self,
        query: str,
        max_results: int = 10,
    ) -> List[SearchResult]:
        """
        Search using the best available provider.
        Falls back to keyword if semantic provider is unavailable.
        """
        if self.semantic_provider and self.semantic_provider.is_available():
            return self.semantic_provider.search(query, self.keyword.index, max_results)

        return self.keyword.search(query, max_results)

    @property
    def active_provider(self) -> str:
        """Return the name of the currently active provider."""
        if self.semantic_provider and self.semantic_provider.is_available():
            return self.semantic_provider.__class__.__name__
        return "KeywordSearchProvider"
