# Figma Foundation Setup — Prep Document

**Owner:** CDO (exec-cdo)
**Status:** Phase 0 Quick Win (QW6) + Figma Foundation Setup, Step 1
**Last updated:** 2026-06-06
**Constraint:** CDO does not have Figma desktop/API access. The CEO performs all Figma drag-and-drop actions. This document is the CEO's exact playbook.

---

## Why This Document Exists

The Figma foundation is approved as a standalone deliverable. The CDO will not do creative drag-and-drop in Figma — the CEO is the human hands. The CDO delivers:

1. The file structure (this document).
2. The component specifications (in `Figma-Setup/Component-Library-Spec.md`).
3. The template inventory (in `Figma-Setup/Templates-Spec.md`).
4. The asset organization plan (in `Figma-Setup/Asset-Organization-Plan.md`).
5. The token values (in `BRAND/tokens.json` — already done in QW3).

The CEO opens Figma, follows the playbook, and reports back. The CDO reviews screenshots and updates tokens/specs.

---

## Figma Account & Initial Setup

### Step 1: Verify Figma Account

1. Go to https://www.figma.com
2. Sign in with the email associated with the user's existing Figma access (or create a free account if none exists).
3. Confirm the workspace name. Recommend: `Titus Banks Studio`.

### Step 2: Create the Master Brand File

1. Click **"+"** in the team file browser.
2. Choose **Design file** (NOT FigJam).
3. Name: `Titus Banks — Master Brand System`.
4. Description: "Source of truth for all Titus Banks design. Owner: CDO. Do not duplicate without CDO approval."
5. Set the file's cover image to the FINAL APPROVED book cover.
6. Click **Create**.

### Step 3: Set Up the Page Architecture

Inside the new file, create these pages (Figma's left sidebar, right-click "Pages" panel > "Add page"):

| # | Page Name | Purpose | Status |
|---|-----------|---------|--------|
| 1 | 📘 Cover | File index, version, last-updated stamp | New |
| 2 | 🎨 Brand Tokens | Color, type, spacing as Figma Variables | New |
| 3 | 🧱 Components | Buttons, cards, inputs, icons, nav | New |
| 4 | 🖼 Templates | Reusable layouts (hero, post, story, ad) | New |
| 5 | 🌐 Web — Landing Pages | Linkpod-style hero, feature, CTA, footer | New |
| 6 | 📱 Social — Instagram | 1080x1080, 1080x1920 templates | New |
| 7 | 📱 Social — Facebook | 1200x630, 1080x1080 ad templates | New |
| 8 | 📱 Social — LinkedIn | 1200x627 templates | New |
| 9 | 🎥 YouTube | Thumbnails 1280x720, end screens | New |
| 10 | 📚 Book Assets | Struck Down cover, mockup, ads, quotes | New |
| 11 | 📊 Decks — Pitch | 16:9 slide master, pitch deck template | New |
| 12 | 🗂 Asset Library | Indexed, tagged, searchable | New |
| 13 | 📋 Archive | Retired, deprecated, replaced | New |

### Step 4: Set Up Variables (Tokens)

On the **Brand Tokens** page, the CEO creates Figma Variables matching `BRAND/tokens.json`. The CDO's spec is:

- **Color Variables** (Collection: `color`):
  - `navy` = `#0F2742`
  - `navy-deep` = `#0A1B30`
  - `gold` = `#D4A14A`
  - `gold-soft` = `#E8C98A`
  - `green-success` = `#1F6B4A`
  - `slate` = `#5A6B7B`
  - `cream` = `#F5F1E8`
  - `white` = `#FFFFFF`
  - `off-black` = `#0E1116`
- **Number Variables** (Collection: `space`):
  - `space-xxs` = 4
  - `space-xs` = 8
  - `space-sm` = 12
  - `space-md` = 16
  - `space-lg` = 24
  - `space-xl` = 32
  - `space-2xl` = 48
  - `space-3xl` = 64
  - `space-4xl` = 96
- **Radius Variables** (Collection: `radius`):
  - `radius-sm` = 4
  - `radius-md` = 8
  - `radius-lg` = 16
  - `radius-pill` = 9999

Variables let the CDO change one value and the entire file (and all linked components) updates. The CDO will use this for any future token change.

### Step 5: First Component (Button)

On the **Components** page, the CEO creates a single reusable button as the seed:

1. Draw a frame 180x48px.
2. Set fill to `gold` variable.
3. Set text inside: "Get the book" (placeholder).
4. Set text color to `navy-deep`.
5. Set corner radius to `radius-md` variable.
6. Set auto-layout: horizontal, padded 12 / 24.
7. Name the component: `Button / Primary / Default`.
8. Duplicate and create variants:
   - `Button / Primary / Hover` (gold-soft background)
   - `Button / Primary / Disabled` (slate background, white text, 60% opacity)
   - `Button / Secondary / Default` (transparent, navy border, navy text)

This is the only component the CDO needs to start. The rest of the library grows as projects need them. Premature component creation wastes CEO time and bloats the file.

### Step 6: Add the File to the Team Library

1. In the file header, click the **book icon** ("Open Library").
2. Toggle "Publish styles and components" on for the `Button / *` component.
3. This lets all future Titus Banks Figma files link to this component rather than copy it.

---

## Reporting Back

After completing steps 1-6 (estimated 60-90 minutes for a first-time Figma user, 20-30 minutes for someone with Figma experience), the CEO replies with:

1. Figma file URL.
2. Confirmation that all 13 pages exist.
3. Confirmation that the 9 color variables, 9 space variables, and 4 radius variables are created.
4. Screenshot of the Button / Primary component on the Components page.

The CDO will then begin Step 7 — the Component Library expansion plan — and submit the first batch of new components for the CEO to build.

---

## What the CDO Will Do Next (After CEO Completes Steps 1-6)

1. Write `Figma-Setup/Component-Library-Spec.md` with the full component list (Phase 1, 2, 3 priority).
2. Write `Figma-Setup/Templates-Spec.md` with the template inventory and base frame sizes.
3. Write `Figma-Setup/Asset-Organization-Plan.md` with the indexing/tagging system.
4. Update `BRAND/Asset-Library-Index.md` with Figma file URL once provided.
5. Begin the Master Brand System documentation referencing this Figma file as the live source.

---

## Time & Cost

- Figma free tier supports 3 files, unlimited editors on a team. For a single-CEO design studio, the free tier is enough.
- Figma Professional ($15/month per editor) is only needed if the CDO needs write access via API (not yet).
- Recommendation: stay on free tier until a clear need (multi-editor collaboration or design system expansion beyond 1 user) appears.

---

## Risks

- **Figma learning curve.** If the CEO is new to Figma, the first session may take 90 minutes. The CDO is patient and will iterate.
- **Token drift.** If the CEO hard-codes values in components before variables are set, refactoring is painful. Step 4 must come before Step 5.
- **File proliferation.** The CDO will reject any "Titus Banks v2.fg" duplicate files. All work lives in the single Master file.
- **API access.** Without Figma API token in OpenCode, the CDO cannot programmatically read/update the file. If that becomes a need, a token can be added to `opencode.json` env later.

---

## Approval

This prep document does not require separate CEO approval. It executes the Figma Foundation Setup authorization already granted. The CEO proceeds when ready.
