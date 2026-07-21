"use client";

import { useState } from "react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import {
  businessRequirements,
  functionalRequirements,
  nonfunctionalRequirements,
} from "@/data/content/requirements-data";

type ReqType = "all" | "br" | "fr" | "nfr";
type PriorityFilter = "all" | "High" | "Medium" | "Low";

export default function RequirementsPage() {
  const [reqType, setReqType] = useState<ReqType>("all");
  const [priority, setPriority] = useState<PriorityFilter>("all");
  const [search, setSearch] = useState("");
  const [showStories, setShowStories] = useState(false);

  const allRendered = () => {
    let items: { id: string; statement: string; priority: string; type: string }[] = [];
    if (reqType === "all" || reqType === "br") items.push(...businessRequirements.map((r) => ({ id: r.id, statement: r.statement, priority: r.priority, type: "BR" })));
    if (reqType === "all" || reqType === "fr") items.push(...functionalRequirements.map((r) => ({ id: r.id, statement: r.statement, priority: r.priority, type: "FR" })));
    if (reqType === "all" || reqType === "nfr") items.push(...nonfunctionalRequirements.map((r) => ({ id: r.id, statement: r.statement, priority: r.priority, type: "NFR" })));
    if (priority !== "all") items = items.filter((i) => i.priority === priority);
    if (search) items = items.filter((i) => i.id.toLowerCase().includes(search.toLowerCase()) || i.statement.toLowerCase().includes(search.toLowerCase()));
    return items;
  };

  const rendered = allRendered();

  const counts = {
    br: { total: businessRequirements.length, high: businessRequirements.filter((r) => r.priority === "High").length },
    fr: { total: functionalRequirements.length, high: functionalRequirements.filter((r) => r.priority === "High").length },
    nfr: { total: nonfunctionalRequirements.length, high: nonfunctionalRequirements.filter((r) => r.priority === "High").length },
  };

  // User stories data
  const userStories = [
    { id: "US-001", role: "Recruiter", capability: "Access the demo without creating an account", value: "Evaluate portfolio without barriers", priority: "High" as const, linkedBr: "BR-013" },
    { id: "US-002", role: "Recruiter", capability: "See a clear business scenario explained", value: "Understand context of the analysis", priority: "High" as const, linkedBr: "BR-001" },
    { id: "US-003", role: "Recruiter", capability: "See stakeholder analysis", value: "Evaluate stakeholder engagement skills", priority: "High" as const, linkedBr: "BR-001" },
    { id: "US-004", role: "Recruiter", capability: "See current-state and future-state process maps", value: "Assess process analysis skills", priority: "High" as const, linkedBr: "BR-001, BR-002" },
    { id: "US-005", role: "Recruiter", capability: "See a complete requirements traceability matrix", value: "Evaluate analytical thoroughness", priority: "High" as const, linkedBr: "BR-001 through BR-015" },
    { id: "US-006", role: "Recruiter", capability: "See KPI definitions and calculated metrics", value: "Assess data-driven analysis skills", priority: "High" as const, linkedBr: "BR-008" },
    { id: "US-007", role: "Recruiter", capability: "See a professional BRD", value: "Evaluate documentation quality", priority: "High" as const, linkedBr: "BR-001 through BR-015" },
    { id: "US-008", role: "Recruiter", capability: "Demo works on my phone", value: "Review on the go", priority: "Medium" as const, linkedBr: "BR-015" },
    { id: "US-009", role: "Hiring Manager", capability: "See acceptance criteria in Given/When/Then format", value: "Evaluate requirement specification quality", priority: "High" as const, linkedBr: "BR-001 through BR-015" },
    { id: "US-010", role: "Hiring Manager", capability: "See a risk register with mitigations", value: "Assess risk management skills", priority: "High" as const, linkedBr: "BR-009" },
    { id: "US-011", role: "Ops Manager", capability: "See shift status at a glance", value: "Identify at-risk shifts quickly", priority: "High" as const, linkedBr: "BR-001, BR-006" },
    { id: "US-012", role: "Ops Manager", capability: "See KPI trends over time", value: "Identify improvement or decline patterns", priority: "High" as const, linkedBr: "BR-008" },
  ];

  return (
    <div className="content-container py-8">
      <PageHeading title="Requirements Management" subtitle="45 requirements across 3 categories with full traceability" />

      {/* Summary Cards */}
      <div className="mb-6 grid gap-3 sm:grid-cols-3">
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-4">
          <div className="text-xs font-medium text-blue-600">Business Requirements</div>
          <div className="text-2xl font-bold text-blue-700">{counts.br.total}</div>
          <div className="text-xs text-blue-500">{counts.br.high} high priority</div>
        </div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <div className="text-xs font-medium text-green-600">Functional Requirements</div>
          <div className="text-2xl font-bold text-green-700">{counts.fr.total}</div>
          <div className="text-xs text-green-500">{counts.fr.high} high priority</div>
        </div>
        <div className="rounded-lg border border-purple-200 bg-purple-50 p-4">
          <div className="text-xs font-medium text-purple-600">Nonfunctional Requirements</div>
          <div className="text-2xl font-bold text-purple-700">{counts.nfr.total}</div>
          <div className="text-xs text-purple-500">{counts.nfr.high} high priority</div>
        </div>
      </div>

      {/* Filters */}
      <ContentPanel className="mb-6">
        <div className="flex flex-wrap gap-4">
          <div>
            <label className="text-xs font-medium text-surface-500">Type</label>
            <div className="mt-1 flex flex-wrap gap-1">
              {(["all", "br", "fr", "nfr"] as const).map((t) => (
                <button key={t} onClick={() => setReqType(t)} className={`rounded px-2.5 py-1 text-xs font-medium ${reqType === t ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{t === "all" ? "All" : t.toUpperCase()}</button>
              ))}
            </div>
          </div>
          <div>
            <label className="text-xs font-medium text-surface-500">Priority</label>
            <div className="mt-1 flex flex-wrap gap-1">
              {(["all", "High", "Medium", "Low"] as const).map((p) => (
                <button key={p} onClick={() => setPriority(p)} className={`rounded px-2.5 py-1 text-xs font-medium ${priority === p ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{p}</button>
              ))}
            </div>
          </div>
          <div>
            <label className="text-xs font-medium text-surface-500">Search</label>
            <input type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="ID or keyword..." className="mt-1 rounded border border-surface-300 px-2.5 py-1 text-xs focus:border-brand-500 focus:outline-none" aria-label="Search requirements" />
          </div>
        </div>
        <div className="mt-2 text-xs text-surface-400">{rendered.length} of {counts.br.total + counts.fr.total + counts.nfr.total} requirements shown</div>
      </ContentPanel>

      {/* Requirements Table */}
      <ContentPanel className="mb-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">ID</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Type</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Statement</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Priority</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {rendered.map((req) => (
                <tr key={req.id} className="hover:bg-surface-50">
                  <td className="whitespace-nowrap px-3 py-2 font-mono text-xs text-surface-400">{req.id}</td>
                  <td className="px-3 py-2"><StatusBadge label={req.type} variant={req.type === "BR" ? "info" : req.type === "FR" ? "success" : "neutral"} /></td>
                  <td className="px-3 py-2 text-surface-700">{req.statement}</td>
                  <td className="px-3 py-2"><StatusBadge label={req.priority} variant={req.priority === "High" ? "error" : req.priority === "Medium" ? "warning" : "success"} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </ContentPanel>

      {/* User Stories Toggle */}
      <ContentPanel>
        <button
          onClick={() => setShowStories(!showStories)}
          className="flex w-full items-center justify-between text-left"
          aria-expanded={showStories}
        >
          <SectionHeading title="User Stories and Acceptance Criteria" description="26 user stories organized by stakeholder role" />
          <span className="text-sm text-brand-600">{showStories ? "Hide" : "Show"}</span>
        </button>
        {showStories && (
          <div className="mt-4 space-y-2 border-t border-surface-100 pt-4">
            {userStories.map((story) => (
              <div key={story.id} className="rounded-lg border border-surface-200 p-3">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-surface-400">{story.id}</span>
                  <StatusBadge label={story.role} variant="info" />
                  <StatusBadge label={story.priority} variant={story.priority === "High" ? "error" : "warning"} />
                </div>
                <p className="mt-1 text-sm text-surface-700">
                  <strong>As a</strong> {story.role}, <strong>I want</strong> {story.capability}, <strong>so that</strong> {story.value}.
                </p>
                <div className="mt-1 text-xs text-surface-400">Linked: {story.linkedBr}</div>
              </div>
            ))}
            <div className="mt-3 rounded-lg border border-dashed border-surface-300 bg-surface-50 p-3">
              <p className="text-xs text-surface-500">
                <strong>Acceptance Criteria Example (AC-001):</strong><br />
                Given a recruiter navigates to the BA Compass application URL<br />
                When the application loads<br />
                Then the application displays content without any login prompt or authentication barrier
              </p>
            </div>
            <p className="mt-2 text-xs text-surface-400">Showing 12 of 26 approved user stories. Full set available in docs/13-user-stories.md and docs/14-acceptance-criteria.md.</p>
          </div>
        )}
      </ContentPanel>

      <div className="mt-6 flex justify-between">
        <a href="/future-state" className="text-sm font-medium text-brand-600 hover:text-brand-700">← Future State</a>
        <a href="/risks" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: Risks →</a>
      </div>
    </div>
  );
}
