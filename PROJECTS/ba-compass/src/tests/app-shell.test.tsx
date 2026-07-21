// BA Compass — Application Shell Component Tests

import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { StatusBadge } from "@/components/ui/status-badge";
import { MetricCard } from "@/components/ui/metric-card";
import { DataNotice } from "@/components/ui/data-notice";

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
