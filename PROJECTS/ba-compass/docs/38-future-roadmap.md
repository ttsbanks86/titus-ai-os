# Future Roadmap — BA Compass

Planned and aspirational enhancements for the BA Compass project beyond v1.0.0. Each item includes priority, effort estimate, and dependencies.

Priority levels:
- **P0** — Critical path for project evolution
- **P1** — High value, should pursue
- **P2** — Nice to have
- **P3** — Aspirational

Effort estimates: **S** (< 1 week), **M** (1–3 weeks), **L** (1–2 months), **XL** (2+ months)

---

## Near Term (0–3 Months)

### 1. Data Import from CSV

Add a client-side CSV parser that allows users to upload their own shift, caregiver, or client data and see KPI calculations from their imported data.

| | |
|---|----|
| **Priority** | P1 |
| **Effort** | M |
| **Dependencies** | File upload UI, CSV parsing library (Papa Parse), validation schema for each entity type, fallback to synthetic data on error |
| **Status** | Not started |

### 2. User Feedback Collection

Add a lightweight, privacy-respecting feedback mechanism (optional, no account required) for recruiters and reviewers to leave comments on the project.

| | |
|---|----|
| **Priority** | P1 |
| **Effort** | S |
| **Dependencies** | Feedback form component, data storage (email-to-form service or simple Airtable/Google Sheets integration), privacy policy update |
| **Status** | Not started |

### 3. Enhanced Navigation

Add a breadcrumb trail, site map, and keyboard shortcut (e.g., `?` key) for showing available shortcuts.

| | |
|---|----|
| **Priority** | P2 |
| **Effort** | S |
| **Dependencies** | Layout component modification |
| **Status** | Not started |

### 4. Dark Mode

Add a theme toggle for light/dark mode with persistence in localStorage.

| | |
|---|----|
| **Priority** | P2 |
| **Effort** | M |
| **Dependencies** | Tailwind dark mode configuration, color token audit, theme toggle component, localStorage persistence |
| **Status** | Not started |

---

## Medium Term (3–6 Months)

### 5. AI-Assisted Requirements Generation (Optional)

Integrate an LLM API (user-provided key, no built-in cost) to suggest requirement phrasings, generate user stories from input, or identify gaps in existing requirements.

| | |
|---|----|
| **Priority** | P1 |
| **Effort** | L |
| **Dependencies** | AI service abstraction layer (provider-agnostic), optional key configuration, prompt engineering for BA context, human-review-before-apply workflow, synthetic data disclaimer on AI output |
| **Status** | Not started |
| **Notes** | Must be explicitly optional, require user API key, and label all AI-generated content. No AI data should mix with synthetic data. |

### 6. Advanced KPI Forecasting

Extend the KPI engine with trend analysis using linear regression or simple forecasting to predict future KPI values based on the existing dataset.

| | |
|---|----|
| **Priority** | P2 |
| **Effort** | M |
| **Dependencies** | Extended synthetic dataset (more weeks of data), trend calculation library or custom function, visualization component for trend lines |
| **Status** | Not started |

### 7. Export to Professional Formats

Replace browser print-to-PDF with a dedicated library (jsPDF or react-pdf) for programmatic PDF generation. Add DOCX export using a library like docx.js.

| | |
|---|----|
| **Priority** | P1 |
| **Effort** | M |
| **Dependencies** | PDF library integration (jsPDF / @react-pdf/renderer), DOCX library integration (docx.js), template design for each document type |
| **Status** | Not started |

### 8. Guided BA Methodology Wizard

Add a step-by-step wizard that guides users through the BA process: define problem → identify stakeholders → map process → analyze gaps → write requirements → define KPIs → plan implementation.

| | |
|---|----|
| **Priority** | P2 |
| **Effort** | L |
| **Dependencies** | Wizard state management, progress tracking, optional data export at each step, integration with existing content pages |
| **Status** | Not started |

---

## Long Term (6–12 Months)

### 9. Multi-Scenario Support

Add support for additional fictional companies and industries beyond BrightCare Home Services. Allow users to switch between scenarios (e.g., BrightCare Home Services, GreenLeaf Logistics, Riverbend Retail).

| | |
|---|----|
| **Priority** | P2 |
| **Effort** | XL |
| **Dependencies** | Scenario data architecture (pluggable data modules), scenario selector component, updated synthetic data engine for multiple companies, documentation for each scenario |
| **Status** | Not started |

### 10. Integration with Real BA Tools

Add optional integration connectors for Jira (export requirements as issues), Confluence (publish BRD to wiki), and Slack (share KPI summaries).

| | |
|---|----|
| **Priority** | P3 |
| **Effort** | XL |
| **Dependencies** | External API authentication, OAuth flow or API key configuration, mapping between BA Compass data models and tool-specific schemas |
| **Status** | Not started |
| **Notes** | All integrations must be optional, require user-provided credentials, and clearly indicate that data will be sent to third-party services. |

### 11. Offline Support with Service Worker

Add a service worker for caching the application and enabling offline access. Useful for presentations where internet connectivity may be unreliable.

| | |
|---|----|
| **Priority** | P2 |
| **Effort** | M |
| **Dependencies** | Service worker registration, cache strategy (pre-cache all static assets on first load), offline fallback page, testing across browsers |
| **Status** | Not started |

---

## Separate Project

### 12. BA Compass Work Simulation Lab

A companion project where users can work through realistic BA scenarios — receive a business problem brief, identify stakeholders, write requirements, define KPIs, and receive automated feedback. This would transform BA Compass from a read-only portfolio into an interactive learning tool.

| | |
|---|----|
| **Priority** | P0 (separate project) |
| **Effort** | XL |
| **Dependencies** | Scenario content library, answer validation engine, scoring rubric, progress tracking (localStorage or account-based) |
| **Status** | Planned as separate project |

---

## Summary

| Timeline | Items | Total Effort |
|----------|-------|--------------|
| Near term (0–3 months) | 4 items | ~6–9 weeks |
| Medium term (3–6 months) | 4 items | ~14–20 weeks |
| Long term (6–12 months) | 3 items | ~18–26 weeks |
| Separate project | 1 item | ~8+ weeks |

All dates and effort estimates are approximate. Items may be reprioritized, deferred, or descoped based on feedback and available development time.
