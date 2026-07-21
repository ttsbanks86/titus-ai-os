// BA Compass — KPI Input Aggregator
// Aggregates synthetic data into KPI input structure for calculations.
// DISCLAIMER: All data is fictional.

import type { KpiInput, Shift } from "@/types";
import { shifts } from "./shifts";
import { escalations } from "./escalations";
import { documentationRecords } from "./documentation";
import { serviceIssues } from "./issues";
import { followUpRecords } from "./followups";

/**
 * Calculates the difference in minutes between two ISO datetime strings.
 * Returns 0 if either value is null.
 */
function minutesBetween(start: string, end: string): number {
  const ms = new Date(end).getTime() - new Date(start).getTime();
  return Math.max(0, Math.round(ms / 60000));
}

/**
 * Calculates the difference in hours between two ISO datetime strings.
 * Returns 0 if either value is null.
 */
function hoursBetween(start: string, end: string | null): number {
  if (!end) return 0;
  const ms = new Date(end).getTime() - new Date(start).getTime();
  return Math.max(0, Math.round((ms / 3600000) * 10) / 10);
}

/**
 * Aggregates all synthetic data into a KpiInput structure.
 * Only counts completed shifts for KPI denominators that require finalized data.
 */
export function getAllShiftData(): KpiInput {
  // Total scheduled shifts (all statuses except cancelled)
  const totalScheduled = shifts.filter((s) => s.status !== "cancelled").length;

  // Confirmed shifts (confirmed or better status, with caregiver)
  const confirmed = shifts.filter(
    (s) => s.caregiverId !== null && s.status !== "unconfirmed"
  ).length;

  // Missed shifts
  const missed = shifts.filter((s) => s.status === "missed").length;

  // Completed shifts (with actual arrival)
  const completed = shifts.filter(
    (s) => s.status === "completed" && s.actualArrival !== null
  ).length;

  // Late arrivals among completed shifts
  const late = shifts.filter((s) => s.status === "completed" && s.isLate === true).length;

  // Escalations: total and sum of escalation times
  const resolvedEscalations = escalations.filter(
    (e) => e.escalationTime !== null && e.status !== "open"
  );
  const totalEscalations = resolvedEscalations.length;
  const sumEscalationMinutes = resolvedEscalations.reduce((sum, e) => {
    return sum + minutesBetween(e.identifiedTime, e.escalationTime!);
  }, 0);

  // Documentation completion (among completed shifts that require docs)
  const completedShiftIds = new Set(
    shifts
      .filter((s) => s.status === "completed" && s.documentationStatus !== "not_required")
      .map((s) => s.shiftId)
  );
  const shiftsWithDocComplete = Array.from(completedShiftIds).filter((id) => {
    const doc = documentationRecords.find((d) => d.shiftId === id);
    return doc && doc.status === "complete";
  }).length;
  const totalShiftsRequiringDocs = completedShiftIds.size;

  // Open gaps (unconfirmed shifts in next 48h or with no caregiver)
  const openGaps = shifts.filter(
    (s) => s.caregiverId === null && s.status === "unconfirmed"
  ).length;

  // Issue resolution time
  const resolvedIssues = serviceIssues.filter(
    (iss) => iss.status === "resolved"
  );
  const totalResolvedIssues = resolvedIssues.length;
  const sumResolutionHours = resolvedIssues.reduce((sum, iss) => {
    // Use shift data for resolution estimate
    const shift = shifts.find((s) => s.shiftId === iss.shiftId);
    if (!shift) return sum;
    // Resolution time from issue report to shift completion or escalation resolve
    const escalation = escalations.find((e) => e.shiftId === iss.shiftId);
    if (escalation?.resolvedTime) {
      return sum + hoursBetween(iss.reportedTime, escalation.resolvedTime);
    }
    return sum + 1; // Default 1 hour if no resolution data
  }, 0);

  // Follow-up completion
  const requiredFollowUps = followUpRecords.length;
  const completedFollowUps = followUpRecords.filter(
    (f) => f.status === "completed"
  ).length;

  return {
    totalScheduledShifts: totalScheduled,
    confirmedShifts: confirmed,
    missedShifts: missed,
    completedShifts: completed,
    lateArrivals: late,
    totalEscalations,
    sumEscalationMinutes,
    shiftsWithDocComplete,
    openGaps,
    totalResolvedIssues,
    sumResolutionHours,
    requiredFollowUps,
    completedFollowUps,
  };
}

/**
 * Returns detailed counts for documentation rate calculation.
 */
export function getDocumentationCounts(): {
  completed: number;
  required: number;
} {
  const completedShiftIds = shifts
    .filter((s) => s.status === "completed" && s.documentationStatus !== "not_required")
    .map((s) => s.shiftId);

  const completed = completedShiftIds.filter((id) => {
    const doc = documentationRecords.find((d) => d.shiftId === id);
    return doc && doc.status === "complete";
  }).length;

  return {
    completed,
    required: completedShiftIds.length,
  };
}
