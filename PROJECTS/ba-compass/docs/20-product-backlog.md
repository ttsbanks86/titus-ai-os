# Product Backlog

**Company:** BrightCare Home Services (Fictional)  
**Document:** 20-product-backlog.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Backlog Epics

| Epic | Description | Priority |
|------|-------------|----------|
| EPIC-01 | Business Scenario | Scenario selection and business context views |
| EPIC-02 | Stakeholder Analysis | Stakeholder register and power-interest views |
| EPIC-03 | Process Mapping | Current-state and future-state process visualization |
| EPIC-04 | Gap Analysis | Pain-point analysis and gap identification views |
| EPIC-05 | KPI Dashboard | Metric display, trends, and filtering |
| EPIC-06 | Requirements Management | Requirement tables, filtering, and display |
| EPIC-07 | Risk Register | Risk identification and mitigation display |
| EPIC-08 | BRD and Executive Summary | Document viewer and summary views |
| EPIC-09 | Responsible AI | AI ethics and transparency documentation |
| EPIC-10 | Recruiter Experience | Navigation, exports, mobile responsiveness |
| EPIC-11 | Testing | Unit tests, accessiblity, quality verification |
| EPIC-12 | Deployment | Vercel deployment and public access |
| EPIC-13 | Career Package | Resume, LinkedIn, interview materials |

---

## Backlog Items

### EPIC-01: Business Scenario

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-001 | Scenario selection screen with BrightCare Home Services overview | High | 2 days | None | AC-002 | BR-001 | Planned |
| BL-002 | Business context view showing company background and operational problems | High | 1 day | BL-001 | AC-002 | BR-001 | Planned |
| BL-003 | Scenario data loader for synthetic demo data | High | 2 days | None | AC-002 | BR-013 | Planned |

### EPIC-02: Stakeholder Analysis

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-004 | Stakeholder register view with 10 fictional roles | High | 2 days | BL-001 | AC-003 | BR-001 | Planned |
| BL-005 | Power-interest matrix visualization | Medium | 1 day | BL-004 | AC-003 | BR-001 | Planned |
| BL-006 | Stakeholder detail view with pain points and needs | High | 1 day | BL-004 | AC-003 | BR-001 | Planned |

### EPIC-03: Process Mapping

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-007 | Current-state process flow diagram | High | 2 days | BL-001 | AC-004 | BR-001, BR-002 | Planned |
| BL-008 | Step-by-step process detail view | High | 1 day | BL-007 | AC-004 | BR-001, BR-002 | Planned |
| BL-009 | Future-state process flow diagram | High | 2 days | BL-007 | AC-024 | BR-001, BR-002, BR-003 | Planned |
| BL-010 | Side-by-side process comparison view | Medium | 2 days | BL-007, BL-009 | AC-024 | BR-001, BR-002 | Planned |

### EPIC-04: Gap Analysis

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-011 | Pain-point analysis view categorized by area | High | 2 days | BL-001 | AC-004 | BR-001 through BR-015 | Planned |
| BL-012 | Gap summary table with severity ratings | Medium | 1 day | BL-011 | AC-004 | BR-001 through BR-015 | Planned |

### EPIC-05: KPI Dashboard

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-013 | KPI dashboard with 8 operational metrics | High | 3 days | BL-001 | AC-006 | BR-008 | Planned |
| BL-014 | KPI trend visualization over time | High | 2 days | BL-013 | AC-006 | BR-008 | Planned |
| BL-015 | KPI filtering by time period | Medium | 1 day | BL-013 | AC-006 | BR-008 | Planned |
| BL-016 | Target vs actual comparison indicators | High | 1 day | BL-013 | AC-006 | BR-008 | Planned |

### EPIC-06: Requirements Management

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-017 | Business requirements table with filtering | High | 2 days | BL-001 | AC-016 | BR-001 through BR-015 | Planned |
| BL-018 | Functional requirements view | High | 1 day | BL-017 | AC-016 | FR-001 through FR-018 | Planned |
| BL-019 | Nonfunctional requirements view | High | 1 day | BL-017 | AC-016 | NFR-001 through NFR-012 | Planned |
| BL-020 | Requirements traceability matrix view | High | 2 days | BL-017 | AC-005 | All requirements | Planned |
| BL-021 | User stories organized by role | High | 2 days | BL-017 | AC-010 | US-001 through US-026 | Planned |
| BL-022 | Acceptance criteria display (Given/When/Then) | High | 1 day | BL-021 | AC-010 | US-001 through US-026 | Planned |

### EPIC-07: Risk Register

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-023 | Risk register view with scores and mitigations | High | 2 days | BL-001 | AC-011 | BR-009 | Planned |
| BL-024 | Risk category and severity filtering | Medium | 1 day | BL-023 | AC-011 | BR-009 | Planned |

### EPIC-08: BRD and Executive Summary

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-025 | BRD document viewer within application | High | 3 days | BL-017 | AC-007 | BR-001 through BR-015 | Planned |
| BL-026 | Executive summary view with findings and recommendations | High | 2 days | BL-013, BL-025 | AC-018 | BR-008 | Planned |
| BL-027 | Data dictionary display | Medium | 1 day | BL-001 | — | All | Planned |

