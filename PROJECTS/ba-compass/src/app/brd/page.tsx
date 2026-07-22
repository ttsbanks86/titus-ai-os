"use client";

import { useRef } from "react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { DataNotice } from "@/components/ui/data-notice";
import { businessRequirements, functionalRequirements, nonfunctionalRequirements } from "@/data/content/requirements-data";
import { risks } from "@/data/content/risks-data";
import { stakeholders } from "@/data/content/stakeholders";
import { downloadText } from "@/lib/export";
import { getAllShiftData, getDocumentationCounts } from "@/data/synthetic/kpi-input";
import { calculateAllKpis } from "@/lib/kpi/calculations";
import { APP, SYNTHETIC_NOTICE } from "@/lib/constants";

export default function BrdPage() {
  const printRef = useRef<HTMLDivElement>(null);
  const kpiInput = getAllShiftData();
  const docCounts = getDocumentationCounts();
  const kpis = calculateAllKpis(kpiInput, docCounts.completed, docCounts.required);

  const sections = [
    { id: "executive-summary", label: "Executive Summary" },
    { id: "background", label: "Background" },
    { id: "business-problem", label: "Business Problem" },
    { id: "objectives", label: "Objectives" },
    { id: "stakeholders", label: "Stakeholders" },
    { id: "scope", label: "Scope" },
    { id: "current-state", label: "Current State" },
    { id: "future-state", label: "Future State" },
    { id: "requirements", label: "Requirements" },
    { id: "kpis", label: "KPIs" },
    { id: "risks", label: "Risks" },
    { id: "assumptions", label: "Assumptions" },
  ];

  const handleExportMarkdown = () => {
    const md = `# Business Requirements Document — BA Compass\n**Company:** BrightCare Home Services (Fictional)\n**Version:** 0.1 (Portfolio Simulation)\n**Generated:** ${new Date().toISOString().split("T")[0]}\n${SYNTHETIC_NOTICE}\n\n## Executive Summary\nBrightCare Home Services is a fictional home-care provider experiencing systemic operational failures including missed shifts, late arrivals, incomplete documentation, and delayed escalation. This BRD documents the business context, stakeholder needs, requirements, and success measures for a structured analysis and proposed solution.\n\n## Business Requirements\n${businessRequirements.map((r) => `- **${r.id}** (${r.priority}): ${r.statement}`).join("\n")}\n\n## KPIs\n${[
  `- Shift Fill Rate: ${kpis.shiftFillRate.value}% (target: 95%)`,
  `- Missed Shift Rate: ${kpis.missedShiftRate.value}% (target: <2%)`,
  `- Late Arrival Rate: ${kpis.lateArrivalRate.value}% (target: <10%)`,
  `- Avg Escalation Time: ${kpis.averageEscalationTime.value}m (target: <30m)`,
  `- Doc Completion Rate: ${kpis.documentationCompletionRate.value}% (target: 95%)`,
  `- Open Staffing Gaps: ${kpis.openStaffingGaps.value} (target: <3)`,
  `- Issue Resolution Time: ${kpis.issueResolutionTime.value}h (target: <4h)`,
  `- Follow-Up Rate: ${kpis.followUpCompletionRate.value}% (target: 90%)`,
].join("\n")}\n\n## Risks\n${risks.map((r) => `- **${r.id}** [${r.riskLevel}] ${r.description}`).join("\n")}\n\n---\n*This document is a portfolio simulation. All data is synthetic and fictional.*`;
    downloadText(md, "ba-compass-brd.md");
  };

  return (
    <div className="content-container py-8" ref={printRef}>
      <div className="mb-4 flex items-center justify-between">
        <PageHeading title="Business Requirements Document" subtitle="BA Compass — Portfolio Simulation" />
        <div className="flex gap-2">
          <button onClick={handleExportMarkdown} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Export MD</button>
          <button onClick={() => window.print()} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Print / PDF</button>
        </div>
      </div>
      <DataNotice />

      {/* Table of Contents */}
      <ContentPanel className="mb-6" printHide>
        <SectionHeading title="Table of Contents" />
        <nav aria-label="BRD sections" className="grid grid-cols-2 gap-1 sm:grid-cols-3">
          {sections.map((s) => (
            <a key={s.id} href={`#${s.id}`} className="text-sm text-brand-600 hover:text-brand-700 hover:underline">{s.label}</a>
          ))}
        </nav>
      </ContentPanel>

      <div className="space-y-6" id="brd-content">
        <ContentPanel id="executive-summary">
          <SectionHeading title="1. Executive Summary" />
          <p className="text-surface-600">BrightCare Home Services, a fictional home-care provider, is experiencing systemic operational failures that reduce service reliability and limit management visibility. This BRD documents the business context, stakeholder needs, requirements, and success measures for a structured analysis and proposed solution.</p>
        </ContentPanel>

        <ContentPanel id="background">
          <SectionHeading title="2. Background" />
          <p className="text-surface-600">BrightCare Home Services manages caregiver-client assignments through informal, decentralized processes relying on spreadsheets, phone calls, and paper documentation. The BA Compass project was initiated to document current processes, define requirements, create traceable success measures, and produce a recruiter-ready demonstration of BA skills.</p>
        </ContentPanel>

        <ContentPanel id="business-problem">
          <SectionHeading title="3. Business Problem" />
          <p className="text-surface-600">The core problem is that BrightCare Home Services cannot reliably identify, track, or resolve operational service failures: missed shifts, late arrivals, delayed escalation, incomplete documentation, fragmented communication, and no KPI visibility for management.</p>
        </ContentPanel>

        <ContentPanel id="objectives">
          <SectionHeading title="4. Objectives" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>Document current-state operational processes</li>
            <li>Identify root causes of operational failures</li>
            <li>Define traceable business requirements</li>
            <li>Create KPI framework for operational measurement</li>
            <li>Design future-state process improvements</li>
            <li>Produce professional BA deliverables</li>
          </ul>
        </ContentPanel>

        <ContentPanel id="stakeholders">
          <SectionHeading title="5. Stakeholders" />
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-surface-200 text-sm">
              <thead className="bg-surface-50"><tr><th className="px-3 py-2 text-left font-medium text-surface-600">ID</th><th className="px-3 py-2 text-left font-medium text-surface-600">Role</th><th className="px-3 py-2 text-left font-medium text-surface-600">Interest</th><th className="px-3 py-2 text-left font-medium text-surface-600">Influence</th></tr></thead>
              <tbody className="divide-y divide-surface-100">
                {stakeholders.map((s) => (
                  <tr key={s.id} className="hover:bg-surface-50"><td className="px-3 py-2 font-mono text-xs text-surface-400">{s.id}</td><td className="px-3 py-2 text-surface-700">{s.role}</td><td className="px-3 py-2 text-surface-600">{s.interest}</td><td className="px-3 py-2 text-surface-600">{s.influence}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </ContentPanel>

        <ContentPanel id="scope">
          <SectionHeading title="6. Scope" />
          <div className="grid gap-4 text-sm sm:grid-cols-2">
            <div><strong className="text-green-700">In Scope:</strong><ul className="mt-1 list-inside list-disc text-surface-600"><li>Shift-status visibility</li><li>Staffing-gap identification</li><li>Missed-shift and late-arrival tracking</li><li>Documentation tracking</li><li>Escalation tracking</li><li>KPI reporting</li></ul></div>
            <div><strong className="text-red-700">Out of Scope:</strong><ul className="mt-1 list-inside list-disc text-surface-600"><li>Payroll, billing, EHR</li><li>Clinical decision-making</li><li>Real client records</li><li>Production deployment</li><li>Real-time GPS tracking</li></ul></div>
          </div>
        </ContentPanel>

        <ContentPanel id="requirements">
          <SectionHeading title="9. Business Requirements" />
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-surface-200 text-sm">
              <thead className="bg-surface-50"><tr><th className="px-3 py-2 text-left font-medium text-surface-600">ID</th><th className="px-3 py-2 text-left font-medium text-surface-600">Statement</th><th className="px-3 py-2 text-left font-medium text-surface-600">Priority</th></tr></thead>
              <tbody className="divide-y divide-surface-100">
                {businessRequirements.map((r) => (
                  <tr key={r.id} className="hover:bg-surface-50"><td className="px-3 py-2 font-mono text-xs text-surface-400">{r.id}</td><td className="px-3 py-2 text-surface-700">{r.statement}</td><td className="px-3 py-2">{r.priority}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-xs text-surface-400">Plus 18 functional requirements (FR-001 through FR-018) and 12 nonfunctional requirements (NFR-001 through NFR-012).</p>
        </ContentPanel>

        <ContentPanel id="kpis">
          <SectionHeading title="10. Key Performance Indicators" />
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-surface-200 text-sm">
              <thead className="bg-surface-50"><tr><th className="px-3 py-2 text-left font-medium text-surface-600">KPI</th><th className="px-3 py-2 text-left font-medium text-surface-600">Value</th><th className="px-3 py-2 text-left font-medium text-surface-600">Target</th></tr></thead>
              <tbody className="divide-y divide-surface-100">
                {[
                  { name: "Shift Fill Rate", val: `${kpis.shiftFillRate.value}%`, tgt: "95%" },
                  { name: "Missed Shift Rate", val: `${kpis.missedShiftRate.value}%`, tgt: "< 2%" },
                  { name: "Late Arrival Rate", val: `${kpis.lateArrivalRate.value}%`, tgt: "< 10%" },
                  { name: "Avg Escalation Time", val: `${kpis.averageEscalationTime.value}m`, tgt: "< 30m" },
                  { name: "Doc Completion Rate", val: `${kpis.documentationCompletionRate.value}%`, tgt: "95%" },
                  { name: "Open Gaps", val: `${kpis.openStaffingGaps.value}`, tgt: "< 3" },
                  { name: "Resolution Time", val: `${kpis.issueResolutionTime.value}h`, tgt: "< 4h" },
                  { name: "Follow-Up Rate", val: `${kpis.followUpCompletionRate.value}%`, tgt: "90%" },
                ].map((k) => (
                  <tr key={k.name} className="hover:bg-surface-50"><td className="px-3 py-2 text-surface-700">{k.name}</td><td className="px-3 py-2 font-medium">{k.val}</td><td className="px-3 py-2 text-surface-500">{k.tgt}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
        </ContentPanel>

        <ContentPanel id="risks">
          <SectionHeading title="11. Risk Summary" />
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-surface-200 text-sm">
              <thead className="bg-surface-50"><tr><th className="px-3 py-2 text-left font-medium text-surface-600">ID</th><th className="px-3 py-2 text-left font-medium text-surface-600">Description</th><th className="px-3 py-2 text-left font-medium text-surface-600">Score</th></tr></thead>
              <tbody className="divide-y divide-surface-100">
                {risks.slice(0, 8).map((r) => (
                  <tr key={r.id} className="hover:bg-surface-50"><td className="px-3 py-2 font-mono text-xs text-surface-400">{r.id}</td><td className="px-3 py-2 text-surface-700">{r.description}</td><td className="px-3 py-2 font-medium">{r.riskScore}</td></tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-xs text-surface-400">Full risk register with all 15 risks available in the Risk Register view.</p>
        </ContentPanel>

        <ContentPanel id="assumptions">
          <SectionHeading title="12. Assumptions and Constraints" />
          <p className="text-sm text-surface-600"><strong>Key assumptions:</strong> All data is synthetic; recruiters have limited review time; no authentication required; zero operational cost for core functionality; portfolio demonstration only.</p>
          <p className="mt-2 text-sm text-surface-600"><strong>Key constraints:</strong> No real data; no paid API dependency; no production deployment; solo developer timeline; simple technology stack.</p>
        </ContentPanel>

        <ContentPanel>
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-sm text-yellow-800">
            <strong>Portfolio Simulation Notice:</strong> This BRD is a portfolio case study demonstrating Business Analyst documentation skills. It does not represent an approved or implemented business requirements document for a real organization. No employer approval or signature is claimed.
          </div>
        </ContentPanel>
      </div>
    </div>
  );
}
