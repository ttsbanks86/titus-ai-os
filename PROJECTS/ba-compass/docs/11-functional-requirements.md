# Functional Requirements

**Company:** BrightCare Home Services (Fictional)  
**Document:** 11-functional-requirements.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Functional Requirements

### FR-001: Operational Dashboard

| Field | Value |
|-------|-------|
| ID | FR-001 |
| Statement | The application shall provide a dashboard view displaying shift status, open gaps, escalation count, and documentation completion percentage. |
| Business Justification | Users need immediate visibility into operational health without navigating multiple screens. |
| Priority | High |
| Linked BR | BR-001, BR-006 |
| Status | Proposed |

### FR-002: Scenario Selection

| Field | Value |
|-------|-------|
| ID | FR-002 |
| Statement | The application shall provide a scenario selection screen where users can choose from pre-defined operational scenarios. |
| Business Justification | Recruiters need to understand the business context before exploring analysis details. |
| Priority | High |
| Linked BR | BR-001 |
| Status | Proposed |

### FR-003: Stakeholder Register View

| Field | Value |
|-------|-------|
| ID | FR-003 |
| Statement | The application shall display a stakeholder register with roles, interests, influence levels, and pain points. |
| Business Justification | Stakeholder analysis is a core BA deliverable that recruiters expect to see. |
| Priority | High |
| Linked BR | BR-001 |
| Status | Proposed |

### FR-004: Current-State Process View

| Field | Value |
|-------|-------|
| ID | FR-004 |
| Statement | The application shall display the current-state (as-is) process flow with step details including actor, input, action, output, delays, and failure points. |
| Business Justification | Demonstrates ability to document and analyze existing workflows. |
| Priority | High |
| Linked BR | BR-001, BR-002 |
| Status | Proposed |

### FR-005: Future-State Process View

| Field | Value |
|-------|-------|
| ID | FR-005 |
| Statement | The application shall display the future-state (to-be) process flow showing improved workflows addressing identified gaps. |
| Business Justification | Demonstrates ability to design process improvements. |
| Priority | High |
| Linked BR | BR-001, BR-002, BR-003 |
| Status | Proposed |

### FR-006: Side-by-Side Process Comparison

| Field | Value |
|-------|-------|
| ID | FR-006 |
| Statement | The application shall support a side-by-side comparison view of current-state and future-state processes. |
| Business Justification | Recruiters need to see how analysis leads to improvement recommendations. |
| Priority | Medium |
| Linked BR | BR-001, BR-002 |
| Status | Proposed |

### FR-007: Business Requirements Table

| Field | Value |
|-------|-------|
| ID | FR-007 |
| Statement | The application shall display a sortable, filterable table of business requirements with IDs, descriptions, priorities, and status. |
| Business Justification | Requirements management is a core BA skill that must be demonstrated. |
| Priority | High |
| Linked BR | BR-001 through BR-015 |
| Status | Proposed |

### FR-008: User Stories Display

| Field | Value |
|-------|-------|
| ID | FR-008 |
| Statement | The application shall display user stories organized by stakeholder role with acceptance criteria references. |
| Business Justification | User stories demonstrate requirement decomposition and stakeholder focus. |
| Priority | High |
| Linked BR | BR-001 through BR-015 |
| Status | Proposed |

### FR-009: Acceptance Criteria View

| Field | Value |
|-------|-------|
| ID | FR-009 |
| Statement | The application shall display acceptance criteria in Given/When/Then format linked to user stories. |
| Business Justification | Acceptance criteria demonstrate requirement specificity and testability. |
| Priority | High |
| Linked BR | BR-001 through BR-015 |
| Status | Proposed |

### FR-010: Risk Register View

| Field | Value |
|-------|-------|
| ID | FR-010 |
| Statement | The application shall display a risk register with risk descriptions, likelihood, impact, scores, and mitigation strategies. |
| Business Justification | Risk management demonstrates proactive analysis and planning. |
| Priority | High |
| Linked BR | BR-009 |
| Status | Proposed |

### FR-011: KPI Dashboard with Filtering

