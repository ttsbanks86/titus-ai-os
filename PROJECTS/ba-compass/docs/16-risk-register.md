# Risk Register

**Company:** BrightCare Home Services (Fictional)  
**Document:** 16-risk-register.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Risk Register

### R-001: Scope Growth

| Field | Value |
|-------|-------|
| ID | R-001 |
| Description | Project scope expands beyond portfolio needs, adding features that do not demonstrate BA skills |
| Category | Scope |
| Likelihood | High (4) |
| Impact | Medium (3) |
| Risk Score | 12 (High) |
| Owner | Business Analyst |
| Mitigation | Document clear scope boundaries in charter, review scope against BA skill demonstration goals before adding features |
| Contingency | If scope grows, defer non-essential features to "future enhancement" list |
| Trigger | Stakeholder request for features outside BRD scope |
| Status | Active |

### R-002: Incorrect KPI Calculations

| Field | Value |
|-------|-------|
| ID | R-002 |
| Description | KPI values calculated incorrectly in the demo, undermining analytical credibility |
| Category | Quality |
| Likelihood | Medium (3) |
| Impact | High (4) |
| Risk Score | 12 (High) |
| Owner | Business Analyst / Developer |
| Mitigation | Define all KPI formulas in the KPI dictionary before implementation; unit-test every KPI calculation |
| Contingency | If KPI error found, fix formula, update affected data, and re-verify |
| Trigger | KPI value does not match manual calculation from demo data |
| Status | Active |

### R-003: Synthetic Data Appearing Real

| Field | Value |
|-------|-------|
| ID | R-003 |
| Description | Demo synthetic data could be mistaken for real operational data |
| Category | Privacy |
| Likelihood | Low (2) |
| Impact | High (4) |
| Risk Score | 8 (Medium) |
| Owner | Business Analyst |
| Mitigation | Label all data as synthetic on every page; use clearly fictional names and company identifiers |
| Contingency | If data is mistaken for real, add additional disclaimers and review data patterns |
| Trigger | External inquiry about real data |
| Status | Active |

### R-004: Privacy Exposure

| Field | Value |
|-------|-------|
| ID | R-004 |
| Description | Real personal information accidentally included in synthetic data |
| Category | Privacy |
| Likelihood | Low (1) |
| Impact | High (4) |
| Risk Score | 4 (Low) |
| Owner | Business Analyst |
| Mitigation | Use only fictional names and data; never copy from real sources; scan all data before commit |
| Contingency | If real data found, immediately remove and replace with synthetic equivalent |
| Trigger | Data scan or review identifies real information |
| Status | Active |

### R-005: AI Hallucinations in Demo

| Field | Value |
|-------|-------|
| ID | R-005 |
| Description | If AI integration is added in the future, AI-generated content may contain inaccuracies or hallucinations |
| Category | Quality |
| Likelihood | Medium (3) |
| Impact | Medium (3) |
| Risk Score | 9 (Medium) |
| Owner | Business Analyst |
| Mitigation | No AI API dependency in core MVP; any future AI integration will be clearly identified as AI-generated |
| Contingency | Remove AI features if they cannot be made reliable |
| Trigger | AI-generated content with factual errors |
| Status | Active |

### R-006: Poor Recruiter Usability

| Field | Value |
|-------|-------|
| ID | R-006 |
| Description | Recruiters find the demo confusing, cluttered, or difficult to navigate |
| Category | Usability |
| Likelihood | Medium (3) |
| Impact | High (4) |
| Risk Score | 12 (High) |
| Owner | Business Analyst |
| Mitigation | Design with recruiter walkthrough in mind; clear navigation; limit to essential views; test with peers |
| Contingency | Gather feedback and iterate on navigation and content layout |
| Trigger | User feedback or observed navigation difficulty |
| Status | Active |

### R-007: Broken Export Functions

| Field | Value |
|-------|-------|
| ID | R-007 |
| Description | PDF or Markdown export functions fail or produce unusable output |
| Category | Technical |
| Likelihood | Medium (3) |
| Impact | Medium (3) |
| Risk Score | 9 (Medium) |
| Owner | Developer |
| Mitigation | Unit-test export functions; verify output format validity |
| Contingency | Provide manual copy-paste fallback instructions |
| Trigger | Export produces empty or malformed file |
| Status | Active |

### R-008: Mobile Layout Failure

| Field | Value |
|-------|-------|
| ID | R-008 |
| Description | Application layout breaks on mobile viewports |
| Category | Technical |
| Likelihood | Medium (3) |
| Impact | Medium (3) |
| Risk Score | 9 (Medium) |
| Owner | Developer |
| Mitigation | Responsive design from the start; test on 375px, 768px, and 1920px viewports |
| Contingency | Fix layout issues iteratively; consider mobile-first CSS approach |
| Trigger | Layout break at any viewport width |
| Status | Active |

### R-009: Inaccessible Process Diagrams

