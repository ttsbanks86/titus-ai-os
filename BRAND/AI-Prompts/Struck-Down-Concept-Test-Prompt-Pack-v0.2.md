# 3-Concept Test Prompt Pack — Struck Down But Not Destroyed

**Owner:** CDO (exec-cdo)
**Status:** v0.2 — DRAFT 2026-06-06
**Purpose:** 6 active prompts to be generated manually by the CEO before the winning concept is picked. NO IMAGE GENERATION has been performed yet. This document is the prompt pack only.
**Supersedes:** v0.1 (12-prompt version, retired 2026-06-06 over 12-vs-6/8 budget inconsistency)

**Approval required:** CEO picks the winning concept after reviewing the 6 outputs (plus up to 2 backups). No Priority A production begins until CEO chooses Concept A, B, or C as the production direction.

---

## 1. Budget Reconciliation (v0.2)

This is the correction that v0.1 owed the CEO.

| Layer | Count | Notes |
|-------|-------|-------|
| **Active generations (Round 1)** | **6** | 3 Landing Page Heroes + 3 Social Ads (Facebook), one of each per concept |
| **Backup generations (conditional)** | **2** | Reserved. Used only with explicit CEO approval per the rules in section 6 |
| **Total budget** | **6-8** | Min = 6 active only. Max = 6 active + 2 backups |
| **Deferred to Round 2 (NOT in this budget)** | **6** | 3 Instagram posts + 3 email headers, one per concept. Reserved for after the winning concept is picked |
| **Generations performed so far** | **0** | Confirmed 2026-06-06. No AI engine touched. |

**Vendor allocation (recommended):**

| Vendor | Count | Rationale |
|--------|-------|-----------|
| DALL-E (ChatGPT) | 4-5 of 10/24h window | Primary engine. Strong on type rendering and editorial compositions |
| Leonardo.ai | 2-3 of 134 token balance | Secondary. Strong on painterly and dramatic lighting. Test how the same concept renders differently across engines |
| Backup (same engine as the failed concept) | 0-2 | Reserved. See section 6 |

**Default generation order** (this is a recommendation, not a rule — CEO may re-order):

| # | Prompt ID | Engine | File to save as |
|---|-----------|--------|-----------------|
| 1 | CT-A-LP-01 | DALL-E | `CT-A-LP-01.png` |
| 2 | CT-B-LP-01 | DALL-E | `CT-B-LP-01.png` |
| 3 | CT-C-LP-01 | DALL-E | `CT-C-LP-01.png` |
| 4 | CT-A-SA-01 | DALL-E | `CT-A-SA-01.png` |
| 5 | CT-B-SA-01 | Leonardo | `CT-B-SA-01.png` |
| 6 | CT-C-SA-01 | Leonardo | `CT-C-SA-01.png` |
| 7 | BACKUP-1 | (rule 1) | `BACKUP-1.png` |
| 8 | BACKUP-2 | (rule 2) | `BACKUP-2.png` |

If both backups are unused, the run ends at generation 6. If one is used, it ends at 7. If both, at 8. **Stop at 8 regardless.**

---

## 2. Concept Test Framework (unchanged from v0.1)

### The 3 Concepts

| Concept | Name | Frame | Visual register | Risk profile |
|---------|------|-------|------------------|---------------|
| **A** | **Quiet** | Hold the tension through stillness. Cream + soft navy. Book cover dominant. No motion, no flourishes. Wide negative space. | Quiet warmth. The cover IS the message. Type does the talking. | Lowest production risk. Most on-brand. Boring for scroll-stoppers. |
| **B** | **Bold** | Hold the tension through contrast. Navy + gold saturated. Book cover tilted or 3D-rotated. Implied motion. | Quiet warmth pushed to the edge. Cover dominates but at an angle. | Higher production risk. More scroll-stopping. Could feel like a different brand. |
| **C** | **Author-led** | Hold the tension through Bonolo's face. Cream background, real-author portrait (placeholder for test), book cover secondary. | Warmth comes from the human, not the type. Author's voice carries the message. | Highest production risk (depends on photo session). Most platform-lifting. Lowest risk if photo session is delayed. |

