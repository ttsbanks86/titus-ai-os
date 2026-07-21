# Architecture Proposal

**Company:** BrightCare Home Services (Fictional)  
**Document:** 21-architecture-proposal.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Architecture Overview

### Recommended Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Framework | Next.js 14+ (App Router) | Static export capable, React-based, strong community |
| Language | TypeScript | Type safety, industry standard |
| Styling | Tailwind CSS | Utility-first, responsive design, small bundle |
| UI Components | shadcn/ui | Accessible, customizable, copy-paste components |
| Charts | Recharts | React-native charting, works with static export |
| Data | Local JSON/TypeScript modules | No backend required, deterministic demo mode |
| Testing | Vitest + Playwright | Fast unit tests, browser-level E2E testing |
| Deployment | Vercel | Static export or serverless, free tier, CDN |
| Version Control | Git (GitHub) | Existing repository, standard workflow |

---

## Application Structure

```
ba-compass/
├── docs/                    # Phase 1 documentation
├── diagrams/                # Process diagrams and visuals
├── data/                    # Synthetic data files
├── portfolio/              # Career package materials
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── page.tsx         # Home / scenario selection
│   │   ├── scenario/        # Scenario views
│   │   ├── stakeholders/    # Stakeholder analysis
│   │   ├── processes/       # Process mapping
│   │   ├── requirements/    # Requirements management
│   │   ├── kpi/             # KPI dashboard
│   │   ├── risk/            # Risk register
│   │   ├── brd/             # BRD viewer
│   │   └── executive/       # Executive summary
│   ├── components/          # Shared UI components
│   │   ├── ui/              # shadcn/ui components
│   │   ├── dashboard/       # Dashboard-specific components
│   │   ├── process-map/     # Process flow components
│   │   └── kpi-card/        # KPI metric display components
│   ├── data/                # Synthetic data modules
│   │   ├── shifts.ts
│   │   ├── caregivers.ts
│   │   ├── clients.ts
│   │   ├── escalations.ts
│   │   ├── kpi-data.ts
│   │   └── index.ts
│   ├── lib/                 # Utility functions
│   │   ├── kpi-calculations.ts
│   │   ├── data-utils.ts
│   │   └── export-utils.ts
│   └── types/               # TypeScript type definitions
│       └── index.ts
├── public/                  # Static assets
├── tests/                   # Test files
│   ├── unit/
│   └── e2e/
├── portfolio/               # Career materials
├── README.md
└── CHANGELOG.md
```

---

## Component Structure

```
components/
├── layout/
│   ├── nav.tsx                    # Navigation component
│   ├── header.tsx                 # Page header
│   ├── footer.tsx                 # Footer with disclaimer
│   └── mobile-nav.tsx             # Mobile navigation drawer
├── dashboard/
│   ├── shift-summary.tsx          # Shift status summary
│   ├── gap-alert.tsx              # Open gap indicator
│   └── quick-stats.tsx            # Top-level metrics row
├── stakeholder/
│   ├── stakeholder-table.tsx      # Stakeholder register table
│   └── power-interest-matrix.tsx  # Matrix visualization
├── process-map/
│   ├── process-flow.tsx           # Process diagram
│   ├── step-detail.tsx            # Step details panel
│   └── process-comparison.tsx     # Side-by-side comparison
├── requirements/
│   ├── requirement-table.tsx      # Filterable requirements table
│   ├── traceability-matrix.tsx    # RTM display
│   └── user-story-card.tsx        # User story display card
├── kpi/
│   ├── kpi-card.tsx               # Single KPI display with gauge
│   ├── kpi-dashboard.tsx          # Dashboard of all KPIs
│   ├── kpi-trend-chart.tsx        # Trend line chart
│   └── kpi-filter.tsx             # Time period filter
├── risk/
│   ├── risk-register-table.tsx    # Risk register
│   └── risk-heatmap.tsx           # Risk heatmap visualization
├── brd/
│   ├── brd-viewer.tsx             # Document viewer
│   └── brd-section.tsx            # Section navigation
├── export/
│   ├── pdf-export.tsx             # PDF export handler
│   └── markdown-export.tsx        # Markdown export handler
└── shared/
    ├── data-disclaimer.tsx        # Synthetic data notice
    ├── page-header.tsx            # Reusable page header
    └── loading-state.tsx          # Loading indicator
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Synthetic Data Layer                      │
│  (TypeScript modules containing typed demo data objects)     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Utility Layer                        │
│  (KPI calculations, data transformation, filtering logic)   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application State                         │
│  (React state / URL params — no Redux needed for MVP)       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    UI Components                             │
│  (Dashboard, process maps, tables, charts, document views)  │
└─────────────────────────────────────────────────────────────┘
```

