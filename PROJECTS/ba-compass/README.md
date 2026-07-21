# BA Compass

**AI-Assisted Business Process and Requirements Analyzer**

A recruiter-ready Business Analyst portfolio project demonstrating end-to-end business analysis through a fictional home-care services case study.

---

## Overview

BA Compass showcases the complete Business Analyst lifecycle — from problem identification and stakeholder analysis through requirements documentation, process design, KPI definition, and executive communication.

**Fictional Case Study:** BrightCare Home Services — a home-care company experiencing systemic operational failures including missed shifts, late arrivals, incomplete documentation, and delayed escalation.

---

## Phase 1: Documentation Foundation (Complete)

Phase 1 delivers 25 Business Analyst documentation deliverables:

| Area | Documents |
|------|-----------|
| **Foundation** | Project Charter, Business Problem, Business Case, Scope |
| **Stakeholder** | Stakeholder Register, Stakeholder Analysis |
| **Process Analysis** | Current-State Process, Pain-Point & Gap Analysis |
| **Requirements** | BRD, Business Requirements (15), Functional Requirements (18), Nonfunctional Requirements (12) |
| **Stories & Criteria** | User Stories (26), Acceptance Criteria (24) |
| **Traceability** | Requirements Traceability Matrix |
| **Governance** | Risk Register (15), Assumptions & Constraints, KPI Dictionary (8), Data Dictionary (10 entities) |
| **Planning** | Product Backlog (52 items), Architecture Proposal, Milestone Plan |
| **Quality** | Definition of Done, Decision Log, Change Log |

---

## Phase 2: Application Foundation (Complete)

Phase 2 delivers a working Next.js application foundation with:

- **13 static routes** with navigation and placeholder content
- **Strict TypeScript domain types** matching the data dictionary
- **Deterministic synthetic dataset** (42 shifts, 10 caregivers, 8 clients, 6 escalations, 22 documentation records, 7 service issues, 7 follow-ups)
- **8 KPI calculation functions** matching approved formulas
- **41 unit tests** (34 KPI + 7 component tests)
- **6 Playwright e2e smoke tests** — all passing
- **Professional UI foundation** with accessible components
- **CI-ready** with lint, typecheck, test, and build scripts

### Technology Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 15.5 (App Router) |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS 3 |
| Charts | Recharts (ready for Phase 3) |
| Icons | Lucide React |
| Unit Tests | Vitest + Testing Library |
| E2E Tests | Playwright |
| CI | GitHub Actions |
| Deployment | Vercel (Phase 6) |

### Key Scripts

```bash
npm run dev        # Development server
npm run build      # Production build
npm run lint       # ESLint
npm run typecheck  # TypeScript check
npm run test       # Unit tests (41 tests)
npm run test:e2e   # Playwright tests (6 tests)
npm run validate   # Full validation: typecheck + lint + test + build
```

### Application Routes

| Route | Content |
|-------|---------|
| `/` | Landing page with KPI snapshot |
| `/overview` | Business scenario overview |
| `/stakeholders` | Stakeholder register (10 roles) |
| `/current-state` | 11-step current process |
| `/analysis` | Gap analysis (9 dimensions) |
| `/dashboard` | Live KPI dashboard (8 metrics) |
| `/future-state` | Future state improvements |
| `/requirements` | Requirements summary |
| `/risks` | Risk register (12+ risks) |
| `/recommendations` | Prioritized recommendations |
| `/project` | About this project |
| `/responsible-ai` | AI ethics documentation |

---

## Quick Metrics

| Metric | Value |
|--------|-------|
| Phase 1 Documents | 25 |
| Business Requirements | 15 (BR-001 through BR-015) |
| Functional Requirements | 18 (FR-001 through FR-018) |
| Nonfunctional Requirements | 12 (NFR-001 through NFR-012) |
| User Stories | 26 (US-001 through US-026) |
| Acceptance Criteria | 24 (AC-001 through AC-024) |
| Stakeholders | 10 fictional roles |
| Risks | 15 (R-001 through R-015) |
| KPIs | 8 (KPI-001 through KPI-008) |
| Unit Tests | 41 (all passing) |
| E2E Tests | 6 (all passing) |

---

## Getting Started

```bash
# Navigate to project
cd PROJECTS/ba-compass

# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

---

## Project Structure

```
PROJECTS/ba-compass/
├── docs/                         # Phase 1 BA documentation (25 files)
├── src/
│   ├── app/                      # Next.js App Router pages
│   │   ├── page.tsx              # Landing page
│   │   ├── layout.tsx            # Root layout with header/footer
│   │   ├── overview/             # Business scenario
│   │   ├── stakeholders/         # Stakeholder analysis
│   │   ├── current-state/        # Current process
│   │   ├── analysis/             # Gap analysis
│   │   ├── dashboard/            # KPI dashboard
│   │   ├── future-state/         # Future process
│   │   ├── requirements/         # Requirements management
│   │   ├── risks/                # Risk register
│   │   ├── recommendations/      # Recommendations
│   │   ├── project/              # About the project
│   │   └── responsible-ai/       # AI ethics
│   ├── components/
│   │   ├── layout/               # Header, Footer
│   │   ├── ui/                   # PageHeading, MetricCard, etc.
│   │   ├── navigation/           # (Phase 3)
│   │   ├── charts/               # (Phase 3)
│   │   └── process/              # (Phase 3)
│   ├── data/synthetic/           # Deterministic synthetic data
│   ├── lib/
│   │   ├── kpi/                  # KPI calculation engine
│   │   ├── constants/            # App constants
│   │   ├── formatting/           # (Phase 3)
│   │   └── validation/           # (Phase 3)
│   ├── types/                    # TypeScript domain types
│   └── tests/
│       ├── setup.ts              # Test configuration
│       ├── kpi-calculations.test.ts  # 34 KPI tests
│       ├── app-shell.test.tsx    # 7 component tests
│       └── e2e/smoke.spec.ts     # 6 Playwright tests
├── diagrams/
├── data/
├── portfolio/
├── .github/workflows/ci.yml      # CI pipeline
├── .env.example                  # Documented variables
└── package.json
```

---

## Privacy and Security

- **Zero API keys** — No AI API dependency
- **Zero data collection** — No analytics, cookies, or tracking
- **Zero real data** — All synthetic, clearly labeled
- **Zero backend** — Static site, no server or database
- **Public access** — No login, no authentication

---

## Future Phases

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 1 | Documentation Foundation | **Complete** |
| Phase 2 | Application Foundation | **Complete** |
| Phase 3 | Recruiter-Facing MVP | **Planned** |
| Phase 4 | Interactive Features | Planned |
| Phase 5 | Testing and Quality | Planned |
| Phase 6 | Deployment and Career Package | Planned |

---

## Disclaimer

**All data, companies, scenarios, and stakeholders in this project are fictional.** This is a portfolio case study demonstrating Business Analyst skills. No real client, caregiver, employer, or patient information is used.

---

## Author

**Titus Banks** — Business Analyst | WGU IT Management

This project is part of a comprehensive BA portfolio for job search and career development.
