# Change Log

**Company:** BrightCare Home Services (Fictional)  
**Document:** 25-change-log.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Change Log

| Version | Date | Author | Document | Change Description |
|---------|------|--------|----------|-------------------|
| 0.1 | 2026-07-21 | Titus Banks | 01-project-charter.md | Initial creation — Phase 1 |
| 0.1 | 2026-07-21 | Titus Banks | 02-business-problem.md | Initial creation |
| 0.1 | 2026-07-21 | Titus Banks | 03-business-case.md | Initial creation |
| 0.1 | 2026-07-21 | Titus Banks | 04-scope.md | Initial creation |
| 0.1 | 2026-07-21 | Titus Banks | 05-stakeholder-register.md | Initial creation — 10 fictional stakeholders |
| 0.1 | 2026-07-21 | Titus Banks | 06-stakeholder-analysis.md | Initial creation — power-interest matrix |
| 0.1 | 2026-07-21 | Titus Banks | 07-current-state-process.md | Initial creation — Mermaid diagram + 11 steps |
| 0.1 | 2026-07-21 | Titus Banks | 08-pain-point-analysis.md | Initial creation — 9 dimensions, 22 pain points |
| 0.1 | 2026-07-21 | Titus Banks | 09-business-requirements-document.md | Initial creation — full BRD |
| 0.1 | 2026-07-21 | Titus Banks | 10-business-requirements.md | Initial creation — BR-001 through BR-015 |
| 0.1 | 2026-07-21 | Titus Banks | 11-functional-requirements.md | Initial creation — FR-001 through FR-018 |
| 0.1 | 2026-07-21 | Titus Banks | 12-nonfunctional-requirements.md | Initial creation — NFR-001 through NFR-012 |
| 0.1 | 2026-07-21 | Titus Banks | 13-user-stories.md | Initial creation — US-001 through US-026 |
| 0.1 | 2026-07-21 | Titus Banks | 14-acceptance-criteria.md | Initial creation — AC-001 through AC-024 |
| 0.1 | 2026-07-21 | Titus Banks | 15-requirements-traceability-matrix.md | Initial creation — 15 traceability lines |
| 0.1 | 2026-07-21 | Titus Banks | 16-risk-register.md | Initial creation — R-001 through R-015 |
| 0.1 | 2026-07-21 | Titus Banks | 17-assumptions-and-constraints.md | Initial creation — 20 assumptions, 20 constraints |
| 0.1 | 2026-07-21 | Titus Banks | 18-kpi-dictionary.md | Initial creation — KPI-001 through KPI-008 |
| 0.1 | 2026-07-21 | Titus Banks | 19-data-dictionary.md | Initial creation — 10 entities defined |
| 0.1 | 2026-07-21 | Titus Banks | 20-product-backlog.md | Initial creation — 13 epics, 52 backlog items |
| 0.1 | 2026-07-21 | Titus Banks | 21-architecture-proposal.md | Initial creation — Next.js stack recommendation |
| 0.1 | 2026-07-21 | Titus Banks | 22-milestone-plan.md | Initial creation — 6-phase delivery plan |
| 0.1 | 2026-07-21 | Titus Banks | 23-definition-of-done.md | Initial creation — Phase 1-6 completion criteria |
| 0.1 | 2026-07-21 | Titus Banks | 24-decision-log.md | Initial creation — 10 key decisions |
| 0.1 | 2026-07-21 | Titus Banks | 25-change-log.md | Initial creation — this document |
| 0.1 | 2026-07-21 | Titus Banks | README.md | Initial creation |
| 0.1 | 2026-07-21 | Titus Banks | CHANGELOG.md | Initial creation |
| 0.2 | 2026-07-21 | Titus Banks | Multiple | **Phase 2: Application Foundation** — see below for detailed changes |
| 0.2 | 2026-07-21 | Titus Banks | package.json | Created with Next.js 15.5, TypeScript 5.8, Vitest, Playwright |
| 0.2 | 2026-07-21 | Titus Banks | tsconfig.json, next.config.ts, tailwind.config.ts | Application configuration files |
| 0.2 | 2026-07-21 | Titus Banks | postcss.config.mjs | PostCSS config with Tailwind + Autoprefixer |
| 0.2 | 2026-07-21 | Titus Banks | vitest.config.ts, playwright.config.ts | Test framework configuration |
| 0.2 | 2026-07-21 | Titus Banks | eslint.config.mjs | ESLint flat config |
| 0.2 | 2026-07-21 | Titus Banks | .env.example | Documented environment variables (none required) |
| 0.2 | 2026-07-21 | Titus Banks | .gitignore | Project-specific ignores |
| 0.2 | 2026-07-21 | Titus Banks | .github/workflows/ci.yml | GitHub Actions CI workflow |
| 0.2 | 2026-07-21 | Titus Banks | src/types/*.ts | Domain types: domain, requirements, risks, kpi, index |
| 0.2 | 2026-07-21 | Titus Banks | src/data/synthetic/*.ts | Synthetic data modules: shifts, caregivers, clients, escalations, documentation, issues, followups, kpi-input |
| 0.2 | 2026-07-21 | Titus Banks | src/lib/kpi/calculations.ts | 8 KPI calculation functions |
| 0.2 | 2026-07-21 | Titus Banks | src/lib/constants/index.ts | Application constants and KPI targets |
| 0.2 | 2026-07-21 | Titus Banks | src/components/layout/*.tsx | Header with mobile nav, Footer |
| 0.2 | 2026-07-21 | Titus Banks | src/components/ui/*.tsx | UI components: PageHeading, MetricCard, StatusBadge, ContentPanel, DataNotice, etc. |
| 0.2 | 2026-07-21 | Titus Banks | src/app/*.tsx | Root layout + landing page |
| 0.2 | 2026-07-21 | Titus Banks | src/app/*/page.tsx | 11 route pages with placeholder content |
| 0.2 | 2026-07-21 | Titus Banks | src/tests/kpi-calculations.test.ts | 34 KPI unit tests |
| 0.2 | 2026-07-21 | Titus Banks | src/tests/app-shell.test.tsx | 7 component tests |
| 0.2 | 2026-07-21 | Titus Banks | src/tests/e2e/smoke.spec.ts | 6 Playwright e2e tests |
| 0.2 | 2026-07-21 | Titus Banks | README.md | Updated with Phase 2 information |
| 0.2 | 2026-07-21 | Titus Banks | CHANGELOG.md | Updated with Phase 2 |
| 0.2 | 2026-07-21 | Titus Banks | 24-decision-log.md | Added Phase 2 decisions (DEC-011 through DEC-015) |
| 0.2 | 2026-07-21 | Titus Banks | 25-change-log.md | Updated with Phase 2 |

---

## Change Management Process

1. **Version numbering**: 0.x for internal drafts, 1.0 for Phase 1 sign-off
2. **Change tracking**: All changes recorded in this log with date, author, document, and description
3. **Review**: Changes reviewed as part of the quality control process before Phase 1 sign-off
4. **Approval**: Significant changes require approval per the stakeholder approval matrix

---

## Related Documents

- 24-decision-log.md — Decision tracking
- 23-definition-of-done.md — Completion criteria
