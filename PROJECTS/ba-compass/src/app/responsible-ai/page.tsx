import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

export default function ResponsibleAiPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Responsible AI"
        subtitle="Ethical AI considerations for the BA Compass project"
      />
      <ContentPanel>
        <h3 className="font-semibold text-surface-700">Current Status: No AI Dependency</h3>
        <p className="mt-2 text-surface-600">
          The BA Compass MVP does not use any AI services. All data is statically defined,
          all KPI calculations are deterministic, and the application works without any
          API configuration. This is by design — recruiters must be able to evaluate the
          portfolio without managing API keys or incurring costs.
        </p>

        <h3 className="mt-6 font-semibold text-surface-700">Future AI Integration Principles</h3>
        <p className="mt-2 text-surface-600">
          If AI features are added in future phases, they will follow these principles:
        </p>
        <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-surface-600">
          <li>AI will be optional — never required for core functionality</li>
          <li>All AI-generated content will be clearly labeled</li>
          <li>No real client, caregiver, or patient data will be sent to AI services</li>
          <li>A provider-independent architecture will be used</li>
          <li>Users will be informed before any AI API call is made</li>
        </ul>

        <h3 className="mt-6 font-semibold text-surface-700">Data Ethics</h3>
        <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-surface-600">
          <li>All project data is synthetic and clearly labeled</li>
          <li>No real personal information is stored or processed</li>
          <li>No user tracking, analytics, or data collection occurs</li>
          <li>No cookies or session storage are used</li>
          <li>The application is privacy-preserving by design</li>
        </ul>

        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include more detailed AI ethics documentation and
          transparency notes.
        </p>
      </ContentPanel>
    </div>
  );
}
