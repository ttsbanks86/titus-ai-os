# M3 OpenCode Customization Decision

**Date:** 2026-07-31
**Status:** Decided

---

## Decision

**Do not customize OpenCode directly. Build a standalone dashboard.**

## Rationale

1. OpenCode is a TUI (Terminal User Interface), not a web app
2. Customizing the TUI would require forking OpenCode
3. Forking creates upgrade maintenance burden
4. A standalone web dashboard provides better UX for project oversight
5. The dashboard can read from the same Knowledge Engine (M2) modules

## Alternative Approaches Considered

### Option A: Fork OpenCode TUI
- **Pros:** Integrated experience
- **Cons:** High maintenance, upgrade risk, TUI limitations
- **Verdict:** Rejected

### Option B: OpenCode Plugin/Skill
- **Pros:** No fork needed, uses existing system
- **Cons:** Limited UI capabilities, terminal-based
- **Verdict:** Rejected for dashboard, kept for backend operations

### Option C: Standalone Web Dashboard (CHOSEN)
- **Pros:** Full UI control, brand compliance, accessible, responsive
- **Cons:** Separate app to run, two UIs to maintain
- **Verdict:** Accepted

### Option D: Electron Desktop App
- **Pros:** Native feel, offline capable
- **Cons:** Heavy, complex build, overkill for MVP
- **Verdict:** Deferred to future consideration

## Implementation Notes

- Dashboard runs on `localhost:3000`
- API server runs on `localhost:8000`
- Both are started with a single script
- No changes to OpenCode itself
- OpenCode continues to work as before
- Dashboard provides the "understandable" layer on top

## Upgrade Path

- OpenCode upgrades do not affect the dashboard
- Dashboard can be upgraded independently
- M2 Knowledge Engine modules are shared
- No fork maintenance required
