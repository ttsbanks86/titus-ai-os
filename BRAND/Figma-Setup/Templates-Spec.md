# Figma Templates Specification

**Owner:** CDO (exec-cdo)
**Status:** Figma Foundation Setup, Step 4 — DRAFT v0.1
**Last updated:** 2026-06-06

Templates are pre-built frames the CEO can duplicate when starting a new project. They are NOT projects themselves. They live on Page 4 of the Master Figma file (see `CEO-Playbook.md`).

**Build rule:** Build templates only when a real project needs them. The CDO does not pre-build 20 templates nobody has used.

---

## Template Inventory (8 total, Phase 3)

### T1. Landing Page / Lead Magnet

- **Frame size:** 1440 wide, auto height (typical 2400-3200px)
- **Sections top to bottom:**
  1. Top nav (uses Nav / Top Bar component)
  2. Hero — left: heading + lead + email input + submit button; right: book cover or relevant image
  3. 3 benefits grid (uses Block / Feature Grid)
  4. Testimonial (uses Block / Testimonial)
  5. CTA banner (uses Block / CTA Banner)
  6. Footer (uses Nav / Footer component)
- **Use for:** PDF downloads, email list growth, free resource gates.
- **Real use case:** "The Faithful Father's 5-Day Devotional" PDF for FJQ.

### T2. Landing Page / Book Sales

- **Frame size:** 1440 wide, auto height (typical 3200-4000px)
- **Sections top to bottom:**
  1. Top nav
  2. Hero — large 3D book mockup left, headline + subhead + buy buttons (paperback + Kindle + PDF) right
  3. 3 "what you'll find" benefits
  4. Author bio (Titus portrait + 3-sentence bio)
  5. 3 pull quotes from the book
  6. Endorsements / testimonials
  7. FAQ (3-5 questions)
  8. Final CTA
  9. Footer
- **Use for:** Payhip, KDP author page, ad landing pages.

### T3. Instagram Post / Quote

- **Frame size:** 1080x1080
- **Layout:** Cream bg, large navy heading, gold accent rule, body quote in body font, small "Titus Banks" wordmark bottom center
- **Variants:** 1-line quote, 3-line quote, full quote
- **Use for:** Weekly inspirational posts on Instagram.

### T4. Instagram Story / 5-Frame Sequence

- **Frame size:** 1080x1920 each, 5 frames in a row
- **Frame 1:** Hook question or bold statement
- **Frame 2-4:** Content (one idea per frame)
- **Frame 5:** CTA — "Tap to read" / "Link in bio" / "DM 'yes'"
- **Use for:** Lead generation, book launch teasers, event promos.

### T5. Facebook Ad / Lead

- **Frame size:** 1200x628
- **Layout:** 60% image right, 40% text + CTA left
- **Use for:** Lead form ads, traffic ads.

### T6. YouTube Thumbnail

- **Frame size:** 1280x720
- **Layout:** Big text (3-4 words max) left, 60% face or scene right
- **Rules:** Text must read at 1-inch tall. Face must show clear emotion.
- **Use for:** Every YouTube video published.

### T7. Pitch Deck / Slide

- **Frame size:** 1920x1080 (16:9)
- **Layout variants:**
  - Title slide — big statement, no body
  - Content slide — heading + bullets + optional image
  - Section divider — large number or phrase on navy bg
  - Quote slide — large quote, attribution
  - Closing CTA — single call to action
- **Use for:** Investor pitches, partner pitches, course launches, ministry presentations.

### T8. LinkedIn Carousel / Slide

- **Frame size:** 1080x1080
- **Layout:** Top: small number badge (01/10, 02/10) + slide title. Middle: 3-5 bullets or one big idea. Bottom: page number + "Titus Banks" wordmark.
- **Use for:** BA carousel, PM carousel, thought leadership carousels.

---

## Template State (in Figma)

Each template frame has 3 states shown side-by-side:

| State | Description |
|-------|-------------|
| Empty | Placeholders with `[HEADING HERE]`, `[IMAGE]`, etc. |
| Populated | Filled with realistic content for the template's first use case (e.g., for T1, the devotional). |
| Annotated | Same as Populated but with callouts explaining the design choices. |

When the CEO duplicates a template for a new project, they duplicate the **Empty** state.

---

## Template Maintenance

- **Update template** when a real project reveals a flaw.
- **Never** change a template's frame size or core structure without checking all current uses.
- **Always** update the on-disk `BRAND/Asset-Library-Index.md` when a template version changes.

---

## When to Build New Templates

Only when:

1. A real project is starting AND
2. No existing template fits AND
3. The CDO estimates at least 3 future uses of the new template

If only 1 future use is expected, build the asset directly without making a template. The CDO will keep a one-off file in the relevant project page, not the templates page.

---

## Cross-References

- `BRAND/Figma-Setup/Component-Library-Spec.md` — components templates use
- `BRAND/Figma-Setup/Asset-Organization-Plan.md` — naming and tagging system
- `BRAND/Asset-Library-Index.md` — on-disk record
