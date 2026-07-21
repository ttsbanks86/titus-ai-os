// BA Compass — KPI Calculation Engine
// =======================================
// Pure functions matching docs/18-kpi-dictionary.md
// All formulas verified against the KPI dictionary.
// No side effects — deterministic results.

import type { KpiInput, KpiStatus } from "@/types";
import {
  KPI_TARGETS,
  KPI_WARNINGS,
  LATE_ARRIVAL_THRESHOLD_MINUTES,
} from "@/lib/constants";

// ─── Helpers ───────────────────────────────────────────────

/**
 * Safe percentage calculation. Returns 0 when denominator is 0.
 */
function safePercent(numerator: number, denominator: number): number {
  if (denominator === 0) return 0;
  return Math.round((numerator / denominator) * 1000) / 10; // One decimal place
}

/**
 * Safe average calculation. Returns 0 when count is 0.
 */
function safeAverage(sum: number, count: number): number {
  if (count === 0) return 0;
  return Math.round((sum / count) * 10) / 10; // One decimal place
}

/**
 * Classify a KPI where higher is better.
 */
function statusHigherIsBetter(
  actual: number,
  target: number,
  warningThreshold: number
): KpiStatus {
  if (actual >= target) return "on_track";
  if (actual >= warningThreshold) return "warning";
  return "critical";
}

/**
 * Classify a KPI where lower is better.
 */
function statusLowerIsBetter(
  actual: number,
  target: number,
  warningThreshold: number
): KpiStatus {
  if (actual <= target) return "on_track";
  if (actual <= warningThreshold) return "warning";
  return "critical";
}

// ─── KPI Functions ─────────────────────────────────────────

/**
 * KPI-001: Shift Fill Rate
 * Formula: (Confirmed Shifts / Total Scheduled Shifts) x 100
 * Target: >= 95%  Warning: < 90%
 * Unit: Percentage
 * Higher is better.
 */
export function calculateShiftFillRate(data: KpiInput): {
  value: number;
  status: KpiStatus;
} {
  const value = safePercent(data.confirmedShifts, data.totalScheduledShifts);
  const status = statusHigherIsBetter(
    value,
    KPI_TARGETS.SHIFT_FILL_RATE,
    KPI_WARNINGS.SHIFT_FILL_RATE
  );
  return { value, status };
}

/**
 * KPI-002: Missed Shift Rate
 * Formula: (Missed Shifts / Total Scheduled Shifts) x 100
 * Target: < 2%  Warning: > 5%
 * Unit: Percentage
 * Lower is better.
 */
export function calculateMissedShiftRate(data: KpiInput): {
  value: number;
  status: KpiStatus;
} {
  const value = safePercent(data.missedShifts, data.totalScheduledShifts);
  const status = statusLowerIsBetter(
    value,
    KPI_TARGETS.MISSED_SHIFT_RATE,
    KPI_WARNINGS.MISSED_SHIFT_RATE
  );
  return { value, status };
}

/**
 * KPI-003: Late Arrival Rate
 * Formula: (Late Arrivals / Total Completed Shifts) x 100
 * Late defined as arrival > 15 min after scheduled start.
 * Target: < 10%  Warning: > 15%
 * Unit: Percentage
 * Lower is better.
 */
export function calculateLateArrivalRate(data: KpiInput): {
  value: number;
  status: KpiStatus;
} {
  const value = safePercent(data.lateArrivals, data.completedShifts);
  const status = statusLowerIsBetter(
    value,
    KPI_TARGETS.LATE_ARRIVAL_RATE,
    KPI_WARNINGS.LATE_ARRIVAL_RATE
  );
  return { value, status };
}

/**
 * KPI-004: Average Escalation Time
 * Formula: SUM(Escalation Time - Identification Time) / Total Escalated Issues
 * Target: < 30 min  Warning: > 60 min
 * Unit: Minutes
 * Lower is better.
 */
export function calculateAverageEscalationTime(data: KpiInput): {
  value: number;
  status: KpiStatus;
} {
  const value = safeAverage(data.sumEscalationMinutes, data.totalEscalations);
  const status = statusLowerIsBetter(
    value,
    KPI_TARGETS.AVG_ESCALATION_TIME,
    KPI_WARNINGS.AVG_ESCALATION_TIME
  );
  return { value, status };
}

