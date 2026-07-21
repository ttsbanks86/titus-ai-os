# Business Requirements Document (BRD)

**Project:** BA Compass: AI-Assisted Business Process and Requirements Analyzer  
**Company (Fictional):** BrightCare Home Services  
**Document:** 09-business-requirements-document.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  
**Version:** 0.1 (Draft — Phase 1)

---

## Disclaimer

This document describes a **fictional** business scenario and portfolio case study. All company names, data, scenarios, and stakeholders are synthetic. No real client, caregiver, employer, or patient information is used.

---

## 1. Executive Summary

BrightCare Home Services, a fictional home-care provider, is experiencing systemic operational failures that reduce service reliability and limit management visibility. Missed shifts, late arrivals, incomplete documentation, and delayed escalation create a cycle of reactive management and inconsistent client experiences.

BA Compass is a portfolio project that demonstrates how a Business Analyst would approach these problems through structured analysis, stakeholder engagement, requirements management, and data-driven recommendations. The project produces a complete BA documentation suite and a recruiter-facing demonstration application.

This BRD documents the business context, stakeholder needs, requirements, and success measures for the analysis and proposed solution.

---

## 2. Background

BrightCare Home Services manages caregiver-client assignments through informal, decentralized processes. The organization relies on spreadsheets, phone calls, text messages, and paper documentation. As the organization has grown, these informal processes have become insufficient to maintain reliable operations.

The BA Compass project was initiated to:
- Document current operational processes and pain points
- Define structured requirements for an improved operational model
- Create traceable success measures
- Produce a recruiter-ready demonstration of BA skills

---

## 3. Business Problem

The core business problem is that BrightCare Home Services cannot reliably identify, track, or resolve operational service failures. This manifests as:

- Missed shifts and open staffing gaps
- Late caregiver arrivals without tracking or escalation
- Delayed issue resolution due to unclear escalation paths
- Incomplete service documentation creating compliance risk
- Fragmented communication requiring repeated manual follow-up
- No operational visibility or KPI dashboard for management
- Inability to identify recurring failure patterns

---

## 4. Objectives

| ID | Objective | Success Measure |
|----|-----------|----------------|
| OBJ-01 | Document current-state operational processes | Complete process map validated by stakeholders |
| OBJ-02 | Identify root causes of operational failures | Gap analysis with proposed improvements |
| OBJ-03 | Define traceable business requirements | All BRs linked to problems and KPIs |
| OBJ-04 | Create KPI framework for operational measurement | 8+ defined KPIs with formulas |
| OBJ-05 | Design future-state process improvements | To-be process map addressing identified gaps |
| OBJ-06 | Produce professional BA deliverables | Complete 25-document Phase 1 suite |
| OBJ-07 | Build recruiter-facing demonstration | Public web application without login |
| OBJ-08 | Demonstrate requirements traceability | Full RTM linking problem through KPI |

---

## 5. Stakeholders

| ID | Role | Category |
|----|------|----------|
| STK-001 | Agency Owner | Strategic / Decision-maker |
| STK-002 | Operations Manager | Operational / Process Owner |
| STK-003 | Scheduling Coordinator | Tactical / Day-to-Day |
| STK-004 | Care Coordinator | Tactical / Client-Facing |
| STK-005 | Caregiver | Frontline / Field |
| STK-006 | Quality Assurance Lead | Compliance / Quality |
| STK-007 | Client Services Representative | Client-Facing |
| STK-008 | IT Administrator | Technical |
| STK-009 | Compliance Representative | Regulatory |
| STK-010 | Client / Family Representative | Service Recipient |

---

## 6. Scope

### In Scope

- Shift-status visibility analysis
- Staffing-gap identification process
- Missed-shift and late-arrival tracking requirements
- Documentation-completion tracking
- Escalation and follow-up tracking
- KPI reporting and dashboard requirements
- Current-state and future-state workflow documentation
- Requirements management and traceability
- Risk tracking and mitigation
- Responsible AI planning
- Synthetic demo data creation

