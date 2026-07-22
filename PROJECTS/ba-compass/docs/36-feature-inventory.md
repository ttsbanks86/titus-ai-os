# Feature Inventory — BA Compass v1.0.0

Complete inventory of all application features, routes, components, data modules, KPI calculations, tests, and exports.

---

## Routes (16)

| # | Route | Page Type | Description | Status |
|---|-------|-----------|-------------|--------|
| 1 | `/` | Server | Landing page with KPI snapshot (8 metrics), business problem summary, CTA buttons (Explore, Dashboard, Tour, My Contribution), feature highlight cards, navigation links | Complete |
| 2 | `/overview` | Server | Business scenario overview with BA lifecycle diagram, project background, objectives, scope boundaries | Complete |
| 3 | `/stakeholders` | Server | Stakeholder register with 10 roles, power-interest mapping, expandable profile cards showing pain points, needs, communication preferences | Complete |
| 4 | `/current-state` | Server | 11-step current-state process flow with actor/input/action/output per step, expandable step details, failure analysis, channel reliability table | Complete |
| 5 | `/analysis` | Server | Gap analysis with 21 pain points across 9 business dimensions, severity counts, dimension filtering, gap severity summary | Complete |
| 6 | `/dashboard` | Client | KPI dashboard with 8 live metric cards, period selector (All/Week1/Week2), 4 Recharts visualizations (pie + bar), drill-down tables, KPI definitions table | Complete |
| 7 | `/future-state` | Server | Future-state improvements with 8 improvement items, side-by-side comparison table, improvement detail cards with linked requirements and KPIs | Complete |
| 8 | `/requirements` | Client | Requirements management page with 45 requirements across 3 categories, type/priority/search filters, edit mode, validation, export, user stories toggle | Complete |
| 9 | `/brd` | Client | BRD viewer with 12 sections, table of contents navigation, expandable sections, export to Markdown, Print/PDF support | Complete |
| 10 | `/traceability` | Client | Traceability matrix with 15 traceability links, search input, status filter dropdown, coverage summary, MD/CSV export, Print support | Complete |
| 11 | `/executive-summary` | Client | Executive summary with 5 key findings, KPI summary cards, top risks, priority recommendations, expected benefits, implementation considerations, MD export | Complete |
| 12 | `/risks` | Client | Risk register with 15 risks, heatmap visualization, likelihood/impact/score columns, category filtering, expandable risk details, MD/CSV export, Print | Complete |
| 13 | `/recommendations` | Server | 11 prioritized recommendations across Immediate / Near-Term / Future categories with description, effort, impact for each | Complete |
| 14 | `/project` | Server | About the project page with 12 BA work items, technology stack, testing metrics, privacy and security statement, author credit | Complete |
| 15 | `/responsible-ai` | Server | AI ethics documentation with 10-item checklist, risk considerations, ethical guardrails, data ethics, transparency note | Complete |
| 16 | `/tour` | Client | 5-minute recruiter tour with 10 steps, progress bar, prev/next navigation, "Open full page" links, exit option | Complete |

### System Pages

| Route | Description | Status |
|-------|-------------|--------|
| `/_not-found` | Internal Next.js 404 placeholder | Complete |
| `/404` | Static 404 page for direct navigation to unknown routes | Complete |

---

## Interactive Features

