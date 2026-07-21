import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { MetricCard } from "@/components/ui/metric-card";
import { DataNotice } from "@/components/ui/data-notice";
import { getAllShiftData, getDocumentationCounts } from "@/data/synthetic/kpi-input";
import { calculateAllKpis } from "@/lib/kpi/calculations";

export default function DashboardPage() {
  const kpiInput = getAllShiftData();
  const docCounts = getDocumentationCounts();
  const kpis = calculateAllKpis(kpiInput, docCounts.completed, docCounts.required);

  type MetricItem = { label: string; value: string; status: "on_track" | "warning" | "critical" };
  const metrics: MetricItem[] = [
    { label: "Shift Fill Rate", value: `${kpis.shiftFillRate.value}%`, status: kpis.shiftFillRate.status },
    { label: "Missed Shift Rate", value: `${kpis.missedShiftRate.value}%`, status: kpis.missedShiftRate.status },
    { label: "Late Arrival Rate", value: `${kpis.lateArrivalRate.value}%`, status: kpis.lateArrivalRate.status },
    { label: "Avg Escalation Time", value: `${kpis.averageEscalationTime.value}m`, status: kpis.averageEscalationTime.status },
    { label: "Doc Completion Rate", value: `${kpis.documentationCompletionRate.value}%`, status: kpis.documentationCompletionRate.status },
    { label: "Open Staffing Gaps", value: `${kpis.openStaffingGaps.value}`, status: kpis.openStaffingGaps.status },
    { label: "Issue Resolution Time", value: `${kpis.issueResolutionTime.value}h`, status: kpis.issueResolutionTime.status },
    { label: "Follow-Up Rate", value: `${kpis.followUpCompletionRate.value}%`, status: kpis.followUpCompletionRate.status },
  ];

  return (
    <div className="content-container py-8">
      <PageHeading
        title="KPI Dashboard"
        subtitle="Operational metrics — BrightCare Home Services (Synthetic Data)"
      />
      <div className="mb-6">
        <DataNotice />
      </div>
      <ContentPanel>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {metrics.map((m) => (
            <MetricCard key={m.label} label={m.label} value={m.value} status={m.status} />
          ))}
        </div>
        <div className="mt-6 border-t border-surface-200 pt-4">
          <h3 className="mb-2 text-sm font-semibold text-surface-700">KPI Data Summary</h3>
          <ul className="space-y-1 text-xs text-surface-500">
            <li>Total Scheduled Shifts: {kpiInput.totalScheduledShifts}</li>
            <li>Confirmed Shifts: {kpiInput.confirmedShifts}</li>
            <li>Completed Shifts: {kpiInput.completedShifts}</li>
            <li>Missed Shifts: {kpiInput.missedShifts}</li>
            <li>Late Arrivals: {kpiInput.lateArrivals}</li>
            <li>Open Gaps: {kpiInput.openGaps}</li>
            <li>Resolved Issues: {kpiInput.totalResolvedIssues}</li>
          </ul>
        </div>
      </ContentPanel>
      <p className="mt-4 text-sm text-surface-400">
        Full Phase 3 content will include trend visualizations (Recharts), time-period
        filtering, target vs. actual comparisons, and exportable reports.
      </p>
    </div>
  );
}
