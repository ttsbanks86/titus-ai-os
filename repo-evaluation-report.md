# Open-Source Repo Evaluation for a Faith-Based Content Creation Business

**Scope:** 10 candidate repos (9 named + 1 group of creator-adjacent repos) for use in a faith-based content creation business — devotionals, sermon prep, faith-based courses, ebooks, social content, and possibly Christian publishing.

**Method:** Real GitHub data gathered via web search on 2026-06-05. Star counts and stats are scraped from search snippets; some drift is possible. Items I could not verify directly are flagged in-line.

---

## Executive Summary

### Install This Week (Top 3)
1. **thedotmack/claude-mem** — Persistent memory layer for Claude Code. Most "must-have" piece. Faith-content work is *always* multi-session (sermon series, books, course modules). claude-mem gives you continuity, context recovery, and ~10x token savings. Zero infra.
2. **czlonkowski/n8n-mcp** — Exposes 525+ n8n workflow nodes to your AI. This is the automation spine: schedule social posts to faith platforms, drip email devotionals, pipe YouTube transcripts into research notes, auto-format Substack drafts. Requires n8n hosting (free tier or self-host) but pays back fast.
3. **open-gsd/gsd-core** (or `get-shit-done-cc` on npm) — Spec-driven project execution. Faith-content projects (a 30-day devotional, an 8-week study) need scoping, milestone tracking, and verification. GSD turns fuzzy goals into shipped artifacts. Used at Amazon/Google/Shopify.

### Monitor (Q3 — install when one specific pain point appears)
- **HKUDS/LightRAG** — when you need scripture/theology-aware retrieval across a personal library.
- **kepano/obsidian-skills** — if/when you move sermon prep and study notes into Obsidian.
- **nextlevelbuilder/ui-ux-pro-max-skill** — when social/ebook design output becomes a bottleneck.

### Skip (or use as reference, not install)
- **hesreallyhim/awesome-claude-code** — a curated *list*, not a tool. Bookmark it; don't install.
- **affaan-m/everything-claude-code** — 168K-star mega-bundle with 28 subagents, 119 skills, 60 commands. *Too much* for a small content business; pick what you need from the list rather than the whole bundle. The AgentShield security subagent is the one piece worth lifting.
- **obra/superpowers** — 218K stars and powerful, but the meta-skill framework adds friction for a non-dev creator. Revisit when you have a developer or when solo-agent ceiling becomes the bottleneck.
- **obra/the-elements-of-style + obra/private-journal-mcp** — niche; the writing-quality guidance overlaps with what GSD and a focused editing skill already cover; the journaling MCP only matters if you want a Strunk-style journal workflow.

---

## Per-Repo Profiles

### 1. thedotmack/claude-mem
A persistent memory layer for Claude Code that captures, indexes, and retrieves past session context. Built on Chroma (vector DB) with a 3-layer workflow: `search()` returns an index of relevant observations; `timeline(anchor=ID)` gives context around a hit; `get_observations([IDs])` returns full details on demand. This tiered fetch is what produces the ~10x token savings vs. dumping full transcripts.
- **Install:** `npx claude-mem` or `bunx claude-mem`. Zero infra.
- **Hardware:** trivial — runs locally, Chroma embedded.
- **Maintenance:** low. Auto-prunes; Chroma is self-contained.
- **Security:** local-first; verify the no-telemetry claim on the repo's README before relying on it for confidential sermon drafts.
- **Popularity:** ~65K–80K stars (numbers vary across scrapers). Apache-2.0.
- **Long-term:** very high. Solves a problem that doesn't go away.
- **Faith fit:** excellent. Sermon series, multi-book projects, recurring courses — *all* benefit from cross-session memory.

### 2. czlonkowski/n8n-mcp
An MCP server that exposes n8n's 525+ nodes (Slack, Gmail, YouTube, WordPress, Substack, Notion, Airtable, etc.) to any MCP-compatible client. Comes with a hosted free tier (100 calls/day) plus a self-hosted `npx n8n-mcp` option.
- **Install:** npx, or point at the hosted endpoint.
- **Hardware:** none locally; the *n8n* instance itself needs a small VPS or Docker container if you self-host workflows.
- **Maintenance:** low for the MCP; medium for the n8n workflows you build on top.
- **Security:** OAuth handled by n8n credentials; keep workflow credentials in n8n's encrypted store, not in your prompts.
- **Popularity:** ~10K–21.5K stars. MIT.
- **Long-term:** high. n8n itself is a stable, well-funded OSS platform.
- **Faith fit:** strong. Schedule devotionals to Substack/WordPress, drip email series via Gmail/Mailchimp nodes, ingest YouTube sermons for transcription/quote extraction.

