---
name: no-gold-plating
description: Keep Claude Fable 5 changes minimal — no unrequested refactors, abstractions, defensive code, or feature creep. Use in code review, bug fixes, and any coding session where diffs come back bigger than the ask, with extra helpers, error handling, or "while I was here" cleanup. Particularly important at high and xhigh effort.
---

# No Gold-Plating

At higher effort, Fable 5's thoroughness can spill over into the diff: speculative abstractions, defensive checks for impossible states, cleanup nobody requested. Each of these enlarges review surface and risk. The discipline:

## Think Before Coding (Karpathy Rule 1)

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## Verify Before Calling Done (Karpathy Rule 4)

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan with verification:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

## Rules

- The diff should map one-to-one to the request. A bug fix touches the bug; it does not reorganize the neighborhood.
- No helpers, layers, or abstractions for a single call site. Inline it.
- Do not design for requirements that don't exist yet. The simplest correct implementation wins; generality is a cost paid today for a benefit that may never arrive.
- Validate only at system boundaries — user input, external APIs, file contents. Inside the system, trust the framework and your own invariants; do not add error handling for states that cannot occur.
- Prefer changing code over compatibility shims, flags, or deprecation layers, unless the code is a published interface someone else depends on.
- If you notice genuinely valuable adjacent work, note it in one sentence at the end. Do not do it.

## Self-check before finalizing a diff

1. Could a reviewer trace every hunk back to the user's request in one step?
2. Did I add any function, parameter, or branch "just in case"?
3. Is any new error-handling path actually reachable?

If any answer is wrong, cut it.