### EPIC-09: Responsible AI

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-028 | AI ethics documentation view (future AI integration plan) | Medium | 1 day | BL-001 | — | None | Planned |
| BL-029 | Transparency note on synthetic data generation | High | 0.5 day | None | AC-023 | BR-014 | Planned |

### EPIC-10: Recruiter Experience

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-030 | Navigation system between all views | High | 2 days | BL-001 | AC-001 | BR-013 | Planned |
| BL-031 | Export requirements to Markdown | Medium | 1 day | BL-017 | AC-009 | BR-012 | Planned |
| BL-032 | Export dashboard to PDF | Medium | 2 days | BL-013 | AC-009 | BR-012 | Planned |
| BL-033 | Export risk register to Markdown | Medium | 1 day | BL-023 | AC-009 | BR-012 | Planned |
| BL-034 | Mobile-responsive layout for all views | High | 3 days | All views | AC-008 | BR-015 | Planned |
| BL-035 | Synthetic data disclaimer on every page | High | 0.5 day | None | AC-023 | BR-014 | Planned |
| BL-036 | Deterministic demo data mode | Medium | 1 day | BL-003 | AC-001 | BR-013 | Planned |
| BL-037 | Demo data reset capability | Medium | 1 day | BL-003 | AC-001 | BR-013 | Planned |

### EPIC-11: Testing

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-038 | Unit tests for KPI calculation functions | High | 2 days | BL-013 | AC-006 | BR-008, NFR-011 | Planned |
| BL-039 | Unit tests for data integrity | High | 1 day | BL-003 | — | NFR-011 | Planned |
| BL-040 | Accessibility audit (axe DevTools) | High | 1 day | All views | AC-005 | NFR-001 | Planned |
| BL-041 | Mobile responsiveness testing | High | 1 day | BL-034 | AC-008 | NFR-003 | Planned |
| BL-042 | Cross-browser testing | Medium | 1 day | All views | AC-008 | NFR-009 | Planned |
| BL-043 | Recruiter walkthrough script | Medium | 1 day | All views | — | BR-013 | Planned |

### EPIC-12: Deployment

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-044 | Next.js project setup | High | 1 day | None | — | — | Planned |
| BL-045 | Vercel deployment configuration | High | 0.5 day | BL-044 | AC-021 | NFR-008 | Planned |
| BL-046 | Domain or Vercel subdomain setup | High | 0.5 day | BL-045 | AC-001 | BR-013 | Planned |
| BL-047 | Build verification and smoke test | High | 0.5 day | BL-045 | AC-021 | NFR-008 | Planned |

### EPIC-13: Career Package

| ID | Description | Priority | Effort | Dependencies | AC Refs | BR Links | Status |
|----|-------------|----------|--------|-------------|---------|----------|--------|
| BL-048 | Resume bullet points for BA Compass | High | 1 day | All views | — | — | Planned |
| BL-049 | LinkedIn profile updates | High | 1 day | BL-048 | — | — | Planned |
| BL-050 | Interview talking points and demo script | High | 1 day | BL-048 | — | — | Planned |
| BL-051 | Handshake portfolio submission | High | 0.5 day | BL-046 | — | — | Planned |
| BL-052 | Portfolio README with project overview | High | 1 day | All docs | — | — | Planned |

---

## MVP Prioritization

For the recruiter-ready MVP (Phase 3), the following backlog items are critical:

| Priority | Items |
|----------|-------|
| Must Have | BL-001, BL-002, BL-003, BL-004, BL-006, BL-007, BL-008, BL-011, BL-013, BL-014, BL-016, BL-017, BL-020, BL-021, BL-022, BL-023, BL-025, BL-026, BL-030, BL-034, BL-035, BL-044, BL-045 |
| Should Have | BL-005, BL-009, BL-010, BL-012, BL-015, BL-024, BL-027, BL-031, BL-032, BL-033, BL-036, BL-037 |
| Nice to Have | BL-028, BL-038, BL-039, BL-040, BL-041, BL-042, BL-043, BL-046, BL-047, BL-048, BL-049, BL-050, BL-051, BL-052 |

---

## Effort Summary

| Epic | Items | Total Effort |
|------|-------|-------------|
| EPIC-01 Business Scenario | 3 | 5 days |
| EPIC-02 Stakeholder Analysis | 3 | 4 days |
| EPIC-03 Process Mapping | 4 | 7 days |
| EPIC-04 Gap Analysis | 2 | 3 days |
| EPIC-05 KPI Dashboard | 4 | 7 days |
| EPIC-06 Requirements Management | 6 | 9 days |
| EPIC-07 Risk Register | 2 | 3 days |
| EPIC-08 BRD and Executive Summary | 3 | 6 days |
| EPIC-09 Responsible AI | 2 | 1.5 days |
| EPIC-10 Recruiter Experience | 8 | 10.5 days |
| EPIC-11 Testing | 6 | 7 days |
| EPIC-12 Deployment | 4 | 2.5 days |
| EPIC-13 Career Package | 5 | 4.5 days |
| **Total** | **52** | **~70 days** |

---

## Related Documents

- 22-milestone-plan.md — Phased delivery schedule
- 10-business-requirements.md — BR links
- 14-acceptance-criteria.md — AC references
