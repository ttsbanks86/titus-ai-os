# STAR Stories — BA Compass | BrightCare Home Services

All scenarios are from a portfolio simulation using synthetic data and a fictional company (BrightCare Home Services). These are not real employment experiences.

---

## 1. Ambiguous Business Problem

**Situation:** In this portfolio simulation, BrightCare Home Services leadership described their problem as we need better technology. No specific pain points, no measurable outcomes, just a vague sense that the current way of working wasnt sustainable. As the Business Analyst on the project, I needed to translate this broad dissatisfaction into a specific, actionable problem statement.

**Task:** My goal was to define the business problem with enough precision that it could drive requirements, prioritization, and success measurement. I needed to move the conversation from we need software to here are the specific operational gaps and what we should measure to close them.

**Action:** I designed a structured discovery process. First, I identified 14 stakeholders across operations, clinical, finance, and technology. I conducted individual interviews with each group, asking about their daily workflows, pain points, and what done would look like from their perspective. I documented current-state processes for scheduling, care documentation, and billing, which revealed 7 distinct pain points including double-bookings, 48-hour documentation lag, and 14-day billing cycles. I synthesized these into a problem statement with three measurable success criteria tied to specific operational outcomes.

**Result:** The executive sponsor approved the problem statement, which became the foundation for the entire project. The requirements, KPIs, and success criteria all traced back to this initial framing. This experience reinforced my belief that the most valuable thing a BA can do early in a project is force clarity out of ambiguity.

---

## 2. Conflicting Stakeholder Priorities

**Situation:** During the prioritization phase of the BrightCare simulation, three stakeholder groups had fundamentally different views on what mattered most. The clinical director wanted comprehensive care documentation features above all else. The CFO prioritized billing cycle improvements and revenue tracking. Operations leadership cared most about scheduling optimization. Each group had legitimate business justifications, and all three could not be fully delivered within a reasonable scope.

**Task:** I needed to facilitate a prioritization process that acknowledged all perspectives, created a transparent framework for tradeoff decisions, and produced a scope that the executive sponsor could approve without alienating any stakeholder group.

**Action:** I mapped all 14 stakeholders to a power/interest grid to identify decision authority. I then introduced a MoSCoW framework and facilitated a structured prioritization workshop. Before the session, I drafted an initial requirement list and asked each stakeholder group to privately rank their priorities. In the workshop, I presented the aggregate results, which showed clear common ground: scheduling and billing were universally recognized as must-haves. I focused the discussion on the legitimate edge cases where priorities diverged and used the power/interest map to guide escalation to the executive sponsor when needed.

**Result:** The final scope included all must-have scheduling and billing capabilities along with core clinical documentation features. Non-critical features were deferred. The clinical director agreed to the tradeoff because she could see her core requirements were protected and understood the cost of including everything. The project moved forward with stakeholder buy-in from all three groups.

---

## 3. Requirements Traceability

**Situation:** After the BRD was drafted with 24 requirements, I faced a common BA challenge: ensuring every requirement was actually delivered and tested, with no orphan requirements and no undocumented features. In many projects, traceability is an afterthought, leading to scope gaps or wasted effort on unrequested functionality.

**Task:** I needed to build a traceability framework that linked every requirement to its implementation and verification, making it possible to answer at any point what requirements are complete and which features trace back to which business need.

**Action:** I created a requirements traceability matrix with bidirectional links. Each of the 16 functional requirements received a unique ID (F-001 through F-016) and was mapped to its source stakeholder, acceptance criteria, associated test cases, and the specific application route or component where it was implemented. The matrix was built as a living document inside the application itself, with filtering by status, priority, and coverage. For validation, I ran a coverage check that confirmed 100% of requirements had at least one passing test case and one UI component.

**Result:** The traceability matrix became a central reference point for the project. It proved that no requirements were lost and no features were built without a business case. When I demonstrated the project to recruiters, the traceability matrix was one of the artifacts that consistently generated interest because it is a concrete example of rigorous BA practice that many hiring managers look for.

---

## 4. KPI Definition

**Situation:** BrightCare leadership in the simulation wanted a dashboard that would give them visibility into operational performance, but they initially asked for everything: every metric they could think of, without clear definitions or data sources. Without structure, the dashboard would have been a cluttered display of unactionable numbers.

**Task:** My job was to define a focused set of KPIs that were measurable, actionable, and tied directly to the business objectives we had established in the problem statement. Each KPI needed a clear definition, methodology, target, and data source.

**Action:** I started by mapping the business objectives from the problem statement to potential metrics. I evaluated each candidate against a set of criteria: is it measurable with available data, is it actionable, does it tie to a specific business outcome, and is there a reasonable target value. This narrowed the field significantly. I landed on 12 KPIs organized into four categories: scheduling efficiency, clinical quality, financial performance, and workforce management. For each, I documented the definition, formula, data source, reporting frequency, and target. I then designed an interactive dashboard using Recharts that showed trend lines with target bands, bar charts for period comparisons, and status indicators for at-a-glance monitoring.

