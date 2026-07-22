import { APP, SYNTHETIC_NOTICE } from "@/lib/constants";
import { PageHeading } from "@/components/ui/page-heading";
import { MetricCard } from "@/components/ui/metric-card";
import { ContentPanel } from "@/components/ui/content-panel";
import { DataNotice } from "@/components/ui/data-notice";
import { getAllShiftData, getDocumentationCounts } from "@/data/synthetic/kpi-input";
import { calculateAllKpis } from "@/lib/kpi/calculations";

export default function HomePage() {
  const kpiInput = getAllShiftData();
  const docCounts = getDocumentationCounts();
  const kpis = calculateAllKpis(kpiInput, docCounts.completed, docCounts.required);

  return (
    <div className="content-container py-8">
      {/* Hero Section */}
      <div className="mb-8 text-center">
        <div className="mb-2 inline-block rounded-full bg-brand-100 px-3 py-1 text-xs font-medium text-brand-700">
          Portfolio Project — Fictional Case Study
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-surface-900 sm:text-4xl">
          {APP.NAME}
        </h1>
        <p className="mt-2 text-lg text-surface-500">{APP.SUBTITLE}</p>
        <p className="mx-auto mt-4 max-w-2xl text-surface-600">
          BA Compass demonstrates how a Business Analyst can turn fragmented operational problems
          into measurable requirements, process improvements, and decision-ready recommendations.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <a href="/overview" className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-medium text-white transition-colors hover:bg-brand-700">
            Explore the Case Study
          </a>
          <a href="/dashboard" className="rounded-lg border border-surface-300 bg-white px-5 py-2.5 text-sm font-medium text-surface-700 transition-colors hover:bg-surface-50">
            View the Dashboard
          </a>
          <a href="/tour" className="rounded-lg border border-brand-300 bg-white px-5 py-2.5 text-sm font-medium text-brand-700 transition-colors hover:bg-brand-50">
            Start 5-Minute Tour
          </a>
          <a href="/project" className="rounded-lg border border-surface-300 bg-white px-5 py-2.5 text-sm font-medium text-surface-700 transition-colors hover:bg-surface-50">
            About My Contribution
          </a>
        </div>
      </div>

      {/* Business Problem Summary */}
      <ContentPanel className="mb-8">
        <h2 className="font-semibold text-surface-800">The Business Problem</h2>
        <p className="mt-2 text-surface-600">
          <strong>{APP.COMPANY}</strong>, a fictional home-care provider, is experiencing systemic operational failures:
          missed shifts, late caregiver arrivals, delayed escalation, incomplete documentation,
          and fragmented communication. Without centralized visibility or KPI tracking, management
          cannot identify recurring problems or measure improvement.
        </p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <div className="rounded-lg border border-red-100 bg-red-50 p-3 text-sm text-red-800">
            <strong>Operational</strong><br />Missed shifts, late arrivals, open gaps
          </div>
          <div className="rounded-lg border border-yellow-100 bg-yellow-50 p-3 text-sm text-yellow-800">
            <strong>Documentation</strong><br />Incomplete records, compliance risk
          </div>
          <div className="rounded-lg border border-orange-100 bg-orange-50 p-3 text-sm text-orange-800">
            <strong>Visibility</strong><br />No KPI dashboard, reactive management
          </div>
        </div>
      </ContentPanel>

      {/* Data Notice */}
      <div className="mb-8">
        <DataNotice />
      </div>

      {/* KPI Snapshot */}
      <h2 className="mb-4 text-xl font-semibold text-surface-800">KPI Snapshot</h2>
      <div className="mb-8 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        <MetricCard label="Shift Fill Rate" value={`${kpis.shiftFillRate.value}%`} status={kpis.shiftFillRate.status} />
        <MetricCard label="Missed Shift Rate" value={`${kpis.missedShiftRate.value}%`} status={kpis.missedShiftRate.status} />
        <MetricCard label="Late Arrival Rate" value={`${kpis.lateArrivalRate.value}%`} status={kpis.lateArrivalRate.status} />
        <MetricCard label="Avg Escalation Time" value={`${kpis.averageEscalationTime.value}m`} status={kpis.averageEscalationTime.status} />
        <MetricCard label="Doc Completion" value={`${kpis.documentationCompletionRate.value}%`} status={kpis.documentationCompletionRate.status} />
        <MetricCard label="Open Gaps" value={`${kpis.openStaffingGaps.value}`} status={kpis.openStaffingGaps.status} />
        <MetricCard label="Resolution Time" value={`${kpis.issueResolutionTime.value}h`} status={kpis.issueResolutionTime.status} />
        <MetricCard label="Follow-Up Rate" value={`${kpis.followUpCompletionRate.value}%`} status={kpis.followUpCompletionRate.status} />
      </div>

      {/* Key Project Capabilities */}
      <h2 className="mb-4 text-xl font-semibold text-surface-800">What This Project Demonstrates</h2>
      <div className="mb-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-lg border border-surface-200 bg-white p-4"><h3 className="font-medium text-brand-700">Stakeholder Analysis</h3><p className="mt-1 text-sm text-surface-500">10 stakeholder roles with power-interest mapping</p></div>
        <div className="rounded-lg border border-surface-200 bg-white p-4"><h3 className="font-medium text-brand-700">Process Mapping</h3><p className="mt-1 text-sm text-surface-500">11-step current-state and future-state workflows</p></div>
        <div className="rounded-lg border border-surface-200 bg-white p-4"><h3 className="font-medium text-brand-700">Gap Analysis</h3><p className="mt-1 text-sm text-surface-500">22 pain points across 9 business dimensions</p></div>
        <div className="rounded-lg border border-surface-200 bg-white p-4"><h3 className="font-medium text-brand-700">KPI Definitions</h3><p className="mt-1 text-sm text-surface-500">8 operational metrics with formulas and targets</p></div>
        <div className="rounded-lg border border-surface-200 bg-white p-4"><h3 className="font-medium text-brand-700">Requirements Management</h3><p className="mt-1 text-sm text-surface-500">45 requirements across 3 categories with traceability</p></div>
        <div className="rounded-lg border border-surface-200 bg-white p-4"><h3 className="font-medium text-brand-700">Risk Management</h3><p className="mt-1 text-sm text-surface-500">15 risks with mitigation and contingency plans</p></div>
      </div>

      {/* Navigation Links */}
      <div className="flex flex-wrap justify-center gap-2 text-sm text-surface-500">
        <a href="/overview" className="underline hover:text-brand-600">Overview</a>
        <span aria-hidden="true">·</span>
        <a href="/stakeholders" className="underline hover:text-brand-600">Stakeholders</a>
        <span aria-hidden="true">·</span>
        <a href="/current-state" className="underline hover:text-brand-600">Current State</a>
        <span aria-hidden="true">·</span>
        <a href="/analysis" className="underline hover:text-brand-600">Gap Analysis</a>
        <span aria-hidden="true">·</span>
        <a href="/future-state" className="underline hover:text-brand-600">Future State</a>
        <span aria-hidden="true">·</span>
        <a href="/requirements" className="underline hover:text-brand-600">Requirements</a>
        <span aria-hidden="true">·</span>
        <a href="/risks" className="underline hover:text-brand-600">Risks</a>
        <span aria-hidden="true">·</span>
        <a href="/recommendations" className="underline hover:text-brand-600">Recommendations</a>
      </div>
    </div>
  );
}
