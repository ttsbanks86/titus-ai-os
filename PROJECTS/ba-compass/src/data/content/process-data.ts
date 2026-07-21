// BA Compass — Process Content (from docs/07-current-state-process.md)
// DISCLAIMER: All data is fictional.

export interface ProcessStep {
  step: number;
  name: string;
  actor: string;
  input: string;
  action: string;
  output: string;
  channel: string;
  delay: string;
  failurePoint: string;
  manualWork: string;
  dataGap: string;
  controlWeakness: string;
}

export const currentStateSteps: ProcessStep[] = [
  { step: 1, name: "Shift Creation", actor: "Scheduling Coordinator", input: "Client care plan, service schedule, caregiver availability", action: "Create shift record in spreadsheet or written schedule", output: "New shift entry", channel: "Spreadsheet, paper calendar, or email", delay: "No real-time creation; often batched weekly", failurePoint: "No validation that shift information is complete", manualWork: "Entirely manual entry", dataGap: "No structured format — inconsistent data entry", controlWeakness: "No approval or verification step" },
  { step: 2, name: "Caregiver Assignment", actor: "Scheduling Coordinator", input: "Shift details, caregiver availability", action: "Call or text potential caregivers to fill shift", output: "Verbal or text-based agreement", channel: "Phone, text message", delay: "Dependent on caregiver response time", failurePoint: "No confirmation system; verbal agreements can be forgotten", manualWork: "Phone tag, multiple calls per shift", dataGap: "No centralized record of assignment status", controlWeakness: "No documented acceptance process" },
  { step: 3, name: "Shift Confirmation", actor: "Scheduling Coordinator / Caregiver", input: "Assigned shift details", action: "Caregiver verbally confirms or does not respond", output: "Confirmed (or assumed) shift coverage", channel: "Phone call, text message", delay: "Confirmation often received after deadline", failurePoint: "Assumed confirmation if no response received", manualWork: "Manual confirmation tracking", dataGap: "No confirmation timestamp or record", controlWeakness: "No systematic confirmation before shift start" },
  { step: 4, name: "Late-Arrival Detection", actor: "Caregiver / Care Coordinator", input: "Shift start time, actual arrival time", action: "Caregiver may call if running late; coordinator may notice absence", output: "Informal late notification", channel: "Phone call, text message", delay: "Late notification often received after shift should have started", failurePoint: "No automated detection or threshold tracking", manualWork: "Waiting and wondering", dataGap: "No arrival time data collected", controlWeakness: "No standard definition of 'late'" },
  { step: 5, name: "Missed-Shift Discovery", actor: "Client, Care Coordinator, or Caregiver", input: "Missing caregiver at client location", action: "Client calls office; coordinator discovers absence", output: "Emergency gap notification", channel: "Phone call from client or caregiver", delay: "Discovered reactively after shift start time", failurePoint: "No pre-shift confirmation check", manualWork: "Emergency scrambling to find replacement", dataGap: "No record of missed shift frequency or patterns", controlWeakness: "No preventive screening before shift" },
  { step: 6, name: "Escalation", actor: "Care Coordinator / Operations Manager", input: "Issue notification (missed shift, late arrival, complaint)", action: "Pass issue to next person via phone or email", output: "Issue handed off", channel: "Phone, email, text", delay: "Dependent on recipient availability", failurePoint: "No documented escalation path or severity levels", manualWork: "Multiple handoffs before reaching decision-maker", dataGap: "No escalation history or timeline", controlWeakness: "No audit trail of escalation decisions" },
  { step: 7, name: "Replacement Search", actor: "Scheduling Coordinator", input: "Open shift that needs coverage", action: "Call alternative caregivers to fill gap", output: "Replacement caregiver or unfilled gap", channel: "Phone, text", delay: "Significant — each call takes time, no guarantee of success", failurePoint: "No backup caregiver list or pre-qualified replacements", manualWork: "Entirely manual search process", dataGap: "No record of replacement success rate or time-to-fill", controlWeakness: "No defined process for when replacement cannot be found" },
  { step: 8, name: "Client Communication", actor: "Client Services Rep / Care Coordinator", input: "Change in schedule or caregiver", action: "Call client to inform of change", output: "Verbal or message notification", channel: "Phone call, voicemail", delay: "Communication may happen after caregiver was due", failurePoint: "Client may not receive notification before shift", manualWork: "Manual dialing, leaving messages, call-backs", dataGap: "No record of whether client was notified", controlWeakness: "No confirmation that client received the message" },
  { step: 9, name: "Service Documentation", actor: "Caregiver", input: "Shift details, services provided", action: "Complete paper or digital documentation after shift", output: "Documentation record", channel: "Paper form, basic digital form", delay: "Completion varies from immediately to days later", failurePoint: "No tracking of documentation status or completion rate", manualWork: "Paper forms need manual data entry", dataGap: "No visibility into documentation completion", controlWeakness: "No enforcement of documentation deadlines" },
  { step: 10, name: "Follow-Up", actor: "Care Coordinator / Operations Manager", input: "Issue that was resolved or escalated", action: "Check back on issue if time permits", output: "Verbal status update", channel: "Phone, email", delay: "Follow-up is ad-hoc, if done at all", failurePoint: "No scheduled follow-up or ownership assignment", manualWork: "Remembering to follow up with no system prompts", dataGap: "No follow-up status or completion tracking", controlWeakness: "No verification that issues are closed" },
  { step: 11, name: "Management Reporting", actor: "Operations Manager", input: "Scattered data from spreadsheets, emails, phone notes", action: "Manually compile operational summary", output: "Verbal or written status update", channel: "Email, meeting", delay: "Report may be weeks out of date", failurePoint: "Manual compilation is time-consuming and error-prone", manualWork: "Data gathering, reconciliation, formatting", dataGap: "No real-time metrics; no historical trends", controlWeakness: "No standardized report format or metrics" },
];

