# Master Notes Plan

**Date:** 2026-06-21
**Purpose:** Define every master note, its contents, and its wiki-link architecture.

---

## What Is a Master Note?

A master note is the single entry point for any major area of the Titus AI OS. OpenCode does not need to scan directories or guess where information lives. It opens the master note and follows wiki-links.

Every master note follows a consistent structure:
1. **Overview** — one paragraph summary
2. **Current State** — where things stand right now
3. **Goals** — what we are trying to achieve
4. **Linked Notes** — wiki-links to all related content
5. **Active Tasks** — what is being worked on right now
6. **Decisions Made** — key decisions with dates
7. **References** — links to SOPs, templates, external resources

---

## Master Note Inventory

### Tier 1: Dashboard (Vault Entry Point)

| Master Note | Location | Purpose |
|---|---|---|
| [[Home]] | `01-Dashboard/Home.md` | Vault index. Links to every Tier 2 master note. First note OpenCode reads. |
| [[Personal-Context]] | `01-Dashboard/Personal-Context.md` | Who Titus is, family, location, story. |
| [[My-Rules]] | `01-Dashboard/My-Rules.md` | How OpenCode should operate. What to do and never do. |
| [[My-Goals]] | `01-Dashboard/My-Goals.md` | Financial, career, family, ministry, and legacy goals. |
| [[My-Voice]] | `01-Dashboard/My-Voice.md` | Writing and speaking voice definition. |

### Tier 2: Businesses

| Master Note | Location | Purpose |
|---|---|---|
| [[Businesses]] | `03-Businesses/Businesses.md` | Master index of all active and planned businesses. |
| [[CareNotes-Pro]] | `03-Businesses/CareNotes-Pro.md` | The healthcare documentation platform. |
| [[Business-Ideas]] | `03-Businesses/Business-Ideas.md` | Active ideas under evaluation. |
| [[Legacy-Businesses]] | `03-Businesses/Legacy-Businesses.md` | Archived business ventures for reference. |

### Tier 2: Products

| Master Note | Location | Purpose |
|---|---|---|
| [[Products]] | `04-Products/Products.md` | Master index of all products and tools. |
| [[Personal-AI-Operator]] | `04-Products/Personal-AI-Operator.md` | Desktop AI assistant system. |
| [[Content-Income-System]] | `04-Products/Content-Income-System.md` | Content monetization pipeline. |
| [[EchoKeys]] | `04-Products/EchoKeys.md` | Voice dictation tool. |
| [[NOLA-Voice]] | `04-Products/NOLA-Voice.md` | Voice assistant for desktop control. |
| [[Whisper-Pro]] | `04-Products/Whisper-Pro.md` | Speech recognition and transcription. |
| [[Floating-AI-Tutor]] | `04-Products/Floating-AI-Tutor.md` | Desktop overlay AI tutor. |
| [[DocFlow]] | `04-Products/DocFlow.md` | Document automation pipeline. |
| [[Hermes-Gateway]] | `04-Products/Hermes-Gateway.md` | API gateway and model router. |

### Tier 2: Career

| Master Note | Location | Purpose |
|---|---|---|
| [[Career]] | `05-Career/Career.md` | Master index of career development. |
| [[Job-Search]] | `05-Career/Job-Search.md` | Active job applications, status tracking. |
| [[Resume]] | `05-Career/Resume.md` | Resume versions, strategy, tailoring rules. |
| [[LinkedIn-Strategy]] | `05-Career/LinkedIn-Strategy.md` | Profile optimization, outreach, content. |
| [[Portfolio]] | `05-Career/Portfolio.md` | PM portfolio projects and development. |
| [[Certifications]] | `05-Career/Certifications.md` | Completed and planned certifications. |
| [[Education]] | `05-Career/Education.md` | Degrees, coursework, continuing education. |
| [[Business-Analyst-Path]] | `05-Career/Business-Analyst-Path.md` | BA career development roadmap. |

### Tier 2: Projects

| Master Note | Location | Purpose |
|---|---|---|
| [[Projects]] | `06-Projects/Projects.md` | Master index of all active projects. |
| [[AeroCardia]] | `06-Projects/AeroCardia.md` | Riipen micro-internship market entry project. |
| [[Bonolo-Book-Marketing]] | `06-Projects/Bonolo-Book-Marketing.md` | Book marketing for Bonolo's two books. |
| [[PM-Portfolio]] | `06-Projects/PM-Portfolio.md` | Building PM portfolio for career transition. |
| [[Ministry-Return]] | `06-Projects/Ministry-Return.md` | Planning the return to independent ministry. |
| [[Local-Business-AI-Services]] | `06-Projects/Local-Business-AI-Services.md` | AI services for local businesses. |

### Tier 2: Knowledge Domains

