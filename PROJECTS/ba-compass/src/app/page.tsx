import { APP } from "@/lib/constants";
import { PageHeading } from "@/components/ui/page-heading";
import { MetricCard } from "@/components/ui/metric-card";
import { ContentPanel } from "@/components/ui/content-panel";
import { getAllShiftData, getDocumentationCounts } from "@/data/synthetic/kpi-input";
import { calculateAllKpis } from "@/lib/kpi/calculations";

export default function HomePage() {
  const kpiInput = getAllShiftData();
  const docCounts = getDocumentationCounts();
  const kpis = calculateAllKpis(kpiInput, docCounts.completed, docCounts.required);

  const features = [
    { label: "Stakeholder Analysis", href: "/stakeholders", desc: "10 fictional stakeholder profiles with power-interest analysis" },
    { label: "Current State Process", href: "/current-state", desc: "As-is workflow with step-by-step failure point analysis" },
    { label: "Gap Analysis", href: "/analysis", desc: "Root cause identification across 9 business dimensions" },
    { label: "KPI Dashboard", href: "/dashboard", desc: "8 operational metrics with target comparisons" },
    { label: "Future State Design", href: "/future-state", desc: "To-be workflow addressing identified gaps" },
    { label: "Requirements Management", href: "/requirements", desc: "Full BRD, user stories, and acceptance criteria" },
    { label: "Risk Register", href: "/risks", desc: "15 identified risks with mitigation strategies" },
    { label: "Recommendations", href: "/recommendations", desc: "Prioritized improvement recommendations" },
  ];

  return (
    <div className="content-container py-8">
      <PageHeading
        title={APP.NAME}
        subtitle={APP.SUBTITLE}
      />

      <ContentPanel className="mb-8">
        <p className="text-lg text-surface-600">
          <strong>Case Study:</strong> {APP.COMPANY} — A fictional home-care company experiencing
          systemic operational failures including missed shifts, late arrivals,
          incomplete documentation, and delayed escalation.
        </p>
        <p className="mt-2 text-surface-500">
          This portfolio project demonstrates end-to-end Business Analyst skills:
          from problem identification and stakeholder analysis through requirements
          documentation, process design, KPI definition, and executive communication.
        </p>
      </ContentPanel>

      {/* KPI Snapshot */}
      <h2 className="mb-4 text-xl font-semibold text-surface-800">KPI Snapshot</h2>
      <div className="mb-8 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        <MetricCard label="Shift Fill Rate" value={`${kpis.shiftFillRate.value}%`} status={kpis.shiftFillRate.status} />
        <MetricCard label="Missed Shift Rate" value={`${kpis.missedShiftRate.value}%`} status={kpis.missedShiftRate.status} />
        <MetricCard label="Late Arrival Rate" value={`${kpis.lateArrivalRate.value}%`} status={kpis.lateArrivalRate.status} />
        <MetricCard label="Escalation Time" value={`${kpis.averageEscalationTime.value}m`} status={kpis.averageEscalationTime.status} />
        <MetricCard label="Doc Completion" value={`${kpis.documentationCompletionRate.value}%`} status={kpis.documentationCompletionRate.status} />
        <MetricCard label="Open Gaps" value={`${kpis.openStaffingGaps.value}`} status={kpis.openStaffingGaps.status} />
        <MetricCard label="Resolution Time" value={`${kpis.issueResolutionTime.value}h`} status={kpis.issueResolutionTime.status} />
        <MetricCard label="Follow-Up Rate" value={`${kpis.followUpCompletionRate.value}%`} status={kpis.followUpCompletionRate.status} />
      </div>

      {/* Feature Navigation */}
      <h2 className="mb-4 text-xl font-semibold text-surface-800">Explore the Analysis</h2>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {features.map((f) => (
          <a
            key={f.href}
            href={f.href}
            className="block rounded-lg border border-surface-200 bg-white p-4 transition-colors hover:border-brand-300 hover:bg-brand-50"
          >
            <h3 className="font-medium text-brand-700">{f.label}</h3>
            <p className="mt-1 text-sm text-surface-500">{f.desc}</p>
          </a>
        ))}
      </div>

      {/* Phase Status */}
      <div className="mt-8 rounded-lg border border-surface-200 bg-white p-4">
        <h3 className="font-medium text-surface-700">Phase 2 — Application Foundation</h3>
        <p className="mt-1 text-sm text-surface-500">
          The application foundation is complete. Synthetic data, KPI calculation engine,
          and route structure are ready. Recruiter-facing MVP content will be built in Phase 3.
        </p>
      </div>
    </div>
  );
}