### 3. HKUDS/LightRAG
Graph-augmented RAG from the HKU Data Science lab. Published at EMNLP 2025; arXiv:2410.05779. Combines vector retrieval with a knowledge graph so you can ask "where does Paul quote Isaiah in Romans?" and get *connected* answers across a personal theology library.
- **Install:** `pip install lightrag`; needs an LLM API key and (optionally) a graph/vector backend.
- **Hardware:** medium. Python service; can run on a laptop for personal-scale libraries; recommend a small VPS for anything > 1k documents.
- **Maintenance:** medium. Embedding re-indexes when your library changes.
- **Security:** data lives where you put it; pick a self-hosted LLM endpoint if doctrine-sensitive.
- **Popularity:** ~36K stars, 282 contributors, +37 stars in the past week. Active.
- **Long-term:** very high. EMNLP publication and active academic backing.
- **Faith fit:** *the* killer app here is scripture cross-referencing + commentary retrieval. The graph layer is exactly what theological study wants.

### 4. hesreallyhim/awesome-claude-code
A curated list of Claude Code resources, skills, and tools. ~44K stars, ~3.7K forks.
- **Install:** none — it's a markdown list.
- **Hardware:** none.
- **Maintenance:** none.
- **Security:** n/a.
- **Long-term:** medium. Lists age fast; treat as a discovery surface, not a tool.
- **Faith fit:** indirect. Use it to find the next tool, not as a tool itself.

### 5. nextlevelbuilder/ui-ux-pro-max-skill
A Claude Code skill that injects 50+ design styles, 97 color palettes, 57 font pairings, 99 UX guidelines, and 25 chart types into your prompts. Install via `npx claude-code-templates@latest --skill creative-design/ui-ux-pro-max`.
- **Install:** npx, one command.
- **Hardware:** none.
- **Maintenance:** low. Updated styles/guidelines land via the registry.
- **Security:** prompt-content only; no data egress.
- **Popularity:** ~87K stars — outsized for a single skill.
- **Long-term:** high. Style guides don't age fast.
- **Faith fit:** strong if you produce visual content (social cards, ebook layouts, course slides). Less useful if you only write.

### 6. obra/superpowers
A composable skill framework for AI coding agents (Claude Code, Codex, Cursor, Gemini, OpenCode). 218K stars, MIT, 441 commits, written in JavaScript. Adds a meta-layer for spawning, monitoring, and routing between specialized sub-agents.
- **Install:** per-agent hookup; framework-y.
- **Hardware:** none locally; underlying model costs scale with sub-agent fan-out.
- **Maintenance:** medium. Framework updates can break skills.
- **Security:** review any sub-agent that touches credentials.
- **Long-term:** high; well-maintained.
- **Faith fit:** medium. Powerful but a power-user tool. Worth it once you hit a "one agent can't do it all" wall — typical for, say, a multi-format content pipeline (write → design → schedule → translate).

### 7. affaan-m/everything-claude-code
A mega-bundle: 28 subagents, 119 skills, 60 slash commands, plus AgentShield (security scanner). 168K stars, 26K forks.
- **Install:** clone the repo into your Claude config dir.
- **Hardware:** none.
- **Maintenance:** *high*. With 119 skills and 28 agents, you'll burn time configuring, debugging conflicts, and pruning what you don't use.
- **Security:** AgentShield is the standout — but the bundle's breadth means you must audit what you're enabling.
- **Long-term:** medium. A bundle this large drifts unless you treat it as a *menu* and pick 5–10 items, not the whole thing.
- **Faith fit:** low-medium. Too much surface area for a solo content creator.

### 8. kepano/obsidian-skills
The official skill pack from Obsidian's CEO (Steph Ango). Five skills: Markdown, Bases, JSON Canvas, CLI, Defuddle. MIT. ~14K–34K stars.
- **Install:** drop into `.claude/skills/`.
- **Hardware:** none.
- **Maintenance:** low; Obsidian itself is stable.
- **Security:** local-first; no telemetry.
- **Long-term:** high. Made by the people who make Obsidian.
- **Faith fit:** conditional. Only valuable if you actually use Obsidian for sermon prep / study notes. If yes, these skills make the vault AI-native.

### 9. open-gsd/gsd-core (npm: `get-shit-done-cc`)
Spec-driven project execution. You describe a goal, GSD scopes it, plans it, executes it in phases, and verifies each phase before moving on. Created by Lex Christopherson (glittercowboy); used at Amazon, Google, Shopify. ~23K–31K stars, MIT, Node 18+/22+.
- **Install:** `npx get-shit-done-cc` (or install from `open-gsd/gsd-core`).
- **Hardware:** none.
- **Maintenance:** low.
- **Security:** spec/plan files in your repo; review before approving destructive actions.
- **Long-term:** high. Project-execution pattern is a durable need.
- **Faith fit:** *excellent.* A 30-day devotional, an 8-week Bible study, a book manuscript — all map cleanly to GSD's phase/verify loop.

