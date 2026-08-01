# Titus Banks — Brand Design System

## Brand Identity
- **Brand:** Titus Banks / Open Door AI Systems
- **Feel:** Premium, warm, grounded, professional, faith-rooted
- **Voice:** Clear, direct, practical, human. No hype. No corporate filler.

## Core Palette

| Token | Hex | Usage |
|---|---|---|
| Navy | `#0F2742` | Primary backgrounds, headers |
| Navy Deep | `#0A1B30` | Heavy contrast, deep sections |
| Gold | `#D4A14A` | Accent, CTAs, focal emphasis |
| Gold Soft | `#E8C98A` | Secondary accent, hover states |
| Green | `#1F6B4A` | Success, confirmation, growth |
| Cream | `#F5F1E8` | Light backgrounds, cards |
| White | `#FFFFFF` | Pure surface, text on dark |
| Slate | `#5A6B7B` | Body text on light, secondary |
| Off-Black | `#0E1116` | Primary body text on light |

## Typography

- **Display/Headings:** Inter, weight 700-800, letter-spacing -0.02em
- **Body:** Inter, weight 400-500, line-height 1.6
- **Mono/Code:** JetBrains Mono, weight 400
- **Scale:** 12 / 14 / 16 / 18 / 20 / 24 / 32 / 40 / 48 / 64 px
- **Body minimum:** 16px on web

## Spacing

- **Base unit:** 4px
- **Section padding:** 80px desktop, 40px mobile
- **Card padding:** 24px
- **Max content width:** 1200px
- **Grid:** 12 columns, 24px gutter

## Breakpoints

| Name | Width | Usage |
|---|---|---|
| Mobile | 375px+ | Single column |
| Tablet | 768px+ | 2 column |
| Desktop | 1024px+ | 3 column |
| Wide | 1440px+ | Max-width container |

## Components

### Buttons
- **Primary:** Gold `#D4A14A` background, white text, 16px horizontal padding, 8px radius
- **Secondary:** Navy `#0F2742` outline, gold text, same dimensions
- **Hover:** Darken 10%, subtle scale 1.02
- **Disabled:** 40% opacity, no hover

### Cards
- Background: Cream `#F5F1E8` or White `#FFFFFF`
- Border: none, shadow: 0 2px 8px rgba(0,0,0,0.06)
- Radius: 12px
- Padding: 24px

### Forms
- Input background: White, border: 1px solid `#E2E8F0`
- Focus: border `#D4A14A`, ring 2px `rgba(212,161,74,0.3)`
- Labels: Slate `#5A6B7B`, 14px, weight 500
- Error: border `#DC2626`, message in red

### Navigation
- Desktop: Horizontal, Navy background, gold active state
- Mobile: Hamburger, slide-out drawer, same tokens

## States

- **Empty:** Centered illustration + friendly CTA, cream background
- **Loading:** Subtle gold pulse/shimmer
- **Error:** Clear message, action button, never raw stack trace
- **Success:** Green `#1F6B4A` indicator with checkmark

## Motion

- **Duration:** 200ms default, 300ms page transitions
- **Easing:** Ease-out for enter, ease-in for exit
- **Hover:** 150ms color/scale transitions
- **Reduced motion:** Respects `prefers-reduced-motion`

## Accessibility (WCAG 2.1 AA)

- Normal text contrast: 4.5:1 minimum
- Large text contrast: 3:1 minimum
- Focus visible: 2px gold outline on all interactive elements
- Touch targets: 44x44px minimum
- Alt text on all meaningful images
- No color-only signals — always pair with icon or text

## Voice & Content Rules

- No em dashes
- No corporate filler words: "elevate", "seamless", "unleash", "next-gen"
- Reading level: Grade 8 or below for body copy
- Faith content: warm, hopeful, honest, dignified — never hollow
- Banned: profanity, hype, manipulation, AI-generated slop

## Status Indicators

