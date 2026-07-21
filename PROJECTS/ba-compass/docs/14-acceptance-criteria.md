# Acceptance Criteria

**Company:** BrightCare Home Services (Fictional)
**Document:** 14-acceptance-criteria.md
**Date:** July 21, 2026
**Author:** Titus Banks — Business Analyst

---

## Format

All criteria follow the Given/When/Then format:

```
Given [context/state]
When [action/trigger]
Then [expected outcome]
```

---

## Acceptance Criteria

### AC-001: Public Access Without Login

| Field | Value |
|-------|-------|
| ID | AC-001 |
| Linked User Story | US-001 |
| Given | A recruiter navigates to the BA Compass application URL |
| When | The application loads |
| Then | The application displays content without any login prompt, registration form, or authentication barrier |
| Verification | Manual walkthrough — no auth prompt appears |
| Priority | High |

### AC-002: Synthetic Scenario Launch

| Field | Value |
|-------|-------|
| ID | AC-002 |
| Linked User Story | US-002 |
| Given | The BA Compass application is loaded |
| When | The user selects the BrightCare Home Services scenario |
| Then | A business context overview is displayed showing the fictional company name, industry, and key operational problems |
| Verification | Scenario loads with BrightCare branding and problem summary |
| Priority | High |

### AC-003: Stakeholder Analysis Visibility

| Field | Value |
|-------|-------|
| ID | AC-003 |
| Linked User Story | US-003 |
| Given | The user is viewing the scenario |
| When | The user navigates to the stakeholder analysis view |
| Then | A stakeholder register with 10 fictional roles is displayed, each with role, interest, influence, and pain points |
| Verification | All 10 stakeholders visible with complete profiles |
| Priority | High |

### AC-004: Process Visibility

| Field | Value |
|-------|-------|
| ID | AC-004 |
| Linked User Stories | US-004, US-013 |
| Given | The user is viewing the scenario |
| When | The user navigates to the process view |
| Then | A current-state process flow is displayed with at least 10 steps, each showing actor, action, failure points, and delays |
| Verification | Process diagram and step details visible |
| Priority | High |

### AC-005: Requirements Traceability

| Field | Value |
|-------|-------|
| ID | AC-005 |
| Linked User Stories | US-005, US-012 |
| Given | The user is viewing the requirements traceability matrix |
| When | The user inspects any high-priority requirement |
| Then | The requirement is linked to a business problem, stakeholder need, functional requirement, user story, acceptance criterion, KPI, and test method |
| Verification | RTM shows all links for each high-priority requirement |
| Priority | High |

### AC-006: KPI Calculations

| Field | Value |
|-------|-------|
| ID | AC-006 |
| Linked User Stories | US-006, US-014 |
| Given | The user is viewing the KPI dashboard |
| When | The dashboard loads |
| Then | At least 8 KPIs are displayed with current calculated values, target values, and visual indicators (above/below target) |
| Verification | Each KPI value matches its formula when calculated against demo data |
| Priority | High |

### AC-007: BRD Accessibility

| Field | Value |
|-------|-------|
| ID | AC-007 |
| Linked User Story | US-007 |
| Given | The user is viewing the scenario |
| When | The user navigates to the BRD view |
| Then | A formatted Business Requirements Document is displayed with executive summary, background, scope, requirements, and KPIs |
| Verification | BRD document renders with all major sections |
| Priority | High |

### AC-008: Mobile Display

| Field | Value |
|-------|-------|
| ID | AC-008 |
| Linked User Story | US-008 |
| Given | A recruiter opens the application on a mobile device (375px viewport) |
| When | The application loads |
| Then | All major views are functional and readable without horizontal scrolling |
| Verification | Dashboard, stakeholders, processes, requirements, KPI views all render at 375px |
| Priority | High |

### AC-009: Export Function

| Field | Value |
|-------|-------|
| ID | AC-009 |
| Linked User Story | US-009 |
| Given | The user is viewing a KPI dashboard, requirements list, or risk register |
| When | The user clicks the export button |
| Then | Content is exported as a downloadable PDF or Markdown file |
| Verification | Export function produces valid file |
| Priority | Medium |

### AC-010: Given/When/Then Format

| Field | Value |
|-------|-------|
| ID | AC-010 |
| Linked User Story | US-010 |
| Given | The user is viewing acceptance criteria |
| When | Any criterion is displayed |
| Then | It follows the Given/When/Then format with clear context, action, and expected outcome |
| Verification | All displayed criteria use the standard format |
| Priority | High |

### AC-011: Risk Register Visibility

| Field | Value |
|-------|-------|
| ID | AC-011 |
| Linked User Stories | US-011, US-024 |
| Given | The user navigates to the risk register view |
| When | The page loads |
| Then | At least 12 risks are displayed with description, category, likelihood, impact, risk score, and mitigation strategy |
| Verification | Risk register shows complete data for all risks |
| Priority | High |

### AC-012: Shift Status View

| Field | Value |
|-------|-------|
| ID | AC-012 |
| Linked User Story | US-013 |
| Given | The user is viewing the operational dashboard |
| When | The dashboard loads |
| Then | Shift status summary is displayed showing counts of confirmed, unconfirmed, in-progress, completed, and missed shifts |
| Verification | Shift status distribution visible |
| Priority | High |

### AC-013: Gap Highlighting

| Field | Value |
|-------|-------|
| ID | AC-013 |
| Linked User Story | US-015 |
| Given | The user is viewing the operational dashboard |
| When | There are open staffing gaps in the demo data |
| Then | The gaps are visually highlighted with a count and details |
| Verification | Open gap count matches demo data |
| Priority | High |

