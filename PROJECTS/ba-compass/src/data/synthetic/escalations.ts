// BA Compass — Synthetic Escalation Data
// DISCLAIMER: All data is fictional.

import type { Escalation } from "@/types";

export const escalations: Escalation[] = [
  // Escalation for missed shift SH-008
  {
    escalationId: "ESC-001",
    shiftId: "SH-008",
    issueType: "missed_shift",
    severity: "high",
    identifiedTime: "2026-07-15T09:15:00Z",
    escalationTime: "2026-07-15T09:30:00Z",
    resolvedTime: "2026-07-15T11:00:00Z",
    status: "resolved",
    owner: "Coordinator A",
    resolutionNotes: "Replacement caregiver CG-008 dispatched",
  },
  // Escalation for late arrival SH-003
  {
    escalationId: "ESC-002",
    shiftId: "SH-003",
    issueType: "late_arrival",
    severity: "low",
    identifiedTime: "2026-07-14T09:25:00Z",
    escalationTime: "2026-07-14T09:40:00Z",
    resolvedTime: "2026-07-14T10:00:00Z",
    status: "resolved",
    owner: "Coordinator B",
    resolutionNotes: "Caregiver arrived, client notified",
  },
  // Escalation for missed shift SH-014
  {
    escalationId: "ESC-003",
    shiftId: "SH-014",
    issueType: "no_show",
    severity: "critical",
    identifiedTime: "2026-07-16T13:15:00Z",
    escalationTime: null, // Delayed escalation
    resolvedTime: "2026-07-16T14:30:00Z",
    status: "resolved",
    owner: "Coordinator A",
    resolutionNotes: "Emergency replacement sent, client apologized to",
  },
  // Escalation for late arrival SH-011
  {
    escalationId: "ESC-004",
    shiftId: "SH-011",
    issueType: "late_arrival",
    severity: "medium",
    identifiedTime: "2026-07-16T09:20:00Z",
    escalationTime: "2026-07-16T09:45:00Z",
    resolvedTime: null, // Not yet resolved
    status: "open",
    owner: "Coordinator B",
    resolutionNotes: null,
  },
  // Escalation for late arrival SH-018
  {
    escalationId: "ESC-005",
    shiftId: "SH-018",
    issueType: "late_arrival",
    severity: "medium",
    identifiedTime: "2026-07-17T09:50:00Z",
    escalationTime: "2026-07-17T10:15:00Z",
    resolvedTime: "2026-07-17T11:30:00Z",
    status: "resolved",
    owner: "Coordinator A",
    resolutionNotes: "Caregiver arrived, documentation flagged for follow-up",
  },
  // Escalation for late arrival SH-024
  {
    escalationId: "ESC-006",
    shiftId: "SH-024",
    issueType: "late_arrival",
    severity: "medium",
    identifiedTime: "2026-07-18T13:30:00Z",
    escalationTime: "2026-07-18T13:50:00Z",
    resolvedTime: "2026-07-18T14:15:00Z",
    status: "resolved",
    owner: "Coordinator B",
    resolutionNotes: "Client notified, care extended to cover full hours",
  },
];
