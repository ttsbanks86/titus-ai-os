# knowledge_engine/access.py
# Phase G: Access Control — filtering documents by access level and ownership

from __future__ import annotations

from typing import Optional

from .config import KnowledgeEngineConfig
from .index import KnowledgeIndex
from .models import (
    AccessLevel,
    AuthorityRank,
    DocumentMetadata,
    DocumentType,
)


class AccessControl:
    """
    Access control for knowledge documents.

    Enforces:
    - Access level filtering (public < shared < project < restricted < secret)
    - Authority rank filtering
    - Ownership verification
    - Document type permissions
    - Archive exclusion
    """

    # Access level ordering (lowest to highest)
    LEVEL_ORDER: dict[AccessLevel, int] = {
        AccessLevel.PUBLIC: 0,
        AccessLevel.SHARED: 1,
        AccessLevel.PROJECT: 2,
        AccessLevel.RESTRICTED: 3,
        AccessLevel.SECRET: 4,
    }

    def __init__(
        self,
        index: KnowledgeIndex,
        config: Optional[KnowledgeEngineConfig] = None,
    ):
        self.index = index
        self.config = config or index.config

    def filter_by_access(
        self,
        documents: list[DocumentMetadata],
        max_level: AccessLevel = AccessLevel.PUBLIC,
    ) -> list[DocumentMetadata]:
        """
        Filter documents to those accessible at or below the given level.

        Args:
            documents: Documents to filter
            max_level: Maximum access level allowed

        Returns:
            Filtered list of documents
        """
        max_idx = self.LEVEL_ORDER.get(max_level, 0)
        return [
            doc for doc in documents
            if self.LEVEL_ORDER.get(doc.access_level, 0) <= max_idx
        ]

    def filter_by_authority(
        self,
        documents: list[DocumentMetadata],
        min_authority: AuthorityRank = AuthorityRank.GOVERNING,
    ) -> list[DocumentMetadata]:
        """
        Filter documents to those at or above the given authority rank.

        Args:
            documents: Documents to filter
            min_authority: Minimum authority rank required

        Returns:
            Filtered list of documents
        """
        min_val = min_authority.value
        return [
            doc for doc in documents
            if doc.authority.value >= min_val
        ]

    def filter_by_ownership(
        self,
        documents: list[DocumentMetadata],
        owner_pattern: str,
    ) -> list[DocumentMetadata]:
        """
        Filter documents by ownership (title or filename contains pattern).

        Args:
            documents: Documents to filter
            owner_pattern: Pattern to match in title or filename

        Returns:
            Filtered list of documents
        """
        pattern_lower = owner_pattern.lower()
        return [
            doc for doc in documents
            if pattern_lower in doc.title.lower()
            or pattern_lower in doc.filename.lower()
        ]

    def filter_by_type(
        self,
        documents: list[DocumentMetadata],
        doc_type: str,
    ) -> list[DocumentMetadata]:
        """Filter documents by type."""
        return [
            doc for doc in documents
            if doc.doc_type.value == doc_type
        ]

    def filter_excludes_archived(
        self,
        documents: list[DocumentMetadata],
    ) -> list[DocumentMetadata]:
        """Remove archived documents."""
        return [doc for doc in documents if not doc.is_archived]

    def filter_source_of_truth(
        self,
        documents: list[DocumentMetadata],
    ) -> list[DocumentMetadata]:
        """Filter to only source-of-truth documents."""
        return [doc for doc in documents if doc.is_source_of_truth]

    def filter_governing(
        self,
        documents: list[DocumentMetadata],
    ) -> list[DocumentMetadata]:
        """Filter to governing-level documents (SOPs, agents, rules)."""
        return [
            doc for doc in documents
            if doc.authority == AuthorityRank.GOVERNING
            or doc.doc_type in (DocumentType.SOP, DocumentType.AGENT)
        ]

    def is_accessible(
        self,
        document: DocumentMetadata,
        max_level: AccessLevel = AccessLevel.PUBLIC,
    ) -> bool:
        """Check if a document is accessible at the given level."""
        return self.LEVEL_ORDER.get(document.access_level, 0) <= self.LEVEL_ORDER.get(max_level, 0)

    def get_accessible_documents(
        self,
        max_level: AccessLevel = AccessLevel.PUBLIC,
        include_archived: bool = False,
    ) -> list[DocumentMetadata]:
        """Get all documents accessible at or below the given level."""
        docs = self.index.documents
        if not include_archived:
            docs = self.filter_excludes_archived(docs)
        return self.filter_by_access(docs, max_level)

    def get_summary(self) -> dict:
        """Get access control summary statistics."""
        docs = self.index.documents
        by_level = {}
        for level in AccessLevel:
            by_level[level.value] = len(self.filter_by_access(docs, level))
        return {
            "total_documents": len(docs),
            "by_access_level": by_level,
            "source_of_truth_count": len(self.filter_source_of_truth(docs)),
            "governing_count": len(self.filter_governing(docs)),
            "archived_count": len([d for d in docs if d.is_archived]),
        }
