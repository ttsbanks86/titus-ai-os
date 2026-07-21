import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";

const contributions = [
  "Defined the business problem and created the project charter",
  "Identified and analyzed 10 stakeholder roles with power-interest mapping",
  "Documented 11-step current-state process with failure point analysis",
  "Performed gap analysis identifying 22 pain points across 9 dimensions",
  "Defined 15 business, 18 functional, and 12 nonfunctional requirements",
  "Created 26 user stories with acceptance criteria in Given/When/Then format",
  "Developed the requirements traceability matrix linking problem through KPI",
  "Defined 8 KPIs with formulas, targets, and warning thresholds",
  "Created the risk register with 15 risks, mitigations, and contingency plans",
  "Designed the future-state process with side-by-side comparison",
  "Built and tested the portfolio application with 47 automated tests",
  "Documented responsible AI principles and ethical considerations",
];

export default function ProjectPage() {
  return (
    <div className="content-container py-8">
      <PageHeading title="About the Project" subtitle="BA Compass — Portfolio Case Study" />

      <ContentPanel className="mb-6">
        <SectionHeading title="Why This Project Exists" />
        <p className="text-surface-600">
          BA Compass was created to demonstrate real, recruiter-visible Business Analyst skills
          through a complete case study. Rather than listing BA skills on a resume, this project
          shows them in action — from problem discovery through requirements documentation, KPI
          definition, process design, and risk management.
        </p>
      </ContentPanel>

      {/* My Contribution */}
      <ContentPanel className="mb-6">
        <SectionHeading title="My Contribution" description="Business Analyst work completed in this project" />
        <div className="grid gap-2 text-sm sm:grid-cols-2">
          {contributions.map((item, i) => (
            <div key={i} className="flex items-start gap-2">
              <span className="mt-0.5 h-2 w-2 shrink-0 rounded-full bg-brand-500" aria-hidden="true" />
              <span className="text-surface-700">{item}</span>
            </div>
          ))}
        </div>
      </ContentPanel>

      {/* Approach */}
      <ContentPanel className="mb-6">
        <SectionHeading title="The Business Analyst Approach" />
        <p className="text-surface-600">
          This project follows a structured BA methodology: <strong>Discover → Analyze → Define →
          Design → Validate → Recommend</strong>. Every requirement is traceable to a business problem.
          Every KPI has a defined formula. Every risk has a mitigation strategy. The documentation
          is designed to be reviewed by recruiters and hiring managers who want to see how a BA
          thinks, communicates, and delivers value.
        </p>
      </ContentPanel>

      {/* Tools */}
      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        <ContentPanel>
          <SectionHeading title="Tools and Technologies" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>Next.js 15 (App Router) with TypeScript</li>
            <li>Tailwind CSS for responsive styling</li>
            <li>Recharts for KPI data visualization</li>
            <li>Lucide React for icons</li>
            <li>Vitest + Testing Library (47 tests)</li>
            <li>Playwright for end-to-end testing</li>
            <li>GitHub Actions for CI</li>
            <li>Git for version control</li>
          </ul>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="Documents Produced" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>25 Business Analyst documentation deliverables</li>
            <li>Full Business Requirements Document (BRD)</li>
            <li>Requirements Traceability Matrix</li>
            <li>KPI Dictionary with 8 defined metrics</li>
            <li>Data Dictionary covering 10 entities</li>
            <li>Risk Register with 15 entries</li>
            <li>Product Backlog with 52 items</li>
          </ul>
        </ContentPanel>
      </div>

      {/* Testing and Privacy */}
      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        <ContentPanel>
          <SectionHeading title="Testing Approach" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>34 KPI calculation unit tests</li>
            <li>7 UI component tests</li>
            <li>6 Playwright e2e smoke tests</li>
            <li>TypeScript strict mode compilation</li>
            <li>ESLint code quality checks</li>
            <li>Production build verification</li>
          </ul>
        </ContentPanel>
        <ContentPanel>
          <SectionHeading title="Privacy Approach" />
          <ul className="list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>All data is synthetic and fictional</li>
            <li>No real client, caregiver, or patient information</li>
            <li>No API keys or secrets in the codebase</li>
            <li>No cookies, tracking, or analytics</li>
            <li>No backend server or database</li>
            <li>No user accounts or authentication</li>
          </ul>
        </ContentPanel>
      </div>

      {/* Current Status */}
      <ContentPanel>
        <SectionHeading title="Project Status" />
        <div className="space-y-2 text-sm">
          <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-green-500" /><span className="text-surface-700"><strong>Phase 1:</strong> Documentation Foundation — Complete (25 documents)</span></div>
          <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-green-500" /><span className="text-surface-700"><strong>Phase 2:</strong> Application Foundation — Complete (Next.js app, types, data, KPI engine)</span></div>
          <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-green-500" /><span className="text-surface-700"><strong>Phase 3:</strong> Recruiter-Facing MVP — Complete (full content pages, charts, navigation)</span></div>
          <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-surface-300" /><span className="text-surface-400"><strong>Phase 4:</strong> Interactive Features — Planned</span></div>
          <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-surface-300" /><span className="text-surface-400"><strong>Phase 5:</strong> Testing and Quality — Planned</span></div>
          <div className="flex items-center gap-2"><span className="h-2 w-2 rounded-full bg-surface-300" /><span className="text-surface-400"><strong>Phase 6:</strong> Deployment and Career Package — Planned</span></div>
        </div>
      </ContentPanel>

      <div className="mt-6 flex justify-between">
        <a href="/recommendations" className="text-sm font-medium text-brand-600 hover:text-brand-700">← Recommendations</a>
        <a href="/responsible-ai" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: Responsible AI →</a>
      </div>
    </div>
  );
}
