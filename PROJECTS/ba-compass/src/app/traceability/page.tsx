"use client";

import { useState, useMemo } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { downloadText, downloadCsv } from "@/lib/export";

const traceabilityData = [
  { id: "T-001", businessProblem: "Missed shifts discovered reactively", stakeholder: "Operations Manager", br: "BR-001", fr: "FR-001", userStory: "US-013", ac: "AC-012", kpi: "KPI-001", feature: "Shift status dashboard", test: "Verify shift counts match data", status: "Implemented" as const },
  { id: "T-002", businessProblem: "Open gaps invisible until client impact", stakeholder: "Scheduling Coordinator", br: "BR-002", fr: "FR-004", userStory: "US-015", ac: "AC-013", kpi: "KPI-006", feature: "Gap highlight with details", test: "Verify gap count matches data", status: "Implemented" as const },
  { id: "T-003", businessProblem: "Delayed escalation with no audit trail", stakeholder: "Care Coordinator", br: "BR-003", fr: "FR-005", userStory: "US-022", ac: "AC-020", kpi: "KPI-004", feature: "Escalation timeline view", test: "Verify escalation time calculations", status: "Implemented" as const },
  { id: "T-004", businessProblem: "Repeated manual follow-up", stakeholder: "Care Coordinator", br: "BR-004", fr: "FR-010", userStory: "US-024", ac: "AC-011", kpi: "KPI-008", feature: "Risk register with follow-up tracking", test: "Verify follow-up calculation", status: "Implemented" as const },
  { id: "T-005", businessProblem: "Incomplete service documentation", stakeholder: "QA Lead", br: "BR-005", fr: "FR-001", userStory: "US-021", ac: "AC-019", kpi: "KPI-005", feature: "Dashboard doc completion metric", test: "Verify doc rate calculation", status: "Implemented" as const },
  { id: "T-006", businessProblem: "No single source of truth", stakeholder: "Operations Manager", br: "BR-006", fr: "FR-001", userStory: "US-013", ac: "AC-012", kpi: "KPI-001-KPI-008", feature: "Consolidated dashboard", test: "Verify data consolidation", status: "Implemented" as const },
  { id: "T-007", businessProblem: "Clients not notified of changes", stakeholder: "Client Services Rep", br: "BR-007", fr: "FR-007", userStory: "US-002", ac: "AC-002", kpi: "KPI-001 (indirect)", feature: "Requirements table", test: "Verify requirements display", status: "Implemented" as const },
  { id: "T-008", businessProblem: "No operational KPI dashboard", stakeholder: "Agency Owner", br: "BR-008", fr: "FR-011", userStory: "US-006", ac: "AC-006", kpi: "KPI-001-KPI-008", feature: "KPI dashboard with trends", test: "Verify KPI calculation", status: "Implemented" as const },
  { id: "T-009", businessProblem: "Late arrivals not tracked", stakeholder: "Operations Manager", br: "BR-011", fr: "FR-001", userStory: "US-017", ac: "AC-015", kpi: "KPI-003", feature: "Late arrival metric on dashboard", test: "Verify late arrival calculation", status: "Implemented" as const },
  { id: "T-010", businessProblem: "Recruiters need barrier-free access", stakeholder: "Agency Owner", br: "BR-013", fr: "FR-018", userStory: "US-001", ac: "AC-001", kpi: "N/A", feature: "Public app without auth", test: "Verify no auth prompt", status: "Implemented" as const },
  { id: "T-011", businessProblem: "Synthetic data must be labeled", stakeholder: "Compliance Rep", br: "BR-014", fr: "NFR-012", userStory: "US-002", ac: "AC-023", kpi: "N/A", feature: "Disclaimer on every page", test: "Visual inspection", status: "Implemented" as const },
  { id: "T-012", businessProblem: "Mobile accessibility for recruiters", stakeholder: "IT Administrator", br: "BR-015", fr: "NFR-003", userStory: "US-008", ac: "AC-008", kpi: "N/A", feature: "Responsive design", test: "Viewport testing", status: "Implemented" as const },
  { id: "T-013", businessProblem: "Management needs concise overview", stakeholder: "Agency Owner", br: "BR-008", fr: "FR-012", userStory: "US-023", ac: "AC-018", kpi: "KPI-001-KPI-008", feature: "Executive summary", test: "Verify summary renders", status: "Implemented" as const },
  { id: "T-014", businessProblem: "No structured risk identification", stakeholder: "Agency Owner", br: "BR-009", fr: "FR-010", userStory: "US-011", ac: "AC-011", kpi: "N/A", feature: "Risk register", test: "Verify all risks display", status: "Implemented" as const },
  { id: "T-015", businessProblem: "Need centralized requirements document", stakeholder: "Agency Owner", br: "BR-001-BR-015", fr: "FR-013", userStory: "US-007", ac: "AC-007", kpi: "N/A", feature: "BRD view", test: "Verify BRD renders", status: "Implemented" as const },
];

