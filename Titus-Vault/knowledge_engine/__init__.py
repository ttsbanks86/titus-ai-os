# knowledge_engine/__init__.py
# Titus AI OS — Knowledge & Context Engine
# Milestone 2: Knowledge retrieval layer for vault-based knowledge

"""
Knowledge & Context Engine for Titus AI OS.

Provides:
- Knowledge inventory and indexing
- Exact, keyword, tag, and project search
- Authority-aware ranking
- Hot context caching
- Context assembly with budget control
- Access model with project isolation
"""

__version__ = "0.1.0"

from .access import AccessControl
from .agents import AgentContextProvider, AgentRole, AgentContextResponse
from .assembler import ContextAssembler
from .cache import HotContextCache
from .config import KnowledgeEngineConfig
from .index import KnowledgeIndex
from .inventory import scan_vault, build_inventory_report
from .models import (
    AccessLevel,
    AuthorityRank,
    CacheEntry,
    ContextRequest,
    ContextResponse,
    DocumentMetadata,
    DocumentType,
    SearchResult,
)
from .search import SearchEngine

__all__ = [
    "AccessControl",
    "AgentContextProvider",
    "AgentRole",
    "AgentContextResponse",
    "ContextAssembler",
    "HotContextCache",
    "KnowledgeEngineConfig",
    "KnowledgeIndex",
    "scan_vault",
    "build_inventory_report",
    "AccessLevel",
    "AuthorityRank",
    "CacheEntry",
    "ContextRequest",
    "ContextResponse",
    "DocumentMetadata",
    "DocumentType",
    "SearchResult",
    "SearchEngine",
]
