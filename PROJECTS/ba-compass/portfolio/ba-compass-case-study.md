# BA Compass: End-to-End Business Analysis for BrightCare Home Services

**A structured case study in operational remediation through the full BA lifecycle**

**Author:** Titus Banks — Business Analyst  
**Date:** July 2026  
**Demo:** [ba-compass.vercel.app](https://ba-compass.vercel.app)  
**Repository:** [github.com/titus-banks/ba-compass](https://github.com/titus-banks/ba-compass)

> **Fictional-Case Disclosure:** This case study is based on BrightCare Home Services, a fictional home-care company created for portfolio demonstration purposes. All company data, stakeholder profiles, operational metrics, and scenario details are synthetic. No real client, caregiver, employer, or patient information is represented. The purpose is to demonstrate Business Analyst skills, methodology, and deliverables.

---

## 1. Executive Summary

BrightCare Home Services, a mid-sized home-care provider operating across three regions, was experiencing systemic operational failures that threatened service quality and business viability. Missed shifts averaged 18 per week, caregiver late arrivals affected 32% of all visits, and incomplete service documentation left the company exposed to compliance and billing risks. Management operated without a centralized view of operations, relying on spreadsheets, phone calls, and institutional memory to manage day-to-day service delivery.

This case study documents the complete Business Analyst engagement: from discovery and stakeholder analysis through requirements definition, KPI design, risk assessment, and future-state recommendations. The engagement produced 45 requirements (15 business, 18 functional, 12 nonfunctional), 8 operational KPIs with traceable formulas, 15 identified risks with mitigation strategies, and 11 prioritized recommendations across immediate, near-term, and future horizons.

The BA Compass web application serves as both a demonstration of the analytical process and an interactive tool for exploring the findings. Built with Next.js 15, TypeScript, and Recharts, the application presents the full BA documentation suite in a recruiter-friendly format with a guided tour, live KPI dashboard, and exportable deliverables.

---

## 2. Business Challenge

BrightCare Home Services provides non-medical in-home care to elderly and disabled clients. The company employs approximately 40 caregivers serving 150 clients across three service regions. Operations were managed through a combination of phone calls, text messages, and spreadsheets stored on a shared network drive.

The operational failures were well-known to staff but poorly understood in aggregate:

- **Missed shifts** averaged 18 per week, requiring last-minute caregiver reassignment or client rescheduling
- **Late arrivals** affected nearly one in three visits, with clients reporting dissatisfaction
- **Documentation gaps** meant 22% of completed visits lacked required service notes within 24 hours
- **Escalation delays** left unresolved issues stretching days or weeks
- **Communication breakdowns** forced coordinators to make an average of 3.4 follow-up attempts per scheduling issue
- **No operational dashboard** existed — management relied on ad-hoc reports compiled manually

The absence of structured data collection and analysis meant that the company could not identify root causes, measure the impact of changes, or communicate operational status to stakeholders with confidence. The organization was caught in a cycle of reactive firefighting with no clear path to improvement.

---

## 3. BA Approach: The Full Lifecycle

The engagement followed a structured six-phase BA lifecycle. Each phase produced specific deliverables that fed into the next.

### Discover
**Goal:** Understand the business context, stakeholders, and problem space.  
**Activities:** Stakeholder identification, project chartering, scope definition.  
**Deliverables:** Project Charter, Business Problem Statement, Stakeholder Register.

### Analyze
**Goal:** Document current operations and identify root causes.  
**Activities:** Process mapping, pain-point analysis, gap identification.  
**Deliverables:** Current-State Process Map, Pain-Point Analysis, Gap Analysis (21 pain points across 9 dimensions).

### Define
**Goal:** Specify what the solution must accomplish.  
**Activities:** Requirements elicitation, prioritization, user story creation.  
**Deliverables:** Business Requirements Document, 45 Requirements (BR/FR/NFR), 26 User Stories, Acceptance Criteria.

### Design
**Goal:** Design the future-state solution and success metrics.  
**Activities:** Future-state process design, KPI definition, architecture planning.  
**Deliverables:** Future-State Process Map, KPI Dictionary (8 KPIs), Architecture Proposal.

### Validate
**Goal:** Ensure requirements are testable, traceable, and complete.  
**Activities:** Traceability matrix construction, risk assessment, audit preparation.  
**Deliverables:** Requirements Traceability Matrix, Risk Register (15 risks), Accessibility Audit.

### Recommend
**Goal:** Deliver actionable, prioritized recommendations.  
**Activities:** Recommendation prioritization, executive summary, milestone planning.  
**Deliverables:** Executive Summary, Recommendations (11 prioritized), Milestone Plan.

The lifecycle was implemented iteratively, with each phase informing the next and earlier phases revisited as new understanding emerged.

---

## 4. Stakeholder Analysis

Ten stakeholder roles were identified across five functional areas. Each was assessed for power, interest, and engagement requirements using a power-interest matrix.

| Stakeholder | Role | Power | Interest | Engagement Strategy |
|---|---|---|---|---|
| Agency Owner | Strategic leader | High | High | Monthly briefings, strategic alignment |
| Operations Manager | Daily operations | High | High | Weekly touchpoints, involved in all phases |
| Scheduling Coordinator | Shift scheduling | Low | High | Direct participation, workflow validation |
| Care Coordinator | Client-caregiver matching | Low | High | Process feedback, pain-point reporting |
| Caregiver | Frontline service delivery | Low | Moderate | Surveys, feedback sessions |
| Quality Assurance Lead | Compliance monitoring | High | High | Review cycles, audit criteria input |
| Client Services Rep | Client communication | Low | Moderate | Issue pattern reporting |
| IT Administrator | System implementation | Moderate | Moderate | Technical requirements, architecture input |
| Compliance Rep | Regulatory requirements | High | High | Regulatory review, approval gates |
| Client/Family Rep | Service recipient | Low | Moderate | Satisfaction feedback, expectation setting |

**Key stakeholder conflicts resolved:**
- Operations vs. Compliance: resolved through shared KPI ownership
- Scheduling vs. Quality: resolved by defining separate but aligned success metrics
- Caregiver workload vs. documentation requirements: resolved by integrating documentation into the workflow rather than adding it after
- Client Services vs. Operations on escalation thresholds: resolved through tiered escalation levels with clear criteria
- IT vs. Operations on implementation timeline: resolved by phasing delivery to match operational capacity

---

## 5. Current-State Findings

The current-state process for shift management was mapped across 11 steps, from client need identification through post-visit documentation. Key breakdowns were identified at nearly every step:

**Process Step: Client Requests Care**
- Breakdown: Intake handled by phone or text with no structured data capture
- Impact: Lost request details, inconsistent information gathering

**Process Step: Coordinator Matches Caregiver**
- Breakdown: Manual matching based on coordinator memory, not systematic criteria
- Impact: Suboptimal matches, inconsistent workload distribution

**Process Step: Schedule Is Confirmed**
- Breakdown: Confirmation sent by individual text messages, no central schedule record
- Impact: No real-time schedule visibility, missed updates

**Process Step: Shift Is Staffed**
- Breakdown: No proactive monitoring of open shifts
- Impact: Shifts went unfilled until the last minute, clients notified late

**Process Step: Caregiver Arrives On Site**
- Breakdown: No arrival confirmation system
- Impact: Late arrivals undetected until client complaint

**Process Step: Care Is Delivered**
- Breakdown: No structured check-in during visit
- Impact: Issues during visits unreported until after the fact

**Process Step: Service Is Documented**
- Breakdown: Paper or unstructured digital notes, no deadline enforcement
- Impact: 22% of visits lacked documentation within 24 hours

**Process Step: Documentation Is Reviewed**
- Breakdown: No systematic review process
- Impact: Missing or incomplete documentation not caught

**Process Step: Issues Are Escalated**
- Breakdown: No defined escalation criteria or tracking
- Impact: Issues lingered unresolved, multiple follow-ups required

**Process Step: Billing Is Processed**
- Breakdown: Billing depended on completed documentation that was often missing
- Impact: Delayed billing, revenue leakage

**Process Step: Performance Is Reviewed**
- Breakdown: No KPI tracking or operational reporting
- Impact: Management blind to trends, unable to measure improvement

**Channel reliability findings** confirmed the communication fragmentation: phone (variable), email (delayed), text messages (unreliable), paper forms (no tracking), and spreadsheets (stale data).

---

## 6. Gap Analysis Summary

21 distinct pain points were identified across 9 operational dimensions. Each was assessed for severity (Critical, Major, Moderate) and assigned to a root cause category.

| Dimension | Pain Points | Severity Distribution |
|---|---|---|
| Visibility | 3 | 2 Critical, 1 Major |
| Scheduling | 3 | 1 Critical, 1 Major, 1 Moderate |
| Communication | 3 | 1 Critical, 2 Major |
| Documentation | 3 | 1 Critical, 1 Major, 1 Moderate |
| Compliance | 2 | 1 Critical, 1 Major |
| Staffing | 2 | 1 Major, 1 Moderate |
| Client Management | 2 | 1 Major, 1 Moderate |
| Performance | 2 | 1 Critical, 1 Major |
| Billing | 1 | 1 Major |

**Total: 21 pain points | 6 Critical, 10 Major, 5 Moderate**

**Critical gaps requiring immediate attention:**
- No centralized operational visibility dashboard
- No proactive shift-status monitoring
- Inconsistent documentation completion
- Missed-shift root cause not tracked
- No escalation tracking or SLA enforcement
- No KPI-based performance measurement

**Root cause analysis** revealed that 62% of pain points stemmed from the absence of structured data capture and the reliance on informal communication channels. An additional 24% were caused by a lack of defined processes and accountability. Only 14% were resource-constrained issues requiring additional staffing.

---

## 7. Requirements Overview

45 requirements were defined across three categories, each with unique identifiers, priorities, and traceability links.

### Business Requirements (15)
High-level statements of what the business needs to achieve. Examples:
- **BR-01:** Centralized operational dashboard serving all user roles
- **BR-02:** Automated shift-status tracking from scheduling through documentation
- **BR-03:** Structured escalation management with defined criteria and SLA enforcement
- **BR-04:** KPI-driven performance reporting with configurable periods
- **BR-05:** Role-based access ensuring data security and appropriate visibility

### Functional Requirements (18)
Specific system capabilities and behaviors. Examples:
- **FR-01:** Dashboard displays real-time counts for scheduled, in-progress, completed, and missed shifts
- **FR-06:** System tracks caregiver arrival time and flags late arrivals automatically
- **FR-10:** Escalation workflow triggers notifications at defined SLA thresholds
- **FR-14:** Searchable requirements repository with type, priority, and status filters
- **FR-17:** Export capabilities for requirements, traceability matrix, and risk register

### Nonfunctional Requirements (12)
Quality attributes and constraints. Examples:
- **NFR-01:** All pages must render in under 2 seconds on standard broadband
- **NFR-04:** Application must be navigable by keyboard alone
- **NFR-07:** All data is explicitly labeled as synthetic and fictional
- **NFR-10:** Application must pass WCAG 2.1 AA accessibility standards
- **NFR-12:** Zero data persistence of user information on the server

**Priority distribution:** 18 High, 15 Medium, 12 Low. Every high-priority requirement is traceable to a specific business problem and stakeholder need.

---

## 8. KPI Framework

8 operational KPIs were defined with explicit formulas, data sources, and target thresholds. Each KPI maps to one or more business requirements and is calculated from the synthetic dataset in the demo application.

| KPI | Formula | Target | Business Requirement |
|---|---|---|---|
| Shift Fulfillment Rate | (Completed Shifts / Scheduled Shifts) x 100 | > 92% | BR-02 |
| On-Time Arrival Rate | (On-Time Arrivals / Total Arrivals) x 100 | > 95% | BR-07 |
| Documentation Completion Rate | (Docs Completed Within 24h / Total Visits) x 100 | > 90% | BR-08 |
| Average Response to Escalation | Sum(Response Times) / Total Escalations | < 30 min | BR-03 |
| Client Satisfaction Score | (Positive Feedback / Total Feedback) x 100 | > 85% | BR-11 |
| Staffing Fill Rate | (Filled Shifts / Open Shifts) x 100 | > 90% | BR-02 |
| Average Shift Duration Variance | Sum(|Actual - Scheduled|) / Total Shifts | < 15 min | BR-07 |
| Documentation Accuracy Rate | (Accurate Docs / Total Docs Reviewed) x 100 | > 95% | BR-08 |

Each KPI is validated through 3-5 unit tests covering normal operation, edge cases (zero values, missing data), and boundary conditions. The demo dashboard renders live-calculated values with period filtering.

---

## 9. Future-State Design

Eight interconnected improvements form the future-state solution, addressing the root causes identified in the gap analysis rather than treating symptoms.

**Improvement 1: Centralized Dashboard** — A role-based operational dashboard replaces spreadsheets and manual reporting. Every user sees information relevant to their role. Links to BR-01, BR-04.

**Improvement 2: Structured Shift Lifecycle** — Every shift moves through defined states: Requested, Scheduled, Confirmed, In Progress, Completed, Documented. Status changes trigger notifications and update dashboard metrics. Links to BR-02.

**Improvement 3: Automated Arrival Confirmation** — Caregivers confirm arrival via a simple mobile-friendly interface. Late arrivals trigger automatic alerts to coordinators. Links to BR-07.

**Improvement 4: Documentation Workflow** — Digital documentation with structured fields, deadline enforcement, and completeness validation before submission. Links to BR-08.

**Improvement 5: Escalation Engine** — Defined escalation criteria, SLA timers, automatic notification routing, and tracking dashboards. Links to BR-03.

**Improvement 6: KPI Reporting Suite** — Automated KPI calculation with configurable periods, trend visualization, and exportable reports. Links to BR-04, BR-09.

**Improvement 7: Communication Hub** — Structured communication threaded by shift, reducing reliance on fragmented phone calls and texts. Links to BR-06.

**Improvement 8: Mobile-First Design** — Caregiver-facing interfaces optimized for mobile use, with offline capability for documentation. Links to NFR-05, NFR-08.

The side-by-side process comparison in the demo application shows how each current-state breakdown is addressed by one or more future-state improvements, with measurable KPI targets for each.

---

## 10. Risk Assessment

15 risks were identified and assessed across four categories: Operational, Technical, Organizational, and External. Each risk was scored on likelihood (1-5) and impact (1-5) to produce a composite risk score and determine mitigation priority.

**Top 5 Risks by Composite Score:**

| Risk ID | Description | Likelihood | Impact | Score | Mitigation |
|---|---|---|---|---|---|
| R-01 | Staff resistance to digital documentation | 4 | 4 | 16 | Phased rollout with caregiver input, training, and visible benefits |
| R-03 | Data quality issues in initial KPI calculations | 3 | 4 | 12 | Data validation rules, parallel running period, manual spot checks |
| R-05 | Escalation SLA causing alert fatigue | 3 | 4 | 12 | Tiered alerting, smart thresholds, quiet hours configuration |
| R-07 | Incomplete adoption of shift-status tracking | 4 | 3 | 12 | Mandatory status updates tied to shift confirmation process |
| R-02 | Dashboard information overload for coordinators | 3 | 3 | 9 | Role-based views, customizable layouts, progressive disclosure |

All 15 risks are documented in the risk register with full descriptions, impact assessments, mitigation strategies, contingency plans, and status tracking.

---

## 11. Recommendations

11 recommendations were developed from the findings and prioritized into three horizons based on business value, implementation complexity, and dependency analysis.

### Immediate (0-3 Months)
1. **Deploy centralized dashboard** to establish operational visibility as the foundation for all other improvements
2. **Implement shift-status tracking** to replace manual status checks and provide real-time operational data
3. **Launch documentation workflow** to address compliance risk and billing delays simultaneously
4. **Establish KPI baseline measurement** to quantify current performance and enable improvement tracking

### Near-Term (3-6 Months)
5. **Implement escalation engine** with defined SLA thresholds and automated notification routing
6. **Deploy automated arrival confirmation** to reduce late-arrival impact and improve client satisfaction
7. **Build client satisfaction feedback loop** to capture real-time service quality data
8. **Develop role-based training program** for all system users

### Future (6-12 Months)
9. **Implement communication hub** integrating shift-related communication in a single thread
10. **Deploy mobile-optimized caregiver interface** with offline documentation capability
11. **Establish continuous improvement process** with quarterly KPI review and process refinement cycles

Each recommendation specifies required resources, success criteria, dependency links to other recommendations, and the business value it delivers.

---

## 12. Traceability Approach

End-to-end traceability was established from business problem through measurable outcome, ensuring every requirement is justified and every KPI is linked to a specific business need.

**Traceability chain:** Business Problem → Stakeholder Need → Business Requirement → Functional Requirement → User Story → Acceptance Criteria → KPI → Test

The traceability matrix in the demo application covers 15 high-priority features with full linkage across the entire chain. Each entry shows how a specific capability addresses a business problem, which stakeholders benefit, which requirement authorizes it, which KPI will measure its success, and which test validates its implementation.

This approach ensures that:
- No requirement exists without a business justification
- Every high-priority feature is testable
- KPI changes can be traced back to specific business outcomes
- Stakeholder concerns are linked to measurable improvements
- Implementation decisions maintain alignment with business goals

---

## 13. Responsible AI Considerations

The BA Compass project includes explicit consideration of ethical and responsible AI principles, reflecting the growing importance of AI governance in business analysis practice.

**AI Usage Transparency:** AI tools were used as productivity accelerators for code generation and content drafting. Every BA artifact was reviewed, validated, and edited by the author. Analytical decisions, methodology choices, and conclusions are the author's own work.

**Responsible AI Checklist applied:**
- All synthetic data is explicitly labeled as fictional
- No real personal information is used in any dataset
- AI-generated content is reviewed for accuracy and bias
- The application includes no surveillance or monitoring capabilities
- Privacy-by-design: zero data persistence on the server
- Accessibility compliance ensures equitable access
- Algorithmic transparency: all KPI formulas are documented and auditable
- User autonomy: no lock-in, no dark patterns, no manipulative design
- Environmental consideration: static generation minimizes compute requirements
- Accountability: all analytical decisions are documented in the decision log

---

## 14. Portfolio Project Outcomes

This case study demonstrates the following BA competencies:

- **Structured methodology:** Full BA lifecycle from discovery through recommendation
- **Stakeholder management:** Comprehensive analysis of 10 stakeholder roles with power-interest mapping and conflict resolution
- **Process analysis:** Current-state and future-state process mapping with gap identification
- **Requirements engineering:** 45 requirements across three categories with prioritization and traceability
- **Analytical thinking:** 21 pain points identified and analyzed across 9 dimensions with root cause analysis
- **Data-driven decision making:** 8 KPIs with documented formulas and traceability to business requirements
- **Risk management:** 15 risks identified with scoring and mitigation strategies
- **Communication:** Executive summary, BRD, and multiple stakeholder-appropriate deliverables
- **Technical literacy:** Full-stack application development demonstrating understanding of modern web architecture
- **Quality assurance:** 76 unit tests and 14 end-to-end tests with structured coverage

---

## 15. Lessons Learned

**What worked well:**
- The six-phase lifecycle provided a clear framework that kept analysis organized and deliverables connected
- Deterministic synthetic data made KPI calculations predictable and testable
- Starting with documentation before code ensured the application had clear requirements to implement
- The traceability matrix forced consistency across all deliverables

**What would be done differently:**
- In a real engagement, stakeholder involvement would be continuous rather than front-loaded, with regular validation checkpoints
- A real implementation would require a pilot phase with a subset of clients before full rollout
- More time would be spent on quantitative analysis of the gap data to establish statistical significance
- User acceptance testing with real users would inform requirement adjustments before finalization

**For real-world application:**
- The same BA lifecycle is transferable to any domain, not just home care
- The documentation framework can serve as a template for future BA engagements
- The traceability approach ensures alignment from business problem through implementation
- The risk framework can be adapted to any project's specific risk profile

---

## 16. Author Contribution

Titus Banks served as the sole Business Analyst for this engagement, performing all analysis work including:

- Stakeholder identification, analysis, and conflict resolution
- Current-state process mapping and pain-point identification
- Gap analysis and root cause investigation
- Requirements elicitation, documentation, and prioritization
- KPI definition, formula validation, and traceability
- Risk identification, assessment, and mitigation planning
- Future-state process and solution design
- Executive communication and recommendation development
- Quality assurance and cross-deliverable consistency review
- Deliverable production and professional presentation

AI tools assisted with code generation for the demonstration application and initial drafting of documentation content. All analytical decisions, methodology choices, validation, and editorial refinement are the author's own work.

---

## 17. Live Demo

**[ba-compass.vercel.app](https://ba-compass.vercel.app)** — No login required. The guided tour at `/tour` provides a step-by-step walkthrough of all 15 pages.

Key pages to explore:
- `/overview` — BA lifecycle and project scope
- `/stakeholders` — Power-interest matrix and stakeholder profiles
- `/current-state` — 11-step process with failure analysis
- `/analysis` — Gap analysis by dimension with severity filtering
- `/dashboard` — Live KPI dashboard with period filtering and charts
- `/future-state` — Side-by-side process comparison
- `/requirements` — 45 requirements with search and filtering
- `/brd` — Complete Business Requirements Document
- `/traceability` — Requirements traceability matrix
- `/risks` — Risk register with heatmap matrix
- `/executive-summary` — Key findings and recommendations

---

## 18. GitHub Repository

**[github.com/titus-banks/ba-compass](https://github.com/titus-banks/ba-compass)**

The repository contains:
- Complete BA documentation suite (40+ files in `/docs`)
- Next.js 15 application source code
- Synthetic dataset generator and data layer
- 76 unit tests (Vitest) across KPI, validation, and content categories
- 14 end-to-end tests (Playwright) covering the full recruiter journey
- GitHub Actions CI pipeline
- Career package materials for job applications

---

## 19. Technical Approach Summary

The BA Compass demonstration application was built to showcase the analytical findings in an accessible, recruiter-friendly format.

**Stack:**
- **Framework:** Next.js 15.5 with App Router and static generation
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS with responsive design
- **Visualization:** Recharts for KPI charts and risk heatmaps
- **Testing:** Vitest (unit) + Playwright (end-to-end)
- **CI/CD:** GitHub Actions for automated testing
- **Deployment:** Vercel with static export

**Key technical decisions:**
- Static generation ensures fast page loads and zero server cost
- Deterministic synthetic data makes all KPI calculations reproducible
- No authentication required — the application is fully public
- Local storage for edit features keeps user data on the user's device
- Mobile-responsive design supports review on any device

---

## 20. Testing Summary

| Test Type | Count | Scope |
|---|---|---|
| Unit tests (KPI functions) | 34 | 8 KPI formulas, 3-5 tests each covering normal, edge, and boundary |
| Unit tests (validation) | 23 | 7 validation rules for requirements editing |
| Unit tests (content) | 19 | Component rendering, data integrity, navigation |
| **Unit tests total** | **76** | All passing |
| End-to-end tests | 14 | Full recruiter journey, page rendering, navigation, interactive features |

**Coverage highlights:**
- KPI calculation correctness under normal conditions
- Edge cases: zero values, missing data, boundary thresholds
- Component rendering with different data states
- Navigation and routing integrity across all 18 pages
- Interactive features: editing, filtering, search, export, print
- Accessibility: keyboard navigation, screen reader compatibility

---

## 21. Synthetic-Data Disclosure

All data used in this case study and the BA Compass demonstration application is synthetic and fictional.

**What is synthetic:**
- BrightCare Home Services as a company
- All caregiver, client, and staff names
- All shift records, schedules, and operational metrics
- All stakeholder profiles and perspectives
- All performance data and KPI calculations
- All risk scenarios and assessments

**What is not synthetic:**
- The BA methodology and analytical framework
- The requirements structure and documentation templates
- The KPI formulas and measurement approaches
- The risk assessment methodology
- The project itself (this is a real portfolio project)

**Why synthetic data was used:**
- To demonstrate BA skills without exposing any real entity's information
- To create a complete, internally consistent scenario for evaluation
- To ensure reproducibility — every KPI calculation produces the same result every time
- To avoid any HIPAA, privacy, or confidentiality concerns
- To allow recruiters and hiring managers to freely review and share the work

No real client, caregiver, employer, or patient information is represented anywhere in this project.
