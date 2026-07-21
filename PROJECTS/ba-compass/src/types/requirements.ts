// BA Compass — Requirements Types

export type RequirementType = "business" | "functional" | "nonfunctional";

export type RequirementPriority = "high" | "medium" | "low";

export type RequirementStatus =
  | "proposed"
  | "approved"
  | "in_progress"
  | "implemented";

export interface Requirement {
  reqId: string;
  type: RequirementType;
  statement: string;
  priority: RequirementPriority;
  stakeholderOwner: string;
  source: string;
  acceptanceMeasure: string;
  relatedKpi: string | null;
  status: RequirementStatus;
}

export interface UserStory {
  storyId: string;
  role: string;
  capability: string;
  businessValue: string;
  priority: RequirementPriority;
  linkedRequirementIds: string[];
  acceptanceCriterionIds: string[];
  status: RequirementStatus;
}

export interface AcceptanceCriterion {
  criterionId: string;
  storyId: string;
  given: string;
  when: string;
  then: string;
  priority: RequirementPriority;
}