### Asset Types Tested in Round 1

| # | Asset | Format | Why this asset | Reuse into Priority A |
|---|-------|--------|----------------|------------------------|
| **LP-01** | Landing page hero (wide) | 1920x800 | Tests the highest-stakes first impression (Payhip/KDP sales page top fold) | Becomes A1 in Priority A |
| **SA-01** | Facebook ad (landscape) | 1200x628 | Tests paid social scroll-stopping power, primary paid channel | Becomes A3 / A4 / A5 in Priority A |

**Round 2 will test Instagram post (1080x1080) and email header (1500x600).** Both are deferred until the winning concept is locked.

---

## 3. Brand Context (LOCKED — apply to every prompt below)

This block is constant. Each prompt below inherits it.

### Type (FINAL, locked 2026-06-06)

- **Display:** Playfair Display (visual style: "high-contrast modern serif")
- **Body:** Inter (visual style: "clean modern sans-serif")
- **Tagline lockup:** "STRUCK DOWN" / "but not" / "DESTROYED"
- **Tagline (footer on all assets):** "You're not done yet."

### Color (LOCKED)

- **Primary:** Cream `#F5F1E8` + Navy `#0F2742` + Gold `#D4A14A`
- **Secondary:** Gold Soft `#E8C98A` + Off-Black `#0E1116` + Slate `#5A6B7B`
- **Forbidden:** bright red, neon green, heavy gradients, stock-photo clichés

### Voice (LOCKED)

- Clear, direct, warm, practical, grounded, human
- Banned words: "Elevate", "Seamless", "Unleash", "Next-Gen", "leverage", "synergy", "holistic", "paradigm"
- No em dashes in customer-facing copy (em dashes OK in operator syntax / prompts)

### Author + Book Context (LOCKED)

- Book: "Struck Down but Not Destroyed"
- Author: "by Bonolo Morake" (attribution on all assets)
- Cover: Existing approved 3D mockup at `BRAND-SYSTEM/MASTER/Struck-Down-Book-Assets/3D_Book_Mockup.jpg`

### Universal Negative Prompt (apply to every prompt below)

```
em dash, banned words, stock photo, bright red, neon green, gradient, prosperity gospel, light from above, dove, crown, halo, mountain sunrise, hand reaching up, brain, lightbulb, handshake, AI artifacts, distorted text, distorted fingers, asymmetric eyes, clickbait arrows, fake testimonial screenshots
```

---

## 4. ROUND 1A — Landing Page Heroes (3 prompts)

These three are the highest-stakes first-impression assets. They will run first in the manual generation order.

---

### CT-A-LP-01 — Concept A Quiet, Landing Page Hero

**Format:** 1920x800 PNG
**Asset purpose:** Top fold of Payhip / KDP sales page. The book + tagline must read at first glance.

**Prompt (paste into DALL-E or Leonardo):**

```
Wide landing page hero, 1920x800. Cream background #F5F1E8 filling 70% of the frame. The approved "Struck Down but Not Destroyed" book cover (3D mockup, navy spine, cream front with stylized figure) is placed left-of-center, scaled to fill roughly 35% of the frame height, sitting on a thin cream surface. To the right of the book, a single line of navy display serif text reads "You're not done yet." Below that, in smaller body sans-serif, "A book for the season you're still in. By Bonolo Morake." A small gold-soft #E8C98A accent line beneath the tagline. The remaining 30% of the frame is empty negative space (cream). No people. No motion. No flourish. Camera: straight-on editorial product shot. Lighting: soft window light from upper left, no harsh shadows. Mood: still, contemplative, like a quiet morning. Type: high-contrast modern serif for the tagline, clean modern sans-serif for the body. NO em dashes, NO banned words, NO stock photo clichés, NO bright red, NO gradients, NO prosperity-gospel light from above.
```

**Negative prompt:** (Universal block above, no additions)

