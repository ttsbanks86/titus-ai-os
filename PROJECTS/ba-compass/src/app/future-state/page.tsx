import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

const improvements = [
  { area: "Shift Status", current: "Manual spreadsheets", future: "Real-time dashboard" },
  { area: "Gap Detection", current: "Reactive discovery", future: "Proactive alerts" },
  { area: "Escalation", current: "Informal phone/email", future: "Structured with severity levels" },
  { area: "Documentation", current: "No tracking", future: "Status dashboard with reminders" },
  { area: "Issue Follow-Up", current: "Ad-hoc", future: "Assigned ownership with deadlines" },
  { area: "Reporting", current: "Manual compilation", future: "Automated KPI dashboard" },
  { area: "Audit Trail", current: "None", future: "System-generated logs" },
  { area: "Client Communication", current: "Phone calls only", future: "Structured notifications" },
];

export default function FutureStatePage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Future-State Process"
        subtitle="Proposed improvements addressing identified gaps"
      />
      <ContentPanel>
        <p className="mb-4 text-surface-600">
          The future-state process introduces centralized visibility, proactive alerts,
          structured escalation, automated KPI tracking, and clear ownership assignment
          for every operational function.
        </p>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Area</th>
                <th className="px-3 py-2 text-left font-medium text-red-600">Current State</th>
                <th className="px-3 py-2 text-left font-medium text-green-600">Future State</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {improvements.map((imp) => (
                <tr key={imp.area} className="hover:bg-surface-50">
                  <td className="px-3 py-2 font-medium text-surface-700">{imp.area}</td>
                  <td className="px-3 py-2 text-red-600">{imp.current}</td>
                  <td className="px-3 py-2 text-green-600">{imp.future}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include a future-state process flow diagram,
          side-by-side comparison, and implementation roadmap.
        </p>
      </ContentPanel>
    </div>
  );
}
