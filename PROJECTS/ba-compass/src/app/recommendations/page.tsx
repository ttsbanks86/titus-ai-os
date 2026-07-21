import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";

const immediateActions = [
  { problem: "Missed shifts and no shift confirmation", recommendation: "Implement pre-shift confirmation workflow with automated reminders for unconfirmed shifts", value: "Reduce missed shifts by ensuring coverage is verified before start time", br: "BR-001, BR-002", kpi: "KPI-001, KPI-006", risk: "Scope growth (R-001)", priority: "Critical" },
  { problem: "No centralized operational visibility", recommendation: "Deploy centralized shift status dashboard consolidating all operational data", value: "Single source of truth eliminates phone tag and manual reconciliation", br: "BR-006", kpi: "KPI-001 through KPI-008", risk: "Poor recruiter usability (R-006)", priority: "Critical" },
  { problem: "Informal escalation with no audit trail", recommendation: "Define and enforce escalation paths with severity levels, ownership, and response SLAs", value: "Faster issue resolution with clear accountability and audit trail", br: "BR-003", kpi: "KPI-004", risk: "Scope growth (R-001)", priority: "Critical" },
];

const nearTermActions = [
  { problem: "Late caregiver arrivals untracked", recommendation: "Implement arrival time tracking with configurable lateness thresholds and escalation triggers", value: "Identify chronic lateness patterns and address before client impacts", br: "BR-011", kpi: "KPI-003", risk: "KPI calculation errors (R-002)", priority: "High" },
  { problem: "Incomplete service documentation", recommendation: "Deploy documentation status dashboard with automated reminders and escalation for overdue items", value: "Reduced compliance risk and billing delays", br: "BR-005", kpi: "KPI-005", risk: "Scope growth (R-001)", priority: "High" },
  { problem: "No structured issue follow-up", recommendation: "Create follow-up tracking system with assigned ownership, deadlines, and completion verification", value: "Prevent recurring issues and improve client satisfaction", br: "BR-004", kpi: "KPI-008", risk: "Overengineering (R-013)", priority: "High" },
  { problem: "No KPI dashboard for management", recommendation: "Build automated KPI dashboard with trend views, target comparisons, and configurable time periods", value: "Data-driven decision-making replaces anecdotal reporting", br: "BR-008", kpi: "KPI-001 through KPI-008", risk: "KPI calculation errors (R-002)", priority: "High" },
  { problem: "No client notification tracking", recommendation: "Implement structured client notification process with delivery confirmation", value: "Improved client trust and reduced status inquiries", br: "BR-007", kpi: "KPI-001 (indirect)", risk: "Scope growth (R-001)", priority: "High" },
];

const futureEnhancements = [
  { problem: "No documented operational policies", recommendation: "Develop and publish operational policies for gap-filling, escalation, and documentation deadlines", value: "Consistent decision-making across the organization", br: "BR-009", kpi: "KPI-005 (indirect)", risk: "Scope growth (R-001)", priority: "Medium" },
  { problem: "No audit trail for compliance", recommendation: "Implement system-generated audit logging for all operational actions", value: "Compliance readiness and event reconstruction", br: "BR-010", kpi: "KPI-005 (indirect)", risk: "Overengineering (R-013)", priority: "Medium" },
  { problem: "No reporting export capability", recommendation: "Add PDF and Markdown export for dashboard, requirements, and risk register", value: "Stakeholder communication and record-keeping", br: "BR-012", kpi: "Indirect", risk: "Broken exports (R-007)", priority: "Medium" },
];

