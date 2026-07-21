# Requirements Traceability Matrix (RTM)

**Company:** BrightCare Home Services (Fictional)  
**Document:** 15-requirements-traceability-matrix.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## RTM Structure

| Business Problem | Stakeholder Need | BR | FR | User Story | AC | KPI | Planned Feature | Test Method | Status |
|-----------------|-----------------|-----|-----|-----------|-----|-----|----------------|-------------|--------|

---

## RTM — High Priority Items

### Traceability Line 1: Shift Status Visibility

| Element | Reference |
|---------|-----------|
| Business Problem | Missed shifts discovered reactively |
| Stakeholder Need | STK-002: Real-time shift status |
| BR | BR-001 — Shift Status Visibility |
| FR | FR-001 — Operational Dashboard |
| User Story | US-013 — Shift status at a glance |
| AC | AC-012 — Shift status view |
| KPI | KPI-001 — Shift Fill Rate |
| Planned Feature | Dashboard with shift status summary |
| Test Method | Verify shift counts match synthetic data |
| Status | Planned |

### Traceability Line 2: Gap Identification

| Element | Reference |
|---------|-----------|
| Business Problem | Open staffing gaps invisible until client impact |
| Stakeholder Need | STK-003: Visibility into unfilled shifts |
| BR | BR-002 — Gap Identification |
| FR | FR-004 — Current-State Process View |
| User Story | US-015 — Open gaps highlighted |
| AC | AC-013 — Gap highlighting |
| KPI | KPI-006 — Open Staffing Gaps |
| Planned Feature | Dashboard gap highlight with details |
| Test Method | Verify gap count matches synthetic data |
| Status | Planned |

### Traceability Line 3: Escalation Tracking

| Element | Reference |
|---------|-----------|
| Business Problem | Delayed escalation with no audit trail |
| Stakeholder Need | STK-004: Structured escalation path |
| BR | BR-003 — Escalation Tracking |
| FR | FR-005 — Future-State Process View |
| User Story | US-022 — Escalation response times |
| AC | AC-020 — Escalation time tracking |
| KPI | KPI-004 — Average Escalation Time |
| Planned Feature | Escalation timeline view |
| Test Method | Verify escalation time calculations |
| Status | Planned |

### Traceability Line 4: Issue Follow-Up

| Element | Reference |
|---------|-----------|
| Business Problem | Repeated manual follow-up with no tracking |
| Stakeholder Need | STK-004: Structured follow-up |
| BR | BR-004 — Issue Follow-Up |
| FR | FR-010 — Risk Register View |
| User Story | US-024 — Risk and mitigation visibility |
| AC | AC-011 — Risk register visibility |
| KPI | KPI-008 — Follow-Up Completion Rate |
| Planned Feature | Risk register with follow-up tracking |
| Test Method | Verify follow-up completion calculation |
| Status | Planned |

### Traceability Line 5: Documentation Tracking

| Element | Reference |
|---------|-----------|
| Business Problem | Incomplete service documentation |
| Stakeholder Need | STK-006: Documentation completion visibility |
| BR | BR-005 — Documentation Completion Tracking |
| FR | FR-001 — Operational Dashboard |
| User Story | US-021 — Documentation completion rates |
| AC | AC-019 — Documentation completion rate |
| KPI | KPI-005 — Documentation Completion Rate |
| Planned Feature | Dashboard documentation completion metric |
| Test Method | Verify documentation rate calculation |
| Status | Planned |

### Traceability Line 6: Centralized Operational View

| Element | Reference |
|---------|-----------|
| Business Problem | No single source of truth for operations |
| Stakeholder Need | STK-002: Consolidated operational visibility |
| BR | BR-006 — Centralized Operational View |
| FR | FR-001 — Operational Dashboard |
| User Story | US-013 — Shift status at a glance |
| AC | AC-012 — Shift status view |
| KPI | KPI-001 through KPI-008 (overall) |
| Planned Feature | Consolidated dashboard with all metrics |
| Test Method | Verify all data sources consolidated |
| Status | Planned |

### Traceability Line 7: Client Communication

| Element | Reference |
|---------|-----------|
| Business Problem | Clients not notified of schedule changes |
| Stakeholder Need | STK-007: Client notification tracking |
| BR | BR-007 — Client Communication Tracking |
| FR | FR-007 — Business Requirements Table |
| User Story | US-002 — Clear business scenario |
| AC | AC-002 — Scenario launch |
| KPI | KPI-001 (indirect) |
| Planned Feature | Requirements table with communication requirements |
| Test Method | Verify requirements display |
| Status | Planned |

### Traceability Line 8: KPI Dashboard

| Element | Reference |
|---------|-----------|
| Business Problem | No operational KPI dashboard |
| Stakeholder Need | STK-001: Operational performance visibility |
| BR | BR-008 — KPI Dashboard |
| FR | FR-011 — KPI Dashboard with Filtering |
| User Story | US-006 — KPI definitions and metrics |
| AC | AC-006 — KPI calculations |
| KPI | KPI-001 through KPI-008 |
| Planned Feature | KPI dashboard with trend views |
| Test Method | Verify each KPI calculation against formula |
| Status | Planned |

### Traceability Line 9: Late Arrival Tracking

