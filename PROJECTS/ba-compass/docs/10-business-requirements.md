# Business Requirements

**Company:** BrightCare Home Services (Fictional)  
**Document:** 10-business-requirements.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Business Requirements

### BR-001: Shift Status Visibility

| Field | Value |
|-------|-------|
| Requirement ID | BR-001 |
| Statement | The system shall provide visibility into the status of all scheduled shifts, including confirmed, unconfirmed, in-progress, completed, and missed states. |
| Business Justification | Without shift status visibility, the organization cannot proactively identify at-risk shifts before they impact clients. |
| Priority | High |
| Stakeholder Owner | STK-002 Operations Manager |
| Source | PP-PROC-01, PP-TECH-01 |
| Acceptance Measure | All shift statuses visible in a single view, filterable by date and caregiver |
| Related KPI | KPI-001 Shift Fill Rate |
| Status | Proposed |

### BR-002: Gap Identification

| Field | Value |
|-------|-------|
| Requirement ID | BR-002 |
| Statement | The system shall identify and display open staffing gaps where no caregiver is assigned to a scheduled shift. |
| Business Justification | Open gaps must be visible before the shift start time to allow proactive gap-filling. |
| Priority | High |
| Stakeholder Owner | STK-003 Scheduling Coordinator |
| Source | PP-PEOPLE-01, PP-PROC-01 |
| Acceptance Measure | Gaps are flagged with configurable lead time before shift start |
| Related KPI | KPI-006 Open Staffing Gaps |
| Status | Proposed |

### BR-003: Escalation Tracking

| Field | Value |
|-------|-------|
| Requirement ID | BR-003 |
| Statement | The system shall track service issues from identification through resolution, including escalation path, ownership, and status. |
| Business Justification | Without escalation tracking, issues are handled informally with no accountability or audit trail. |
| Priority | High |
| Stakeholder Owner | STK-004 Care Coordinator |
| Source | PP-PROC-02, PP-COMM-01 |
| Acceptance Measure | All issues visible in a timeline with status, owner, and resolution |
| Related KPI | KPI-004 Average Escalation Time |
| Status | Proposed |

### BR-004: Issue Follow-Up

| Field | Value |
|-------|-------|
| Requirement ID | BR-004 |
| Statement | The system shall support structured follow-up on resolved issues, with assigned ownership and completion deadlines. |
| Business Justification | Without structured follow-up, recurring issues go unidentified and client satisfaction declines. |
| Priority | High |
| Stakeholder Owner | STK-004 Care Coordinator |
| Source | PP-PROC-03, PP-RISK-02 |
| Acceptance Measure | Follow-up items tracked with owner, deadline, and completion status |
| Related KPI | KPI-008 Follow-Up Completion Rate |
| Status | Proposed |

### BR-005: Documentation Completion Tracking

| Field | Value |
|-------|-------|
| Requirement ID | BR-005 |
| Statement | The system shall track service documentation completion status per shift and provide visibility into overdue documentation. |
| Business Justification | Incomplete documentation creates compliance risk and billing delays. Tracking ensures accountability. |
| Priority | High |
| Stakeholder Owner | STK-006 Quality Assurance Lead |
| Source | PP-DATA-02, PP-RISK-01 |
| Acceptance Measure | Documentation status visible per shift with completion rate metric |
| Related KPI | KPI-005 Documentation Completion Rate |
| Status | Proposed |

### BR-006: Centralized Operational View

| Field | Value |
|-------|-------|
| Requirement ID | BR-006 |
| Statement | The system shall provide a single view that consolidates shift status, gaps, escalations, and documentation status. |
| Business Justification | Fragmented information across spreadsheets and phone calls prevents effective operational management. |
| Priority | High |
| Stakeholder Owner | STK-002 Operations Manager |
| Source | PP-TECH-01, PP-COMM-01 |
| Acceptance Measure | All operational information accessible from a single dashboard |
| Related KPI | KPI-001 through KPI-008 (overall) |
| Status | Proposed |

### BR-007: Client Communication Tracking

| Field | Value |
|-------|-------|
| Requirement ID | BR-007 |
| Statement | The system shall track client notifications related to schedule changes, cancellations, and service issues. |
| Business Justification | Clients must be informed of changes in a timely manner to maintain trust and satisfaction. |
| Priority | Medium |
| Stakeholder Owner | STK-007 Client Services Representative |
| Source | PP-COMM-02, PP-CLIENT-02 |
| Acceptance Measure | Notification records visible with timestamp, method, and delivery status |
| Related KPI | KPI-001 (indirect) |
| Status | Proposed |

### BR-008: KPI Dashboard

| Field | Value |
|-------|-------|
| Requirement ID | BR-008 |
| Statement | The system shall provide a KPI dashboard displaying defined operational metrics with trend views and configurable time periods. |
| Business Justification | Management cannot make data-driven decisions without visibility into operational performance. |
| Priority | High |
| Stakeholder Owner | STK-001 Agency Owner |
| Source | PP-REPORT-01, PP-REPORT-02 |
| Acceptance Measure | Minimum 8 KPIs displayed with trend data and time period filtering |
| Related KPI | KPI-001 through KPI-008 |
| Status | Proposed |

