import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

const stakeholders = [
  { id: "STK-001", role: "Agency Owner", interest: "Strategic", influence: "High" as const },
  { id: "STK-002", role: "Operations Manager", interest: "Operational", influence: "High" as const },
  { id: "STK-003", role: "Scheduling Coordinator", interest: "Tactical", influence: "Medium" as const },
  { id: "STK-004", role: "Care Coordinator", interest: "Tactical", influence: "Medium" as const },
  { id: "STK-005", role: "Caregiver", interest: "Frontline", influence: "Low" as const },
  { id: "STK-006", role: "Quality Assurance Lead", interest: "Compliance", influence: "Medium" as const },
  { id: "STK-007", role: "Client Services Rep", interest: "Client-facing", influence: "Low" as const },
  { id: "STK-008", role: "IT Administrator", interest: "Technical", influence: "Medium" as const },
  { id: "STK-009", role: "Compliance Representative", interest: "Regulatory", influence: "High" as const },
  { id: "STK-010", role: "Client / Family Rep", interest: "Service Quality", influence: "Low" as const },
];

export default function StakeholdersPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Stakeholder Analysis"
        subtitle="10 fictional stakeholder roles identified and analyzed"
      />
      <ContentPanel>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">ID</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Role</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Interest</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Influence</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {stakeholders.map((s) => (
                <tr key={s.id} className="hover:bg-surface-50">
                  <td className="px-3 py-2 font-mono text-xs text-surface-400">{s.id}</td>
                  <td className="px-3 py-2 font-medium text-surface-700">{s.role}</td>
                  <td className="px-3 py-2 text-surface-600">{s.interest}</td>
                  <td className="px-3 py-2">
                    <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                      s.influence === "High"
                        ? "bg-red-50 text-red-700"
                        : s.influence === "Medium"
                        ? "bg-yellow-50 text-yellow-700"
                        : "bg-green-50 text-green-700"
                    }`}>
                      {s.influence}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include power-interest matrix, engagement approach,
          communication plans, detailed pain points, and conflict resolution strategies.
        </p>
      </ContentPanel>
    </div>
  );
}
