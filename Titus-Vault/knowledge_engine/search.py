# knowledge_engine/search.py
# Phase D: Search Engine — exact, keyword, tag, project search with authority ranking

from __future__ import annotations

import re
import time
from typing import Optional

from .config import KnowledgeEngineConfig
from .index import KnowledgeIndex
from .models import (
    AccessLevel,
    AuthorityRank,
    DocumentMetadata,
    SearchResult,
)


class SearchEngine:
    """
    Search engine over the knowledge index.

    Supports:
    - Exact search (title, filename, path match)
    - Keyword search (word-level matching)
    - Tag search
    - Project search
    - Title search
    - Authority-aware ranking
    - Archive filtering
    - Access level filtering
    """

    def __init__(
        self,
        index: KnowledgeIndex,
        config: Optional[KnowledgeEngineConfig] = None,
    ):
        self.index = index
        self.config = config or index.config

    def search(
        self,
        query: str,
        *,
        project: Optional[str] = None,
        doc_type: Optional[str] = None,
        tag: Optional[str] = None,
        access_level: Optional[AccessLevel] = None,
        include_archived: bool = False,
        max_results: Optional[int] = None,
    ) -> list[SearchResult]:
        """
        Search the knowledge base.

        Args:
            query: Search query string
            project: Filter by project name
            doc_type: Filter by document type
            tag: Filter by tag
            access_level: Filter by access level (max level)
            include_archived: Whether to include archived documents
            max_results: Maximum results to return

        Returns:
            List of SearchResult sorted by relevance score (highest first)
        """
        if max_results is None:
            max_results = self.config.max_search_results

        # Get candidate documents
        candidates = self._get_candidates(query, project, doc_type, tag, access_level, include_archived)

        # Score each candidate
        results = []
        for doc in candidates:
            score, reason, factors = self._score_document(doc, query, project, doc_type, tag)
            if score >= self.config.min_relevance_score:
                results.append(SearchResult(
                    document=doc,
                    score=score,
                    match_reason=reason,
                    rank_factors=factors,
                ))

        # Sort by score descending
        results.sort(key=lambda r: r.score, reverse=True)

        return results[:max_results]

    def search_exact(self, query: str, **kwargs) -> list[SearchResult]:
        """Exact title/filename match."""
        results = []
        query_lower = query.lower()
        for doc in self.index.documents:
            if doc.title.lower() == query_lower or doc.filename.lower() == query_lower:
                results.append(SearchResult(
                    document=doc,
                    score=1.0,
                    match_reason=f"Exact match: '{query}'",
                    rank_factors={"exact_match": True},
                ))
        return results

    def search_keyword(self, query: str, **kwargs) -> list[SearchResult]:
        """Keyword-based search."""
        return self.search(query, **kwargs)

    def search_by_tag(self, tag: str, **kwargs) -> list[SearchResult]:
        """Search by tag."""
        docs = self.index.get_by_tag(tag)
        return [
            SearchResult(
                document=doc,
                score=0.8,
                match_reason=f"Tag match: '{tag}'",
                rank_factors={"tag_match": True},
            )
            for doc in docs
        ]

    def search_by_project(self, project: str, **kwargs) -> list[SearchResult]:
        """Search by project."""
        docs = self.index.get_by_project(project)
        return [
            SearchResult(
                document=doc,
                score=0.7,
                match_reason=f"Project match: '{project}'",
                rank_factors={"project_match": True},
            )
            for doc in docs
        ]

    def search_by_title(self, title: str, **kwargs) -> list[SearchResult]:
        """Search by title (substring match)."""
        results = []
        title_lower = title.lower()
        for doc in self.index.documents:
            if title_lower in doc.title.lower():
                score = 0.9 if title_lower == doc.title.lower() else 0.6
                results.append(SearchResult(
                    document=doc,
                    score=score,
                    match_reason=f"Title match: '{title}'",
                    rank_factors={"title_match": True},
                ))
        return results

    # ─── Internal Methods ─────────────────────────────────────────────

    def _get_candidates(
        self,
        query: str,
        project: Optional[str],
        doc_type: Optional[str],
        tag: Optional[str],
        access_level: Optional[AccessLevel],
        include_archived: bool,
    ) -> list[DocumentMetadata]:
        """Get candidate documents based on filters."""
        candidates = list(self.index.documents)

        # Filter by project
        if project:
            candidates = [d for d in candidates if d.project == project]

        # Filter by type
        if doc_type:
            candidates = [d for d in candidates if d.doc_type.value == doc_type]

        # Filter by tag
        if tag:
            tag_lower = tag.lower()
            candidates = [d for d in candidates if tag_lower in [t.lower() for t in d.tags]]

        # Filter by access level
        if access_level:
            max_level = access_level.value
            level_order = ["public", "shared", "project", "restricted", "secret"]
            max_idx = level_order.index(max_level) if max_level in level_order else 0
            candidates = [
                d for d in candidates
                if level_order.index(d.access_level.value) <= max_idx
            ]

        # Filter archived
        if not include_archived:
            candidates = [d for d in candidates if not d.is_archived]

        return candidates

    def _score_document(
        self,
        doc: DocumentMetadata,
        query: str,
        project: Optional[str],
        doc_type: Optional[str],
        tag: Optional[str],
    ) -> tuple[float, str, dict]:
        """
        Score a document against a query.

        Returns (score, reason, factors) tuple.
        """
        factors = {}
        scores = []

        query_lower = query.lower()
        query_words = set(re.findall(r"[a-z0-9]+", query_lower))

        # 1. Title match (high weight)
        title_lower = doc.title.lower()
        if query_lower == title_lower:
            scores.append(1.0)
            factors["title_exact"] = True
        elif query_lower in title_lower:
            scores.append(0.8)
            factors["title_contains"] = True
        elif query_words:
            title_words = set(re.findall(r"[a-z0-9]+", title_lower))
            overlap = query_words & title_words
            if overlap:
                scores.append(0.5 * len(overlap) / len(query_words))
                factors["title_word_overlap"] = len(overlap)

        # 2. Filename match
        filename_lower = doc.filename.lower()
        if query_lower in filename_lower:
            scores.append(0.6)
            factors["filename_match"] = True

        # 3. Tag match
        tag_words = set()
        for t in doc.tags:
            tag_words.update(re.findall(r"[a-z0-9]+", t.lower()))
        if query_words and tag_words:
            overlap = query_words & tag_words
            if overlap:
                scores.append(0.7 * len(overlap) / len(query_words))
                factors["tag_match"] = len(overlap)

        # 4. Path match
        if query_lower in doc.path.lower():
            scores.append(0.3)
            factors["path_match"] = True

        # 5. Content preview match
        if query_lower in doc.content_preview.lower():
            scores.append(0.4)
            factors["content_match"] = True

        # 6. Wiki-link match
        for link in doc.wiki_links:
            if query_lower in link.lower():
                scores.append(0.5)
                factors["wiki_link_match"] = True
                break

        # Calculate base relevance score
        if scores:
            relevance = max(scores)
        else:
            relevance = 0.0

        # 7. Authority bonus
        authority_bonus = doc.authority.value / 5.0 * self.config.authority_weight

        # 8. Recency bonus
        recency_bonus = 0.0
        if doc.modified:
            days_old = (time.time() - doc.modified.timestamp()) / 86400
            recency_bonus = max(0, 1.0 - days_old / 365) * self.config.recency_weight

        # Final score
        final_score = (
            relevance * self.config.relevance_weight
            + authority_bonus
            + recency_bonus
        )

        # Build reason
        reason_parts = []
        if factors.get("title_exact"):
            reason_parts.append(f"exact title match: '{doc.title}'")
        elif factors.get("title_contains"):
            reason_parts.append(f"title contains: '{doc.title}'")
        elif factors.get("tag_match"):
            reason_parts.append(f"tag match")
        elif factors.get("content_match"):
            reason_parts.append(f"content match")
        else:
            reason_parts.append(f"path match")

        if doc.is_source_of_truth:
            reason_parts.append("source of truth")

        reason = "; ".join(reason_parts) if reason_parts else "scored result"

        return min(final_score, 1.0), reason, factors