### Out of Scope

- Payroll, billing, clinical decision-making, EHR, medication management
- Real employee scheduling or real client records
- Production deployment for a real agency
- Legal/regulatory certification
- Real-time GPS tracking
- Authentication or accounts

---

## 7. Current-State Summary

The current operational model at BrightCare Home Services is characterized by:

- **Manual scheduling:** Shift creation, assignment, and confirmation handled via spreadsheets and phone calls
- **Reactive issue detection:** Missed shifts and late arrivals discovered after client impact
- **Informal escalation:** Issues passed through undefined channels with no audit trail
- **No documentation tracking:** Service documentation completion is not monitored
- **Ad-hoc follow-up:** Issue follow-up depends on individual initiative and memory
- **No KPI dashboard:** Management has no real-time operational visibility
- **Fragmented communication:** Information scattered across phone, email, text, and paper

Full details are in 07-current-state-process.md and 08-pain-point-analysis.md.

---

## 8. Future-State Vision

The future state provides:

1. **Centralized visibility** — Single view of shift status, gaps, escalations, and documentation
2. **Proactive alerts** — Early notification of unconfirmed shifts, pending gaps, and approaching deadlines
3. **Structured escalation** — Defined severity levels, escalation paths, and ownership
4. **Documented follow-up** — Assigned ownership, deadlines, and completion tracking
5. **KPI dashboard** — Real-time metrics with trend views and export
6. **Audit trail** — System-generated record of all operational actions
7. **Mobile-responsive access** — Accessible from desktop and mobile devices
8. **Requirements traceability** — Every feature linked to a business problem and success measure

---

## 9. Business Requirements

See 10-business-requirements.md for the complete list of numbered business requirements (BR-001 through BR-015).

| Area | Requirements Count |
|------|-------------------|
| Operational visibility | BR-001 through BR-004 |
| Escalation and follow-up | BR-005 through BR-007 |
| Documentation and compliance | BR-008 through BR-009 |
| Reporting and KPIs | BR-010 through BR-012 |
| Usability and access | BR-013 through BR-015 |

---

## 10. Functional Requirements Summary

See 11-functional-requirements.md for the complete list of numbered functional requirements (FR-001 through FR-018).

| Area | Requirements Count |
|------|-------------------|
| Dashboard and views | FR-001 through FR-006 |
| Process visualization | FR-007 through FR-009 |
| Requirements management | FR-010 through FR-012 |
| Reporting and export | FR-013 through FR-016 |
| Demo and access | FR-017 through FR-018 |

---

## 11. Nonfunctional Requirements Summary

See 12-nonfunctional-requirements.md for the complete list (NFR-001 through NFR-012).

| Area | Requirements Count |
|------|-------------------|
| Accessibility | NFR-001 |
| Performance | NFR-002 |
| Responsiveness | NFR-003, NFR-004 |
| Security and Privacy | NFR-005, NFR-006 |
| Maintainability | NFR-007 |
| Reliability | NFR-008 |
| Compatibility | NFR-009 |
| Usability | NFR-010, NFR-011 |
| Data Labeling | NFR-012 |

---

## 12. Data Requirements

| Requirement | Description |
|-------------|-------------|
| DR-001 | All data must be synthetic, generated for demo purposes |
| DR-002 | No real personally identifiable information (PII) may be stored |
| DR-003 | Data must be clearly labeled as fictional/synthetic |
| DR-004 | Synthetic data must demonstrate realistic operational patterns |
| DR-005 | Data must support deterministic demo mode (same data each time) |
| DR-006 | Demo data must be resetable to initial state |
| DR-007 | KPI calculations must use defined formulas from the KPI dictionary |

---

## 13. Reporting Requirements

