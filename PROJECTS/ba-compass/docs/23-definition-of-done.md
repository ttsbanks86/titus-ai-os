# Definition of Done

**Company:** BrightCare Home Services (Fictional)  
**Document:** 23-definition-of-done.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Phase 1 Completion Criteria

Phase 1 is complete **only when** all of the following criteria are met:

### Documentation Completeness

| # | Criterion | Verification Method | Status |
|---|-----------|-------------------|--------|
| DOD-01 | Every listed document exists in the docs/ directory | File system check | ☐ |
| DOD-02 | All documents use the same project name (BA Compass) | Cross-document string search | ☐ |
| DOD-03 | All documents use the same fictional company name (BrightCare Home Services) | Cross-document string search | ☐ |
| DOD-04 | All documents include the disclaimer that data is fictional | Visual inspection | ☐ |
| DOD-05 | Every requirement has a unique ID in the correct format | Cross-reference check | ☐ |
| DOD-06 | Every high-priority feature is traceable through the RTM | RTM completeness check | ☐ |
| DOD-07 | Every KPI has a defined formula and data source | KPI dictionary review | ☐ |
| DOD-08 | Every risk has an identified mitigation strategy | Risk register review | ☐ |
| DOD-09 | All data is labeled as synthetic/fictional | Content scan | ☐ |
| DOD-10 | No real private information appears in any document | Content scan | ☐ |

### Consistency

| # | Criterion | Verification Method | Status |
|---|-----------|-------------------|--------|
| DOD-11 | No conflicting requirement statements across documents | Cross-document comparison | ☐ |
| DOD-12 | Priority levels are consistent across requirements, stories, and backlog | Priority audit | ☐ |
| DOD-13 | Requirement IDs are unique with no duplicates | ID scan | ☐ |
| DOD-14 | KPI formulas are internally consistent with data dictionary fields | Formula verification | ☐ |
| DOD-15 | Scope boundaries are consistently described across all documents | Scope audit | ☐ |

### Quality

| # | Criterion | Verification Method | Status |
|---|-----------|-------------------|--------|
| DOD-16 | All documents use professional Business Analyst language | Language review | ☐ |
| DOD-17 | Documents are readable and scannable with clear headings | Format review | ☐ |
| DOD-18 | No markdown syntax errors | Markdown validation | ☐ |
| DOD-19 | All cross-document links reference correct file paths | Link verification | ☐ |
| DOD-20 | Architecture is documented but not implemented | Codebase check | ☐ |

### Process

| # | Criterion | Verification Method | Status |
|---|-----------|-------------------|--------|
| DOD-21 | No production Titus Platform code was modified | Git status check | ☐ |
| DOD-22 | All new files are in the ba-compass project directory | Git status check | ☐ |
| DOD-23 | Decision log is updated with key decisions | Decision log review | ☐ |
| DOD-24 | Change log reflects document creation | Change log review | ☐ |
| DOD-25 | All files have been re-read and verified after creation | Re-read check | ☐ |

---

## Phase 2-6 Completion Criteria

### Phase 2: Application Foundation

- Next.js project initializes without errors
- TypeScript compiles with strict mode
- All synthetic data modules load correctly
- Basic routing works for all planned views
- Navigation component renders on all pages
- KPI calculation functions return correct values
- Application builds for production without errors

### Phase 3: Recruiter-Facing MVP

- Scenario selection screen displays BrightCare Home Services context
- Stakeholder register shows all 10 fictional roles
- Current-state process diagram renders with step details
- KPI dashboard shows 8 metrics with calculated values
- Business requirements table renders with filtering
- Risk register shows all 15 risks with scores
- Executive summary renders key findings and recommendations
- BRD viewer displays formatted document
- All views accessible without login
- Application functional on mobile (375px+)

### Phase 4: Interactive Features

- Requirement table supports sorting and filtering
- PDF export produces valid output
- Markdown export produces valid output
- Process comparison view renders correctly
- Demo data reset returns to initial state
- Deterministic mode produces consistent results
- Risk register supports category filtering

### Phase 5: Testing and Quality

- All unit tests pass (Vitest)
- Zero critical or serious accessibility violations (axe DevTools)
- All views functional at 375px, 768px, and 1920px viewports
- Application functional in Chrome, Firefox, Safari, Edge
- KPI values verified against formulas
- No console errors on any view
- Markdown files validate without errors

### Phase 6: Deployment and Career Package

- Application deployed and accessible at public URL
- Synthetic data disclaimer visible on every page
- Resume bullet points created for BA Compass
- LinkedIn profile updated with project
- Interview talking points documented
- Handshake portfolio submission ready
- Demo script created for recruiter walkthroughs

---

## Quality Gates

| Gate | Location | Check |
|------|----------|-------|
| Before Phase 2 start | Phase 1 completion | All Phase 1 DoD criteria met |
| Before Phase 3 start | Phase 2 completion | App builds, data loads, routing works |
| Before Phase 4 start | Phase 3 completion | MVP views functional, recruiter walkthrough passes |
| Before Phase 5 start | Phase 4 completion | Interactive features functional |
| Before Phase 6 start | Phase 5 completion | All tests pass, a11y clear |
| Project completion | Phase 6 completion | Deployed, career package ready |

---

## Related Documents

- 22-milestone-plan.md — Milestone schedule
- 24-change-log.md — Change tracking