**Result:** The KPI dashboard was delivered with all 12 metrics visualized against targets using synthetic time-series data. The structured KPI definitions ensured that every number on the dashboard had a clear meaning and a clear action associated with it. When I walk through this project in interviews, I focus on the process of selection, not just the final dashboard, because that is where the BA skill is demonstrated.

---

## 5. Risk Mitigation

**Situation:** Partway through the requirements phase in the BrightCare simulation, it became clear that several risks could derail the project if not addressed. The highest-concern items were caregiver resistance to technology adoption and the risk of scheduling disruption during cutover.

**Task:** I needed to lead a structured risk assessment that identified, scored, and developed mitigation strategies for the most significant project risks. The goal was not to eliminate risk but to ensure we had planned responses ready.

**Action:** I facilitated a risk identification workshop structured around four categories: technology, operational, organizational, and external. We identified 11 risks and scored each on probability (1-5) and impact (1-5). The two highest-scoring risks were caregiver technology adoption resistance (probability 4, impact 4) and scheduling disruption during cutover (probability 3, impact 5). For each risk, I developed a primary mitigation strategy and, for items with a composite score above 12, a contingency plan. The caregiver adoption risk, for example, had mitigations including early involvement of lead caregivers in UAT, a phased rollout starting with the most tech-comfortable team, and a paper fallback process for the transition period.

**Result:** The risk register was documented with all 11 risks, scores, mitigations, and contingency plans. The executive sponsor reviewed and approved the risk responses. While I cannot prove the mitigations would have worked (this is a simulation), the structured approach demonstrated that I understand risk management as a proactive, continuous BA responsibility.

---

## 6. Quality Assurance

**Situation:** After requirements were documented and the application was built, I needed to verify that the delivered product actually met the specifications. Without structured quality assurance, the risk of requirements being misinterpreted or incompletely implemented would go undetected.

**Task:** I needed to design a test strategy that linked directly back to requirements and provided confidence that each functional requirement was working as specified.

**Action:** I wrote acceptance criteria for each of the 16 functional requirements before development began. These criteria were specific, testable, and included both positive and negative test cases. For instance, the scheduling conflict detection requirement had criteria covering overlapping visit detection, caregiver availability validation, and edge cases like same-day rescheduling. I then translated these criteria into test cases organized by requirement ID. The project ended up with 76 unit tests covering individual functions and 14 end-to-end tests covering complete user workflows. I ran the full suite after each major change, and the traceability matrix was updated to show test status per requirement.

**Result:** The test suite achieved 100% pass rate with TypeScript strict mode enforcing type safety across the codebase. Every requirement had at least one passing test. The structured approach meant I could produce a test coverage report that mapped directly back to the BRD. This demonstrated that I understand quality assurance as an integral part of the BA role, not something that gets handed off to a separate QA team without BA involvement.

---

## 7. Scope Control

**Situation:** During the requirements review phase, one of the high-power stakeholders requested a significant addition: a mobile app for caregivers with offline capabilities, push notifications, and GPS check-in. This was not in the original scope. It was a valuable idea, but adding it would have delayed the project and stretched resources.

**Task:** I needed to handle this scope change request professionally without rejecting the stakeholders idea outright or derailing the project plan. The BA challenge was to acknowledge the value, evaluate the impact, and manage the decision process transparently.

**Action:** I thanked the stakeholder for the suggestion and documented it as a formal change request with estimated effort, dependencies, and impact on the existing scope. I analyzed the request against the MoSCoW framework: it clearly fell into the could-have or wont-have category given the current timeline. I presented the tradeoff analysis to the stakeholder and the executive sponsor together, showing what would need to be deferred if this feature were added. The analysis made the decision straightforward: we kept the original scope, added the mobile features to the roadmap for a future phase, and the stakeholder felt heard because their request was formally documented and not simply rejected.

**Result:** Scope was maintained, the stakeholder remained engaged and supportive, and the change request was logged for future consideration. This experience reinforced the importance of having a structured change management process, even in a simulated project, because scope creep is one of the most common threats to project success.

---

## 8. Responsible Use of AI

**Situation:** I chose to use AI tools during the development phase of this portfolio project to generate application code, write test cases, and debug issues. This decision presented a professional challenge: how do I demonstrate BA competence when the implementation artifacts were partially AI-generated?

**Task:** I needed to use AI in a way that accelerated the project without letting it substitute for my own analytical work. I also needed to be transparent about AI use so that anyone evaluating the project could make an informed assessment of my skills.

**Action:** I drew a clear boundary. The BA work defining the problem, identifying stakeholders, writing requirements, selecting KPIs, assessing risks, designing processes, and structuring traceability was entirely my own analysis. AI was used for implementation, which is a technical execution task, not a BA task. I reviewed every line of AI-generated code, made architectural decisions about structure and routing, and wrote the specifications that guided what the AI generated. I documented this approach in a disclosure statement that appears on every page of the application alongside the synthetic data disclosure.

**Result:** The project was delivered faster than if I had written every line of code manually. More importantly, the BA artifacts are clearly mine, and the AI contribution is transparently disclosed. I have a consistent answer for interviewers: I use AI as a productivity tool, not as a substitute for BA thinking. This positions me as someone who works efficiently without compromising on analytical rigor.
