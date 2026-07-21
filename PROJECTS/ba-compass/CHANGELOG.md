# Changelog

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
