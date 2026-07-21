import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

const risks = [
  { id: "R-001", description: "Scope growth beyond portfolio needs", score: 12, category: "Scope" },
  { id: "R-002", description: "Incorrect KPI calculations in demo", score: 12, category: "Quality" },
  { id: "R-006", description: "Poor recruiter usability", score: 12, category: "Usability" },
  { id: "R-003", description: "Synthetic data appearing real", score: 8, category: "Privacy" },
  { id: "R-005", description: "AI hallucinations (future features)", score: 9, category: "Quality" },
  { id: "R-007", description: "Broken export functions", score: 9, category: "Technical" },
  { id: "R-008", description: "Mobile layout failure", score: 9, category: "Technical" },
  { id: "R-009", description: "Inaccessible process diagrams", score: 9, category: "Accessibility" },
  { id: "R-010", description: "Deployment failure", score: 8, category: "Technical" },
  { id: "R-011", description: "Exposed API keys", score: 8, category: "Security" },
  { id: "R-013", description: "Overengineering", score: 8, category: "Scope" },
  { id: "R-014", description: "Timeline slippage", score: 9, category: "Project Management" },
];

export default function RisksPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Risk Register"
        subtitle="15 identified risks with mitigation strategies"
      />
      <ContentPanel>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">ID</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Category</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Description</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              {risks.map((r) => (
                <tr key={r.id} className="hover:bg-surface-50">
                  <td className="px-3 py-2 font-mono text-xs text-surface-400">{r.id}</td>
                  <td className="px-3 py-2 text-surface-600">{r.category}</td>
                  <td className="px-3 py-2 text-surface-700">{r.description}</td>
                  <td className="px-3 py-2">
                    <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                      r.score >= 12 ? "bg-red-50 text-red-700" :
                      r.score >= 8 ? "bg-yellow-50 text-yellow-700" :
                      "bg-green-50 text-green-700"
                    }`}>
                      {r.score}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include complete risk details: likelihood, impact,
          mitigation, contingency, trigger, and owner for all 15 risks.
        </p>
      </ContentPanel>
    </div>
  );
}
