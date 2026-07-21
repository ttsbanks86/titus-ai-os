import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

const areas = [
  { area: "People", problems: 3, topIssue: "Scheduling coordinator overload" },
  { area: "Process", problems: 3, topIssue: "No shift confirmation process" },
  { area: "Technology", problems: 3, topIssue: "No centralized system" },
  { area: "Data", problems: 2, topIssue: "No attendance data collection" },
  { area: "Communication", problems: 2, topIssue: "Fragmented issue communication" },
  { area: "Governance", problems: 2, topIssue: "No defined operational policies" },
  { area: "Reporting", problems: 2, topIssue: "No operational dashboard" },
  { area: "Risk", problems: 2, topIssue: "Compliance exposure" },
  { area: "Client Experience", problems: 2, topIssue: "Inconsistent care delivery" },
];

export default function AnalysisPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Gap Analysis"
        subtitle="Pain-point analysis across 9 business dimensions"
      />
      <ContentPanel>
        <p className="mb-4 text-surface-600">
          Twenty-two distinct pain points were identified across people, process, technology,
          data, communication, governance, reporting, risk, and client experience dimensions.
          Each pain point includes root cause analysis, severity rating, and proposed improvement.
        </p>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Dimension</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Pain Points</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Top Issue</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {areas.map((a) => (
                <tr key={a.area} className="hover:bg-surface-50">
                  <td className="px-3 py-2 font-medium text-surface-700">{a.area}</td>
                  <td className="px-3 py-2 text-surface-600">{a.problems}</td>
                  <td className="px-3 py-2 text-surface-500">{a.topIssue}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include detailed root cause analysis for each pain point,
          severity scores, current workarounds, and linked requirements.
        </p>
      </ContentPanel>
    </div>
  );
}