**Quality check (before approving this output):**
- [ ] Cream background dominates (no other color competes)
- [ ] Book cover is recognizable as the approved design
- [ ] Tagline reads cleanly at thumbnail size
- [ ] No flourishes, no motion blur, no extra elements
- [ ] "by Bonolo Morake" attribution is present and readable

---

### CT-B-LP-01 — Concept B Bold, Landing Page Hero

**Format:** 1920x800 PNG
**Asset purpose:** Top fold of Payhip / KDP sales page, alternate direction. Tilt + saturated navy + gold contrast.

**Prompt:**

```
Wide landing page hero, 1920x800. Deep navy background #0A1B30 filling 60% of the frame, with a cream #F5F1E8 right-side band taking the remaining 40%. The approved book cover (3D mockup, navy spine, gold accents) is placed in the right third, rotated 8-12 degrees counter-clockwise, scaled to fill roughly 40% of frame height, casting a soft gold-tinted shadow. To the left, in display serif gold #D4A14A: "You're not done yet." Below that, in body sans-serif cream: "A book for the season you're still in." Below that, "by Bonolo Morake" in body sans-serif gold-soft #E8C98A. The composition feels like a moment of leaning forward, not standing still. A subtle gold-soft #E8C98A accent line on the lower edge. Type: high-contrast modern serif for the headline, clean modern sans-serif for body. Lighting: studio, with the gold tint of late afternoon. Mood: holding forward, leaning into something. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel, NO additional figures, NO crowns.
```

**Negative prompt:** (Universal block above, no additions)

**Quality check:**
- [ ] Tilted book reads as intentional, not mistake
- [ ] Navy + gold contrast works at small size
- [ ] Tagline readable
- [ ] "by Bonolo Morake" present
- [ ] No second figure or stock photo

---

### CT-C-LP-01 — Concept C Author-led, Landing Page Hero

**Format:** 1920x800 PNG
**Asset purpose:** Author-as-anchor variant. Tests whether the personal voice carries the campaign.

**PLACEHOLDER NOTE:** The author photo session (A13-A15) is **NOT APPROVED** as of 2026-06-06. This prompt uses a CONCEPT TEST PLACEHOLDER. The final Priority A asset will use the real Bonolo photo once the photo session is approved and executed. The placeholder is a real-person stand-in for concept direction only — it is NOT Bonolo and must not be presented as Bonolo.

**Prompt:**

```
Wide landing page hero, 1920x800. Cream background #F5F1E8. Right side: an editorial portrait of a warm, mid-30s Black woman with short natural hair, soft expression, no smile, against a cream background, wearing a navy or cream top, looking slightly off-camera as if in mid-thought, lit by soft window light from upper left. The portrait takes roughly 45% of frame width, on the right side. THIS IS A CONCEPT TEST PLACEHOLDER, NOT BONOLO. To the left, in display serif navy: "You're not done yet." Below that, in body sans-serif slate: "A book for the season you're still in." Below that, in body sans-serif gold #D4A14A: "by Bonolo Morake." A small gold-soft accent line beneath the tagline. The composition feels like Bonolo is in the room with you. NO em dashes, NO banned words, NO stock photo cliché, NO bright red, NO gradients, NO prosperity gospel, NO crown on the person, NO halo effect, NO over-stylized "Black excellence" tropes.
```

**Negative prompt:** (Universal block above, plus: "front-facing smiling portrait, Black excellence trope, generic stock-photo Black woman")

**Quality check:**
- [ ] Portrait looks like a real person, not a stock image
- [ ] Soft expression, not smiling
- [ ] Cream + navy + gold palette
- [ ] Tagline + "by Bonolo Morake" present
- [ ] No halo or crown
- [ ] Clearly a placeholder, not a generated "fake Bonolo"

---

## 5. ROUND 1B — Social Ads / Facebook (3 prompts)

These three test paid social scroll-stopping. They are the lower-stakes Round 1B test (the LP hero is the highest stakes).

---

### CT-A-SA-01 — Concept A Quiet, Facebook Ad

**Format:** 1200x628 PNG
**Asset purpose:** Paid Facebook ad. Pull-quote anchored. Cream-dominant.

