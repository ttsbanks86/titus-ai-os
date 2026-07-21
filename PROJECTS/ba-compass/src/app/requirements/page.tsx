import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

export default function RequirementsPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Requirements Management"
        subtitle="Business, functional, and nonfunctional requirements"
      />
      <ContentPanel>
        <div className="grid gap-4 sm:grid-cols-3">
          <div className="rounded-lg border border-blue-200 bg-blue-50 p-4">
            <h3 className="font-semibold text-blue-800">Business Requirements</h3>
            <p className="mt-1 text-2xl font-bold text-blue-600">15</p>
            <p className="mt-1 text-xs text-blue-500">BR-001 through BR-015</p>
          </div>
          <div className="rounded-lg border border-green-200 bg-green-50 p-4">
            <h3 className="font-semibold text-green-800">Functional Requirements</h3>
            <p className="mt-1 text-2xl font-bold text-green-600">18</p>
            <p className="mt-1 text-xs text-green-500">FR-001 through FR-018</p>
          </div>
          <div className="rounded-lg border border-purple-200 bg-purple-50 p-4">
            <h3 className="font-semibold text-purple-800">Nonfunctional Requirements</h3>
            <p className="mt-1 text-2xl font-bold text-purple-600">12</p>
            <p className="mt-1 text-xs text-purple-500">NFR-001 through NFR-012</p>
          </div>
        </div>
        <div className="mt-6">
          <h3 className="font-semibold text-surface-700">Additional BA Artifacts</h3>
          <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-surface-600">
            <li>26 user stories (US-001 through US-026)</li>
            <li>24 acceptance criteria (AC-001 through AC-024)</li>
            <li>15-line requirements traceability matrix</li>
            <li>Full Business Requirements Document (BRD)</li>
          </ul>
        </div>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include sortable/filterable requirement tables,
          user story cards, Given/When/Then criteria display, and the complete RTM.
        </p>
      </ContentPanel>
    </div>
  );
}
