"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { stakeholders, powerInterestMatrix, stakeholderConflicts } from "@/data/content/stakeholders";

export default function StakeholdersPage() {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  return (
    <div className="content-container py-8">
      <PageHeading title="Stakeholder Analysis" subtitle="10 fictional stakeholder roles at BrightCare Home Services" />

      {/* Power-Interest Matrix */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Power-Interest Matrix" description="Mapping stakeholders by influence and engagement priority" />
        <div className="grid gap-3 sm:grid-cols-2">
          {powerInterestMatrix.map((quadrant) => (
            <div key={quadrant.label} className={`rounded-lg border-2 p-4 ${
              quadrant.label === "Manage Closely" ? "border-red-300 bg-red-50" :
              quadrant.label === "Keep Satisfied" ? "border-blue-300 bg-blue-50" :
              quadrant.label === "Keep Informed" ? "border-yellow-300 bg-yellow-50" :
              "border-gray-300 bg-gray-50"
            }`}>
              <div className="text-xs font-semibold uppercase tracking-wider text-surface-500">{quadrant.x} · {quadrant.y}</div>
              <div className="mt-1 text-base font-bold">{quadrant.label}</div>
              <ul className="mt-2 list-inside list-disc text-sm text-surface-600">
                {quadrant.stakeholders.map((s) => <li key={s}>{s}</li>)}
              </ul>
            </div>
          ))}
        </div>
      </ContentPanel>

      {/* Stakeholder Register */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Stakeholder Register" description="All 10 stakeholders with roles, influence, and priorities" />
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">ID</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Role</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Interest</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Influence</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Approach</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {stakeholders.map((s) => (
                <tr key={s.id} className="hover:bg-surface-50">
                  <td className="px-3 py-2 font-mono text-xs text-surface-400">{s.id}</td>
                  <td className="px-3 py-2 font-medium text-surface-700">{s.role}</td>
                  <td className="px-3 py-2 text-surface-600">{s.interest}</td>
                  <td className="px-3 py-2">
                    <StatusBadge label={s.influence} variant={s.influence === "High" ? "error" : s.influence === "Medium" ? "warning" : "success"} />
                  </td>
                  <td className="px-3 py-2 text-surface-600">{s.priority}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ContentPanel>

      {/* Detailed Stakeholder Profiles */}
      <SectionHeading title="Stakeholder Details" description="Expand each stakeholder for full profile" />
      <div className="mb-6 space-y-2">
        {stakeholders.map((s) => (
          <ContentPanel key={s.id}>
            <button
              onClick={() => setExpandedId(expandedId === s.id ? null : s.id)}
              className="flex w-full items-center justify-between text-left"
              aria-expanded={expandedId === s.id}
              aria-controls={`detail-${s.id}`}
            >
              <div>
                <span className="font-mono text-xs text-surface-400">{s.id}</span>
                <span className="ml-2 font-medium text-surface-800">{s.role}</span>
                <span className="ml-2 text-xs text-surface-400">— {s.interest}</span>
              </div>
              {expandedId === s.id ? <ChevronUp className="h-4 w-4 text-surface-400" /> : <ChevronDown className="h-4 w-4 text-surface-400" />}
            </button>
            {expandedId === s.id && (
              <div id={`detail-${s.id}`} className="mt-3 grid gap-3 border-t border-surface-100 pt-3 text-sm sm:grid-cols-2 lg:grid-cols-3">
                <div><span className="font-medium text-surface-700">Needs:</span><p className="text-surface-600">{s.needs}</p></div>
                <div><span className="font-medium text-surface-700">Pain Points:</span><p className="text-surface-600">{s.painPoints}</p></div>
                <div><span className="font-medium text-surface-700">Decision Authority:</span><p className="text-surface-600">{s.decisionAuthority}</p></div>
                <div><span className="font-medium text-surface-700">Communication:</span><p className="text-surface-600">{s.communication}</p></div>
                <div><span className="font-medium text-surface-700">Responsibilities:</span><p className="text-surface-600">{s.responsibilities}</p></div>
                <div><span className="font-medium text-surface-700">Requirement Ownership:</span><p className="text-surface-600">{s.requirementOwnership}</p></div>
                <div className="sm:col-span-2 lg:col-span-3"><span className="font-medium text-red-600">Risks/Concerns:</span><p className="text-surface-600">{s.risks}</p></div>
              </div>
            )}
          </ContentPanel>
        ))}
      </div>

      {/* Stakeholder Conflicts */}
      <ContentPanel>
        <SectionHeading title="Stakeholder Conflict Resolution" description="How conflicting needs between stakeholder groups would be handled" />
        <div className="space-y-3">
          {stakeholderConflicts.map((conflict, i) => (
            <div key={i} className="rounded-lg border border-surface-200 p-3">
              <div className="font-medium text-surface-700">{conflict.parties}</div>
              <div className="mt-1 text-sm text-surface-600"><strong>Issue:</strong> {conflict.issue}</div>
              <div className="mt-1 text-sm text-green-700"><strong>Resolution:</strong> {conflict.resolution}</div>
            </div>
          ))}
        </div>
        <div className="mt-4 text-sm text-surface-500">
          <strong>Conflict resolution process:</strong> Identify specific conflict → Document both perspectives →
          Evaluate impact on objectives → Facilitate structured discussion → Seek compromise →
          Escalate to Agency Owner if no consensus → Document decision in decision log.
        </div>
      </ContentPanel>
    </div>
  );
}
