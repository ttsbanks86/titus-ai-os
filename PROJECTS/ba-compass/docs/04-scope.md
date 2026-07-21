# Project Scope

**Company:** BrightCare Home Services (Fictional)  
**Document:** 04-scope.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## In Scope

### Analysis and Documentation

- Shift-status visibility analysis
- Staffing-gap identification process
- Missed-shift and late-arrival tracking requirements
- Service-documentation completion tracking
- Escalation process and follow-up tracking
- KPI reporting and dashboard requirements
- Current-state (as-is) workflow documentation
- Future-state (to-be) workflow design
- Requirements management and traceability
- Risk tracking and mitigation planning
- Responsible AI planning for optional future features
- Executive summary and BRD generation

### Demonstration Application

- Public-facing web application (no login required)
- Scenario selection and navigation
- Stakeholder register and analysis views
- Current-state process visualization
- Future-state process comparison
- Business requirements table with filtering
- Functional and nonfunctional requirements views
- User stories with acceptance criteria display
- Risk register viewer
- KPI dashboard with calculated metrics
- Executive summary view
- BRD document viewer
- Export functions (PDF, Markdown)
- Deterministic demo mode for consistent recruiter experience
- Demo data reset capability

### Data

- Synthetic shift records
- Synthetic caregiver profiles (fictional names, no real identities)
- Synthetic client account records (fictional, no real PII)
- Synthetic assignment, escalation, and documentation records
- Synthetic KPI results calculated from demo data
- All data clearly labeled as synthetic/fictional

---

## Out of Scope

### Operations and Business Processes

- Payroll processing or integration
- Billing or invoicing systems
- Clinical decision-making support
- Medication management or prescription tracking
- Electronic health records (EHR) or medical records
- Real employee scheduling or time tracking
- Real client records or PII storage
- Automated hiring, credentialing, or onboarding
- Production deployment for a real home-care agency
- Legal or regulatory certification
- Real-time GPS tracking or geofencing
- Medical advice, triage, or clinical recommendations
- Direct caregiver monitoring or surveillance

### Technology

- Real-time communication systems (chat, SMS integration)
- API connections to real scheduling or HR systems
- Authentication or user account system
- Payment processing
- Third-party data integrations
- Mobile app (native iOS/Android)
- Real-time notifications or alerts
- Video conferencing or telehealth features

### Compliance and Legal

- HIPAA compliance certification
- Regulatory audit preparation
- Legal review or advice
- Insurance or liability documentation
- Employment law compliance
- Licensing or credentialing verification

---

## Scope Boundaries

| Boundary | Definition |
|----------|------------|
| Organizational | BrightCare Home Services (fictional) only |
| Functional | Shift operations, issue tracking, documentation, reporting |
| Data | Synthetic data only — no real PII or PHI |
| User access | Public, no login required |
| Technology | Browser-based web application |
| Geographic | United States (English language) |
| Time | Portfolio project — no ongoing operations |
| Budget | Zero operational cost for core functionality |

---

## Scope Governance

Scope changes will be documented in the decision log (23-decision-log.md) and change log (24-change-log.md). Any proposed scope addition must:

1. Be traceable to a business problem or stakeholder need
2. Not introduce real data or PII
3. Not require a paid API or service for core functionality
4. Not modify production Titus Platform services
5. Be documented with rationale and impact assessment

---

## Related Documents

- 01-project-charter.md — Project overview and scope summary
- 03-business-case.md — Business justification
- 17-assumptions-and-constraints.md — Project boundaries
