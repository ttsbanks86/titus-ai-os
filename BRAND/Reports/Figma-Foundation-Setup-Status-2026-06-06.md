# Figma Foundation Setup — Status Report

**Date:** 2026-06-06
**Owner:** CDO (exec-cdo) for delivery; CEO (Titus Banks) for execution
**Status:** SPECS COMPLETE, CEO EXECUTION PENDING
**Authority:** CEO approved Figma Foundation Setup 2026-06-06

---

## Honest Constraint Disclosure

**The CDO cannot perform Figma drag-and-drop actions.** Figma is a browser/desktop GUI tool that requires the CEO's Figma account and active session. The CDO's role is to deliver:

1. The file structure (pages, layout, naming)
2. The component specifications (Phases 1, 2, 3)
3. The template inventory
4. The asset organization plan
5. The token values (in `BRAND/tokens.json` — done in QW3)
6. The copy-paste variable cheat sheet (created today)
7. The CEO's session checklist (created today)
8. The CEO's report-back template (created today)

The CEO performs Steps 1-6 of the CEO Playbook in a 60-90 minute Figma session.

**This is the same constraint as before.** Nothing has changed. The CDO is the spec deliverer; the CEO is the human hands.

---

## What the CDO Delivered Today (2026-06-06)

### 1. Figma-CEO-Action-Package.md (NEW)

A single, ready-to-execute bundle at `BRAND\Figma-Setup\Figma-CEO-Action-Package.md` that contains:

- **Variable Cheat Sheet** — copy-paste list of all 22 Figma variables (9 color + 9 space + 4 radius) with exact names and values matching `BRAND/tokens.json`
- **CEO Session Checklist** — print-friendly or phone-friendly checklist for the 60-90 min Figma session, broken into 6 steps with time budgets
- **CEO Report-Back Template** — structured reply template for the CEO to report completion back to the CDO

### 2. Consolidated Figma Setup Folder

All Figma-related docs in one place (`BRAND\Figma-Setup\`):

| File | Status | Purpose |
|------|--------|---------|
| `CEO-Playbook.md` | EXISTING | 6-step Figma setup walkthrough |
| `Component-Library-Spec.md` | EXISTING | 56-component blueprint (30 Phase 1, 18 Phase 2, 8 Phase 3) |
| `Templates-Spec.md` | EXISTING | 8 template inventory with Empty/Populated/Annotated states |
| `Asset-Organization-Plan.md` | EXISTING | Naming, tagging, archive, indexing rules |
| `Figma-CEO-Action-Package.md` | NEW (2026-06-06) | CEO cheat sheet + session checklist + report-back template |

### 3. Total Asset Spec for Figma

| Category | Count | Notes |
|----------|-------|-------|
| Pages | 13 | Cover, Brand Tokens, Components, Templates, 4x social channels, Web, Book, Decks, Asset Library, Archive |
| Color variables | 9 | All locked in `BRAND/tokens.json` |
| Spacing variables | 9 | All locked in `BRAND/tokens.json` |
| Radius variables | 4 | All locked in `BRAND/tokens.json` |
| Phase 1 components | 30 | Buttons, cards, headings, logos, icons |
| Phase 2 components | 18 | Navigation, forms, content blocks |
| Phase 3 templates | 8 | Landing page, IG post, IG story, FB ad, YouTube thumb, pitch deck, LinkedIn carousel, book sales |
| **Total components + templates** | **56** | Built in 3 phases over multiple CEO sessions |

---

## What the CEO Will Do (60-90 min Figma session)

Following the CEO-Playbook.md and Figma-CEO-Action-Package.md:

### Pre-Session (5 min)
- Sign in to Figma.com
- Open the Action Package in a second tab
- Set workspace name to "Titus Banks Studio"

### Step 1 — Master Brand File (5 min)
- Create "Design file" named `Titus Banks — Master Brand System`
- Set cover image to the approved book 3D mockup

### Step 2 — Page Architecture (10 min)
- Create 13 pages per the spec (Cover, Brand Tokens, Components, Templates, Web, IG, FB, LinkedIn, YouTube, Book Assets, Decks, Asset Library, Archive)

### Step 3 — Variables (15-20 min)
- Create 3 collections (color / space / radius) with 22 variables total
- Use the Variable Cheat Sheet for exact names and values

### Step 4 — First Component (Button) (20-30 min)
- Build the seed `Button / Primary / Default` component
- Create 5 more variants (Hover, Disabled, Secondary Default, Secondary Hover, Ghost Default)
- This is the only component built today; the rest grow over time

### Step 5 — Publish to Library (5 min)
- Toggle "Publish styles and components" on for the Button / * components
- This allows future Titus Banks Figma files to link to these components

### Step 6 — Report Back (5 min)
- Copy the Figma file URL
- Take a screenshot of the Button / Primary component
- Reply using the CEO Report-Back Template

**Total CEO time: 60-90 minutes first session, 20-30 min future sessions.**

---

## Figma CEO Action Package Time Estimates

| Step | First-time Figma user | Experienced Figma user |
|------|----------------------|------------------------|
| Pre-Session | 5 min | 5 min |
| Step 1 (File creation) | 5 min | 2 min |
| Step 2 (Pages) | 10 min | 5 min |
| Step 3 (Variables) | 20 min | 10 min |
| Step 4 (Button component) | 30 min | 15 min |
| Step 5 (Publish) | 5 min | 3 min |
| Step 6 (Report back) | 5 min | 5 min |
| **TOTAL** | **80 min** | **45 min** |

Realistic estimate: **60-90 minutes for first-time Figma user** (matches the existing CEO-Playbook estimate).

---

## What CDO Will Do After CEO Completes the Session

1. **Review the Figma file** (screenshot or live URL).
2. **Update `BRAND/Asset-Library-Index.md`** with the Figma file URL.
3. **Begin Phase 1 component expansion** — submit the next batch of 24 components (Phase 1 minus the 6 buttons just built) for CEO build.
4. **Reference the Figma file** in the Master Brand System v0.2 (after current v0.1 ratification).
5. **Update `BRAND/Figma-Setup/CEO-Playbook.md`** with any lessons learned from the first session.

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Figma learning curve for first-time user | CDO is patient. First session may take 90 min. Future sessions faster. |
| Token drift if CEO hard-codes values | Step 3 (Variables) MUST come before Step 4 (Components). Session Checklist enforces the order. |
| File proliferation | Single Master file only. CDO will reject any "Titus Banks v2.fg" duplicates. |
| Figma API not in OpenCode | Not needed yet. Can add later if CDO programmatic access becomes valuable. |
| CEO runs out of time mid-session | The Action Package is modular. CEO can stop after Step 3 (Variables) and resume Step 4 (Components) in a future session. |

---

## Cost & Tier

- **Figma free tier**: 3 files per workspace, unlimited editors on a team. Sufficient for single-CEO design studio.
- **Figma Professional**: $15/month per editor. Only needed for multi-editor collaboration or API access. **NOT YET NEEDED.**
- **Recommendation:** Stay on free tier until a clear need (multi-editor collaboration or design system expansion beyond 1 user) appears.

---

## Status: READY FOR CEO EXECUTION

All CDO deliverables for the Figma Foundation Setup are in place. The CEO has everything needed to execute the 60-90 min session independently. No further CDO action on Figma is required until the CEO reports back.

**Next action:** CEO schedules the Figma session and runs the 6-step checklist.

---

**Last updated:** 2026-06-06
**Owner:** CDO (exec-cdo)
**Next action:** CEO schedules 60-90 min Figma session
