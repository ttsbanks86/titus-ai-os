# Stakeholder Analysis

**Company:** BrightCare Home Services (Fictional)  
**Document:** 06-stakeholder-analysis.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Power-Interest Matrix

### High Power, High Interest (Key Players — Manage Closely)

| ID | Stakeholder | Engagement Approach |
|----|-------------|-------------------|
| STK-001 | Agency Owner | Regular executive summaries, milestone reviews, involve in scope decisions |
| STK-002 | Operations Manager | Weekly operational reviews, daily dashboard access, include in process design |
| STK-009 | Compliance Representative | Quarterly compliance updates, involve in requirements review |

These stakeholders have the authority to block or accelerate the project. They need frequent, structured communication and active involvement in key decisions.

### High Power, Low Interest (Keep Satisfied)

| ID | Stakeholder | Engagement Approach |
|----|-------------|-------------------|
| STK-008 | IT Administrator | Technical design reviews, deployment planning, involve on architecture decisions |

This stakeholder has technical authority but may not be interested in daily project details. Keep informed of major decisions and involve when technical input is needed.

### Low Power, High Interest (Keep Informed)

| ID | Stakeholder | Engagement Approach |
|----|-------------|-------------------|
| STK-003 | Scheduling Coordinator | Daily updates, involve in requirements validation, gather firsthand feedback |
| STK-004 | Care Coordinator | Daily issue tracking, involve in escalation design, regular feedback loops |
| STK-006 | Quality Assurance Lead | Monthly quality reviews, involve in documentation requirements |

These stakeholders have deep operational knowledge. Keep them informed and involve them in requirement validation and process design.

### Low Power, Low Interest (Monitor)

| ID | Stakeholder | Engagement Approach |
|----|-------------|-------------------|
| STK-005 | Caregiver | Communicate changes through existing channels, gather periodic feedback |
| STK-007 | Client Services Rep | Issue tracking updates, involve in escalation process design |
| STK-010 | Client/Family Rep | Communicate through client services, satisfaction surveys |

These stakeholders need minimal active engagement but should not be neglected. Keep communication clear and gather feedback periodically.

---

## Engagement Approach by Phase

### Phase 1: Documentation Foundation

| Stakeholder | Engagement |
|-------------|-----------|
| Agency Owner | Review charter and scope, approve Phase 1 completion |
| Operations Manager | Validate current-state process, provide operational context |
| Scheduling Coordinator | Provide scheduling process details, validate pain points |
| Care Coordinator | Provide escalation context, validate issue tracking needs |
| QA Lead | Validate documentation requirements |
| Compliance Rep | Review privacy and compliance requirements |
| IT Admin | Review architecture constraints |
| Others | Inform of project initiation |

### Phase 2-3: Application Foundation and MVP

| Stakeholder | Engagement |
|-------------|-----------|
| Operations Manager | Review prototype, validate KPI display |
| Scheduling Coordinator | Test scheduling views, provide feedback |
| IT Admin | Review technical approach, deployment plan |
| Others | Prototype demonstrations, feedback sessions |

### Phase 4-6: Interactive Features and Deployment

| Stakeholder | Engagement |
|-------------|-----------|
| Agency Owner | Final review, approval |
| Operations Manager | User acceptance testing |
| QA Lead | Validate quality metrics |
| All | Training, go-live communication |

---

## Communication Plan

| Audience | Channel | Frequency | Content |
|----------|---------|-----------|---------|
| Executive (Agency Owner) | Executive summary | Monthly | Progress, KPIs, risks, decisions needed |
| Operational (Ops Manager, Coordinators) | Dashboard + meetings | Weekly | Metrics, issues, upcoming changes |
| Technical (IT Admin) | Technical reviews | Per milestone | Architecture, deployment, support |
| Compliance (Compliance Rep, QA Lead) | Compliance reports | Quarterly | Audit readiness, documentation status |
| All stakeholders | Status update | Per phase | Milestone completion, next steps |
| End users (Caregivers, CS Reps) | Notifications, training | As needed | Process changes, system updates |

---

## Stakeholder Conflicts and Resolution

### Potential Conflicts

| Conflicting Parties | Issue | Resolution Approach |
|--------------------|-------|-------------------|
| Operations Manager vs. Compliance Rep | Process speed vs. documentation rigor | Design workflow stages that capture documentation without blocking operations |
| Scheduling Coordinators vs. Caregivers | Fill-gap pressure vs. schedule flexibility | Define clear gap-fill procedures with caregiver preference options |
| Agency Owner vs. IT Admin | Feature scope vs. technical simplicity | Prioritize must-have features, document future enhancements |
| Quality Assurance vs. Scheduling | Documentation completion vs. quick assignments | Define acceptable documentation windows, not real-time requirements |
| Client Services vs. Operations | Client requests vs. operational capacity | Establish structured escalation with clear response SLAs |

### Conflict Resolution Process

1. Identify the specific conflict and stakeholders involved
2. Document both perspectives with supporting rationale
3. Evaluate impact on project objectives, scope, and timeline
4. Facilitate a structured discussion between conflicting parties
5. Seek compromise that meets core needs of both parties
6. If no consensus, escalate to Agency Owner for decision
7. Document the decision and rationale in the decision log

---

## Stakeholder Priorities by Requirement Area

| Requirement Area | Primary Stakeholder | Secondary Stakeholder |
|-----------------|--------------------|---------------------|
| Shift scheduling | STK-003 Scheduling Coordinator | STK-004 Care Coordinator |
| Gap identification | STK-002 Operations Manager | STK-003 Scheduling Coordinator |
| Escalation process | STK-004 Care Coordinator | STK-002 Operations Manager |
| Documentation tracking | STK-006 QA Lead | STK-009 Compliance Rep |
| KPI dashboard | STK-001 Agency Owner | STK-002 Operations Manager |
| Client communication | STK-007 Client Services Rep | STK-010 Client Rep |
| Risk tracking | STK-001 Agency Owner | STK-009 Compliance Rep |
| Reporting | STK-002 Operations Manager | STK-001 Agency Owner |

---

## Requirement Ownership

| Requirement Type | Primary Owner | Approver |
|-----------------|--------------|----------|
| Business requirements | Operations Manager | Agency Owner |
| Functional requirements | IT Administrator | Operations Manager |
| Nonfunctional requirements | IT Administrator | Agency Owner |
| User stories | Business Analyst | Operations Manager |
| Acceptance criteria | Business Analyst | QA Lead |
| KPIs | Business Analyst | Agency Owner |
| Risk register | Business Analyst | Operations Manager |

---

## Approval Responsibilities

| Decision | Approver | Consultation |
|----------|----------|-------------|
| Project charter | Agency Owner | Operations Manager |
| Scope changes | Agency Owner | All affected stakeholders |
| Requirements sign-off | Operations Manager | QA Lead, Compliance Rep |
| Architecture decisions | IT Administrator | Agency Owner |
| Deployment approval | Agency Owner | Operations Manager, IT Admin |
| Phase completion | Agency Owner | Operations Manager |

---

## Related Documents

- 05-stakeholder-register.md — Detailed stakeholder profiles
- 09-business-requirements-document.md — BRD with stakeholder context
