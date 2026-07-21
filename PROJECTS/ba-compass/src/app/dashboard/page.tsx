"use client";

import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { MetricCard } from "@/components/ui/metric-card";
import { DataNotice } from "@/components/ui/data-notice";
import { getAllShiftData, getDocumentationCounts } from "@/data/synthetic/kpi-input";
import { calculateAllKpis } from "@/lib/kpi/calculations";
import { shifts } from "@/data/synthetic/shifts";
import { escalations } from "@/data/synthetic/escalations";
import { serviceIssues } from "@/data/synthetic/issues";
import { followUpRecords } from "@/data/synthetic/followups";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend,
} from "recharts";

const STATUS_COLORS = ["#16a34a", "#d97706", "#2563eb", "#6b7280", "#dc2626"];
const PIE_COLORS = ["#16a34a", "#d97706", "#dc2626", "#6b7280"];

export default function DashboardPage() {
  const kpiInput = getAllShiftData();
  const docCounts = getDocumentationCounts();
  const kpis = calculateAllKpis(kpiInput, docCounts.completed, docCounts.required);

  // Shift status distribution
  const statusCounts = {
    confirmed: shifts.filter((s) => s.status === "confirmed").length,
    unconfirmed: shifts.filter((s) => s.status === "unconfirmed").length,
    in_progress: shifts.filter((s) => s.status === "in_progress").length,
    completed: shifts.filter((s) => s.status === "completed").length,
    missed: shifts.filter((s) => s.status === "missed").length,
  };
  const shiftStatusData = [
    { name: "Completed", value: statusCounts.completed },
    { name: "Confirmed", value: statusCounts.confirmed },
    { name: "In Progress", value: statusCounts.in_progress },
    { name: "Unconfirmed", value: statusCounts.unconfirmed },
    { name: "Missed", value: statusCounts.missed },
  ];

  // Escalation status
  const escStatus = {
    resolved: escalations.filter((e) => e.status === "resolved").length,
    open: escalations.filter((e) => e.status === "open").length,
  };
  const escalationData = [
    { name: "Resolved", value: escStatus.resolved },
    { name: "Open", value: escStatus.open },
  ];

  // Issue status
  const issueStatus = {
    resolved: serviceIssues.filter((i) => i.status === "resolved").length,
    open: serviceIssues.filter((i) => i.status === "open").length,
  };
  const issueData = [
    { name: "Resolved", value: issueStatus.resolved },
    { name: "Open", value: issueStatus.open },
  ];

  // Follow-up status
  const fupCounts = {
    completed: followUpRecords.filter((f) => f.status === "completed").length,
    pending: followUpRecords.filter((f) => f.status === "pending" || f.status === "in_progress").length,
  };
  const followUpData = [
    { name: "Completed", value: fupCounts.completed },
    { name: "Pending", value: fupCounts.pending },
  ];

  // KPI target comparison
  const kpiComparisonData = [
    { name: "Shift Fill Rate", actual: kpis.shiftFillRate.value, target: 95 },
    { name: "Missed Shift Rate", actual: kpis.missedShiftRate.value, target: 2 },
    { name: "Late Arrival Rate", actual: kpis.lateArrivalRate.value, target: 10 },
    { name: "Doc Completion", actual: kpis.documentationCompletionRate.value, target: 95 },
    { name: "Follow-Up Rate", actual: kpis.followUpCompletionRate.value, target: 90 },
  ];

  const metrics = [
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
      <PageHeading title="KPI Dashboard" subtitle="Operational metrics from synthetic BrightCare Home Services data" />
      <div className="mb-6"><DataNotice /></div>

      {/* KPI Cards */}
      <div className="mb-8 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        {metrics.map((m) => <MetricCard key={m.label} label={m.label} value={m.value} status={m.status} />)}
      </div>

      {/* Charts Row 1 */}
      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        {/* Shift Status Distribution */}
        <ContentPanel>
          <SectionHeading title="Shift Status Distribution" description="How shifts are distributed across status categories" />
          <div className="h-64" role="img" aria-label={`Pie chart showing shift distribution: ${shiftStatusData.map(d => `${d.name}: ${d.value}`).join(", ")}`}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={shiftStatusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ name, value }) => `${name}: ${value}`}>
                  {shiftStatusData.map((_, i) => <Cell key={i} fill={STATUS_COLORS[i]} />)}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-2 text-xs text-surface-500"><strong>What the data shows:</strong> Most shifts are completed. Unconfirmed and missed shifts represent the key operational risk areas requiring process improvement.</p>
        </ContentPanel>

        {/* KPI Target Comparison */}
        <ContentPanel>
          <SectionHeading title="KPI Target Comparison" description="Actual values vs. target thresholds (selected KPIs)" />
          <div className="h-64" role="img" aria-label={`Bar chart comparing actual KPI values to targets`}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={kpiComparisonData}>
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="actual" fill="#2563eb" name="Actual" />
                <Bar dataKey="target" fill="#94a3b8" name="Target" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-2 text-xs text-surface-500"><strong>Why it matters:</strong> Comparing actual values to targets reveals which areas need immediate management attention.</p>
        </ContentPanel>
      </div>

      {/* Charts Row 2 */}
      <div className="mb-6 grid gap-6 lg:grid-cols-3">
        {/* Escalations */}
        <ContentPanel>
          <SectionHeading title="Escalations" description="Resolved vs. open escalations" />
          <div className="h-48" role="img" aria-label={`Bar chart showing ${escStatus.resolved} resolved escalations and ${escStatus.open} open escalations`}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={escalationData}>
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#2563eb" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-1 text-xs text-surface-500"><strong>Insight:</strong> Most escalations are resolved. Open items need follow-up assignment.</p>
        </ContentPanel>

        {/* Service Issues */}
        <ContentPanel>
          <SectionHeading title="Service Issues" description="Resolved vs. open service issues" />
          <div className="h-48" role="img" aria-label={`Bar chart showing ${issueStatus.resolved} resolved issues and ${issueStatus.open} open issues`}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={issueData}>
                <XAxis dataKey="name" tick={{ fontSize: 11 }} />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="value" fill="#d97706" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-1 text-xs text-surface-500"><strong>Insight:</strong> Open issues require escalation follow-through to prevent recurrence.</p>
        </ContentPanel>

        {/* Follow-Ups */}
        <ContentPanel>
          <SectionHeading title="Follow-Up Completion" description="Follow-up records by status" />
          <div className="h-48" role="img" aria-label={`Pie chart showing ${fupCounts.completed} completed follow-ups and ${fupCounts.pending} pending`}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={followUpData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} label={({ name, value }) => `${name}: ${value}`}>
                  {followUpData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p className="mt-1 text-xs text-surface-500"><strong>Insight:</strong> Follow-up completion needs process improvement to ensure issue closure.</p>
        </ContentPanel>
      </div>

      {/* KPI Definitions */}
      <ContentPanel>
        <SectionHeading title="KPI Definitions and Interpretation" description="How each metric is calculated and what it means" />
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr><th className="px-3 py-2 text-left font-medium text-surface-600">KPI</th><th className="px-3 py-2 text-left font-medium text-surface-600">Formula</th><th className="px-3 py-2 text-left font-medium text-surface-600">Current</th><th className="px-3 py-2 text-left font-medium text-surface-600">Target</th><th className="px-3 py-2 text-left font-medium text-surface-600">Interpretation</th></tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {[
                { kpi: "Shift Fill Rate", formula: "(Confirmed / Total) x 100", val: `${kpis.shiftFillRate.value}%`, tgt: "95%", interp: "Higher is better. Measures scheduling effectiveness." },
                { kpi: "Missed Shift Rate", formula: "(Missed / Total) x 100", val: `${kpis.missedShiftRate.value}%`, tgt: "< 2%", interp: "Lower is better. Missed shifts directly impact client care." },
                { kpi: "Late Arrival Rate", formula: "(Late / Completed) x 100", val: `${kpis.lateArrivalRate.value}%`, tgt: "< 10%", interp: "Lower is better. Late arrivals reduce client satisfaction." },
                { kpi: "Avg Escalation Time", formula: "SUM(Time) / Count", val: `${kpis.averageEscalationTime.value}m`, tgt: "< 30m", interp: "Lower is better. Faster escalation means quicker response." },
                { kpi: "Doc Completion Rate", formula: "(Completed / Required) x 100", val: `${kpis.documentationCompletionRate.value}%`, tgt: "95%", interp: "Higher is better. Incomplete docs create compliance risk." },
                { kpi: "Open Staffing Gaps", formula: "Count of unassigned shifts (48h)", val: `${kpis.openStaffingGaps.value}`, tgt: "< 3", interp: "Lower is better. Gaps need immediate attention." },
                { kpi: "Issue Resolution Time", formula: "SUM(Hours) / Count", val: `${kpis.issueResolutionTime.value}h`, tgt: "< 4h", interp: "Lower is better. Faster resolution improves service." },
                { kpi: "Follow-Up Rate", formula: "(Completed / Required) x 100", val: `${kpis.followUpCompletionRate.value}%`, tgt: "90%", interp: "Higher is better. Ensures issues stay closed." },
              ].map((row) => (
                <tr key={row.kpi} className="hover:bg-surface-50">
                  <td className="px-3 py-2 font-medium text-surface-700">{row.kpi}</td>
                  <td className="px-3 py-2 font-mono text-xs text-surface-500">{row.formula}</td>
                  <td className="px-3 py-2 font-medium">{row.val}</td>
                  <td className="px-3 py-2 text-surface-500">{row.tgt}</td>
                  <td className="px-3 py-2 text-xs text-surface-500">{row.interp}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ContentPanel>

      <div className="mt-6 flex justify-between">
        <a href="/analysis" className="text-sm font-medium text-brand-600 hover:text-brand-700">← Gap Analysis</a>
        <a href="/future-state" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: Future State →</a>
      </div>
    </div>
  );
}
