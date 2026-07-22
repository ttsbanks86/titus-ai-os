"use client";

import { useState } from "react";
import Link from "next/link";
import { ChevronLeft, ChevronRight, X } from "lucide-react";
import { ContentPanel } from "@/components/ui/content-panel";
import { DataNotice } from "@/components/ui/data-notice";

const tourSteps = [
  {
    title: "Welcome to BA Compass",
    page: "/",
    note: "This 5-minute tour walks through the key Business Analyst deliverables in this portfolio project. All data is synthetic — no real client information is used.",
    highlight: "Landing page with KPI snapshot",
  },
  {
    title: "The Business Problem",
    page: "/overview",
    note: "BrightCare Home Services is a fictional home-care company experiencing missed shifts, late arrivals, incomplete documentation, and fragmented communication. As a BA, my first step was to understand and document the full problem scope.",
    highlight: "Project background, objectives, and scope boundaries",
  },
  {
    title: "Stakeholder Analysis",
    page: "/stakeholders",
    note: "I identified 10 stakeholder roles, mapped their influence and interest, documented their pain points, and planned how to resolve conflicting needs between groups like Operations and Compliance.",
    highlight: "Power-interest matrix and expandable stakeholder profiles",
  },
  {
    title: "Current-State Process",
    page: "/current-state",
    note: "I documented the 11-step current workflow from shift creation to management reporting. Every step includes the actor, delay, failure point, and data gap — showing where the process breaks down.",
    highlight: "Step-by-step process visualization with failure analysis",
  },
  {
    title: "Gap Analysis",
    page: "/analysis",
    note: "I identified 21 pain points across 9 business dimensions. Each gap has a root cause, severity rating, and proposed future state.",
    highlight: "Filterable gaps by dimension with severity counts",
  },
  {
    title: "KPI Dashboard",
    page: "/dashboard",
    note: "I defined 8 operational KPIs with formulas from the KPI dictionary. The dashboard shows live calculated values with target comparisons and trend visualizations.",
    highlight: "Interactive charts and period filtering",
  },
  {
    title: "Future-State Process",
    page: "/future-state",
    note: "Based on the gap analysis, I designed a future-state process with 8 improvements. Each is linked to a business requirement and expected KPI impact.",
    highlight: "Side-by-side comparison of current vs. future state",
  },
  {
    title: "Requirements and Traceability",
    page: "/requirements",
    note: "I documented 45 requirements across business, functional, and nonfunctional categories. The traceability matrix links every requirement to a business problem, user story, acceptance criterion, KPI, and test method.",
    highlight: "Filterable requirements table and traceability view",
  },
  {
    title: "Risk Register",
    page: "/risks",
    note: "I identified 15 risks with likelihood, impact, and mitigation strategies. The risk heatmap shows where attention is most needed.",
    highlight: "Risk heatmap and category filtering",
  },
  {
    title: "My Contribution",
    page: "/project",
    note: "This project demonstrates 12 BA skill areas — from problem definition through requirements management, KPI design, risk planning, and application development. All 76 tests pass and the production build is clean.",
    highlight: "Complete list of BA contributions",
  },
];

export default function TourPage() {
  const [step, setStep] = useState(0);
  const current = tourSteps[step];

  return (
    <div className="content-container py-8">
      <div className="mx-auto max-w-2xl">
        <div className="mb-4 flex items-center justify-between">
          <h1 className="text-xl font-bold text-surface-800">5-Minute Recruiter Tour</h1>
          <Link href="/" className="flex items-center gap-1 text-sm text-surface-400 hover:text-surface-600" aria-label="Exit tour">
            <X className="h-4 w-4" /> Exit
          </Link>
        </div>
        <DataNotice />

        {/* Progress */}
        <div className="mb-4 flex items-center gap-2">
          <div className="flex-1">
            <div className="h-1.5 rounded-full bg-surface-200">
              <div className="h-1.5 rounded-full bg-brand-500 transition-all" style={{ width: `${((step + 1) / tourSteps.length) * 100}%` }} />
            </div>
          </div>
          <span className="text-xs text-surface-400">{step + 1} of {tourSteps.length}</span>
        </div>

        {/* Step Content */}
        <ContentPanel className="mb-4">
          <h2 className="text-lg font-semibold text-surface-800">{current.title}</h2>
          <p className="mt-3 text-sm text-surface-600 leading-relaxed">{current.note}</p>
          <div className="mt-3 rounded-lg border border-brand-100 bg-brand-50 p-2 text-xs text-brand-700">
            <strong>See it on the:</strong> {current.highlight}
          </div>
        </ContentPanel>

        {/* Navigation */}
        <div className="flex items-center justify-between">
          <button
            onClick={() => setStep(Math.max(0, step - 1))}
            disabled={step === 0}
            className="flex items-center gap-1 rounded-lg border border-surface-300 px-3 py-2 text-sm font-medium text-surface-700 hover:bg-surface-50 disabled:opacity-30"
          >
            <ChevronLeft className="h-4 w-4" /> Previous
          </button>

          <Link
            href={current.page}
            className="rounded-lg bg-brand-600 px-3 py-2 text-sm font-medium text-white hover:bg-brand-700"
          >
            Open full page
          </Link>

          {step < tourSteps.length - 1 ? (
            <button
              onClick={() => setStep(step + 1)}
              className="flex items-center gap-1 rounded-lg border border-surface-300 px-3 py-2 text-sm font-medium text-surface-700 hover:bg-surface-50"
            >
              Next <ChevronRight className="h-4 w-4" />
            </button>
          ) : (
            <Link
              href="/"
              className="flex items-center gap-1 rounded-lg bg-brand-600 px-3 py-2 text-sm font-medium text-white hover:bg-brand-700"
            >
              Finish tour
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
