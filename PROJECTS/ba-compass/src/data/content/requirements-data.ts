// BA Compass — Requirements Content (from docs/10-business-requirements.md, 11-functional-requirements.md, 12-nonfunctional-requirements.md)
// DISCLAIMER: All data is fictional.

export interface BusinessReq {
  id: string;
  statement: string;
  justification: string;
  priority: "High" | "Medium" | "Low";
  stakeholderOwner: string;
  source: string;
  acceptanceMeasure: string;
  relatedKpi: string;
  status: "Proposed" | "Approved" | "In Progress" | "Implemented";
}

export interface FunctionalReq {
  id: string;
  statement: string;
  priority: "High" | "Medium" | "Low";
  linkedBr: string;
}

export interface NonfunctionalReq {
  id: string;
  statement: string;
  priority: "High" | "Medium" | "Low";
  acceptanceMeasure: string;
}

export const businessRequirements: BusinessReq[] = [
  { id: "BR-001", statement: "The system shall provide visibility into the status of all scheduled shifts, including confirmed, unconfirmed, in-progress, completed, and missed states.", justification: "Without shift status visibility, the organization cannot proactively identify at-risk shifts before they impact clients.", priority: "High", stakeholderOwner: "Operations Manager", source: "PP-PROC-01, PP-TECH-01", acceptanceMeasure: "All shift statuses visible in a single view, filterable by date and caregiver", relatedKpi: "KPI-001 Shift Fill Rate", status: "Proposed" },
  { id: "BR-002", statement: "The system shall identify and display open staffing gaps where no caregiver is assigned to a scheduled shift.", justification: "Open gaps must be visible before the shift start time to allow proactive gap-filling.", priority: "High", stakeholderOwner: "Scheduling Coordinator", source: "PP-PEOPLE-01, PP-PROC-01", acceptanceMeasure: "Gaps are flagged with configurable lead time before shift start", relatedKpi: "KPI-006 Open Staffing Gaps", status: "Proposed" },
  { id: "BR-003", statement: "The system shall track service issues from identification through resolution, including escalation path, ownership, and status.", justification: "Without escalation tracking, issues are handled informally with no accountability or audit trail.", priority: "High", stakeholderOwner: "Care Coordinator", source: "PP-PROC-02, PP-COMM-01", acceptanceMeasure: "All issues visible in a timeline with status, owner, and resolution", relatedKpi: "KPI-004 Avg Escalation Time", status: "Proposed" },
  { id: "BR-004", statement: "The system shall support structured follow-up on resolved issues, with assigned ownership and completion deadlines.", justification: "Without structured follow-up, recurring issues go unidentified and client satisfaction declines.", priority: "High", stakeholderOwner: "Care Coordinator", source: "PP-PROC-03, PP-RISK-02", acceptanceMeasure: "Follow-up items tracked with owner, deadline, and completion status", relatedKpi: "KPI-008 Follow-Up Rate", status: "Proposed" },
  { id: "BR-005", statement: "The system shall track service documentation completion status per shift and provide visibility into overdue documentation.", justification: "Incomplete documentation creates compliance risk and billing delays.", priority: "High", stakeholderOwner: "QA Lead", source: "PP-DATA-02, PP-RISK-01", acceptanceMeasure: "Documentation status visible per shift with completion rate metric", relatedKpi: "KPI-005 Doc Completion Rate", status: "Proposed" },
  { id: "BR-006", statement: "The system shall provide a single view that consolidates shift status, gaps, escalations, and documentation status.", justification: "Fragmented information across spreadsheets and phone calls prevents effective operational management.", priority: "High", stakeholderOwner: "Operations Manager", source: "PP-TECH-01, PP-COMM-01", acceptanceMeasure: "All operational information accessible from a single dashboard", relatedKpi: "KPI-001 through KPI-008", status: "Proposed" },
  { id: "BR-007", statement: "The system shall track client notifications related to schedule changes, cancellations, and service issues.", justification: "Clients must be informed of changes in a timely manner to maintain trust.", priority: "Medium", stakeholderOwner: "Client Services Rep", source: "PP-COMM-02, PP-CLIENT-02", acceptanceMeasure: "Notification records visible with timestamp, method, and delivery status", relatedKpi: "KPI-001 (indirect)", status: "Proposed" },
  { id: "BR-008", statement: "The system shall provide a KPI dashboard displaying defined operational metrics with trend views and configurable time periods.", justification: "Management cannot make data-driven decisions without visibility into operational performance.", priority: "High", stakeholderOwner: "Agency Owner", source: "PP-REPORT-01, PP-REPORT-02", acceptanceMeasure: "Minimum 8 KPIs displayed with trend data and time period filtering", relatedKpi: "KPI-001 through KPI-008", status: "Proposed" },
  { id: "BR-009", statement: "The system shall provide access to documented operational policies including gap-filling procedures, escalation paths, and documentation deadlines.", justification: "Consistent operational decisions require documented policies.", priority: "Medium", stakeholderOwner: "Compliance Representative", source: "PP-GOV-01", acceptanceMeasure: "Policies visible and searchable within the application", relatedKpi: "KPI-005 (indirect)", status: "Proposed" },
  { id: "BR-010", statement: "The system shall maintain an audit trail of operational actions including shift status changes, escalations, and documentation updates.", justification: "Audit trail is necessary for compliance and reconstructing events.", priority: "Medium", stakeholderOwner: "Compliance Representative", source: "PP-GOV-02, PP-RISK-01", acceptanceMeasure: "Action history visible with timestamp, user, and change details", relatedKpi: "KPI-005 (indirect)", status: "Proposed" },
  { id: "BR-011", statement: "The system shall track caregiver arrival times and identify late arrivals based on configurable thresholds.", justification: "Late arrivals affect client care quality and cannot be managed without tracking.", priority: "High", stakeholderOwner: "Operations Manager", source: "PP-DATA-01, PP-CLIENT-01", acceptanceMeasure: "Arrival times recorded per shift, late arrivals flagged with threshold", relatedKpi: "KPI-003 Late Arrival Rate", status: "Proposed" },
  { id: "BR-012", statement: "The system shall support export of operational data and reports in common formats (PDF, Markdown).", justification: "Stakeholders need the ability to share reports with team members.", priority: "Medium", stakeholderOwner: "Agency Owner", source: "PP-REPORT-01", acceptanceMeasure: "Dashboard, requirements, and risk register exportable", relatedKpi: "KPI-001 through KPI-008 (indirect)", status: "Proposed" },
  { id: "BR-013", statement: "The system shall be publicly accessible without requiring user registration or login.", justification: "Recruiters evaluating the portfolio must access the demo without barriers.", priority: "High", stakeholderOwner: "Agency Owner", source: "Project charter assumption", acceptanceMeasure: "Application loads without any authentication prompt", relatedKpi: "N/A (usability)", status: "Approved" },
  { id: "BR-014", statement: "All data displayed in the system shall be clearly labeled as synthetic/fictional.", justification: "Prevent confusion with real data and ensure ethical use of the demonstration.", priority: "High", stakeholderOwner: "Compliance Representative", source: "Privacy requirement, project charter", acceptanceMeasure: "Visible disclaimer on every page and exported document", relatedKpi: "N/A (privacy)", status: "Approved" },
  { id: "BR-015", statement: "The system shall be accessible and functional on mobile devices including smartphones and tablets.", justification: "Recruiters may review the portfolio on mobile devices.", priority: "Medium", stakeholderOwner: "IT Administrator", source: "PP-TECH-03", acceptanceMeasure: "Application functional on viewports from 375px width", relatedKpi: "N/A (usability)", status: "Approved" },
];

