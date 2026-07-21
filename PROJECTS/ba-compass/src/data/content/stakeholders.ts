// BA Compass — Stakeholder Content (from docs/05-stakeholder-register.md + docs/06-stakeholder-analysis.md)
// DISCLAIMER: All stakeholders are fictional.

export interface StakeholderContent {
  id: string;
  role: string;
  interest: string;
  influence: "High" | "Medium" | "Low";
  priority: string;
  needs: string;
  painPoints: string;
  responsibilities: string;
  communication: string;
  decisionAuthority: string;
  risks: string;
  requirementOwnership: string;
}

export const stakeholders: StakeholderContent[] = [
  {
    id: "STK-001",
    role: "Agency Owner",
    interest: "Strategic",
    influence: "High",
    priority: "Key Player",
    needs: "Operational visibility, trend data, risk awareness, strategic recommendations",
    painPoints: "No dashboard, anecdotal reporting, cannot identify systemic issues",
    responsibilities: "Strategic direction, funding, final approval",
    communication: "Monthly executive summaries, milestone reviews, KPI reports",
    decisionAuthority: "Final sign-off on scope, requirements, budget",
    risks: "Cost of change, disruption to operations, implementation timeline",
    requirementOwnership: "BR-008 (KPI Dashboard), BR-012 (Reporting)",
  },
  {
    id: "STK-002",
    role: "Operations Manager",
    interest: "Operational",
    influence: "High",
    priority: "Key Player",
    needs: "Real-time shift status, gap alerts, escalation visibility, KPI tracking",
    painPoints: "Reactive firefighting, no consolidated view, manual coordination",
    responsibilities: "Daily operations, team management, process improvement",
    communication: "Weekly operational reviews, daily dashboard access, ad-hoc reports",
    decisionAuthority: "Operational process changes, escalation procedures",
    risks: "New system disrupting current workflow, staff training burden",
    requirementOwnership: "BR-001 (Shift Visibility), BR-006 (Centralized View), BR-011 (Late Arrival)",
  },
  {
    id: "STK-003",
    role: "Scheduling Coordinator",
    interest: "Tactical",
    influence: "Medium",
    priority: "Keep Informed",
    needs: "Gap visibility, shift confirmation tracking, easy status updates",
    painPoints: "Manual calls to fill gaps, no confirmation system, phone tag",
    responsibilities: "Creating schedules, assigning caregivers, filling gaps",
    communication: "Daily operational updates, scheduling reports, shift data entry",
    decisionAuthority: "Schedule adjustments within operational guidelines",
    risks: "Increased data entry burden, technology replacing judgment",
    requirementOwnership: "BR-002 (Gap Identification)",
  },
  {
    id: "STK-004",
    role: "Care Coordinator",
    interest: "Tactical",
    influence: "Medium",
    priority: "Keep Informed",
    needs: "Issue escalation path, documentation status, client feedback tracking",
    painPoints: "No structured issue tracking, repeated explanations, no follow-up system",
    responsibilities: "Client assignment, issue resolution, caregiver communication",
    communication: "Daily updates on issues, client feedback, care plan changes",
    decisionAuthority: "Client reassignment, caregiver changes, service adjustments",
    risks: "Inability to customize for unique client needs",
    requirementOwnership: "BR-003 (Escalation), BR-004 (Follow-Up)",
  },
  {
    id: "STK-005",
    role: "Caregiver",
    interest: "Frontline",
    influence: "Low",
    priority: "Keep Informed",
    needs: "Clear schedule, easy documentation, issue reporting path",
    painPoints: "Schedule changes without notice, no feedback on reports",
    responsibilities: "Shift completion, service documentation, issue reporting",
    communication: "Schedule notifications, documentation reminders, issue reporting",
    decisionAuthority: "Shift acceptance / decline within guidelines",
    risks: "Technology burden, reduced flexibility, monitoring concerns",
    requirementOwnership: "Input into usability requirements",
  },
  {
    id: "STK-006",
    role: "Quality Assurance Lead",
    interest: "Compliance",
    influence: "Medium",
    priority: "Keep Informed",
    needs: "Documentation completion tracking, audit trail, compliance reporting",
    painPoints: "No documentation tracking, cannot identify gaps, audit preparation is manual",
    responsibilities: "Quality monitoring, documentation auditing, compliance reporting",
    communication: "Monthly quality reports, documentation dashboards, audit preparation",
    decisionAuthority: "Quality standards, documentation requirements",
    risks: "Incomplete data, resistance to documentation requirements",
    requirementOwnership: "BR-005 (Documentation Tracking)",
  },
  {
    id: "STK-007",
    role: "Client Services Representative",
    interest: "Client-facing",
    influence: "Low",
    priority: "Keep Informed",
    needs: "Clear escalation path, issue tracking, client communication templates",
    painPoints: "Issues passed verbally, no tracking, status inquiries require chasing",
    responsibilities: "Client intake, issue reporting, client communication",
    communication: "Client updates, issue reports, escalation notifications",
    decisionAuthority: "Issue intake, initial response",
    risks: "Technology replacing personal touch, increased monitoring",
    requirementOwnership: "BR-007 (Client Communication)",
  },
  {
    id: "STK-008",
    role: "IT Administrator",
    interest: "Technical",
    influence: "Medium",
    priority: "Key Player",
    needs: "Clear requirements, deployment plan, support processes",
    painPoints: "Unclear requirements, scope creep, no deployment plan",
    responsibilities: "Technical implementation, system support, integration",
    communication: "Technical design reviews, deployment planning, support handoff",
    decisionAuthority: "Technical architecture, tools selection",
    risks: "Integration complexity, maintenance burden, security exposure",
    requirementOwnership: "NFR-007 (Maintainability), NFR-008 (Reliability)",
  },
  {
    id: "STK-009",
    role: "Compliance Representative",
    interest: "Regulatory",
    influence: "High",
    priority: "Key Player",
    needs: "Audit trail, documentation tracking, privacy controls, reporting",
    painPoints: "Cannot demonstrate documentation compliance, manual audit preparation",
    responsibilities: "Regulatory compliance, audit preparation, policy enforcement",
    communication: "Compliance reports, audit findings, regulatory updates",
    decisionAuthority: "Compliance requirements, privacy controls",
    risks: "Inadequate documentation, privacy breaches, regulatory findings",
    requirementOwnership: "BR-009 (Policy Doc), BR-010 (Audit Trail), BR-014 (Data Labeling)",
  },
  {
    id: "STK-010",
    role: "Client / Family Representative",
    interest: "Service Quality",
    influence: "Low",
    priority: "Monitor",
    needs: "Reliable care, schedule visibility, issue resolution",
    painPoints: "Missed shifts, late arrivals, no communication about changes",
    responsibilities: "Receiving care, providing feedback",
    communication: "Shift notifications, issue updates, satisfaction surveys",
    decisionAuthority: "Service acceptance, feedback",
    risks: "Privacy, reduced human interaction, impersonal service",
    requirementOwnership: "Indirect — represented through BR-007",
  },
];