export default function RecommendationsPage() {
  return (
    <div className="content-container py-8">
      <PageHeading title="Recommendations" subtitle="Prioritized improvements with business impact and KPI alignment" />

      {/* Executive Summary */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Executive Summary" />
        <p className="text-surface-600">
          Based on the analysis of BrightCare Home Services (a fictional case study), the organization&apos;s
          operational failures stem from fragmented communication, reactive issue detection, and the
          absence of centralized visibility. The recommended improvements focus on establishing core
          operational infrastructure before adding advanced capabilities.
        </p>
        <div className="mt-4 grid gap-3 text-sm sm:grid-cols-3">
          <div className="rounded-lg border border-red-200 bg-red-50 p-3"><strong className="text-red-800">Immediate (3)</strong><p className="text-red-600">Critical operational gaps</p></div>
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-3"><strong className="text-yellow-800">Near-Term (5)</strong><p className="text-yellow-600">High-priority improvements</p></div>
          <div className="rounded-lg border border-blue-200 bg-blue-50 p-3"><strong className="text-blue-800">Future (3)</strong><p className="text-blue-600">Enhancements for later phases</p></div>
        </div>
      </ContentPanel>

      {/* Immediate Actions */}
      <SectionHeading title="Immediate Actions" description="Critical gaps requiring immediate attention" />
      <div className="mb-6 space-y-3">
        {immediateActions.map((action, i) => (
          <ContentPanel key={i}>
            <div className="flex items-start gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-red-100 text-xs font-bold text-red-700">{(i + 1)}</span>
              <div className="flex-1">
                <p className="text-xs font-medium text-red-600">Problem: {action.problem}</p>
                <p className="mt-1 font-medium text-surface-800">{action.recommendation}</p>
                <p className="mt-1 text-sm text-green-700"><strong>Business value:</strong> {action.value}</p>
                <div className="mt-2 flex flex-wrap gap-2 text-xs">
                  <span className="rounded bg-blue-50 px-2 py-0.5 text-blue-700">{action.br}</span>
                  <span className="rounded bg-green-50 px-2 py-0.5 text-green-700">{action.kpi}</span>
                  <span className="rounded bg-amber-50 px-2 py-0.5 text-amber-700">Risk: {action.risk}</span>
                </div>
              </div>
            </div>
          </ContentPanel>
        ))}
      </div>

      {/* Near-Term Actions */}
      <SectionHeading title="Near-Term Actions" description="High-priority improvements for the next implementation phase" />
      <div className="mb-6 space-y-3">
        {nearTermActions.map((action, i) => (
          <ContentPanel key={i}>
            <div className="flex items-start gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-yellow-100 text-xs font-bold text-yellow-700">{(i + 1)}</span>
              <div className="flex-1">
                <p className="text-xs font-medium text-yellow-600">Problem: {action.problem}</p>
                <p className="mt-1 font-medium text-surface-800">{action.recommendation}</p>
                <p className="mt-1 text-sm text-green-700"><strong>Business value:</strong> {action.value}</p>
                <div className="mt-2 flex flex-wrap gap-2 text-xs">
                  <span className="rounded bg-blue-50 px-2 py-0.5 text-blue-700">{action.br}</span>
                  <span className="rounded bg-green-50 px-2 py-0.5 text-green-700">{action.kpi}</span>
                  <span className="rounded bg-amber-50 px-2 py-0.5 text-amber-700">Risk: {action.risk}</span>
                </div>
              </div>
            </div>
          </ContentPanel>
        ))}
      </div>

      {/* Future Enhancements */}
      <SectionHeading title="Future Enhancements" description="Recommended for later phases after core infrastructure is stable" />
      <div className="mb-6 space-y-3">
        {futureEnhancements.map((action, i) => (
          <ContentPanel key={i}>
            <div className="flex items-start gap-3">
              <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-100 text-xs font-bold text-blue-700">{(i + 1)}</span>
              <div className="flex-1">
                <p className="text-xs font-medium text-blue-600">Problem: {action.problem}</p>
                <p className="mt-1 font-medium text-surface-800">{action.recommendation}</p>
                <p className="mt-1 text-sm text-green-700"><strong>Business value:</strong> {action.value}</p>
                <div className="mt-2 flex flex-wrap gap-2 text-xs">
                  <span className="rounded bg-blue-50 px-2 py-0.5 text-blue-700">{action.br}</span>
                  <span className="rounded bg-green-50 px-2 py-0.5 text-green-700">{action.kpi}</span>
                  <span className="rounded bg-amber-50 px-2 py-0.5 text-amber-700">Risk: {action.risk}</span>
                </div>
              </div>
            </div>
          </ContentPanel>
        ))}
      </div>

      <ContentPanel>
        <p className="text-sm text-surface-400">
          These recommendations are projected improvements based on the fictional case-study analysis.
          They represent expected outcomes, not real operational results. Actual outcomes would depend
          on implementation quality, stakeholder adoption, and organizational context.
        </p>
      </ContentPanel>

      <div className="mt-6 flex justify-between">
        <a href="/risks" className="text-sm font-medium text-brand-600 hover:text-brand-700">← Risk Register</a>
        <a href="/project" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: About the Project →</a>
      </div>
    </div>
  );
}
