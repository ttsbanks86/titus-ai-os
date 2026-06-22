# Figma Component Library Specification

**Owner:** CDO (exec-cdo)
**Status:** Figma Foundation Setup, Step 2 — DRAFT v0.1
**Last updated:** 2026-06-06
**Builds on:** `Figma-Setup/CEO-Playbook.md`

This document is the CDO's blueprint for the Figma component library. The CEO builds the components in the order below. The CDO reviews each batch.

**Build rule:** Phase 1 components are the foundation. Do not skip to Phase 2 until Phase 1 is approved. Premature components = file bloat + naming chaos.

---

## Phase 1: Foundation (CEO builds first)

These are the 12 components the CDO needs to start any meaningful Titus Banks design.

### 1.1 Buttons

| Component | Variants | Notes |
|-----------|----------|-------|
| Button / Primary / Default | — | Gold bg, navy-deep text, radius-md |
| Button / Primary / Hover | — | Gold-soft bg |
| Button / Primary / Disabled | — | Slate bg, white text, 60% opacity |
| Button / Secondary / Default | — | Transparent bg, navy border, navy text |
| Button / Secondary / Hover | — | Navy bg, white text |
| Button / Ghost / Default | — | No bg, no border, navy text, gold underline on hover |

Auto-layout: horizontal, padded 12 / 24. Text style: Body / Button (16px, weight 600, body font).

### 1.2 Cards

| Component | Variants | Notes |
|-----------|----------|-------|
| Card / Default | — | White bg, radius-lg, shadow-sm, padded lg |
| Card / Cream | — | Cream bg, radius-lg, no shadow |
| Card / Dark | — | Navy-deep bg, white text |

### 1.3 Headings

| Component | Variants | Notes |
|-----------|----------|-------|
| Heading / Display | XL, L | Display font, navy color, tight line-height |
| Heading / H1–H4 | 4 sizes | Display font, navy color |
| Overline | — | Body font, 11px, gold color, all caps, letter-spacing 0.1em |
| Lead | — | Body-lg, slate color, relaxed line-height |

### 1.4 Logos

| Component | Variants | Notes |
|-----------|----------|-------|
| Logo / Titus Banks / Dark | — | Navy text on light bg |
| Logo / Titus Banks / Light | — | White text on dark bg |
| Logo / Sub-brand / FJQ | — | Placeholder for now |
| Logo / Sub-brand / AI at Work | — | Placeholder for now |
| Logo / Sub-brand / BA | — | Placeholder for now |
| Logo / Sub-brand / Open Door | — | Placeholder for now |
| Logo / Sub-brand / Built With Truth | — | Placeholder for now |
| Logo / Sub-brand / Divine Works Hub | — | Placeholder for now |

Sub-brand logos are placeholders. They get built when the sub-brand differentiation work happens in the Master Brand System.

### 1.5 Icons

| Component | Variants | Notes |
|-----------|----------|-------|
| Icon set: Core 16 | — | home, book, work, mail, phone, arrow-right, check, x, plus, minus, search, menu, close, share, heart, info |
| Icon set: Faith 8 | — | dove, cross, book-open, hands-prayer, candle, path, key, light |

All icons: 24x24, 1.5px stroke, rounded caps, navy color (gold for active/CTA).

**Total Phase 1: 30 components.** Estimated CEO build time: 4-6 hours across multiple sessions.

---

## Phase 2: Composition (after Phase 1 approved)

These are larger composed pieces. 18 components. Build order: nav first (most reused), then forms (most complex), then content blocks.

### 2.1 Navigation

| Component | Variants | Notes |
|-----------|----------|-------|
| Nav / Top Bar / Default | — | Logo left, links center, CTA right |
| Nav / Top Bar / Sticky | — | Same with shadow-md on scroll |
| Nav / Footer / Default | — | 4-column footer with social links |
| Nav / Mobile Drawer | — | Hamburger menu slide-out |
| Nav / Breadcrumbs | — | Slash-separated with home icon |

