# M4 Branding Audit & Theme Mapping

**Date:** 2026-07-31
**Milestone:** M4 — Hybrid OpenCode Integration and Unified Startup
**Status:** AUDIT COMPLETE — REUSE, no new brand assets created

---

## 1. Existing Brand System (verified, current)

| Asset | Location | Content |
|-------|----------|---------|
| Design tokens (canonical) | `BRAND\tokens.css` | Full token set: color, typography, spacing, radius, elevation, status, alerts, table, layout; dark mode block |
| Design system | `BRAND\DESIGN.md` | Design principles + guidance |
| Master brand standards | `BRAND\Brand-System\Master-Brand-Standards.md` | Voice, identity, standards |
| Sub-brand differentiation | `BRAND\Brand-System\Sub-Brand-Differentiation.md` | Brand hierarchy |
| Titus AI OS design system | `BRAND\Open-Design\design-systems\titus-ai-os\DESIGN.md` | Product-specific guidance |

**Decision: REUSE.** No new tokens needed. OpenCode theming consumes a subset of the existing palette.

## 2. Canonical Tokens (source of truth)

| Token | Value | Role |
|-------|-------|------|
| `--color-navy` | `#0F2742` | Primary, headings, anchors |
| `--color-navy-deep` | `#0A1B30` | Deepest background |
| `--color-gold` | `#D4A14A` | Accent, CTA, premium |
| `--color-gold-soft` | `#E8C98A` | Hover, gradients |
| `--color-green` | `#1F6B4A` | Success |
| `--color-slate` | `#5A6B7B` | Secondary text |
| `--color-cream` | `#F5F1E8` | Light background |
| `--color-white` | `#FFFFFF` | Cards |
| `--color-off-black` | `#0E1116` | Body text on light |
| `--status-blocked` | `#DC2626` | Error/blocked |
| `--status-review` | `#7C3AED` | Review/pending decision |
| `--font-display` | Playfair Display | Display type |
| `--font-body` | Inter | Body type |

## 3. OpenCode Theme Mapping (Phase G deliverable: `themes/titus.json`)

OpenCode JSON theme tokens → Titus palette. Dark theme is the primary (terminal native).

### Dark theme (primary)
| OpenCode token | Titus token | Value |
|----------------|-------------|-------|
| `background` | navy-deep | `#0A1B30` |
| `backgroundSidebar` | navy | `#0F2742` |
| `foreground` | cream | `#F5F1E8` |
| `foregroundMuted` | slate | `#94A3B8` (dark-mode slate per tokens.css dark block) |
| `primary` | gold | `#D4A14A` |
| `primaryForeground` | navy-deep | `#0A1B30` |
| `secondary` | gold-soft | `#E8C98A` |
| `accent` | gold | `#D4A14A` |
| `border` | navy (lightened) | `#1E3A5F` |
| `sidebarBackground` | navy | `#0F2742` |
| `sidebarForeground` | cream | `#F5F1E8` |
| `sidebarActive` | gold-soft | `#E8C98A` |
| `selectionBackground` | gold @ 25% | `#D4A14A40` |
| `markdown.code` | slate-light | `#94A3B8` |
| `syntax.*` | cream/gold/slate family | `#F5F1E8`, `#D4A14A`, `#E8C98A`, `#94A3B8` |
| `diff.added` | green | `#1F6B4A` |
| `diff.removed` | status-blocked | `#DC2626` |
| `success` | green | `#1F6B4A` |
| `error` | status-blocked | `#DC2626` |
| `warning` | gold | `#D4A14A` |

### Light theme (secondary, for daylight use)
| OpenCode token | Titus token | Value |
|----------------|-------------|-------|
| `background` | cream | `#F5F1E8` |
| `foreground` | off-black | `#0E1116` |
| `primary` | navy | `#0F2742` |
| `accent` | gold | `#D4A14A` |
| `sidebarBackground` | navy | `#0F2742` |
| `sidebarForeground` | white | `#FFFFFF` |
| `border` | table-border | `#E2E8F0` |

**Note:** Theme token names are validated against the live theme schema before writing (Phase G step: create theme file, run `opencode` to confirm no theme load errors, screenshot-verify via TUI).

## 4. Selection Mechanism

- `~/.config/opencode/tui.json` → `"theme": "titus"` (dark) — user can toggle with `/theme` at runtime.
- Keep the stock `opencode` theme available; Titus theme is an overlay, not a replacement.

## 5. Guardrails Applied

1. No new brand tokens created — only mapped.
2. Gold used as accent only (CTA/selection/active), never as background wash — matches brand guardrails.
3. Cream/off-black light theme is secondary; terminal sessions default to dark (navy-deep) per brand dark-mode block.
4. No fonts changed in TUI (terminal font is user-controlled; brand serif/body fonts apply to web surfaces only — dashboard already uses them via tokens.css).

## 6. Acceptance Criteria

1. `themes/titus.json` loads without errors in OpenCode.
2. Theme appears in `/theme` switcher.
3. Primary/accent/sidebar/selection visible per mapping above.
4. Light variant selectable.
5. No impact on existing dashboard branding (separate surface).
