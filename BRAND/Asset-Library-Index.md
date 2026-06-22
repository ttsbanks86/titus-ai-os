# Asset Library Index

**Owner:** CDO (exec-cdo)
**Status:** Phase 0 Quick Win (QW2) — DRAFT v0.1
**Last updated:** 2026-06-06
**Source:** `BRAND-SYSTEM/Asset-Audit-Report.md`

This index is the single source of truth for **what reusable design assets we have, where they live, and what they can be used for.** When a new project needs an asset, search this file first. Only build new when nothing in here fits.

---

## How to Use This Index

1. Before any new design work, the CDO searches this index for matching assets.
2. If an asset fits: **reuse it.** Don't redesign.
3. If an asset is close: **adapt it.** Don't redesign.
4. If nothing fits: **improve the closest match** and add the result back to this index.
5. If it's truly new: build it, document it here, link the source file.

Every entry below is an asset that passed the audit and scored production-ready (70+ on the 75-point scale). The score reflects brand alignment, technical quality, reusability, and conversion potential.

---

## Production-Ready Assets (19)

### Book Launch — "Struck Down but Not Destroyed" (Approved)

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| B1 | FINAL APPROVED Cover (JPG) | `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/Struck_Down_but_Not_Destroyed_FINAL_APPROVED_COVER.jpg` | Primary book cover — all marketing | 75/75 |
| B2 | FINAL Cover (PNG, transparent safe) | `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/Struck_Down_but_Not_Destroyed_FINAL_COVER.png` | Mockups, layered compositions | 75/75 |
| B3 | 3D Book Mockup (APPROVED) | `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/3D_Book_Mockup_APPROVED.jpg` | Web hero, ads, social | 75/75 |
| B4 | Full Cover Flat (print-ready) | `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/Full_Cover_Flat.jpg` | KDP upload, print | 75/75 |
| B5 | Back Cover | `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/Back_Cover.jpg` | Print back, KDP details | 72/75 |
| B6 | Spine | `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/Spine.jpg` | Print spine layout | 70/75 |

### Master Brand — Titus Banks

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| M1 | "Titus Banks" wordmark (text-based) | VistaCreate (text element) | Headers, signatures, presentation slides | 72/75 |
| M2 | Navy/Gold/Cream palette swatches | `BRAND/tokens.json` | All visual work | 75/75 |
| M3 | Tagline: "Faith-rooted wisdom for real-life growth." | `BRAND/Brand-Voice-Cheatsheet.md` | Hero text, signatures, ads | 75/75 |

### Faithful Journey Quest (FJQ)

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| F1 | "Faithful Journey Quest" wordmark (text-based) | VistaCreate | Headers, footers | 70/75 |
| F2 | Quest-pathway visual language (compass + path motif) | Note in `BRAND/Figma-Setup/Sub-Brand-Specs.md` | Book covers, devotionals, social | 72/75 |

### Business Analysis & Operations (BA)

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| A1 | BA Carousel (10 slides, 1080x1080) | `NETLIFY-DROP/ba/` (current) | LinkedIn lead magnet | 70/75 |
| A2 | BA Carousel slide-1 hook image (the one to swap — see QW7) | Slide 1 of carousel | LinkedIn thumbnail | 70/75 |

### AI at Work

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| AI1 | "AI at Work" wordmark (text-based) | VistaCreate | Headers | 70/75 |
| AI2 | Minimalist code + lightbulb motif | Note in `BRAND/Figma-Setup/Sub-Brand-Specs.md` | Thumbnails, blog art | 71/75 |

### Open Door AI Systems (Master + sub-brand)

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| O1 | "Open Door AI Systems" wordmark (text-based) | VistaCreate | Headers, decks | 70/75 |
| O2 | Doorway + circuit motif | Note in `BRAND/Figma-Setup/Sub-Brand-Specs.md` | Site hero, decks | 72/75 |

### Built With Truth

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| T1 | "Built With Truth" wordmark (text-based) | VistaCreate | Headers | 70/75 |
| T2 | Blueprint / cornerstone motif | Note in `BRAND/Figma-Setup/Sub-Brand-Specs.md` | Course thumbnails | 71/75 |

### Divine Works Hub (NEW — not yet designed)

| # | Asset | Location | Use For | Score |
|---|-------|----------|---------|-------|
| D1 | Pending first design pass | n/a | All DWH collateral | 0/75 |

---

## Asset Categories Needing Future Work (Reference Only)

These are documented in `BRAND-SYSTEM/Asset-Audit-Report.md` Section 7. They are NOT in the reusable library. The CDO will redesign them in future phases per the execution plan, only after Master Brand System is approved.

- Pitch Deck Rebuild (Phase 3)
- Book Launch Social Ad Kit (Phase 1 of original plan, now retitled "Struck Down Production" under new Priority 3)
- FJQ Cover Page Refresh
- Master Brand Style Guide
- BA Carousel Visual Variety

---

## Maintenance Rules

1. **Any new production-ready asset gets added to this index** before it's shipped.
2. **Retired assets get a `RETIRED — date — reason` line** added, but the entry is preserved for history.
3. **No orphan files.** If a creative file exists on disk but is not in this index, the CDO either documents it or retires it on next pass.
4. **Score updates require a re-audit.** Don't bump scores casually.

---

## Cross-References

- `BRAND/tokens.json` — color, typography, spacing tokens
- `BRAND/Brand-Voice-Cheatsheet.md` — copy rules
- `BRAND/Asset-Library/...` — physical storage (to be populated as Master Brand System builds out)
- `BRAND-SYSTEM/Asset-Audit-Report.md` — the audit this index was derived from
- `BRAND/AI-Prompts/...` — AI prompt library for new asset generation
