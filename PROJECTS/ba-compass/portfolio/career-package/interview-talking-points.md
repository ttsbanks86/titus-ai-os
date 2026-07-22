# Interview Talking Points — BA Compass | BrightCare Home Services

All data is synthetic. BrightCare Home Services is a fictional company created for portfolio purposes. Do not claim real operational results or employer sponsorship.

---

## 1. Business Problem

The core problem I defined was that a growing home-care agency had fragmented operational processes that hadn't scaled with its growth. Three specific pain points emerged: scheduling was managed through spreadsheets and phone calls, leading to double-bookings and missed visits; care documentation was paper-based and often reached the office days late; and billing was delayed because paper records needed manual data entry before invoices could go out. Leadership had no real-time visibility into any of these areas. I framed this as a problem statement with three measurable success criteria: reduce scheduling conflicts, reduce documentation lag, and reduce billing cycle time.

In a real engagement, I would validate these assumptions with actual data from the operational systems, interview a broader set of frontline staff, and conduct time-motion studies to quantify the baseline.

---

## 2. Stakeholder Analysis

I identified 14 stakeholders across four domains: operations (schedulers, caregivers, branch managers), clinical (clinical director, care coordinators), finance (billing team, CFO), and technology (IT manager, external EHR vendor). I mapped each to a power/interest grid and classified them as high-power/high-interest, high-power/low-interest, low-power/high-interest, or low-power/low-interest. This directly informed my engagement strategy: high-power stakeholders got regular status updates and decision invitations; high-interest stakeholders were included in workshops and requirement reviews.

The key insight was that schedulers and caregivers had high interest but low formal authority, so I made sure their pain points were represented during prioritization even though they werent the primary decision-makers.

---

## 3. Requirements Prioritization

I used MoSCoW prioritization because it is straightforward, collaborative, and forces clear tradeoff conversations. I drafted an initial list of 20 potential features based on the problem analysis and stakeholder input, then facilitated a prioritization exercise using the power/interest map to decide who had decision authority.

The must-haves centered on scheduling (conflict detection, caregiver assignment), care documentation (digital notes, signature capture), and billing (invoice generation, claims tracking). Should-haves included reporting and basic dashboards. Could-haves included mobile push notifications and advanced analytics. The explicit wont-haves were dropped to protect scope.

In a real organization, I would prioritize with more formal cost-benefit analysis and use weighted scoring against strategic objectives, not just stakeholder opinion.

---

## 4. KPI Selection

I defined 12 KPIs across four categories: scheduling efficiency (schedule fill rate, same-day confirmation rate), clinical quality (documentation timeliness, compliance score), financial performance (revenue per visit, billing cycle time, first-pass billing yield), and workforce management (caregiver utilization, turnover rate, training compliance).

Each KPI has a definition, measurement formula, data source, target value, and reporting frequency documented in a KPI register. I designed them to be leading indicators where possible so leadership could act before problems escalated.

For the dashboard, I chose Recharts because it is flexible, React-native, and supports the visualization types I needed: trend lines with target bands, bar charts for comparisons, and status indicators for at-a-glance monitoring.

---

## 5. Traceability

The traceability matrix is a table with each requirement listed with its ID, description, priority, source, associated test cases, and the application component or route that implements it.

I built it as a living document in the application that can be filtered by requirement status, priority, or coverage. It serves two purposes: it proves every requirement is addressed, and it makes impact analysis straightforward when a change is proposed. If someone asks what happens if we remove Requirement F-005, the matrix shows exactly which test cases and UI components are affected.

In a real engagement, a traceability matrix is non-negotiable for regulated industries and extremely useful for managing change requests in any context.

---

## 6. Risk Analysis

I identified 11 risks through a structured brainstorming approach organized by category: technology risks (data migration failure, integration complexity), operational risks (caregiver resistance to new system, scheduling disruption during transition), organizational risks (budget overrun, scope creep), and external risks (vendor reliability, regulatory changes).

Each risk was scored on probability (1-5) and impact (1-5) to produce a risk score. The highest-severity items were caregiver technology adoption resistance (high probability, high impact) and scheduling disruption during cutover (moderate probability, high impact). For each risk I developed a mitigation strategy and, for risks above a threshold score, a contingency plan.

I learned that risk registers are only useful if they are actively maintained. This one includes review cadence and owner assignments as a reminder that risk management is a continuous activity.

---

