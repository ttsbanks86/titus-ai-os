# M2 Architecture — Knowledge & Context Engine

**Date:** 2026-07-31
**Version:** 1.0
**Status:** Complete

---

## Overview

The Knowledge & Context Engine is the Intelligence Layer (Layer 2) of the Titus AI OS. It provides vault-based knowledge retrieval, search, caching, and role-specific context assembly for agents.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AgentContextProvider                       │
│  CEO / Engineer / QA context loading with role priorities    │
├─────────────┬──────────────┬──────────────┬─────────────────┤
│ SearchEngine│ KnowledgeIndex│ HotContextCache│ AccessControl  │
│  (query)    │  (lookup)    │  (cache)     │ (filter)        │
├─────────────┴──────────────┴──────────────┴─────────────────┤
│                   ContextAssembler                           │
│  (orchestrates search + index + cache + access)              │
├─────────────────────────────────────────────────────────────┤
│                      Inventory                               │
│  (scan_vault → DocumentMetadata list)                        │
├─────────────────────────────────────────────────────────────┤
│                 KnowledgeEngineConfig                        │
│  (all settings, exclusions, paths)                           │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Inventory (`inventory.py`)
- Scans vault recursively
- Parses YAML frontmatter
- Extracts wiki-links
- Computes SHA-256 checksums
- Detects document type, authority, access level
- Saves/loads inventory JSON

### Knowledge Index (`index.py`)
- In-memory index with lookup by path, project, type, authority, tag, keywords
- Incremental update via checksum comparison
- Authority ranking support
- Wiki-link target resolution

### Search Engine (`search.py`)
- Exact, keyword, tag, project, title search
- Authority-aware scoring with recency bonus
- Configurable weights

### Hot Context Cache (`cache.py`)
- LRU with TTL expiration
- Thread-safe (threading.Lock)
- Prefix-based invalidation
- Hit/miss statistics

### Context Assembler (`assembler.py`)
- Assembles context packages from requests
- Token budget enforcement
- Cache-first lookup
- Wiki-link expansion

### Access Control (`access.py`)
- Filters by access level (public < shared < project < restricted < secret)
- Filters by authority rank
- Filters by document type

### Agent Integration (`agents.py`)
- Role-specific context loading (CEO, Engineer, QA)
- Each role receives different ranked context
- Project isolation enforced
- Archived and secret docs excluded

## Data Flow

```
Session Start
    ↓
AgentContextProvider.get_*_context(project, max_tokens)
    ↓
┌─ Cache Hit? → Return cached response
│
└─ Cache Miss:
    ↓
    Index.get_source_of_truth()
    Index.get_governing()
    Search.search(task_queries)
    AccessControl.filter_by_access(PUBLIC)
    ↓
    Deduplicate → Apply Budget → Cache → Return
```

## Authority Hierarchy

| Level | Rank | Examples |
|-------|------|----------|
| SOURCE_OF_TRUTH | 5 | Dashboard docs (Home.md, My-Rules.md) |
| GOVERNING | 4 | SOPs, Agent definitions |
| CURRENT | 3 | Active project docs |
| REFERENCE | 2 | Knowledge base, notes |
| ARCHIVED | 1 | Archive directory |

## Access Levels

| Level | Description |
|-------|-------------|
| PUBLIC | Accessible to all agents |
| SHARED | Accessible to collaborating agents |
| PROJECT | Limited to project members |
| RESTRICTED | Limited to specific roles |
| SECRET | Never returned to agents |

## Performance Baselines

| Operation | Threshold | Measured |
|-----------|-----------|----------|
| Full indexing | <10s | 6.3s |
| Incremental indexing | <10s | 5.9s |
| Keyword search | <100ms avg | 4.3ms |
| Cache hit | <1ms | 0.1ms |
| CEO context assembly | <2s | 20ms |
| Engineer context assembly | <2s | 23ms |
| QA context assembly | <2s | 31ms |
