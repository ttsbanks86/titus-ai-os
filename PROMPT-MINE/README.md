# PROMPT-MINE

**Prompt Mining & Intelligence Engine**

A living reference of AI system prompt patterns extracted from the world's best AI tools. Built to make our AI stack smarter.

---

## Why This Matters

Every major AI tool (Claude, ChatGPT, Gemini, Grok, Copilot) follows a hidden instruction set called a **system prompt**. These prompts have grown from 74 words (ChatGPT 2022) to 10,000+ words (2026). They represent millions of dollars in R&D — patterns that companies discovered through trial and error.

We're mining those patterns and injecting them into our stack.

---

## The Universal Three-Layer Architecture

Every successful AI system prompt follows this structure:

### Layer 1: Identity & Context
*Who the AI is, where it comes from, what it knows*

Example pattern:
```
You are [NAME], created by [COMPANY]. 
Current date: [DATE]. Knowledge cutoff: [DATE].
You are an AI assistant with expertise in [DOMAIN].
```

**What we can use:** Every agent in our stack should know exactly who it is. Our agents currently lack clear identity definitions.

### Layer 2: Capabilities & Constraints
*What the AI can and cannot do*

Example pattern:
```
You have access to the following tools:
- [TOOL_NAME]: [DESCRIPTION]
- [TOOL_NAME]: [DESCRIPTION]

You cannot: [LIMITATIONS]
```

**What we can use:** Our agents need clearer boundaries. Currently they just have tool access but no explicit "don't do this" rules.

### Layer 3: Behavioral Guidelines
*How to interact, handle edge cases, format responses*

Example pattern:
```
- Never start responses with flattery ("great question")
- Be concise but thorough
- If you cannot fulfill a request, offer an alternative
- Avoid over-formatting with lists and bullet points
```

---

## Key Patterns We're Using

### 1. The Agent Loop Pattern
```
ANALYZE → PLAN → EXECUTE → OBSERVE → ITERATE
```
Used by: Manus, Cursor, Windsurf, Gemini CLI

**Apply to:** Our Personal AI Operator should use this exact loop instead of linear execution.

### 2. Anti-List Bias
```
Avoid using pure lists and bullet points format in any language.
Never have a list with only one single solitary bullet.
Claude avoids over-formatting responses with bold emphasis, headers, lists.
```

**Apply to:** Our agents should format responses naturally, not as bullet-point machines.

### 3. Constructive Refusal Pattern
```
Instead of "I can't help with that" → 
"I can't help with [X], but if you're interested in [Y], I can help with that."
```

**Apply to:** When our agents can't fulfill a request, they should redirect, not just refuse.

### 4. Memory Architecture (Three Rules)
```
1. Explicit consent — Only save what user volunteers
2. Structured storage — Tag with categories and timestamps
3. Selective recall — Load only relevant memories per session
```

**Apply to:** Our claude-mem system follows this already, but we can tighten it.

### 5. Tool-as-API Pattern
```
edit_file(target_file: string, instructions: string, code_edit: string) -> result
```

**Apply to:** Our tools should have typed signatures, not loose descriptions.

---

## Quick Reference: 10-Minute Study

| Pattern | What It Does | Use In |
|---------|-------------|--------|
| Identity Layer | Sets who the agent is | All agents |
| Agent Loop | Plan → Do → Check → Repeat | AI Operator |
| Anti-List | Natural formatting | All responses |
| Refusal Redirect | Say no + offer alternative | All agents |
| Memory Rules | What to remember/forget | claude-mem |
| Tool Signatures | Typed function definitions | OpenCode tools |
| Correction Layer | Override default AI habits | System prompts |

---

## How to Apply These

1. **Identity Layer** — Add to agent descriptions in OpenCode config
2. **Agent Loop** — Restructure AI Operator to use the loop pattern
3. **Anti-List** — Add instruction to CLAUDE.md
4. **Refusal Redirect** — Add to agent behavioral guidelines
5. **Memory Rules** — Already partially implemented in claude-mem
6. **Tool Signatures** — Update tool descriptions to be typed APIs

---

*Last Updated: June 11, 2026*