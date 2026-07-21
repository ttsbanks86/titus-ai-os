"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { gaps } from "@/data/content/gaps-data";

const dimensions = [...new Set(gaps.map((g) => g.dimension))];
const severityCounts = {
  Critical: gaps.filter((g) => g.severity === "Critical").length,
  High: gaps.filter((g) => g.severity === "High").length,
  Medium: gaps.filter((g) => g.severity === "Medium").length,
};

export default function AnalysisPage() {
  const [selectedDim, setSelectedDim] = useState<string | null>(null);
  const [expandedGap, setExpandedGap] = useState<string | null>(null);

  const filtered = selectedDim ? gaps.filter((g) => g.dimension === selectedDim) : gaps;

  return (
    <div className="content-container py-8">
      <PageHeading title="Gap Analysis" subtitle="22 pain points identified across 9 business dimensions" />

      {/* Summary Cards */}
      <div className="mb-6 grid grid-cols-3 gap-3">
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-center">
          <div className="text-2xl font-bold text-red-700">{severityCounts.Critical}</div>
          <div className="text-xs font-medium text-red-600">Critical Gaps</div>
        </div>
        <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-center">
          <div className="text-2xl font-bold text-yellow-700">{severityCounts.High}</div>
          <div className="text-xs font-medium text-yellow-600">High Priority</div>
        </div>
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-4 text-center">
          <div className="text-2xl font-bold text-blue-700">{severityCounts.Medium}</div>
          <div className="text-xs font-medium text-blue-600">Medium Priority</div>
        </div>
      </div>

      {/* Dimension Filter */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Filter by Dimension" description="Select a business area to focus on specific gaps" />
        <div className="flex flex-wrap gap-2">
          <button onClick={() => setSelectedDim(null)} className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${!selectedDim ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>All</button>
          {dimensions.map((d) => (
            <button key={d} onClick={() => setSelectedDim(d)} className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${selectedDim === d ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{d} ({gaps.filter((g) => g.dimension === d).length})</button>
          ))}
        </div>
      </ContentPanel>

      {/* Gap List */}
      <div className="space-y-2">
        {filtered.map((gap, i) => (
          <ContentPanel key={i}>
            <button
              onClick={() => setExpandedGap(expandedGap === `${gap.dimension}-${i}` ? null : `${gap.dimension}-${i}`)}
              className="flex w-full items-center justify-between text-left"
              aria-expanded={expandedGap === `${gap.dimension}-${i}`}
            >
              <div className="flex items-center gap-3">
                <StatusBadge label={gap.severity} variant={gap.severity === "Critical" ? "error" : gap.severity === "High" ? "warning" : "info"} />
                <div>
                  <span className="text-xs text-surface-400">{gap.dimension}</span>
                  <span className="ml-2 font-medium text-surface-800">{gap.problem}</span>
                </div>
              </div>
              {expandedGap === `${gap.dimension}-${i}` ? <ChevronUp className="h-4 w-4 text-surface-400" /> : <ChevronDown className="h-4 w-4 text-surface-400" />}
            </button>
            {expandedGap === `${gap.dimension}-${i}` && (
              <div className="mt-3 grid gap-3 border-t border-surface-100 pt-3 text-sm sm:grid-cols-2">
                <div><span className="font-medium text-surface-700">Root Cause:</span><p className="text-surface-600">{gap.rootCause}</p></div>
                <div><span className="font-medium text-surface-700">Business Impact:</span><p className="text-surface-600">{gap.impact}</p></div>
                <div><span className="font-medium text-green-700">Proposed Future State:</span><p className="text-surface-600">{gap.futureState}</p></div>
                <div><span className="font-medium text-brand-700">Linked Requirement:</span><p className="text-surface-600">{gap.linkedBr}</p></div>
              </div>
            )}
          </ContentPanel>
        ))}
      </div>

      {/* Gap Summary Table */}
      <div className="mt-6">
        <ContentPanel>
          <SectionHeading title="Gap Summary by Dimension" description="Current state vs. target state comparison" />
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-surface-200 text-sm">
              <thead className="bg-surface-50">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-surface-600">Dimension</th>
                  <th className="px-3 py-2 text-left font-medium text-red-600">Current State</th>
                  <th className="px-3 py-2 text-left font-medium text-green-600">Target State</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-surface-100">
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">Shift Visibility</td><td className="px-3 py-2 text-red-600">Manual spreadsheets</td><td className="px-3 py-2 text-green-600">Real-time dashboard</td></tr>
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">Gap Detection</td><td className="px-3 py-2 text-red-600">Reactive discovery</td><td className="px-3 py-2 text-green-600">Proactive alerts</td></tr>
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">Escalation</td><td className="px-3 py-2 text-red-600">Informal phone/email</td><td className="px-3 py-2 text-green-600">Structured with severity</td></tr>
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">Documentation</td><td className="px-3 py-2 text-red-600">No tracking</td><td className="px-3 py-2 text-green-600">Status dashboard</td></tr>
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">Issue Follow-Up</td><td className="px-3 py-2 text-red-600">Ad-hoc</td><td className="px-3 py-2 text-green-600">Assigned ownership</td></tr>
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">KPI Reporting</td><td className="px-3 py-2 text-red-600">None</td><td className="px-3 py-2 text-green-600">Defined metrics</td></tr>
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">Audit Trail</td><td className="px-3 py-2 text-red-600">None</td><td className="px-3 py-2 text-green-600">System logs</td></tr>
                <tr className="hover:bg-surface-50"><td className="px-3 py-2 font-medium">Client Notifications</td><td className="px-3 py-2 text-red-600">Phone calls</td><td className="px-3 py-2 text-green-600">Structured process</td></tr>
              </tbody>
            </table>
          </div>
        </ContentPanel>
      </div>

      <div className="mt-6 flex justify-between">
        <a href="/current-state" className="text-sm font-medium text-brand-600 hover:text-brand-700">← Current State</a>
        <a href="/dashboard" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: KPI Dashboard →</a>
      </div>
    </div>
  );
}
