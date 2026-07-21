// BA Compass — Synthetic Client Account Data
// DISCLAIMER: All names are fictional.

import type { ClientAccount } from "@/types";

export const clients: ClientAccount[] = [
  {
    clientId: "CL-001",
    firstName: "Client",
    lastName: "A",
    region: "Northside",
    careLevel: "personal",
    status: "active",
    preferredCaregiverId: "CG-001",
  },
  {
    clientId: "CL-002",
    firstName: "Client",
    lastName: "B",
    region: "Northside",
    careLevel: "companion",
    status: "active",
    preferredCaregiverId: null,
  },
  {
    clientId: "CL-003",
    firstName: "Client",
    lastName: "C",
    region: "Southside",
    careLevel: "specialized",
    status: "active",
    preferredCaregiverId: "CG-003",
  },
  {
    clientId: "CL-004",
    firstName: "Client",
    lastName: "D",
    region: "Eastside",
    careLevel: "personal",
    status: "active",
    preferredCaregiverId: "CG-004",
  },
  {
    clientId: "CL-005",
    firstName: "Client",
    lastName: "E",
    region: "Westside",
    careLevel: "companion",
    status: "active",
    preferredCaregiverId: null,
  },
  {
    clientId: "CL-006",
    firstName: "Client",
    lastName: "F",
    region: "Northside",
    careLevel: "personal",
    status: "active",
    preferredCaregiverId: "CG-006",
  },
  {
    clientId: "CL-007",
    firstName: "Client",
    lastName: "G",
    region: "Southside",
    careLevel: "companion",
    status: "inactive",
    preferredCaregiverId: null,
  },
  {
    clientId: "CL-008",
    firstName: "Client",
    lastName: "H",
    region: "Eastside",
    careLevel: "personal",
    status: "active",
    preferredCaregiverId: "CG-008",
  },
];
