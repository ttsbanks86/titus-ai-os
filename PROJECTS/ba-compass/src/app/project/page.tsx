import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

export default function ProjectPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="About the Project"
        subtitle="BA Compass — Portfolio Case Study"
      />
      <ContentPanel>
        <h3 className="font-semibold text-surface-700">Project Overview</h3>
        <p className="mt-2 text-surface-600">
          BA Compass is a recruiter-ready Business Analyst portfolio project demonstrating
          end-to-end business analysis through a fictional home-care services case study.
        </p>

        <h3 className="mt-6 font-semibold text-surface-700">Technology Stack</h3>
        <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-surface-600">
          <li>Next.js 15 App Router with TypeScript</li>
          <li>Tailwind CSS for styling</li>
          <li>Recharts for data visualization (Phase 3)</li>
          <li>Vitest + Playwright for testing</li>
          <li>Vercel for deployment (Phase 6)</li>
          <li>No backend server required</li>
          <li>No AI API dependency</li>
        </ul>

        <h3 className="mt-6 font-semibold text-surface-700">Synthetic Data Notice</h3>
        <p className="mt-2 text-surface-600">
          All data, companies, scenarios, and stakeholders in this project are fictional.
          No real client, caregiver, employer, or patient information is used. This is a
          portfolio demonstration project.
        </p>

        <h3 className="mt-6 font-semibold text-surface-700">Phase Status</h3>
        <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-surface-600">
          <li><strong>Phase 1:</strong> Documentation Foundation — Complete</li>
          <li><strong>Phase 2:</strong> Application Foundation — Complete</li>
          <li><strong>Phase 3:</strong> Recruiter-Facing MVP — Planned</li>
          <li><strong>Phase 4:</strong> Interactive Features — Planned</li>
          <li><strong>Phase 5:</strong> Testing and Quality — Planned</li>
          <li><strong>Phase 6:</strong> Deployment and Career Package — Planned</li>
        </ul>
      </ContentPanel>
    </div>
  );
}
