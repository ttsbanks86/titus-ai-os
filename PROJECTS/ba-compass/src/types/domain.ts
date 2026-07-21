// BA Compass — Domain Types
// Matches docs/19-data-dictionary.md (BrightCare Home Services — Fictional)

// ─── Shift Status ───────────────────────────────────────────
export type ShiftStatus =
  | "confirmed"
  | "unconfirmed"
  | "in_progress"
  | "completed"
  | "missed"
  | "cancelled";

// ─── Documentation Status ───────────────────────────────────
export type DocumentationStatus =
  | "complete"
  | "incomplete"
  | "not_required"
  | "overdue";

// ─── Assignment Method ──────────────────────────────────────
export type AssignmentMethod = "auto" | "manual" | "replacement";

// ─── Issue / Escalation Types ───────────────────────────────
export type IssueType =
  | "missed_shift"
  | "late_arrival"
  | "no_show"
  | "client_complaint"
  | "documentation_missing";

export type SeverityLevel = "low" | "medium" | "high" | "critical";

export type IssueStatus = "open" | "in_progress" | "resolved" | "closed";

// ─── Follow-Up ──────────────────────────────────────────────
export type FollowUpStatus = "pending" | "in_progress" | "completed";

// ─── Caregiver Status ───────────────────────────────────────
export type CaregiverStatus = "active" | "on_leave" | "inactive";

export type AvailabilityPattern = "full_time" | "part_time" | "weekend_only";

// ─── Client Account ─────────────────────────────────────────
export type CareLevel = "companion" | "personal" | "specialized";

export type AccountStatus = "active" | "inactive" | "pending";

// ─── Shift ──────────────────────────────────────────────────
export interface Shift {
  shiftId: string;
  clientId: string;
  caregiverId: string | null;
  scheduledDate: string; // ISO date YYYY-MM-DD
  scheduledStart: string; // HH:mm
  scheduledEnd: string; // HH:mm
  status: ShiftStatus;
  confirmationTime: string | null; // ISO datetime
  actualArrival: string | null; // HH:mm
  documentationStatus: DocumentationStatus;
  documentationTime: string | null; // ISO datetime
  isLate: boolean;
  notes: string | null;
}

// ─── Caregiver ──────────────────────────────────────────────
export interface Caregiver {
  caregiverId: string;
  firstName: string;
  lastName: string;
  status: CaregiverStatus;
  availability: AvailabilityPattern;
  preferredRegion: string;
  activeClients: number;
}

// ─── Client Account ─────────────────────────────────────────
export interface ClientAccount {
  clientId: string;
  firstName: string;
  lastName: string;
  region: string;
  careLevel: CareLevel;
  status: AccountStatus;
  preferredCaregiverId: string | null;
}

// ─── Assignment ─────────────────────────────────────────────
export interface Assignment {
  assignmentId: string;
  shiftId: string;
  caregiverId: string;
  assignedTime: string; // ISO datetime
  assignmentMethod: AssignmentMethod;
  confirmed: boolean;
}

// ─── Escalation ─────────────────────────────────────────────
export interface Escalation {
  escalationId: string;
  shiftId: string;
  issueType: IssueType;
  severity: SeverityLevel;
  identifiedTime: string; // ISO datetime
  escalationTime: string | null; // ISO datetime
  resolvedTime: string | null; // ISO datetime
  status: IssueStatus;
  owner: string;
  resolutionNotes: string | null;
}

// ─── Documentation Record ───────────────────────────────────
export interface DocumentationRecord {
  docId: string;
  shiftId: string;
  caregiverId: string;
  submittedTime: string; // ISO datetime
  status: DocumentationStatus;
  serviceSummary: string | null;
}

// ─── Service Issue ──────────────────────────────────────────
export interface ServiceIssue {
  issueId: string;
  shiftId: string;
  reportedBy: string;
  reportedTime: string; // ISO datetime
  description: string;
  category: string;
  status: IssueStatus;
}

// ─── Follow-Up Record ───────────────────────────────────────
export interface FollowUpRecord {
  followupId: string;
  issueId: string;
  owner: string;
  deadline: string; // ISO date
  completedTime: string | null; // ISO datetime
  status: FollowUpStatus;
  notes: string | null;
}