export const functionalRequirements: FunctionalReq[] = [
  { id: "FR-001", statement: "Operational dashboard displaying shift status, open gaps, escalation count, and documentation completion percentage", priority: "High", linkedBr: "BR-001, BR-006" },
  { id: "FR-002", statement: "Scenario selection screen with pre-defined operational scenarios", priority: "High", linkedBr: "BR-001" },
  { id: "FR-003", statement: "Stakeholder register view with roles, interests, influence levels, and pain points", priority: "High", linkedBr: "BR-001" },
  { id: "FR-004", statement: "Current-state process flow with step details including actor, input, action, output, delays, and failure points", priority: "High", linkedBr: "BR-001, BR-002" },
  { id: "FR-005", statement: "Future-state process flow showing improved workflows addressing identified gaps", priority: "High", linkedBr: "BR-001, BR-002, BR-003" },
  { id: "FR-006", statement: "Side-by-side comparison view of current-state and future-state processes", priority: "Medium", linkedBr: "BR-001, BR-002" },
  { id: "FR-007", statement: "Sortable, filterable table of business requirements with IDs, descriptions, priorities, and status", priority: "High", linkedBr: "BR-001 through BR-015" },
  { id: "FR-008", statement: "User stories display organized by stakeholder role with acceptance criteria references", priority: "High", linkedBr: "BR-001 through BR-015" },
  { id: "FR-009", statement: "Acceptance criteria view in Given/When/Then format linked to user stories", priority: "High", linkedBr: "BR-001 through BR-015" },
  { id: "FR-010", statement: "Risk register view with risk descriptions, likelihood, impact, scores, and mitigation strategies", priority: "High", linkedBr: "BR-009" },
  { id: "FR-011", statement: "KPI dashboard with calculated metrics, target comparisons, trend views, and time-period filtering", priority: "High", linkedBr: "BR-008, BR-012" },
  { id: "FR-012", statement: "Executive summary view with key findings, recommendations, and KPI highlights", priority: "High", linkedBr: "BR-008" },
  { id: "FR-013", statement: "BRD document viewer within the application", priority: "High", linkedBr: "BR-001 through BR-015" },
  { id: "FR-014", statement: "Export current view as PDF", priority: "Medium", linkedBr: "BR-012" },
  { id: "FR-015", statement: "Export requirements and risk register as Markdown", priority: "Medium", linkedBr: "BR-012" },
  { id: "FR-016", statement: "Demo data reset mechanism", priority: "Medium", linkedBr: "BR-013" },
  { id: "FR-017", statement: "Deterministic demo mode for consistent recruiter experience", priority: "Medium", linkedBr: "BR-013" },
  { id: "FR-018", statement: "No-login public access", priority: "High", linkedBr: "BR-013" },
];

