// BA Compass — KPI Types

export type KpiPeriod = "daily" | "weekly" | "monthly";

export type KpiStatus = "on_track" | "warning" | "critical";

export interface KpiDefinition {
  kpiId: string;
  name: string;
  description: string;
  formula: string;
  unit: string;
  target: number;
  warningThreshold: number;
  owner: string;
  refreshFrequency: string;
}

export interface KpiResult {
  kpiId: string;
  period: KpiPeriod;
  periodDate: string; // ISO date
  actualValue: number;
  targetValue: number;
  status: KpiStatus;
}

export interface KpiInput {
  totalScheduledShifts: number;
  confirmedShifts: number;
  missedShifts: number;
  completedShifts: number;
  lateArrivals: number;
  totalEscalations: number;
  sumEscalationMinutes: number;
  shiftsWithDocComplete: number;
  openGaps: number;
  totalResolvedIssues: number;
  sumResolutionHours: number;
  requiredFollowUps: number;
  completedFollowUps: number;
}
