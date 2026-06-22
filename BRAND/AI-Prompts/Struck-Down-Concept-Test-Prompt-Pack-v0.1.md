# 3-Concept Test Prompt Pack — Struck Down But Not Destroyed

**Owner:** CDO (exec-cdo)
**Status:** **SUPERSEDED 2026-06-06 by v0.2** — DO NOT USE
**Superseded by:** `Struck-Down-Concept-Test-Prompt-Pack-v0.2.md` (same folder)
**Supersession reason:** v0.1 listed 12 prompts against a 6-8 generation budget — a math mismatch that violated the v0.3 brief's budget discipline. v0.2 reconciles to 6 active prompts + 2 backup rules + 6 deferred to Round 2.
**Retained for:** history only. v0.2 is the current working prompt pack.

**v0.1 contents (12 prompts, 3 concepts × 4 asset types):** retained below verbatim for traceability. All 12 prompts are either preserved in v0.2 (the 3 LP heroes + 3 FB ads) or moved to Round 2 deferred (the 3 IG posts + 3 email headers).

**Original v0.1 status line (now historical):**

> v0.1 — DRAFT 2026-06-06. 12 prompts to be generated before the CEO picks a winning concept. NO IMAGE GENERATION has been performed yet. This document is the prompt pack only.
>
> Approval required: CEO picks the winning concept after reviewing the 12 outputs. No Priority A production begins until CEO chooses Concept A, B, or C as the production direction.

---

## Concept Test Framework

### The 3 Concepts

| Concept | Name | Frame | Visual register | Risk profile |
|---------|------|-------|------------------|---------------|
| **A** | **Quiet** | Hold the tension through stillness. Cream + soft navy. Book cover dominant. No motion, no flourishes. Wide negative space. | Quiet warmth. The cover IS the message. Type does the talking. | Lowest production risk. Most on-brand. Boring for scroll-stoppers. |
| **B** | **Bold** | Hold the tension through contrast. Navy + gold saturated. Book cover tilted or 3D-rotated. Implied motion. | Quiet warmth pushed to the edge. Cover dominates but at an angle. | Higher production risk. More scroll-stopping. Could feel like a different brand. |
| **C** | **Author-led** | Hold the tension through Bonolo's face. Cream background, real-author portrait (or placeholder for test), book cover secondary. | Warmth comes from the human, not the type. Author's voice carries the message. | Highest production risk (depends on photo session). Most platform-lifting. Lowest risk if photo session is delayed. |

### The 4 Asset Types Tested

| # | Asset | Format | Why this asset | Reuse |
|---|-------|--------|----------------|-------|
| **CT-1** | Landing page hero (wide) | 1920x800 | Tests the highest-stakes first impression (Payhip/KDP sales page top fold) | Concept test → A1 in Priority A |
| **CT-2** | Facebook ad | 1200x628 | Tests paid social scroll-stopping power | Concept test → A3 / A4 / A5 in Priority A |
| **CT-3** | Instagram post | 1080x1080 | Tests organic social shareability | Concept test → A6 / A7 / A8 in Priority A |
| **CT-4** | Email header | 1500x600 | Tests email open rates and click-through | Concept test → A10 / A11 in Priority A |

### Total: 3 concepts × 4 asset types = **12 prompts**, 6-8 AI generations with backups.

### Timeline (5 days)

| Day | Action | Owner | Time |
|-----|--------|-------|------|
| Day -7 (or Day 1) | Generate the 12 prompts | CDO (delegated) | 60 min |
| Day -7 to -5 | Generate 6-8 AI images using DALL-E (primary) or Leonardo (secondary) | CDO (delegated) | 90 min |
| Day -4 | Review and pick top 3 per concept (9 candidates → 3 finalists) | CDO | 60 min |
| Day -3 | CEO reviews 3 finalists in 30-min review session, picks the winning concept | CEO | 30 min |
| Day -2 to Day 0 | Locked concept moves to Priority A production | CDO | 5 days |

---

## Brand Context (Apply to ALL 12 Prompts)

This block is constant. Each prompt below inherits it.

### Type (FINAL, locked 2026-06-06)

