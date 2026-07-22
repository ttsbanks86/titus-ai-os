# BA Simulation Practice Guide

**Purpose:** Five manual BA simulations you can practice right now, without any special tools, to build real Business Analyst skills for your portfolio.

**Company Setting:** BrightCare Home Services (fictional home-care agency)

**Disclaimer:** All scenarios, data, and stakeholders are fictional. These simulations are for skill development and portfolio use only. No real business outcomes are claimed.

---

## How to Use This Guide

1. Pick a simulation and block out the suggested time
2. Read the scenario fully before starting
3. Use whatever tools you prefer (Word, Google Docs, Markdown, pen and paper)
4. Produce real BA deliverables — save them for your portfolio
5. After finishing, work through the self-evaluation and reflection questions
6. Repeat with harder simulations as your skills grow

---

## Simulation 1: Unclear Manager Request

### Scenario Title
Fix the Scheduling Process

### Manager Request

**From:** Jamie R. (Operations Manager)  
**To:** You (Business Analyst)  
**Subject:** Scheduling is a mess — fix it

> Hey,
>
> I need you to take a look at our scheduling process. It's not working well and I'm getting complaints from every direction. Caregivers are showing up late, clients are calling upset, and the coordinators say they're overwhelmed. I want you to fix it.
>
> We need a new scheduling system or something. Just figure out what's wrong and tell me what to do. I've attached a few emails from clients and coordinators so you can see what we're dealing with.
>
> Let's chat when you have some initial thoughts.
>
> Thanks,
> Jamie

### Background Documents

**BrightCare Home Services Overview:**
- Mid-sized home-care agency, ~150 caregivers, ~200 active clients
- 3 scheduling coordinators, 5 care coordinators, 1 operations manager
- Services: personal care, companion care, respite care, medication reminders
- Current "system": paper schedules + Excel + text messages + phone calls
- The company has grown 40% in the past 2 years and the old process can't keep up

**Client Complaint Email (excerpt):**
> "My mom's caregiver was supposed to be there at 9am. She showed up at 10:15. No one called to tell us. This is the third time this month. We're paying for reliable care and we're not getting it."

**Coordinator Note (internal):**
> "I'm drowning. I spend 4 hours every morning just confirming who's actually showing up. Half the time caregivers don't respond to texts. I'm calling backup caregivers constantly. By the time I do client follow-ups, it's already 2pm and I'm behind on tomorrow's schedule."

### Stakeholder Roles Involved

| Stakeholder | Role | Known Concern |
|-------------|------|---------------|
| Jamie R. | Operations Manager | Wants a fix, doesn't know what it should be |
| Maria T. | Scheduling Coordinator | Overwhelmed, feels unheard |
| Diane K. | Caregiver (team lead) | Frustrated with last-minute changes |
| Helen P. | Client's daughter | Worried about her mom's care quality |
| Carlos D. | Compliance Lead | Worried about documentation gaps |

### Hidden Complications

- The real problem may not be the scheduling system at all — it could be communication, capacity, or process
- Jamie assumes a new system is the answer, but the root cause might be something else entirely
- Coordinators have workarounds they haven't told anyone about
- There's no defined escalation process when a caregiver doesn't show up
- Jamie is biased toward a technology solution and may resist non-technical recommendations
- The "scheduling" problem actually touches caregiver onboarding, client intake, payroll, and compliance

### Assignment

Discover the real problem behind Jamie's vague request. Conduct a mini stakeholder analysis, identify root causes, and recommend a path forward — whether it's a new system, process changes, training, or all of the above.

### Deliverables

1. **Stakeholder Discovery Notes** (1-2 pages) — What you learned from each stakeholder, key quotes, concerns identified
2. **Problem Definition Statement** (half page) — A clear, specific statement of the real problem (not the assumed problem)
3. **5-Whys or Root Cause Analysis** — Trace the presenting symptom to root cause(s)
4. **Recommendation Memo** (1 page) — Your recommended approach with rationale

### Estimated Duration

45-60 minutes

### Evaluation Criteria

| Criteria | Self-Score (1-5) | Notes |
|----------|------------------|-------|
| Did you uncover requirements beyond the initial request? | | |
| Did you identify stakeholders beyond the manager? | | |
| Is your problem definition specific and actionable? | | |
| Did you avoid jumping to the solution (new system)? | | |
| Are your recommendations backed by evidence from stakeholders? | | |
| Is your memo professional and ready for a real manager? | | |