| Feature | Route(s) | Description | Status |
|---------|----------|-------------|--------|
| Requirements editing | `/requirements` | Inline textarea editing for BR statements, select dropdowns for priority/status. Context + useReducer state. | Complete |
| Requirements validation | `/requirements` | 7 validation rules: ID format, statement length (10–5000 chars), priority (High/Medium/Low), status (Proposed/Approved/In Progress/Implemented), stakeholder owner, justification length, KPI reference format. Real-time validation on blur with `role="alert"` error display. | Complete |
| Requirements filtering | `/requirements` | Type filter (All/BR/FR/NFR), priority filter (All/High/Medium/Low), keyword search across ID and statement | Complete |
| Individual requirement reset | `/requirements` | Reset single requirement to its original value while keeping other edits | Complete |
| Demo reset all | `/requirements` | Confirmation dialog with Cancel/Confirm. Clears localStorage, restores all 15 BRs to defaults, shows "Data reset" feedback | Complete |
| KPI period filtering | `/dashboard` | Filter shifts by Full Period (Jul 14–27), Week 1 (Jul 14–20), Week 2 (Jul 21–27). Charts and metrics recalculate from filtered data. | Complete |
| KPI drill-down | `/dashboard` | Clickable metric cards reveal contributing records table with status, date, detail, and inclusion reason | Complete |
| KPI definitions table | `/dashboard` | Read-only table showing all 8 KPIs with name, formula, current value, target, and interpretation | Complete |
| Dashboard charts | `/dashboard` | 4 Recharts visualizations: shift distribution pie chart, KPI target comparison bar chart, escalations/service-issues/follow-ups mini charts | Complete |
| Markdown export | `/requirements`, `/risks`, `/brd`, `/traceability`, `/executive-summary` | Browser-native Markdown generation with synthetic data notice. Blob URL download. | Complete |
| CSV export | `/requirements`, `/risks`, `/traceability` | Browser-native CSV generation with proper escaping and synthetic data notice | Complete |
| Print/PDF | `/requirements`, `/brd`, `/risks`, `/traceability`, `/executive-summary` | Print stylesheets hide navigation and interactive controls. Uses browser print-to-PDF. | Complete |
| Recruiter tour | `/tour` | 10-step guided tour with progress bar, prev/next navigation, linked to each content page | Complete |
| Sequential navigation | All content pages | Prev/Next links at bottom of each content page following NAV_SEQUENCE | Complete |
| Navigation menu | All pages | 14-item desktop navigation in header, hamburger menu on mobile, skip-to-content link | Complete |
| Synthetic data notice | All pages | Yellow notice bar at top of every page: "All data displayed here is synthetic and fictional..." | Complete |

---

## Components

### Layout Components

| Component | File | Description | Status |
|-----------|------|-------------|--------|
| Header | `src/components/layout/header.tsx` | Site header with logo/title, desktop navigation (14 items), mobile hamburger menu, active route indication | Complete |
| Footer | `src/components/layout/footer.tsx` | Site footer with navigation links, synthetic data disclaimer, privacy note | Complete |

### UI Components

| Component | File | Description | Status |
|-----------|------|-------------|--------|
| PageHeading | `src/components/ui/page-heading.tsx` | Page title with optional subtitle | Complete |
| SectionHeading | `src/components/ui/section-heading.tsx` | Section title with optional description | Complete |
| ContentPanel | `src/components/ui/content-panel.tsx` | Content wrapper with border, padding, background | Complete |
| MetricCard | `src/components/ui/metric-card.tsx` | KPI display card with label, value, status color (on_track=green, warning=yellow, critical=red) | Complete |
| StatusBadge | `src/components/ui/status-badge.tsx` | Colored badge with 4 variants (success, warning, error, info, neutral) | Complete |
| DataNotice | `src/components/ui/data-notice.tsx` | Synthetic data disclaimer card with icon | Complete |
| EmptyState | `src/components/ui/empty-state.tsx` | Empty state placeholder with message | Complete |
| TableWrapper | `src/components/ui/table-wrapper.tsx` | Responsive table container with horizontal scroll | Complete |

### Shared Components

| Component | File | Description | Status |
|-----------|------|-------------|--------|
| DemoReset | `src/components/shared/demo-reset.tsx` | Confirmation dialog with Cancel/Confirm buttons, "Data reset" status message | Complete |
| EmptyStateMsg | `src/components/shared/empty-state-msg.tsx` | Generic empty state message | Complete |
| ErrorBoundary | `src/components/shared/error-boundary.tsx` | React error boundary with fallback UI | Complete |
| LoadingSkeleton | `src/components/shared/loading-skeleton.tsx` | Loading placeholder skeleton | Complete |

---

## Data Modules

### Synthetic Data (`src/data/synthetic/`)

| Module | File | Records | Description |
|--------|------|---------|-------------|
| Shifts | `shifts.ts` | 42 | Shift records with status, timing, caregiver assignment, documentation status, late flags |
| Caregivers | `caregivers.ts` | 10 | Caregiver profiles with availability, region, status |
| Clients | `clients.ts` | 8 | Client accounts with care level, region, account status |
| Escalations | `escalations.ts` | 6 | Escalation records with severity, timing, resolution |
| Documentation | `documentation.ts` | 22 | Documentation records with submission time, status, service summary |
| Service Issues | `issues.ts` | 7 | Service issue records with category, status, reporter |
| Follow-Ups | `followups.ts` | 7 | Follow-up records with deadlines, completion status |
| KPI Input | `kpi-input.ts` | — | Aggregation layer: `getAllShiftData()` produces KpiInput, `getDocumentationCounts()` produces doc counts |

### Content Data (`src/data/content/`)