- **Display:** Playfair Display (use "Playfair Display" in font token references; for AI generators, the visual style is "high-contrast modern serif")
- **Body:** Inter (for AI generators, "clean modern sans-serif")
- **Tagline lockup:** "STRUCK DOWN" / "but not" / "DESTROYED" using display + italic for "but not" + display for "DESTROYED"
- **Tagline (footer on all assets):** "You're not done yet."

### Color (locked)

- **Primary:** Cream `#F5F1E8` + Navy `#0F2742` + Gold `#D4A14A`
- **Secondary:** Gold Soft `#E8C98A` + Off-Black `#0E1116` + Slate `#5A6B7B`
- **Forbidden:** bright red, neon green, heavy gradients, stock-photo clichés

### Voice (locked)

- Clear, direct, warm, practical, grounded, human
- Banned: "Elevate", "Seamless", "Unleash", "Next-Gen", corporate filler
- No em dashes in customer-facing copy (em dashes OK in operator syntax / prompts)

### Author + Book Context

- Book: "Struck Down but Not Destroyed"
- Author: Bonolo Morake (attribution: "by Bonolo Morake" on all assets)
- Cover: Existing approved 3D mockup from `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/3D_Book_Mockup.jpg`
- ISBN: 978-1-945693-01-4 (not on assets; on KDP listing only)

### Negative Prompt (apply to all 12)

```
No em dashes. No banned words (elevate, seamless, unleash, next-gen, leverage, synergy, holistic, paradigm). No bright red, neon green, or saturated corporate colors. No stock photo clichés (handshake, lightbulb, brain, mountain peak at sunrise, generic Black silhouettes). No gradients except the existing approved book cover. No new AI generation of the existing protagonist figure on the book cover. No prosperity-gospel visual tropes (golden light from above, white doves flying off, crowns). No AI bypass markers (visible fingers, asymmetric eyes).
```

---

## CONCEPT A — QUIET

### Frame: Hold the tension through stillness. Wide negative space. The book cover IS the message.

---

### CT-A-1 — Landing Page Hero (Concept A: Quiet)

**Format:** 1920x800 PNG

**Prompt:**

```
Wide landing page hero, 1920x800. Cream background #F5F1E8 filling 70% of the frame. The approved "Struck Down but Not Destroyed" book cover (3D mockup, navy spine, cream front with stylized figure) is placed left-of-center, scaled to fill roughly 35% of the frame height, sitting on a thin cream surface. To the right of the book, a single line of navy display serif text reads "You're not done yet." Below that, in smaller body sans-serif, "A book for the season you're still in. By Bonolo Morake." A small gold-soft #E8C98A accent line beneath the tagline. The remaining 30% of the frame is empty negative space (cream). No people. No motion. No flourish. Camera: straight-on editorial product shot. Lighting: soft window light from upper left, no harsh shadows. Mood: still, contemplative, like a quiet morning. Type: high-contrast modern serif for the tagline, clean modern sans-serif for the body. NO em dashes, NO banned words, NO stock photo clichés, NO bright red, NO gradients, NO prosperity-gospel light from above.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, light from above, dove, crown, hand reaching up, brain, lightbulb, handshake, mountain, sunrise, AI artifacts, distorted fingers
```

**Quality check (before approving this output):**
- [ ] Cream background dominates (no other color competes)
- [ ] Book cover is recognizable as the approved design
- [ ] Tagline reads cleanly at thumbnail size
- [ ] No flourishes, no motion blur, no extra elements
- [ ] "by Bonolo Morake" attribution is present and readable

---

### CT-A-2 — Facebook Ad (Concept A: Quiet)

**Format:** 1200x628 PNG

**Prompt:**