### Status Colors
| Status | Color | Icon | Usage |
|---|---|---|---|
| Complete | Green `#1F6B4A` | Checkmark | Finished tasks, passing tests |
| Running | Gold `#D4A14A` | Spinner | In-progress work, active agents |
| Blocked | Red `#DC2626` | X circle | Failed tests, blockers, errors |
| Pending | Slate `#5A6B7B` | Clock | Waiting tasks, queued work |
| Review | Purple `#7C3AED` | Eye | Awaiting approval, in review |

### Status Badges
- Inline pill: 20px height, 8px horizontal padding, 12px font, radius pill
- Background: status color at 12% opacity
- Text: status color at 100%
- Icon: 14px, left of text

## Progress Indicators

### Progress Bar
- Height: 8px, radius: 4px
- Track: `#E2E8F0` (light gray)
- Fill: Green `#1F6B4A` (complete), Gold `#D4A14A` (in progress)
- Label: Percentage in Caption style, right-aligned

### Milestone Progress
- Circular ring: 48px diameter, 4px stroke
- Fill: Green when complete, Gold when in progress
- Center: Percentage or checkmark

## Alerts

### Alert Types
| Type | Border | Background | Icon | Usage |
|---|---|---|---|---|
| Success | Green `#1F6B4A` | Green at 8% | Checkmark | Confirmation, completion |
| Warning | Gold `#D4A14A` | Gold at 8% | Triangle | Caution, attention needed |
| Error | Red `#DC2626` | Red at 8% | X circle | Failure, blocking issue |
| Info | Slate `#5A6B7B` | Slate at 8% | Info circle | Information, context |

### Alert Layout
- Padding: 16px
- Border-left: 4px solid (type color)
- Border-radius: 8px
- Icon: 20px, type color
- Title: Body bold, type color
- Message: Body, Off-Black
- Dismiss: X button, Slate, right-aligned

## Tables

### Table Layout
- Header: Navy background, White text, Caption style uppercase
- Rows: White background, alternating Cream at 50%
- Cells: 16px padding, body text
- Borders: 1px solid `#E2E8F0` between rows
- Hover: Gold at 4% background

### Table States
- Loading: Gold shimmer rows
- Empty: Centered message with CTA
- Error: Red alert above table

## Dark Mode

### Dark Mode Tokens
| Token | Light | Dark |
|---|---|---|
| Background | Cream `#F5F1E8` | Navy Deep `#0A1B30` |
| Surface | White `#FFFFFF` | Navy `#0F2742` |
| Surface hover | Cream `#F5F1E8` | Navy Mid `#14294D` |
| Text primary | Off-Black `#0E1116` | Cream `#F5F1E8` |
| Text secondary | Slate `#5A6B7B` | Slate Light `#94A3B8` |
| Border | `#E2E8F0` | `rgba(255,255,255,0.1)` |

### Dark Mode Rules
- Activate via `prefers-color-scheme: dark` or manual toggle
- Same components, different token values
- Gold and Green remain unchanged
- Focus rings use Gold in both modes

## Responsive Behavior

### Mobile (< 768px)
- Single column layout
- Navigation: hamburger menu
- Cards: full-width, 16px padding
- Tables: horizontal scroll or card layout
- Touch targets: 44x44px minimum

### Tablet (768px - 1023px)
- 2 column layout
- Navigation: condensed horizontal
- Cards: 2-column grid
- Tables: full-width

### Desktop (1024px+)
- 3 column layout
- Navigation: full horizontal
- Cards: 3-column grid
- Tables: full-width with sorting

## Sub-Brands

| Brand | Variation |
|---|---|
| Open Door AI Systems | Same system, emphasis on professionalism + approachability |
| NOLO | Same system, warmer cream backgrounds, larger type for video |
| JARVIS | Dark mode variant: Navy Deep `#0A1B30` backgrounds, cyan accents |
| Titus AI OS | Same system, dashboard-focused, status indicators prominent |
