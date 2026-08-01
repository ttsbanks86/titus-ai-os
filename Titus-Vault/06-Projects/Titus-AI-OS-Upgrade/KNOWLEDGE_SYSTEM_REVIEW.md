# Knowledge System Review — Memory Architecture Comparison

**Date:** 2026-07-31
**Reviewed Projects:**
- `hereisSwapnil/memwiki` — Persistent memory protocol for AI agents
- `0jrm/truth` — Local-first, OKF-native memory for AI agents

---

## Executive Summary

Two markdown-based knowledge systems were researched. Both solve "Agent Amnesia" but take different approaches. Our Obsidian vault is already superior in structure but lacks the intelligence layer these projects provide.

**Recommendation: Adopt Truth's hybrid search and memwiki's hot cache pattern. Keep our vault structure.**

---

## Project 1: memwiki

### Architecture
- **Pattern:** Markdown wiki with hook files for AI agents
- **Storage:** `.memory/wiki/` directory with structured markdown files
- **Hooks:** `.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`
- **Protocol:** `AGENTS.md` defines agent behavior

### Key Features
1. **Hot Cache (`hot.md`)** — Recent context, read first
2. **Immutable Sources (`.raw/`)** — Drop PDFs, docs for agent processing
3. **Autonomous Updating** — Agents maintain wiki proactively
4. **Slash Commands** — `/memwiki-ingest`, `/memwiki-lint`, `/memwiki-fold`
5. **Enterprise Scaling** — Dynamic file creation for large projects

### Folder Structure
```
[Project Root]
├── .cursorrules           (Hook for Cursor)
├── .github/copilot-instructions.md (Hook for Copilot)
├── CLAUDE.md              (Hook for Claude Code)
├── AGENTS.md              (The master protocol file)
└── .memory/
    ├── .raw/              (Immutable source documents)
    └── wiki/
        ├── hot.md         (Hot cache: recent context)
        ├── index.md       (Table of contents)
        ├── log.md         (Append-only changelog)
        ├── stack.md       (Tech stack details)
        ├── patterns.md    (Coding patterns)
        ├── bugs.md        (Known issues)
        └── decisions.md   (Architecture Decision Records)
```

### Strengths
- Zero friction setup (one command)
- Universal compatibility (Cursor, Claude, Copilot)
- Autonomous maintenance by agents
- Hot cache for immediate context
- Immutable sources for reference

### Weaknesses
- No vector search
- No semantic retrieval
- Manual file organization
- No embedding-based search
- Limited to text matching

### Adoptable Concepts
1. **Hot Cache Pattern** — Keep immediate context in a single file
2. **Hook Files** — Auto-load context for any AI tool
3. **Autonomous Updating** — Agents maintain their own knowledge
4. **Slash Commands** — Built-in agent operations

---

## Project 2: Truth

### Architecture
- **Pattern:** OKF (Open Knowledge Format) markdown with SQLite index
- **Storage:** `notes/` directory with markdown files
- **Index:** SQLite with vector search (sqlite-vec) and FTS5
- **Search:** Hybrid vector + BM25 + Reciprocal Rank Fusion
- **Embeddings:** Local nomic-embed-text-v1.5 (768-dim)

### Key Features
1. **OKF Format** — YAML frontmatter with type field
2. **Hybrid Search** — Vector + keyword + rank fusion
3. **File Watcher** — Auto-indexes changes in real-time
4. **MCP Server** — Exposes memory_search, memory_write, memory_delete
5. **Browser Inspector** — Visual explorer for notes
6. **Local-first** — All data stays on machine

### Performance
| Operation | Time |
|-----------|------|
| Model cold load | ~2.5s |
| Index warm, unchanged | ~5-7ms |
| Index warm, 12 files | ~107ms |
| Embed 1 doc | ~51-69ms |
| Search k=5 | ~55-68ms |
| Write → Searchable | ~2.2s |

