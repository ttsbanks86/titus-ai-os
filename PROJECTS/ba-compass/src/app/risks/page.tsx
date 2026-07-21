"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { risks, riskCategorySummary } from "@/data/content/risks-data";

export default function RisksPage() {
  const [expandedRisk, setExpandedRisk] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const filtered = selectedCategory ? risks.filter((r) => r.category === selectedCategory) : risks;

  return (
    <div className="content-container py-8">
      <PageHeading title="Risk Register" subtitle="15 identified risks with mitigation and contingency strategies" />

      {/* Summary */}
      <div className="mb-6 grid grid-cols-3 gap-3 sm:grid-cols-5">
        <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-center">
          <div className="text-lg font-bold text-red-700">{risks.filter((r) => r.riskLevel === "High").length}</div>
          <div className="text-xs text-red-600">High</div>
        </div>
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-3 text-center">
          <div className="text-lg font-bold text-yellow-700">{risks.filter((r) => r.riskLevel === "Medium").length}</div>
          <div className="text-xs text-yellow-600">Medium</div>
        </div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-3 text-center">
          <div className="text-lg font-bold text-green-700">{risks.filter((r) => r.riskLevel === "Low").length}</div>
          <div className="text-xs text-green-600">Low</div>
        </div>
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-3 text-center sm:col-span-2">
          <div className="text-lg font-bold text-blue-700">{risks.length}</div>
          <div className="text-xs text-blue-600">Total Risks</div>
        </div>
      </div>

      {/* Risk Heatmap */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Risk Heatmap" description="Likelihood vs. Impact matrix showing risk distribution" />
        <div className="overflow-x-auto" role="img" aria-label="Risk matrix with likelihood on Y-axis and impact on X-axis. High risks: scope growth, incorrect KPI calculations, poor recruiter usability.">
          <table className="min-w-full border-collapse text-xs">
            <thead>
              <tr><th className="p-1"></th><th className="p-1 text-center text-surface-500">Impact: Low (1-2)</th><th className="p-1 text-center text-surface-500">Impact: Med (3)</th><th className="p-1 text-center text-surface-500">Impact: High (4-5)</th></tr>
            </thead>
            <tbody>
              {[
                { label: "Likelihood: High (4-5)", impacts: ["low", "medium", "high"], risks: ["", "R-013 (8)", "R-001 (12), R-006 (12)"] },
                { label: "Likelihood: Med (3)", impacts: ["low", "medium", "high"], risks: ["R-004 (4)", "R-005 (9), R-007 (9), R-008 (9), R-009 (9), R-012 (9), R-014 (9), R-015 (9)", "R-002 (12)"] },
                { label: "Likelihood: Low (1-2)", impacts: ["low", "medium", "high"], risks: ["", "R-003 (8), R-010 (8), R-011 (8)", ""] },
              ].map((row, i) => (
                <tr key={i}>
                  <td className="whitespace-nowrap p-1 text-surface-500">{row.label}</td>
                  {row.impacts.map((level, j) => (
                    <td key={j} className={`p-2 text-center align-top ${level === "high" ? "bg-red-100" : level === "medium" ? "bg-yellow-100" : "bg-green-100"}`}>
                      {row.risks[j] ? <span className="text-[10px] text-surface-700">{row.risks[j]}</span> : <span className="text-surface-300">—</span>}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-2 flex items-center gap-3 text-xs text-surface-400">
          <span className="flex items-center gap-1"><span className="inline-block h-3 w-3 rounded bg-green-100" /> Low</span>
          <span className="flex items-center gap-1"><span className="inline-block h-3 w-3 rounded bg-yellow-100" /> Medium</span>
          <span className="flex items-center gap-1"><span className="inline-block h-3 w-3 rounded bg-red-100" /> High</span>
        </div>
      </ContentPanel>

      {/* Category Filter */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Filter by Category" />
        <div className="flex flex-wrap gap-2">
          <button onClick={() => setSelectedCategory(null)} className={`rounded-full px-3 py-1 text-xs font-medium ${!selectedCategory ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>All</button>
          {riskCategorySummary.map((c) => (
            <button key={c.category} onClick={() => setSelectedCategory(c.category)} className={`rounded-full px-3 py-1 text-xs font-medium ${selectedCategory === c.category ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{c.category} ({c.count})</button>
          ))}
        </div>
      </ContentPanel>

      {/* Risk List */}
      <div className="space-y-2">
        {filtered.map((risk) => (
          <ContentPanel key={risk.id}>
            <button
              onClick={() => setExpandedRisk(expandedRisk === risk.id ? null : risk.id)}
              className="flex w-full items-center justify-between text-left"
              aria-expanded={expandedRisk === risk.id}
            >
              <div className="flex items-center gap-3">
                <StatusBadge label={risk.riskLevel} variant={risk.riskLevel === "High" ? "error" : risk.riskLevel === "Medium" ? "warning" : "success"} />
                <div>
                  <span className="font-mono text-xs text-surface-400">{risk.id}</span>
                  <span className="ml-2 text-xs text-surface-400">{risk.category}</span>
                  <p className="text-sm font-medium text-surface-800">{risk.description}</p>
                </div>
                <div className="ml-auto flex items-center gap-1">
                  <span className="text-lg font-bold text-surface-600">{risk.riskScore}</span>
                </div>
              </div>
              {expandedRisk === risk.id ? <ChevronUp className="h-4 w-4 shrink-0 text-surface-400" /> : <ChevronDown className="h-4 w-4 shrink-0 text-surface-400" />}
            </button>
            {expandedRisk === risk.id && (
              <div className="mt-3 grid gap-3 border-t border-surface-100 pt-3 text-sm sm:grid-cols-2">
                <div><span className="font-medium text-surface-700">Likelihood:</span><span className="ml-1 text-surface-600">{risk.likelihood}/5</span></div>
                <div><span className="font-medium text-surface-700">Impact:</span><span className="ml-1 text-surface-600">{risk.impact}/5</span></div>
                <div><span className="font-medium text-surface-700">Owner:</span><span className="ml-1 text-surface-600">{risk.owner}</span></div>
                <div><span className="font-medium text-surface-700">Status:</span><span className="ml-1 text-surface-600">{risk.status}</span></div>
                <div className="sm:col-span-2"><span className="font-medium text-green-700">Mitigation:</span><p className="text-surface-600">{risk.mitigation}</p></div>
                <div className="sm:col-span-2"><span className="font-medium text-amber-700">Contingency:</span><p className="text-surface-600">{risk.contingency}</p></div>
                <div className="sm:col-span-2"><span className="font-medium text-surface-700">Trigger:</span><p className="text-surface-600">{risk.trigger}</p></div>
              </div>
            )}
          </ContentPanel>
        ))}
      </div>

      {/* Category Summary Table */}
      <div className="mt-6">
        <ContentPanel>
          <SectionHeading title="Risk Categories" description="Distribution of risks across categories" />
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-surface-200 text-sm">
              <thead className="bg-surface-50">
                <tr><th className="px-3 py-2 text-left font-medium text-surface-600">Category</th><th className="px-3 py-2 text-left font-medium text-surface-600">Count</th><th className="px-3 py-2 text-left font-medium text-surface-600">Risk IDs</th></tr>
              </thead>
              <tbody className="divide-y divide-surface-100">
                {riskCategorySummary.map((c) => (
                  <tr key={c.category} className="hover:bg-surface-50">
                    <td className="px-3 py-2 font-medium text-surface-700">{c.category}</td>
                    <td className="px-3 py-2">{c.count}</td>
                    <td className="px-3 py-2 font-mono text-xs text-surface-500">{c.ids}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </ContentPanel>
      </div>

      <div className="mt-6 flex justify-between">
        <a href="/requirements" className="text-sm font-medium text-brand-600 hover:text-brand-700">← Requirements</a>
        <a href="/recommendations" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: Recommendations →</a>
      </div>
    </div>
  );
}
