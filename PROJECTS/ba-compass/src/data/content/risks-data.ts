// BA Compass — Risk Register Content (from docs/16-risk-register.md)
// DISCLAIMER: All data is fictional.

export interface RiskContent {
  id: string;
  description: string;
  category: string;
  likelihood: number;
  impact: number;
  riskScore: number;
  riskLevel: "High" | "Medium" | "Low";
  owner: string;
  mitigation: string;
  contingency: string;
  trigger: string;
  status: string;
}

export const risks: RiskContent[] = [
  { id: "R-001", description: "Scope growth beyond portfolio needs, adding features that do not demonstrate BA skills", category: "Scope", likelihood: 4, impact: 3, riskScore: 12, riskLevel: "High", owner: "Business Analyst", mitigation: "Document clear scope boundaries in charter; review scope against BA skill demonstration goals before adding features", contingency: "Defer non-essential features to future enhancement list", trigger: "Stakeholder request for features outside BRD scope", status: "Active" },
  { id: "R-002", description: "KPI values calculated incorrectly in the demo, undermining analytical credibility", category: "Quality", likelihood: 3, impact: 4, riskScore: 12, riskLevel: "High", owner: "Business Analyst / Developer", mitigation: "Define all KPI formulas in the KPI dictionary before implementation; unit-test every KPI calculation", contingency: "If KPI error found, fix formula, update affected data, and re-verify", trigger: "KPI value does not match manual calculation from demo data", status: "Active" },
  { id: "R-003", description: "Demo synthetic data could be mistaken for real operational data", category: "Privacy", likelihood: 2, impact: 4, riskScore: 8, riskLevel: "Medium", owner: "Business Analyst", mitigation: "Label all data as synthetic on every page; use clearly fictional names", contingency: "If data is mistaken for real, add additional disclaimers", trigger: "External inquiry about real data", status: "Active" },
  { id: "R-004", description: "Real personal information accidentally included in synthetic data", category: "Privacy", likelihood: 1, impact: 4, riskScore: 4, riskLevel: "Low", owner: "Business Analyst", mitigation: "Use only fictional names and data; never copy from real sources; scan all data before commit", contingency: "If real data found, immediately remove and replace with synthetic equivalent", trigger: "Data scan or review identifies real information", status: "Active" },
  { id: "R-005", description: "If AI integration is added in the future, AI-generated content may contain inaccuracies or hallucinations", category: "Quality", likelihood: 3, impact: 3, riskScore: 9, riskLevel: "Medium", owner: "Business Analyst", mitigation: "No AI API dependency in core MVP; any future AI integration will be clearly identified as AI-generated", contingency: "Remove AI features if they cannot be made reliable", trigger: "AI-generated content with factual errors", status: "Active" },
  { id: "R-006", description: "Recruiters find the demo confusing, cluttered, or difficult to navigate", category: "Usability", likelihood: 3, impact: 4, riskScore: 12, riskLevel: "High", owner: "Business Analyst", mitigation: "Design with recruiter walkthrough in mind; clear navigation; limit to essential views; test with peers", contingency: "Gather feedback and iterate on navigation and content layout", trigger: "User feedback or observed navigation difficulty", status: "Active" },
  { id: "R-007", description: "PDF or Markdown export functions fail or produce unusable output", category: "Technical", likelihood: 3, impact: 3, riskScore: 9, riskLevel: "Medium", owner: "Developer", mitigation: "Unit-test export functions; verify output format validity", contingency: "Provide manual copy-paste fallback instructions", trigger: "Export produces empty or malformed file", status: "Active" },
  { id: "R-008", description: "Application layout breaks on mobile viewports", category: "Technical", likelihood: 3, impact: 3, riskScore: 9, riskLevel: "Medium", owner: "Developer", mitigation: "Responsive design from the start; test on 375px, 768px, and 1920px viewports", contingency: "Fix layout issues iteratively", trigger: "Layout break at any viewport width", status: "Active" },
  { id: "R-009", description: "Process flow diagrams are not readable by screen readers or cannot be understood without color coding", category: "Accessibility", likelihood: 3, impact: 3, riskScore: 9, riskLevel: "Medium", owner: "Developer", mitigation: "Provide text-based alternative descriptions for all diagrams; ensure color is not the only differentiator", contingency: "If diagram library lacks a11y support, provide text table fallback", trigger: "Screen reader test reveals inaccessible diagram content", status: "Active" },
  { id: "R-010", description: "Application fails to deploy on Vercel or does not function after deployment", category: "Technical", likelihood: 2, impact: 4, riskScore: 8, riskLevel: "Medium", owner: "Developer", mitigation: "Test build locally before deploy; use Vercel's recommended Next.js configuration", contingency: "If Vercel fails, consider alternative static hosting (Netlify, GitHub Pages)", trigger: "Build or deployment error", status: "Active" },
  { id: "R-011", description: "API keys, secrets, or credentials accidentally included in the codebase", category: "Security", likelihood: 2, impact: 4, riskScore: 8, riskLevel: "Medium", owner: "Developer", mitigation: "No API keys in code; use environment variables if needed; scan before commit", contingency: "Rotate exposed keys immediately; remove from history", trigger: "Security scan or code review identifies exposed secret", status: "Active" },
  { id: "R-012", description: "Some requirements or features lack clear traceability to business problems", category: "Quality", likelihood: 3, impact: 3, riskScore: 9, riskLevel: "Medium", owner: "Business Analyst", mitigation: "Complete RTM during Phase 1; verify every high-priority feature has traceability links", contingency: "Remediate missing links during quality review", trigger: "RTM review reveals gaps", status: "Active" },
  { id: "R-013", description: "Solution becomes more complex than necessary for a portfolio demonstration", category: "Scope", likelihood: 4, impact: 2, riskScore: 8, riskLevel: "Medium", owner: "Business Analyst", mitigation: "Prioritize simple stack; resist adding unnecessary features; focus on BA skill demonstration", contingency: "Simplify or remove overengineered components", trigger: "Architecture or feature decisions exceed portfolio needs", status: "Active" },
  { id: "R-014", description: "Project takes longer than expected, delaying the career package and job applications", category: "Project Management", likelihood: 3, impact: 3, riskScore: 9, riskLevel: "Medium", owner: "Business Analyst", mitigation: "Prioritize Phase 1-3 as MVP; defer lower-priority features; track progress against milestones", contingency: "Reduce scope for later phases if timeline pressure increases", trigger: "Missed milestone date", status: "Active" },
  { id: "R-015", description: "Requirements across BR, FR, and NFR documents lack consistency or have conflicting statements", category: "Quality", likelihood: 3, impact: 3, riskScore: 9, riskLevel: "Medium", owner: "Business Analyst", mitigation: "Cross-reference all requirements during creation; review for consistency before Phase 1 sign-off", contingency: "Correct conflicting requirements and update affected documents", trigger: "Cross-document review reveals inconsistency", status: "Active" },
];

export const riskCategorySummary = [
  { category: "Scope", count: 2, ids: "R-001, R-013" },
  { category: "Quality", count: 4, ids: "R-002, R-005, R-012, R-015" },
  { category: "Privacy", count: 2, ids: "R-003, R-004" },
  { category: "Usability", count: 1, ids: "R-006" },
  { category: "Technical", count: 3, ids: "R-007, R-008, R-010" },
  { category: "Accessibility", count: 1, ids: "R-009" },
  { category: "Security", count: 1, ids: "R-011" },
  { category: "Project Management", count: 1, ids: "R-014" },
];
