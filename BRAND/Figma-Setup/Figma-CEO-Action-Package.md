# Figma Foundation Setup — CEO Action Package

**Owner:** CDO (exec-cdo) for delivery; CEO (Titus Banks) for execution
**Status:** v0.1 — 2026-06-06
**Purpose:** Bundle every document, cheat sheet, checklist, and reporting template the CEO needs to execute the Figma Foundation Setup in one focused 60-90 minute session.

---

## What's In This Package

| File | Purpose | Already in folder? |
|------|---------|---------------------|
| `CEO-Playbook.md` | The 6-step Figma setup walkthrough | YES |
| `Component-Library-Spec.md` | Full 56-component blueprint (30 Phase 1, 18 Phase 2, 8 Phase 3) | YES |
| `Templates-Spec.md` | 8 template inventory with Empty/Populated/Annotated states | YES |
| `Asset-Organization-Plan.md` | Naming, tagging, archive, indexing rules | YES |
| `BRAND/tokens.json` | Machine-readable design tokens | YES |
| `BRAND/tokens.css` | Web implementation of tokens | YES |
| **NEW** `Variable-Cheat-Sheet.md` | Copy-paste list of all 22 Figma variables | NO (created today) |
| **NEW** `CEO-Session-Checklist.md` | Print-friendly checklist for the 60-90 min Figma session | NO (created today) |
| **NEW** `CEO-Report-Back-Template.md` | Structured reply template for after the session | NO (created today) |

---

## Figma CEO Action Package — Variable Cheat Sheet

Copy this list directly into Figma Variables. Names and values match `BRAND/tokens.json` exactly.

### Color Variables (9 total)

Create a Collection called `color`. For each variable, set the Type to `Color` and Mode to the default.

| Variable name | Value | Type |
|---------------|-------|------|
| `navy` | `#0F2742` | color |
| `navy-deep` | `#0A1B30` | color |
| `gold` | `#D4A14A` | color |
| `gold-soft` | `#E8C98A` | color |
| `green-success` | `#1F6B4A` | color |
| `slate` | `#5A6B7B` | color |
| `cream` | `#F5F1E8` | color |
| `white` | `#FFFFFF` | color |
| `off-black` | `#0E1116` | color |

### Spacing Variables (9 total)

Create a Collection called `space`. For each variable, set the Type to `Number`.

| Variable name | Value | Type |
|---------------|-------|------|
| `space-xxs` | `4` | number |
| `space-xs` | `8` | number |
| `space-sm` | `12` | number |
| `space-md` | `16` | number |
| `space-lg` | `24` | number |
| `space-xl` | `32` | number |
| `space-2xl` | `48` | number |
| `space-3xl` | `64` | number |
| `space-4xl` | `96` | number |

### Radius Variables (4 total)

Create a Collection called `radius`. For each variable, set the Type to `Number`.

| Variable name | Value | Type |
|---------------|-------|------|
| `radius-sm` | `4` | number |
| `radius-md` | `8` | number |
| `radius-lg` | `16` | number |
| `radius-pill` | `9999` | number |

**Total: 22 variables across 3 collections.** All values match `BRAND/tokens.json` exactly. If a value is updated in `tokens.json` later, the Figma variable will not auto-sync — manual update required.

---

## Figma CEO Session Checklist (Print or Have Open on Phone)

**Time budget:** 60-90 minutes for first-time Figma user; 20-30 minutes for experienced.

### Pre-Session (5 min)

- [ ] Open Figma.com in browser, sign in (or create free account)
- [ ] Open this checklist in a second tab/window
- [ ] Open `Variable-Cheat-Sheet.md` in a third tab
- [ ] Set workspace name to "Titus Banks Studio" if creating new

### Step 1 — Master Brand File (5 min)

- [ ] Click "+" in team file browser
- [ ] Choose "Design file" (NOT FigJam)
- [ ] Name: `Titus Banks — Master Brand System`
- [ ] Description: "Source of truth for all Titus Banks design. Owner: CDO. Do not duplicate without CDO approval."
- [ ] Set file cover image to FINAL APPROVED book cover (the 3D mockup from `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/3D_Book_Mockup.jpg` or similar)
- [ ] Click Create

### Step 2 — Page Architecture (10 min)

Create these 13 pages by right-clicking the Pages panel and "Add page":

