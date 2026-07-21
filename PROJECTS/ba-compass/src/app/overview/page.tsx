import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { DataNotice } from "@/components/ui/data-notice";

const analysisPhases = [
  { phase: "Discover", description: "Identify the business problem, current-state process, and stakeholder landscape" },
  { phase: "Analyze", description: "Perform gap analysis, root cause identification, and pain-point assessment" },
  { phase: "Define", description: "Document business, functional, and nonfunctional requirements with traceability" },
  { phase: "Design", description: "Create future-state process, KPI framework, and solution architecture" },
  { phase: "Validate", description: "Define acceptance criteria, risk register, and success measures" },
  { phase: "Recommend", description: "Prioritized recommendations with business impact and KPI alignment" },
];

export default function OverviewPage() {
  return (
    <div className="content-container py-8">
      <PageHeading title="Project Overview" subtitle="BrightCare Home Services — Business Analysis Case Study" />
      <DataNotice />

      {/* Background */}
      <ContentPanel className="mb-6 mt-6">
        <SectionHeading title="Business Challenge" description="A fictional home-care company with systemic operational failures" />
        <p className="text-surface-600">
          BrightCare Home Services is a fictional home-care provider serving approximately 8 active clients
          across four regions. The organization relies on spreadsheets, phone calls, and paper documentation
          to manage caregiver assignments, shift scheduling, and service documentation. As the organization
          has grown, these informal processes have become insufficient to maintain reliable operations.
        </p>
      </ContentPanel>

      {/* Objectives */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Project Objectives" />
        <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
          <li>Document the current-state business process for shift management</li>
          <li>Identify root causes of operational failures through structured analysis</li>
          <li>Define business, functional, and nonfunctional requirements for a solution</li>
          <li>Create traceable user stories with acceptance criteria</li>
          <li>Define KPIs and success measures for operational improvement</li>
          <li>Design a future-state process that addresses identified gaps</li>
          <li>Produce a professional BRD and supporting documentation suite</li>
        </ul>
      </ContentPanel>

      {/* Scope */}
      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        <ContentPanel>
          <SectionHeading title="In Scope" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>Shift-status visibility analysis</li>
            <li>Staffing-gap identification</li>
            <li>Missed-shift and late-arrival tracking</li>
            <li>Documentation-completion tracking</li>
            <li>Escalation and follow-up tracking</li>
            <li>KPI reporting and dashboard</li>
            <li>Current-state and future-state workflow</li>
            <li>Requirements management and traceability</li>
            <li>Risk tracking and mitigation</li>
          </ul>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="Out of Scope" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-500">
            <li>Payroll or billing systems</li>
            <li>Clinical decision-making or EHR</li>
            <li>Medication management</li>
            <li>Real employee scheduling</li>
            <li>Real client records or PII</li>
            <li>Automated hiring or onboarding</li>
            <li>Production deployment for a real agency</li>
            <li>Real-time GPS tracking</li>
          </ul>
        </ContentPanel>
      </div>

      {/* BA Lifecycle */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Business Analyst Lifecycle" description="The structured approach used in this case study" />
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {analysisPhases.map((p) => (
            <div key={p.phase} className="rounded-lg border border-brand-100 bg-brand-50 p-3">
              <div className="text-xs font-bold uppercase tracking-wider text-brand-600">{p.phase}</div>
              <p className="mt-1 text-sm text-surface-600">{p.description}</p>
            </div>
          ))}
        </div>
      </ContentPanel>

      {/* Deliverables */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Major Deliverables" />
        <div className="grid gap-3 text-sm sm:grid-cols-2 lg:grid-cols-3">
          <div><span className="font-medium">Project Charter</span> — Scope, objectives, success criteria</div>
          <div><span className="font-medium">Business Problem Statement</span> — Operational failure analysis</div>
          <div><span className="font-medium">Business Case</span> — Justification and expected benefits</div>
          <div><span className="font-medium">Stakeholder Analysis</span> — Register, power-interest matrix</div>
          <div><span className="font-medium">Process Maps</span> — Current and future-state workflows</div>
          <div><span className="font-medium">Gap Analysis</span> — Pain points across 9 dimensions</div>
          <div><span className="font-medium">BRD</span> — Complete business requirements document</div>
          <div><span className="font-medium">Requirements</span> — 45 BR, FR, NFR with traceability</div>
          <div><span className="font-medium">User Stories</span> — 26 stories with acceptance criteria</div>
          <div><span className="font-medium">RTM</span> — Full traceability matrix</div>
          <div><span className="font-medium">Risk Register</span> — 15 risks with mitigations</div>
          <div><span className="font-medium">KPI Dictionary</span> — 8 operational metrics</div>
        </div>
      </ContentPanel>

      {/* Key Links */}
      <div className="flex flex-wrap gap-3">
        <a href="/stakeholders" className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">View Stakeholders</a>
        <a href="/current-state" className="rounded-lg border border-surface-300 bg-white px-4 py-2 text-sm font-medium text-surface-700 hover:bg-surface-50">View Current State</a>
        <a href="/analysis" className="rounded-lg border border-surface-300 bg-white px-4 py-2 text-sm font-medium text-surface-700 hover:bg-surface-50">View Gap Analysis</a>
      </div>
    </div>
  );
}
