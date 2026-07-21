# Changelog

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
