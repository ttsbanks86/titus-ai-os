# Business Problem Statement

**Company:** BrightCare Home Services (Fictional)  
**Document:** 02-business-problem.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Disclaimer

This document describes a **fictional** business scenario for a portfolio case study. All companies, roles, data, and incidents are synthetic.

---

## Executive Summary

BrightCare Home Services is a fictional home-care provider experiencing systemic operational failures that reduce service reliability, increase administrative burden, and limit management visibility. The organization lacks a structured system for monitoring shift fulfillment, tracking service issues, documenting caregiver performance, and measuring operational health. These gaps create a cycle of reactive management, inconsistent client experiences, and staff inefficiency.

---

## Current Operational Failures

### 1. Missed Shifts

Caregiver shifts are scheduled but frequently go unfilled or are cancelled at the last minute. There is no systematic process for confirming shift coverage before the shift start time. When a shift is missed, the discovery often happens after the shift should have started, leaving clients without care and requiring emergency re-scheduling.

### 2. Open Staffing Gaps

The scheduling process does not provide real-time visibility into unfilled shifts. Open gaps remain invisible until a client or caregiver reports an issue. The organization relies on manual checks and informal communication to identify staffing shortages.

### 3. Late Caregiver Arrivals

Caregiver arrival times are not systematically tracked. Late arrivals are documented inconsistently, if at all. There is no standard threshold for what constitutes late, no escalation trigger for repeated lateness, and no aggregated view of arrival-time patterns across the caregiver population.

### 4. Delayed Escalation

When a service issue occurs — missed shift, late arrival, client complaint — the escalation path is unclear. Issues are passed through informal channels (phone calls, text messages) with no documented process. Response times vary, and there is no audit trail of how or when issues were resolved.

### 5. Incomplete Service Documentation

Caregivers are expected to complete service documentation after each shift. Completion rates vary widely, and there is no systematic tracking of documentation status. Missing documentation creates downstream risks for billing, compliance, and care continuity.

### 6. Communication Delays

Coordination between scheduling, care coordination, and client services happens through fragmented channels — phone, text, email, paper notes. Information is duplicated, lost, or delayed. Follow-up requires repeated manual effort across multiple people and systems.

### 7. Repeated Manual Follow-Up

Without a centralized issue-tracking system, staff spend significant time following up on the same issues across multiple channels. There is no single view of open items, their status, or who is responsible for resolution.

---

## Business Impact

| Area | Impact |
|------|--------|
| Client trust | Missed and late shifts erode confidence |
| Client retention | Service failures increase churn risk |
| Staff morale | Administrative burden and reactive firefighting causes burnout |
| Scheduling efficiency | Manual processes consume coordinator time |
| Management decision-making | No data to identify patterns or root causes |
| Compliance risk | Incomplete documentation creates audit exposure |
| Growth capacity | Current operational model does not scale |

*Note: These impacts are synthetic scenario assumptions used for portfolio demonstration.*

---

## Staff Impact

- Scheduling coordinators spend excessive time on manual gap-filling and phone calls
- Care coordinators lack visibility into real-time shift status
- Client services representatives handle complaints without structured escalation
- Caregivers receive inconsistent communication about schedule changes
- Management cannot distinguish between isolated incidents and systemic problems

---

## Client-Service Impact

- Clients experience inconsistent care due to missed or late shifts
- Communication about schedule changes is unreliable
- Issues require repeated explanation to different staff members
- No systematic follow-up occurs after a service failure
- Clients lack visibility into their care schedule and status

---

## Management Visibility Gap

- No real-time dashboard exists for operational metrics
- Shift fill rates, late arrivals, and documentation completion are not tracked
- Historical trend data is unavailable
- Management relies on anecdotal reports and manual data pulls
- Pattern identification requires digging through emails, phone logs, and paper records

---

## Documentation Gap

- Service documentation completion is not tracked centrally
- No requirements, user stories, or acceptance criteria exist for operational systems
- Process workflows are undocumented
- There is no single source of truth for how operational issues are handled
- KPI definitions are absent or inconsistent

---

## Escalation Gap

- Escalation paths are informal and undocumented
- No defined severity levels for service issues
- Response time expectations are not established
- Escalation history is not recorded
- There is no mechanism to identify recurring issues requiring systemic solutions

---

## Why the Current Process Is Insufficient

The current approach to managing shift operations, service issues, and documentation is fragmented and reactive. BrightCare Home Services relies on:

- Informal communication channels (phone, text, email threads)
- Manual tracking methods (paper notes, spreadsheets, individual memory)
- Decentralized issue handling with no ownership assignment
- No aggregated data for pattern identification
- No standardized escalation or follow-up process

This approach worked when the organization was smaller, but operational complexity has outgrown the informal systems. Without structured processes and visibility tools, the organization cannot reliably identify, address, or prevent service failures.

---

## Why a Structured Solution Is Needed

A structured analysis and solution approach will provide:

1. **Visibility** — Real-time operational metrics and status tracking
2. **Consistency** — Standardized processes for scheduling, escalation, and documentation
3. **Accountability** — Clear ownership for issues and follow-up actions
4. **Efficiency** — Reduced manual coordination and repeated follow-up
5. **Pattern identification** — Data-driven recognition of recurring failures
6. **Scalability** — Processes that support organizational growth
7. **Documentation** — Clear requirements, traceability, and success measures

The BA Compass project demonstrates how a Business Analyst would approach these problems — through structured analysis, stakeholder engagement, requirements management, and data-driven recommendations.

---

## Related Documents

- 01-project-charter.md — Project overview and scope
- 03-business-case.md — Justification for structured solution
- 07-current-state-process.md — Detailed current workflow
- 08-pain-point-analysis.md — Root cause and gap analysis
