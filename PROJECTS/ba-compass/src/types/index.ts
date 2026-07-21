// BA Compass — Type Exports

export * from "./domain";
export * from "./requirements";
export * from "./risks";
export * from "./kpi";

// ─── Additional Domain Types ────────────────────────────────

export type StakeholderInfluence = "high" | "medium" | "low";
export type StakeholderInterest = "strategic" | "operational" | "tactical" | "frontline" | "client_facing" | "technical" | "compliance" | "regulatory" | "service_quality";

export interface Stakeholder {
  stakeholderId: string;
  role: string;
  interest: string;
  influence: StakeholderInfluence;
  needs: string;
  painPoints: string;
  responsibilities: string;
  communicationNeeds: string;
  decisionAuthority: string;
  risks: string;
}

export interface ProcessStep {
  stepNumber: number;
  name: string;
  actor: string;
  input: string;
  action: string;
  output: string;
  systemChannel: string;
  delay: string;
  failurePoint: string;
  manualWork: string;
  dataGap: string;
  controlWeakness: string;
}

export interface Recommendation {
  recommendationId: string;
  title: string;
  description: string;
  category: string;
  priority: "critical" | "high" | "medium" | "low";
  effort: string;
  impact: string;
  linkedRequirementIds: string[];
  linkedKpiIds: string[];
}