---

## State Management

For the MVP, state management will be minimal:

- **URL parameters** for view state (selected scenario, active tab, filter values)
- **React component state** for UI interactions (expanded details, toggles)
- **No Redux, Zustand, or external state library** needed for this scope
- All data is read-only from static TypeScript modules

---

## Export Approach

| Export Type | Library / Method |
|-------------|-----------------|
| PDF | Browser print-to-PDF or `html2canvas` + `jspdf` |
| Markdown | Client-side generation and download via blob URL |
| Requirements table | HTML table → Markdown conversion |
| Process diagrams | SVG export from Mermaid or inline SVG |

---

## Testing Approach

| Test Type | Tool | Scope |
|-----------|------|-------|
| Unit tests | Vitest | KPI calculations, data validation, utility functions |
| Component tests | Vitest + React Testing Library | UI component rendering |
| Accessibility | axe DevTools (automated) | WCAG 2.1 AA compliance |
| E2E | Playwright | Navigation flow, export functions, viewport testing |
| Visual regression | Playwright screenshot comparison | Layout integrity |

---

## Deployment Approach

1. **Development**: `npm run dev` (local Next.js dev server)
2. **Build**: `npm run build` (static export or serverless build)
3. **Preview**: Vercel preview deployment per branch
4. **Production**: Vercel production deployment from main branch
5. **Domain**: Vercel subdomain (ba-compass.vercel.app) or custom via Titus platform

No backend server, database, or API is required for deployment. The application runs entirely on client-side data.

---

## Security Controls

| Control | Implementation |
|---------|---------------|
| No authentication | Public access, no user accounts |
| No secrets in code | No API keys, no credentials in source |
| No data transmission | All data local, no external API calls |
| No storage | No cookies, localStorage, or session storage |
| Content Security Policy | CSP headers if deploy platform supports |
| No analytics | No tracking scripts or analytics |

---

## Privacy Controls

| Control | Implementation |
|---------|---------------|
| Synthetic data only | All data clearly fictional |
| Disclaimer on every page | "All data is synthetic" notice |
| No PII | Fictional names only |
| No PHI | No medical information |
| No user data collection | Zero data capture |
| No cookies | No tracking or session cookies |

---

## Optional Future AI Integration

The current architecture does not depend on AI APIs. If AI features are added in the future:

1. AI would be an **optional enhancement**, not a core dependency
2. AI features would be **clearly labeled** as AI-generated
3. AI would use a **configurable provider** (following the system's provider-independent pattern)
4. Potential uses: generate alternative scenario data, suggest requirement wording, validate KPI calculations
5. AI integration would happen **after** the core MVP is complete

**Why the MVP must not depend on an AI API:**

- Recruiters must be able to view the demo without configuring API keys
- Zero operational cost for core functionality
- No single point of failure from API outages
- Demonstrates BA skills independently of AI tooling
- Aligns with the system's provider-independent philosophy

---

## Architecture Constraints

| Constraint | Implication |
|------------|-------------|
| No backend server | All data must be client-side |
| Static export capable | No server-side rendering dependencies |
| No paid APIs | Core functionality at zero cost |
| Mobile responsive | Design mobile-first |
| No data persistence | All demo data in source code |

---

## Related Documents

- 22-milestone-plan.md — Implementation phases
- 23-definition-of-done.md — Completion criteria
- 20-product-backlog.md — Development tasks
