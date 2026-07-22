// BA Compass — Gap Analysis Content (from docs/08-pain-point-analysis.md)
// DISCLAIMER: All data is fictional.

export interface GapItem {
  dimension: string;
  problem: string;
  rootCause: string;
  impact: string;
  severity: "Critical" | "High" | "Medium";
  futureState: string;
  linkedBr: string;
}

export const gaps: GapItem[] = [
  { dimension: "People", problem: "Scheduling coordinator overload from manual phone calls", rootCause: "No centralized visibility into caregiver availability", impact: "High coordinator turnover risk, missed shifts due to coordinator capacity", severity: "High", futureState: "Centralized availability view and gap-alert system", linkedBr: "BR-001" },
  { dimension: "People", problem: "Client services frustration from inability to provide real-time status", rootCause: "No centralized operational status view", impact: "Client frustration, repeated callbacks, damaged relationships", severity: "High", futureState: "Operational status view accessible to client services", linkedBr: "BR-007" },
  { dimension: "People", problem: "Caregiver communication overload from inconsistent channels", rootCause: "No single communication method for schedule changes", impact: "Missed shifts, confusion, frustration", severity: "Medium", futureState: "Unified schedule notification system", linkedBr: "BR-007" },
  { dimension: "Process", problem: "No shift confirmation process before start time", rootCause: "No defined confirmation step in the scheduling workflow", impact: "Missed shifts discovered after client impact", severity: "Critical", futureState: "Pre-shift confirmation workflow with alerts", linkedBr: "BR-001" },
  { dimension: "Process", problem: "No standard escalation path for service issues", rootCause: "No escalation policy or severity classification", impact: "Delayed resolution, inconsistent handling, no audit trail", severity: "Critical", futureState: "Defined escalation paths with severity levels", linkedBr: "BR-003" },
  { dimension: "Process", problem: "No structured follow-up after issue resolution", rootCause: "No follow-up process or ownership assignment", impact: "Recurring issues not identified, client satisfaction drops", severity: "High", futureState: "Structured follow-up workflow with ownership and deadlines", linkedBr: "BR-004" },
  { dimension: "Technology", problem: "No centralized system — operations managed across spreadsheets, paper, phone, and email", rootCause: "No investment in operations management software", impact: "Data inconsistency, manual rework, lost information", severity: "Critical", futureState: "Centralized web application for operational visibility", linkedBr: "BR-006" },
  { dimension: "Technology", problem: "No KPI dashboard for management visibility", rootCause: "No data collection or reporting infrastructure", impact: "Reactive management, no trend identification, no early warning", severity: "Critical", futureState: "KPI dashboard with defined metrics and trend views", linkedBr: "BR-008" },
  { dimension: "Technology", problem: "No mobile access for field staff", rootCause: "No mobile-compatible system", impact: "Caregivers call office for basic schedule information", severity: "Medium", futureState: "Mobile-responsive web application", linkedBr: "BR-015" },
  { dimension: "Data", problem: "No attendance data collected systematically", rootCause: "No time-tracking or check-in process", impact: "Cannot measure lateness, cannot identify chronic late caregivers", severity: "High", futureState: "Arrival time tracking as part of shift documentation", linkedBr: "BR-011" },
  { dimension: "Data", problem: "No documentation completion tracking", rootCause: "No documentation status process", impact: "Compliance risk, billing delays, care continuity gaps", severity: "High", futureState: "Documentation status tracking with reminders", linkedBr: "BR-005" },
  { dimension: "Communication", problem: "Fragmented issue communication with no central record", rootCause: "No issue-tracking system", impact: "Information lost, clients repeat explanations, delayed resolution", severity: "High", futureState: "Centralized issue tracking with timeline and status", linkedBr: "BR-003" },
  { dimension: "Communication", problem: "No client notification confirmation", rootCause: "No notification tracking process", impact: "Clients not informed of changes, missed shifts", severity: "Medium", futureState: "Notification delivery tracking", linkedBr: "BR-007" },
  { dimension: "Governance", problem: "No defined operational policies", rootCause: "Informal management culture, no policy development", impact: "Inconsistent decisions, staff confusion, compliance risk", severity: "High", futureState: "Documented operational policies and procedures", linkedBr: "BR-009" },
  { dimension: "Governance", problem: "No audit trail for operational decisions", rootCause: "Informal communication channels, no documentation", impact: "Cannot reconstruct events, compliance exposure, liability risk", severity: "High", futureState: "System-generated audit trail for all operational actions", linkedBr: "BR-010" },
  { dimension: "Reporting", problem: "No operational dashboard or real-time metrics", rootCause: "No data collection or reporting infrastructure", impact: "Management flies blind, cannot identify trends", severity: "Critical", futureState: "KPI dashboard with trend views and export", linkedBr: "BR-008" },
  { dimension: "Reporting", problem: "No historical trend data available", rootCause: "Data is not collected in structured format over time", impact: "Cannot measure improvement or identify seasonal patterns", severity: "Medium", futureState: "Data persistence with time-series KPI tracking", linkedBr: "BR-008" },
  { dimension: "Risk", problem: "Compliance exposure from incomplete documentation", rootCause: "No documentation tracking or audit trail", impact: "Regulatory findings, billing audits, legal exposure", severity: "Critical", futureState: "Continuous documentation tracking with compliance reporting", linkedBr: "BR-005, BR-010" },
  { dimension: "Risk", problem: "Client churn risk from service failures", rootCause: "No systematic service recovery process", impact: "Revenue loss, reputation damage", severity: "High", futureState: "Structured service recovery and follow-up process", linkedBr: "BR-004" },
  { dimension: "Client Experience", problem: "Inconsistent care from missed shifts and late arrivals", rootCause: "Inadequate scheduling and gap-filling processes", impact: "Dissatisfaction, churn, negative word-of-mouth", severity: "Critical", futureState: "Reliability metrics, consistency tracking", linkedBr: "BR-001, BR-002" },
  { dimension: "Client Experience", problem: "Poor issue communication to clients", rootCause: "No client notification process", impact: "Frustration, distrust, churn", severity: "High", futureState: "Proactive notification system", linkedBr: "BR-007" },
];