/**
 * KPI-005: Documentation Completion Rate
 * Formula: (Shifts with Documentation Completed / Total Completed Shifts Requiring Docs) x 100
 * Target: >= 95%  Warning: < 85%
 * Unit: Percentage
 * Higher is better.
 */
export function calculateDocumentationCompletionRate(
  completedShifts: number,
  totalShiftsRequiringDocs: number
): { value: number; status: KpiStatus } {
  const value = safePercent(completedShifts, totalShiftsRequiringDocs);
  const status = statusHigherIsBetter(
    value,
    KPI_TARGETS.DOC_COMPLETION_RATE,
    KPI_WARNINGS.DOC_COMPLETION_RATE
  );
  return { value, status };
}

/**
 * KPI-006: Open Staffing Gaps
 * Formula: Count of unassigned shifts within next 48 hours
 * Target: < 3  Warning: > 5
 * Unit: Count (integer)
 * Lower is better.
 */
export function calculateOpenStaffingGaps(data: KpiInput): {
  value: number;
  status: KpiStatus;
} {
  const value = data.openGaps;
  const status = statusLowerIsBetter(
    value,
    KPI_TARGETS.OPEN_STAFFING_GAPS,
    KPI_WARNINGS.OPEN_STAFFING_GAPS
  );
  return { value, status };
}

/**
 * KPI-007: Issue Resolution Time
 * Formula: SUM(Resolution Time) / Total Resolved Issues
 * Target: < 4 hours  Warning: > 8 hours
 * Unit: Hours
 * Lower is better.
 */
export function calculateIssueResolutionTime(data: KpiInput): {
  value: number;
  status: KpiStatus;
} {
  const value = safeAverage(data.sumResolutionHours, data.totalResolvedIssues);
  const status = statusLowerIsBetter(
    value,
    KPI_TARGETS.ISSUE_RESOLUTION_TIME,
    KPI_WARNINGS.ISSUE_RESOLUTION_TIME
  );
  return { value, status };
}

/**
 * KPI-008: Follow-Up Completion Rate
 * Formula: (Completed Follow-Ups / Required Follow-Ups) x 100
 * Target: >= 90%  Warning: < 75%
 * Unit: Percentage
 * Higher is better.
 */
export function calculateFollowUpCompletionRate(data: KpiInput): {
  value: number;
  status: KpiStatus;
} {
  const value = safePercent(data.completedFollowUps, data.requiredFollowUps);
  const status = statusHigherIsBetter(
    value,
    KPI_TARGETS.FOLLOW_UP_COMPLETION_RATE,
    KPI_WARNINGS.FOLLOW_UP_COMPLETION_RATE
  );
  return { value, status };
}

// ─── All KPIs ──────────────────────────────────────────────

export interface AllKpiResults {
  shiftFillRate: ReturnType<typeof calculateShiftFillRate>;
  missedShiftRate: ReturnType<typeof calculateMissedShiftRate>;
  lateArrivalRate: ReturnType<typeof calculateLateArrivalRate>;
  averageEscalationTime: ReturnType<typeof calculateAverageEscalationTime>;
  documentationCompletionRate: ReturnType<typeof calculateDocumentationCompletionRate>;
  openStaffingGaps: ReturnType<typeof calculateOpenStaffingGaps>;
  issueResolutionTime: ReturnType<typeof calculateIssueResolutionTime>;
  followUpCompletionRate: ReturnType<typeof calculateFollowUpCompletionRate>;
}

/**
 * Calculate all 8 KPIs from a single data input.
 */
export function calculateAllKpis(
  data: KpiInput,
  docCompleted: number,
  docRequired: number
): AllKpiResults {
  return {
    shiftFillRate: calculateShiftFillRate(data),
    missedShiftRate: calculateMissedShiftRate(data),
    lateArrivalRate: calculateLateArrivalRate(data),
    averageEscalationTime: calculateAverageEscalationTime(data),
    documentationCompletionRate: calculateDocumentationCompletionRate(
      docCompleted,
      docRequired
    ),
    openStaffingGaps: calculateOpenStaffingGaps(data),
    issueResolutionTime: calculateIssueResolutionTime(data),
    followUpCompletionRate: calculateFollowUpCompletionRate(data),
  };
}
