# knowledge_engine/models.py
# Shared data models for the Knowledge & Context Engine

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class DocumentType(Enum):
    """Types of documents in the vault."""
    NOTE = "note"
    PROJECT = "project"
    SOP = "sop"
    AGENT = "agent"
    REFERENCE = "reference"
    DECISION = "decision"
    DASHBOARD = "dashboard"
    TEMPLATE = "template"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"


class AccessLevel(Enum):
    """Access levels for documents."""
    PUBLIC = "public"
    SHARED = "shared"
    PROJECT = "project"
    RESTRICTED = "restricted"
    SECRET = "secret"


class AuthorityRank(Enum):
    """Authority ranking for documents. Higher rank = higher authority."""
    SOURCE_OF_TRUTH = 5
    GOVERNING = 4
    CURRENT = 3
    REFERENCE = 2
    ARCHIVED = 1
    UNKNOWN = 0


@dataclass
class DocumentMetadata:
    """Metadata for a single document in the vault."""
    path: str                          # Relative path from vault root
    filename: str                      # Just the filename
    title: str                         # Display title
    doc_type: DocumentType             # Document type
    project: str                       # Project name (or "general")
    owner: str                         # Owner/author
    authority: AuthorityRank           # Authority level
    tags: list[str] = field(default_factory=list)
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    size_bytes: int = 0
    is_archived: bool = False
    is_source_of_truth: bool = False
    access_level: AccessLevel = AccessLevel.PUBLIC
    wiki_links: list[str] = field(default_factory=list)
    content_preview: str = ""          # First 200 chars
    checksum: str = ""                 # SHA-256 for change detection

    @property
    def extension(self) -> str:
        return Path(self.filename).suffix.lower()

    @property
    def directory(self) -> str:
        return str(Path(self.path).parent)

    @property
    def estimated_tokens(self) -> int:
        """Estimate token count (roughly 4 chars per token)."""
        return max(1, len(self.content_preview) // 4)

    def matches_query(self, query: str) -> bool:
        """Check if this document matches a search query."""
        query_lower = query.lower()
        return (
            query_lower in self.title.lower()
            or query_lower in self.filename.lower()
            or query_lower in " ".join(self.tags).lower()
            or query_lower in self.path.lower()
        )


@dataclass
class SearchResult:
    """A single search result with ranking information."""
    document: DocumentMetadata
    score: float                       # Relevance score (0.0 to 1.0)
    match_reason: str                  # Why this matched
    rank_factors: dict = field(default_factory=dict)


@dataclass
class ContextRequest:
    """Request for context assembly."""
    project: str
    agent_role: str
    task: str
    context_budget: int = 4000         # Max tokens
    permissions: list[AccessLevel] = field(default_factory=lambda: [AccessLevel.PUBLIC, AccessLevel.SHARED])
    include_archived: bool = False
    max_documents: int = 20


@dataclass
class ContextResponse:
    """Response from context assembly."""
    source_of_truth_docs: list[DocumentMetadata]
    current_milestone_docs: list[DocumentMetadata]
    architecture_docs: list[DocumentMetadata]
    supporting_docs: list[DocumentMetadata]
    citations: list[str]
    excluded_files: list[str]
    token_estimate: int
    retrieval_evidence: list[SearchResult]
    assembly_time_ms: float


@dataclass
class CacheEntry:
    """A cached context entry."""
    key: str
    data: dict
    created_at: datetime
    expires_at: Optional[datetime] = None
    hit_count: int = 0

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