### 2.2 Forms

| Component | Variants | Notes |
|-----------|----------|-------|
| Form / Input / Default | — | Navy border, cream bg, navy text |
| Form / Input / Focus | — | Gold border, thicker |
| Form / Input / Error | — | Red border (define `--color-error: #B23A48` token), red helper text |
| Form / Textarea | — | Same as input, taller |
| Form / Select | — | Dropdown with chevron |
| Form / Checkbox | — | Square, navy border, gold check |
| Form / Radio | — | Circle, navy border, gold fill |
| Form / Submit | — | Uses Button / Primary / Default |

**Color note:** Add `--color-error: #B23A48` and `--color-warning: #C77B30` to the color tokens before building these.

### 2.3 Content Blocks

| Component | Variants | Notes |
|-----------|----------|-------|
| Block / Hero / Default | — | Large heading, subhead, 1-2 CTAs, image right |
| Block / Hero / Centered | — | Same, image as background or below |
| Block / Feature Grid / 3-col | — | Icon + heading + body, 3 across |
| Block / Quote | — | Large quote, attribution, optional photo |
| Block / Testimonial | — | Photo + quote + name + role |
| Block / CTA Banner | — | Navy bg, gold heading, white CTA |
| Block / Stats | — | 3-4 stat numbers with labels |

**Total Phase 2: 18 components.** Estimated CEO build time: 6-8 hours.

---

## Phase 3: Templates (after Phase 2 approved)

These are full page templates. 8 templates. Build only when projects need them — premature templates become outdated.

| Template | Use For | Notes |
|----------|---------|-------|
| Landing Page / Lead Magnet | Gated PDF download | Hero + form + benefits + social proof |
| Landing Page / Book Sales | Struck Down sales page | Hero + book mockup + 3 benefits + endorsements + buy buttons |
| Instagram Post / Quote | 1080x1080 quote graphic | Heading + body + logo + accent |
| Instagram Story / 5-frame | 1080x1920 sequence | Frame 1 hook, 2-4 content, 5 CTA |
| Facebook Ad / Lead | 1200x628 | Hook image + 2-line copy + CTA button |
| YouTube Thumbnail | 1280x720 | Big face/text left, context image right |
| Pitch Deck / Slide | 16:9 | Title slide, content slide, section divider, closing CTA |
| LinkedIn Carousel / Slide | 1080x1080 | Number badge + heading + body + accent |

**Total Phase 3: 8 templates.** Estimated CEO build time: 8-10 hours.

---

## Naming & Organization Rules

1. **Slash-separated hierarchy:** `Category / Type / Variant / State`
   - Example: `Button / Primary / Default`
   - Example: `Card / Default / Hover`
2. **Use Figma's nested structure** in the Assets panel. Don't dump all 56 components at the same level.
3. **Description field is required** on every component. One sentence describing its purpose.
4. **Tags:** Add at least 3 tags per component (e.g., "button", "primary", "gold").
5. **No "v2" components.** When a component needs a redesign, the CDO updates the master and the file auto-updates via variants.

---

## Approval Checkpoints

The CEO reports back to the CDO at:

- **Checkpoint 1:** After Phase 1 components built (30 components).
- **Checkpoint 2:** After Phase 2 components built (48 total).
- **Checkpoint 3:** After Phase 3 templates built (56 total).

The CDO reviews the file via screenshot at each checkpoint, updates this spec with any changes, and approves before the next phase begins.

---

## What This Spec Does NOT Cover

- **Animation/interaction specs.** Figma prototyping (smart animate, scroll triggers) is a separate spec written when the first interactive project lands.
- **Code handoff.** When a Figma file goes to web/code, the CDO writes a separate handoff doc. This is a future need, not Phase 0.
- **Sub-brand differentiation visuals.** Those are part of the Master Brand System and come after this spec is approved.
