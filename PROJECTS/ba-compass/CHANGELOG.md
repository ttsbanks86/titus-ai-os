# Changelog

## 0.4 (2026-07-21)

### Phase 4: Interactive Analysis and Document Export

- **Phase 3 reconciliation:** Corrected chart count (5, not 4) and gap count (21, not 20). Added missing PP-PEOPLE-03 gap item.
- **Requirements context:** React Context + useReducer + localStorage for editable requirements. Default data from approved source. Edits are local only.
- **Edit Demo mode:** Inline textarea editing for BR statements, select for priority/status. Edit/Cancel/Reset per requirement. Read-only is default.
- **Requirements validation:** 7 validation rules (ID format, statement length, priority, status, owner, justification, KPI ref). 23 unit tests.
- **Requirements export:** Markdown (.md) and CSV (.csv) with synthetic-case-study notice, local edit indicators.
- **BRD viewer:** /brd route with 12 sections, table of contents navigation, Markdown export, Print/PDF support.
- **Traceability matrix:** /traceability route with 15 traceability links, search, status filter, coverage summary, MD/CSV/Print export.
- **Risk register export:** Markdown and CSV export added to /risks page.
- **Executive summary:** /executive-summary route with 5 findings, KPI summary, top risks, recommendations, MD/Print export.
- **KPI time-period filtering:** Full period / Week 1 / Week 2 filters recalculating charts and metrics from filtered data.
- **Dashboard drill-down:** Clickable metric cards showing contributing synthetic records with status, date, and inclusion reason.
- **Demo reset:** Confirmation dialog, restores approved defaults, clears localStorage, status feedback.
- **Print styles:** Hide navigation, edit controls. Preserve headings, tables, synthetic notice. Page-break handling.
- **Navigation:** Added BRD, Traceability, Executive Summary to NAV_ITEMS (14 items) and NAV_SEQUENCE (15 items).
- **Accessibility:** Edit controls labeled, validation errors use role="alert", reset confirmation keyboard accessible, metric drill-down uses aria-expanded.
- **Local storage:** Edits stored in "ba-compass-requirements-edits" key. Corrupt data handled gracefully. Reset clears only project keys.
- **76 unit tests** (23 validation + 34 KPI + 19 content) — all passing.
- **13 Playwright e2e tests** — all passing.
- **18 static pages** — all generating successfully.

## 0.3 (2026-07-21)

### Phase 3: Recruiter-Facing MVP

- Complete recruiter-facing landing page with KPI snapshot and project overview
- Project overview page with BA lifecycle (Discover → Analyze → Define → Design → Validate → Recommend)
- Stakeholder analysis page with all 10 roles, power-interest matrix, expandable profiles, and conflict resolution
- Current-state process page with 11-step flow visualization, expandable step details, and channel reliability table
- Gap analysis page with 22 pain points across 9 dimensions, severity counts, dimension filtering, and gap summary
- KPI dashboard with 8 live metric cards, 4 Recharts visualizations (pie, bar), and KPI definitions table
- Future-state process page with side-by-side comparison table and improvement detail cards linked to requirements/KPIs
- Requirements page with 45 BR/FR/NFR, type/priority/search filtering, and user stories toggle
- Risk register page with 15 risks, risk heatmap matrix, category filtering, and expandable risk details
- Recommendations page with 11 prioritized recommendations across immediate/near-term/future categories
- About the Project page with My Contribution section (12 BA work items), tools, testing, and privacy
- Responsible AI page with 10-item checklist, risk considerations, data ethics, and transparency note
- Sequential prev/next navigation on all content pages
- 53 unit tests (34 KPI + 19 content/component) — all passing
- 11 Playwright e2e tests covering full recruiter journey — all passing
- Mobile-responsive navigation with functional menu
- Accessibility: skip link, role regions, aria labels, focus states, text alternatives for charts

## 0.2 (2026-07-21)

### Phase 2: Application Foundation

- Next.js 15.5 application initialized with TypeScript strict mode
- 13 static routes created with layout and navigation
- Domain types defined matching docs/19-data-dictionary.md
- Deterministic synthetic dataset (42 shifts, 10 caregivers, 8 clients)
- 8 KPI calculation functions matching docs/18-kpi-dictionary.md
- 34 KPI unit tests + 7 component tests (41 total, all passing)
- 6 Playwright e2e smoke tests (all passing)
- UI foundation: PageHeading, MetricCard, StatusBadge, ContentPanel, DataNotice
- Professional app shell with header, footer, mobile nav, skip link
- Synthetic data notice on every page
- Production build succeeds (15 static pages)
- GitHub Actions CI workflow
- .env.example with documented variables
- Privacy scan: zero secrets, zero real data exposure
- Dependency audit: 2 moderate (documented, no fix available)

## 0.1 (2026-07-21)

- Phase 1 documentation foundation complete
- 25 Business Analyst deliverables created
- Project structure established at `PROJECTS/ba-compass/`
- Fictional company: BrightCare Home Services
