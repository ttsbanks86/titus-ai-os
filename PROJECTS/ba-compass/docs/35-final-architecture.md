# Final Architecture — BA Compass

Complete architecture documentation for the BA Compass application.

---

## Overview

BA Compass is a static Next.js 15 application that demonstrates the complete Business Analyst lifecycle through a fictional home-care company case study. The application generates 18+ static HTML pages at build time with no server runtime, no database, and no external API dependencies.

---

## Next.js App Router Structure

The application uses the Next.js App Router with static export (`output: "export"`).

```
src/app/
  layout.tsx             — Root layout: header, footer, synthetic data notice, RequirementsProvider
  page.tsx               — Landing page with KPI snapshot
  overview/page.tsx      — Business scenario overview
  stakeholders/page.tsx  — Stakeholder register
  current-state/page.tsx — Current-state process flow
  analysis/page.tsx      — Gap analysis
  dashboard/page.tsx     — KPI dashboard (client component)
  future-state/page.tsx  — Future-state improvements
  requirements/page.tsx  — Requirements management (client component)
  brd/page.tsx           — BRD viewer (client component)
  traceability/page.tsx  — Traceability matrix (client component)
  executive-summary/page.tsx — Executive summary (client component)
  risks/page.tsx         — Risk register (client component)
  recommendations/page.tsx — Prioritized recommendations
  project/page.tsx       — About the project
  responsible-ai/page.tsx — AI ethics documentation
  tour/page.tsx          — 5-minute recruiter tour (client component)
  not-found/page.tsx     — Custom 404 page
  globals.css            — Global styles with Tailwind directives
```

### Static vs. Client Pages

| Type | Pages | Reason |
|------|-------|--------|
| **Server components** (default) | `/`, `/overview`, `/stakeholders`, `/current-state`, `/analysis`, `/future-state`, `/recommendations`, `/project`, `/responsible-ai`, `/not-found` | Pure content display, no interactivity needed |
| **Client components** (`"use client"`) | `/dashboard`, `/requirements`, `/brd`, `/traceability`, `/executive-summary`, `/risks`, `/tour` | Interactive features: state, charts, event handlers, localStorage |

All interactive pages use `"use client"` at the top of their component file. There are no hybrid or streaming components.

---

## Component Hierarchy

```
RootLayout (server)
  ├── SyntheticDataNoticeBar
  ├── Header
  │     ├── Logo / Site Title
  │     ├── Desktop Nav (NAV_ITEMS — 14 links)
  │     └── Mobile Hamburger Menu
  ├── RequirementsProvider (React Context)
  │     └── <main>
  │           └── [Page Content]
  └── Footer
        ├── Nav Links
        └── Privacy / Disclaimer Text
```

### Component Library

```
src/components/
  layout/
    header.tsx        — Site header with navigation
    footer.tsx        — Site footer with links
  ui/
    content-panel.tsx — Content section wrapper with padding and border
    data-notice.tsx   — Synthetic data disclaimer notice
    empty-state.tsx   — Empty state placeholder
    index.ts          — Barrel export
    metric-card.tsx   — KPI metric display with status color
    page-heading.tsx  — Page title and subtitle
    section-heading.tsx — Section title with optional description
    status-badge.tsx  — Colored status label (success/warning/error/info)
    table-wrapper.tsx — Responsive table container with horizontal scroll
  shared/
    demo-reset.tsx    — Confirmation dialog for resetting demo data
    empty-state-msg.tsx — Empty state message component
    error-boundary.tsx — React error boundary wrapper
    loading-skeleton.tsx — Loading placeholder
  charts/             — (Reserved for additional chart components)
  navigation/         — (Reserved for additional navigation components)
  process/            — (Reserved for process visualization components)
```

### UI Component Patterns

All UI components follow a consistent pattern:
- Single responsibility — one component, one purpose
- Accept `className` prop for Tailwind customization
- Use `class-variance-authority` for variant management (where applicable)
- Accessible with ARIA attributes where needed
- TypeScript strict with explicit prop interfaces

---

## Data Flow

### Content Data Flow

```
src/data/content/*.ts (static TypeScript modules)
  → Imported directly by page components
  → Rendered as HTML at build time
```

Content data is static TypeScript arrays and objects. Pages import data directly:

```
// Example: stakeholders/page.tsx
import { stakeholders } from "@/data/content/stakeholders";
// → Renders 10 stakeholder profiles
```

### Synthetic Data Flow

```
src/data/synthetic/
  shifts.ts ──────────────┐
  caregivers.ts ──────────┤
  clients.ts ─────────────┤
  escalations.ts ─────────┤
  documentation.ts ───────┤
  issues.ts ──────────────┤
  followups.ts ───────────┘
                          │
src/data/synthetic/       │
  kpi-input.ts ───────────┤──→ KpiInput object
                          │
src/lib/kpi/              │
  calculations.ts ────────┘──→ AllKpiResults (8 KPIs with values + statuses)
  index.ts                   → Re-exports calculation functions
```

