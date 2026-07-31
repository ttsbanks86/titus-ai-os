# M3 Design Authority Map

**Date:** 2026-07-31
**Status:** Complete

---

## Authority Hierarchy

### Level 1: Canonical Brand Reference

**`BRAND/Brand-System/Master-Brand-Standards.md`**

- Defines brand essence, visual system, voice, sub-brand architecture
- Status: v0.1 DRAFT (awaiting CEO ratification)
- Governs: All Titus Banks visual and voice decisions
- Override requires: CEO sign-off

### Level 2: Machine-Readable Tokens

**`BRAND/tokens.json`**

- Colors, typography scale, spacing, logo rules, photography, iconography
- Status: v0.1.0
- Consumers: VistaCreate, Figma, Web, Documents
- Override requires: CDO approval

### Level 3: Implementation Design System

**`BRAND/DESIGN.md`**

- Components, states, motion, accessibility, content rules
- Status: Complete
- Note: Uses Inter for all typography (practical default until CEO picks display font)
- Override requires: CDO approval

### Level 4: Open Design Package

**`BRAND/Open-Design/design-systems/titus-open-door/`**

- Reusable Open Design system for dashboards and command centers
- Status: Established
- Includes: DESIGN.md, open-design.json manifest

### Level 5: Sub-Brand Variants

**`TitusVideoStudio/docs/DESIGN_SYSTEM.md`**

- Dark-mode variant for Titus Video Studio
- Status: Complete
- Scope: TVS only, does not override master

---

## Titus AI OS Design Authority

For M3 implementation, the Titus AI OS interface follows:

1. **Master Brand Standards** for colors, typography, voice
2. **DESIGN.md** for components, states, motion, accessibility
3. **tokens.json** for CSS variable values
4. **Open Design package** for dashboard layout patterns

### Color Assignment (Titus AI OS)

| Element | Color | Source |
|---------|-------|--------|
| Page background | Cream `#F5F1E8` | Master Brand Standards |
| Navigation | Navy `#0F2742` | Master Brand Standards |
| Primary actions | Gold `#D4A14A` | Master Brand Standards |
| Success states | Green `#1F6B4A` | Master Brand Standards |
| Body text | Off-Black `#0E1116` | Master Brand Standards |
| Secondary text | Slate `#5A6B7B` | Master Brand Standards |
| Card backgrounds | White `#FFFFFF` | DESIGN.md |
| Error states | Red `#DC2626` | DESIGN.md |
| Focus rings | Gold `#D4A14A` | Master Brand Standards |

### Typography Assignment (Titus AI OS)

| Element | Font | Weight | Source |
|---------|------|--------|--------|
| Body | Inter | 400-500 | DESIGN.md (practical default) |
| Headings | Inter | 700-800 | DESIGN.md (practical default) |
| Code | JetBrains Mono | 400 | DESIGN.md |
| Display | TBD | 700 | Awaiting CEO font decision |

---

## Cross-Project Reuse Rules

1. All Titus projects share the master color palette
2. Sub-brands differentiate by accent color and motif, not by inventing new palettes
3. Titus AI OS uses the light theme (cream background) as default
4. Dark mode variant follows TVS/JARVIS pattern (Navy Deep backgrounds)
5. Component library is shared across projects via DESIGN.md
6. No project may override Master Brand Standards without CEO approval
