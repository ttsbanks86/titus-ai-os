// BA Compass — KPI Calculation Unit Tests
// Formula source: docs/18-kpi-dictionary.md

import { describe, it, expect } from "vitest";
import type { KpiInput } from "@/types";
import {
  calculateShiftFillRate,
  calculateMissedShiftRate,
  calculateLateArrivalRate,
  calculateAverageEscalationTime,
  calculateDocumentationCompletionRate,
  calculateOpenStaffingGaps,
  calculateIssueResolutionTime,
  calculateFollowUpCompletionRate,
} from "@/lib/kpi/calculations";

// ─── Test Data Factory ─────────────────────────────────────

function makeKpiInput(overrides: Partial<KpiInput> = {}): KpiInput {
  return {
    totalScheduledShifts: 100,
    confirmedShifts: 90,
    missedShifts: 5,
    completedShifts: 85,
    lateArrivals: 8,
    totalEscalations: 10,
    sumEscalationMinutes: 250,
    shiftsWithDocComplete: 80,
    openGaps: 3,
    totalResolvedIssues: 10,
    sumResolutionHours: 30,
    requiredFollowUps: 20,
    completedFollowUps: 18,
    ...overrides,
  };
}

// ─── KPI-001: Shift Fill Rate ──────────────────────────────

describe("calculateShiftFillRate", () => {
  it("calculates standard rate correctly", () => {
    const data = makeKpiInput({ confirmedShifts: 95, totalScheduledShifts: 100 });
    const result = calculateShiftFillRate(data);
    expect(result.value).toBe(95);
    expect(result.status).toBe("on_track");
  });

  it("returns warning when below 90%", () => {
    const data = makeKpiInput({ confirmedShifts: 85, totalScheduledShifts: 100 });
    const result = calculateShiftFillRate(data);
    expect(result.value).toBe(85);
    expect(result.status).toBe("critical");
  });

  it("handles all shifts confirmed", () => {
    const data = makeKpiInput({ confirmedShifts: 50, totalScheduledShifts: 50 });
    const result = calculateShiftFillRate(data);
    expect(result.value).toBe(100);
    expect(result.status).toBe("on_track");
  });

  it("handles empty dataset (zero denominator)", () => {
    const data = makeKpiInput({ totalScheduledShifts: 0, confirmedShifts: 0 });
    const result = calculateShiftFillRate(data);
    expect(result.value).toBe(0);
    expect(result.status).toBe("critical");
  });

  it("rounds to one decimal place", () => {
    const data = makeKpiInput({ confirmedShifts: 1, totalScheduledShifts: 3 });
    const result = calculateShiftFillRate(data);
    expect(result.value).toBe(33.3);
  });
});

// ─── KPI-002: Missed Shift Rate ────────────────────────────

describe("calculateMissedShiftRate", () => {
  it("calculates standard rate correctly", () => {
    const data = makeKpiInput({ missedShifts: 1, totalScheduledShifts: 100 });
    const result = calculateMissedShiftRate(data);
    expect(result.value).toBe(1);
    expect(result.status).toBe("on_track");
  });

  it("flags warning when above 5%", () => {
    const data = makeKpiInput({ missedShifts: 8, totalScheduledShifts: 100 });
    const result = calculateMissedShiftRate(data);
    expect(result.value).toBe(8);
    expect(result.status).toBe("critical");
  });

  it("returns zero when no missed shifts", () => {
    const data = makeKpiInput({ missedShifts: 0, totalScheduledShifts: 50 });
    const result = calculateMissedShiftRate(data);
    expect(result.value).toBe(0);
    expect(result.status).toBe("on_track");
  });

  it("handles zero denominator", () => {
    const data = makeKpiInput({ totalScheduledShifts: 0, missedShifts: 0 });
    const result = calculateMissedShiftRate(data);
    expect(result.value).toBe(0);
  });
});

// ─── KPI-003: Late Arrival Rate ───────────────────────────

describe("calculateLateArrivalRate", () => {
  it("calculates standard rate correctly", () => {
    const data = makeKpiInput({ lateArrivals: 5, completedShifts: 100 });
    const result = calculateLateArrivalRate(data);
    expect(result.value).toBe(5);
    expect(result.status).toBe("on_track");
  });

  it("flags warning above 15%", () => {
    const data = makeKpiInput({ lateArrivals: 20, completedShifts: 100 });
    const result = calculateLateArrivalRate(data);
    expect(result.value).toBe(20);
    expect(result.status).toBe("critical");
  });

  it("returns zero when no late arrivals", () => {
    const data = makeKpiInput({ lateArrivals: 0, completedShifts: 50 });
    const result = calculateLateArrivalRate(data);
    expect(result.value).toBe(0);
    expect(result.status).toBe("on_track");
  });

  it("handles zero completed shifts", () => {
    const data = makeKpiInput({ completedShifts: 0, lateArrivals: 0 });
    const result = calculateLateArrivalRate(data);
    expect(result.value).toBe(0);
  });

  it("handles all late arrivals", () => {
    const data = makeKpiInput({ lateArrivals: 30, completedShifts: 30 });
    const result = calculateLateArrivalRate(data);
    expect(result.value).toBe(100);
    expect(result.status).toBe("critical");
  });
});

// ─── KPI-004: Average Escalation Time ─────────────────────

