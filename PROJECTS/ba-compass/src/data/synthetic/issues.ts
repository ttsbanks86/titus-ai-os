// BA Compass — Synthetic Service Issue Data
// DISCLAIMER: All data is fictional.

import type { ServiceIssue } from "@/types";

export const serviceIssues: ServiceIssue[] = [
  {
    issueId: "ISS-001",
    shiftId: "SH-008",
    reportedBy: "Client Services Desk",
    reportedTime: "2026-07-15T09:15:00Z",
    description: "Caregiver did not arrive for scheduled shift. Client called office at 9:15 AM.",
    category: "attendance",
    status: "resolved",
  },
  {
    issueId: "ISS-002",
    shiftId: "SH-003",
    reportedBy: "Client Services Desk",
    reportedTime: "2026-07-14T09:20:00Z",
    description: "Caregiver arrived 20 minutes late. Client reported on-time arrival expectation.",
    category: "attendance",
    status: "resolved",
  },
  {
    issueId: "ISS-003",
    shiftId: "SH-014",
    reportedBy: "Coordinator B",
    reportedTime: "2026-07-16T13:15:00Z",
    description: "Caregiver did not arrive and did not respond to calls. Client left without care.",
    category: "attendance",
    status: "resolved",
  },
  {
    issueId: "ISS-004",
    shiftId: "SH-011",
    reportedBy: "Client Services Desk",
    reportedTime: "2026-07-16T09:20:00Z",
    description: "Caregiver arrived 15 minutes late. Client concerned about recurring lateness.",
    category: "attendance",
    status: "open",
  },
  {
    issueId: "ISS-005",
    shiftId: "SH-009",
    reportedBy: "Quality Assurance Lead",
    reportedTime: "2026-07-16T10:00:00Z",
    description: "Documentation not submitted for shift completed on 2026-07-15.",
    category: "documentation",
    status: "open",
  },
  {
    issueId: "ISS-006",
    shiftId: "SH-018",
    reportedBy: "Coordinator A",
    reportedTime: "2026-07-17T09:50:00Z",
    description: "Late arrival and documentation not yet submitted.",
    category: "attendance",
    status: "resolved",
  },
  {
    issueId: "ISS-007",
    shiftId: "SH-024",
    reportedBy: "Client Services Desk",
    reportedTime: "2026-07-18T13:30:00Z",
    description: "Caregiver arrived 25 minutes late. Client expressed dissatisfaction.",
    category: "attendance",
    status: "resolved",
  },
];