| Field | Value |
|-------|-------|
| ID | FR-011 |
| Statement | The application shall display a KPI dashboard with calculated metrics, target comparisons, trend views, and time-period filtering. |
| Business Justification | KPI definition and visualization demonstrate data-driven analysis. |
| Priority | High |
| Linked BR | BR-008, BR-012 |
| Status | Proposed |

### FR-012: Executive Summary View

| Field | Value |
|-------|-------|
| ID | FR-012 |
| Statement | The application shall provide an executive summary view with key findings, recommendations, and KPI highlights. |
| Business Justification | Executive communication is a critical BA skill that must be demonstrated. |
| Priority | High |
| Linked BR | BR-008 |
| Status | Proposed |

### FR-013: BRD Document Viewer

| Field | Value |
|-------|-------|
| ID | FR-013 |
| Statement | The application shall display the Business Requirements Document in a readable format within the application. |
| Business Justification | The BRD is the central BA deliverable and must be easily accessible. |
| Priority | High |
| Linked BR | BR-001 through BR-015 |
| Status | Proposed |

### FR-014: Export to PDF

| Field | Value |
|-------|-------|
| ID | FR-014 |
| Statement | The application shall support exporting the current view (dashboard, requirements, risk register) as PDF. |
| Business Justification | Recruiters may want to download or print portfolio materials. |
| Priority | Medium |
| Linked BR | BR-012 |
| Status | Proposed |

### FR-015: Export to Markdown

| Field | Value |
|-------|-------|
| ID | FR-015 |
| Statement | The application shall support exporting requirements and risk register content as Markdown files. |
| Business Justification | Markdown export enables sharing in developer-friendly formats. |
| Priority | Medium |
| Linked BR | BR-012 |
| Status | Proposed |

### FR-016: Demo Data Reset

| Field | Value |
|-------|-------|
| ID | FR-016 |
| Statement | The application shall provide a mechanism to reset demo data to its initial state. |
| Business Justification | Recruiters exploring the demo may make changes that need to be reset for the next viewer. |
| Priority | Medium |
| Linked BR | BR-013 |
| Status | Proposed |

### FR-017: Deterministic Demo Mode

| Field | Value |
|-------|-------|
| ID | FR-017 |
| Statement | The application shall operate in a deterministic mode where the same sequence of actions produces the same results every time. |
| Business Justification | Recruiters must have a consistent demonstration experience. |
| Priority | Medium |
| Linked BR | BR-013 |
| Status | Proposed |

### FR-018: No-Login Public Access

| Field | Value |
|-------|-------|
| ID | FR-018 |
| Statement | The application shall load and function completely without any authentication or login requirement. |
| Business Justification | Recruiters must access the demo without barriers or account creation. |
| Priority | High |
| Linked BR | BR-013 |
| Status | Proposed |

---

## Requirements Summary

| Priority | Count | IDs |
|----------|-------|-----|
| High | 12 | FR-001 through FR-005, FR-007 through FR-013, FR-018 |
| Medium | 6 | FR-006, FR-014 through FR-017 |
| Low | 0 | — |
| **Total** | **18** | FR-001 through FR-018 |

---

## Functional Mapping to Business Requirements

| Business Requirement | Functional Requirements |
|--------------------|----------------------|
| BR-001 Shift visibility | FR-001, FR-002, FR-003, FR-004, FR-005, FR-006 |
| BR-002 Gap identification | FR-004, FR-005, FR-006 |
| BR-003 Escalation tracking | FR-005, FR-010 |
| BR-004 Issue follow-up | FR-010 |
| BR-005 Documentation tracking | FR-001, FR-007 |
| BR-006 Centralized view | FR-001 |
| BR-007 Client communication | FR-007 |
| BR-008 KPI dashboard | FR-011, FR-012 |
| BR-009 Policy documentation | FR-010 |
| BR-010 Audit trail | FR-007 |
| BR-011 Late arrival tracking | FR-001, FR-011 |
| BR-012 Reporting / export | FR-014, FR-015 |
| BR-013 No-login access | FR-018 |
| BR-014 Synthetic data label | (NFR-012) |
| BR-015 Mobile access | (NFR-003, NFR-004) |

---

## Related Documents

- 10-business-requirements.md — Business requirements
- 12-nonfunctional-requirements.md — Nonfunctional requirements
- 15-requirements-traceability-matrix.md — Traceability