// Future-state improvements
export interface FutureStateImprovement {
  area: string;
  currentState: string;
  futureState: string;
  brLink: string;
  kpiLink: string;
  expectedOutcome: string;
}

export const futureStateImprovements: FutureStateImprovement[] = [
  { area: "Shift Status", currentState: "Manual spreadsheets", futureState: "Real-time dashboard with status indicators", brLink: "BR-001", kpiLink: "KPI-001", expectedOutcome: "Proactive identification of at-risk shifts before client impact" },
  { area: "Gap Detection", currentState: "Reactive discovery after shift start", futureState: "Proactive alerts for unconfirmed and unassigned shifts", brLink: "BR-002", kpiLink: "KPI-006", expectedOutcome: "Earlier gap identification, reduced missed shifts" },
  { area: "Escalation", currentState: "Informal phone/email with no audit trail", futureState: "Structured escalation with severity levels, ownership, and timeline", brLink: "BR-003", kpiLink: "KPI-004", expectedOutcome: "Faster resolution, clear accountability, audit trail" },
  { area: "Documentation", currentState: "No tracking of documentation status", futureState: "Status dashboard with automated reminders and deadlines", brLink: "BR-005", kpiLink: "KPI-005", expectedOutcome: "Improved compliance, reduced billing delays" },
  { area: "Issue Follow-Up", currentState: "Ad-hoc follow-up, if done at all", futureState: "Assigned ownership with deadlines and completion tracking", brLink: "BR-004", kpiLink: "KPI-008", expectedOutcome: "Higher issue resolution rates, pattern identification" },
  { area: "Reporting", currentState: "Manual compilation, weeks out of date", futureState: "Automated KPI dashboard with trend views", brLink: "BR-008", kpiLink: "KPI-001 through KPI-008", expectedOutcome: "Data-driven decision-making, trend identification" },
  { area: "Audit Trail", currentState: "None — no record of operational actions", futureState: "System-generated logs with timestamp and user attribution", brLink: "BR-010", kpiLink: "KPI-005 (indirect)", expectedOutcome: "Compliance readiness, event reconstruction capability" },
  { area: "Client Communication", currentState: "Phone calls only, no delivery confirmation", futureState: "Structured notifications with delivery tracking", brLink: "BR-007", kpiLink: "KPI-001 (indirect)", expectedOutcome: "Improved client satisfaction, fewer inquiries" },
];
