import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

const steps = [
  { step: 1, name: "Shift Creation", actor: "Scheduling Coordinator", failurePoint: "No validation" },
  { step: 2, name: "Caregiver Assignment", actor: "Scheduling Coordinator", failurePoint: "No confirmation system" },
  { step: 3, name: "Shift Confirmation", actor: "Caregiver", failurePoint: "Assumed confirmation" },
  { step: 4, name: "Late Arrival Detection", actor: "Care Coordinator", failurePoint: "No automated detection" },
  { step: 5, name: "Missed Shift Discovery", actor: "Client / Coordinator", failurePoint: "Reactive discovery" },
  { step: 6, name: "Escalation", actor: "Care Coordinator", failurePoint: "No defined path" },
  { step: 7, name: "Replacement Search", actor: "Scheduling Coordinator", failurePoint: "No backup list" },
  { step: 8, name: "Client Communication", actor: "Client Services Rep", failurePoint: "No delivery confirmation" },
  { step: 9, name: "Service Documentation", actor: "Caregiver", failurePoint: "No deadline enforcement" },
  { step: 10, name: "Follow-Up", actor: "Care Coordinator", failurePoint: "Ad-hoc, if done" },
  { step: 11, name: "Management Reporting", actor: "Operations Manager", failurePoint: "Manual, error-prone" },
];

export default function CurrentStatePage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Current-State Process"
        subtitle="As-is workflow — BrightCare Home Services"
      />
      <ContentPanel>
        <p className="mb-4 text-surface-600">
          The current operational workflow spans 11 steps from shift creation to management
          reporting. Every step relies on manual processes, fragmented communication channels,
          and informal tracking methods.
        </p>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Step</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Process</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Actor</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Failure Point</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {steps.map((s) => (
                <tr key={s.step} className="hover:bg-surface-50">
                  <td className="px-3 py-2 text-surface-400">{s.step}</td>
                  <td className="px-3 py-2 font-medium text-surface-700">{s.name}</td>
                  <td className="px-3 py-2 text-surface-600">{s.actor}</td>
                  <td className="px-3 py-2 text-red-600">{s.failurePoint}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include a Mermaid process flow diagram, detailed
          step-level analysis with inputs, outputs, delays, and data gaps.
        </p>
      </ContentPanel>
    </div>
  );
}
