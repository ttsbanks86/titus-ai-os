"""
Titus AI OS Search Engine
Provider-based search with keyword fallback and semantic search boundary.

Gate D correction: The original "SemanticSearch" was reclassified as
"KeywordSearch" because it uses only string matching, not embeddings
or cosine similarity. A provider boundary has been added so that real
semantic search (vector-based) can be plugged in when available.
"""

from .search import (
    SearchResult,
    SearchQuery,
    KeywordSearch,
    SemanticSearchProvider,
    KeywordSearchProvider,
    HybridSearch,
)

__all__ = [
    "SearchResult",
    "SearchQuery",
    "KeywordSearch",
    "SemanticSearchProvider",
    "KeywordSearchProvider",
    "HybridSearch",
]