**Prompt:**

```
Facebook ad, 1200x628. Cream background #F5F1E8. The approved book cover (flat version, no 3D rotation) on the left, taking 40% of the frame width. On the right, a navy pull quote in display serif: "Walks with you, not past you." Below that, in body sans-serif, smaller: "Struck Down but Not Destroyed by Bonolo Morake." A small gold-soft #E8C98A accent dot or short line in the lower right. No CTA button (test the visual without button first). No people. No motion. No flourishes. Editorial stillness. Soft window light. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt:** (Universal block above, no additions)

**Quality check:**
- [ ] Pull quote is the visual anchor (not the book cover)
- [ ] Cream dominates
- [ ] No CTA button competing for attention
- [ ] "by Bonolo Morake" present
- [ ] Reads at Facebook thumbnail size

---

### CT-B-SA-01 — Concept B Bold, Facebook Ad

**Format:** 1200x628 PNG
**Asset purpose:** Paid Facebook ad, alternate direction. Navy + gold, book tilted.

**Prompt:**

```
Facebook ad, 1200x628. Navy #0A1B30 background. The approved book cover (flat, 3D optional) on the right, slightly rotated 5-8 degrees clockwise, casting a gold-soft shadow. Left side: a single pull quote in display serif gold #D4A14A: "Walks with you, not past you." Below that, in body sans-serif cream: "Struck Down but Not Destroyed by Bonolo Morake." A small gold accent dot in the lower right. Composition feels like a book mid-toss, caught in motion. NO CTA button on the ad itself (test without first). NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel.
```

**Negative prompt:** (Universal block above, no additions)

**Quality check:**
- [ ] Tilt is subtle but visible
- [ ] Gold-on-navy contrast works
- [ ] Pull quote is the anchor
- [ ] "by Bonolo Morake" present
- [ ] Reads at FB thumbnail

---

### CT-C-SA-01 — Concept C Author-led, Facebook Ad

**Format:** 1200x628 PNG
**Asset purpose:** Author-anchored Facebook ad. Tests whether the personal voice + portrait combination outperforms book-only.

**PLACEHOLDER NOTE:** Same as CT-C-LP-01. This is a CONCEPT TEST PLACEHOLDER, not Bonolo.

**Prompt:**

```
Facebook ad, 1200x628. Cream background #F5F1E8. Right: the editorial portrait of a warm, mid-30s Black woman with short natural hair (SAME PERSON AS CT-C-LP-01, or real Bonolo if photo session done), at 40% of frame width, looking slightly off-camera. THIS IS A CONCEPT TEST PLACEHOLDER, NOT BONOLO. Left: a single pull quote in display serif navy: "Walks with you, not past you." Below that, in body sans-serif gold #D4A14A: "Bonolo Morake." A small navy accent dot in the lower right. No CTA button on the ad itself. NO em dashes, NO banned words, NO stock photo, NO bright red, NO gradients, NO prosperity gospel, NO crown, NO halo.
```

**Negative prompt:** (Universal block above, plus: "front-facing smiling portrait, Black excellence trope")

**Quality check:**
- [ ] Portrait is the visual anchor
- [ ] Pull quote present
- [ ] "Bonolo Morake" attribution
- [ ] Reads at FB thumbnail
- [ ] Clearly a placeholder, not a fake Bonolo

---

## 6. BACKUP RULES (2 reserved, conditional on CEO approval)

The two backup generations are NOT automatic. They are reserved. Each one requires explicit CEO approval before the CEO generates it. The CEO can refuse to use either backup and stop at 6 generations total.

### BACKUP-1 — Quality Recovery (use if a single output fails)

**Rule:** If, after the 6 active generations, any single output fails 3 or more of its 5 quality check criteria, the CEO may re-generate THAT prompt ONE TIME using:
- The same prompt text
- One small variation hint (e.g. "re-render with cooler color temperature" or "re-render the book smaller")
- The same engine that produced the original (don't switch engines mid-test)

**Cost:** 1 generation. Counts toward the 8 max.

**What this is NOT:** This is not creative exploration. It is recovery from a clearly bad output. If 2+ outputs fail, the CEO pauses and reports the pattern before re-generating — that signals a prompt or engine issue, not bad luck.

### BACKUP-2 — Strongest Concept Variant (use after the CEO picks the winning concept)

**Rule:** After the CEO reviews the 6 active outputs and picks the winning concept (A, B, or C), the CEO may use the second backup to generate ONE additional variant of the winning concept. The variant is NOT a different concept — it is a different composition, angle, or lighting of the SAME concept.

**Examples:**
- If Concept B wins on the LP hero, BACKUP-2 could be the same concept with a different book tilt (e.g. 15 degrees instead of 10)
- If Concept A wins on the FB ad, BACKUP-2 could be the same concept with the book on the right side instead of the left

**Cost:** 1 generation. Counts toward the 8 max.

**Why this is useful:** The CDO recommends this because the winning concept's FIRST rendering may not be its BEST rendering. A second look at the winning concept gives the CEO a stronger basis for the Priority A production call.

### If backups are not used

The test ends at 6 generations. The CEO still picks the winning concept from the 6 active outputs. The 2 backups are not "wasted" — they are held for a future concept test if needed.

---

## 7. ROUND 2 (DEFERRED — not in this budget)

These 6 prompts are reserved for AFTER the CEO picks the winning concept. They are NOT to be generated in Round 1. The CDO will issue a Round 2 prompt pack as a separate document after the concept decision is locked.

| Concept | Instagram Post (1080x1080) | Email Header (1500x600) |
|---------|----------------------------|--------------------------|
| **A Quiet** | CT-A-IG-02 (deferred) | CT-A-EM-02 (deferred) |
| **B Bold** | CT-B-IG-02 (deferred) | CT-B-EM-02 (deferred) |
| **C Author-led** | CT-C-IG-02 (deferred) | CT-C-EM-02 (deferred) |

**Why these are deferred:**
1. The 6-8 generation budget cannot accommodate them.
2. Generating IG and email variants for all 3 concepts would burn 12 generations before the CEO has picked a direction.
3. Generating IG and email variants for the WINNING concept only (3 generations) is more efficient and respects the budget.

**What the CEO does with this section:** Nothing. Read it. Confirm the deferred list matches your expectations. The CDO will produce the Round 2 prompt pack after the concept decision.

**Concept C Round 2 note:** When the CDO drafts the Round 2 prompt pack, the Instagram post and email header for Concept C will be re-evaluated. If the real Bonolo photo is available, the placeholder swaps out. If not, Concept C Round 2 prompts may shift to back-of-head or silhouette compositions that don't require the face.

---

## 8. Manual Generation Run Sheet (for the CEO)

This is the step-by-step the CEO follows. No automation. No Playwright. No DALL-E API calls. The CEO does this in their own ChatGPT and Leonardo sessions.

### Before you start

- [ ] Open ChatGPT in your browser (chat.openai.com). Make sure DALL-E is accessible.
- [ ] Open Leonardo.ai in a second tab. Confirm your token balance (you have ~134 tokens).
- [ ] Create the output folder: `BRAND/Struck-Down-Concept-Test-Round-1/images/`
- [ ] Open the generation log file: `BRAND/Struck-Down-Concept-Test-Round-1/generation-log.md` (create if it doesn't exist)

### Generation order

| Step | Prompt ID | Engine | Save as |
|------|-----------|--------|---------|
| 1 | CT-A-LP-01 | DALL-E | `BRAND/Struck-Down-Concept-Test-Round-1/images/CT-A-LP-01.png` |
| 2 | CT-B-LP-01 | DALL-E | `BRAND/Struck-Down-Concept-Test-Round-1/images/CT-B-LP-01.png` |
| 3 | CT-C-LP-01 | DALL-E | `BRAND/Struck-Down-Concept-Test-Round-1/images/CT-C-LP-01.png` |
| 4 | CT-A-SA-01 | DALL-E | `BRAND/Struck-Down-Concept-Test-Round-1/images/CT-A-SA-01.png` |
| 5 | CT-B-SA-01 | Leonardo | `BRAND/Struck-Down-Concept-Test-Round-1/images/CT-B-SA-01.png` |
| 6 | CT-C-SA-01 | Leonardo | `BRAND/Struck-Down-Concept-Test-Round-1/images/CT-C-SA-01.png` |
| 7 | (only if needed) BACKUP-1 | same engine as failed prompt | `BRAND/Struck-Down-Concept-Test-Round-1/images/BACKUP-1.png` |
| 8 | (only if needed) BACKUP-2 | CEO's choice (typically DALL-E for type) | `BRAND/Struck-Down-Concept-Test-Round-1/images/BACKUP-2.png` |

### For each generation step

- [ ] Copy the **prompt block** (the text inside the triple backticks) for that step
- [ ] Open the appropriate engine (DALL-E or Leonardo) in your browser
- [ ] Paste the prompt
- [ ] Generate (DALL-E usually returns 4 variations; pick the best 1, or re-roll up to 2 times)
- [ ] Download the chosen image as PNG
- [ ] Rename and save to the file path in the table above
- [ ] In `generation-log.md`, log:
  - Step number
  - Prompt ID
  - Engine
  - DALL-E generation count used (e.g. "1 of 10") OR Leonardo tokens used (e.g. "1 token")
  - Time taken (e.g. "90 sec")
  - Re-rolls (e.g. "0", "1", "2")
  - Any issues (e.g. "title rendered as 'Struck Dawn' on first try, re-rolled")
  - Quality check pass/fail (1-5 score per criterion)

### After step 6

- [ ] STOP. Do not start Round 2. Do not start Priority A production.
- [ ] Do not spend money on the author photo session.
- [ ] Do not commission the author photo session.
- [ ] A13, A14, A15 stay blocked.
- [ ] Reply to OpenCode: "Round 1 concept test images uploaded. 6 active generations used. [Plus N backups used.] Ready for CDO review."

### If you use a backup

- [ ] Confirm the backup rule (rule 1 or rule 2) before generating
- [ ] Log the backup use in `generation-log.md` with the rule invoked
- [ ] Do not use more than 2 backups total

### If something goes wrong

- [ ] If DALL-E is down, swap that step to Leonardo and note in the log
- [ ] If Leonardo is down, swap to DALL-E and note in the log
- [ ] If both are down, stop. Do not improvise with another engine. Report.
- [ ] If a generation produces something unusable (text garbled, image corrupted), re-roll once. If still unusable, log it and move to the next prompt. Use BACKUP-1 only if the failure is severe (3+ quality criteria failed).

---

## 9. Upload and Review Instructions (for the CEO → CDO)

When the 6 (or 6+N backup) images are saved, the CEO:

1. **Verifies** all images are in `BRAND/Struck-Down-Concept-Test-Round-1/images/` with the correct filenames.
2. **Completes** `BRAND/Struck-Down-Concept-Test-Round-1/generation-log.md` with one row per generation.
3. **Replies** to OpenCode with one of:
   - "Concept test images uploaded. Ready for CDO review." (and we proceed)
   - "I have quality concerns. Holding for CDO check before upload." (and we investigate)
   - "Backups used: [list]. [N] total generations consumed." (and we proceed with backup notes)

The CDO then:

1. Opens each image and scores it on the 5 quality criteria (1-5 each, 25 max).
2. Picks the best 3 candidates across the 3 concepts.
3. Writes a CDO recommendation for the winning concept with rationale.
4. Returns the 7 deliverables the CEO asked for (concept test results, best 3, CDO recommendation, AI generations used, remaining AI budget, quality concerns, next CEO decision).

The CEO then:

1. Reviews the CDO recommendation.
2. Picks the winning concept (A, B, or C) — or requests revisions — or rejects and requests a new concept test.
3. Locks the concept for Priority A production. **No Priority A work begins until this step is complete.**

---

## 10. Quality Check (5 criteria, 1-5 scale, 25 max)

Every image is scored against these 5 criteria. The score determines whether the image is usable, marginal, or failing.

| # | Criterion | 1 (fail) | 3 (pass) | 5 (excellent) |
|---|-----------|----------|----------|---------------|
| 1 | Concept match | Off-concept. Looks like a different concept entirely. | Concept is recognizable. | Concept is unmistakable at thumbnail size. |
| 2 | Title legibility | Title is unreadable or garbled. | Title is readable at full size, marginal at thumbnail. | Title is readable at thumbnail. |
| 3 | Color palette on-brand | Wrong colors (red, neon, off-palette) or palette mismatch. | Palette is correct, but accents fight the primary. | Palette is on-brand, no color competes. |
| 4 | Banned elements | Contains em dash, banned word, AI artifact, or stock cliché. | No banned elements, but has minor concern. | No banned elements. Clean. |
| 5 | Emotional tone | Wrong tone (cheerful, salesy, generic). | Tone is correct but flat. | Tone conveys "You're not done yet" without text. |

**Scoring band:**

| Score | Verdict | Action |
|-------|---------|--------|
| 22-25 | Strong candidate | Keep. Present to CEO as finalist. |
| 18-21 | Workable | Keep. Note minor issue. May be improved in BACKUP-2 if this is the winning concept. |
| 14-17 | Marginal | Flag. Do not present as finalist unless needed. |
| Below 14 | Fail | Re-roll once. If still fails, use BACKUP-1. |

---

## 11. CEO Concept Decision Template

After reviewing the 6 outputs (and any backups), the CEO replies with this:

```
Concept Test Decision
Date: ___________
Reviewer: CEO (Titus Banks)