### Interactive Data Flow

```
User Action (click, type)
  → Client Component Event Handler
    → dispatch({ type, payload }) — useReducer
      → Reducer produces new state
        → React re-renders component
          → UI updates
```

For requirements editing:
```
User edits field
  → updateRequirement(id, field, value)
    → dispatch({ type: "UPDATE_REQUIREMENT", id, field, value })
      → Reducer updates state
        → useEffect saves to localStorage
          → Component re-renders with new values
```

---

## State Management

### Architecture: React Context + useReducer + localStorage

The application uses a single context provider for interactive state:

```
RequirementsProvider (src/lib/state/requirements-store.tsx)
  ├── State: { requirements: EditableRequirement[], editMode: boolean }
  ├── Actions: ENTER_EDIT_MODE | EXIT_EDIT_MODE | UPDATE_REQUIREMENT |
  |             RESET_REQUIREMENT | RESET_ALL | LOAD_EDITS
  ├── Reducer: Pure function returning new state
  ├── useEffect: Load edits from localStorage on mount
  ├── useEffect: Save edits to localStorage on state change
  └── Context value: { state, enterEditMode, exitEditMode, updateRequirement,
                       resetRequirement, resetAll, getEditedCount }
```

### State Persistence

- **localStorage key:** `ba-compass-requirements-edits`
- **Storage format:** JSON object keyed by requirement ID
- **Load on mount:** Reads from localStorage and dispatches LOAD_EDITS
- **Save on change:** useEffect watches state.requirements, writes to localStorage
- **Reset:** Removes localStorage key, dispatches RESET_ALL
- **Error handling:** try/catch on both read and write — gracefully falls back to defaults

### State Shape

```typescript
interface RequirementsState {
  requirements: EditableRequirement[];
  editMode: boolean;
}

interface EditableRequirement {
  id: string;
  statement: string;
  priority: RequirementPriority;
  status: RequirementStatus;
  stakeholderOwner: string;
  justification: string;
  relatedKpi: string;
  _edited: boolean;      // Tracking flag
  _original: string;      // For reset capability
}
```

---

## KPI Calculation Engine

### Location: `src/lib/kpi/`

```
kpi/
  index.ts         — Re-exports 8 calculation functions and AllKpiResults type
  calculations.ts  — 8 pure calculation functions + calculateAllKpis()
```

### Design Principles

- **Pure functions** — No side effects, no state, no randomness. Given the same input, always return the same output.
- **Deterministic** — All KPI results are reproducible.
- **Edge-case safe** — All functions handle zero denominators gracefully (return 0 instead of NaN or error).
- **Status classification** — Each KPI classifies as `on_track`, `warning`, or `critical` based on defined thresholds.

### The 8 KPIs

| ID | Function | Formula | Target |
|----|----------|---------|--------|
| KPI-001 | `calculateShiftFillRate` | (Confirmed / Total) x 100 | >= 95% |
| KPI-002 | `calculateMissedShiftRate` | (Missed / Total) x 100 | < 2% |
| KPI-003 | `calculateLateArrivalRate` | (Late / Completed) x 100 | < 10% |
| KPI-004 | `calculateAverageEscalationTime` | SUM(Time) / Count | < 30 min |
| KPI-005 | `calculateDocumentationCompletionRate` | (Complete / Required) x 100 | >= 95% |
| KPI-006 | `calculateOpenStaffingGaps` | Count of unassigned (48h) | < 3 |
| KPI-007 | `calculateIssueResolutionTime` | SUM(Hours) / Count | < 4 hrs |
| KPI-008 | `calculateFollowUpCompletionRate` | (Completed / Required) x 100 | >= 90% |

### Constants

KPI targets and warning thresholds live in `src/lib/constants/index.ts`:
```
KPI_TARGETS — On-track targets for all 8 KPIs
KPI_WARNINGS — Warning thresholds for all 8 KPIs
LATE_ARRIVAL_THRESHOLD_MINUTES — 15 minutes
DOCUMENTATION_WINDOW_HOURS — 24 hours
TARGET_ESCALATION_MINUTES — 30 minutes
WARNING_ESCALATION_MINUTES — 60 minutes
```

---

## Export System

### Location: `src/lib/export/index.ts`

The export system generates Markdown and CSV files entirely in the browser using Blob URLs. No server is involved.

### Export Functions

| Function | Output | Format |
|----------|--------|--------|
| `requirementsToMarkdown()` | Requirements table | Markdown |
| `requirementsToCsv()` | Requirements table | CSV |
| `traceabilityToMarkdown()` | Traceability matrix | Markdown |
| `risksToMarkdown()` | Risk register | Markdown |
| `risksToCsv()` | Risk register | CSV |
| `executiveSummaryToMarkdown()` | Executive summary | Markdown |

### Download Helpers