| Field | Value |
|-------|-------|
| ID | R-009 |
| Description | Process flow diagrams are not readable by screen readers or cannot be understood without color coding |
| Category | Accessibility |
| Likelihood | Medium (3) |
| Impact | Medium (3) |
| Risk Score | 9 (Medium) |
| Owner | Developer |
| Mitigation | Provide text-based alternative descriptions for all diagrams; ensure color is not the only differentiator |
| Contingency | If diagram library lacks a11y support, provide a text table fallback |
| Trigger | Screen reader test reveals inaccessible diagram content |
| Status | Active |

### R-010: Deployment Failure

| Field | Value |
|-------|-------|
| ID | R-010 |
| Description | Application fails to deploy on Vercel or does not function after deployment |
| Category | Technical |
| Likelihood | Low (2) |
| Impact | High (4) |
| Risk Score | 8 (Medium) |
| Owner | Developer |
| Mitigation | Test build locally before deploy; use Vercel's recommended Next.js configuration |
| Contingency | If Vercel fails, consider alternative static hosting (Netlify, GitHub Pages) |
| Trigger | Build or deployment error |
| Status | Active |

### R-011: Exposed API Keys or Secrets

| Field | Value |
|-------|-------|
| ID | R-011 |
| Description | API keys, secrets, or credentials accidentally included in the codebase |
| Category | Security |
| Likelihood | Low (2) |
| Impact | High (4) |
| Risk Score | 8 (Medium) |
| Owner | Developer |
| Mitigation | No API keys in code; use environment variables if needed; scan before commit |
| Contingency | Rotate exposed keys immediately; remove from history |
| Trigger | Security scan or code review identifies exposed secret |
| Status | Active |

### R-012: Weak Requirement Traceability

| Field | Value |
|-------|-------|
| ID | R-012 |
| Description | Some requirements or features lack clear traceability to business problems |
| Category | Quality |
| Likelihood | Medium (3) |
| Impact | Medium (3) |
| Risk Score | 9 (Medium) |
| Owner | Business Analyst |
| Mitigation | Complete RTM during Phase 1; verify every high-priority feature has traceability links |
| Contingency | Remediate missing links during quality review |
| Trigger | RTM review reveals gaps |
| Status | Active |

### R-013: Overengineering

| Field | Value |
|-------|-------|
| ID | R-013 |
| Description | Solution becomes more complex than necessary for a portfolio demonstration |
| Category | Scope |
| Likelihood | High (4) |
| Impact | Low (2) |
| Risk Score | 8 (Medium) |
| Owner | Business Analyst |
| Mitigation | Prioritize simple stack; resist adding unnecessary features; focus on BA skill demonstration |
| Contingency | Simplify or remove overengineered components |
| Trigger | Architecture or feature decisions exceed portfolio needs |
| Status | Active |

### R-014: Timeline Slippage

| Field | Value |
|-------|-------|
| ID | R-014 |
| Description | Project takes longer than expected, delaying the career package and job applications |
| Category | Project Management |
| Likelihood | Medium (3) |
| Impact | Medium (3) |
| Risk Score | 9 (Medium) |
| Owner | Business Analyst |
| Mitigation | Prioritize Phase 1-3 as MVP; defer lower-priority features; track progress against milestones |
| Contingency | Reduce scope for later phases if timeline pressure increases |
| Trigger | Missed milestone date |
| Status | Active |

### R-015: Requirements Duplication or Conflict

| Field | Value |
|-------|-------|
| ID | R-015 |
| Description | Requirements across BR, FR, and NFR documents lack consistency or have conflicting statements |
| Category | Quality |
| Likelihood | Medium (3) |
| Impact | Medium (3) |
| Risk Score | 9 (Medium) |
| Owner | Business Analyst |
| Mitigation | Cross-reference all requirements during creation; review for consistency before Phase 1 sign-off |
| Contingency | Correct conflicting requirements and update affected documents |
| Trigger | Cross-document review reveals inconsistency |
| Status | Active |

---

## Risk Summary

| Risk Level | Count | IDs |
|-----------|-------|-----|
| High (12+) | 3 | R-001, R-002, R-006 |
| Medium (8-11) | 10 | R-003, R-005, R-007, R-008, R-009, R-010, R-011, R-012, R-013, R-014, R-015 |
| Low (1-4) | 2 | R-004 |
| **Total** | **15** | R-001 through R-015 |

---

## Risk Categories

| Category | Count | Risk IDs |
|----------|-------|----------|
| Scope | 2 | R-001, R-013 |
| Quality | 3 | R-002, R-005, R-012, R-015 |
| Privacy | 2 | R-003, R-004 |
| Usability | 1 | R-006 |
| Technical | 3 | R-007, R-008, R-010 |
| Accessibility | 1 | R-009 |
| Security | 1 | R-011 |
| Project Management | 1 | R-014 |

---

## Related Documents

- 01-project-charter.md — Initial risks
- 09-business-requirements-document.md — BRD risks section
- 17-assumptions-and-constraints.md — Boundaries
