# knowledge_engine/index.py
# Phase C: Knowledge Index — lookup support with incremental updates

from __future__ import annotations

import json
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import KnowledgeEngineConfig
from .inventory import load_inventory, scan_vault, save_inventory
from .models import (
    AccessLevel,
    AuthorityRank,
    DocumentMetadata,
    DocumentType,
)


class KnowledgeIndex:
    """
    In-memory index over vault documents.

    Supports:
    - Exact lookup by path
    - Keyword lookup by title, tags, content
    - Tag lookup
    - Project lookup
    - Authority ranking
    - Archive filtering
    - Ownership filtering
    - Incremental rebuilds
    """

    def __init__(self, config: Optional[KnowledgeEngineConfig] = None):
        self.config = config or KnowledgeEngineConfig()
        self.documents: list[DocumentMetadata] = []
        self._by_path: dict[str, DocumentMetadata] = {}
        self._by_project: dict[str, list[DocumentMetadata]] = defaultdict(list)
        self._by_type: dict[str, list[DocumentMetadata]] = defaultdict(list)
        self._by_authority: dict[str, list[DocumentMetadata]] = defaultdict(list)
        self._by_tag: dict[str, list[DocumentMetadata]] = defaultdict(list)
        self._by_access: dict[str, list[DocumentMetadata]] = defaultdict(list)
        self._keywords: dict[str, set[str]] = defaultdict(set)  # word -> set of paths
        self._built = False
        self._build_time: Optional[float] = None
        self._last_rebuild: Optional[datetime] = None

    def build(self, vault_root: Optional[Path] = None) -> None:
        """Build the index from scratch by scanning the vault."""
        start = time.time()
        self.documents = scan_vault(vault_root, self.config)
        self._rebuild_indices()
        self._build_time = time.time() - start
        self._last_rebuild = datetime.now()
        self._built = True

    def incremental_update(self, vault_root: Optional[Path] = None) -> int:
        """
        Perform incremental update. Returns number of documents changed.

        Compares checksums to detect changed files, then rebuilds
        affected indices.
        """
        if not self._built:
            self.build(vault_root)
            return len(self.documents)

        # Scan current vault state
        new_docs = scan_vault(vault_root, self.config)
        new_by_path = {d.path: d for d in new_docs}

        # Find changed, added, removed
        old_by_path = {d.path: d for d in self.documents}
        changed = 0

        for path, new_doc in new_by_path.items():
            old_doc = old_by_path.get(path)
            if old_doc is None:
                # New document
                changed += 1
            elif old_doc.checksum != new_doc.checksum:
                # Changed document
                changed += 1

        removed = set(old_by_path.keys()) - set(new_by_path.keys())
        changed += len(removed)

        if changed > 0:
            self.documents = new_docs
            self._rebuild_indices()
            self._last_rebuild = datetime.now()

        return changed

    def _rebuild_indices(self) -> None:
        """Rebuild all lookup indices from the documents list."""
        self._by_path.clear()
        self._by_project.clear()
        self._by_type.clear()
        self._by_authority.clear()
        self._by_tag.clear()
        self._by_access.clear()
        self._keywords.clear()

        for doc in self.documents:
            self._by_path[doc.path] = doc
            self._by_project[doc.project].append(doc)
            self._by_type[doc.doc_type.value].append(doc)
            self._by_authority[doc.authority.name].append(doc)
            self._by_access[doc.access_level.value].append(doc)

            for tag in doc.tags:
                self._by_tag[tag.lower()].append(doc)

            # Index keywords from title, filename, tags, path
            words = set()
            for text in [doc.title, doc.filename, doc.path, " ".join(doc.tags)]:
                words.update(self._tokenize(text))
            for word in words:
                self._keywords[word].add(doc.path)

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Tokenize text into lowercase words."""
        import re
        return [w.lower() for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 1]

    # ─── Lookup Methods ───────────────────────────────────────────────

    def get_by_path(self, path: str) -> Optional[DocumentMetadata]:
        """Exact lookup by relative path."""
        return self._by_path.get(path)

    def get_by_project(self, project: str) -> list[DocumentMetadata]:
        """Lookup all documents for a project."""
        return list(self._by_project.get(project, []))

    def get_by_type(self, doc_type: str) -> list[DocumentMetadata]:
        """Lookup all documents of a type."""
        return list(self._by_type.get(doc_type, []))

    def get_by_authority(self, authority: str) -> list[DocumentMetadata]:
        """Lookup all documents at an authority level."""
        return list(self._by_authority.get(authority, []))

    def get_by_tag(self, tag: str) -> list[DocumentMetadata]:
        """Lookup all documents with a specific tag."""
        return list(self._by_tag.get(tag.lower(), []))

    def get_by_access(self, access_level: str) -> list[DocumentMetadata]:
        """Lookup all documents at an access level."""
        return list(self._by_access.get(access_level, []))

    def keyword_search(self, query: str) -> list[DocumentMetadata]:
        """Search documents by keyword in title, tags, path."""
        query_words = self._tokenize(query)
        if not query_words:
            return []

        # Find documents matching ANY query word
        candidate_paths: set[str] = set()
        for word in query_words:
            for path in self._keywords.get(word, set()):
                candidate_paths.add(path)

        # If no direct matches, fall back to substring matching
        if not candidate_paths:
            for doc in self.documents:
                if doc.matches_query(query):
                    candidate_paths.add(doc.path)

        return [self._by_path[p] for p in candidate_paths if p in self._by_path]

    def get_source_of_truth(self) -> list[DocumentMetadata]:
        """Get all source-of-truth documents."""
        return [d for d in self.documents if d.is_source_of_truth]

    def get_governing(self) -> list[DocumentMetadata]:
        """Get all governing-level documents (SOPs, agents, rules)."""
        return [
            d for d in self.documents
            if d.authority == AuthorityRank.GOVERNING
            or d.doc_type in (DocumentType.SOP, DocumentType.AGENT)
        ]

    def get_non_archived(self) -> list[DocumentMetadata]:
        """Get all non-archived documents."""
        return [d for d in self.documents if not d.is_archived]

    def get_wiki_link_targets(self, link_name: str) -> list[DocumentMetadata]:
        """Find documents that could satisfy a wiki-link name."""
        results = []
        link_lower = link_name.lower().replace("-", " ").replace("_", " ")
        for doc in self.documents:
            doc_title_lower = doc.title.lower()
            doc_stem = Path(doc.filename).stem.lower().replace("-", " ").replace("_", " ")
            if link_lower == doc_title_lower or link_lower == doc_stem:
                results.append(doc)
        return results

    # ─── Authority Ranking ────────────────────────────────────────────

    def rank_by_authority(self, docs: list[DocumentMetadata]) -> list[DocumentMetadata]:
        """Sort documents by authority rank (highest first)."""
        return sorted(docs, key=lambda d: d.authority.value, reverse=True)

    # ─── Statistics ───────────────────────────────────────────────────

    def stats(self) -> dict:
        """Return index statistics."""
        return {
            "total_documents": len(self.documents),
            "by_type": {k: len(v) for k, v in self._by_type.items()},
            "by_project": {k: len(v) for k, v in self._by_project.items()},
            "by_authority": {k: len(v) for k, v in self._by_authority.items()},
            "by_access": {k: len(v) for k, v in self._by_access.items()},
            "unique_tags": len(self._by_tag),
            "unique_keywords": len(self._keywords),
            "built": self._built,
            "build_time_ms": round(self._build_time * 1000, 1) if self._build_time else None,
            "last_rebuild": self._last_rebuild.isoformat() if self._last_rebuild else None,
        }

    # ─── Persistence ──────────────────────────────────────────────────

    def save(self, path: Optional[Path] = None) -> None:
        """Save index to disk."""
        if path is None:
            path = self.config.vault_root / self.config.index_filename
        save_inventory(self.documents, path)

    def load(self, path: Optional[Path] = None) -> bool:
        """Load index from disk. Returns True if successful."""
        if path is None:
            path = self.config.vault_root / self.config.index_filename
        if not path.exists():
            return False
        try:
            self.documents = load_inventory(path)
            self._rebuild_indices()
            self._built = True
            return True
        except (json.JSONDecodeError, KeyError):
            return False
