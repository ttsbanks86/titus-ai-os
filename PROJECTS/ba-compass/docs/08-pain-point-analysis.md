# Pain-Point and Gap Analysis

**Company:** BrightCare Home Services (Fictional)  
**Document:** 08-pain-point-analysis.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Analysis Framework

Each pain point is analyzed across nine dimensions:

1. Current problem
2. Root cause
3. Business impact
4. Affected stakeholders
5. Frequency
6. Severity (1-5)
7. Current workaround
8. Proposed improvement
9. Linked requirement

---

## 1. People Pain Points

### PP-PEOPLE-01: Scheduling Coordinator Overload

| Element | Description |
|---------|-------------|
| Current problem | Scheduling coordinators spend excessive time on manual phone calls to fill gaps |
| Root cause | No centralized visibility into caregiver availability |
| Impact | High coordinator turnover risk, missed shifts due to coordinator capacity |
| Affected stakeholders | STK-003 Scheduling Coordinator, STK-002 Operations Manager |
| Frequency | Daily |
| Severity | 4 / 5 |
| Current workaround | Overtime hours, prioritizing calls by urgency |
| Proposed improvement | Centralized availability view and gap-alert system |
| Linked requirement | BR-001, FR-001 |

### PP-PEOPLE-02: Caregiver Communication Overload

| Element | Description |
|---------|-------------|
| Current problem | Caregivers receive schedule updates through multiple inconsistent channels |
| Root cause | No single communication method for schedule changes |
| Impact | Missed shifts, confusion, frustration |
| Affected stakeholders | STK-005 Caregiver, STK-003 Scheduling Coordinator |
| Frequency | Daily |
| Severity | 3 / 5 |
| Current workaround | Caregivers check multiple channels, call office to confirm |
| Proposed improvement | Unified schedule notification system |
| Linked requirement | BR-005, FR-002 |

### PP-PEOPLE-03: Client Services Frustration

| Element | Description |
|---------|-------------|
| Current problem | Client services representatives cannot give clients accurate real-time information |
| Root cause | No centralized operational status view |
| Impact | Client frustration, repeated callbacks, damaged relationships |
| Affected stakeholders | STK-007 Client Services Rep, STK-010 Client/Family Rep |
| Frequency | Daily |
| Severity | 3 / 5 |
| Current workaround | Calling coordinators directly for status |
| Proposed improvement | Operational status view accessible to client services |
| Linked requirement | BR-007, FR-003 |

---

## 2. Process Pain Points

### PP-PROC-01: No Shift Confirmation Process

| Element | Description |
|---------|-------------|
| Current problem | Shifts are assigned but not systematically confirmed before start time |
| Root cause | No defined confirmation step in the scheduling workflow |
| Impact | Missed shifts discovered after client impact |
| Affected stakeholders | STK-002 Ops Manager, STK-004 Care Coordinator, STK-010 Client |
| Frequency | Daily |
| Severity | 5 / 5 |
| Current workaround | Manual check-in calls by coordinators |
| Proposed improvement | Pre-shift confirmation workflow with alerts for unconfirmed shifts |
| Linked requirement | BR-001, BR-002, FR-004 |

### PP-PROC-02: No Standard Escalation Path

| Element | Description |
|---------|-------------|
| Current problem | Issues are escalated through informal channels with no documented process |
| Root cause | No escalation policy or severity classification |
| Impact | Delayed resolution, inconsistent handling, no audit trail |
| Affected stakeholders | STK-004 Care Coordinator, STK-002 Ops Manager |
| Frequency | Daily |
| Severity | 4 / 5 |
| Current workaround | Escalate to whoever answers the phone first |
| Proposed improvement | Defined escalation paths with severity levels and ownership |
| Linked requirement | BR-003, FR-005 |

### PP-PROC-03: No Structured Follow-Up

| Element | Description |
|---------|-------------|
| Current problem | Issues are resolved or dropped without systematic follow-up |
| Root cause | No follow-up process or ownership assignment |
| Impact | Recurring issues not identified, client satisfaction drops |
| Affected stakeholders | STK-004 Care Coordinator, STK-010 Client/Family Rep |
| Frequency | Weekly |
| Severity | 3 / 5 |
| Current workaround | Individual staff maintain their own follow-up lists |
| Proposed improvement | Structured follow-up workflow with ownership and deadlines |
| Linked requirement | BR-004, FR-006 |

---

## 3. Technology Pain Points

### PP-TECH-01: No Centralized System

| Element | Description |
|---------|-------------|
| Current problem | Operations managed across spreadsheets, paper, phone, and email |
| Root cause | No investment in operations management software |
| Impact | Data inconsistency, manual rework, lost information |
| Affected stakeholders | All stakeholders |
| Frequency | Constant |
| Severity | 5 / 5 |
| Current workaround | Manual reconciliation across sources |
| Proposed improvement | Centralized web application for operational visibility |
| Linked requirement | BR-006, FR-001 |

