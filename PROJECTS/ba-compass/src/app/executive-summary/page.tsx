"use client";

import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { DataNotice } from "@/components/ui/data-notice";
import { MetricCard } from "@/components/ui/metric-card";
import { risks } from "@/data/content/risks-data";
import { getAllShiftData, getDocumentationCounts } from "@/data/synthetic/kpi-input";
import { calculateAllKpis } from "@/lib/kpi/calculations";
import { downloadText } from "@/lib/export";
import { APP, SYNTHETIC_NOTICE } from "@/lib/constants";

export default function ExecutiveSummaryPage() {
  const kpiInput = getAllShiftData();
  const docCounts = getDocumentationCounts();
  const kpis = calculateAllKpis(kpiInput, docCounts.completed, docCounts.required);

  const topRisks = risks.filter((r) => r.riskLevel === "High").slice(0, 3);

  const handleExport = () => {
    const md = `# BA Compass — Executive Summary\n**Company:** BrightCare Home Services (Fictional)\n**Generated:** ${new Date().toISOString().split("T")[0]}\n${SYNTHETIC_NOTICE}\n\n## Business Problem\nBrightCare Home Services experiences missed shifts, late arrivals, delayed escalation, incomplete documentation, and no KPI visibility.\n\n## Key Findings\n1. Shift fill rate of ${kpis.shiftFillRate.value}% indicates missed coverage opportunities\n2. ${kpis.missedShiftRate.value}% missed shift rate directly impacts client care reliability\n3. Average escalation time of ${kpis.averageEscalationTime.value} minutes needs improvement\n4. Documentation completion at ${kpis.documentationCompletionRate.value}% creates compliance risk\n5. Follow-up completion at ${kpis.followUpCompletionRate.value}% shows process gaps\n\n## KPIs\n${[
  `- Shift Fill Rate: ${kpis.shiftFillRate.value}% (target: 95%)`,
  `- Missed Shift Rate: ${kpis.missedShiftRate.value}% (target: <2%)`,
  `- Late Arrival Rate: ${kpis.lateArrivalRate.value}% (target: <10%)`,
  `- Avg Escalation Time: ${kpis.averageEscalationTime.value}m (target: <30m)`,
  `- Doc Completion Rate: ${kpis.documentationCompletionRate.value}% (target: 95%)`,
  `- Open Gaps: ${kpis.openStaffingGaps.value} (target: <3)`,
  `- Resolution Time: ${kpis.issueResolutionTime.value}h (target: <4h)`,
  `- Follow-Up Rate: ${kpis.followUpCompletionRate.value}% (target: 90%)`,
].join("\n")}\n\n## Top Risks\n${topRisks.map((r) => `- ${r.description} (Score: ${r.riskScore})`).join("\n")}\n\n## Recommendations\n1. Implement pre-shift confirmation workflow\n2. Deploy centralized operational dashboard\n3. Define structured escalation paths\n4. Track documentation completion\n5. Build automated KPI reporting\n\n## Disclaimer\nThis is a portfolio case study using synthetic data. All information is fictional.\n`;
    downloadText(md, "ba-compass-executive-summary.md");
  };

  return (
    <div className="content-container py-8">
      <div className="mb-4 flex items-center justify-between">
        <PageHeading title="Executive Summary" subtitle="Key findings, KPIs, and recommendations at a glance" />
        <div className="flex gap-2">
          <button onClick={handleExport} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Export MD</button>
          <button onClick={() => window.print()} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Print / PDF</button>
        </div>
      </div>
      <DataNotice />

      {/* Business Problem */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Business Problem" />
        <p className="text-surface-600">
          BrightCare Home Services, a fictional home-care provider, experiences systemic operational failures including
          missed shifts, late caregiver arrivals, delayed escalation, incomplete documentation, and fragmented communication.
          The organization lacks a KPI dashboard, structured escalation paths, and systematic follow-up processes.
        </p>
      </ContentPanel>

      {/* Key Findings */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Five Strongest Findings" />
        <ol className="list-inside list-decimal space-y-2 text-sm text-surface-600">
          <li><strong>Shift fill rate of {kpis.shiftFillRate.value}%</strong> — Below the 95% target, indicating significant missed coverage opportunities and recurring client impact.</li>
          <li><strong>Missed shift rate of {kpis.missedShiftRate.value}%</strong> — Every missed shift represents a client left without care. This is the highest-priority operational risk.</li>
          <li><strong>Average escalation time of {kpis.averageEscalationTime.value} minutes</strong> — Delays in escalation mean issues linger longer, increasing client dissatisfaction.</li>
          <li><strong>Documentation completion at {kpis.documentationCompletionRate.value}%</strong> — Below the 95% target, creating compliance exposure and potential billing issues.</li>
          <li><strong>Follow-up completion at {kpis.followUpCompletionRate.value}%</strong> — Without structured follow-up, recurring problems go undetected and unresolved.</li>
        </ol>
      </ContentPanel>

      {/* KPI Summary */}
      <div className="mb-6">
        <SectionHeading title="KPI Summary" />
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <MetricCard label="Shift Fill Rate" value={`${kpis.shiftFillRate.value}%`} status={kpis.shiftFillRate.status} />
          <MetricCard label="Missed Shift Rate" value={`${kpis.missedShiftRate.value}%`} status={kpis.missedShiftRate.status} />
          <MetricCard label="Late Arrival Rate" value={`${kpis.lateArrivalRate.value}%`} status={kpis.lateArrivalRate.status} />
          <MetricCard label="Avg Escalation Time" value={`${kpis.averageEscalationTime.value}m`} status={kpis.averageEscalationTime.status} />
          <MetricCard label="Doc Completion" value={`${kpis.documentationCompletionRate.value}%`} status={kpis.documentationCompletionRate.status} />
          <MetricCard label="Open Gaps" value={`${kpis.openStaffingGaps.value}`} status={kpis.openStaffingGaps.status} />
          <MetricCard label="Resolution Time" value={`${kpis.issueResolutionTime.value}h`} status={kpis.issueResolutionTime.status} />
          <MetricCard label="Follow-Up Rate" value={`${kpis.followUpCompletionRate.value}%`} status={kpis.followUpCompletionRate.status} />
        </div>
      </div>

      {/* Top Risks */}
      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        <ContentPanel>
          <SectionHeading title="Highest Risks" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            {topRisks.map((r) => (
              <li key={r.id}><strong>{r.id}:</strong> {r.description} <span className="text-red-600">(Score: {r.riskScore})</span></li>
            ))}
            <li className="text-xs text-surface-400">Full risk register available in the Risks view.</li>
          </ul>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="Priority Recommendations" />
          <ol className="list-inside list-decimal space-y-1 text-sm text-surface-600">
            <li>Implement pre-shift confirmation workflow</li>
            <li>Deploy centralized operational dashboard</li>
            <li>Define structured escalation paths with severity levels</li>
            <li>Track documentation completion with automated reminders</li>
            <li>Build automated KPI reporting for management visibility</li>
          </ol>
        </ContentPanel>
      </div>

      {/* Future-State Benefits */}
      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        <ContentPanel>
          <SectionHeading title="Expected Future-State Benefits" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>Proactive gap detection before client impact</li>
            <li>Structured escalation with clear accountability</li>
            <li>Automated KPI tracking and trend analysis</li>
            <li>Documented audit trail for compliance</li>
            <li>Reduced manual coordination effort</li>
          </ul>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="Implementation Considerations" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>Phased rollout starting with shift visibility</li>
            <li>Stakeholder training and change management</li>
            <li>Data migration from existing spreadsheets</li>
            <li>Integration with existing communication tools</li>
          </ul>
        </ContentPanel>
      </div>

      {/* Limitations */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Limitations" />
        <p className="text-sm text-surface-600">
          This executive summary is based on a fictional case study using synthetic data. The KPIs, findings, and
          recommendations represent projected outcomes from the analysis, not real operational results. Actual
          outcomes would depend on implementation quality, stakeholder adoption, and organizational context.
        </p>
      </ContentPanel>

      {/* Responsible AI */}
      <ContentPanel>
        <SectionHeading title="Responsible AI Statement" />
        <p className="text-sm text-surface-600">
          The BA Compass portfolio application uses no AI services for its core functionality. All KPI calculations
          are deterministic. All requirements, risks, and recommendations were developed through structured BA
          methodology. Any future AI integration will be optional, labeled, and reviewed by a human analyst.
        </p>
      </ContentPanel>
    </div>
  );
}