describe("calculateAverageEscalationTime", () => {
  it("calculates average correctly", () => {
    const data = makeKpiInput({ sumEscalationMinutes: 150, totalEscalations: 10 });
    const result = calculateAverageEscalationTime(data);
    expect(result.value).toBe(15);
    expect(result.status).toBe("on_track");
  });

  it("flags warning when above 60 minutes", () => {
    const data = makeKpiInput({ sumEscalationMinutes: 700, totalEscalations: 10 });
    const result = calculateAverageEscalationTime(data);
    expect(result.value).toBe(70);
    expect(result.status).toBe("critical");
  });

  it("returns zero for no escalations", () => {
    const data = makeKpiInput({ totalEscalations: 0, sumEscalationMinutes: 0 });
    const result = calculateAverageEscalationTime(data);
    expect(result.value).toBe(0);
    expect(result.status).toBe("on_track");
  });

  it("handles single escalation", () => {
    const data = makeKpiInput({ sumEscalationMinutes: 25, totalEscalations: 1 });
    const result = calculateAverageEscalationTime(data);
    expect(result.value).toBe(25);
    expect(result.status).toBe("on_track");
  });
});

// ─── KPI-005: Documentation Completion Rate ────────────────

describe("calculateDocumentationCompletionRate", () => {
  it("calculates standard rate correctly", () => {
    const result = calculateDocumentationCompletionRate(95, 100);
    expect(result.value).toBe(95);
    expect(result.status).toBe("on_track");
  });

  it("flags warning below 85%", () => {
    const result = calculateDocumentationCompletionRate(70, 100);
    expect(result.value).toBe(70);
    expect(result.status).toBe("critical");
  });

  it("returns 100% when all complete", () => {
    const result = calculateDocumentationCompletionRate(50, 50);
    expect(result.value).toBe(100);
    expect(result.status).toBe("on_track");
  });

  it("handles zero required", () => {
    const result = calculateDocumentationCompletionRate(0, 0);
    expect(result.value).toBe(0);
  });

  it("handles no completed docs", () => {
    const result = calculateDocumentationCompletionRate(0, 50);
    expect(result.value).toBe(0);
    expect(result.status).toBe("critical");
  });
});

// ─── KPI-006: Open Staffing Gaps ─────────────────────────

describe("calculateOpenStaffingGaps", () => {
  it("reports gap count correctly", () => {
    const data = makeKpiInput({ openGaps: 2 });
    const result = calculateOpenStaffingGaps(data);
    expect(result.value).toBe(2);
    expect(result.status).toBe("on_track");
  });

  it("flags warning when above 5", () => {
    const data = makeKpiInput({ openGaps: 7 });
    const result = calculateOpenStaffingGaps(data);
    expect(result.value).toBe(7);
    expect(result.status).toBe("critical");
  });

  it("returns zero when no gaps", () => {
    const data = makeKpiInput({ openGaps: 0 });
    const result = calculateOpenStaffingGaps(data);
    expect(result.value).toBe(0);
    expect(result.status).toBe("on_track");
  });
});

// ─── KPI-007: Issue Resolution Time ───────────────────────

describe("calculateIssueResolutionTime", () => {
  it("calculates average resolution time correctly", () => {
    const data = makeKpiInput({ sumResolutionHours: 20, totalResolvedIssues: 10 });
    const result = calculateIssueResolutionTime(data);
    expect(result.value).toBe(2);
    expect(result.status).toBe("on_track");
  });

  it("flags warning when above 8 hours", () => {
    const data = makeKpiInput({ sumResolutionHours: 90, totalResolvedIssues: 10 });
    const result = calculateIssueResolutionTime(data);
    expect(result.value).toBe(9);
    expect(result.status).toBe("critical");
  });

  it("handles zero resolved issues", () => {
    const data = makeKpiInput({ totalResolvedIssues: 0, sumResolutionHours: 0 });
    const result = calculateIssueResolutionTime(data);
    expect(result.value).toBe(0);
  });

  it("handles single issue with quick resolution", () => {
    const data = makeKpiInput({ sumResolutionHours: 1.5, totalResolvedIssues: 1 });
    const result = calculateIssueResolutionTime(data);
    expect(result.value).toBe(1.5);
    expect(result.status).toBe("on_track");
  });
});

// ─── KPI-008: Follow-Up Completion Rate ────────────────────

describe("calculateFollowUpCompletionRate", () => {
  it("calculates standard rate correctly", () => {
    const data = makeKpiInput({ completedFollowUps: 18, requiredFollowUps: 20 });
    const result = calculateFollowUpCompletionRate(data);
    expect(result.value).toBe(90);
    expect(result.status).toBe("on_track");
  });

  it("flags warning below 75%", () => {
    const data = makeKpiInput({ completedFollowUps: 10, requiredFollowUps: 20 });
    const result = calculateFollowUpCompletionRate(data);
    expect(result.value).toBe(50);
    expect(result.status).toBe("critical");
  });

  it("returns 100% when all completed", () => {
    const data = makeKpiInput({ completedFollowUps: 15, requiredFollowUps: 15 });
    const result = calculateFollowUpCompletionRate(data);
    expect(result.value).toBe(100);
    expect(result.status).toBe("on_track");
  });

  it("handles zero required", () => {
    const data = makeKpiInput({ requiredFollowUps: 0, completedFollowUps: 0 });
    const result = calculateFollowUpCompletionRate(data);
    expect(result.value).toBe(0);
  });
});
