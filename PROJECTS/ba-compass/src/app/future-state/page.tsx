import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { futureStateImprovements } from "@/data/content/process-data";

export default function FutureStatePage() {
  return (
    <div className="content-container py-8">
      <PageHeading title="Future-State Process" subtitle="Proposed improvements addressing identified operational gaps" />

      <ContentPanel className="mb-6">
        <SectionHeading title="Vision" description="What the improved operational model looks like" />
        <p className="text-surface-600">
          The future-state process introduces centralized visibility, proactive alerts, structured escalation,
          automated KPI tracking, and clear ownership assignment for every operational function. These changes
          address the six critical breakdowns identified in the current-state analysis.
        </p>
      </ContentPanel>

      {/* Side-by-side comparison */}
      <SectionHeading title="Current vs. Future State" description="Side-by-side comparison of key operational areas" />
      <div className="mb-6 overflow-x-auto">
        <table className="min-w-full divide-y divide-surface-200 text-sm">
          <thead className="bg-surface-50">
            <tr>
              <th className="px-4 py-3 text-left font-medium text-surface-600">Area</th>
              <th className="px-4 py-3 text-left font-medium text-red-600">Current State</th>
              <th className="px-4 py-3 text-left font-medium text-green-600">Future State</th>
              <th className="px-4 py-3 text-left font-medium text-surface-600">Expected Outcome</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-surface-100">
            {futureStateImprovements.map((imp) => (
              <tr key={imp.area} className="hover:bg-surface-50">
                <td className="px-4 py-3 font-medium text-surface-700">{imp.area}</td>
                <td className="px-4 py-3 text-red-600">{imp.currentState}</td>
                <td className="px-4 py-3 text-green-600">{imp.futureState}</td>
                <td className="px-4 py-3 text-xs text-surface-500">{imp.expectedOutcome}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Detailed Improvement Cards */}
      <SectionHeading title="Improvement Details" description="Each improvement linked to requirements and KPIs" />
      <div className="mb-6 grid gap-4 sm:grid-cols-2">
        {futureStateImprovements.map((imp) => (
          <ContentPanel key={imp.area}>
            <h3 className="font-semibold text-surface-800">{imp.area}</h3>
            <div className="mt-2 grid grid-cols-2 gap-2 text-xs">
              <div><span className="font-medium text-red-600">Current:</span><p className="text-surface-500">{imp.currentState}</p></div>
              <div><span className="font-medium text-green-600">Future:</span><p className="text-surface-500">{imp.futureState}</p></div>
            </div>
            <div className="mt-2 flex flex-wrap gap-2 text-xs">
              <span className="rounded bg-blue-50 px-2 py-0.5 text-blue-700">BR: {imp.brLink}</span>
              <span className="rounded bg-green-50 px-2 py-0.5 text-green-700">KPI: {imp.kpiLink}</span>
            </div>
            <p className="mt-2 text-xs text-surface-500"><strong>Expected outcome:</strong> {imp.expectedOutcome}</p>
          </ContentPanel>
        ))}
      </div>

      {/* Key Improvements Summary */}
      <div className="mb-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <h3 className="font-semibold text-green-800">Centralized Visibility</h3>
          <p className="mt-1 text-sm text-green-700">Single dashboard for shift status, gaps, escalations, and documentation. No more spreadsheets and phone tag.</p>
        </div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <h3 className="font-semibold text-green-800">Proactive Alerts</h3>
          <p className="mt-1 text-sm text-green-700">Early notification of unconfirmed shifts, pending gaps, and approaching documentation deadlines.</p>
        </div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <h3 className="font-semibold text-green-800">Structured Escalation</h3>
          <p className="mt-1 text-sm text-green-700">Defined severity levels, escalation paths, and ownership. Every issue has an audit trail.</p>
        </div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <h3 className="font-semibold text-green-800">KPI Dashboard</h3>
          <p className="mt-1 text-sm text-green-700">Real-time metrics with trend views. Management can identify problems before they escalate.</p>
        </div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <h3 className="font-semibold text-green-800">Clear Ownership</h3>
          <p className="mt-1 text-sm text-green-700">Every issue and follow-up has an assigned owner with a deadline. No more dropped balls.</p>
        </div>
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <h3 className="font-semibold text-green-800">Audit Trail</h3>
          <p className="mt-1 text-sm text-green-700">Every operational action logged with timestamp and user attribution. Compliance-ready.</p>
        </div>
      </div>

      <ContentPanel>
        <p className="text-sm text-surface-400">
          These improvements are projected outcomes based on the case-study analysis. They represent expected
          improvements, not real operational results. Actual outcomes would depend on implementation quality,
          stakeholder adoption, and ongoing refinement.
        </p>
      </ContentPanel>

      <div className="mt-6 flex justify-between">
        <a href="/dashboard" className="text-sm font-medium text-brand-600 hover:text-brand-700">← KPI Dashboard</a>
        <a href="/requirements" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: Requirements →</a>
      </div>
    </div>
  );
}