```
Facebook ad, 1200x628. Cream background #F5F1E8. The approved book cover (flat version, no 3D rotation) on the left, taking 40% of the frame width. On the right, a navy pull quote in display serif: "Walks with you, not past you." Below that, in body sans-serif, smaller: "Struck Down but Not Destroyed by Bonolo Morake." A small gold-soft #E8C98A accent dot or short line in the lower right. No CTA button (test the visual without button first). No people. No motion. No flourishes. Editorial stillness. Soft window light. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt (appended):**

```
em dash, banned words, elevate, seamless, unleash, next-gen, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, mountain, sunrise, AI artifacts
```

**Quality check:**
- [ ] Pull quote is the visual anchor (not the book cover)
- [ ] Cream dominates
- [ ] No CTA button competing for attention
- [ ] "by Bonolo Morake" present
- [ ] Reads at Facebook thumbnail size

---

### CT-A-3 — Instagram Post (Concept A: Quiet)

**Format:** 1080x1080 PNG

**Prompt:**

```
Square Instagram post, 1080x1080. Cream background #F5F1E8. Centered: the approved book cover (flat, square crop) at 50% of frame width, slightly above center. Above the book, a small navy display serif header: "The book is here." Below the book, a single line in body sans-serif gold #D4A14A: "You're not done yet." At the bottom edge, in 12pt slate, "Bonolo Morake" with an Instagram handle placeholder. Editorial stillness. No people. No motion. No flourishes. Soft window light. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, AI artifacts
```

**Quality check:**
- [ ] Square format reads at Instagram thumbnail (small)
- [ ] Header line readable
- [ ] Tagline readable
- [ ] Author handle placeholder present
- [ ] No clutter

---

### CT-A-4 — Email Header (Concept A: Quiet)

**Format:** 1500x600 PNG

**Prompt:**

```
Email header, 1500x600. Cream background #F5F1E8 filling the full frame. Left: the approved book cover (flat, square crop) at 30% of frame height. Right: a navy display serif line "You're not done yet." with a small gold-soft #E8C98A horizontal accent line beneath. Below that, in body sans-serif slate: "The book is here. Pre-order opens [date]." Editorial stillness. No people. No motion. No flourishes. Soft window light. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, AI artifacts
```

**Quality check:**
- [ ] Renders well at email preview size (often cropped to 600x150 or similar)
- [ ] Tagline + accent line + book cover all readable
- [ ] Date placeholder present
- [ ] No clutter

---

## CONCEPT B — BOLD

### Frame: Hold the tension through contrast. Saturated navy + gold. Tilted book. Implied motion. The book cover dominates but at an angle.

---

### CT-B-1 — Landing Page Hero (Concept B: Bold)

**Format:** 1920x800 PNG

**Prompt:**

```
Wide landing page hero, 1920x800. Deep navy background #0A1B30 filling 60% of the frame, with a cream #F5F1E8 right-side band taking the remaining 40%. The approved book cover (3D mockup, navy spine, gold accents) is placed in the right third, rotated 8-12 degrees counter-clockwise, scaled to fill roughly 40% of frame height, casting a soft gold-tinted shadow. To the left, in display serif gold #D4A14A: "You're not done yet." Below that, in body sans-serif cream: "A book for the season you're still in." Below that, "by Bonolo Morake" in body sans-serif gold-soft #E8C98A. The composition feels like a moment of leaning forward, not standing still. A subtle gold-soft #E8C98A accent line on the lower edge. Type: high-contrast modern serif for the headline, clean modern sans-serif for body. Lighting: studio, with the gold tint of late afternoon. Mood: holding forward, leaning into something. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel, NO additional figures, NO crowns.
```

**Negative prompt (appended):**

```
em dash, banned words, elevate, seamless, unleash, next-gen, stock photo, bright red, neon green, gradient, prosperity gospel, light from above, dove, crown, hand reaching up, brain, lightbulb, handshake, mountain, sunrise, AI artifacts
```

**Quality check:**
- [ ] Tilted book reads as intentional, not mistake
- [ ] Navy + gold contrast works at small size
- [ ] Tagline readable
- [ ] "by Bonolo Morake" present
- [ ] No second figure or stock photo

---

### CT-B-2 — Facebook Ad (Concept B: Bold)

**Format:** 1200x628 PNG

**Prompt:**

```
Facebook ad, 1200x628. Navy #0A1B30 background. The approved book cover (flat, 3D optional) on the right, slightly rotated 5-8 degrees clockwise, casting a gold-soft shadow. Left side: a single pull quote in display serif gold #D4A14A: "Walks with you, not past you." Below that, in body sans-serif cream: "Struck Down but Not Destroyed by Bonolo Morake." A small gold accent dot in the lower right. Composition feels like a book mid-toss, caught in motion. NO CTA button on the ad itself (test without first). NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, mountain, sunrise, AI artifacts
```

**Quality check:**
- [ ] Tilt is subtle but visible
- [ ] Gold-on-navy contrast works
- [ ] Pull quote is the anchor
- [ ] "by Bonolo Morake" present
- [ ] Reads at FB thumbnail

---

### CT-B-3 — Instagram Post (Concept B: Bold)

**Format:** 1080x1080 PNG

**Prompt:**

```
Square Instagram post, 1080x1080. Deep navy background #0A1B30. Centered: the approved book cover (flat, square crop) rotated 6-10 degrees counter-clockwise, taking 55% of frame width. Above the book, a small display serif gold line: "The book is here." Below the book, a single line in body sans-serif gold-soft #E8C98A: "You're not done yet." At the bottom edge, in 12pt cream: "Bonolo Morake." The composition feels like a moment of leaning forward. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, AI artifacts
```

**Quality check:**
- [ ] Tilt reads as intentional
- [ ] Gold-on-navy works at thumbnail
- [ ] "You're not done yet" readable
- [ ] "Bonolo Morake" present
- [ ] No clutter

---

### CT-B-4 — Email Header (Concept B: Bold)

**Format:** 1500x600 PNG

**Prompt:**

```
Email header, 1500x600. Navy #0A1B30 background. Right: the approved book cover (flat, square crop) rotated 5-7 degrees counter-clockwise, taking 35% of frame height. Left: a display serif gold line: "You're not done yet." with a small gold-soft accent line beneath. Below that, in body sans-serif cream: "The book is here. Pre-order opens [date]." Composition feels like a book caught mid-motion. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, AI artifacts
```

**Quality check:**
- [ ] Tilt works at email preview
- [ ] Gold-on-navy contrast holds
- [ ] Tagline + date readable
- [ ] No clutter

---

## CONCEPT C — AUTHOR-LED

### Frame: Hold the tension through Bonolo's face. Real-author portrait (or placeholder for test), cream background, book cover secondary.

**NOTE:** Concept C depends on the author photo session. For the CONCEPT TEST, the placeholder is "a warm, mid-30s Black woman or man with short natural hair, soft expression, no smile, against a cream background, wearing a navy or cream top, looking slightly off-camera as if in mid-thought." If the real photo is available, the prompt swaps the placeholder for the real photo reference.

---

### CT-C-1 — Landing Page Hero (Concept C: Author-led)

**Format:** 1920x800 PNG

**Prompt:**

```
Wide landing page hero, 1920x800. Cream background #F5F1E8. Right side: an editorial portrait of a warm, mid-30s Black woman with short natural hair, soft expression, no smile, against a cream background, wearing a navy or cream top, looking slightly off-camera as if in mid-thought, lit by soft window light from upper left. The portrait takes roughly 45% of frame width, on the right side. To the left, in display serif navy: "You're not done yet." Below that, in body sans-serif slate: "A book for the season you're still in." Below that, in body sans-serif gold #D4A14A: "by Bonolo Morake." A small gold-soft accent line beneath the tagline. The composition feels like Bonolo is in the room with you. NO em dashes, NO banned words, NO stock photo cliché, NO bright red, NO gradients, NO prosperity gospel, NO crown on the person, NO halo effect, NO over-stylized "Black excellence" tropes.
```

**Negative prompt (appended):**

```
em dash, banned words, elevate, seamless, unleash, next-gen, stock photo, bright red, neon green, gradient, prosperity gospel, light from above, dove, crown, halo, Black excellence trope, AI artifacts, distorted fingers, asymmetric eyes
```

**Quality check:**
- [ ] Portrait looks like a real person, not a stock image
- [ ] Soft expression, not smiling
- [ ] Cream + navy + gold palette
- [ ] Tagline + "by Bonolo Morake" present
- [ ] No halo or crown

---

### CT-C-2 — Facebook Ad (Concept C: Author-led)

**Format:** 1200x628 PNG

**Prompt:**

```
Facebook ad, 1200x628. Cream background #F5F1E8. Right: the editorial portrait of Bonolo (same person as CT-C-1, or real Bonolo if photo session done), at 40% of frame width, looking slightly off-camera. Left: a single pull quote in display serif navy: "Walks with you, not past you." Below that, in body sans-serif gold #D4A14A: "Bonolo Morake." A small navy accent dot in the lower right. No CTA button on the ad itself. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel, NO crown, NO halo.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, halo, Black excellence trope, AI artifacts, distorted fingers
```

**Quality check:**
- [ ] Portrait is the visual anchor
- [ ] Pull quote present
- [ ] "Bonolo Morake" attribution
- [ ] Reads at FB thumbnail

---

### CT-C-3 — Instagram Post (Concept C: Author-led)

**Format:** 1080x1080 PNG

**Prompt:**

```
Square Instagram post, 1080x1080. Cream background #F5F1E8. Top half: the editorial portrait of Bonolo, head and shoulders, soft expression, looking slightly off-camera, lit by soft window light, no smile. Bottom half: a small display serif gold #D4A14A line: "The book is here." Below that, in body sans-serif navy: "You're not done yet." At the very bottom, in 12pt slate: "Bonolo Morake." NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel, NO crown, NO halo.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, halo, Black excellence trope, AI artifacts
```

**Quality check:**
- [ ] Portrait is the visual anchor
- [ ] "You're not done yet" readable
- [ ] "Bonolo Morake" present
- [ ] Reads at IG thumbnail

---

### CT-C-4 — Email Header (Concept C: Author-led)

**Format:** 1500x600 PNG

**Prompt:**

```
Email header, 1500x600. Cream background #F5F1E8. Left: the editorial portrait of Bonolo, head and shoulders, at 35% of frame height, soft expression, looking slightly off-camera. Right: a display serif navy line: "You're not done yet." with a small gold-soft accent line beneath. Below that, in body sans-serif slate: "The book is here. Pre-order opens [date]." Below that, in body sans-serif gold: "Bonolo Morake." NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel, NO crown, NO halo.
```

**Negative prompt (appended):**

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, dove, crown, halo, Black excellence trope, AI artifacts
```