export const nonfunctionalRequirements: NonfunctionalReq[] = [
  { id: "NFR-001", statement: "The application shall meet WCAG 2.1 Level AA accessibility standards for all public-facing views.", priority: "High", acceptanceMeasure: "Passes automated axe DevTools scan with zero critical or serious violations" },
  { id: "NFR-002", statement: "The application shall load initial content within 3 seconds on a standard broadband connection.", priority: "Medium", acceptanceMeasure: "Lighthouse performance score of 80+" },
  { id: "NFR-003", statement: "The application shall be fully functional on mobile devices with viewport widths of 375px and above.", priority: "High", acceptanceMeasure: "All views functional and readable at 375px, 768px, and 1920px widths" },
  { id: "NFR-004", statement: "The application shall display optimally on desktop viewports from 1024px to 2560px width.", priority: "Medium", acceptanceMeasure: "No layout breakage between 1024px and 2560px" },
  { id: "NFR-005", statement: "The application shall not expose any API keys, credentials, or internal configuration in client-side code.", priority: "High", acceptanceMeasure: "No hardcoded secrets found in client-side bundle" },
  { id: "NFR-006", statement: "The application shall not collect, store, or transmit any user data.", priority: "High", acceptanceMeasure: "Zero cookies set, zero analytics calls made" },
  { id: "NFR-007", statement: "The codebase shall use TypeScript, follow a consistent file structure, and include documentation for all major components.", priority: "Medium", acceptanceMeasure: "TypeScript compilation passes with strict mode" },
  { id: "NFR-008", statement: "The application shall function correctly when deployed as a static export or on Vercel, with no server-side runtime dependencies.", priority: "High", acceptanceMeasure: "Application loads and functions correctly on Vercel deployment" },
  { id: "NFR-009", statement: "The application shall function correctly on the latest versions of Chrome, Firefox, Safari, and Edge.", priority: "Medium", acceptanceMeasure: "All views functional in all four browsers" },
  { id: "NFR-010", statement: "All text content shall use a minimum font size of 16px for body text with sufficient contrast.", priority: "Medium", acceptanceMeasure: "No text below 16px body, contrast ratio meets WCAG AA" },
  { id: "NFR-011", statement: "All calculated KPI values shall match the formulas defined in the KPI dictionary.", priority: "High", acceptanceMeasure: "Each KPI value verified against its formula with test data" },
  { id: "NFR-012", statement: "Every view and exported document shall display a clear notice that all data is synthetic/fictional.", priority: "High", acceptanceMeasure: "Visible disclaimer on every page and every exported file" },
];
