# Video Production Guide

## Asset Sources (Free)

### Background Videos
- **Pixabay** (pixabay.com/videos) — 2M+ free stock videos, no attribution
- **Pexels** (pexels.com/videos) — HD/4K stock footage
- **Mixkit** (mixkit.co) — Free motion graphics, transitions, overlays
- **Coverr** (coverr.co) — Free background clips

### Music & Sound Effects
- **Uppbeat** (uppbeat.io) — Free background music with attribution
- **Pixabay Music** (pixabay.com/music) — Free, no attribution
- **Mixkit Music** — Free SFX and loops

### Icons & Graphics
- **Font Awesome** (fontawesome.com) — Free SVG icons
- **Canva** (canva.com) — Templates, export PNG/SVG

---

## Our Template System

We have 4 reusable templates in `templates/MASTER-TEMPLATE.html`:

| Template | Duration | Purpose |
|----------|----------|---------|
| Intro Card | 4s | Title + subtitle with animated background |
| Caption Sequence | 20s | Synced captions over tech background |
| Stat Highlight | 5s | Big number + label with scale animation |
| End Card | 4s | Name, title, portfolio URL |

Total: 33s template capacity

---

## Production Pipeline

```
Step 1: Write script.txt (200-300 words)
Step 2: npx hyperframes tts script.txt --voice [voice] --output narration.wav
Step 3: python transcribe.py (generates transcript.json with timestamps)
Step 4: Build composition in index.html using templates
Step 5: Preview in studio (npm run dev)
Step 6: npm run check (lint + validate)
Step 7: npx hyperframes render (output to renders/)
```

## Quick Start for New Video

1. Copy `templates/MASTER-TEMPLATE.html` patterns into `index.html`
2. Replace text in title, captions, and end card
3. Match caption timestamps to transcript segments
4. Set `data-duration` on root div to match narration length + 2s
5. Preview in studio
6. Render to MP4

## Voice Selection

| Vibe | Voice |
|------|-------|
| Professional/Warm | af_nova |
| Energetic/Auth | af_sky |
| Neutral/Tutorial | bf_emma |
| Deep/Authoritative | am_michael |