### Strengths
- Hybrid search (vector + keyword)
- Real-time indexing via file watcher
- Local-first privacy
- MCP integration
- Browser inspector for debugging
- OKF standard compliance

### Weaknesses
- Python-only
- Requires embedding model (~550MB)
- SQLite concurrency limits (~8 clients)
- Porter FTS stems English aggressively

### Adoptable Concepts
1. **Hybrid Search** — Vector + keyword for better retrieval
2. **File Watcher** — Auto-index on changes
3. **OKF Format** — Standardized markdown with frontmatter
4. **MCP Integration** — Expose memory as tools
5. **Browser Inspector** — Visual debugging

---

## Our Current System (Titus Vault)

### Architecture
- **Pattern:** Obsidian vault with wiki-links
- **Storage:** 10 top-level directories
- **Index:** Obsidian's built-in search
- **Search:** Text-based (Obsidian search)
- **Links:** Wiki-links `[[Note-Name]]`

### Folder Structure
```
Titus-Vault/
├── 01-Dashboard/          (Home, Goals, Rules)
├── 02-Daily-Notes/        (Daily logs)
├── 03-Archive/            (Archived files)
├── 04-Templates/          (Document templates)
├── 05-Reference/          (Books, courses, papers)
├── 06-Projects/           (Active projects)
├── 07-SOPs/               (Standard operating procedures)
├── 08-Agents/             (Agent profiles)
├── 09-Knowledge/          (Domain knowledge)
└── 10-Business/           (Business documents)
```

### Strengths
- Excellent folder organization
- Wiki-links for cross-referencing
- Rich metadata (YAML frontmatter)
- Obsidian ecosystem (plugins, themes)
- Human-readable and editable

### Weaknesses
- No vector search
- No semantic retrieval
- No auto-indexing
- No MCP integration
- No embedding-based search
- Manual organization required

---

## Comparison Matrix

| Feature | memwiki | Truth | Titus Vault | Winner |
|---------|---------|-------|-------------|--------|
| Setup friction | Zero | Low | None | memwiki |
| Search quality | Text only | Hybrid vector+keyword | Text only | Truth |
| Auto-indexing | None | File watcher | None | Truth |
| MCP integration | None | Yes | None | Truth |
| Privacy | Local | Local | Local | Tie |
| Folder structure | Simple | Simple | Excellent | Titus |
| Wiki-links | No | No | Yes | Titus |
| Hot cache | Yes | No | No | memwiki |
| Autonomous update | Yes | Yes | No | Tie |
| Browser inspector | No | Yes | No | Truth |

---

## Adoption Plan

### Immediate (This Week)

1. **Hot Cache Pattern** (from memwiki)
   - Create `01-Dashboard/Hot-Cache.md`
   - Keep immediate context: current task, next steps, recent decisions
   - Update at end of each session

2. **OKF Frontmatter** (from Truth)
   - Add `type` field to all vault notes
   - Standardize metadata across vault
   - Enable future indexing

3. **Hook Files** (from memwiki)
   - Create agent hook files that auto-load vault context
   - Ensure any AI tool reads vault on startup

### Short-term (Week 2-3)

4. **Hybrid Search** (from Truth)
   - Install sqlite-vec for vector search
   - Create embedding index for vault
   - Implement search-before-answer pattern

5. **File Watcher** (from Truth)
   - Auto-index vault changes
   - Keep search index current
   - Real-time knowledge updates

6. **Slash Commands** (from memwiki)
   - `/vault-ingest` — Scan and index vault
   - `/vault-lint` — Health check vault structure
   - `/vault-fold` — Condense old entries

### Medium-term (Week 4-6)

7. **MCP Integration** (from Truth)
   - Expose vault search as MCP tools
   - Enable external tool access
   - Build agent discovery service

8. **Browser Inspector** (from Truth)
   - Build visual vault explorer
   - Show links, graph, search
   - Debug knowledge structure

---