| Module | File | Records | Description |
|--------|------|---------|-------------|
| Requirements | `requirements-data.ts` | 45 (15 BR + 18 FR + 12 NFR) | Business, functional, and nonfunctional requirements with priority, status, stakeholder, KPI links |
| Stakeholders | `stakeholders.ts` | 10 | Stakeholder profiles with interest, influence, needs, pain points, communication needs |
| Risks | `risks-data.ts` | 15 | Risk entries with likelihood, impact, score, mitigation, contingency |
| Process | `process-data.ts` | 11 steps + 8 improvements | Current-state process steps and future-state improvements |
| Gaps | `gaps-data.ts` | 21 | Gap analysis items across 9 business dimensions |

---

## KPI Calculations

| ID | Name | Function | Formula Source | Unit | Status |
|----|------|----------|----------------|------|--------|
| KPI-001 | Shift Fill Rate | `calculateShiftFillRate()` | docs/18-kpi-dictionary.md | Percentage | Complete |
| KPI-002 | Missed Shift Rate | `calculateMissedShiftRate()` | docs/18-kpi-dictionary.md | Percentage | Complete |
| KPI-003 | Late Arrival Rate | `calculateLateArrivalRate()` | docs/18-kpi-dictionary.md | Percentage | Complete |
| KPI-004 | Avg Escalation Time | `calculateAverageEscalationTime()` | docs/18-kpi-dictionary.md | Minutes | Complete |
| KPI-005 | Doc Completion Rate | `calculateDocumentationCompletionRate()` | docs/18-kpi-dictionary.md | Percentage | Complete |
| KPI-006 | Open Staffing Gaps | `calculateOpenStaffingGaps()` | docs/18-kpi-dictionary.md | Count | Complete |
| KPI-007 | Issue Resolution Time | `calculateIssueResolutionTime()` | docs/18-kpi-dictionary.md | Hours | Complete |
| KPI-008 | Follow-Up Completion Rate | `calculateFollowUpCompletionRate()` | docs/18-kpi-dictionary.md | Percentage | Complete |

### KPI Constants

| Constant | File | Description |
|----------|------|-------------|
| KPI_TARGETS | `src/lib/constants/index.ts` | On-track targets for all 8 KPIs |
| KPI_WARNINGS | `src/lib/constants/index.ts` | Warning thresholds for all 8 KPIs |
| LATE_ARRIVAL_THRESHOLD_MINUTES | `src/lib/constants/index.ts` | 15-minute late threshold |
| DOCUMENTATION_WINDOW_HOURS | `src/lib/constants/index.ts` | 24-hour doc window |

---

## Tests

### Unit Tests — 76 total

| Test File | Test Count | Coverage |
|-----------|-----------|----------|
| `src/tests/kpi-calculations.test.ts` | 34 | 8 KPI functions: standard cases, edge cases, zero denominators, all status thresholds |
| `src/tests/validation.test.ts` | 23 | 7 validation functions: valid input, invalid input, edge cases, boundary values |
| `src/tests/app-shell.test.tsx` | 19 | 3 components (StatusBadge: 5, MetricCard: 3, DataNotice: 1) + 10 content integrity checks |

### E2E Tests — 14 total

| File | Test Count | Coverage |
|------|-----------|----------|
| `src/tests/e2e/smoke.spec.ts` | 14 | Landing page, 404, all 16 routes, tour navigation, edit mode, demo reset, period filters, traceability search, BRD TOC, risk register, executive summary, export buttons, data notice, skip link |

---

## Exports

| Page | Formats | Content |
|------|---------|---------|
| `/requirements` | Markdown, CSV | Requirements table with all fields, local edit indicators |
| `/risks` | Markdown, CSV | Risk register with all fields |
| `/traceability` | Markdown, CSV | Traceability matrix with all links |
| `/executive-summary` | Markdown | Full executive summary content |
| `/brd` | Markdown | Full BRD document with all 12 sections |
| All pages | Print/PDF | Clean print layout via browser Ctrl+P |

Every export includes the synthetic data disclaimer.

---

## TypeScript Types (`src/types/`)

| File | Types | Description |
|------|-------|-------------|
| `domain.ts` | Shift, Caregiver, ClientAccount, Assignment, Escalation, DocumentationRecord, ServiceIssue, FollowUpRecord, + enums | Core domain models matching data dictionary |
| `kpi.ts` | KpiInput, KpiResult, KpiDefinition, KpiStatus, KpiPeriod | KPI calculation and display types |
| `requirements.ts` | Requirement, UserStory, AcceptanceCriterion, RequirementType, RequirementPriority, RequirementStatus | Requirements domain models |
| `risks.ts` | Risk, RiskCategory, RiskStatus | Risk register types |
| `index.ts` | Stakeholder, StakeholderInfluence, StakeholderInterest, ProcessStep, Recommendation | Additional domain types |
