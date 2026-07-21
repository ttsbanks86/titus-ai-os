// BA Compass — Application Shell Component Tests

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { StatusBadge } from "@/components/ui/status-badge";
import { MetricCard } from "@/components/ui/metric-card";
import { DataNotice } from "@/components/ui/data-notice";
import { businessRequirements, functionalRequirements, nonfunctionalRequirements } from "@/data/content/requirements-data";
import { stakeholders } from "@/data/content/stakeholders";
import { risks } from "@/data/content/risks-data";
import { currentStateSteps, futureStateImprovements } from "@/data/content/process-data";
import { gaps } from "@/data/content/gaps-data";
import { NAV_ITEMS, NAV_SEQUENCE } from "@/lib/constants";

describe("StatusBadge", () => {
  it("renders with default variant", () => {
    render(<StatusBadge label="Test" />);
    expect(screen.getByText("Test")).toBeInTheDocument();
  });
  it("renders with success variant", () => {
    render(<StatusBadge label="Complete" variant="success" />);
    const badge = screen.getByText("Complete");
    expect(badge).toBeInTheDocument();
    expect(badge.className).toContain("status-badge--success");
  });
  it("renders with error variant", () => {
    render(<StatusBadge label="Failed" variant="error" />);
    const badge = screen.getByText("Failed");
    expect(badge).toBeInTheDocument();
    expect(badge.className).toContain("status-badge--error");
  });
  it("renders with warning variant", () => {
    render(<StatusBadge label="Warning" variant="warning" />);
    expect(screen.getByText("Warning")).toBeInTheDocument();
  });
  it("renders with info variant", () => {
    render(<StatusBadge label="Info" variant="info" />);
    expect(screen.getByText("Info")).toBeInTheDocument();
  });
});

describe("MetricCard", () => {
  it("renders label and value", () => {
    render(<MetricCard label="Fill Rate" value="95%" status="on_track" />);
    expect(screen.getByText("Fill Rate")).toBeInTheDocument();
    expect(screen.getByText("95%")).toBeInTheDocument();
  });
  it("renders with warning status", () => {
    render(<MetricCard label="Gaps" value="5" status="warning" />);
    expect(screen.getByText("Gaps")).toBeInTheDocument();
    expect(screen.getByText("5")).toBeInTheDocument();
  });
  it("renders with critical status", () => {
    render(<MetricCard label="Missed Rate" value="8%" status="critical" />);
    expect(screen.getByText("Missed Rate")).toBeInTheDocument();
    expect(screen.getByText("8%")).toBeInTheDocument();
  });
});

describe("DataNotice", () => {
  it("renders synthetic data notice", () => {
    render(<DataNotice />);
    expect(screen.getByText(/synthetic and fictional/i)).toBeInTheDocument();
  });
});

describe("Content Data Integrity", () => {
  it("business requirements content is complete", () => {
    expect(businessRequirements.length).toBe(15);
    expect(businessRequirements[0].id).toBe("BR-001");
    expect(businessRequirements[14].id).toBe("BR-015");
  });
  it("functional requirements content is complete", () => {
    expect(functionalRequirements.length).toBe(18);
    expect(functionalRequirements[0].id).toBe("FR-001");
  });
  it("nonfunctional requirements content is complete", () => {
    expect(nonfunctionalRequirements.length).toBe(12);
    expect(nonfunctionalRequirements[0].id).toBe("NFR-001");
  });
  it("stakeholder content has 10 stakeholders", () => {
    expect(stakeholders.length).toBe(10);
    expect(stakeholders[0].id).toBe("STK-001");
    expect(stakeholders[9].id).toBe("STK-010");
  });
  it("risks content has 15 risks", () => {
    expect(risks.length).toBe(15);
    expect(risks[0].id).toBe("R-001");
    expect(risks[14].id).toBe("R-015");
  });
  it("current state process has 11 steps", () => {
    expect(currentStateSteps.length).toBe(11);
    expect(currentStateSteps[0].step).toBe(1);
    expect(currentStateSteps[10].step).toBe(11);
  });
  it("gap analysis has 20 gaps", () => {
    expect(gaps.length).toBe(20);
  });
  it("future state improvements are defined", () => {
    expect(futureStateImprovements.length).toBe(8);
  });
  it("navigation has 11 items", () => {
    expect(NAV_ITEMS.length).toBe(11);
  });
  it("navigation sequence has 12 items (including home)", () => {
    expect(NAV_SEQUENCE.length).toBe(12);
  });
});
