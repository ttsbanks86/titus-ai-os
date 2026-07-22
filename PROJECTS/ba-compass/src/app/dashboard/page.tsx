"use client";

import { useState, useMemo } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
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
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from "recharts";

const STATUS_COLORS = ["#16a34a", "#d97706", "#2563eb", "#6b7280", "#dc2626"];
const PIE_COLORS = ["#16a34a", "#d97706", "#dc2626", "#6b7280"];

type Period = "full" | "week1" | "week2";

export default function DashboardPage() {
  const [period, setPeriod] = useState<Period>("full");
  const [drillDown, setDrillDown] = useState<string | null>(null);

  const filtered = useMemo(() => {
    if (period === "full") return { shifts, escalations, issues: serviceIssues, followUps: followUpRecords };
    const week1Start = "2026-07-14";
    const week1End = "2026-07-20";
    const week2Start = "2026-07-21";
    const week2End = "2026-07-27";

    const inWeek = (date: string, start: string, end: string) => date >= start && date <= end;
    const isWeek1 = period === "week1";
    const rangeStart = isWeek1 ? week1Start : week2Start;
    const rangeEnd = isWeek1 ? week1End : week2End;

    return {
      shifts: shifts.filter((s) => inWeek(s.scheduledDate, rangeStart, rangeEnd)),
      escalations: escalations.filter((e) => {
        const shift = shifts.find((s) => s.shiftId === e.shiftId);
        return shift && inWeek(shift.scheduledDate, rangeStart, rangeEnd);
      }),
      issues: serviceIssues.filter((iss) => {
        const shift = shifts.find((s) => s.shiftId === iss.shiftId);
        return shift && inWeek(shift.scheduledDate, rangeStart, rangeEnd);
      }),
      followUps: followUpRecords, // Show all follow-ups (they span the whole period)
    };
  }, [period]);

  const kpiInput = getAllShiftData();
  const docCounts = getDocumentationCounts();
  const kpis = calculateAllKpis(kpiInput, docCounts.completed, docCounts.required);

  const shiftStatusData = [
    { name: "Completed", value: filtered.shifts.filter((s) => s.status === "completed").length },
    { name: "Confirmed", value: filtered.shifts.filter((s) => s.status === "confirmed").length },
    { name: "In Progress", value: filtered.shifts.filter((s) => s.status === "in_progress").length },
    { name: "Unconfirmed", value: filtered.shifts.filter((s) => s.status === "unconfirmed").length },
    { name: "Missed", value: filtered.shifts.filter((s) => s.status === "missed").length },
  ];

  const escalationData = [
    { name: "Resolved", value: filtered.escalations.filter((e) => e.status === "resolved").length },
    { name: "Open", value: filtered.escalations.filter((e) => e.status === "open").length },
  ];

  const issueData = [
    { name: "Resolved", value: filtered.issues.filter((i) => i.status === "resolved").length },
    { name: "Open", value: filtered.issues.filter((i) => i.status === "open").length },
  ];

  const followUpData = [
    { name: "Completed", value: filtered.followUps.filter((f) => f.status === "completed").length },
    { name: "Pending", value: filtered.followUps.filter((f) => f.status !== "completed").length },
  ];

  const kpiComparisonData = [
    { name: "Shift Fill", actual: kpis.shiftFillRate.value, target: 95 },
    { name: "Missed", actual: kpis.missedShiftRate.value, target: 2 },
    { name: "Late Arrival", actual: kpis.lateArrivalRate.value, target: 10 },
    { name: "Doc Complete", actual: kpis.documentationCompletionRate.value, target: 95 },
    { name: "Follow-Up", actual: kpis.followUpCompletionRate.value, target: 90 },
  ];

  // Drill-down records
  const drillDownRecords = useMemo(() => {
    if (!drillDown) return [];
    switch (drillDown) {
      case "shift-fill":
        return filtered.shifts.filter((s) => s.status === "completed" || s.status === "confirmed").map((s) => ({ id: s.shiftId, status: s.status, date: s.scheduledDate, detail: `Caregiver: ${s.caregiverId || "Unassigned"}`, included: true }));
      case "missed-shift":
        return filtered.shifts.filter((s) => s.status === "missed").map((s) => ({ id: s.shiftId, status: "Missed", date: s.scheduledDate, detail: s.notes || "No notes", included: true }));
      case "late-arrival":
        return filtered.shifts.filter((s) => s.isLate).map((s) => ({ id: s.shiftId, status: "Late", date: s.scheduledDate, detail: `Scheduled: ${s.scheduledStart}, Arrived: ${s.actualArrival}`, included: true }));
      case "documentation":
        return filtered.shifts.filter((s) => s.status === "completed" && s.documentationStatus !== "not_required").map((s) => ({ id: s.shiftId, status: s.documentationStatus === "complete" ? "Complete" : "Incomplete", date: s.scheduledDate, detail: `Documentation: ${s.documentationStatus}`, included: s.documentationStatus === "complete" }));
      case "escalation":
        return filtered.escalations.map((e) => ({ id: e.escalationId, status: e.status === "resolved" ? "Resolved" : "Open", date: e.identifiedTime.split("T")[0], detail: `Type: ${e.issueType}, Severity: ${e.severity}`, included: e.status === "resolved" }));
      case "followup":
        return filtered.followUps.map((f) => ({ id: f.followupId, status: f.status === "completed" ? "Completed" : "Pending", date: f.deadline, detail: `Owner: ${f.owner}`, included: f.status === "completed" }));
      default:
        return [];
    }
  }, [drillDown, filtered]);

  const periodLabel = period === "full" ? "Full Period (Jul 14–27)" : period === "week1" ? "Week 1 (Jul 14–20)" : "Week 2 (Jul 21–27)";

  return (
    <div className="content-container py-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <PageHeading title="KPI Dashboard" subtitle={`Operational metrics — ${periodLabel}`} />
        <div className="flex gap-1 no-print">
          {(["full", "week1", "week2"] as const).map((p) => (
            <button key={p} onClick={() => setPeriod(p)} className={`rounded px-2.5 py-1 text-xs font-medium ${period === p ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{p === "full" ? "All" : p === "week1" ? "Week 1" : "Week 2"}</button>
          ))}
        </div>
      </div>
      <div className="mb-6"><DataNotice /></div>

      {/* KPI Cards */}
      <div className="mb-8 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        <div onClick={() => setDrillDown(drillDown === "shift-fill" ? null : "shift-fill")} className="cursor-pointer" role="button" tabIndex={0} aria-expanded={drillDown === "shift-fill"} onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setDrillDown(drillDown === "shift-fill" ? null : "shift-fill"); }}}>
          <MetricCard label="Shift Fill Rate" value={`${kpis.shiftFillRate.value}%`} status={kpis.shiftFillRate.status} />
        </div>
        <div onClick={() => setDrillDown(drillDown === "missed-shift" ? null : "missed-shift")} className="cursor-pointer" role="button" tabIndex={0} aria-expanded={drillDown === "missed-shift"} onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); setDrillDown(drillDown === "missed-shift" ? null : "missed-shift"); }}}>
          <MetricCard label="Missed Shift Rate" value={`${kpis.missedShiftRate.value}%`} status={kpis.missedShiftRate.status} />
        </div>
        <div onClick={() => setDrillDown(drillDown === "late-arrival" ? null : "late-arrival")} className="cursor-pointer" role="button" tabIndex={0} aria-expanded={drillDown === "late-arrival"}>
          <MetricCard label="Late Arrival Rate" value={`${kpis.lateArrivalRate.value}%`} status={kpis.lateArrivalRate.status} />
        </div>
        <div onClick={() => setDrillDown(drillDown === "escalation" ? null : "escalation")} className="cursor-pointer" role="button" tabIndex={0} aria-expanded={drillDown === "escalation"}>
          <MetricCard label="Avg Escalation Time" value={`${kpis.averageEscalationTime.value}m`} status={kpis.averageEscalationTime.status} />
        </div>
        <div onClick={() => setDrillDown(drillDown === "documentation" ? null : "documentation")} className="cursor-pointer" role="button" tabIndex={0} aria-expanded={drillDown === "documentation"}>
          <MetricCard label="Doc Completion" value={`${kpis.documentationCompletionRate.value}%`} status={kpis.documentationCompletionRate.status} />
        </div>
        <MetricCard label="Open Gaps" value={`${kpis.openStaffingGaps.value}`} status={kpis.openStaffingGaps.status} />
        <MetricCard label="Resolution Time" value={`${kpis.issueResolutionTime.value}h`} status={kpis.issueResolutionTime.status} />
        <div onClick={() => setDrillDown(drillDown === "followup" ? null : "followup")} className="cursor-pointer" role="button" tabIndex={0} aria-expanded={drillDown === "followup"}>
          <MetricCard label="Follow-Up Rate" value={`${kpis.followUpCompletionRate.value}%`} status={kpis.followUpCompletionRate.status} />
        </div>
      </div>

      {/* Drill-Down */}
      {drillDown && drillDownRecords.length > 0 && (
        <ContentPanel className="mb-6">
          <div className="flex items-center justify-between">
            <SectionHeading title={`Drill-Down: ${drillDown}`} description={`${drillDownRecords.length} records — ${periodLabel}`} />
            <button onClick={() => setDrillDown(null)} className="text-xs text-brand-600 hover:text-brand-700">Close</button>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-surface-200 text-sm">
              <thead className="bg-surface-50"><tr><th className="px-3 py-2 text-left font-medium text-surface-600">ID</th><th className="px-3 py-2 text-left font-medium text-surface-600">Status</th><th className="px-3 py-2 text-left font-medium text-surface-600">Date</th><th className="px-3 py-2 text-left font-medium text-surface-600">Detail</th><th className="px-3 py-2 text-left font-medium text-surface-600">Included</th></tr></thead>
              <tbody className="divide-y divide-surface-100">
                {drillDownRecords.map((r) => (
                  <tr key={r.id} className="hover:bg-surface-50"><td className="px-3 py-2 font-mono text-xs text-surface-400">{r.id}</td><td className="px-3 py-2">{r.status}</td><td className="px-3 py-2 text-surface-600">{r.date}</td><td className="px-3 py-2 text-xs text-surface-500">{r.detail}</td><td className="px-3 py-2">{r.included ? <span className="text-green-600">Yes</span> : <span className="text-red-600">No</span>}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </ContentPanel>
      )}

      {/* Charts */}
      <div className="mb-6 grid gap-6 lg:grid-cols-2">
        <ContentPanel>
          <SectionHeading title="Shift Status Distribution" description={`${filtered.shifts.length} shifts in this period`} />
          <div className="h-64" role="img" aria-label={`Shift distribution: ${shiftStatusData.map(d => `${d.name}: ${d.value}`).join(", ")}`}>
            <ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={shiftStatusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ name, value }) => `${name}: ${value}`}>{shiftStatusData.map((_, i) => <Cell key={i} fill={STATUS_COLORS[i]} />)}</Pie><Tooltip /><Legend /></PieChart></ResponsiveContainer>
          </div>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="KPI Target Comparison" />
          <div className="h-64" role="img" aria-label="Bar chart comparing actual KPI values to targets">
            <ResponsiveContainer width="100%" height="100%"><BarChart data={kpiComparisonData}><XAxis dataKey="name" tick={{ fontSize: 11 }} /><YAxis /><Tooltip /><Legend /><Bar dataKey="actual" fill="#2563eb" name="Actual" /><Bar dataKey="target" fill="#94a3b8" name="Target" /></BarChart></ResponsiveContainer>
          </div>
        </ContentPanel>
      </div>

      <div className="mb-6 grid gap-6 lg:grid-cols-3">
        <ContentPanel>
          <SectionHeading title="Escalations" />
          <div className="h-48"><ResponsiveContainer width="100%" height="100%"><BarChart data={escalationData}><XAxis dataKey="name" tick={{ fontSize: 11 }} /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#2563eb" /></BarChart></ResponsiveContainer></div>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="Service Issues" />
          <div className="h-48"><ResponsiveContainer width="100%" height="100%"><BarChart data={issueData}><XAxis dataKey="name" tick={{ fontSize: 11 }} /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#d97706" /></BarChart></ResponsiveContainer></div>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="Follow-Ups" />
          <div className="h-48"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={followUpData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} label={({ name, value }) => `${name}: ${value}`}>{followUpData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer></div>
        </ContentPanel>
      </div>

      {/* KPI Definitions Table */}
      <ContentPanel>
        <SectionHeading title="KPI Definitions" />
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50"><tr><th className="px-3 py-2 text-left font-medium text-surface-600">KPI</th><th className="px-3 py-2 text-left font-medium text-surface-600">Formula</th><th className="px-3 py-2 text-left font-medium text-surface-600">Value</th><th className="px-3 py-2 text-left font-medium text-surface-600">Target</th><th className="px-3 py-2 text-left font-medium text-surface-600">Interpretation</th></tr></thead>
            <tbody className="divide-y divide-surface-100">
              {[
                { kpi: "Shift Fill Rate", formula: "(Confirmed / Total) x 100", val: `${kpis.shiftFillRate.value}%`, tgt: "95%", interp: "Higher is better" },
                { kpi: "Missed Shift Rate", formula: "(Missed / Total) x 100", val: `${kpis.missedShiftRate.value}%`, tgt: "< 2%", interp: "Lower is better" },
                { kpi: "Late Arrival Rate", formula: "(Late / Completed) x 100", val: `${kpis.lateArrivalRate.value}%`, tgt: "< 10%", interp: "Lower is better" },
                { kpi: "Avg Escalation Time", formula: "SUM(Time) / Count", val: `${kpis.averageEscalationTime.value}m`, tgt: "< 30m", interp: "Lower is better" },
                { kpi: "Doc Completion Rate", formula: "(Complete / Required) x 100", val: `${kpis.documentationCompletionRate.value}%`, tgt: "95%", interp: "Higher is better" },
                { kpi: "Open Staffing Gaps", formula: "Count of unassigned (48h)", val: `${kpis.openStaffingGaps.value}`, tgt: "< 3", interp: "Lower is better" },
                { kpi: "Issue Resolution Time", formula: "SUM(Hours) / Count", val: `${kpis.issueResolutionTime.value}h`, tgt: "< 4h", interp: "Lower is better" },
                { kpi: "Follow-Up Rate", formula: "(Completed / Required) x 100", val: `${kpis.followUpCompletionRate.value}%`, tgt: "90%", interp: "Higher is better" },
              ].map((row) => (<tr key={row.kpi} className="hover:bg-surface-50"><td className="px-3 py-2 font-medium text-surface-700">{row.kpi}</td><td className="px-3 py-2 font-mono text-xs text-surface-500">{row.formula}</td><td className="px-3 py-2 font-medium">{row.val}</td><td className="px-3 py-2 text-surface-500">{row.tgt}</td><td className="px-3 py-2 text-xs text-surface-500">{row.interp}</td></tr>))}
            </tbody>
          </table>
        </div>
      </ContentPanel>

      <div className="mt-4 text-xs text-surface-400">Showing {filtered.shifts.length} shifts in selected period. Click any metric card to drill down to contributing records.</div>
    </div>
  );
}
