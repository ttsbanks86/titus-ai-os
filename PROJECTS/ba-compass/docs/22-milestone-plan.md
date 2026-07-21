# Milestone Plan

**Company:** BrightCare Home Services (Fictional)  
**Document:** 22-milestone-plan.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Milestone Overview

| Phase | Name | Target | Status |
|-------|------|--------|--------|
| Phase 1 | Documentation Foundation | Complete | Active |
| Phase 2 | Application Foundation | TBD | Planned |
| Phase 3 | Recruiter-Facing MVP | TBD | Planned |
| Phase 4 | Interactive Features | TBD | Planned |
| Phase 5 | Testing and Quality | TBD | Planned |
| Phase 6 | Deployment and Career Package | TBD | Planned |

---

## Phase 1: Documentation Foundation

| Element | Detail |
|---------|--------|
| Objective | Complete all 25 BA documentation deliverables for the BrightCare Home Services case study |
| Deliverables | Project charter, business problem, business case, scope, stakeholder register, stakeholder analysis, current-state process, pain-point analysis, BRD, business requirements, functional requirements, nonfunctional requirements, user stories, acceptance criteria, RTM, risk register, assumptions/constraints, KPI dictionary, data dictionary, product backlog, architecture proposal, milestone plan, definition of done, decision log, change log |
| Entry Criteria | Workspace inspected, project location confirmed, BrightCare Home Services defined |
| Exit Criteria | All 25 documents exist, internally consistent, traceable, and reviewed |
| Dependencies | None |
| Risks | Scope creep, inconsistent terminology, missing traceability links |
| Estimated Effort | 8-12 hours |

**Status: ACTIVE**

---

## Phase 2: Application Foundation

| Element | Detail |
|---------|--------|
| Objective | Set up the Next.js application scaffold with TypeScript, Tailwind CSS, and shadcn/ui |
| Deliverables | Next.js project initialized, synthetic data modules created, type definitions established, basic routing structure, navigation framework, data layer with KPI calculation functions |
| Entry Criteria | Phase 1 complete and signed off, architecture proposal approved |
| Exit Criteria | Application builds without errors, data modules compile, routing works, KPI calculations return correct values |
| Dependencies | Phase 1 complete |
| Risks | Build configuration issues, dependency conflicts, data structure mismatches with documentation |
| Estimated Effort | 4-6 hours |

**Status: Planned**

---

## Phase 3: Recruiter-Facing MVP

| Element | Detail |
|---------|--------|
| Objective | Build the core recruiter-facing views: scenario selection, stakeholder analysis, process mapping, KPI dashboard, requirements tables, risk register, executive summary |
| Deliverables | Scenario selection screen, stakeholder register view, current-state process visualization, KPI dashboard with calculated metrics, requirements table, risk register viewer, executive summary view, BRD viewer |
| Entry Criteria | Phase 2 complete, data layer functional, navigation system working |
| Exit Criteria | All core views render correctly with synthetic data, KPI calculations verified, navigation between views works, mobile responsive |
| Dependencies | Phase 2 complete |
| Risks | Poor recruiter usability, incorrect KPI display, missing data fields |
| Estimated Effort | 6-10 hours |

**Status: Planned**

---

## Phase 4: Interactive Features

| Element | Detail |
|---------|--------|
| Objective | Add interactivity: requirement filtering, export functions, process comparison, demo reset, deterministic mode |
| Deliverables | Requirement table with sorting/filtering, PDF and Markdown export, side-by-side process comparison, demo data reset, deterministic demo mode |
| Entry Criteria | Phase 3 complete and stable |
| Exit Criteria | All interactive features functional, exports produce valid output, demo reset returns application to initial state |
| Dependencies | Phase 3 complete |
| Risks | Export function failures, data reset corruption, complexity of deterministic mode |
| Estimated Effort | 4-8 hours |

**Status: Planned**

---

## Phase 5: Testing and Quality

| Element | Detail |
|---------|--------|
| Objective | Ensure application quality through unit tests, accessibility audit, mobile responsiveness testing, and cross-browser validation |
| Deliverables | Unit tests for KPI calculations, unit tests for data integrity, accessibility report (axe DevTools), mobile responsiveness verification, cross-browser test results |
| Entry Criteria | Phase 4 complete, application stable |
| Exit Criteria | All tests pass, zero critical/serious accessibility violations, all views functional at 375px+, functional in Chrome, Firefox, Safari, Edge |
| Dependencies | Phase 4 complete |
| Risks | Test coverage gaps, accessibility issues requiring structural changes, cross-browser layout differences |
| Estimated Effort | 3-5 hours |

**Status: Planned**

---

## Phase 6: Deployment and Career Package

| Element | Detail |
|---------|--------|
| Objective | Deploy the BA Compass application to Vercel and prepare career package materials |
| Deliverables | Vercel deployment, public URL, resume bullet points, LinkedIn profile updates, interview talking points, Handshake portfolio submission, demo script |
| Entry Criteria | Phase 5 complete, all tests passing |
| Exit Criteria | Application accessible at public URL, career package complete and ready for use |
| Dependencies | Phase 5 complete |
| Risks | Deployment configuration issues, domain setup delays, career material quality |
| Estimated Effort | 3-5 hours |

**Status: Planned**

---

## Milestone Dependencies

```
Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4 ──→ Phase 5 ──→ Phase 6
(Docs)     (Scaffold)  (MVP)       (Features)  (Testing)   (Deploy)
```

Each phase builds on the previous. Phase 1 documentation defines what Phase 2-4 will implement. Phase 3 delivers the minimum recruiter-viable product. Phases 4-5 add quality and polish. Phase 6 makes it public.

---

## Risk Mitigation per Phase

| Phase | Key Risk | Mitigation |
|-------|----------|------------|
| Phase 1 | Inconsistent documentation | Cross-document review checklist |
| Phase 2 | Build configuration issues | Use proven Next.js template |
| Phase 3 | Poor usability | Recruiter walkthrough design upfront |
| Phase 4 | Export failures | Test with sample data early |
| Phase 5 | Test gaps | Define test cases alongside requirements |
| Phase 6 | Deployment delays | Test Vercel build before final phase |

---

## Related Documents

- 20-product-backlog.md — Detailed task breakdown
- 23-definition-of-done.md — Completion criteria per phase
