# M3 Reuse Decision Record

**Date:** 2026-07-31
**Status:** Complete

---

## Decision Principles

1. **Reuse authoritative assets** — never recreate what already exists
2. **Extend, don't compete** — add to existing systems, don't create parallel versions
3. **Document gaps** — if something is missing, record it, don't invent a replacement
4. **Respect authority order** — Master Brand Standards governs all visual decisions

---

## Reuse Decisions

### Brand Colors

| Decision | Rationale |
|----------|-----------|
| **REUSE** `BRAND/tokens.json` color definitions | Authoritative, machine-readable, comprehensive |
| **REUSE** `BRAND/DESIGN.md` component colors | Implementation-ready, tested |
| **DO NOT** create new color tokens | Master palette is complete |
| **DO NOT** use TitusVideoStudio colors | Sub-brand variant, not master |

### Typography

| Decision | Rationale |
|----------|-----------|
| **REUSE** Inter from DESIGN.md for body/headings | Practical default, already specified |
| **REUSE** JetBrains Mono for code | Already specified in DESIGN.md |
| **DEFER** display font to CEO decision | Master Brand Standards has candidates TBD |
| **DO NOT** pick a display font autonomously | Requires CEO ratification |

### Spacing and Layout

| Decision | Rationale |
|----------|-----------|
| **REUSE** 4px base unit from DESIGN.md | Already specified |
| **REUSE** 12-column grid from DESIGN.md | Already specified |
| **REUSE** breakpoints from DESIGN.md | Already specified |
| **DO NOT** create new spacing tokens | System is complete |

### Components

| Decision | Rationale |
|----------|-----------|
| **REUSE** Button specs from DESIGN.md | Gold primary, Navy secondary, already defined |
| **REUSE** Card specs from DESIGN.md | Cream/White, shadow, radius already defined |
| **REUSE** Form specs from DESIGN.md | Input, focus, error states already defined |
| **REUSE** Navigation specs from DESIGN.md | Desktop horizontal, mobile hamburger already defined |
| **CREATE** Status indicators | Not in DESIGN.md, needed for M3 dashboards |
| **CREATE** Progress indicators | Not in DESIGN.md, needed for M3 milestones |
| **CREATE** Alert components | Not in DESIGN.md, needed for M3 notifications |
| **CREATE** Empty states | Not in DESIGN.md, needed for M3 first-run |
| **CREATE** Loading states | Not in DESIGN.md, needed for M3 async operations |

### States and Motion

| Decision | Rationale |
|----------|-----------|
| **REUSE** Empty/Loading/Error/Success states from DESIGN.md | Already defined |
| **REUSE** Motion specs from DESIGN.md | 200ms default, 300ms transitions, ease-out/in |
| **REUSE** Accessibility rules from DESIGN.md | WCAG 2.1 AA, focus visible, touch targets |

### Voice and Content

| Decision | Rationale |
|----------|-----------|
| **REUSE** Voice anchors from Master Brand Standards | Clear, Direct, Warm, Practical, Grounded |
| **REUSE** Banned words list | No em dashes, no corporate filler |
| **REUSE** Brand Voice Cheatsheet | Comprehensive copy rules |

### Open Design

| Decision | Rationale |
|----------|-----------|
| **REUSE** `BRAND/Open-Design/design-systems/titus-open-door/` | Established package for dashboards |
| **REUSE** open-design.json manifest | Plugin pattern already defined |
| **EXTEND** with Titus AI OS specific views | Dashboard, milestone, agent views |

### Existing Code

| Decision | Rationale |
|----------|-----------|
| **REUSE** M2 Knowledge Engine | 131 tests passing, production-ready |
| **REUSE** M2 Agent Context Provider | CEO, Engineer, QA contexts working |
| **REUSE** M2 Access Control | Project isolation verified |
| **CREATE** Orchestration layer | No existing orchestration code in project |
| **CREATE** Milestone runner | No existing runner code in project |
| **CREATE** Semantic search extension | M2 deferred, no existing implementation |

---

## Gaps Identified

| Gap | Impact | Action |
|-----|--------|--------|
| Display font not selected | Low — Inter works for now | Defer to CEO, note in decisions |
| No component library for status/progress | Medium — needed for dashboards | Create in M3 Phase B |
| No existing orchestration code | High — must build from scratch | Build in M3 Phase F |
| No existing milestone runner | High — must build from scratch | Build in M3 Phase G |
| No semantic search implementation | Medium — M2 deferred | Build in M3 Phase H |
| No auto-indexing implementation | Medium — M2 deferred | Build in M3 Phase I |