### PP-TECH-02: No KPI Dashboard

| Element | Description |
|---------|-------------|
| Current problem | Management has no real-time visibility into operational metrics |
| Root cause | No data collection or reporting infrastructure |
| Impact | Reactive management, no trend identification, no early warning |
| Affected stakeholders | STK-001 Agency Owner, STK-002 Ops Manager |
| Frequency | Constant |
| Severity | 4 / 5 |
| Current workaround | Manual data pulls from spreadsheets for ad-hoc reports |
| Proposed improvement | KPI dashboard with defined metrics and trend views |
| Linked requirement | BR-008, FR-007 |

### PP-TECH-03: No Mobile Access

| Element | Description |
|---------|-------------|
| Current problem | Field staff cannot access schedule information on mobile devices |
| Root cause | No mobile-compatible system |
| Impact | Caregivers call office for basic schedule information |
| Affected stakeholders | STK-005 Caregiver, STK-003 Scheduling Coordinator |
| Frequency | Daily |
| Severity | 3 / 5 |
| Current workaround | Phone calls to office |
| Proposed improvement | Mobile-responsive web application |
| Linked requirement | NFR-003 |

---

## 4. Data Pain Points

### PP-DATA-01: No Attendance Data

| Element | Description |
|---------|-------------|
| Current problem | Caregiver arrival times are not systematically recorded |
| Root cause | No time-tracking or check-in process |
| Impact | Cannot measure lateness, cannot identify chronic late caregivers |
| Affected stakeholders | STK-002 Ops Manager, STK-006 QA Lead |
| Frequency | Per shift |
| Severity | 4 / 5 |
| Current workaround | Word-of-mouth, sporadic reporting |
| Proposed improvement | Arrival time tracking as part of shift documentation |
| Linked requirement | BR-002, FR-008 |

### PP-DATA-02: No Documentation Tracking

| Element | Description |
|---------|-------------|
| Current problem | Service documentation completion is not tracked |
| Root cause | No documentation status process |
| Impact | Compliance risk, billing delays, care continuity gaps |
| Affected stakeholders | STK-006 QA Lead, STK-009 Compliance Rep |
| Frequency | Per shift |
| Severity | 4 / 5 |
| Current workaround | Manual follow-up calls to caregivers |
| Proposed improvement | Documentation status tracking with reminders |
| Linked requirement | BR-005, FR-009 |

---

## 5. Communication Pain Points

### PP-COMM-01: Fragmented Issue Communication

| Element | Description |
|---------|-------------|
| Current problem | Issue details are communicated through phone and email with no central record |
| Root cause | No issue-tracking system |
| Impact | Information lost, clients repeat explanations, delayed resolution |
| Affected stakeholders | STK-004 Care Coordinator, STK-007 Client Services Rep, STK-010 Client |
| Frequency | Daily |
| Severity | 4 / 5 |
| Current workaround | Follow-up emails summarizing phone conversations |
| Proposed improvement | Centralized issue tracking with timeline and status |
| Linked requirement | BR-003, FR-005 |

### PP-COMM-02: No Client Notification Confirmation

| Element | Description |
|---------|-------------|
| Current problem | No confirmation that clients received schedule change notifications |
| Root cause | No notification tracking process |
| Impact | Clients not informed of changes, missed shifts, dissatisfaction |
| Affected stakeholders | STK-010 Client/Family Rep, STK-007 Client Services Rep |
| Frequency | Weekly |
| Severity | 3 / 5 |
| Current workaround | Call twice if no answer, leave voicemail |
| Proposed improvement | Notification delivery tracking |
| Linked requirement | BR-007, FR-003 |

---

## 6. Governance Pain Points

### PP-GOV-01: No Defined Operational Policies

| Element | Description |
|---------|-------------|
| Current problem | No documented policies for gap-filling, escalation, or documentation deadlines |
| Root cause | Informal management culture, no policy development |
| Impact | Inconsistent decisions, staff confusion, compliance risk |
| Affected stakeholders | STK-002 Ops Manager, STK-006 QA Lead, STK-009 Compliance Rep |
| Frequency | Ongoing |
| Severity | 4 / 5 |
| Current workaround | Decisions made case-by-case |
| Proposed improvement | Documented operational policies and procedures |
| Linked requirement | BR-009, FR-010 |

### PP-GOV-02: No Audit Trail

| Element | Description |
|---------|-------------|
| Current problem | Operational decisions and issue resolutions leave no audit trail |
| Root cause | Informal communication channels, no documentation |
| Impact | Cannot reconstruct events, compliance exposure, liability risk |
| Affected stakeholders | STK-009 Compliance Rep, STK-001 Agency Owner |
| Frequency | Ongoing |
| Severity | 4 / 5 |
| Current workaround | Saving emails and text messages |
| Proposed improvement | System-generated audit trail for all operational actions |
| Linked requirement | BR-010, FR-011 |

