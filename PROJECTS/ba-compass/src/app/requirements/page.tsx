"use client";

import { useState, useMemo } from "react";
import { Pencil, X, Check, RotateCcw, Download } from "lucide-react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { StatusBadge } from "@/components/ui/status-badge";
import { DemoReset } from "@/components/shared/demo-reset";
import { businessRequirements, functionalRequirements, nonfunctionalRequirements } from "@/data/content/requirements-data";
import { useRequirements } from "@/lib/state/requirements-store";
import { validateFullRequirement, type ValidationError } from "@/lib/validation";
import { requirementsToMarkdown, requirementsToCsv, downloadText, downloadCsv } from "@/lib/export";

type ReqType = "all" | "br" | "fr" | "nfr";
type PriorityFilter = "all" | "High" | "Medium" | "Low";

export default function RequirementsPage() {
  const { state, enterEditMode, exitEditMode, updateRequirement, resetRequirement, resetAll } = useRequirements();
  const [reqType, setReqType] = useState<ReqType>("all");
  const [priority, setPriority] = useState<PriorityFilter>("all");
  const [search, setSearch] = useState("");
  const [showStories, setShowStories] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, ValidationError[]>>({});

  const allRendered = useMemo(() => {
    let items: { id: string; statement: string; priority: string; type: string; justification?: string; stakeholderOwner?: string; status?: string; relatedKpi?: string }[] = [];
    if (reqType === "all" || reqType === "br") {
      if (state.editMode) {
        items.push(...state.requirements.map((r) => ({ id: r.id, statement: r.statement, priority: r.priority, type: "BR", justification: r.justification, stakeholderOwner: r.stakeholderOwner, status: r.status, relatedKpi: r.relatedKpi })));
      } else {
        items.push(...businessRequirements.map((r) => ({ id: r.id, statement: r.statement, priority: r.priority, type: "BR" })));
      }
    }
    if (reqType === "all" || reqType === "fr") items.push(...functionalRequirements.map((r) => ({ id: r.id, statement: r.statement, priority: r.priority, type: "FR" })));
    if (reqType === "all" || reqType === "nfr") items.push(...nonfunctionalRequirements.map((r) => ({ id: r.id, statement: r.statement, priority: r.priority, type: "NFR" })));
    if (priority !== "all") items = items.filter((i) => i.priority === priority);
    if (search) items = items.filter((i) => i.id.toLowerCase().includes(search.toLowerCase()) || i.statement.toLowerCase().includes(search.toLowerCase()));
    return items;
  }, [reqType, priority, search, state.editMode, state.requirements]);

  const handleUpdate = (id: string, field: string, value: string) => {
    updateRequirement(id, field, value);
    // Clear validation for this field
    if (validationErrors[id]) {
      const remaining = validationErrors[id].filter((e) => e.field !== field);
      setValidationErrors((prev) => ({ ...prev, [id]: remaining }));
    }
  };

  const handleBlur = (id: string) => {
    const req = state.requirements.find((r) => r.id === id);
    if (!req) return;
    const result = validateFullRequirement({
      statement: req.statement,
      priority: req.priority,
      status: req.status,
      stakeholderOwner: req.stakeholderOwner,
      justification: req.justification,
      relatedKpi: req.relatedKpi,
    });
    setValidationErrors((prev) => ({ ...prev, [id]: result.errors }));
  };

  const handleExportMd = () => {
    const items = allRendered.map((r) => ({
      id: r.id,
      type: r.type,
      statement: r.statement,
      priority: r.priority,
      status: r.status || "Proposed",
      stakeholderOwner: r.stakeholderOwner || "",
      justification: r.justification || "",
      relatedKpi: r.relatedKpi || "",
      edited: state.editMode && state.requirements.find((re) => re.id === r.id)?._edited,
    }));
    downloadText(requirementsToMarkdown(items), "ba-compass-requirements.md");
  };

  const handleExportCsv = () => {
    const items = allRendered.map((r) => ({
      id: r.id,
      type: r.type,
      statement: r.statement,
      priority: r.priority,
      status: r.status || "Proposed",
      stakeholderOwner: r.stakeholderOwner || "",
      justification: r.justification || "",
      relatedKpi: r.relatedKpi || "",
      edited: state.editMode && state.requirements.find((re) => re.id === r.id)?._edited,
    }));
    downloadCsv(requirementsToCsv(items), "ba-compass-requirements.csv");
  };

  const editedCount = state.requirements.filter((r) => r._edited).length;

  const counts = {
    br: { total: businessRequirements.length, high: businessRequirements.filter((r) => r.priority === "High").length },
    fr: { total: functionalRequirements.length, high: functionalRequirements.filter((r) => r.priority === "High").length },
    nfr: { total: nonfunctionalRequirements.length, high: nonfunctionalRequirements.filter((r) => r.priority === "High").length },
  };

  return (
    <div className="content-container py-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <PageHeading title="Requirements Management" subtitle="45 requirements across 3 categories" />
        <div className="flex flex-wrap gap-2 no-print">
          {!state.editMode ? (
            <button onClick={enterEditMode} className="flex items-center gap-1 rounded-lg border border-brand-300 bg-white px-3 py-1.5 text-xs font-medium text-brand-700 hover:bg-brand-50"><Pencil className="h-3 w-3" /> Edit Demo</button>
          ) : (
            <button onClick={exitEditMode} className="flex items-center gap-1 rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50"><X className="h-3 w-3" /> Done Editing</button>
          )}
          <button onClick={handleExportMd} className="flex items-center gap-1 rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50"><Download className="h-3 w-3" /> MD</button>
          <button onClick={handleExportCsv} className="flex items-center gap-1 rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50"><Download className="h-3 w-3" /> CSV</button>
          <button onClick={() => window.print()} className="rounded-lg border border-surface-300 bg-white px-3 py-1.5 text-xs font-medium text-surface-700 hover:bg-surface-50">Print</button>
          <DemoReset onReset={resetAll} label="Reset All" />
        </div>
      </div>

      {state.editMode && (
        <div className="mb-4 rounded-lg border border-yellow-200 bg-yellow-50 p-2 text-xs text-yellow-800 no-print">
          <strong>Demo Edit Mode:</strong> Changes are stored locally in your browser. They do not modify the source project files.
          {editedCount > 0 && <span className="ml-1">{editedCount} requirement(s) edited.</span>}
        </div>
      )}

      {/* Summary Cards */}
      <div className="mb-6 grid gap-3 sm:grid-cols-3">
        <div className="rounded-lg border border-blue-200 bg-blue-50 p-4"><div className="text-xs font-medium text-blue-600">Business Requirements</div><div className="text-2xl font-bold text-blue-700">{counts.br.total}</div><div className="text-xs text-blue-500">{counts.br.high} high priority</div></div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-4"><div className="text-xs font-medium text-green-600">Functional Requirements</div><div className="text-2xl font-bold text-green-700">{counts.fr.total}</div><div className="text-xs text-green-500">{counts.fr.high} high priority</div></div>
        <div className="rounded-lg border border-purple-200 bg-purple-50 p-4"><div className="text-xs font-medium text-purple-600">Nonfunctional Requirements</div><div className="text-2xl font-bold text-purple-700">{counts.nfr.total}</div><div className="text-xs text-purple-500">{counts.nfr.high} high priority</div></div>
      </div>

      {/* Filters */}
      <ContentPanel className="mb-6">
        <div className="flex flex-wrap gap-4">
          <div><label className="text-xs font-medium text-surface-500">Type</label><div className="mt-1 flex flex-wrap gap-1">{(["all", "br", "fr", "nfr"] as const).map((t) => (<button key={t} onClick={() => setReqType(t)} className={`rounded px-2.5 py-1 text-xs font-medium ${reqType === t ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{t === "all" ? "All" : t.toUpperCase()}</button>))}</div></div>
          <div><label className="text-xs font-medium text-surface-500">Priority</label><div className="mt-1 flex flex-wrap gap-1">{(["all", "High", "Medium", "Low"] as const).map((p) => (<button key={p} onClick={() => setPriority(p)} className={`rounded px-2.5 py-1 text-xs font-medium ${priority === p ? "bg-brand-600 text-white" : "bg-surface-100 text-surface-600 hover:bg-surface-200"}`}>{p}</button>))}</div></div>
          <div><label className="text-xs font-medium text-surface-500">Search</label><input type="search" value={search} onChange={(e) => setSearch(e.target.value)} placeholder="ID or keyword..." className="mt-1 rounded border border-surface-300 px-2.5 py-1 text-xs focus:border-brand-500 focus:outline-none" aria-label="Search requirements" /></div>
        </div>
        <div className="mt-2 text-xs text-surface-400">{allRendered.length} of {(state.editMode ? state.requirements.length : 0) + counts.fr.total + counts.nfr.total || counts.br.total + counts.fr.total + counts.nfr.total} shown</div>
      </ContentPanel>

      {/* Requirements Table */}
      <ContentPanel className="mb-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr><th className="px-3 py-2 text-left font-medium text-surface-600">ID</th><th className="px-3 py-2 text-left font-medium text-surface-600">Type</th><th className="px-3 py-2 text-left font-medium text-surface-600">Statement</th><th className="px-3 py-2 text-left font-medium text-surface-600">Priority</th>{state.editMode && <th className="px-3 py-2 text-left font-medium text-surface-600">Actions</th>}</tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {allRendered.map((req) => {
                const isEditable = state.editMode && req.type === "BR";
                const editingReq = state.editMode ? state.requirements.find((r) => r.id === req.id) : null;
                const errors = validationErrors[req.id] || [];
                return (
                  <tr key={req.id} className="hover:bg-surface-50">
                    <td className="whitespace-nowrap px-3 py-2 font-mono text-xs text-surface-400">{req.id}</td>
                    <td className="px-3 py-2"><StatusBadge label={req.type} variant={req.type === "BR" ? "info" : req.type === "FR" ? "success" : "neutral"} /></td>
                    <td className="px-3 py-2 text-surface-700">
                      {isEditable && editingReq ? (
                        <div>
                          <textarea value={editingReq.statement} onChange={(e) => handleUpdate(req.id, "statement", e.target.value)} onBlur={() => handleBlur(req.id)} className="w-full rounded border border-surface-300 p-1 text-xs focus:border-brand-500 focus:outline-none" rows={2} aria-label={`Edit statement for ${req.id}`} />
                          <div className="mt-1 flex flex-wrap gap-1">
                            <select value={editingReq.priority} onChange={(e) => handleUpdate(req.id, "priority", e.target.value)} onBlur={() => handleBlur(req.id)} className="rounded border border-surface-300 px-1 py-0.5 text-[10px]" aria-label={`Priority for ${req.id}`}>
                              <option value="High">High</option><option value="Medium">Medium</option><option value="Low">Low</option>
                            </select>
                            <select value={editingReq.status} onChange={(e) => handleUpdate(req.id, "status", e.target.value)} onBlur={() => handleBlur(req.id)} className="rounded border border-surface-300 px-1 py-0.5 text-[10px]" aria-label={`Status for ${req.id}`}>
                              <option value="Proposed">Proposed</option><option value="Approved">Approved</option><option value="In Progress">In Progress</option><option value="Implemented">Implemented</option>
                            </select>
                            <button onClick={() => resetRequirement(req.id)} className="flex items-center gap-0.5 rounded bg-surface-100 px-1.5 py-0.5 text-[10px] text-surface-500 hover:bg-surface-200" aria-label={`Reset ${req.id}`}><RotateCcw className="h-2.5 w-2.5" /> Reset</button>
                          </div>
                          {errors.length > 0 && <div className="mt-1 text-[10px] text-red-600" role="alert">{errors.map((e) => <div key={e.field}>{e.message}</div>)}</div>}
                          {editingReq._edited && <div className="mt-0.5 text-[10px] text-amber-600">Local edit</div>}
                        </div>
                      ) : (
                        <span>{req.statement}{state.editMode && editingReq?._edited ? <span className="ml-1 text-[10px] text-amber-500">(edited)</span> : ""}</span>
                      )}
                    </td>
                    <td className="px-3 py-2">
                      {isEditable && editingReq ? <StatusBadge label={editingReq.priority} variant={(editingReq.priority as string) === "High" ? "error" : (editingReq.priority as string) === "Medium" ? "warning" : "success"} /> : <StatusBadge label={req.priority} variant={req.priority === "High" ? "error" : req.priority === "Medium" ? "warning" : "success"} />}
                    </td>
                    {state.editMode && <td className="px-3 py-2">{isEditable ? <span className="text-[10px] text-surface-400">Editable</span> : <span className="text-[10px] text-surface-300">Read-only</span>}</td>}
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        {allRendered.length === 0 && <p className="py-4 text-center text-sm text-surface-400">No requirements match your filters.</p>}
      </ContentPanel>

      {/* User Stories Toggle */}
      <ContentPanel>
        <button onClick={() => setShowStories(!showStories)} className="flex w-full items-center justify-between text-left" aria-expanded={showStories}>
          <SectionHeading title="User Stories and Acceptance Criteria" description="26 user stories organized by stakeholder role" />
          <span className="text-sm text-brand-600">{showStories ? "Hide" : "Show"}</span>
        </button>
        {showStories && (
          <div className="mt-4 space-y-2 border-t border-surface-100 pt-4">
            <p className="text-xs text-surface-400">User stories and acceptance criteria are documented in docs/13-user-stories.md and docs/14-acceptance-criteria.md. Full interactive display is available in the BRD view.</p>
          </div>
        )}
      </ContentPanel>

      <div className="mt-4 rounded-lg border border-yellow-200 bg-yellow-50 p-2 text-xs text-yellow-800">
        <strong>Local Storage Notice:</strong> Requirement edits are stored in your browser using localStorage. No data is sent to any server. Reset clears only BA Compass data.
      </div>

      <div className="mt-6 flex justify-between">
        <a href="/future-state" className="text-sm font-medium text-brand-600 hover:text-brand-700">← Future State</a>
        <a href="/brd" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: BRD →</a>
      </div>
    </div>
  );
}
