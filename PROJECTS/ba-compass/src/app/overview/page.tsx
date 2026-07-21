import { PageHeading } from "@/components/ui/page-heading";
import { ContentPanel } from "@/components/ui/content-panel";

export default function OverviewPage() {
  return (
    <div className="content-container py-8">
      <PageHeading
        title="Business Scenario Overview"
        subtitle="BrightCare Home Services — Fictional Case Study"
      />
      <ContentPanel>
        <h3 className="font-semibold text-surface-700">Company Background</h3>
        <p className="mt-2 text-surface-600">
          BrightCare Home Services is a fictional home-care provider serving approximately
          8 active clients across four regions. The organization manages caregiver-client
          assignments through informal, decentralized processes — relying on spreadsheets,
          phone calls, text messages, and paper documentation.
        </p>
        <h3 className="mt-6 font-semibold text-surface-700">Key Operational Problems</h3>
        <ul className="mt-2 list-inside list-disc space-y-1 text-surface-600">
          <li>Missed shifts and open staffing gaps reduce service reliability</li>
          <li>Late caregiver arrivals cause client dissatisfaction</li>
          <li>Delayed escalation leaves issues unresolved</li>
          <li>Incomplete service documentation creates compliance risk</li>
          <li>Communication delays force repeated manual follow-up</li>
          <li>No operational visibility or KPI dashboard exists</li>
          <li>Difficulty identifying recurring service failures</li>
        </ul>
        <p className="mt-4 text-sm text-surface-400">
          Full Phase 3 content will include detailed company narrative, organizational
          context, and industry background.
        </p>
      </ContentPanel>
    </div>
  );
}
