# User Stories

**Company:** BrightCare Home Services (Fictional)  
**Document:** 13-user-stories.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## User Story Format

> **As a** [role], **I want** [capability], **so that** [business value].

---

## Stories by Role

### Role: Recruiter (Primary Portfolio Audience)

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-001 | As a recruiter, I want to access the demo without creating an account, so that I can evaluate the portfolio without barriers. | High | BR-013 | AC-001 | Proposed |
| US-002 | As a recruiter, I want to see a clear business scenario explained, so that I understand the context of the analysis. | High | BR-001 | AC-002 | Proposed |
| US-003 | As a recruiter, I want to see stakeholder analysis, so that I can evaluate the BA's stakeholder engagement skills. | High | BR-001 | AC-003 | Proposed |
| US-004 | As a recruiter, I want to see current-state and future-state process maps, so that I can assess process analysis skills. | High | BR-001, BR-002 | AC-004 | Proposed |
| US-005 | As a recruiter, I want to see a complete requirements traceability matrix, so that I can evaluate analytical thoroughness. | High | BR-001 through BR-015 | AC-005 | Proposed |
| US-006 | As a recruiter, I want to see KPI definitions and calculated metrics, so that I can assess data-driven analysis skills. | High | BR-008 | AC-006 | Proposed |
| US-007 | As a recruiter, I want to see a professional BRD, so that I can evaluate documentation quality. | High | BR-001 through BR-015 | AC-007 | Proposed |
| US-008 | As a recruiter, I want the demo to work on my phone, so that I can review it on the go. | Medium | BR-015 | AC-008 | Proposed |
| US-009 | As a recruiter, I want to export content as PDF or Markdown, so that I can save materials for reference. | Medium | BR-012 | AC-009 | Proposed |

### Role: Hiring Manager

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-010 | As a hiring manager, I want to see acceptance criteria in Given/When/Then format, so that I can evaluate requirement specification quality. | High | BR-001 through BR-015 | AC-010 | Proposed |
| US-011 | As a hiring manager, I want to see a risk register with mitigations, so that I can assess risk management skills. | High | BR-009 | AC-011 | Proposed |
| US-012 | As a hiring manager, I want to see traceability from business problem through KPI, so that I can evaluate end-to-end analytical thinking. | High | BR-001 through BR-015 | AC-005 | Proposed |

### Role: Operations Manager (Fictional Stakeholder)

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-013 | As an operations manager, I want to see shift status at a glance, so that I can identify at-risk shifts quickly. | High | BR-001, BR-006 | AC-012 | Proposed |
| US-014 | As an operations manager, I want to see KPI trends over time, so that I can identify improvement or decline patterns. | High | BR-008 | AC-006 | Proposed |
| US-015 | As an operations manager, I want to see open staffing gaps highlighted, so that I can prioritize filling them. | High | BR-002 | AC-013 | Proposed |

### Role: Scheduling Coordinator (Fictional Stakeholder)

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-016 | As a scheduling coordinator, I want to see unconfirmed shifts before they start, so that I can follow up before problems occur. | High | BR-001 | AC-014 | Proposed |
| US-017 | As a scheduling coordinator, I want late arrivals flagged, so that I can address lateness patterns. | High | BR-011 | AC-015 | Proposed |

### Role: Business Analyst (Demonstrating Skills)

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-018 | As a BA, I want to manage requirements with unique IDs and traceability, so that I can demonstrate structured analysis methodology. | High | BR-001 through BR-015 | AC-016 | Proposed |
| US-019 | As a BA, I want each requirement linked to a business problem and KPI, so that I can demonstrate value-driven analysis. | High | BR-001 through BR-015 | AC-017 | Proposed |
| US-020 | As a BA, I want to produce an executive summary with findings and recommendations, so that I can demonstrate executive communication. | High | BR-008 | AC-018 | Proposed |

### Role: Quality Assurance Lead (Fictional Stakeholder)

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-021 | As a QA lead, I want to see documentation completion rates, so that I can identify compliance risks. | High | BR-005 | AC-019 | Proposed |
| US-022 | As a QA lead, I want to see escalation response times, so that I can evaluate service reliability. | Medium | BR-003 | AC-020 | Proposed |

### Role: Executive Stakeholder / Agency Owner (Fictional)

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-023 | As an agency owner, I want an executive summary of key findings and recommendations, so that I can make informed decisions. | High | BR-008 | AC-018 | Proposed |
| US-024 | As an agency owner, I want to see risk assessment and mitigation plans, so that I can understand operational vulnerabilities. | Medium | BR-009 | AC-011 | Proposed |

### Role: IT Administrator

| ID | User Story | Priority | Linked BR | AC Ref | Status |
|----|-----------|----------|-----------|--------|--------|
| US-025 | As an IT administrator, I want the application to work without a backend server, so that deployment is simple and reliable. | High | BR-013, NFR-008 | AC-021 | Proposed |
| US-026 | As an IT administrator, I want no API keys or secrets in the codebase, so that security is not a concern for the demo. | High | NFR-005 | AC-022 | Proposed |

---

## Story Summary

| Role | Count | Story IDs |
|------|-------|-----------|
| Recruiter | 9 | US-001 through US-009 |
| Hiring Manager | 3 | US-010 through US-012 |
| Operations Manager | 3 | US-013 through US-015 |
| Scheduling Coordinator | 2 | US-016 through US-017 |
| Business Analyst | 3 | US-018 through US-020 |
| Quality Assurance Lead | 2 | US-021 through US-022 |
| Agency Owner | 2 | US-023 through US-024 |
| IT Administrator | 2 | US-025 through US-026 |
| **Total** | **26** | US-001 through US-026 |

---

## Priority Distribution

| Priority | Count | Percentage |
|----------|-------|-----------|
| High | 22 | 85% |
| Medium | 4 | 15% |
| Low | 0 | 0% |

---

## Related Documents

- 10-business-requirements.md — Business requirements
- 14-acceptance-criteria.md — Detailed acceptance criteria
- 15-requirements-traceability-matrix.md — Traceability