### Reflection Questions

- What assumptions did you catch yourself making?
- Where did you have to make educated guesses? What would you ask if you had more time?
- Would your recommendation change if Jamie really wants a new system and won't accept process changes? How would you handle that?
- What additional information would strengthen your analysis?
- How did you decide which stakeholders to talk to and what to ask?

---

## Simulation 2: Conflicting Stakeholder Priorities

### Scenario Title
Speed vs. Documentation

### Manager Request

**From:** Jamie R. (Operations Manager)  
**To:** You (Business Analyst)  
**Subject:** Requirements session follow-up — we need decisions

> We had the requirements workshop yesterday and it got... heated. I need you to pull together the outputs and help us get to a decision.
>
> Here's where we're stuck:
>
> - Operations (me): I need this scheduling system live in 6 weeks. We're bleeding clients and losing caregivers. I don't care about perfect documentation. I care about something that works now.
>
> - Compliance (Carlos): He's threatening to block the whole project unless we have full documentation, role-based access control, audit trails, data retention policies, and sign-off from every department before go-live.
>
> - IT Support (Priya): Says 6 weeks is impossible even for a basic system. Needs at least 10 weeks for integration testing alone. Also needs us to finalize requirements before she can start.
>
> We're stuck in a loop. Operations says go fast. Compliance says go slow. IT says we can't go at all until requirements are done.
>
> I need you to facilitate a resolution. Document the conflicting priorities, propose a path forward, and get us moving again. I expect a decision by Friday.
>
> Jamie

### Background Documents

**Project Context:**
- BrightCare Home Services is implementing a scheduling system (internal project name: "ScheduleRight")
- Requirements have been drafted but not finalized
- Three departments have conflicting timelines and priorities

**Operations Data Points:**
- Client satisfaction score has dropped from 4.2 to 3.6 in 6 months
- 12% of shifts went unfilled last month
- Average caregiver response time to text: 47 minutes
- Estimated monthly revenue at risk from client churn: $18,000

