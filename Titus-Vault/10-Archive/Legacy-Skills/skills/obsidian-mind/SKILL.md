---
name: obsidian-mind
description: "Use for Obsidian-backed long-term memory in Claude Code: each conversation builds structured, linked notes in Obsidian vault. Performance tracking, automatic indexing, works with CLI and Gemini. Local file writes only."
origin: OpenSource Research
version: 0.1.0
---

# Obsidian Mind

Long-term memory layer for Claude Code using Obsidian vault. Each conversation builds on the last via structured, linked notes. Performance tracking, automatic indexing.

## When to Activate

- Start new project or conversation thread
- Need persistent context across sessions
- Want automatic note linking and indexing
- Need performance tracking over time

## Behavior

1. Detect or create Obsidian vault for project
2. Create/update daily note with conversation summary
3. Link concepts, decisions, and tasks across notes
4. Maintain index of all topics, people, projects
5. Track performance metrics: tokens, time, quality
5. All writes local to vault — no cloud sync by default

## Safety

- Local file writes only — no external sync without approval
- No sending vault contents to external APIs
- No auto-commit to git without approval
- Respects `.obsidian-ignore` patterns

## Integration

- Works with `claude-mem` for memory layer
- Works with `continuous-learning-v2` for pattern evolution
- Complements `memory-optimization` for context management
- Uses `/remember` command for manual capture

## Example Triggers

- "Start tracking this project in Obsidian."
- "Summarize today's work in my vault."
- "Link this decision to the project note."
- "Show me performance trends for this week."