### BR-009: Operational Policy Documentation

| Field | Value |
|-------|-------|
| Requirement ID | BR-009 |
| Statement | The system shall provide access to documented operational policies including gap-filling procedures, escalation paths, and documentation deadlines. |
| Business Justification | Consistent operational decisions require documented policies that all staff can reference. |
| Priority | Medium |
| Stakeholder Owner | STK-009 Compliance Representative |
| Source | PP-GOV-01 |
| Acceptance Measure | Policies visible and searchable within the application |
| Related KPI | KPI-005 (indirect) |
| Status | Proposed |

### BR-010: Audit Trail

| Field | Value |
|-------|-------|
| Requirement ID | BR-010 |
| Statement | The system shall maintain an audit trail of operational actions including shift status changes, escalations, and documentation updates. |
| Business Justification | Audit trail is necessary for compliance, liability protection, and reconstructing events. |
| Priority | Medium |
| Stakeholder Owner | STK-009 Compliance Representative |
| Source | PP-GOV-02, PP-RISK-01 |
| Acceptance Measure | Action history visible with timestamp, user, and change details |
| Related KPI | KPI-005 (indirect) |
| Status | Proposed |

### BR-011: Late Arrival Tracking

| Field | Value |
|-------|-------|
| Requirement ID | BR-011 |
| Statement | The system shall track caregiver arrival times and identify late arrivals based on configurable thresholds. |
| Business Justification | Late arrivals affect client care quality and cannot be managed without tracking. |
| Priority | High |
| Stakeholder Owner | STK-002 Operations Manager |
| Source | PP-DATA-01, PP-CLIENT-01 |
| Acceptance Measure | Arrival times recorded per shift, late arrivals flagged with threshold |
| Related KPI | KPI-003 Late Arrival Rate |
| Status | Proposed |

### BR-012: Reporting and Export

| Field | Value |
|-------|-------|
| Requirement ID | BR-012 |
| Statement | The system shall support export of operational data and reports in common formats (PDF, Markdown). |
| Business Justification | Stakeholders need the ability to share reports with team members and external parties. |
| Priority | Medium |
| Stakeholder Owner | STK-001 Agency Owner |
| Source | PP-REPORT-01 |
| Acceptance Measure | Dashboard, requirements, and risk register exportable |
| Related KPI | KPI-001 through KPI-008 (indirect) |
| Status | Proposed |

### BR-013: No-Login Access

| Field | Value |
|-------|-------|
| Requirement ID | BR-013 |
| Statement | The system shall be publicly accessible without requiring user registration or login. |
| Business Justification | Recruiters evaluating the portfolio must access the demo without barriers. |
| Priority | High |
| Stakeholder Owner | STK-001 Agency Owner |
| Source | Project charter assumption |
| Acceptance Measure | Application loads without any authentication prompt |
| Related KPI | N/A (usability) |
| Status | Proposed |

### BR-014: Synthetic Data Labeling

| Field | Value |
|-------|-------|
| Requirement ID | BR-014 |
| Statement | All data displayed in the system shall be clearly labeled as synthetic/fictional. |
| Business Justification | Prevent confusion with real data and ensure ethical use of the demonstration. |
| Priority | High |
| Stakeholder Owner | STK-009 Compliance Representative |
| Source | Privacy requirement, project charter |
| Acceptance Measure | Visible disclaimer on every page and exported document |
| Related KPI | N/A (privacy) |
| Status | Proposed |

### BR-015: Mobile Access

| Field | Value |
|-------|-------|
| Requirement ID | BR-015 |
| Statement | The system shall be accessible and functional on mobile devices including smartphones and tablets. |
| Business Justification | Recruiters may review the portfolio on mobile devices during commutes or between interviews. |
| Priority | Medium |
| Stakeholder Owner | STK-008 IT Administrator |
| Source | PP-TECH-03 |
| Acceptance Measure | Application functional on viewports from 375px width |
| Related KPI | N/A (usability) |
| Status | Proposed |

---

## Requirements Summary

| Priority | Count | IDs |
|----------|-------|-----|
| High | 9 | BR-001, BR-002, BR-003, BR-004, BR-005, BR-006, BR-008, BR-011, BR-013, BR-014 |
| Medium | 5 | BR-007, BR-009, BR-010, BR-012, BR-015 |
| Low | 0 | — |
| **Total** | **15** | BR-001 through BR-015 |

---

## Requirements Mapping

| Business Problem | BR ID |
|-----------------|-------|
| Missed shifts | BR-001, BR-002 |
| Open staffing gaps | BR-002 |
| Late caregiver arrivals | BR-011 |
| Delayed escalation | BR-003 |
| Incomplete documentation | BR-005 |
| Communication delays | BR-007 |
| Manual follow-up | BR-004 |
| Limited visibility | BR-006, BR-008 |
| No KPI dashboard | BR-008, BR-012 |
| Recruiter access | BR-013, BR-015 |
| Data privacy | BR-014 |

---

## Related Documents

- 09-business-requirements-document.md — Full BRD
- 11-functional-requirements.md — Functional requirements
- 12-nonfunctional-requirements.md — Nonfunctional requirements
- 15-requirements-traceability-matrix.md — Traceability