### 10. obra adjacent: the-elements-of-style + private-journal-mcp
Two small repos from the same author as Superpowers:
- **the-elements-of-style** — a Claude skill that injects Strunk's writing guidance into prose output. Niche; the "omit needless words" rule is useful, but most of this duplicates what a good editor prompt already does.
- **private-journal-mcp** — a journaling MCP server with semantic search. Useful only if journaling is part of your content pipeline (e.g., daily pastor's journal → weekly reflection post).
- **Combined score:** moderate. Install `the-elements-of-style` if your prose quality is a real bottleneck; skip `private-journal-mcp` unless journaling is core.

---

## 10×5 Scoring Matrix

Scores 1–10. **BV** = business value, **PV** = productivity value, **AV** = automation value, **EI** = ease of implementation, **LT** = long-term usefulness. Total out of 50.

| Repo | BV | PV | AV | EI | LT | Total |
|---|---|---|---|---|---|---|
| thedotmack/claude-mem | 9 | 8 | 6 | 9 | 9 | **41** |
| czlonkowski/n8n-mcp | 8 | 7 | 10 | 5 | 8 | **38** |
| open-gsd/gsd-core | 8 | 9 | 5 | 6 | 8 | **36** |
| obra/superpowers | 7 | 8 | 7 | 6 | 8 | **36** |
| HKUDS/LightRAG | 9 | 8 | 5 | 4 | 9 | **35** |
| nextlevelbuilder/ui-ux-pro-max-skill | 8 | 8 | 4 | 8 | 7 | **35** |
| affaan-m/everything-claude-code | 7 | 8 | 7 | 6 | 7 | **35** |
| kepano/obsidian-skills | 7 | 7 | 4 | 9 | 8 | **35** |
| obra adjacent (the-elements-of-style + private-journal-mcp) | 7 | 7 | 4 | 7 | 7 | **32** |
| hesreallyhim/awesome-claude-code | 3 | 4 | 2 | 10 | 5 | **24** |

---

## Implementation Priority

| Week | Action | Why |
|---|---|---|
| 1 | Install **claude-mem** | Zero cost, immediate ROI on any multi-session project. |
| 1 | Install **GSD** (`get-shit-done-cc`) | Use it to scope your next content project. |
| 2 | Set up **n8n-mcp** (start with hosted free tier) | Wire one workflow: post a draft to Substack/WordPress. |
| 3 | Add **ui-ux-pro-max-skill** | Use for the next round of social cards or an ebook cover. |
| 4 | Audit **everything-claude-code** for 3–5 specific items you actually need | Don't install the bundle wholesale. Lift AgentShield first. |
| 5+ | Adopt **LightRAG** when you have a real library to query | Don't pre-build infrastructure you don't yet need. |
| 5+ | Adopt **obsidian-skills** *if* you're already in Obsidian | Conditional on existing workflow. |
| 5+ | Revisit **Superpowers** when sub-agent ceiling becomes a real constraint | Framework tax is real; pay it only when it pays you. |

---

## Final Recommendation

**Install this week, in this order:**

1. **claude-mem** — the single highest-ROI piece of infrastructure for any multi-session content business. It will quietly save you hours of re-explaining context for the rest of the project's life.
2. **GSD (`get-shit-done-cc`)** — use it to plan the next sermon series, book, or course. The discipline of "spec → phase → verify" is what separates a content business from a content hobby.
3. **n8n-mcp** — start with the hosted free tier, wire one workflow end-to-end (e.g., "draft devotional in Notion → publish to Substack → announce in Slack/Discord"), then expand.

Everything else is *deferrable*. Bookmark awesome-claude-code, browse everything-claude-code for inspiration, but don't install what you can't yet name a use for.

---

## Data Notes & Flags

- **Star counts** above are scraped from search-result snippets at one point in time. Live GitHub numbers may differ by 5–15% (especially for fast-growing repos like claude-mem and ui-ux-pro-max-skill).
- **claude-mem "no telemetry" claim** is from the README — verify on the repo before relying on it for confidential content.
- **LightRAG hardware** is estimated; I did not find a published minimum spec. Treat as "Python service, runs on a modern laptop for personal use."
- **affaan-m/everything-claude-code** exact subagent/skill counts (28/119/60) come from one source snippet; counts change frequently.
- **obra/private-journal-mcp and the-elements-of-style** star counts and maturity were not surfaced in search; treat as low-traffic side projects rather than flagship tools.
- **No faith-tuned forks** of any of these repos surfaced in search. If one exists, it's niche; verify on GitHub before assuming.
