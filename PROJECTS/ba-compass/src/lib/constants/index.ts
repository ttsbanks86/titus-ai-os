// BA Compass — Application Constants

export const APP = {
  NAME: "BA Compass",
  SUBTITLE: "AI-Assisted Business Process and Requirements Analyzer",
  COMPANY: "BrightCare Home Services",
  COMPANY_SHORT: "BrightCare",
  DESCRIPTION: "A recruiter-ready Business Analyst portfolio project demonstrating end-to-end business analysis through a fictional home-care services case study.",
} as const;

export const SYNTHETIC_NOTICE = "All data displayed here is synthetic and fictional. This is a portfolio demonstration project. No real client, caregiver, or patient information is used." as const;

export const NAV_ITEMS = [
  { label: "Overview", href: "/overview" },
  { label: "Stakeholders", href: "/stakeholders" },
  { label: "Current State", href: "/current-state" },
  { label: "Gap Analysis", href: "/analysis" },
  { label: "KPI Dashboard", href: "/dashboard" },
  { label: "Future State", href: "/future-state" },
  { label: "Requirements", href: "/requirements" },
  { label: "Risks", href: "/risks" },
  { label: "Recommendations", href: "/recommendations" },
  { label: "About the Project", href: "/project" },
  { label: "Responsible AI", href: "/responsible-ai" },
] as const;

// Sequential navigation for prev/next links
export const NAV_SEQUENCE = [
  { label: "Home", href: "/" },
  { label: "Overview", href: "/overview" },
  { label: "Stakeholders", href: "/stakeholders" },
  { label: "Current State", href: "/current-state" },
  { label: "Gap Analysis", href: "/analysis" },
  { label: "KPI Dashboard", href: "/dashboard" },
  { label: "Future State", href: "/future-state" },
  { label: "Requirements", href: "/requirements" },
  { label: "Risks", href: "/risks" },
  { label: "Recommendations", href: "/recommendations" },
  { label: "About the Project", href: "/project" },
  { label: "Responsible AI", href: "/responsible-ai" },
] as const;

export const STATUS_COLORS = {
  success: "bg-green-100 text-green-800 border-green-200",
  warning: "bg-yellow-100 text-yellow-800 border-yellow-200",
  error: "bg-red-100 text-red-800 border-red-200",
  info: "bg-blue-100 text-blue-800 border-blue-200",
  neutral: "bg-gray-100 text-gray-800 border-gray-200",
} as const;

// Late arrival threshold in minutes
export const LATE_ARRIVAL_THRESHOLD_MINUTES = 15;

// Documentation completion window in hours
export const DOCUMENTATION_WINDOW_HOURS = 24;

// Escalation targets
export const TARGET_ESCALATION_MINUTES = 30;
export const WARNING_ESCALATION_MINUTES = 60;

// KPI Targets (from docs/18-kpi-dictionary.md)
export const KPI_TARGETS = {
  SHIFT_FILL_RATE: 95,
  MISSED_SHIFT_RATE: 2,
  LATE_ARRIVAL_RATE: 10,
  AVG_ESCALATION_TIME: 30, // minutes
  DOC_COMPLETION_RATE: 95,
  OPEN_STAFFING_GAPS: 3,
  ISSUE_RESOLUTION_TIME: 4, // hours
  FOLLOW_UP_COMPLETION_RATE: 90,
} as const;

// KPI Warning Thresholds
export const KPI_WARNINGS = {
  SHIFT_FILL_RATE: 90,
  MISSED_SHIFT_RATE: 5,
  LATE_ARRIVAL_RATE: 15,
  AVG_ESCALATION_TIME: 60, // minutes
  DOC_COMPLETION_RATE: 85,
  OPEN_STAFFING_GAPS: 5,
  ISSUE_RESOLUTION_TIME: 8, // hours
  FOLLOW_UP_COMPLETION_RATE: 75,
} as const;