## 7. Future-State Design

The future-state process design focused on three transformed workflows. Scheduling becomes automated with conflict detection, caregiver preference matching, and same-day confirmation. Care documentation becomes mobile-first with structured forms, offline support, and real-time submission. Billing becomes integrated with automated code verification, claim submission tracking, and revenue cycle analytics.

I estimated a 50-60% reduction in manual touchpoints based on the difference between current-state task counts and future-state automated steps. These estimates are illustrative given the synthetic nature of the data.

In a real engagement, I would validate these estimates through process mining or time studies, conduct a pilot before full rollout, and design a change management plan that addresses both process and technology adoption.

---

## 8. Synthetic Data Handling

All data in BA Compass is synthetic. I generated it using Faker.js with constraints to make it realistic: caregivers have skill tags and availability schedules, clients have care plans and visit histories, billing records have realistic codes and amounts. The KPI dashboard uses time-series data engineered to show trends that make sense for the narrative.

I was transparent about this in every deliverable. Every page, document, and description includes a clear disclosure that BrightCare Home Services is fictional. I did this because I want hiring managers to evaluate my BA skills, not wonder if the data is real.

If a recruiter asks why I used synthetic data, the honest answer is: I needed a realistic business context to demonstrate BA skills, and I do not have authorization to share real employer data.

---

## 9. Responsible AI Use

I used AI tools to generate application code, write test cases, and debug issues. That accelerated the development phase significantly, which is common in industry practice.

However, every BA decision in the project is my own. I defined the business problem. I decided which stakeholders to include and how to engage them. I wrote the BRD content. I chose the KPIs. I assessed the risks. I determined the prioritization. The AI was a productivity tool for the implementation phase, not a substitute for BA thinking.

In a real organization, I would follow the same principle: use AI for efficiency gains on production tasks while maintaining full ownership of analysis and methodology decisions.

---

## 10. AI-Assisted Development

Specifically, I used AI to scaffold the Next.js application, generate initial component structures, write boilerplate test cases, and suggest TypeScript types. I reviewed all generated code, modified it to match requirements, and made architectural decisions about routing, state management, and component organization.

The BA-specific pages (BRD viewer, traceability matrix, KPI dashboard, risk register, executive summary) were built from my specifications. I designed the data models to reflect the business domain, defined the calculation logic for KPIs, and structured the traceability matrix to match my requirements documentation.

If an interviewer asks about this, I am direct: yes, I used AI. I also reviewed, modified, and owned every line of output because my name is on the project.

---

## 11. What I Would Do Differently in a Real Organization

Several things. First, I would spend more time on requirements elicitation using multiple techniques: interviews, document analysis, observation, and surveys, not just structured brainstorming. Second, I would conduct proper cost-benefit analysis before prioritization instead of relying solely on stakeholder opinion. Third, I would build a change management plan from day one, not treat it as an afterthought. Fourth, I would design a phased rollout with a pilot group before full deployment. Fifth, I would insist on real user testing with actual caregivers and schedulers before calling any requirement complete.

These are not criticisms of the portfolio project, because the project had constraints (no real users, no real budget, no real organization). They reflect my understanding of what separates a classroom or portfolio exercise from real BA practice.

---

## 12. Assumptions and Limitations

The most significant limitation is that this was a solo project with no real stakeholders, no real budget, no real timeline, and no real users. In a real engagement, stakeholder management is messy, budgets change, timelines slip, and users push back. Requirements are never as clean as they appear in a single-authored BRD. The negotiation, facilitation, and relationship management skills that are central to the BA role cannot be fully demonstrated in a solo portfolio.

Other limitations: no cost-benefit analysis, no formal change request process, no user acceptance testing with actual end users, no production support or post-launch measurement. These are acknowledged gaps, and I discuss them openly to demonstrate my understanding of real-world BA practice.

---

## 13. Questions to Ask the Interviewer

- How does your organization currently handle requirements traceability from ideation through delivery?
- What does the BA role look like in your delivery lifecycle do BAs work through implementation or hand off at a certain point?
- How do you balance the need for documentation velocity in an agile environment with the rigor required for regulated or compliance-heavy domains?
- What tools does your team use for requirements management, and how mature is the current BA practice?
- Can you tell me about a time when stakeholder priorities were in direct conflict and how the BA team helped resolve it?
- How does your organization measure the success of a BA are there specific KPIs for the BA function itself?
