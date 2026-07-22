# BA Compass

**AI-Assisted Business Process and Requirements Analyzer**

A recruiter-ready Business Analyst portfolio project demonstrating end-to-end business analysis through a fictional home-care services case study.

[Live Demo](https://ba-compass.vercel.app) · [GitHub](#) · [5-Minute Recruiter Tour](/tour)

---

## About This Project

BA Compass showcases how a Business Analyst identifies operational problems, analyzes stakeholders, documents requirements, designs process improvements, defines success metrics, and communicates recommendations to executives.

**Case Study:** BrightCare Home Services — a fictional home-care company experiencing missed shifts, late arrivals, incomplete service documentation, delayed escalation, and no operational visibility.

**My Role:** Business Analyst — problem definition, stakeholder analysis, process mapping, gap analysis, requirements engineering, KPI design, risk assessment, future-state design, and portfolio application validation.

> **All data is synthetic.** BrightCare Home Services is a fictional company. No real client, caregiver, or patient information is used.

---

## Business Analyst Competencies Demonstrated

| Competency | Deliverable |
|-----------|-------------|
| Business Problem Analysis | Project charter, business problem statement |
| Stakeholder Engagement | Stakeholder register, power-interest matrix, conflict resolution |
| Process Modeling | 11-step current-state process with failure analysis |
| Gap Analysis | 21 pain points across 9 business dimensions |
| Requirements Engineering | 15 BR, 18 FR, 12 NFR with traceability |
| User Story Development | 26 user stories with acceptance criteria |
| KPI Definition | 8 operational metrics with formulas and targets |
| Risk Management | 15 risks with mitigation and contingency plans |
| Future-State Design | 8-process improvement comparison |
| Executive Communication | BRD, executive summary, recommendations |
| Responsible AI Planning | AI ethics checklist and transparency documentation |
| Solution Validation | 76 unit tests, 14 e2e tests, accessibility review |

---

## Application Features

| Feature | Description |
|---------|-------------|
| **KPI Dashboard** | 8 live metrics with Recharts visualizations and period filtering |
| **Requirements Manager** | Edit demo mode, validation, localStorage persistence, reset |
| **BRD Viewer** | Complete Business Requirements Document with 12 sections |
| **Traceability Matrix** | 15 traceability links with search, filters, and coverage summary |
| **Risk Register** | 15 risks with heatmap, category filtering, and export |
| **Executive Summary** | Key findings, KPIs, and recommendations |
| **Process Maps** | 11-step current-state and 8-improvement future-state |
| **Stakeholder Analysis** | Power-interest matrix and 10 stakeholder profiles |
| **Recruiter Tour** | 10-step guided walkthrough (Start at [/tour](/tour)) |
| **Export** | Markdown and CSV export for requirements, risks, traceability |
| **Print** | Print-friendly views for all documentation pages |

---

## Quick Metrics

| Metric | Count |
|--------|-------|
| BA Documentation Deliverables | 25 |
| Business Requirements | 15 (BR-001 through BR-015) |
| Functional Requirements | 18 (FR-001 through FR-018) |
| Nonfunctional Requirements | 12 (NFR-001 through NFR-012) |
| User Stories | 26 |
| Acceptance Criteria | 24 |
| Stakeholders | 10 |
| Risks | 15 (R-001 through R-015) |
| KPIs | 8 (KPI-001 through KPI-008) |
| Application Routes | 19 |
| Unit Tests | 76 |
| E2E Tests | 14 |

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 15.5 (App Router) |
| Language | TypeScript (strict mode) |
| Styling | Tailwind CSS 3 |
| Charts | Recharts |
| Icons | Lucide React |
| State | React Context + useReducer + localStorage |
| Unit Tests | Vitest + Testing Library |
| E2E Tests | Playwright (Chromium, Firefox, WebKit) |
| CI | GitHub Actions |
| Deployment | Vercel (static export) |

**Zero external dependencies:** No AI API, no database, no backend server, no authentication.

---

## Getting Started

```bash
# Clone and navigate
cd PROJECTS/ba-compass

# Install dependencies
npm install

# Start development
npm run dev

# Run tests
npm run test          # 76 unit tests
npm run test:e2e      # 14 Playwright e2e tests

# Production build
npm run build

# Full validation
npm run validate
```

---

## Project Structure

```
PROJECTS/ba-compass/
├── docs/                     # 41 BA documentation files
├── src/
│   ├── app/                  # 19 Next.js App Router pages
│   ├── components/           # Reusable UI components
│   ├── data/
│   │   ├── synthetic/        # Deterministic synthetic dataset
│   │   └── content/          # BA content modules
│   ├── lib/
│   │   ├── kpi/              # 8 KPI calculation functions
│   │   ├── validation/       # Requirements validation
│   │   ├── export/           # Markdown/CSV export utilities
│   │   ├── state/            # React Context state management
│   │   └── constants/        # Application constants
│   ├── types/                # TypeScript domain types
│   └── tests/                # Unit and e2e tests
├── portfolio/                # Career package materials
├── public/                   # Social preview asset
└── package.json
```

---

## Quality and Accessibility

- **Zero critical or serious accessibility violations** (verified keyboard-only, skip link, ARIA landmarks, screen reader)
- **Cross-browser tested** (Chromium, Firefox, WebKit — 14/14 tests pass on all engines)
- **Responsive** (320px through 1920px)
- **Zero console errors**
- **Zero hydration errors**
- **Zero API keys or secrets** in codebase
- **Zero analytics or tracking**
- **All data clearly labeled as synthetic**

---

## Responsible AI Disclosure

The BA Compass application uses **no AI services** for its core functionality. All KPI calculations are deterministic. All requirements, risks, and recommendations were developed through structured BA methodology.

AI tools assisted with code generation and content drafting. Every BA artifact was reviewed, validated, and edited by a human Business Analyst. The analytical framework, methodology, and conclusions are the author's own work.

---

## Known Limitations

- Static synthetic dataset (2 weeks of data, not dynamic)
- No real-time AI integration (future optional feature)
- No user authentication (intentional — public portfolio)
- No backend database (static export architecture)
- Export uses Markdown and browser print-to-PDF (no PDF library)
- localStorage-dependent editing (cleared on browser data reset)

---

## License

MIT © 2026 Titus Banks. Application source code is open for review and reuse. Case-study narrative and BA documentation are original authored work — attribution appreciated when shared.

---

## Author

**Titus Banks** — Business Analyst | WGU IT Management

This project is part of a comprehensive BA portfolio for job search and career development.