| Element | Reference |
|---------|-----------|
| Business Problem | Late caregiver arrivals not tracked |
| Stakeholder Need | STK-002: Arrival time tracking |
| BR | BR-011 — Late Arrival Tracking |
| FR | FR-001 — Operational Dashboard |
| User Story | US-017 — Late arrivals flagged |
| AC | AC-015 — Late arrival flagging |
| KPI | KPI-003 — Late Arrival Rate |
| Planned Feature | Dashboard late arrival rate metric |
| Test Method | Verify late arrival calculation |
| Status | Planned |

### Traceability Line 10: No-Login Access

| Element | Reference |
|---------|-----------|
| Business Problem | Recruiters need barrier-free access |
| Stakeholder Need | STK-001: Public demo access |
| BR | BR-013 — No-Login Access |
| FR | FR-018 — No-Login Public Access |
| User Story | US-001 — Access without account |
| AC | AC-001 — Public access without login |
| KPI | N/A (usability) |
| Planned Feature | Public application without auth |
| Test Method | Verify no auth prompt appears |
| Status | Planned |

### Traceability Line 11: Synthetic Data Labeling

| Element | Reference |
|---------|-----------|
| Business Problem | Need to distinguish synthetic from real |
| Stakeholder Need | STK-009: Clear data identification |
| BR | BR-014 — Synthetic Data Labeling |
| FR | NFR-012 — Synthetic Data Labeling |
| User Story | US-002 — Clear scenario context |
| AC | AC-023 — Private data verification |
| KPI | N/A (privacy) |
| Planned Feature | Disclaimer on every page |
| Test Method | Visual inspection of all views |
| Status | Planned |

### Traceability Line 12: Mobile Access

| Element | Reference |
|---------|-----------|
| Business Problem | Mobile accessibility for recruiters |
| Stakeholder Need | STK-008: Mobile-responsive demo |
| BR | BR-015 — Mobile Access |
| FR | NFR-003 — Mobile Responsiveness |
| User Story | US-008 — Demo on phone |
| AC | AC-008 — Mobile display |
| KPI | N/A (usability) |
| Planned Feature | Responsive design for all viewports |
| Test Method | Viewport testing at 375px, 768px, 1920px |
| Status | Planned |

### Traceability Line 13: Executive Summary

| Element | Reference |
|---------|-----------|
| Business Problem | Management needs concise operational overview |
| Stakeholder Need | STK-001: Executive-level communication |
| BR | BR-008 — KPI Dashboard |
| FR | FR-012 — Executive Summary View |
| User Story | US-023 — Executive summary |
| AC | AC-018 — Executive summary access |
| KPI | KPI-001 through KPI-008 |
| Planned Feature | Executive summary with findings and KPIs |
| Test Method | Verify summary renders with correct data |
| Status | Planned |

### Traceability Line 14: Risk Register

| Element | Reference |
|---------|-----------|
| Business Problem | No structured risk identification |
| Stakeholder Need | STK-001: Risk awareness |
| BR | BR-009 — Operational Policy Documentation |
| FR | FR-010 — Risk Register View |
| User Story | US-011 — Risk register with mitigations |
| AC | AC-011 — Risk register visibility |
| KPI | N/A (risk management) |
| Planned Feature | Risk register with scores and mitigations |
| Test Method | Verify risk register displays all 12+ risks |
| Status | Planned |

### Traceability Line 15: BRD Access

| Element | Reference |
|---------|-----------|
| Business Problem | Need centralized requirements document |
| Stakeholder Need | STK-001: Complete requirements view |
| BR | BR-001 through BR-015 |
| FR | FR-013 — BRD Document Viewer |
| User Story | US-007 — Professional BRD |
| AC | AC-007 — BRD accessibility |
| KPI | N/A (documentation) |
| Planned Feature | BRD view within application |
| Test Method | Verify BRD renders with all sections |
| Status | Planned |

---

## Coverage Summary

| Element | Total | High-Priority | Traceable to RTM |
|---------|-------|---------------|-----------------|
| Business Problems | 10 | 10 | 10 (100%) |
| Stakeholders | 10 | 6 | 6 (100%) |
| Business Requirements | 15 | 10 | 10 (100%) |
| Functional Requirements | 18 | 12 | 12 (100%) |
| User Stories | 26 | 22 | 15 (68% — top priority) |
| Acceptance Criteria | 24 | 19 | 15 (79% — top priority) |
| KPIs | 8 | 8 | 8 (100%) |
| Risks | 15 | 12 | Documented in risk register |

---

## Verification Status

| Traceability Line | Business Problem | Stakeholder Need | BR | FR | User Story | AC | KPI | Feature | Test |
|-----------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 Shift visibility | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2 Gap identification | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 3 Escalation tracking | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 4 Issue follow-up | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 5 Documentation tracking | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 6 Centralized view | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 7 Client communication | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 8 KPI dashboard | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 9 Late arrival tracking | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 10 No-login access | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ |
| 11 Synthetic data labeling | ✓ | ✓ | ✓ | NFR | ✓ | ✓ | N/A | ✓ | ✓ |
| 12 Mobile access | ✓ | ✓ | ✓ | NFR | ✓ | ✓ | N/A | ✓ | ✓ |
| 13 Executive summary | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 14 Risk register | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ |
| 15 BRD access | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ |

---

## Related Documents

- 10-business-requirements.md — Business requirements
- 11-functional-requirements.md — Functional requirements
- 13-user-stories.md — User stories
- 14-acceptance-criteria.md — Acceptance criteria
- 18-kpi-dictionary.md — KPI definitions