## Recommended Knowledge Architecture

### Layer 1: Storage (Keep Our Vault)
- Obsidian vault with 10 directories
- Wiki-links for cross-referencing
- YAML frontmatter for metadata
- Human-readable markdown

### Layer 2: Index (Adopt from Truth)
- SQLite with vector embeddings
- FTS5 for keyword search
- Hybrid search (vector + keyword)
- File watcher for auto-updates

### Layer 3: Cache (Adopt from memwiki)
- Hot cache for immediate context
- Session-aware context loading
- Automatic updates at session end

### Layer 4: Access (Adopt from Truth)
- MCP server for tool access
- Search-before-answer pattern
- Write-after-learn pattern
- Slash commands for operations

---

## Implementation Specification

### Hot Cache Template

```markdown
---
type: hot-cache
updated: 2026-07-31T10:00:00Z
---

# Hot Cache

## Current Task
- [What I'm working on right now]

## Next Steps
- [What comes next]

## Recent Decisions
- [Decisions made this session]

## Context
- [Important context for this session]
```

### OKF Frontmatter Standard

```yaml
---
type: note  # note | project | sop | agent | reference | decision
title: "Note Title"
created: 2026-07-31
updated: 2026-07-31
tags: [tag1, tag2]
status: active  # active | archived | draft
---
```

### Search Tool Schema

```json
{
  "name": "vault_search",
  "description": "Search the Titus Vault for notes, projects, SOPs, or knowledge",
  "parameters": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Search query"
      },
      "type": {
        "type": "string",
        "enum": ["note", "project", "sop", "agent", "reference", "decision", "all"],
        "description": "Filter by note type"
      },
      "limit": {
        "type": "integer",
        "default": 10,
        "description": "Max results to return"
      }
    },
    "required": ["query"]
  }
}
```

### Write Tool Schema

```json
{
  "name": "vault_write",
  "description": "Write a note to the Titus Vault",
  "parameters": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Relative path in vault (e.g., '06-Projects/MyProject.md')"
      },
      "content": {
        "type": "string",
        "description": "Note content in markdown"
      },
      "type": {
        "type": "string",
        "enum": ["note", "project", "sop", "agent", "reference", "decision"],
        "description": "Note type"
      },
      "title": {
        "type": "string",
        "description": "Note title"
      }
    },
    "required": ["path", "content", "type", "title"]
  }
}
```

---

## Benefits

1. **Better search quality** — Hybrid vector + keyword finds relevant notes faster
2. **Auto-indexing** — Changes are indexed automatically
3. **Hot cache** — Immediate context always available
4. **MCP integration** — External tools can access vault
5. **Standardized format** — OKF frontmatter enables future features

## Trade-offs

1. **Complexity** — More moving parts to maintain
2. **Storage** — Embedding index requires disk space
3. **Privacy** — Embeddings stay local (good) but require computation
4. **Maintenance** — Index must be kept current

## Migration Effort

- **Hot cache:** 1-2 hours to create template and workflow
- **OKF frontmatter:** 4-6 hours to standardize existing notes
- **Hybrid search:** 8-12 hours to implement
- **File watcher:** 4-6 hours to implement
- **Slash commands:** 4-6 hours to implement
- **MCP integration:** 8-12 hours to implement

**Total estimated effort: 29-44 hours**

## Risks

1. **Index corruption** — SQLite index could become corrupted
2. **Performance** — Embedding model requires CPU/GPU
3. **Complexity** — More code to maintain
4. **Storage growth** — Embedding index grows with vault

## Recommendation

**Adopt incrementally.** Start with hot cache and OKF frontmatter (low effort, high value). Add hybrid search in phase 2. Defer MCP integration until core is solid.

---

## Next Steps

1. Create hot cache template
2. Standardize vault frontmatter
3. Install sqlite-vec and create embedding index
4. Implement hybrid search
5. Create slash commands
6. Build MCP server