**Compliance Requirements (Carlos's list):**
- Full audit trail of all schedule changes (who, what, when)
- Role-based access (coordinators vs managers vs admins)
- Data retention per state regulations (3 years minimum)
- HIPAA-compliant messaging for client information
- Quarterly access review capability
- Documentation: System design doc, data flow diagram, security assessment, user training records

**IT Constraints (Priya's notes):**
- Current integration with payroll system requires 4-6 weeks of testing alone
- No dedicated test environment available for another 3 weeks
- One developer available part-time (other projects in-flight)
- Estimated minimum effort: 12 weeks for a properly tested system

### Stakeholder Roles Involved

| Stakeholder | Priority | Non-Negotiable |
|-------------|----------|----------------|
| Jamie R. (Operations) | 6-week go-live | Something that reduces client complaints |
| Carlos D. (Compliance) | Full documentation before go-live | Audit trail and role-based access |
| Priya S. (IT) | Finalized requirements before coding starts | Integration testing time |

### Hidden Complications

- Jamie doesn't fully understand the compliance requirements and may be underestimating their importance
- Carlos has been burned before (a previous system launch had a data breach) and won't compromise on security
- Priya's estimate may be padded or may be realistic — you don't have enough info yet
- There might be a phased approach that satisfies all three, but no one has proposed it yet
- The real constraint is probably not time — it's the unspoken lack of trust between Operations and Compliance
- Jamie said "Friday" — note the short deadline. This is a test of your ability to work under pressure

### Assignment

Facilitate a resolution to the scheduling project deadlock. Document each stakeholder's position, identify common ground, propose a compromise or phased approach, and prepare a decision document.

### Deliverables

1. **Stakeholder Position Summary** — Table showing each stakeholder's priority, constraints, and non-negotiables
2. **Option Analysis** (2-3 options with pros/cons) — At least one phased approach that staggers deliverables
3. **Recommended Approach** with rationale and risk mitigation
4. **Decision Log Entry** — Formal record of the decision, who made it, and what was agreed

### Estimated Duration

60-75 minutes

### Evaluation Criteria

| Criteria | Self-Score (1-5) | Notes |
|----------|------------------|-------|
| Did you accurately represent each stakeholder's position? | | |
| Did you find a creative middle ground or phased approach? | | |
| Did you document trade-offs and risks? | | |
| Is your recommendation practical and implementable? | | |
| Did you consider a path where no one gets everything they want? | | |
| Would each stakeholder accept your proposed path? | | |

### Reflection Questions

- What technique did you use to resolve the conflict (compromise, collaboration, prioritization framework)?
- How would you facilitate the actual meeting where these decisions are made?
- If Jamie rejects your phased approach and insists on 6 weeks, what do you do?
- What risks did you identify that none of the stakeholders mentioned?
- How would your approach change if the agency owner got involved and overruled everyone?

---

## Simulation 3: Mid-Project Scope Change

### Scenario Title
The New Regulation Nobody Saw Coming

### Manager Request

**From:** Carlos D. (Compliance Lead)  
**To:** You (Business Analyst)  
**Subject:** URGENT — New state regulation effective next quarter

> I just got off a call with our industry association. The state is rolling out a new regulation (HB-4721) that takes effect in 90 days. This directly affects our ScheduleRight project.
>
> Here's what HB-4721 requires:
>
> 1. Every caregiver visit must include a **digital signature** from the client or their authorized representative at the time of service
> 2. Digital signatures must be stored with a **timestamp and GPS location** of where the signature was collected
> 3. All visit records must include the **specific tasks performed** (not just "personal care" — must be itemized: bathing, dressing, medication reminders, etc.)
> 4. Monthly reports must be generated showing **visit completion vs. scheduled visits** by caregiver and by client
> 5. Records must be **exportable in a state-specified format** (they're releasing the schema next month)
>
> I know we already drafted requirements for ScheduleRight. I need to know:
> - Which requirements are affected?
> - What new requirements do we need to add?
> - How does this impact our timeline and budget?
> - Do we need to inform any other stakeholders?
>
> I need your impact assessment by end of week.
>
> Carlos

### Background Documents

**ScheduleRight Project Status (before this change):**
- 15 business requirements drafted and reviewed
- 20 functional requirements drafted (not yet finalized)
- 12 user stories approved
- RTM in progress
- Target go-live: 12 weeks from now
- Budget approved: $75,000
- Development not yet started — still finalizing requirements

**Affected Requirements (current draft):**

| ID | Description | Current Status |
|----|-------------|----------------|
| BR-003 | Visit documentation must capture service delivery details | Drafted, no digital signature |
| BR-005 | System must support caregiver visit confirmation | Drafted, basic check-in/out only |
| BR-008 | Client records must be maintained per regulatory requirements | Drafted, does not reference HB-4721 |
| FR-007 | System shall generate daily visit completion reports | Drafted, no GPS or timestamp requirement |
| FR-012 | System shall support export of visit data | Drafted, format is internal only |
| FR-015 | System shall notify stakeholders of completed visits | Drafted, no itemized tasks |

**Current Stakeholder Map (for reference):**

| Stakeholder | Interest Level | Would HB-4721 affect them? |
|-------------|---------------|---------------------------|
| Jamie R. (Ops) | Timeline, budget | Yes — may delay go-live or increase cost |
| Priya S. (IT) | Technical feasibility | Yes — digital signature, GPS, new export format |
| Maria T. (Scheduling) | Ease of use for caregivers | Yes — caregivers must collect signatures |
| Helen P. (Client family) | Quality of care | Indirectly — better documentation |
| Agency Owner | Cost, compliance risk | Yes — non-compliance is a legal risk |

### Hidden Complications

- Some caregivers work with elderly clients who may have difficulty providing digital signatures
- GPS location collection raises privacy concerns that may need separate discussion
- The export schema is "coming next month" — means requirements may need to change again
- No one has budgeted for this; it could mean descoping other features
- Carlos sent this to you without copying Jamie — possible politics between Compliance and Operations
- Digital signature implementation could add 3-5 weeks to development

### Assignment

Assess the impact of HB-4721 on the ScheduleRight project. Identify affected requirements, propose new requirements, analyze timeline and budget impact, and create a communication plan.

### Deliverables

1. **Impact Analysis Document** — Structured assessment of HB-4721's impact on scope, timeline, budget, and stakeholders
2. **Updated Requirements** (at least 3 updated, 2 new) — Show before/after for affected requirements
3. **RTM Update** — Revised traceability matrix including new HB-4721 requirements
4. **Change Request Form** — Formal request to modify the project scope
5. **Stakeholder Communication Plan** — Who needs to know, what they need to know, and when

### Estimated Duration

75-90 minutes

### Evaluation Criteria

| Criteria | Self-Score (1-5) | Notes |
|----------|------------------|-------|
| Did you identify all affected requirements? | | |
| Did you consider downstream effects beyond direct requirements? | | |
| Is your impact analysis quantified (time, cost, effort)? | | |
| Did you identify new requirements for the regulation? | | |
| Did you include a risk assessment for unknowns (export schema)? | | |
| Is your communication plan appropriate for each stakeholder? | | |

### Reflection Questions

- What's the hardest decision you had to make in your impact analysis?
- How would you handle it if the agency owner says to absorb the cost without increasing the budget?
- What assumptions did you make about the digital signature requirement? How confident are you in those?
- Did you identify any opportunities in this change (things that could actually benefit the project)?
- How would you approach the conversation with Jamie about the timeline impact?

---

## Simulation 4: System Implementation UAT

### Scenario Title
ScheduleRight UAT — Finding the Defects

### Manager Request

**From:** Priya S. (IT Lead)  
**To:** You (Business Analyst), Maria T. (Scheduling Coordinator)  
**Subject:** ScheduleRight v0.9 ready for UAT — found bugs but need your help

> The dev team has completed the first build of ScheduleRight. It's functional but needs User Acceptance Testing before we can call it done.
>
> I've set up a test environment with sample data (about 2 weeks of simulated schedules, 30 clients, 25 caregivers, 5 coordinators).
>
> I need you to:
> 1. Develop UAT test scenarios based on the requirements
> 2. Execute the test scenarios against the test environment
> 3. Document any defects you find
> 4. Make a go/no-go recommendation for production release
>
> I've attached the requirements doc, the test environment access info, and a note on known limitations.
>
> I'd say this version is 80% there. There are definitely some rough edges — that's what UAT is for.
>
> Priya

### Background Documents

**ScheduleRight v0.9 — Key Features Implemented:**
- Shift scheduling and assignment
- Caregiver schedule view (mobile web)
- Client profile management
- Visit confirmation (check-in/check-out with timestamp)
- Basic reporting (daily completion report)
- NOT yet implemented: digital signatures, GPS tracking, advanced reporting

**Test Environment Data Provided (simulated):**

*Sample Assignments:*

| Assignment ID | Caregiver | Client | Day | Time | Status in System |
|---------------|-----------|--------|-----|------|-----------------|
| S-1001 | Diane K. (CNA, dementia trained) | Eleanor P. (needs dementia care) | Mon | 9am-12pm | Assigned |
| S-1002 | Mark T. (CNA, no dementia training) | Eleanor P. (needs dementia care) | Mon | 1pm-4pm | Assigned |
| S-1003 | Linda R. (RN, wound care certified) | George M. (requires wound care) | Tue | 10am-11am | Assigned |
| S-1004 | Diane K. (CNA) | Robert S. | Mon 9am-12pm AND Robert S. Tue 9am-12pm | Both | Assigned — same week, different days |
| S-1005 | James W. (CNA) | No certification listed in profile | All | Various | Cannot determine qualification matching |

*Test Data Quirks:*
- One caregiver has two shifts at the exact same time on Monday
- One client's address is listed in a different city than their caregiver's service area
- One caregiver's profile shows no certifications despite being assigned to a client who needs wound care
- The "visit confirmation" feature works but doesn't ask for task details (no itemized task list)
- Export report is missing the "client signature" field (expected — not implemented yet)

### Stakeholder Roles

| Stakeholder | UAT Interest | What They Care About |
|-------------|-------------|-------------------|
| You (BA) | Requirements validation | Does the system meet the requirements? |
| Maria T. (Scheduling) | Usability, accuracy | Can I do my job without it breaking? |
| Jamie R. (Operations) | Go/no-go decision | Is this good enough to launch? |
| Carlos D. (Compliance) | Audit readiness | Are records compliant? |

### Hidden Complications

- The "double-booked" caregiver creates a situation where the system allows conflicts — is this a defect or a feature gap?
- Some of the "defects" you find might actually be missing requirements that were never written
- Priya says 80% done — but 80% toward what? The requirements or her own target?
- The export report bug is expected (signature not implemented), but it's also a compliance issue
- Some bugs might be in the test data, not the system — how do you distinguish?

### Assignment

Execute a structured UAT. Design test scenarios that cover the most critical requirements, identify genuine defects versus data issues versus missing requirements, document everything professionally, and make a recommendation.

### Deliverables

1. **UAT Test Plan** (1 page) — Scope, approach, test environment, schedule
2. **Test Scenarios** (at least 5, with pass/fail criteria and requirement traceability)
3. **Test Execution Log** — Which scenarios passed, which failed, with evidence
4. **Bug Reports** (at least 3) — Structured: severity, steps to reproduce, expected vs actual behavior, evidence
5. **UAT Summary Report** — Overall findings, go/no-go recommendation, risks of going forward, risks of delaying

### Estimated Duration

90-120 minutes

### Evaluation Criteria

| Criteria | Self-Score (1-5) | Notes |
|----------|------------------|-------|
| Did you trace test scenarios to specific requirements? | | |
| Did you distinguish between bugs, data issues, and missing requirements? | | |
| Are your bug reports specific enough for a developer to understand? | | |
| Did you consider both functional and non-functional aspects? | | |
| Is your go/no-go recommendation justified? | | |
| Did you identify risks that Priya didn't mention? | | |

### Reflection Questions

- How did you decide what to test when you can't test everything?
- Which defects were hardest to verify and why?
- If you recommended "no-go," what would it take to get to a "go"?
- How would you communicate a "no-go" recommendation to Jamie when she wants speed?
- What would you do differently if you had real stakeholders to interview before designing the tests?

---

## Simulation 5: Executive Status Report

### Scenario Title
Leadership Wants to Know Where We Stand

### Manager Request

**From:** Agency Owner  
**To:** You (Business Analyst)  
**Cc:** Jamie R. (Operations Manager)  
**Subject:** Operations improvement project — status update needed

> Hi,
>
> I need a concise status update on the operations improvement project (ScheduleRight) for our quarterly board review. I have 15 minutes in the agenda — I need to cover what we've accomplished, where we're at risk, and what's next.
>
> Specifically, I need:
> - A status summary (green/yellow/red for schedule, budget, quality)
> - Key accomplishments since last report
> - Top 3 risks and what we're doing about them
> - KPIs showing whether we're actually improving operations
> - Next steps and milestones for the next quarter
>
> I don't need a novel. I need a board-ready executive summary that tells me what I need to know in 2 pages or less. I'll be presenting this to the board, so it needs to look professional.
>
> Jamie can fill you in on the project details. Pull from whatever project docs you have. If there's data you need that doesn't exist, note it as a gap.
>
> Deadline: 48 hours.
>
> Thanks.

### Background Documents

**Project Status Summary (from Jamie):**

| Area | Status | Notes |
|------|--------|-------|
| Schedule | Yellow | Requirements phase took 2 weeks longer than planned. Development started late. Current target: 8 weeks to go-live. Originally 12 weeks from start, now at week 6. |
| Budget | Green | Spent $22,000 of $75,000 budget. On track for remaining $53,000. |
| Scope | Yellow | HB-4721 regulation (digital signatures, GPS) added scope. Impact analysis complete. Budget impact estimated at $8,000-12,000 additional. |
| Quality | Green | UAT phase 1 complete. 3 critical bugs found and fixed. 2 minor bugs open. |

**KPIs Tracked:**
(Note: some of these are pre-improvement baselines, some are targets)

| KPI | Baseline (Before) | Current | Target | Notes |
|-----|------------------|---------|--------|-------|
| Client Satisfaction Score | 3.8 / 5.0 | 3.6 / 5.0 | 4.5 / 5.0 | Slight decline — likely due to change fatigue |
| Shift Fill Rate | 88% | 88% | 95% | Not yet improved — system not live |
| Caregiver Response Time | 47 min | 42 min | 15 min | Marginal improvement from process changes |
| Average Late Arrival Time | 18 min | 16 min | 5 min | Slight improvement from coordinator training |
| Compliance Audit Findings | 7 open | 5 open | 0 open | 2 resolved from process changes |
| Weekly Admin Hours on Scheduling | 28 hrs | 26 hrs | 10 hrs | Small improvement from template standardization |

**Recent Accomplishments:**
- Requirements phase completed (including HB-4721 impact)
- ScheduleRight v0.9 developed and UAT initiated
- Caregiver communication process updated (text templates, response tracking)
- 2 compliance audit findings resolved through process changes
- Training materials for ScheduleReady drafted

**Next Milestones:**
- Week 8: UAT complete, all critical bugs resolved
- Week 10: Production deployment
- Week 12: Go-live and hyper-care period
- Week 16: Post-implementation review

### Stakeholder Roles

| Stakeholder | What They Want From This Report |
|-------------|-------------------------------|
| Agency Owner | Board-ready executive summary, bottom-line message, confidence in investment |
| Board Members | Clear status, risk awareness, ROI story |
| Jamie R. (Ops) | Accurate representation of progress, protected from blame for delays |

### Hidden Complications

- The yellow status on schedule is understated — the HB-4721 change has not been formally approved yet
- KPI improvements so far are marginal and hard to attribute to the project (could be other factors)
- The board may ask whether this investment is worth it given the marginal improvements
- Client satisfaction declining during the project is a concern — could become a talking point for critics
- There is no explicit ROI calculation in the project docs — the board likely expects one

### Assignment

Compile an executive status report that gives leadership a clear, honest picture of the project's health, progress, and outlook. Balance optimism with transparency.

### Deliverables

1. **Executive Status Report** (2 pages max) — Professional, board-ready summary
2. **Dashboard View** (1 page) — Visual summary with RAG status, KPI table, milestone timeline
3. **Risk Brief** (half page) — Top 3 risks with current mitigation status
4. **Next Quarter Roadmap** (half page) — Key milestones, decisions needed, asks of leadership

### Estimated Duration

60-90 minutes

### Evaluation Criteria

| Criteria | Self-Score (1-5) | Notes |
|----------|------------------|-------|
| Is the report concise enough for a 15-minute board presentation? | | |
| Does it balance good news with honest risks? | | |
| Are KPIs presented clearly with context (baseline, target, trend)? | | |
| Does it tell a coherent story about whether the project is working? | | |
| Would the agency owner feel confident presenting this to the board? | | |
| Did you identify any data gaps that need to be addressed? | | |

### Reflection Questions

- What was the hardest balance to strike — optimism or honesty?
- If the board asks "has this project actually improved anything yet?" what's your answer?
- How would you present the client satisfaction decline without alarming the board?
- What's missing from the project data that would make your report stronger?
- If the agency owner asks for a "green" status when you think it's "yellow," how do you handle it?

---

## Portfolio Tips

### Before You Start Each Simulation

- Save your deliverables with filenames like `simulation-1-discovery-notes.md` so they're easy to reference later
- Note the date, simulation title, and your estimated vs actual time
- Set a timer and respect the time limit — real BA work always has deadlines

### After You Finish

- Rate yourself honestly on the evaluation criteria
- Write 2-3 sentences on what you learned for each simulation
- If you got stuck, note what tripped you up — that's where you need more practice

### How These Help Your Portfolio

- **In interviews:** "Tell me about a time you handled conflicting stakeholder priorities" → Simulation 2
- **In your resume:** "Conducted UAT for scheduling system implementation, identifying 5 critical defects" → Simulation 4
- **In your portfolio:** Include polished deliverables as samples with a header noting they are practice simulations

### Real BA Skills These Simulations Build

| Simulation | Primary Skills | Secondary Skills |
|-----------|---------------|-----------------|
| 1. Unclear Request | Elicitation, problem definition, root cause analysis | Stakeholder identification, communication |
| 2. Conflicting Priorities | Facilitation, prioritization, negotiation | Decision documentation, options analysis |
| 3. Scope Change | Impact analysis, change management, RTM | Requirements writing, communication planning |
| 4. UAT | Test scenario design, defect documentation, QA | Requirement traceability, go/no-go decision |
| 5. Executive Report | Executive communication, KPI presentation, risk reporting | Synthesis, data visualization |

---

## Next Steps After Completing All 5

1. Review your deliverables as a set — do they tell a coherent story about your BA skills?
2. Pick the 2-3 strongest deliverables to polish for your portfolio
3. Repeat any simulation where you scored below 3 on multiple criteria
4. Try the simulations again with a self-imposed constraint (half the time, no templates, unexpected email from a stakeholder mid-way through)
5. When the BA Compass Work Simulation Lab is eventually built, you'll already have a head start on the skills it teaches