| Requirement | Description |
|-------------|-------------|
| RR-001 | KPI dashboard with at least 8 operational metrics |
| RR-002 | Trend views showing metric changes over time |
| RR-003 | Dashboard filterable by time period and metric |
| RR-004 | Export dashboard view as PDF |
| RR-005 | Export requirements table as Markdown |
| RR-006 | Export risk register as Markdown |
| RR-007 | Viewable BRD document within the application |

---

## 14. Security and Privacy Requirements

| Requirement | Description |
|-------------|-------------|
| SPR-001 | No authentication required — public access |
| SPR-002 | No user data collected or stored |
| SPR-003 | No cookies or tracking mechanisms |
| SPR-004 | No API keys hardcoded or required |
| SPR-005 | All data labeled as synthetic/fictional |
| SPR-006 | No external data transmission |
| SPR-007 | Static data only — no user input stored |

---

## 15. Assumptions

- All data is synthetic and fictional
- Recruiters have limited review time (under 10 minutes)
- Demo users will not create accounts
- The application must work without a paid AI API
- The project is a portfolio demonstration, not a production system
- No real employer, client, or patient data will be used
- Low or zero hosting cost is required
- Mobile and desktop support is necessary

---

## 16. Constraints

- No real healthcare, personal, or employer data may be used
- No paid third-party API dependency for core functionality
- Limited development time — solo portfolio project
- Must follow existing workspace repository conventions
- No modification to production Titus Platform services

---

## 17. Dependencies

| Dependency | Description |
|------------|-------------|
| Synthetic data generation | Data must be created before application development |
| Component library | shadcn/ui for consistent UI components |
| Chart library | Recharts for KPI visualizations |
| Deployment platform | Vercel for public hosting |
| Testing framework | Vitest for unit tests, Playwright for e2e |

---

## 18. Risks

Key risks are documented in 16-risk-register.md. Summary:

| Risk Area | Count | Highest Risk |
|-----------|-------|-------------|
| Scope | 2 | Scope growth |
| Quality | 3 | Incorrect KPI calculations |
| Privacy | 2 | Synthetic data appearing real |
| Usability | 2 | Poor recruiter experience |
| Technical | 3 | Deployment failure |

---

## 19. Key Performance Indicators

See 18-kpi-dictionary.md for detailed definitions. All 8 KPIs are defined:

| KPI | Name | Target |
|-----|------|--------|
| KPI-001 | Shift Fill Rate | 95%+ |
| KPI-002 | Missed Shift Rate | < 2% |
| KPI-003 | Late Arrival Rate | < 10% |
| KPI-004 | Average Escalation Time | < 30 min |
| KPI-005 | Documentation Completion Rate | 95%+ |
| KPI-006 | Open Staffing Gaps | < 3 |
| KPI-007 | Issue Resolution Time | < 4 hours |
| KPI-008 | Follow-Up Completion Rate | 90%+ |

---

## 20. Acceptance Approach

| Level | Method | Owner |
|-------|--------|-------|
| Unit testing | Vitest automated tests | Developer |
| Functional testing | Manual walkthrough of user stories | Business Analyst |
| Accessibility testing | Axe DevTools / manual checklist | Developer |
| Mobile responsiveness | Viewport testing (375px to 1920px) | Developer |
| Recruiter walkthrough | Structured demo script | Business Analyst |
| Stakeholder review | Document review against charter | Agency Owner |

---

## 21. Approval

| Role | Name | Approval Status |
|------|------|----------------|
| Business Analyst | Titus Banks | Draft |
| Operations Manager | [Fictional] | Pending |
| Agency Owner | [Fictional] | Pending |

---

## Related Documents

- 01-project-charter.md — Project overview
- 10-business-requirements.md — Numbered business requirements
- 11-functional-requirements.md — Functional requirements
- 12-nonfunctional-requirements.md — Nonfunctional requirements
- 15-requirements-traceability-matrix.md — Traceability
