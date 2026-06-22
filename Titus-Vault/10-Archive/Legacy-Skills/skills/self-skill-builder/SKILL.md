---
name: self-skill-builder
description: "Use when the user wants the agent to propose new reusable skills from repeated workflows. Extends existing skill-creator and memory-optimization skills. Proposes only — never self-installs without approval."
origin: OpenSource Research
version: 0.1.0
---

# Self-Skill Builder

Extends `skill-creator` and `memory-optimization` for autonomous skill proposal. Analyzes repeated workflows, proposes new skills, logs proposals. **Never self-installs** without explicit user approval.

## When to Activate

- User repeats a workflow 3+ times
- User asks "make this a skill"
- Pattern detection in session logs
- User wants to capture a reusable workflow

## Behavior

1. Analyze session history for repeated patterns (via `memory-optimization` / `claude-mem`)
2. Propose skill name, trigger, workflow, safety rules
3. Present proposal to user for approval
4. On approval, create skill file in appropriate directory
5. Register in appropriate system (Claude Code)
5. Log proposal and outcome in memory

## Safety

- **Never self-installs** without explicit user approval
- Never modifies existing skills without approval
- Never creates skills that send messages, spend money, or delete files
- All proposals logged with timestamp and context
- User can reject or modify any proposal

## Integration

- Uses `skill-creator` skill for skill structure
- Uses `memory-optimization` / `claude-mem` for pattern detection
- Uses `continuous-learning-v2` for pattern evolution

## Example Triggers

- "This workflow keeps repeating, make it a skill."
- "Propose a skill for my morning routine."
- "What patterns am I repeating this week?"
