# AI Image Prompt Pack — Titus Banks

**Owner:** CDO (exec-cdo)
**Status:** Master Brand System v0.1 (Priority 2 expansion)
**Last updated:** 2026-06-06

This is the prompt library for AI image generators (DALL-E 3 via ChatGPT, Leonardo.ai, Writeseed, Ideogram, Midjourney, etc.). Every prompt here bakes in the master brand rules, the voice rules, and the per-platform quirks. Copy a prompt, customize the bracketed variables, and ship.

---

## The Brand Prompt Suffix (paste at the end of every prompt)

```
Style: Warm, natural, dignified. Cream background #F5F1E8 with navy #0F2742 and gold #D4A14A accents. No people unless explicitly requested. No stock-photo smiles. No em dashes or typographic flourishes. No text in the image unless explicitly requested. Composition: clean, generous whitespace, real-world feel. 8K, photorealistic or tasteful editorial illustration.
```

This suffix is non-negotiable. The CDO appends it to every prompt to keep brand consistency across AI outputs.

---

## Platform Quirks

| Platform | Quirk | Adjustment |
|----------|-------|------------|
| **DALL-E 3 (ChatGPT)** | Excellent prompt adherence, refuses brand-faith combinations sometimes | Lead with what you want, not what you don't. If refused, simplify the prompt and try again. |
| **Leonardo.ai** | Higher quality, more control, costs tokens | Use for hero/marketing pieces. Save DALL-E for iteration. |
| **Writeseed** | Cheaper, decent quality, less consistent | Use for one-off social graphics and carousel frames. |
| **Ideogram** | Best for text-in-image, sometimes generic look | Use when the asset has a quote or label baked in. |
| **Midjourney** | Best aesthetic, hardest to control | Use for "vibe" explorations, not final assets. |

---

## Prompt Templates by Use Case

### U1. Book Cover / Hero Image (Struck Down)

**Variables:** subject, mood, primary_color

```
A dignified, faith-rooted book cover for "[BOOK TITLE]" by [AUTHOR]. 
Subject: [SUBJECT — e.g., a man kneeling in prayer, a single candle in a window, a father holding a child's hand].
Mood: [MOOD — e.g., quiet strength, hope after struggle, dignified grief].
Composition: [COMPOSITION — e.g., subject in lower third, soft golden light from upper left, generous negative space at top for title placement].
Style: Editorial photography, warm natural light, no faces shown unless specified, real-world textures (not over-stylized).
[BRAND SUFFIX]
```

**Example for Struck Down:**
```
A dignified, faith-rooted book cover for "Struck Down but Not Destroyed" by Bonolo Morake. 
Subject: a single open Bible on a worn wooden table, lit by a single candle, with a faint golden light coming from above. A small hand is just visible at the edge of the frame.
Mood: quiet strength, hope after loss, dignified grief.
Composition: Bible in lower-center, candle to its right, large negative space in upper third for title placement.
Style: Editorial photography, warm natural light, real-world textures, no posed people.
[BRAND SUFFIX]
```

### U2. Facebook Ad / Lead Magnet (1080x1080 or 1200x628)

**Variables:** hook_text, audience, benefit, cta_text

```
A Facebook ad image for a faith-rooted personal brand. 
Hook image shows: [SCENE — e.g., a tired father at a kitchen table, a woman with a laptop at a coffee shop, a hand holding an open Bible].
Mood: [MOOD — e.g., relatable, warm, hopeful, calm authority].
Composition: [COMPOSITION — e.g., subject on right third, clean negative space on left for text overlay].
Aspect ratio: 1:1 (or 1200x628 horizontal).
[BRAND SUFFIX]
No text in the image — text will be added in Canva/VistaCreate. 
Style: photorealistic editorial, warm color grading.
```

### U3. Instagram Post / Quote Background (1080x1080)

**Variables:** quote_topic, mood, accent_color

```
A soft, dignified background image for an inspirational Instagram post. 
Subject: [SCENE — e.g., a single tree against a morning sky, a coffee cup on an open book, hands folded in prayer, an open window with morning light].
Mood: [MOOD — e.g., quiet, hopeful, reflective, calm].
Composition: Center-weighted, generous whitespace for text overlay, no busy edges.
Aspect ratio: 1:1.
[BRAND SUFFIX]
```

### U4. Instagram Story / Sequence (1080x1920, 5 frames)

**Variables:** story_topic, frame_count

```
A series of [N] Instagram story frames telling a single visual story about [TOPIC — e.g., "5 truths about leading your family in faith"].
Each frame should:
- Maintain the same color palette (cream, navy, gold) and visual language.
- Have a single dominant element per frame.
- Use a consistent visual motif throughout the series (e.g., hands, a single object, morning light).
- Feel like a sequence when viewed side-by-side.
Aspect ratio: 9:16 (1080x1920).
[BRAND SUFFIX]
Style: editorial, warm, real-world.
```

### U5. Landing Page Hero (1920x1080 or 1440x720)

**Variables:** landing_purpose, focal_element

```
A landing page hero image for [PURPOSE — e.g., a faith-rooted business analysis course, a devotional PDF download, the Struck Down book sales page].
Focal element: [ELEMENT — e.g., an open laptop with a clean process diagram, a book in 3D, a hand holding a small plant].
Mood: [MOOD — e.g., confident, calm, trustworthy, premium].
Composition: Right-third subject, left-third clean negative space for headline and CTA overlay.
Aspect ratio: 16:9 (1920x1080).
[BRAND SUFFIX]
Style: editorial, premium, real.
```