### AC-014: Unconfirmed Shift Alert

| Field | Value |
|-------|-------|
| ID | AC-014 |
| Linked User Story | US-016 |
| Given | The user is viewing shift status |
| When | Shifts exist that have not been confirmed |
| Then | Unconfirmed shifts are identified with status indicator |
| Verification | Unconfirmed shifts visible |
| Priority | High |

### AC-015: Late Arrival Flagging

| Field | Value |
|-------|-------|
| ID | AC-015 |
| Linked User Story | US-017 |
| Given | The user is viewing arrival time data |
| When | A caregiver arrived more than 15 minutes after the scheduled start |
| Then | The arrival is flagged as late |
| Verification | Late arrival threshold works correctly |
| Priority | High |

### AC-016: Requirements with Unique IDs

| Field | Value |
|-------|-------|
| ID | AC-016 |
| Linked User Story | US-018 |
| Given | The user is viewing requirements |
| When | Any requirement is displayed |
| Then | It has a unique ID in the format BR-XXX, FR-XXX, or NFR-XXX |
| Verification | No duplicate IDs across all requirements |
| Priority | High |

### AC-017: Requirement-Business Problem Link

| Field | Value |
|-------|-------|
| ID | AC-017 |
| Linked User Story | US-019 |
| Given | The user inspects any business requirement |
| When | The requirement details are expanded |
| Then | The business problem it addresses and the KPI it impacts are displayed |
| Verification | Links to problem and KPI visible for each BR |
| Priority | High |

### AC-018: Executive Summary Access

| Field | Value |
|-------|-------|
| ID | AC-018 |
| Linked User Stories | US-020, US-023 |
| Given | The user navigates to the executive summary view |
| When | The page loads |
| Then | Key findings, recommendations, and KPI highlights are displayed in a concise format |
| Verification | Executive summary renders with all sections |
| Priority | High |

### AC-019: Documentation Completion Rate

| Field | Value |
|-------|-------|
| ID | AC-019 |
| Linked User Story | US-021 |
| Given | The user is viewing the KPI dashboard or documentation view |
| When | The documentation completion KPI is displayed |
| Then | The percentage of shifts with completed documentation is shown, calculated from demo data |
| Verification | KPI value matches formula calculation |
| Priority | High |

### AC-020: Escalation Time Tracking

| Field | Value |
|-------|-------|
| ID | AC-020 |
| Linked User Story | US-022 |
| Given | The user is viewing escalation data |
| When | Escalation records are displayed |
| Then | Each escalation shows the time from identification to resolution |
| Verification | Escalation time calculated and displayed |
| Priority | Medium |

### AC-021: No Backend Required

| Field | Value |
|-------|-------|
| ID | AC-021 |
| Linked User Story | US-025 |
| Given | The application is deployed on Vercel or served as static files |
| When | Any page is loaded |
| Then | All content and functionality work without a backend server or API calls |
| Verification | Application runs as static export |
| Priority | High |

### AC-022: No API Key Required

| Field | Value |
|-------|-------|
| ID | AC-022 |
| Linked User Story | US-026 |
| Given | A user opens the BA Compass application |
| When | The application loads and functions |
| Then | No API key configuration, environment variables, or external service credentials are required |
| Verification | Full functionality without any API key |
| Priority | High |

### AC-023: Private Data Verification

| Field | Value |
|-------|-------|
| ID | AC-023 |
| Linked User Story | US-002 |
| Given | Any page or exported document in the application |
| When | The content is inspected |
| Then | No real names, addresses, phone numbers, emails, or medical information appear |
| Verification | All data uses fictional names and synthetic patterns |
| Priority | High |

### AC-024: Future-State Comparison

| Field | Value |
|-------|-------|
| ID | AC-024 |
| Linked User Story | US-004 |
| Given | The user is viewing process maps |
| When | The user switches to future-state view or comparison view |
| Then | Improvements from the current state are highlighted or described |
| Verification | Future-state process shows addressed gaps |
| Priority | Medium |

---

## Criteria Summary

| Priority | Count | IDs |
|----------|-------|-----|
| High | 19 | AC-001 through AC-008, AC-010 through AC-019, AC-021 through AC-023 |
| Medium | 5 | AC-009, AC-020, AC-024 |
| Low | 0 | — |
| **Total** | **24** | AC-001 through AC-024 |

---

## Mapping to User Stories

| User Story | Acceptance Criteria |
|-----------|-------------------|
| US-001 | AC-001 |
| US-002 | AC-002, AC-023 |
| US-003 | AC-003 |
| US-004 | AC-004, AC-024 |
| US-005 | AC-005 |
| US-006 | AC-006 |
| US-007 | AC-007 |
| US-008 | AC-008 |
| US-009 | AC-009 |
| US-010 | AC-010 |
| US-011 | AC-011 |
| US-012 | AC-005 |
| US-013 | AC-012 |
| US-014 | AC-006 |
| US-015 | AC-013 |
| US-016 | AC-014 |
| US-017 | AC-015 |
| US-018 | AC-016 |
| US-019 | AC-017 |
| US-020 | AC-018 |
| US-021 | AC-019 |
| US-022 | AC-020 |
| US-023 | AC-018 |
| US-024 | AC-011 |
| US-025 | AC-021 |
| US-026 | AC-022 |

---

## Related Documents

- 13-user-stories.md — User stories
- 15-requirements-traceability-matrix.md — Traceability
