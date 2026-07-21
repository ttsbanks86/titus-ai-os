// BA Compass — Risk Types

export type RiskCategory =
  | "scope"
  | "quality"
  | "privacy"
  | "usability"
  | "technical"
  | "accessibility"
  | "security"
  | "project_management";

export type RiskStatus = "active" | "mitigated" | "closed";

export interface Risk {
  riskId: string;
  description: string;
  category: RiskCategory;
  likelihood: number; // 1-5
  impact: number; // 1-5
  riskScore: number; // likelihood * impact
  owner: string;
  mitigation: string;
  contingency: string;
  trigger: string;
  status: RiskStatus;
}
