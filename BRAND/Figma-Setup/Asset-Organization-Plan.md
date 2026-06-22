# Figma Asset Organization Plan

**Owner:** CDO (exec-cdo)
**Status:** Figma Foundation Setup, Step 3 — DRAFT v0.1
**Last updated:** 2026-06-06

The Master Figma file has 13 pages (see `CEO-Playbook.md` Step 3). This document defines how content is organized within and across those pages so the file stays searchable as it grows.

---

## Three-Tier Organization

### Tier 1: Pages (left sidebar)

Already defined in `CEO-Playbook.md` Step 3. 13 pages total. Each page has one job.

### Tier 2: Sections within a page

Within a page, use Figma sections to group related frames. Naming: `NN — Section Name` (e.g., `01 — Hero Compositions`, `02 — Quote Compositions`).

### Tier 3: Frames within a section

Within a section, frames are named with the pattern:
`YYYY-MM-DD — ProjectName — AssetType — Variant`

Example: `2026-06-08 — StruckDown — BookMockup — Hero`

This puts date first for chronological sorting, project second for filtering, and asset details last for clarity.

---

## Tagging System

Figma supports tags via the description field and via Figma libraries. The CDO uses this tag vocabulary:

**By Brand:**
- `titus-banks`
- `faithful-journey-quest`
- `ai-at-work`
- `business-analysis`
- `open-door`
- `built-with-truth`
- `divine-works-hub`

**By Asset Type:**
- `hero`
- `quote`
- `mockup`
- `ad`
- `thumbnail`
- `carousel`
- `landing-page`
- `deck-slide`
- `logo`
- `icon`
- `component`
- `template`

**By Status:**
- `draft`
- `in-review`
- `approved`
- `production-ready`
- `retired`

**By Format:**
- `1080x1080` (Instagram square)
- `1080x1920` (Instagram story)
- `1200x628` (Facebook ad)
- `1200x627` (LinkedIn post)
- `1280x720` (YouTube)
- `1920x1080` (Web hero)
- `6x9` (Book trim)
- `16:9` (Deck)

Every approved frame gets all 4 tag types in its description.

---

## Naming Anti-Patterns (banned)

- `Frame 237` — never accept default names.
- `Hero v2` — use the date-stamped pattern instead.
- `Final Final` — there is no final until it's retired. Use `production-ready` tag.
- `Copy of...` — duplicate the master component, don't copy frames ad-hoc.
- `Untitled` — never.

---

## The Asset Library Page (Page 12)

This is the index page inside Figma. It's a living table of contents for the entire file. The CDO maintains it.

### Layout

A single tall frame with:

| Column | Width | Source |
|--------|-------|--------|
| Asset name | 30% | Figma frame name |
| Type | 15% | Figma tag |
| Brand | 15% | Figma tag |
| Status | 10% | Figma tag |
| Last updated | 15% | Figma modification date |
| Link to frame | 15% | Figma frame link |

The CDO updates this table whenever a new asset is approved.

### Maintenance

- Updated: after every checkpoint (Phase 1, 2, 3).
- Reviewed: monthly.
- Archived entries move to the Archive page (Page 13) with `RETIRED — YYYY-MM-DD — reason` prepended to the name.

---

## The Archive Page (Page 13)

Stores:

- Retired components (replaced by new variants).
- Old versions of approved assets (only kept for audit/history, max 1 prior version per asset).
- Designs from past projects that may be relevant for future re-use.

Naming: `RETIRED — YYYY-MM — OriginalName — RetiredReason`

The Archive page is read-only. No editing. If something needs to come back, the CDO copies it to a working page and gives it a new name with today's date.

---

## File Versioning

The Master file uses Figma's native version history. No manual backups needed.

However, the CDO will:

- Snapshot the file once per quarter (export to local PDF, save to `BRAND/Snapshots/`).
- Snapshot before any major restructuring.
- Never save a snapshot with the same name twice (append date and version).

---

## Cross-References

- `BRAND/Asset-Library-Index.md` — the on-disk library index. Stays in sync with this Figma file.
- `BRAND/Figma-Setup/CEO-Playbook.md` — the setup steps.
- `BRAND/Figma-Setup/Component-Library-Spec.md` — what components to build.
- `BRAND/Figma-Setup/Templates-Spec.md` — what templates to build.
