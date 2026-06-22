# Template System Specification

**Owner:** CDO (exec-cdo)
**Status:** Master Brand System v0.1 (Priority 2 expansion)
**Last updated:** 2026-06-06

This is the on-disk (non-Figma) record of the template system. The actual Figma templates are built per `BRAND/Figma-Setup/Templates-Spec.md`. This document describes how templates are named, stored, versioned, and retired in the on-disk asset library.

---

## Why Both Figma and Disk

- **Figma templates** = drag-and-drop starting points for new design work.
- **On-disk templates** = the rendered output (PNG, PDF, etc.) stored for reuse in platforms that don't allow Figma embed (VistaCreate, KDP, Payhip, email tools).

A new template gets created in BOTH places. The Figma version is the source of truth; the on-disk version is the render.

---

## Folder Structure

```
BRAND/
└── Templates/
    ├── README.md (this file)
    ├── Web/
    │   ├── Landing-Page-Lead-Magnet.png
    │   ├── Landing-Page-Book-Sales.png
    │   └── ...
    ├── Social-Instagram/
    │   ├── Post-Quote-v1.png
    │   ├── Story-5Frame-v1.png
    │   └── ...
    ├── Social-Facebook/
    │   └── Ad-Lead-v1.png
    ├── Social-LinkedIn/
    │   └── Post-Carousel-v1.png
    ├── YouTube/
    │   └── Thumbnail-v1.png
    ├── Decks/
    │   ├── Slide-Title.png
    │   ├── Slide-Content.png
    │   └── ...
    ├── Book/
    │   ├── Cover-Flat.png
    │   ├── Cover-3D.png
    │   ├── Mockup.png
    │   └── ...
    └── Email/
        └── Header.png
```

Sub-folders are added as new template categories emerge. Existing categories are never renamed without a search-and-replace across the asset library index.

---

## Naming Convention

`<Category>-<Type>-<Variant>-v<MAJOR>.<MINOR>.<ext>`

- **Category:** Landing-Page, Post, Story, Ad, Thumbnail, Slide, Cover, Header
- **Type:** Quote, Lead, Book-Sales, Title, Content, 3D, Flat
- **Variant:** (optional) v1, v2 for distinct visual approaches
- **Version:** MAJOR (full redesign) or MINOR (color/font tweak)
- **Extension:** png, jpg, pdf, fig (Figma file)

**Examples:**
- `Landing-Page-Lead-Magnet-v1.0.png`
- `Post-Quote-v2.1.png`
- `Story-5Frame-v1.0.png`
- `Slide-Title-v1.0.png`
- `Cover-3D-v3.0.png` (current Struck Down approved cover)

---

## Version Bumping Rules

| Change | Bump |
|--------|------|
| Color tweak, font tweak, small visual adjustment | MINOR (1.0 → 1.1) |
| Layout change, new component, new structure | MAJOR (1.x → 2.0) |
| Full redesign | MAJOR + new variant (1.x → 2.0) AND archive the v1.x series |
| Retired permanently | Move to `BRAND/Templates/Archive/<YYYY-MM>/` |

**The on-disk and Figma versions must have matching version numbers.** If Figma has v1.2, the on-disk render of that template is also v1.2.

---

## The Render Pipeline

When the CDO creates or updates a template:

1. Build in Figma (source of truth).
2. Export the populated state as PNG (1x for digital, 3x for print/retina).
3. Save to the on-disk folder with matching version number.
4. Update `BRAND/Asset-Library-Index.md` with the new template entry.
5. Update the Figma page index (Page 12 in `CEO-Playbook.md`).
6. (If MAJOR bump) Archive the prior version.

---

## Template Reuse Policy

**The CDO always checks for an existing template before building new.**

| Scenario | Action |
|----------|--------|
| New project matches existing template exactly | Duplicate the template. Don't redesign. |
| New project is close to an existing template | Adapt the existing template. Bump MINOR. |
| New project is similar in spirit but visually different | Use existing as inspiration. Build new. Bump MAJOR. New variant if there's a use case for the old one. |
| New project has no analog | Build new template. New category folder if needed. |

---

## Cross-Platform Template Variants

Some templates need different versions for different platforms. Example: A quote post might have:

- `Post-Quote-Instagram-v1.0.png` (1080x1080, square)
- `Post-Quote-LinkedIn-v1.0.png` (1200x627, horizontal)
- `Post-Quote-Story-v1.0.png` (1080x1920, vertical)

Each is a separate template with its own version. The source design in Figma is the same; the export dimensions and small layout shifts are different.

---

## Template Retirement

When a template is retired:

1. Move the file to `BRAND/Templates/Archive/<YYYY-MM>/`.
2. Update `BRAND/Asset-Library-Index.md` with `RETIRED — YYYY-MM — reason`.
3. Note the retirement in the Change Log at the bottom of this file.
4. (If a replacement exists) Link the new template in the retirement entry.

Retired templates are kept for 12 months minimum for audit and reference. After 12 months, the CDO may delete with CEO approval.

---

## Onboarding a New Template Category

When a new template category emerges (e.g., "Discord banner," "Zoom background"):

1. CDO proposes the category name and template list.
2. CEO approves the category and priority.
3. New folder created under `BRAND/Templates/`.
4. New section added to `BRAND/Asset-Library-Index.md`.
5. (If Figma-supported) New template type added to `Figma-Setup/Templates-Spec.md`.

---

## Cross-References

- `BRAND/Figma-Setup/Templates-Spec.md` — the 8 Figma templates
- `BRAND/Asset-Library-Index.md` — the index this system feeds
- `BRAND/Brand-System/Master-Brand-Standards.md` — the design system the templates follow

---

## Change Log

- 2026-06-06 — v0.1 created (Master Brand System, Priority 2 of new execution order).
