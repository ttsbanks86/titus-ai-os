"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { PageHeading } from "@/components/ui/page-heading";
import { SectionHeading } from "@/components/ui/section-heading";
import { ContentPanel } from "@/components/ui/content-panel";
import { currentStateSteps } from "@/data/content/process-data";

const breakdowns = [
  { issue: "Fragmented Communication", detail: "Information scattered across phone, email, text, and paper. No single source of truth." },
  { issue: "Delayed Detection", detail: "Missed shifts and late arrivals discovered reactively after client impact." },
  { issue: "No Shared Status", detail: "No centralized view of shift status, gaps, or escalations across the team." },
  { issue: "Manual Escalation", detail: "Issues passed through undefined channels with no audit trail or ownership tracking." },
  { issue: "Incomplete Documentation", detail: "No tracking of documentation completion. Compliance risk cannot be measured." },
  { issue: "Weak Reporting", detail: "Management reports compiled manually. Data is weeks out of date by the time it reaches decision-makers." },
];

export default function CurrentStatePage() {
  const [expandedStep, setExpandedStep] = useState<number | null>(null);

  return (
    <div className="content-container py-8">
      <PageHeading title="Current-State Process" subtitle="As-is workflow — BrightCare Home Services (Fictional)" />

      {/* Key Breakdowns */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Process Breakdowns at a Glance" description="Six systemic failures in the current workflow" />
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {breakdowns.map((b) => (
            <div key={b.issue} className="rounded-lg border border-red-200 bg-red-50 p-3">
              <div className="font-medium text-red-800">{b.issue}</div>
              <p className="mt-1 text-xs text-red-600">{b.detail}</p>
            </div>
          ))}
        </div>
      </ContentPanel>

      {/* Process Flow Visualization */}
      <ContentPanel className="mb-6">
        <SectionHeading title="Process Flow" description="11-step workflow from shift creation to management reporting" />
        <div className="overflow-x-auto" role="region" aria-label="Process flow diagram">
          <div className="flex min-w-[800px] flex-nowrap gap-2 py-4">
            {currentStateSteps.map((step, i) => (
              <div key={step.step} className="flex shrink-0 flex-col items-center">
                <div className={`flex h-10 w-10 items-center justify-center rounded-full text-sm font-bold text-white ${
                  step.failurePoint.includes("No") ? "bg-red-500" : "bg-amber-500"
                }`}>
                  {step.step}
                </div>
                <div className="mt-1 text-center text-xs font-medium text-surface-700">{step.name}</div>
                <div className="mt-0.5 text-center text-[10px] text-surface-400">{step.actor}</div>
                {i < currentStateSteps.length - 1 && <div className="mt-1 h-8 w-0.5 bg-surface-300" aria-hidden="true" />}
              </div>
            ))}
          </div>
        </div>
        <div className="mt-2 flex items-center gap-4 text-xs text-surface-400">
          <span className="flex items-center gap-1"><span className="inline-block h-3 w-3 rounded-full bg-red-500" /> Failure point</span>
          <span className="flex items-center gap-1"><span className="inline-block h-3 w-3 rounded-full bg-amber-500" /> Delay or risk</span>
        </div>
      </ContentPanel>

      {/* Step Details */}
      <SectionHeading title="Step-by-Step Analysis" description="Each step with actor, delay, failure point, and data gap" />
      <div className="mb-6 space-y-2">
        {currentStateSteps.map((step) => (
          <ContentPanel key={step.step}>
            <button
              onClick={() => setExpandedStep(expandedStep === step.step ? null : step.step)}
              className="flex w-full items-center justify-between text-left"
              aria-expanded={expandedStep === step.step}
            >
              <div className="flex items-center gap-3">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-surface-200 text-xs font-bold text-surface-600">{step.step}</span>
                <div>
                  <span className="font-medium text-surface-800">{step.name}</span>
                  <span className="ml-2 text-xs text-surface-400">{step.actor}</span>
                </div>
              </div>
              {expandedStep === step.step ? <ChevronUp className="h-4 w-4 text-surface-400" /> : <ChevronDown className="h-4 w-4 text-surface-400" />}
            </button>
            {expandedStep === step.step && (
              <div className="mt-3 grid gap-3 border-t border-surface-100 pt-3 text-sm sm:grid-cols-2">
                <div><span className="font-medium text-surface-700">Action:</span><p className="text-surface-600">{step.action}</p></div>
                <div><span className="font-medium text-surface-700">Channel:</span><p className="text-surface-600">{step.channel}</p></div>
                <div><span className="font-medium text-red-600">Delay:</span><p className="text-surface-600">{step.delay}</p></div>
                <div><span className="font-medium text-red-600">Failure Point:</span><p className="text-surface-600">{step.failurePoint}</p></div>
                <div><span className="font-medium text-amber-600">Manual Work:</span><p className="text-surface-600">{step.manualWork}</p></div>
                <div><span className="font-medium text-amber-600">Data Gap:</span><p className="text-surface-600">{step.dataGap}</p></div>
                <div className="sm:col-span-2"><span className="font-medium text-red-600">Control Weakness:</span><p className="text-surface-600">{step.controlWeakness}</p></div>
              </div>
            )}
          </ContentPanel>
        ))}
      </div>

      {/* Communication Channels */}
      <ContentPanel>
        <SectionHeading title="Communication Channel Reliability" description="Every interaction relies on fragmented, low-reliability channels" />
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-surface-200 text-sm">
            <thead className="bg-surface-50">
              <tr>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Interaction</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Channel</th>
                <th className="px-3 py-2 text-left font-medium text-surface-600">Reliability</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-surface-100">
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Shift assignment</td><td className="px-3 py-2">Phone / text</td><td className="px-3 py-2 text-red-600">Low — no written confirmation</td></tr>
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Shift confirmation</td><td className="px-3 py-2">Verbal</td><td className="px-3 py-2 text-red-600">Low — can be forgotten</td></tr>
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Late notification</td><td className="px-3 py-2">Phone</td><td className="px-3 py-2 text-red-600">Low — depends on caregiver initiative</td></tr>
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Gap notification</td><td className="px-3 py-2">Phone</td><td className="px-3 py-2 text-red-600">Low — depends on discovery</td></tr>
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Escalation</td><td className="px-3 py-2">Phone / email</td><td className="px-3 py-2 text-amber-600">Medium — depends on recipient</td></tr>
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Client communication</td><td className="px-3 py-2">Phone</td><td className="px-3 py-2 text-red-600">Low — voicemail may be missed</td></tr>
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Issue follow-up</td><td className="px-3 py-2">Phone / email</td><td className="px-3 py-2 text-red-600">Low — no system</td></tr>
              <tr className="hover:bg-surface-50"><td className="px-3 py-2">Reporting</td><td className="px-3 py-2">Email / meeting</td><td className="px-3 py-2 text-red-600">Low — manual compilation</td></tr>
            </tbody>
          </table>
        </div>
      </ContentPanel>

      <div className="mt-6 text-right">
        <a href="/analysis" className="text-sm font-medium text-brand-600 hover:text-brand-700">Next: Gap Analysis →</a>
      </div>
    </div>
  );
}
