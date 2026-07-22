# Known Limitations — BA Compass v1.0.0

This document describes the known limitations of the BA Compass application. These are design decisions, scoping choices, and areas where the application does not emulate production-grade software. Each limitation includes its impact and the rationale.

---

## Static Dataset

**Limitation:** All data (42 shifts, 10 caregivers, 8 clients, etc.) is hardcoded in TypeScript modules. There is no mechanism to load or generate new data without modifying source files.

**Impact:** The dataset is fixed. Users cannot explore scenarios beyond the built-in Jul 14–27, 2026 timeframe. KPI values never change unless the source code is edited and rebuilt.

**Rationale:** This is a portfolio demonstration, not a live operational tool. Static data ensures deterministic behavior for presentations and eliminates the need for a database.

---

## No Dynamic Data Loading

**Limitation:** The application is fully static. No API endpoints, server functions, or database connections exist. All data is compiled into the HTML at build time.

**Impact:** No real-time data updates. No data refresh without redeployment. No ability to connect to live systems.

**Rationale:** Static architecture eliminates hosting costs, security risks, and operational complexity. Suitable for a portfolio whose purpose is to demonstrate BA documentation skills, not live operations.

---

## No Real AI Integration

**Limitation:** Despite the subtitle "AI-Assisted Business Process and Requirements Analyzer," the application contains no AI services, no LLM integrations, and no machine learning. All analysis is pre-written by the author.

**Impact:** The "AI-Assisted" label refers to the application's positioning as a tool that could be enhanced with AI, not to any built-in AI capability. No features generate content or provide intelligent recommendations dynamically.

**Rationale:** Avoiding AI API dependencies keeps the project zero-cost, zero-key, and zero-privacy-risk. AI features could be added as an optional enhancement (see `38-future-roadmap.md`).

---

## No User Authentication

**Limitation:** There is no login system, no user accounts, no session management. Every visitor sees the same content.

**Impact:** No personalized experiences. No audit trail of who viewed or edited what. No way to restrict access to sensitive content.

**Rationale:** The project is a public portfolio intended for recruiters and hiring managers. Authentication adds complexity without serving the portfolio's purpose.

---

## No Database

**Limitation:** No PostgreSQL, SQLite, or any database. Data lives in TypeScript source files.

**Impact:** No queryability, no joins, no indexing. All data access is read from compiled arrays. There is no write path for any data except in-memory state.

**Rationale:** A database would increase hosting costs, add security requirements, and complicate deployment. Static data is sufficient for a portfolio project.

---

## No Backend

**Limitation:** Zero server-side code. The application contains no server functions, API routes, middleware, or backend logic.

**Impact:** No dynamic request handling. No server-side validation. No email sending. No file processing. No webhooks.

**Rationale:** The application is built as a static site to demonstrate BA documentation and front-end skills. A backend was not required for the project's objectives.

---

## No PDF Export Library

**Limitation:** PDF export uses the browser's native print-to-PDF functionality rather than a dedicated library like jsPDF or react-pdf.

**Impact:** PDF output quality depends on the browser and printer settings. Users must manually use Ctrl+P / Cmd+P and select "Save as PDF." Page breaks, margins, and fonts vary between browsers. No programmatic PDF generation.

**Rationale:** Browser print-to-PDF is zero-dependency, zero-cost, and works reliably for the table-heavy layouts in this application. A dedicated PDF library could be added in a future update.

---

## localStorage-Dependent Editing

**Limitation:** Requirement edits are stored exclusively in the browser's localStorage. Edits are lost if:
- The user clears browser data
- The user switches to a different browser or device
- localStorage quota is exceeded (typically 5MB)
- The user is in private browsing mode (varies by browser)

**Impact:** No cross-device sync. No backup of edits. Data can be accidentally lost.

**Rationale:** This is a demo feature intended to showcase interactive editing, not a production document management system. Genuine document editing should use dedicated tools (Google Docs, Notion, etc.).

---

## No Full-Text Search

**Limitation:** The search feature on the requirements page filters by ID prefix and keyword match against the statement field. There is no full-text search across all pages, all content modules, or all documentation fields.

**Impact:** Users searching for specific terms across content pages must navigate manually.

**Rationale:** Full-text search across a static site would require either a search index library (like Lunr.js or Fuse.js) or a third-party service (like Algolia). Not warranted for a portfolio project with 19 pages.

---

## No Multi-User Support

**Limitation:** The application has no concept of users, roles, or permissions. Multiple people cannot simultaneously view or edit with conflict resolution.

**Impact:** Useful only for single-user demonstrations. Not suitable for team collaboration or workshop use.

**Rationale:** Multi-user support requires a database, API, real-time coordination (WebSockets), and authentication. Out of scope for this project.

---

## No Real-Time Updates

**Limitation:** There are no WebSockets, Server-Sent Events, or polling mechanisms. All data is static. No notifications, alerts, or live updates.

**Impact:** Users must manually refresh to see any changes. There is no mechanism for real-time operational monitoring.

**Rationale:** Real-time features require a server runtime and are unnecessary for a static portfolio demonstrating BA documentation.

---

## Limited KPI Time Range

**Limitation:** Synthetic data spans exactly two weeks (Jul 14–27, 2026). The period filter on the dashboard (Full / Week 1 / Week 2) operates within this fixed range.

**Impact:** No historical trend analysis. No month-over-month or year-over-year comparisons. No ability to demonstrate long-term KPI tracking.

**Rationale:** The synthetic dataset was sized to demonstrate KPI calculations and dashboard features without overwhelming the built-in data volume. A larger dataset would increase the codebase size and build time.

---

## No Data Import Capability

**Limitation:** There is no file upload, CSV import, or API-based data ingestion. All data must be manually entered into TypeScript source files.

**Impact:** Users cannot bring their own data. The application works exclusively with the built-in synthetic BrightCare Home Services dataset.

**Rationale:** CSV import and validation are a potential future enhancement (see `38-future-roadmap.md`). Excluded from v1.0.0 to maintain scope.

---

## No API Integrations

**Limitation:** The application does not integrate with any external services — no Jira, Confluence, Slack, email, or calendar APIs.

**Impact:** Cannot demonstrate or simulate BA tool integrations. No data exchange with real systems.

**Rationale:** API integrations would require backend infrastructure, API keys, and ongoing maintenance. Out of scope for a static portfolio project.

---

## No Mobile App

**Limitation:** The application is a responsive web application but not a native mobile app. There is no iOS or Android version, no push notifications, no device API access.

**Impact:** Mobile users access the site through a browser. Offline access is limited to cached pages. No home screen widget.

**Rationale:** A mobile app would require separate development effort and is not part of the project's scope.

---

## No Offline Support

**Limitation:** The static site works offline only if explicitly cached via service worker. No service worker is configured. The site requires an internet connection to load.

**Impact:** No offline access. Users cannot browse the portfolio without network connectivity.

**Rationale:** A service worker and offline caching strategy could be added but are not required for the primary use case (online portfolio review). Not included to keep the deployment simple.