| Function | Description |
|----------|-------------|
| `downloadText(content, filename, mimeType)` | Creates a Blob, generates a temporary URL, triggers download via hidden anchor, revokes URL |
| `downloadCsv(content, filename)` | Wraps downloadText with CSV MIME type |

### Synthetic Notice

Every export includes the synthetic data disclaimer at the top:
```
DISCLAIMER: All data is synthetic and fictional. This is a portfolio
demonstration project. No real client, caregiver, or patient information is used.
```

---

## Testing Strategy

### Unit Tests: Vitest + Testing Library

**Location:** `src/tests/`

| File | Tests | Type |
|------|-------|------|
| `kpi-calculations.test.ts` | 34 | Pure function tests (input → output) |
| `validation.test.ts` | 23 | Validation function tests |
| `app-shell.test.tsx` | 19 | Component rendering + content integrity |
| **Total** | **76** | |

### E2E Tests: Playwright

**Location:** `src/tests/e2e/smoke.spec.ts`

14 tests covering:
- Landing page core elements
- Custom 404 for unknown routes
- All 16 routes respond (parameterized)
- Recruiter tour navigation
- Requirements page edit mode
- Demo reset with confirmation dialog
- KPI dashboard period filters
- Traceability search
- BRD table of contents
- Risk register visibility
- Executive summary sections
- Export buttons
- Synthetic data notice on key pages
- Skip link accessibility

### CI Integration

GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push:
1. TypeScript type check (`tsc --noEmit`)
2. ESLint
3. Unit tests (Vitest)
4. Production build

---

## Deployment Architecture

### Build Process

```
npm run build
  → next build
    → TypeScript compilation
    → Static page generation (18+ HTML files)
    → CSS extraction
    → Chunk generation
    → Output to out/
```

### Output Structure

```
out/
  index.html              — Landing page
  overview.html           — Business overview
  stakeholders.html       — Stakeholder register
  current-state.html      — Current-state process
  analysis.html           — Gap analysis
  dashboard.html          — KPI dashboard
  future-state.html       — Future-state process
  requirements.html       — Requirements management
  brd.html                — BRD viewer
  traceability.html       — Traceability matrix
  executive-summary.html  — Executive summary
  risks.html              — Risk register
  recommendations.html    — Recommendations
  project.html            — About the project
  responsible-ai.html     — AI ethics
  tour.html               — Recruiter tour
  404.html                — Custom 404 page
  not-found.html          — Next.js fallback 404
  social-preview.svg      — Open Graph preview image
  _next/static/           — JS chunks, CSS, build manifest
```

### Hosting

The static output can be hosted on:
- **Vercel** (recommended) — Automatic deploy from GitHub, global CDN, HTTPS, preview deployments
- **Netlify** — Drag-and-drop `out/` or connect GitHub repo
- **GitHub Pages** — Configure to serve from `out/` directory
- **Any static host** — Nginx, S3, Cloudflare Pages, etc.

### Key Configuration

```typescript
// next.config.ts
const nextConfig: NextConfig = {
  output: "export",          // Static export — no server
  images: { unoptimized: true },  // No image optimization API
  reactStrictMode: true,     // Development quality enforcement
};
```

Build command: `npm run build`
Output directory: `out`
No server functions required.

### Zero Backend Architecture

- **No database** — All data is compiled into static HTML at build time
- **No server** — Static files only, served from CDN
- **No API** — No REST, GraphQL, or serverless functions
- **No authentication** — Public, no login required
- **No cookies** — No tracking, no analytics, no session management

---

## Security and Privacy Model

### Strengths

| Attribute | Implementation |
|-----------|----------------|
| **No API keys** | Zero environment variables required. No AI API dependencies. |
| **No data collection** | No analytics scripts, no cookies, no tracking pixels, no form submissions. |
| **No real data** | All data is synthetic and labeled as such on every page. |
| **No backend** | Static files only — no server-side processing, no database, no API endpoints. No attack surface. |
| **User data isolation** | Requirement edits stored in browser localStorage only. No data transmitted over the network. |
| **HTTPS** | Enforced by hosting platform (Vercel provides automatic SSL). |
| **Robots exclusion** | `robots.meta` set to `index: false, follow: false` — prevents search engine indexing. |

### Limitations

| Aspect | Current State | Notes |
|--------|---------------|-------|
| Authentication | None | No login, no session management. Any visitor can access all pages. |
| Data persistence | localStorage only | Edits do not survive clearing browser data. No cross-device sync. |
| Input validation | Client-side only | Validation runs in the browser. No server-side validation exists (no server). |
| Content Security Policy | Not configured | The application sets no CSP headers. Not needed for static content, but could be added for defense in depth. |
| Dependency vulnerabilities | Managed via npm audit | Run `npm audit` regularly. Document any unavoidable vulnerabilities. |

All synthetic data files include a header comment:
```
// DISCLAIMER: All data in this module is SYNTHETIC and FICTIONAL.
// Created for portfolio demonstration purposes only.
// No real client, caregiver, employer, or patient information is used.
```
