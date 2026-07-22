// BA Compass — Export Utilities

const SYNTHETIC_NOTICE = "DISCLAIMER: All data is synthetic and fictional. This is a portfolio demonstration project. No real client, caregiver, or patient information is used.";

function today(): string {
  return new Date().toISOString().split("T")[0];
}

// ─── Markdown Export ───────────────────────────────────────

export function requirementsToMarkdown(
  items: { id: string; type: string; statement: string; priority: string; status: string; stakeholderOwner: string; justification: string; relatedKpi: string; edited?: boolean }[]
): string {
  const header = `# BA Compass — Requirements Report\n**Company:** BrightCare Home Services (Fictional)\n**Generated:** ${today()}\n${SYNTHETIC_NOTICE}\n\n`;
  const tableHeader = "| ID | Type | Statement | Priority | Status | Stakeholder | Justification | KPI |\n|----|------|-----------|----------|--------|-------------|---------------|-----|\n";
  const rows = items.map((r) => {
    const edited = r.edited ? " *(local edit)*" : "";
    return `| ${r.id} | ${r.type} | ${r.statement.replace(/\|/g, "\\|")} | ${r.priority} | ${r.status} | ${r.stakeholderOwner} | ${r.justification.replace(/\|/g, "\\|")} | ${r.relatedKpi}${edited} |`;
  }).join("\n");
  return header + tableHeader + rows;
}

export function traceabilityToMarkdown(
  items: { id: string; businessProblem: string; br: string; fr: string; userStory: string; acceptanceCriteria: string; kpi: string; status: string }[]
): string {
  const header = `# BA Compass — Traceability Matrix\n**Company:** BrightCare Home Services (Fictional)\n**Generated:** ${today()}\n${SYNTHETIC_NOTICE}\n\n`;
  const tableHeader = "| ID | Business Problem | BR | FR | User Story | AC | KPI | Status |\n|----|-----------------|-----|-----|-----------|-----|-----|--------|\n";
  const rows = items.map((r) => `| ${r.id} | ${r.businessProblem} | ${r.br} | ${r.fr} | ${r.userStory} | ${r.acceptanceCriteria} | ${r.kpi} | ${r.status} |`).join("\n");
  return header + tableHeader + rows;
}

export function risksToMarkdown(
  items: { id: string; description: string; category: string; likelihood: number; impact: number; score: number; owner: string; mitigation: string; status: string }[]
): string {
  const header = `# BA Compass — Risk Register\n**Company:** BrightCare Home Services (Fictional)\n**Generated:** ${today()}\n${SYNTHETIC_NOTICE}\n\n`;
  const tableHeader = "| ID | Description | Category | L | I | Score | Owner | Mitigation | Status |\n|----|-------------|----------|---|---|-------|-------|------------|--------|\n";
  const rows = items.map((r) => `| ${r.id} | ${r.description} | ${r.category} | ${r.likelihood} | ${r.impact} | ${r.score} | ${r.owner} | ${r.mitigation} | ${r.status} |`).join("\n");
  return header + tableHeader + rows;
}

export function executiveSummaryToMarkdown(summary: string): string {
  return `# BA Compass — Executive Summary\n**Company:** BrightCare Home Services (Fictional)\n**Generated:** ${today()}\n${SYNTHETIC_NOTICE}\n\n${summary}`;
}

// ─── CSV Export ───────────────────────────────────────────

function escapeCsv(val: string): string {
  if (val.includes(",") || val.includes('"') || val.includes("\n")) {
    return `"${val.replace(/"/g, '""')}"`;
  }
  return val;
}

export function requirementsToCsv(
  items: { id: string; type: string; statement: string; priority: string; status: string; stakeholderOwner: string; justification: string; relatedKpi: string; edited?: boolean }[]
): string {
  const header = "ID,Type,Statement,Priority,Status,Stakeholder,Justification,KPI,LocalEdit\n";
  const rows = items.map((r) => {
    const fields = [r.id, r.type, r.statement, r.priority, r.status, r.stakeholderOwner, r.justification, r.relatedKpi, r.edited ? "Yes" : "No"];
    return fields.map(escapeCsv).join(",");
  }).join("\n");
  return header + rows + `\n\n${SYNTHETIC_NOTICE}`;
}

export function risksToCsv(
  items: { id: string; description: string; category: string; likelihood: number; impact: number; score: number; owner: string; mitigation: string; status: string }[]
): string {
  const header = "ID,Description,Category,Likelihood,Impact,Score,Owner,Mitigation,Status\n";
  const rows = items.map((r) => {
    const fields = [r.id, r.description, r.category, String(r.likelihood), String(r.impact), String(r.score), r.owner, r.mitigation, r.status];
    return fields.map(escapeCsv).join(",");
  }).join("\n");
  return header + rows + `\n\n${SYNTHETIC_NOTICE}`;
}

// ─── Download Helpers ──────────────────────────────────────

export function downloadText(content: string, filename: string, mimeType = "text/markdown") {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export function downloadCsv(content: string, filename: string) {
  downloadText(content, filename, "text/csv");
}
