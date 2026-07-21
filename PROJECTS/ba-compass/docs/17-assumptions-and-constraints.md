# Assumptions and Constraints

**Company:** BrightCare Home Services (Fictional)  
**Document:** 17-assumptions-and-constraints.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Assumptions

### User Assumptions

| ID | Assumption | Rationale |
|----|-----------|-----------|
| A-001 | Recruiters reviewing this project will have limited time (under 10 minutes per review) | Portfolio projects must be scannable and well-organized |
| A-002 | Demo users will not create accounts or provide personal information | No authentication should be required |
| A-003 | Recruiters may view the project on mobile devices | Mobile responsiveness is essential |
| A-004 | Recruiters value demonstrated methodology over technical complexity | Focus on BA skills, not engineering sophistication |
| A-005 | Hiring managers want to see traceability from problem through solution | RTM is a key demonstration artifact |

### Data Assumptions

| ID | Assumption | Rationale |
|----|-----------|-----------|
| A-006 | All data used is synthetic and fictional | No real PII, PHI, or employer data |
| A-007 | Synthetic data is sufficient for demonstrating BA skills | Real data is not required for a portfolio |
| A-008 | Demo data must be deterministic for consistent recruiter experience | Same data every time ensures reliable demos |
| A-009 | Data patterns should reflect realistic operational scenarios | Credible demonstration requires believable data |
| A-010 | All data must be clearly labeled as synthetic | Prevents confusion with real information |

### Technical Assumptions

| ID | Assumption | Rationale |
|----|-----------|-----------|
| A-011 | The public version must work without a paid AI service | Zero operational cost for core functionality |
| A-012 | The application will be deployed as a static site or on Vercel | Simple deployment without backend infrastructure |
| A-013 | Modern browser features are available | No need to support legacy browsers |
| A-014 | Standard broadband internet is available for demo access | No offline mode required |
| A-015 | The technology stack can be simple and well-documented | Maintainability for solo developer |

### Project Assumptions

| ID | Assumption | Rationale |
|----|-----------|-----------|
| A-016 | The project is a portfolio demonstration, not a production system | Scope is bounded by demonstration goals |
| A-017 | No real employer, client, or patient data will be used at any stage | Ethical and legal boundaries |
| A-018 | The project will be completed by a single developer (Titus Banks) | Solo portfolio project |
| A-019 | Phase 2-6 will follow after Phase 1 documentation is complete | Sequential phased approach |
| A-020 | Feedback from recruiters may lead to refinement | Iterative improvement expected |

---

## Constraints

### Data Constraints

| ID | Constraint | Impact |
|----|-----------|--------|
| C-001 | No real healthcare data may be used | All data must be synthetic |
| C-002 | No personal identifiable information (PII) may be stored | No real names, addresses, phones, emails |
| C-003 | No protected health information (PHI) may be used | No medical records or clinical data |
| C-004 | No real employer data may be used | Fictional company only |
| C-005 | Data must be clearly labeled as synthetic/fictional | Disclaimer on every view |

### Technical Constraints

| ID | Constraint | Impact |
|----|-----------|--------|
| C-006 | No paid third-party API may be required for core functionality | All features must work with zero operational cost |
| C-007 | No backend server or database may be required | Static or serverless deployment only |
| C-008 | No authentication system may be implemented | Public access without login |
| C-009 | No cookies, tracking, or analytics may be used | Privacy-preserving demo |
| C-010 | No real-time communication or external integrations | Self-contained application |

### Project Constraints

| ID | Constraint | Impact |
|----|-----------|--------|
| C-011 | Limited development time (solo portfolio project) | Scope must be realistic |
| C-012 | No modification to production Titus Platform services | Isolated project location |
| C-013 | Must follow existing workspace repository conventions | Consistent project structure |
| C-014 | Low or zero hosting cost for public access | Vercel or static hosting only |
| C-015 | Simple technology stack for maintainability | Next.js, TypeScript, Tailwind |

### Scope Constraints

| ID | Constraint | Impact |
|----|-----------|--------|
| C-016 | No payroll, billing, or financial processing | Out of scope |
| C-017 | No EHR, clinical decision-making, or medical functionality | Out of scope |
| C-018 | No real-time GPS tracking or geofencing | Out of scope |
| C-019 | No mobile app development (native iOS/Android) | Responsive web only |
| C-020 | No production deployment for a real home-care agency | Portfolio only |

---

## Assumptions vs. Constraints Summary

| Category | Assumptions | Constraints |
|----------|-------------|-------------|
| User | 5 | 0 |
| Data | 5 | 5 |
| Technical | 5 | 5 |
| Project | 5 | 5 |
| Scope | 0 | 5 |
| **Total** | **20** | **20** |

---

## Related Documents

- 04-scope.md — Detailed scope boundaries
- 01-project-charter.md — Charter constraints