Concepts reviewed: A (Quiet), B (Bold), C (Author-led)

Winning concept: ☐ A (Quiet) / ☐ B (Bold) / ☐ C (Author-led)

Concept test generation count: [N of 8 max]
Backups used: [none / 1 quality / 1 variant / both]

Concept A score: __/25
Concept B score: __/25
Concept C score: __/25

Notes for Priority A production:
_________________________________________________

Approve to begin Priority A production?
☐ YES, proceed with [winning concept]
☐ HOLD, request revisions (specify)
☐ REJECT, new concept test needed (specify why)
```

The CDO will not begin Priority A work until this template is filled out and returned.

---

## 12. Approval Status

| Checkpoint | Status |
|------------|--------|
| v0.2 prompt pack written | COMPLETE 2026-06-06 |
| v0.1 marked SUPERSEDED | COMPLETE 2026-06-06 |
| CEO review of v0.2 prompt pack | PENDING |
| Round 1 image generation (manual) | NOT STARTED |
| Concept decision | PENDING (after Round 1 review) |
| Round 2 prompt pack (IG + email) | NOT STARTED — drafted after concept decision |
| Priority A production | BLOCKED until concept decision is locked |
| Author photo session (A13-A15) | BLOCKED — pending separate CEO approval |

---

## Change Log

- **v0.2 (2026-06-06):** Reconciled prompt count to 6-8 budget. Cut active prompts from 12 to 6 (3 LP hero + 3 social ad). Added 2 backup rules (quality recovery + strongest concept variant). Moved 6 IG and email header prompts to a deferred Round 2 section. Added manual generation run sheet. Added upload/review instructions. Removed Playwright automation path (CDO cannot safely automate DALL-E; CEO runs it manually). CEO also explicitly asked for the 12-vs-6/8 inconsistency to be reconciled — this is the reconciliation.
- **v0.1 (2026-06-06):** Initial 12-prompt pack. **SUPERSEDED 2026-06-06** by v0.2. Retained for history. The 12-prompt / 6-8 budget mismatch was a real CDO V3.1 self-audit failure and v0.2 fixes it.

---

**Last updated:** 2026-06-06
**Owner:** CDO (exec-cdo)
**Next action:** CEO reviews this v0.2 prompt pack. If approved, CEO runs the 6-step manual generation run sheet (section 8). No automation. No Priority A. No photo session spend. A13-A15 stay blocked.