**Quality check:**
- [ ] Portrait + tagline + date all readable
- [ ] "Bonolo Morake" attribution
- [ ] Works at email preview size

---

## Generation Plan (6-8 AI generations with backups)

| Priority | Vendor | Count | Rationale |
|----------|--------|-------|-----------|
| 1 | DALL-E (ChatGPT) | 5 | User has 24/10-window remaining. Use 5 of the 10 daily. |
| 2 | Leonardo.ai | 3 | User has 134 tokens. Use 3 (low risk). |
| 3 | Midjourney | 0 | Not subscribed. |
| 4 | Backup (if any output fails quality check) | 0-2 | Reserved from remaining 6 budget. |

**Total Phase 0 generation budget: 6-8 generations.** No image has been generated yet. Generation is the next action after CEO approval of this prompt pack.

---

## CEO Concept Decision

After the 12 outputs (3 finalists) are reviewed, the CEO picks the winning concept:

```
Concept Test Decision
Date: ___________
Reviewer: CEO (Titus Banks)

Concepts reviewed: A (Quiet), B (Bold), C (Author-led)

Winning concept: ☐ A (Quiet) / ☐ B (Bold) / ☐ C (Author-led)

Notes for Priority A production:
_________________________________________________

Approve to begin Priority A production?
☐ YES, proceed with [winning concept]
☐ HOLD, request revisions
☐ REJECT, new concept test needed
```

---

## Approval Status

| Checkpoint | Status |
|------------|--------|
| Prompt pack written | COMPLETE 2026-06-06 |
| CEO review of prompt pack | PENDING |
| Image generation | NOT STARTED (blocked until CEO approves prompt pack) |
| Concept decision | PENDING (after generation) |
| Priority A production | PENDING (after concept decision) |

---

**Last updated:** 2026-06-06
**Owner:** CDO (exec-cdo)
**Next action:** CEO reviews this prompt pack; if approved, CDO generates the 12 images using the 6-8 generation budget
