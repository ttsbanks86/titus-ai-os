# Titus Open Door Design System

> Category: Faith-rooted AI operations, professional services, product dashboards, executive systems.
> Use for Titus Banks, The Open Door AI Systems, Divine Works Hub, Faithful Journey Quest, JARVIS, book marketing, career assets, and practical AI operations products unless a more specific sub-brand overrides it.

## 1. Visual Theme and Atmosphere

This design system is premium, grounded, warm, and operational. It should feel like a trusted executive command center and a practical consulting brand, not a generic AI startup. The work should communicate clarity, follow-through, calm authority, and useful leverage.

The visual language combines deep navy structure, measured gold emphasis, cream surfaces, readable typography, and restrained interface detail. Designs should feel professional enough for a Fortune 500 briefing, warm enough for a faith-rooted founder brand, and practical enough for small business operators.

### Key Characteristics
- Deep navy foundations with cream or white working surfaces.
- Gold accents used for decisions, calls to action, premium emphasis, and focal points.
- Practical layout rhythm: clear hierarchy, scannable sections, no visual clutter.
- Executive dashboard feel for operational tools, with calm signals and useful status states.
- Warm human tone for public-facing assets.
- No hype, no generic neon AI imagery, no overused SaaS gradients.
- Faith-rooted dignity: hopeful, honest, family-friendly, never manipulative or vulgar.

## 2. Color Palette and Roles

### Primary
- **Navy** (`#0F2742`): Primary background, headers, sidebars, executive surfaces.
- **Navy Deep** (`#0A1B30`): Heavy contrast, hero sections, command-center panels.
- **Cream Surface** (`#F5F1E8`): Warm light backgrounds, cards, editorial sections.
- **White** (`#FFFFFF`): Clean surfaces, dark-background text, high-clarity panels.

### Accent
- **Gold** (`#D4A14A`): Primary accent, CTA fill, premium highlight, focal rules.
- **Gold Soft** (`#E8C98A`): Secondary accent, hover states, subtle backgrounds.
- **Green Success** (`#1F6B4A`): Success, growth, confirmation, healthy status.

### Text and Neutral
- **Off Black** (`#0E1116`): Primary text on light surfaces.
- **Slate** (`#5A6B7B`): Secondary text, metadata, helper copy.
- **Border Sand** (`#DDD4C3`): Borders on cream and white surfaces.
- **Muted Navy** (`#29435F`): Secondary panels, inactive controls, chart support.

### Semantic Colors
- **Success:** `#1F6B4A`
- **Warning:** `#B7791F`
- **Error:** `#B42318`
- **Info:** `#2563EB`

### Color Rules
- Use gold sparingly. If everything is gold, nothing is important.
- Never place gold text on cream unless contrast is verified.
- Use navy for trust and structure, cream for warmth, white for clarity.
- Color is never the only status signal. Pair color with text, icon, shape, or label.

## 3. Typography Rules

### Font Family
- **Primary UI and body:** `Inter`, fallback `Segoe UI, Arial, sans-serif`.
- **Display and editorial headings:** `Inter Tight`, fallback `Inter, Segoe UI, Arial, sans-serif`.
- **Monospace for code or system output:** `JetBrains Mono`, fallback `Consolas, monospace`.

### Hierarchy
| Role | Size | Weight | Line Height | Notes |
|---|---:|---:|---:|---|
| Hero XL | 64px | 700 | 1.03 | Landing pages and launch pages. |
| Hero L | 52px | 700 | 1.06 | Desktop hero and executive pages. |
| Page Title | 40px | 700 | 1.12 | Main product/dashboard screen title. |
| Section Title | 30px | 650 | 1.18 | Major sections. |
| Card Title | 22px | 650 | 1.25 | Feature cards and panels. |
| Body Large | 18px | 400 | 1.60 | Lead copy and key explanations. |
| Body | 16px | 400 | 1.55 | Default body copy. |
| Small | 14px | 500 | 1.45 | Labels, metadata, nav. |
| Micro | 12px | 600 | 1.35 | Badges and system tags. |

### Typography Principles
- Lead with plain-language value, not technical jargon.
- Use short paragraphs and clear section labels.
- Avoid all-caps body text. All-caps is allowed only for short labels and badges.
- No em dashes in professional copy. Use commas, periods, or parentheses.
- Banned words: Elevate, Seamless, Unleash, Next-Gen.

## 4. Component Styling

### Buttons
- **Primary CTA:** Gold background `#D4A14A`, navy deep text `#0A1B30`, 12px radius, 14px to 18px vertical padding, 600 weight.
- **Primary CTA hover:** Gold soft `#E8C98A` with subtle lift.
- **Secondary CTA:** Transparent or cream surface with navy border and navy text.
- **Dark CTA:** Navy background, white text, gold border or gold left accent.
- **Danger actions:** Red border and text, never decorative.

### Cards and Panels
- Use cream or white cards on navy or cream backgrounds.
- Radius scale: 12px for controls, 16px for cards, 24px for hero panels.
- Use subtle borders more often than heavy shadows.
- Preferred shadow: `0 18px 50px rgba(10, 27, 48, 0.12)`.
- Executive panels can use dark navy surfaces with 1px gold or muted navy borders.

### Navigation
- Sidebars and command centers use navy deep backgrounds.
- Active nav state uses gold left rail, cream text, or soft gold background.
- Keep navigation labels plain and functional.