### U6. YouTube Thumbnail (1280x720)

**Variables:** video_topic, emotion, face_or_object

```
A high-contrast, click-worthy YouTube thumbnail for a video titled "[VIDEO TITLE — e.g., How I Built a Business Analyst Career from Scratch]".
Focal element: [ELEMENT — e.g., a face showing [EMOTION] OR an object like a laptop with a process diagram, oversized red arrow, before/after split].
Composition: Big visual on the right 60%, negative space on left 40% for text overlay (text added separately in Figma).
Aspect ratio: 16:9 (1280x720).
[BRAND SUFFIX]
Style: high-contrast, editorial, eye-catching but not clickbait.
NOTE: Use DALL-E or Ideogram for thumbs; Leonardo for higher-quality hero work.
```

### U7. BA / PM Carousel Frame (1080x1080, one of N frames)

**Variables:** slide_number, slide_topic, layout

```
A single Instagram carousel frame (one of [N] total) for a [TOPIC — e.g., Business Analyst, Project Management, AI at Work] educational series.
Frame [N]: [FRAME_TOPIC — e.g., "The 5 questions every BA should ask in requirements gathering"].
Composition: Top 1/8: small numbered badge "[N]/[TOTAL]" in gold. Center 6/8: clean diagram or single concept visualization. Bottom 1/8: subtle space for "@titusbanks" handle (added separately).
Aspect ratio: 1:1 (1080x1080).
[BRAND SUFFIX]
Style: clean editorial, real-world references, professional but not corporate.
```

### U8. Pitch Deck / Slide Background (1920x1080)

**Variables:** slide_topic, mood

```
A subtle, dignified background image for a pitch deck slide about [TOPIC].
Subject: [SUBJECT — e.g., abstract light through frosted glass, hands at a table, a single open book, an open laptop on a clean desk].
Mood: [MOOD — e.g., confident, premium, trustworthy, calm authority].
Composition: Soft focus, low contrast, no sharp focal point (the slide text will dominate).
Aspect ratio: 16:9 (1920x1080).
[BRAND SUFFIX]
Style: editorial, low-contrast background, real-world.
```

### U9. Icon / Spot Illustration (small, square or icon-shaped)

**Variables:** concept, style

```
A simple, dignified spot illustration of [CONCEPT — e.g., "open Bible," "father and child hand-in-hand," "pathway through trees," "open door," "blueprint corner," "hammer and laptop"].
Style: line art with subtle navy fill, cream background, hand-drawn but clean.
[BRAND SUFFIX]
Style: editorial illustration, restrained, modern.
NOTE: Prefer custom icon design over AI for this size; AI works for exploration.
```

### U10. Email Header (1500x600 or 600x200)

**Variables:** email_topic, mood

```
A horizontal email header image for [EMAIL_TOPIC — e.g., weekly newsletter, course launch, book update].
Subject: [SUBJECT — e.g., open Bible and coffee, single tree, hands at work, open laptop on a desk].
Mood: [MOOD — e.g., warm, weekly, calm].
Composition: left-weighted, generous right-side space for headline overlay.
Aspect ratio: 5:1 (1500x600) or 3:1 (600x200).
[BRAND SUFFIX]
Style: editorial, warm, restrained.
```

---

## Negative Prompt Library (use when supported)

Leonardo, Midjourney, and some others accept negative prompts. Paste this when needed:

```
Negative: stock photo, businessperson, suit, hand shake, boardroom, generic, fake smile, oversaturated, neon, dark and gritty, horror, sexualized, cartoonish, AI-looking face, mannequin, plastic skin, distorted hands, watermarks, text artifacts, low resolution, blurry, lens flare, generic corporate, infographic-style, emoji.
```

---

## Quality Self-Check (run after every generation)

1. Is the brand suffix honored? (cream + navy + gold or compatible accent)
2. Is the composition clean and generous in whitespace?
3. Does the image look real-world and dignified?
4. Would a stranger see it and know it's Titus Banks?
5. Is the emotional register right for the use case?
6. Are there any banned visual elements (stock smile, oversaturation, fake face)?
7. Is the resolution sufficient for the use case (4K for print, 1080+ for digital)?
8. Are hands, faces, and human elements natural and not uncanny?

If 6+ of 8 are yes, the asset is approved for production. If not, regenerate or move to a different platform.

---

## Cost & Token Tracking

- Every generation logged in `BRAND/AI-Prompts/Generation-Log.md`.
- Leonardo: 134 tokens remaining. Per CDO V3.1: alert at 50, stop at 20.
- DALL-E: 10 generations per 24h window per CDO V3.1.
- Writeseed: alert at 20% remaining, stop at 10%.
- Midjourney: not yet enabled (no cost approval).

---

## Cross-References

- `BRAND/Brand-Voice-Cheatsheet.md` — copy rules
- `BRAND/tokens.json` — color values
- `BRAND/Brand-System/Master-Brand-Standards.md` — full visual system
- `BRAND/Brand-System/Sub-Brand-Differentiation.md` — sub-brand accents
- `BRAND/Asset-Library-Index.md` — what assets already exist

---

## Change Log

- 2026-06-06 — v0.1 created. 10 use-case prompt templates + brand suffix + negative prompt + quality check.
