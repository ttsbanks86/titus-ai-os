# Video Intelligence — Tips & Tricks from the Pros

## From Jonny Burger (Remotion Creator)

### 1. Build for Reuse
"Almost any complexity in React can be abstracted, packaged up, and shared."
**Adopt:** Create reusable composition templates (intro card, caption style, lower third) so we don't start from scratch every time.

### 2. Higher-Level Components
"The number one feedback is simple things can be hard. We need higher-level components."
**Adopt:** Build a library of clip templates — title cards, bullet lists, stat displays, credit rolls — that just need text swapped in.

### 3. Start Simple, Add Polish Later
"Low-level primitives will always be here."
**Adopt:** Get the script and captions working first. Add animations and visual flair after the foundation is solid.

### 4. Think in Layers
Remotion's power is composability — scenes, sequences, and components stacked together.
**Adopt:** Our compositions should be modular — background layer, text layer, overlay layer, audio layer. Each independent.

### 5. Deterministic Rendering
"It only works if everything is predictable — no Date.now(), no Math.random()."
**Adopt:** Every animation needs fixed timing. We're already doing this with GSAP timelines.

---

## From HyperFrames / HeyGen Team

### 1. Layout Before Animation
"Position every element at its most visible moment first. Then animate."
**Adopt:** Build the end state in CSS before writing a single GSAP tween. We did this in PROMPT-MINE.

### 2. Container-First Sizing
"The .scene-content container MUST fill the full scene using flex + padding."
**Adopt:** Never use absolute positioning for content. Use flex containers with padding.

### 3. Same-Track, No Overlap
"Same-track clips cannot overlap."
**Adopt:** Use track indexes wisely — voiceover on track 2, captions on track 4, visuals on track 3.

### 4. Variables for Reuse
"Render the same composition with different content without editing HTML."
**Adopt:** Use `data-composition-variables` for reusable templates — different titles, colors, text per video.

### 5. Check Before Render
"Lint, inspect, then render."
**Adopt:** Always run `npm run check` before rendering to catch text overflow and timing issues.

### 6. Audio Drives Duration
"Let audio length dictate the composition duration, not the other way around."
**Adopt:** Write script → generate TTS → measure duration → build composition to fit the audio.

---

## From Ivy (61 Learning AI)

### 1. Post 3x/Day for $0.30/month
She uses Claude Code + Remotion to generate and batch-render videos.
**Adopt:** Batch scripts → batch TTS → batch compositions → batch render. One setup, many outputs.

### 2. Script-First Pipeline
"Write the script, the video builds itself."
**Adopt:** Our pipeline should be: write 200 words → TTS → transcribe → compose → render. One-shot.

### 3. Don't Overcomplicate
"Most of my videos are text + voice + background."
**Adopt:** Not every video needs complex visuals. A clean caption video with good audio beats a cluttered animation.

---

## Our Adopted Workflow

```
1. Write script (200-300 words)
2. Generate TTS → narration.wav
3. Transcribe → transcript.json (word timestamps)
4. Build composition HTML with captions synced to timestamps
5. Add background visuals
6. Add entrance/exit animations
7. Run npm run check
8. Preview in studio
9. Render to MP4
```

## Template Library to Build

| Template | Use |
|----------|-----|
| Intro card | Title + subtitle + gradient bg |
| Caption sequence | Synced captions over gradient |
| Talking points | Bullet list with icons |
| End card | Call to action + branding |
| Stat highlight | Big number + label |
| Quote card | Pull quote + attribution |

---

*Last updated: June 11, 2026*