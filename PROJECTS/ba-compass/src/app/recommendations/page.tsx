import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

export default function RecommendationsPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Recommendations"
        subtitle="Prioritized improvement recommendations"
      />
      <ContentPanel>
        <div className="space-y-4">
          <div className="rounded-lg border border-red-200 bg-red-50 p-4">
            <h3 className="font-semibold text-red-800">Critical Priority</h3>
            <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-red-700">
              <li>Implement centralized shift visibility dashboard</li>
              <li>Establish pre-shift confirmation workflow</li>
              <li>Define and enforce escalation paths with severity levels</li>
            </ul>
          </div>
          <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4">
            <h3 className="font-semibold text-yellow-800">High Priority</h3>
            <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-yellow-700">
              <li>Track caregiver arrival times systematically</li>
              <li>Monitor documentation completion with automated reminders</li>
              <li>Create structured follow-up process with ownership assignment</li>
              <li>Build KPI dashboard with 8 defined metrics</li>
            </ul>
          </div>
          <div className="rounded-lg border border-green-200 bg-green-50 p-4">
            <h3 className="font-semibold text-green-800">Medium Priority</h3>
            <ul className="mt-2 list-inside list-disc space-y-1 text-sm text-green-700">
              <li>Document operational policies and procedures</li>
              <li>Establish audit trail for operational actions</li>
              <li>Implement exportable reporting</li>
            </ul>
          </div>
        </div>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include detailed improvement plans with effort estimates,
          impact analysis, and phased implementation roadmap.
        </p>
      </ContentPanel>
    </div>
  );
}