| Master Note | Location | Purpose |
|---|---|---|
| [[Knowledge-Index]] | `09-Knowledge/Knowledge-Index.md` | Master index of all knowledge areas. |
| [[OpenCode-Config]] | `09-Knowledge/AI-Systems/OpenCode-Config.md` | OpenCode configuration, providers, agents. |
| [[Model-Routing]] | `09-Knowledge/AI-Systems/Model-Routing.md` | Which model for which task. Routing rules. |
| [[API-Keys]] | `09-Knowledge/AI-Systems/API-Keys.md` | Key inventory. No values. Just inventory. |
| [[Provider-Architecture]] | `09-Knowledge/AI-Systems/Provider-Architecture.md` | How providers connect. Fallback chains. |
| [[Brand-Voice]] | `09-Knowledge/Brand/Brand-Voice.md` | Voice, tone, messaging rules. |
| [[Brand-Assets]] | `09-Knowledge/Brand/Brand-Assets.md` | Logos, colors, fonts, design tokens. |
| [[Content-Guidelines]] | `09-Knowledge/Brand/Content-Guidelines.md` | Platform-specific content rules. |
| [[Marketing-Strategy]] | `09-Knowledge/Marketing/Marketing-Strategy.md` | Overall marketing approach and channels. |
| [[Content-Strategy]] | `09-Knowledge/Marketing/Content-Strategy.md` | Content marketing plan and calendar. |
| [[Growth-Engineering]] | `09-Knowledge/Marketing/Growth-Engineering.md` | Growth tactics, experiments, metrics. |
| [[Tech-Stack]] | `09-Knowledge/Technology/Tech-Stack.md` | Current technology choices. |
| [[Infrastructure]] | `09-Knowledge/Technology/Infrastructure.md` | Hosting, servers, deployment details. |
| [[Tools-Reference]] | `09-Knowledge/Technology/Tools-Reference.md` | Tools, subscriptions, licenses. |
| [[Budget]] | `09-Knowledge/Finance/Budget.md` | Current financial snapshot. |
| [[Income-Streams]] | `09-Knowledge/Finance/Income-Streams.md` | Active and planned income sources. |
| [[Tax-Reference]] | `09-Knowledge/Finance/Tax-Reference.md` | Tax-related information and deadlines. |

---

## Wiki-Link Architecture

### How Links Flow

```
Home.md
├── [[Personal-Context]]
├── [[My-Rules]]
├── [[My-Goals]]
├── [[My-Voice]]
├── [[Businesses]] → [[CareNotes-Pro]] → [[CareNotes-Features]], [[CareNotes-Roadmap]], [[CareNotes-Marketing]]
├── [[Products]] → [[Personal-AI-Operator]] → [[PAIO-Architecture]], [[PAIO-Roadmap]]
├── [[Career]] → [[Job-Search]] → [[Job-Applications]], [[Job-Interviews]]
├── [[Projects]] → [[AeroCardia]] → [[AeroCardia-Research]], [[AeroCardia-Deliverables]]
├── [[SOPs-Index]] → [[Job-Application-SOP]], [[LinkedIn-Outreach-SOP]]
├── [[Agents-Index]] → [[CEO-Agent]], [[Engineer-Agent]], [[Research-Agent]]
└── [[Knowledge-Index]] → [[Brand-Voice]], [[Tech-Stack]], [[Budget]]
```

### Rules for Links

1. **Every master note links back to its parent index.** [[CareNotes-Pro]] links to [[Businesses]]. [[Businesses]] links to [[Home]].
2. **Supporting notes link to their master note.** [[CareNotes-Features]] links to [[CareNotes-Pro]].
3. **Cross-domain links are explicit.** If [[Job-Search]] references a marketing strategy, it links to [[Marketing-Strategy]].
4. **No orphan notes.** Every note must be reachable from [[Home]] within 3 hops.
5. **No circular chains that trap retrieval.** A → B → C → A is prohibited.

---

## Example Master Note: [[CareNotes-Pro]]

```markdown
# CareNotes Pro

## Overview
CareNotes Pro is a healthcare documentation platform that [description].

## Current State
- Phase: Planning / Development / Launched / Maintenance
- Last updated: 2026-06-21
- Active team: [if applicable]

## Goals
- Short-term (30 days):
- Medium-term (90 days):
- Long-term (12 months):

## Linked Notes
- [[CareNotes-Features]]
- [[CareNotes-Roadmap]]
- [[CareNotes-Pricing]]
- [[CareNotes-Marketing]]
- [[CareNotes-Architecture]]
- [[CareNotes-Development]]

## Active Tasks
- [ ] Task 1
- [ ] Task 2

## Decisions Made
- 2026-06-15: Decision description

## References
- [[Healthcare-SaaS-SOP]]
- [[Product-Launch-SOP]]
```

Every master note follows this exact structure. No exceptions.

---

## Total Master Notes: 35

| Tier | Count |
|---|---|
| Tier 1 (Dashboard) | 5 |
| Tier 2 (Businesses) | 4 |
| Tier 2 (Products) | 9 |
| Tier 2 (Career) | 8 |
| Tier 2 (Projects) | 6 |
| Tier 2 (Knowledge) | 17+ |
| Index notes (Agents, SOPs, Templates, Archive, Reference) | 5 |
| **Total master notes** | **54** |

Plus supporting sub-notes linked from each master note (estimated 100-150 additional notes).

---

This plan defines the complete master note architecture. Every note, every link, every structure is specified here. The actual note creation happens during Phase 2 of migration.