- [ ] Page 1: `📘 Cover`
- [ ] Page 2: `🎨 Brand Tokens`
- [ ] Page 3: `🧱 Components`
- [ ] Page 4: `🖼 Templates`
- [ ] Page 5: `🌐 Web — Landing Pages`
- [ ] Page 6: `📱 Social — Instagram`
- [ ] Page 7: `📱 Social — Facebook`
- [ ] Page 8: `📱 Social — LinkedIn`
- [ ] Page 9: `🎥 YouTube`
- [ ] Page 10: `📚 Book Assets`
- [ ] Page 11: `📊 Decks — Pitch`
- [ ] Page 12: `🗂 Asset Library`
- [ ] Page 13: `📋 Archive`

### Step 3 — Variables (15-20 min)

On the `🎨 Brand Tokens` page, open the Local Variables panel and create 3 Collections:

- [ ] Collection `color` with 9 color variables (use Cheat Sheet)
- [ ] Collection `space` with 9 number variables
- [ ] Collection `radius` with 4 number variables

**Verify:** Total 22 variables exist. Spot-check: `navy` = `#0F2742`, `gold` = `#D4A14A`.

### Step 4 — First Component (Button) (20-30 min)

On the `🧱 Components` page, build the seed Button component:

- [ ] Draw a frame: 180x48px
- [ ] Fill: `gold` (variable)
- [ ] Text inside: "Get the book" (placeholder)
- [ ] Text color: `navy-deep`
- [ ] Corner radius: `radius-md` (variable)
- [ ] Auto-layout: horizontal, padded 12 / 24
- [ ] Component name: `Button / Primary / Default`
- [ ] Duplicate to create variants:
  - [ ] `Button / Primary / Hover` (gold-soft background)
  - [ ] `Button / Primary / Disabled` (slate bg, white text, 60% opacity)
  - [ ] `Button / Secondary / Default` (transparent, navy border, navy text)
- [ ] `Button / Secondary / Hover` (navy bg, white text)
- [ ] `Button / Ghost / Default` (no bg, no border, navy text, gold underline on hover)

**Total: 6 button variants.** This is the only component built today. Other 55 components grow over time.

### Step 5 — Publish to Library (5 min)

- [ ] Click the book icon in the file header ("Open Library")
- [ ] Toggle "Publish styles and components" on for the `Button / *` components
- [ ] This allows future Titus Banks Figma files to link to these components

### Step 6 — Report Back (5 min)

- [ ] Copy the Figma file URL
- [ ] Take a screenshot of the Button / Primary component
- [ ] Reply using the `CEO-Report-Back-Template.md` template

---

## CEO Report-Back Template

After completing the Figma session, the CEO replies with this format:

```
Figma Foundation Setup — Completion Report
Date: 2026-06-06
Time spent: [X minutes]

Master Brand File URL: [paste Figma file URL here]

Page Architecture: [✓ 13 pages created] / [✗ skipped page __]
Variables: [✓ 22 variables created across 3 collections] / [✗ issue: ___]
First Component: [✓ Button / Primary / Default built with 6 variants] / [✗ issue: ___]
Library Publish: [✓ published] / [✗ issue: ___]

Screenshot of Button / Primary attached: [yes / no]

Issues encountered (if any):
- [describe any blockers, errors, or questions]

CDO Next Steps Requested:
- [what should CDO do next, e.g., "begin Phase 1 component spec review"]
```

---

## Time & Cost Reference

- Figma free tier: 3 files per workspace, unlimited editors on a team. Sufficient for a single-CEO design studio.
- Figma Professional: $15/month per editor. Only needed for multi-editor collaboration or API access. NOT YET NEEDED.
- Estimated total time: 60-90 min first session, 20-30 min future sessions.

---

## What CDO Will Do After CEO Completes This

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
| Token drift if CEO hard-codes values | Step 3 (Variables) MUST come before Step 4 (Components). This checklist enforces the order. |
| File proliferation | Single Master file only. CDO will reject any "Titus Banks v2.fg" duplicates. |
| Figma API not in OpenCode | Not needed yet. Can add later if CDO programmatic access becomes valuable. |

---

**Last updated:** 2026-06-06
**Status:** READY FOR CEO EXECUTION
**Next:** CEO schedules 60-90 min Figma session and runs the 6-step checklist above