---

## 7. Reporting Pain Points

### PP-REPORT-01: No Operational Dashboard

| Element | Description |
|---------|-------------|
| Current problem | No real-time operational metrics or dashboard |
| Root cause | No data collection or reporting infrastructure |
| Impact | Management flies blind, cannot identify trends |
| Affected stakeholders | STK-001 Agency Owner, STK-002 Ops Manager |
| Frequency | Ongoing |
| Severity | 5 / 5 |
| Current workaround | Ad-hoc reports from manual data pulls |
| Proposed improvement | KPI dashboard with trend views and export |
| Linked requirement | BR-008, FR-007, KPI-001 through KPI-008 |

### PP-REPORT-02: No Historical Trend Data

| Element | Description |
|---------|-------------|
| Current problem | Cannot compare month-over-month or week-over-week performance |
| Root cause | Data is not collected in a structured format over time |
| Impact | Cannot measure improvement or identify seasonal patterns |
| Affected stakeholders | STK-001 Agency Owner, STK-002 Ops Manager |
| Frequency | Ongoing |
| Severity | 3 / 5 |
| Current workaround | None |
| Proposed improvement | Data persistence with time-series KPI tracking |
| Linked requirement | BR-008, FR-007 |

---

## 8. Risk Pain Points

### PP-RISK-01: Compliance Exposure

| Element | Description |
|---------|-------------|
| Current problem | Cannot demonstrate consistent documentation or process adherence |
| Root cause | No documentation tracking or audit trail |
| Impact | Regulatory findings, billing audits, legal exposure |
| Affected stakeholders | STK-009 Compliance Rep, STK-001 Agency Owner |
| Frequency | Ongoing |
| Severity | 5 / 5 |
| Current workaround | Reactive documentation when audit is expected |
| Proposed improvement | Continuous documentation tracking with compliance reporting |
| Linked requirement | BR-010, FR-011 |

### PP-RISK-02: Client Churn Risk

| Element | Description |
|---------|-------------|
| Current problem | Service failures without structured recovery reduce client retention |
| Root cause | No systematic service recovery process |
| Impact | Revenue loss, reputation damage |
| Affected stakeholders | STK-001 Agency Owner, STK-010 Client/Family Rep |
| Frequency | Monthly |
| Severity | 4 / 5 |
| Current workaround | Apologize, offer discounts |
| Proposed improvement | Structured service recovery and follow-up process |
| Linked requirement | BR-004, FR-006 |

---

## 9. Client Experience Pain Points

### PP-CLIENT-01: Inconsistent Care

| Element | Description |
|---------|-------------|
| Current problem | Clients experience missed shifts, late arrivals, and different caregivers |
| Root cause | Inadequate scheduling and gap-filling processes |
| Impact | Dissatisfaction, churn, negative word-of-mouth |
| Affected stakeholders | STK-010 Client/Family Rep, STK-001 Agency Owner |
| Frequency | Weekly |
| Severity | 5 / 5 |
| Current workaround | Assign preferred caregivers when available |
| Proposed improvement | Reliability metrics, consistency tracking |
| Linked requirement | BR-001, BR-002 |

### PP-CLIENT-02: Poor Issue Communication

| Element | Description |
|---------|-------------|
| Current problem | Clients are not proactively notified about schedule changes |
| Root cause | No client notification process |
| Impact | Frustration, distrust, churn |
| Affected stakeholders | STK-010 Client/Family Rep, STK-007 Client Services Rep |
| Frequency | Weekly |
| Severity | 3 / 5 |
| Current workaround | Clients call office to check |
| Proposed improvement | Proactive notification system |
| Linked requirement | BR-007, FR-003 |

---

## Gap Summary Table

| Gap Area | Current State | Target State | Gap Severity |
|----------|--------------|--------------|-------------|
| Shift visibility | Manual spreadsheets | Real-time dashboard | Critical |
| Gap identification | Reactive | Proactive alerts | Critical |
| Escalation | Informal | Structured with severity | High |
| Documentation tracking | None | Status dashboard | High |
| Issue follow-up | Ad-hoc | Assigned ownership | High |
| KPI reporting | None | Defined metrics | Critical |
| Audit trail | None | System logs | High |
| Data collection | None | Structured data | Critical |
| Mobile access | None | Responsive web | Medium |
| Client notifications | Phone calls | Structured | Medium |

---

## Related Documents

- 07-current-state-process.md — Detailed current workflow
- 09-business-requirements-document.md — BRD with gap analysis
- 10-business-requirements.md — Numbered requirements