export default function TraceabilityPage() {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [expandedRow, setExpandedRow] = useState<string | null>(null);

  const filtered = useMemo(() => {
    let items = [...traceabilityData];
    if (statusFilter !== "all") items = items.filter((t) => t.status === statusFilter);
    if (search) items = items.filter((t) =>
      t.id.toLowerCase().includes(search.toLowerCase()) ||
      t.br.toLowerCase().includes(search.toLowerCase()) ||
      t.businessProblem.toLowerCase().includes(search.toLowerCase()) ||
      t.kpi.toLowerCase().includes(search.toLowerCase())
    );
    return items;
  }, [search, statusFilter]);

  const coverageCount = traceabilityData.length;
  const implementedCount = traceabilityData.filter((t) => t.status === "Implemented").length;
  const highPriorityCoverage = traceabilityData.filter((t) => t.id <= "T-010").length;

  const handleExportMd = () => {
    const mdLines = traceabilityData.map((t) =>
      `| ${t.id} | ${t.businessProblem} | ${t.br} | ${t.fr} | ${t.userStory} | ${t.ac} | ${t.kpi} | ${t.status} |`
    ).join("\n");
    const md = `# BA Compass — Traceability Matrix\n**Generated:** ${new Date().toISOString().split("T")[0]}\n**DISCLAIMER:** All data is synthetic.\n\n| ID | Business Problem | BR | FR | User Story | AC | KPI | Status |\n|----|-----------------|-----|-----|-----------|-----|-----|--------|\n${mdLines}`;
    downloadText(md, "ba-compass-traceability.md");
  };

  const handleExportCsv = () => {
    const rows = traceabilityData.map((t) =>
      [t.id, t.businessProblem, t.br, t.fr, t.userStory, t.ac, t.kpi, t.status].join(",")
    ).join("\n");
    const csv = `ID,Business Problem,BR,FR,User Story,AC,KPI,Status\n${rows}\n\nDISCLAIMER: All data is synthetic.`;
    downloadCsv(csv, "ba-compass-traceability.csv");
  };

  return (
    <div className="content-container py-8">
      <div className="flex items-center justify-between">
        <PageHeading title="Requirements Traceability Matrix" subtitle="End-to-end traceability from business problem through implementation" />
        <div className="flex gap-2">
          <button onClick={handleExportMd} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Export MD</button>
          <button onClick={handleExportCsv} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Export CSV</button>
          <button onClick={() => window.print()} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Print</button>
        </div>
      </div>

      {/* Coverage Summary */}
      <div className="mb-6 grid gap-3 sm:grid-cols-3">
        <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-center">
          <div className="text-lg font-bold text-green-700">{coverageCount}</div>
          <div className="text-xs text-green-600">Total Traceability Links</div>
        </div>
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-3 text-center">
          <div className="text-lg font-bold text-blue-700">{implementedCount}</div>
          <div className="text-xs text-blue-600">Implemented / Displayed</div>
        </div>
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-center">
          <div className="text-lg font-bold text-amber-700">{traceabilityData.filter((t) => t.status === "Implemented" && t.kpi !== "N/A").length}</div>
          <div className="text-xs text-amber-600">KPI-Linked Items</div>
        </div>
      </div>

      {/* Filters */}
      <ContentPanel className="mb-6">
        <div className="flex flex-wrap gap-4">
          <div>
            <label className="text-xs font-medium text-surface-500">Search</label>
            <input type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="ID, problem, KPI..." className="mt-1 rounded border border-surface-300 px-2.5 py-1 text-xs focus:border-brand-500 focus:outline-none" aria-label="Search traceability" />
          </div>
          <div>
            <label className="text-xs font-medium text-surface-500">Status</label>
            <div className="mt-1 flex gap-1">
              {["all", "Implemented"].map((s) => (
                <button key={s} onClick={() => setStatusFilter(s)} className={`rounded px-2.5 py-1 text-xs font-medium ${statusFilter === s ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{s === "all" ? "All" : s}</button>
              ))}
            </div>
          </div>
          <div className="text-xs text-surface-400">Showing {filtered.length} of {coverageCount} links</div>
        </div>
      </ContentPanel>

      {/* Traceability Table */}
      <ContentPanel>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr><th className="px-3 py-2 text-left font-medium text-surface-600">ID</th><th className="px-3 py-2 text-left font-medium text-surface-600">Business Problem</th><th className="px-3 py-2 text-left font-medium text-surface-600">BR</th><th className="px-3 py-2 text-left font-medium text-surface-600">FR</th><th className="px-3 py-2 text-left font-medium text-surface-600">User Story</th><th className="px-3 py-2 text-left font-medium text-surface-600">AC</th><th className="px-3 py-2 text-left font-medium text-surface-600">KPI</th><th className="px-3 py-2 text-left font-medium text-surface-600">Status</th></tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {filtered.map((t) => (
                <tr key={t.id} className="hover:bg-surface-50">
                  <td className="px-3 py-2 font-mono text-xs text-surface-400">{t.id}</td>
                  <td className="max-w-xs px-3 py-2 text-surface-700">{t.businessProblem}</td>
                  <td className="px-3 py-2 font-mono text-xs text-brand-600">{t.br}</td>
                  <td className="px-3 py-2 font-mono text-xs text-surface-500">{t.fr}</td>
                  <td className="px-3 py-2 font-mono text-xs text-surface-500">{t.userStory}</td>
                  <td className="px-3 py-2 font-mono text-xs text-surface-500">{t.ac}</td>
                  <td className="px-3 py-2 font-mono text-xs text-surface-500">{t.kpi}</td>
                  <td className="px-3 py-2"><StatusBadge label={t.status} variant={t.status === "Implemented" ? "success" : "warning"} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {filtered.length === 0 && <p className="py-4 text-center text-sm text-surface-400">No traceability links match your search.</p>}
      </ContentPanel>

      <div className="mt-6 text-sm text-surface-400">
        <strong>Note:</strong> All 15 traceability links connect business problems through to implemented features. No unlinked high-priority features identified. Full traceability documentation available in docs/15-requirements-traceability-matrix.md.
      </div>
    </div>
  );
}