// Power-Interest Matrix Data
export const powerInterestMatrix = [
  { x: "High Power", y: "High Interest", label: "Manage Closely", stakeholders: ["STK-001 Agency Owner", "STK-002 Operations Manager", "STK-009 Compliance Representative"] },
  { x: "High Power", y: "Low Interest", label: "Keep Satisfied", stakeholders: ["STK-008 IT Administrator"] },
  { x: "Low Power", y: "High Interest", label: "Keep Informed", stakeholders: ["STK-003 Scheduling Coordinator", "STK-004 Care Coordinator", "STK-006 QA Lead"] },
  { x: "Low Power", y: "Low Interest", label: "Monitor", stakeholders: ["STK-005 Caregiver", "STK-007 Client Services Rep", "STK-010 Client/Family Rep"] },
];

// Stakeholder conflicts
export const stakeholderConflicts = [
  {
    parties: "Operations Manager vs. Compliance Representative",
    issue: "Process speed vs. documentation rigor",
    resolution: "Design workflow stages that capture documentation without blocking operations",
  },
  {
    parties: "Scheduling Coordinators vs. Caregivers",
    issue: "Fill-gap pressure vs. schedule flexibility",
    resolution: "Define clear gap-fill procedures with caregiver preference options",
  },
  {
    parties: "Agency Owner vs. IT Administrator",
    issue: "Feature scope vs. technical simplicity",
    resolution: "Prioritize must-have features, document future enhancements",
  },
  {
    parties: "Quality Assurance vs. Scheduling",
    issue: "Documentation completion vs. quick assignments",
    resolution: "Define acceptable documentation windows, not real-time requirements",
  },
  {
    parties: "Client Services vs. Operations",
    issue: "Client requests vs. operational capacity",
    resolution: "Establish structured escalation with clear response SLAs",
  },
];
