// BA Compass — Requirements Validation

export interface ValidationError {
  field: string;
  message: string;
}

export interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
}

const VALID_PRIORITIES = ["High", "Medium", "Low"];
const VALID_STATUSES = ["Proposed", "Approved", "In Progress", "Implemented"];
const MAX_STATEMENT_LENGTH = 5000;
const MAX_JUSTIFICATION_LENGTH = 2000;

export function validateRequirementId(id: string): ValidationResult {
  const errors: ValidationError[] = [];
  if (!id || !id.trim()) errors.push({ field: "id", message: "Requirement ID is required" });
  else if (!/^(BR|FR|NFR)-\d{3}$/.test(id.trim())) errors.push({ field: "id", message: "ID must match format BR-XXX, FR-XXX, or NFR-XXX" });
  return { valid: errors.length === 0, errors };
}

export function validateRequirementStatement(statement: string): ValidationResult {
  const errors: ValidationError[] = [];
  if (!statement || !statement.trim()) errors.push({ field: "statement", message: "Requirement statement is required" });
  else if (statement.trim().length < 10) errors.push({ field: "statement", message: "Statement must be at least 10 characters" });
  else if (statement.length > MAX_STATEMENT_LENGTH) errors.push({ field: "statement", message: `Statement must be under ${MAX_STATEMENT_LENGTH} characters` });
  return { valid: errors.length === 0, errors };
}

export function validatePriority(priority: string): ValidationResult {
  const errors: ValidationError[] = [];
  if (!priority) errors.push({ field: "priority", message: "Priority is required" });
  else if (!VALID_PRIORITIES.includes(priority)) errors.push({ field: "priority", message: `Priority must be one of: ${VALID_PRIORITIES.join(", ")}` });
  return { valid: errors.length === 0, errors };
}

export function validateStatus(status: string): ValidationResult {
  const errors: ValidationError[] = [];
  if (!status) errors.push({ field: "status", message: "Status is required" });
  else if (!VALID_STATUSES.includes(status)) errors.push({ field: "status", message: `Status must be one of: ${VALID_STATUSES.join(", ")}` });
  return { valid: errors.length === 0, errors };
}

export function validateStakeholderOwner(owner: string): ValidationResult {
  const errors: ValidationError[] = [];
  if (!owner || !owner.trim()) errors.push({ field: "stakeholderOwner", message: "Stakeholder owner is required" });
  else if (owner.length > 200) errors.push({ field: "stakeholderOwner", message: "Owner name must be under 200 characters" });
  return { valid: errors.length === 0, errors };
}

export function validateJustification(justification: string): ValidationResult {
  const errors: ValidationError[] = [];
  if (justification && justification.length > MAX_JUSTIFICATION_LENGTH) errors.push({ field: "justification", message: `Justification must be under ${MAX_JUSTIFICATION_LENGTH} characters` });
  return { valid: errors.length === 0, errors };
}

export function validateKpiReference(kpi: string): ValidationResult {
  const errors: ValidationError[] = [];
  if (kpi && !/^KPI-\d{3}(\s|,|$)/.test(kpi) && kpi !== "N/A" && !kpi.includes("indirect")) {
    errors.push({ field: "relatedKpi", message: "KPI reference should match KPI-XXX format" });
  }
  return { valid: errors.length === 0, errors };
}

export function validateFullRequirement(data: {
  id?: string;
  statement?: string;
  priority?: string;
  status?: string;
  stakeholderOwner?: string;
  justification?: string;
  relatedKpi?: string;
}): ValidationResult {
  const allErrors: ValidationError[] = [];

  if (data.id) allErrors.push(...validateRequirementId(data.id).errors);
  allErrors.push(...validateRequirementStatement(data.statement || "").errors);
  allErrors.push(...validatePriority(data.priority || "").errors);
  allErrors.push(...validateStatus(data.status || "").errors);
  allErrors.push(...validateStakeholderOwner(data.stakeholderOwner || "").errors);
  allErrors.push(...validateJustification(data.justification || "").errors);
  allErrors.push(...validateKpiReference(data.relatedKpi || "").errors);

  return { valid: allErrors.length === 0, errors: allErrors };
}