### Forms
- Inputs use white backgrounds, navy text, slate placeholder, border sand outline.
- Focus state: 2px gold or blue outline with strong contrast.
- Minimum field height: 44px.

### Status and Metrics
- Use labeled chips, not color-only dots.
- Metrics should include context: value, trend, time period, and next action when possible.
- Avoid fake data in production-facing mockups. If placeholder data is necessary, label it clearly.

### Imagery
- Prefer clean product screenshots, warm human work scenes, book mockups, and practical system diagrams.
- Avoid robot heads, glowing brains, generic blue AI faces, random circuit backgrounds, and sci-fi clutter.
- Faith-adjacent imagery should feel dignified and hopeful, not sentimental or manipulative.

## 5. Layout Principles

### Spacing System
- Base unit: 8px.
- Use 24px, 32px, 48px, 64px, and 96px for major spacing.
- Cards should have 24px to 32px internal padding.
- Landing pages need strong section breathing room.

### Grid and Containers
- Max content width for landing pages: 1180px to 1240px.
- Dashboard layouts use 12-column grid or sidebar plus content grid.
- Mobile layouts collapse to one column with CTA visible early.

### Visual Hierarchy
- Every screen must answer in 3 seconds: what is this, why does it matter, what should I do next?
- Use one dominant focal point per section.
- CTA placement should follow the decision moment, not interrupt the user.

## 6. Depth, Motion, and Interaction

### Elevation
| Level | Treatment | Use |
|---|---|---|
| 0 | Flat cream, white, or navy | Page background. |
| 1 | Border and slight tint | Cards, panels, input groups. |
| 2 | Soft shadow | Primary cards, modals, feature blocks. |
| 3 | Strong panel contrast | Command centers, overlays, high-priority callouts. |

### Motion
- Use motion to clarify state, not decorate.
- Preferred duration: 160ms to 240ms.
- Respect `prefers-reduced-motion`.
- Avoid infinite busy animations unless indicating real work.

### Interaction Detail
- Minimum touch target: 44px by 44px.
- Keyboard focus must be visible.
- Hover states should be subtle and professional.

## 7. Voice, Copy, and Values

### Voice
- Clear, direct, warm, practical, grounded, human.
- Plain-language benefits before technical details.
- Confident without sounding inflated.
- Practical operations outcomes over vague AI hype.

### Messaging Filter
Every asset should answer:
- Who is this for?
- What problem does it solve?
- What happens next?
- What proof or concrete example makes it believable?
- What is the clear call to action?

### Faith and Values Gate
Reject concepts that:
- Mock or stereotype religion or people of faith.
- Misrepresent scripture.
- Promote manipulation, dishonesty, exploitation, vulgarity, or harm.
- Sexualize people or relationships outside the user’s stated values.
- Feel spiritually hollow on faith-adjacent work.

## 8. Accessibility and Responsive Behavior

### Accessibility
- Normal text contrast: 4.5:1 minimum.
- Large text contrast: 3:1 minimum.
- UI components and graphical objects: 3:1 minimum.
- Body text minimum: 16px on web.
- Touch targets: 44px by 44px minimum.
- Color is never the only signal.
- Meaningful images need alt text. Decorative images use `alt=""`.

### Breakpoints
| Name | Width | Behavior |
|---|---:|---|
| Mobile | 375px to 640px | One-column layout, simplified nav, early CTA. |
| Tablet | 641px to 1023px | Two-column cards, compact hero, larger touch targets. |
| Desktop | 1024px to 1440px | Full grid and dashboard layouts. |
| Wide | 1441px and up | Preserve readable content width, avoid stretched lines. |

## 9. Agent Prompt Guide

### Quick Color Reference
- Navy: `#0F2742`
- Navy Deep: `#0A1B30`
- Gold: `#D4A14A`
- Gold Soft: `#E8C98A`
- Green Success: `#1F6B4A`
- Cream Surface: `#F5F1E8`
- White: `#FFFFFF`
- Slate: `#5A6B7B`
- Off Black: `#0E1116`

### Preferred Directions
- Executive command center for dashboards and AI operating systems.
- Warm practical consultancy for service pages and offers.
- Premium editorial for book launches and faith-centered content.
- Clean SaaS utility for product pages, tools, and CRM concepts.

### Example Prompts
- “Design a Titus Open Door landing page using navy, cream, and gold. Keep the copy clear, practical, and warm. Include hero, proof, three service cards, and a consultation CTA.”
- “Create an executive AI operations dashboard with navy deep sidebar, cream cards, gold active states, and accessible status chips.”
- “Build a faith-rooted book launch page that feels dignified, hopeful, and professional. Avoid sentimental imagery and hype.”
- “Create a CRM product mockup for small-business follow-up, using practical copy, clear workflow cards, and a gold primary CTA.”

### Do
- Use navy for structure, cream for warmth, gold for focus.
- Make the next action obvious.
- Keep text readable at mobile sizes.
- Use real operational language: follow-up, lead recovery, clarity, task flow, customer response.
- Show trust through restraint, spacing, and specificity.

### Do Not
- Do not use generic AI gradients, robot imagery, neon sci-fi, or empty futurism.
- Do not write hype copy or corporate filler.
- Do not use em dashes.
- Do not overuse gold.
- Do not generate designs that look like default templates.
