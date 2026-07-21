// BA Compass — Synthetic Follow-Up Record Data
// DISCLAIMER: All data is fictional.

import type { FollowUpRecord } from "@/types";

export const followUpRecords: FollowUpRecord[] = [
  {
    followupId: "FUP-001",
    issueId: "ISS-001",
    owner: "Coordinator A",
    deadline: "2026-07-17",
    completedTime: "2026-07-16T14:00:00Z",
    status: "completed",
    notes: "Client confirmed satisfaction with replacement caregiver",
  },
  {
    followupId: "FUP-002",
    issueId: "ISS-002",
    owner: "Coordinator B",
    deadline: "2026-07-16",
    completedTime: "2026-07-15T16:00:00Z",
    status: "completed",
    notes: "Caregiver counseled on arrival expectations",
  },
  {
    followupId: "FUP-003",
    issueId: "ISS-003",
    owner: "Coordinator A",
    deadline: "2026-07-18",
    completedTime: "2026-07-17T11:00:00Z",
    status: "completed",
    notes: "Client offered discount for inconvenience",
  },
  {
    followupId: "FUP-004",
    issueId: "ISS-004",
    owner: "Coordinator B",
    deadline: "2026-07-19",
    completedTime: null,
    status: "in_progress",
    notes: "Reviewing caregiver lateness pattern",
  },
  {
    followupId: "FUP-005",
    issueId: "ISS-005",
    owner: "Quality Assurance Lead",
    deadline: "2026-07-19",
    completedTime: null,
    status: "pending",
    notes: "Awaiting documentation submission",
  },
  {
    followupId: "FUP-006",
    issueId: "ISS-006",
    owner: "Coordinator A",
    deadline: "2026-07-19",
    completedTime: "2026-07-18T15:00:00Z",
    status: "completed",
    notes: "Both issues addressed — late arrival noted and documentation flagged",
  },
  {
    followupId: "FUP-007",
    issueId: "ISS-007",
    owner: "Coordinator B",
    deadline: "2026-07-20",
    completedTime: "2026-07-19T10:00:00Z",
    status: "completed",
    notes: "Client contacted and satisfied with follow-up",
  },
];
