# knowledge_engine/assembler.py
# Phase F: Context Assembler — assembles context packages for sessions

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

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
    SearchResult,
)
from .search import SearchEngine


class ContextAssembler:
    """
    Assembles context packages for sessions.

    Orchestrates:
    - Query expansion from source documents
    - Authority-aware document selection
    - Token budget management
    - Cache-first lookup
    - Context assembly and formatting
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

    def assemble(self, request: ContextRequest) -> ContextResponse:
        """
        Assemble a context response for a context request.

        This is the main entry point for context assembly.
        """
        start = time.time()

        # Check cache first
        cache_key = self._cache_key(request)
        cached = self.cache.get(cache_key)
        if cached is not None:
            return ContextResponse(
                source_of_truth_docs=cached["source_of_truth_docs"],
                current_milestone_docs=cached["current_milestone_docs"],
                architecture_docs=cached["architecture_docs"],
                supporting_docs=cached["supporting_docs"],
                citations=cached["citations"],
                excluded_files=cached["excluded_files"],
                token_estimate=cached["token_estimate"],
                retrieval_evidence=cached["retrieval_evidence"],
                assembly_time_ms=time.time() - start,
            )

        # Expand the context to include related documents
        source_of_truth, current, architecture, supporting, citations, excluded = self._expand_context(request)

        # Apply token budget
        all_docs = source_of_truth + current + architecture + supporting
        selected, total_tokens, was_truncated = self._apply_budget(all_docs, request.context_budget)

        # Re-partition selected docs back into categories
        selected_paths = {d.path for d in selected}
        sot = [d for d in source_of_truth if d.path in selected_paths]
        cur = [d for d in current if d.path in selected_paths]
        arch = [d for d in architecture if d.path in selected_paths]
        sup = [d for d in supporting if d.path in selected_paths]

        # Get search results for evidence
        search_results = self.search.search(
            request.task,
            project=request.project if request.project != "general" else None,
            max_results=5,
        )

        response = ContextResponse(
            source_of_truth_docs=sot,
            current_milestone_docs=cur,
            architecture_docs=arch,
            supporting_docs=sup,
            citations=citations,
            excluded_files=excluded,
            token_estimate=total_tokens,
            retrieval_evidence=search_results,
            assembly_time_ms=time.time() - start,
        )

        # Cache the result
        self.cache.set(cache_key, {
            "source_of_truth_docs": sot,
            "current_milestone_docs": cur,
            "architecture_docs": arch,
            "supporting_docs": sup,
            "citations": citations,
            "excluded_files": excluded,
            "token_estimate": total_tokens,
            "retrieval_evidence": search_results,
        })

        return response

    def _expand_context(
        self, request: ContextRequest
    ) -> tuple[
        list[DocumentMetadata],
        list[DocumentMetadata],
        list[DocumentMetadata],
        list[DocumentMetadata],
        list[str],
        list[str],
    ]:
        """
        Expand context from a request.

        Returns (source_of_truth, current_milestone, architecture, supporting, citations, excluded).
        """
        source_of_truth: list[DocumentMetadata] = []
        current_milestone: list[DocumentMetadata] = []
        architecture: list[DocumentMetadata] = []
        supporting: list[DocumentMetadata] = []
        citations: list[str] = []
        excluded: list[str] = []
        seen_paths: set[str] = set()

        def _add(doc: DocumentMetadata, target: list) -> None:
            if doc.path not in seen_paths and doc.access_level not in request.permissions:
                # Check if this access level is allowed
                allowed = False
                for perm in request.permissions:
                    if doc.access_level == perm:
                        allowed = True
                        break
                if not allowed:
                    excluded.append(doc.path)
                    return
            if doc.path not in seen_paths:
                target.append(doc)
                seen_paths.add(doc.path)

        # 1. Source of truth documents
        for doc in self.index.get_source_of_truth():
            _add(doc, source_of_truth)

        # 2. Governing documents (SOPs, agents, rules)
        for doc in self.index.get_governing():
            if doc.path not in seen_paths:
                _add(doc, source_of_truth)

        # 3. Search results for the task
        search_results = self.search.search(
            request.task,
            project=request.project if request.project != "general" else None,
            max_results=10,
            include_archived=request.include_archived,
        )
        for result in search_results:
            doc = result.document
            citations.append(f"{result.score:.2f}: {doc.title} ({doc.path})")
            if doc.path not in seen_paths:
                if doc.doc_type == DocumentType.PROJECT:
                    _add(doc, current_milestone)
                elif doc.doc_type == DocumentType.REFERENCE and "architecture" in doc.path.lower():
                    _add(doc, architecture)
                else:
                    _add(doc, supporting)

        # 4. Project-specific documents
        if request.project and request.project != "general":
            for doc in self.index.get_by_project(request.project):
                if doc.path not in seen_paths:
                    if doc.doc_type == DocumentType.PROJECT:
                        _add(doc, current_milestone)
                    elif doc.doc_type == DocumentType.SOP or doc.doc_type == DocumentType.AGENT:
                        _add(doc, source_of_truth)
                    else:
                        _add(doc, supporting)

        # 5. Expand wiki-links from source of truth docs
        for doc in source_of_truth[:]:
            for link in doc.wiki_links:
                targets = self.index.get_wiki_link_targets(link)
                for target in targets:
                    if target.path not in seen_paths:
                        _add(target, supporting)

        return source_of_truth, current_milestone, architecture, supporting, citations, excluded

    def _apply_budget(
        self,
        documents: list[DocumentMetadata],
        max_tokens: int,
    ) -> tuple[list[DocumentMetadata], int, bool]:
        """
        Apply token budget to documents.

        Returns (selected_documents, total_tokens, was_truncated).
        """
        selected: list[DocumentMetadata] = []
        total_tokens = 0
        truncated = False

        for doc in documents:
            doc_tokens = doc.estimated_tokens if hasattr(doc, 'estimated_tokens') else len(doc.content_preview.split()) * 4
            if total_tokens + doc_tokens <= max_tokens:
                selected.append(doc)
                total_tokens += doc_tokens
            else:
                truncated = True
                break

        return selected, total_tokens, truncated

    def _cache_key(self, request: ContextRequest) -> str:
        """Generate a cache key for a context request."""
        parts = [
            request.project or "",
            request.agent_role or "",
            request.task or "",
            str(request.context_budget),
            str(request.include_archived),
        ]
        return "ctx:" + "|".join(parts)

    def invalidate_project(self, project: str) -> int:
        """Invalidate all cached contexts for a project."""
        return self.cache.invalidate_prefix(f"ctx:{project}|")
