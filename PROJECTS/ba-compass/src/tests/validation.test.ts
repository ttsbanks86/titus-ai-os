// BA Compass — Requirements Validation Tests

import { describe, it, expect } from "vitest";
import {
  validateRequirementId,
  validateRequirementStatement,
  validatePriority,
  validateStatus,
  validateStakeholderOwner,
  validateJustification,
  validateKpiReference,
  validateFullRequirement,
} from "@/lib/validation";

describe("validateRequirementId", () => {
  it("accepts valid BR-XXX format", () => {
    expect(validateRequirementId("BR-001").valid).toBe(true);
    expect(validateRequirementId("FR-015").valid).toBe(true);
    expect(validateRequirementId("NFR-012").valid).toBe(true);
  });
  it("rejects empty ID", () => { expect(validateRequirementId("").valid).toBe(false); });
  it("rejects invalid format", () => { expect(validateRequirementId("BR-01").valid).toBe(false); });
  it("trims whitespace", () => { expect(validateRequirementId("  BR-001  ").valid).toBe(true); });
});

describe("validateRequirementStatement", () => {
  it("accepts valid statement", () => { expect(validateRequirementStatement("The system shall provide visibility into shift status.").valid).toBe(true); });
  it("rejects empty statement", () => { expect(validateRequirementStatement("").valid).toBe(false); });
  it("rejects too short statement", () => { expect(validateRequirementStatement("Short").valid).toBe(false); });
  it("rejects whitespace-only", () => { expect(validateRequirementStatement("   ").valid).toBe(false); });
});

describe("validatePriority", () => {
  it("accepts valid priorities", () => {
    expect(validatePriority("High").valid).toBe(true);
    expect(validatePriority("Medium").valid).toBe(true);
    expect(validatePriority("Low").valid).toBe(true);
  });
  it("rejects invalid priority", () => { expect(validatePriority("Urgent").valid).toBe(false); });
  it("rejects empty", () => { expect(validatePriority("").valid).toBe(false); });
});

describe("validateStatus", () => {
  it("accepts valid statuses", () => {
    expect(validateStatus("Proposed").valid).toBe(true);
    expect(validateStatus("Approved").valid).toBe(true);
    expect(validateStatus("In Progress").valid).toBe(true);
    expect(validateStatus("Implemented").valid).toBe(true);
  });
  it("rejects invalid status", () => { expect(validateStatus("Deleted").valid).toBe(false); });
});

describe("validateStakeholderOwner", () => {
  it("accepts valid owner", () => { expect(validateStakeholderOwner("Operations Manager").valid).toBe(true); });
  it("rejects empty", () => { expect(validateStakeholderOwner("").valid).toBe(false); });
});

describe("validateJustification", () => {
  it("accepts valid justification", () => { expect(validateJustification("This is required for compliance.").valid).toBe(true); });
  it("rejects excessively long", () => { expect(validateJustification("x".repeat(2001)).valid).toBe(false); });
  it("accepts empty", () => { expect(validateJustification("").valid).toBe(true); });
});

describe("validateKpiReference", () => {
  it("accepts valid KPI ref", () => { expect(validateKpiReference("KPI-001").valid).toBe(true); });
  it("accepts N/A", () => { expect(validateKpiReference("N/A").valid).toBe(true); });
  it("accepts indirect", () => { expect(validateKpiReference("KPI-001 (indirect)").valid).toBe(true); });
});

describe("validateFullRequirement", () => {
  it("validates complete valid requirement", () => {
    const r = validateFullRequirement({ id: "BR-001", statement: "The system shall provide visibility into shift status.", priority: "High", status: "Proposed", stakeholderOwner: "Operations Manager", justification: "Required for compliance", relatedKpi: "KPI-001" });
    expect(r.valid).toBe(true);
    expect(r.errors.length).toBe(0);
  });
  it("returns errors for empty requirement", () => {
    const r = validateFullRequirement({ statement: "", priority: "", status: "", stakeholderOwner: "" });
    expect(r.valid).toBe(false);
    expect(r.errors.length).toBeGreaterThan(0);
  });
});
