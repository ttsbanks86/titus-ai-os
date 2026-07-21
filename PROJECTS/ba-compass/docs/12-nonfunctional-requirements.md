# Nonfunctional Requirements

**Company:** BrightCare Home Services (Fictional)  
**Document:** 12-nonfunctional-requirements.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Nonfunctional Requirements

### NFR-001: Accessibility

| Field | Value |
|-------|-------|
| ID | NFR-001 |
| Statement | The application shall meet WCAG 2.1 Level AA accessibility standards for all public-facing views. |
| Business Justification | Portfolio must be accessible to all recruiters, including those using assistive technologies. |
| Priority | High |
| Acceptance Measure | Passes automated axe DevTools scan with zero critical or serious violations |
| Verification Method | Automated accessibility scan + manual keyboard navigation test |
| Status | Proposed |

### NFR-002: Performance

| Field | Value |
|-------|-------|
| ID | NFR-002 |
| Statement | The application shall load initial content within 3 seconds on a standard broadband connection. Navigation between pages shall complete within 1 second. |
| Business Justification | Slow load times create a poor recruiter experience and may cause abandonment. |
| Priority | Medium |
| Acceptance Measure | Lighthouse performance score of 80+ |
| Verification Method | Lighthouse audit, manual timing |
| Status | Proposed |

### NFR-003: Mobile Responsiveness

| Field | Value |
|-------|-------|
| ID | NFR-003 |
| Statement | The application shall be fully functional on mobile devices with viewport widths of 375px and above. |
| Business Justification | Recruiters may review the portfolio on smartphones or tablets. |
| Priority | High |
| Acceptance Measure | All views functional and readable at 375px, 768px, and 1920px widths |
| Verification Method | Viewport testing at specified widths |
| Status | Proposed |

### NFR-004: Desktop Responsiveness

| Field | Value |
|-------|-------|
| ID | NFR-004 |
| Statement | The application shall display optimally on desktop viewports from 1024px to 2560px width. |
| Business Justification | Most recruiters will view on desktop monitors. |
| Priority | Medium |
| Acceptance Measure | No layout breakage between 1024px and 2560px |
| Verification Method | Manual viewport testing |
| Status | Proposed |

### NFR-005: Security - No Exposure

| Field | Value |
|-------|-------|
| ID | NFR-005 |
| Statement | The application shall not expose any API keys, credentials, secrets, or internal configuration in client-side code. |
| Business Justification | Even a portfolio project must follow security best practices to demonstrate professional standards. |
| Priority | High |
| Acceptance Measure | No hardcoded secrets found in client-side bundle |
| Verification Method | Code review, bundle inspection |
| Status | Proposed |

### NFR-006: Privacy - No Data Collection

| Field | Value |
|-------|-------|
| ID | NFR-006 |
| Statement | The application shall not collect, store, or transmit any user data. No cookies, tracking, or analytics shall be implemented. |
| Business Justification | Portfolio viewers should not be tracked or have their data collected. |
| Priority | High |
| Acceptance Measure | Zero cookies set, zero analytics calls made |
| Verification Method | Browser DevTools network and application inspection |
| Status | Proposed |

### NFR-007: Maintainability

| Field | Value |
|-------|-------|
| ID | NFR-007 |
| Statement | The codebase shall use TypeScript, follow a consistent file structure, and include documentation for all major components. |
| Business Justification | The portfolio code should demonstrate professional software development practices. |
| Priority | Medium |
| Acceptance Measure | TypeScript compilation passes with strict mode, components documented |
| Verification Method | Code review, TypeScript compilation |
| Status | Proposed |

### NFR-008: Reliability

| Field | Value |
|-------|-------|
| ID | NFR-008 |
| Statement | The application shall function correctly when deployed as a static export or on Vercel, with no server-side runtime dependencies. |
| Business Justification | The application must work reliably on the chosen deployment platform without backend infrastructure. |
| Priority | High |
| Acceptance Measure | Application loads and functions correctly on Vercel deployment |
| Verification Method | Deployed URL walkthrough |
| Status | Proposed |

### NFR-009: Browser Compatibility

| Field | Value |
|-------|-------|
| ID | NFR-009 |
| Statement | The application shall function correctly on the latest versions of Chrome, Firefox, Safari, and Edge. |
| Business Justification | Recruiters may use any modern browser; compatibility must not be assumed. |
| Priority | Medium |
| Acceptance Measure | All views functional in all four browsers |
| Verification Method | Manual testing in each browser |
| Status | Proposed |

### NFR-010: Readability

| Field | Value |
|-------|-------|
| ID | NFR-010 |
| Statement | All text content shall use a minimum font size of 16px for body text, with sufficient contrast (minimum 4.5:1 ratio). |
| Business Justification | Documentation-heavy portfolio must be readable without strain. |
| Priority | Medium |
| Acceptance Measure | No text below 16px body, contrast ratio meets WCAG AA |
| Verification Method | Visual inspection, contrast checker |
| Status | Proposed |

### NFR-011: Data Integrity

| Field | Value |
|-------|-------|
| ID | NFR-011 |
| Statement | All calculated KPI values shall match the formulas defined in the KPI dictionary. No hardcoded metric values shall be used. |
| Business Justification | Incorrect calculations would undermine the credibility of the BA analysis. |
| Priority | High |
| Acceptance Measure | Each KPI value verified against its formula with test data |
| Verification Method | Unit tests for each KPI calculation |
| Status | Proposed |

### NFR-012: Synthetic Data Labeling

| Field | Value |
|-------|-------|
| ID | NFR-012 |
| Statement | Every view and exported document shall display a clear notice that all data is synthetic/fictional. |
| Business Justification | Prevents confusion with real data and ensures ethical demonstration. |
| Priority | High |
| Acceptance Measure | Visible disclaimer on every page and every exported file |
| Verification Method | Visual inspection of all views and exports |
| Status | Proposed |

---

## Requirements Summary

| Priority | Count | IDs |
|----------|-------|-----|
| High | 7 | NFR-001, NFR-003, NFR-005, NFR-006, NFR-008, NFR-011, NFR-012 |
| Medium | 5 | NFR-002, NFR-004, NFR-007, NFR-009, NFR-010 |
| Low | 0 | — |
| **Total** | **12** | NFR-001 through NFR-012 |

---

## NFR Traceability

| Nonfunctional Requirement | Supporting BR | Supporting FR |
|--------------------------|---------------|---------------|
| NFR-001 Accessibility | BR-013, BR-015 | FR-001 through FR-018 |
| NFR-002 Performance | BR-013 | FR-001 through FR-018 |
| NFR-003 Mobile Responsiveness | BR-015 | FR-001 through FR-018 |
| NFR-004 Desktop Responsiveness | BR-015 | FR-001 through FR-018 |
| NFR-005 Security | BR-014 | FR-018 |
| NFR-006 Privacy | BR-014 | FR-018 |
| NFR-007 Maintainability | (General) | (General) |
| NFR-008 Reliability | BR-013 | FR-018 |
| NFR-009 Browser Compatibility | BR-015 | FR-001 through FR-018 |
| NFR-010 Readability | BR-013 | FR-001 through FR-018 |
| NFR-011 Data Integrity | BR-008 | FR-011 |
| NFR-012 Synthetic Data Labeling | BR-014 | FR-001 through FR-018 |

---

## Related Documents

- 10-business-requirements.md — Business requirements
- 11-functional-requirements.md — Functional requirements
- 15-requirements-traceability-matrix.md — Traceability
