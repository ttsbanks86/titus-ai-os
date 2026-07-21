# Decision Log

**Company:** BrightCare Home Services (Fictional)  
**Document:** 24-decision-log.md  
**Date:** July 21, 2026  
**Author:** Titus Banks — Business Analyst  

---

## Decision Log

### DEC-001: Project Location

| Field | Value |
|-------|-------|
| Decision ID | DEC-001 |
| Date | 2026-07-21 |
| Decision | Place BA Compass project at `PROJECTS/ba-compass/` within the Live Cowork workspace |
| Options Considered | 1. `PROJECTS/ba-compass/` — follows existing project structure |
| | 2. Root of workspace — conflicts with existing file conventions |
| | 3. New top-level directory — inconsistent with project organization |
| Rationale | The workspace has a `PROJECTS/` directory with established project subdirectories. Placing BA Compass here follows the existing pattern, keeps the root clean, and isolates the project from production Titus Platform services. |
| Impact | All project files will be created under `PROJECTS/ba-compass/`. No production files are modified. |
| Status | Implemented |

### DEC-002: Fictional Company Name

| Field | Value |
|-------|-------|
| Decision ID | DEC-002 |
| Date | 2026-07-21 |
| Decision | Use "BrightCare Home Services" as the fictional home-care company |
| Options Considered | 1. BrightCare Home Services — professional, descriptive |
| | 2. CompassionCare — common in home care |
| | 3. HomeFirst Care — more generic |
| Rationale | "BrightCare" is distinct, professional, and not associated with any real company. The name conveys quality and reliability appropriate for the scenario. |
| Impact | All documents, data, and scenarios will reference BrightCare Home Services. |
| Status | Implemented |

### DEC-003: Document Numbering Convention

| Field | Value |
|-------|-------|
| Decision ID | DEC-003 |
| Date | 2026-07-21 |
| Decision | Use two-digit numerical prefix for document files (01-, 02-, etc.) |
| Options Considered | 1. `01-project-charter.md` — numbered, readable |
| | 2. `project-charter.md` — no sequencing |
| | 3. `BA-001-project-charter.md` — verbose |
| Rationale | Two-digit numbering provides clear sequencing while remaining readable. This matches documentation conventions used in some existing workspace files. |
| Impact | Documents will be consistently ordered in file listings and easy to reference. |
| Status | Implemented |

### DEC-004: Requirement ID Format

| Field | Value |
|-------|-------|
| Decision ID | DEC-004 |
| Date | 2026-07-21 |
| Decision | Use BR-XXX, FR-XXX, NFR-XXX, US-XXX, AC-XXX, R-XXX, KPI-XXX format |
| Options Considered | 1. Prefix + sequential number — clear category identification |
| | 2. Single sequential numbering — simpler but harder to identify type |
| | 3. Hierarchical (BR.1.1) — too complex for this scope |
| Rationale | Prefix format immediately identifies requirement type and is standard BA practice. |
| Impact | All requirements, stories, criteria, risks will follow this format. |
| Status | Implemented |

### DEC-005: Architecture - No AI API Dependency

| Field | Value |
|-------|-------|
| Decision ID | DEC-005 |
| Date | 2026-07-21 |
| Decision | The public MVP must work without any AI API. AI features are optional future enhancements. |
| Options Considered | 1. No AI API dependency (chosen) — zero cost, no configuration |
| | 2. Optional AI API — recruiter must configure keys |
| | 3. Built-in AI API — cost, dependency, configuration burden |
| Rationale | Recruiters must be able to view the demo without configuring API keys. Core functionality at zero cost. No single point of failure. |
| Impact | Architecture uses local data only. No AI API calls in the MVP. Any future AI features will be optional. |
| Status | Implemented |

### DEC-006: Stakeholder Count

| Field | Value |
|-------|-------|
| Decision ID | DEC-006 |
| Date | 2026-07-21 |
| Decision | Include 10 fictional stakeholder roles |
| Options Considered | 1. 10 stakeholders — comprehensive coverage |
| | 2. 6-7 stakeholders — simpler but less complete |
| | 3. 12+ stakeholders — overly complex for portfolio |
| Rationale | 10 stakeholders covers all key roles in a home-care agency (from owner to client) while remaining manageable for a portfolio project. |
| Impact | Stakeholder analysis covers operations, compliance, management, client, and field perspectives. |
| Status | Implemented |

### DEC-007: Technology Stack

| Field | Value |
|-------|-------|
| Decision ID | DEC-007 |
| Date | 2026-07-21 |
| Decision | Use Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui, Recharts, Vitest, Playwright, Vercel |
| Options Considered | 1. Next.js + TypeScript + Tailwind (chosen) — modern, proven, recruiter-friendly |
| | 2. React + Vite — simpler but fewer features |
| | 3. Static HTML/CSS/JS — too basic for demonstration |
| Rationale | This stack demonstrates modern web development skills while being practical for a solo portfolio project. All tools have strong community support. |
| Impact | Architecture proposal documents this stack. Implementation begins in Phase 2. |
| Status | Documented (not yet implemented) |

### DEC-008: Project Scope - Excluded Areas

| Field | Value |
|-------|-------|
| Decision ID | DEC-008 |
| Date | 2026-07-21 |
| Decision | Exclude payroll, billing, EHR, clinical decision-making, GPS tracking, and authentication from scope |
| Options Considered | 1. Exclude areas unrelated to BA skill demonstration (chosen) |
| | 2. Include some for completeness — scope creep risk |
| Rationale | These areas do not directly demonstrate BA analysis skills. Including them would add complexity without proportional portfolio value. |
| Impact | Clear scope boundaries documented in 04-scope.md. These areas are out of scope for all phases. |
| Status | Implemented |

### DEC-009: Synthetic Data Approach

| Field | Value |
|-------|-------|
| Decision ID | DEC-009 |
| Date | 2026-07-21 |
| Decision | Generate synthetic data as TypeScript modules with clearly fictional names |
| Options Considered | 1. TypeScript modules (chosen) — type-safe, easy to maintain |
| | 2. JSON files — simpler but less type safety |
| | 3. Generate at build time — more complex |
| Rationale | TypeScript modules provide type safety and are easy to import. Synthetic names are clearly fictional (e.g., Maria Garcia, Eleanor Whitfield). |
| Impact | Data layer will be TypeScript modules. All names and patterns are fictional. |
| Status | Documented |

### DEC-010: Traceability Verification

| Field | Value |
|-------|-------|
| Decision ID | DEC-010 |
| Date | 2026-07-21 |
| Decision | Verify traceability through a manual cross-reference check after all documents are created |
| Options Considered | 1. Manual cross-reference (chosen) — appropriate for Phase 1 scope |
| | 2. Automated RTM verification — overengineered for documentation phase |
| | 3. Spreadsheet-based tracking — less integrated |
| Rationale | Manual cross-reference verification is appropriate for Phase 1. If traceability issues are found, they will be corrected before Phase 2 begins. |
| Impact | Quality control step includes re-reading all documents and verifying links. |
| Status | Complete |

### DEC-011: Package Manager

| Field | Value |
|-------|-------|
| Decision ID | DEC-011 |
| Date | 2026-07-21 |
| Decision | Use npm (not pnpm) for the ba-compass project |
| Options Considered | 1. npm (chosen) — parent workspace uses npm, most universal |
| | 2. pnpm — available but no workspace config in parent repo |
| | 3. yarn — not installed |
| Rationale | npm is already used by the parent workspace (package-lock.json exists). Using npm avoids confusion with mixed lockfiles in the monorepo-style layout. |
| Impact | package-lock.json will be created in PROJECTS/ba-compass/. Minor warning about multiple lockfiles is acceptable. |
| Status | Implemented |

### DEC-012: Next.js Version

| Field | Value |
|-------|-------|
| Decision ID | DEC-012 |
| Date | 2026-07-21 |
| Decision | Use Next.js 15.5.21 (not 16.x) for stability |
| Options Considered | 1. Next.js 15.5.21 (chosen) — stable, well-tested, all libraries compatible |
| | 2. Next.js 16.2.11 — latest but may have compatibility issues with Recharts, shadcn/ui |
| Rationale | Next.js 15.5 is battle-tested with React 19, Tailwind CSS 3, and all selected libraries. Version 16 is recently released and may introduce breaking changes or library incompatibilities. The architecture doc specifies "Next.js 14+", so 15.5 is within scope. |
| Impact | Using Next.js 15.5.21. Plans to upgrade to 16.x can be evaluated later. |
| Status | Implemented |

### DEC-013: Testing Strategy

| Field | Value |
|-------|-------|
| Decision ID | DEC-013 |
| Date | 2026-07-21 |
| Decision | Use Vitest for unit tests + Playwright for e2e tests |
| Options Considered | 1. Vitest + Playwright (chosen) — matches architecture proposal |
| | 2. Jest + Testing Library — slower than Vitest |
| | 3. Cypress — heavier than Playwright for this scope |
| Rationale | Vitest provides fast, native TypeScript unit tests with the same API as Jest. Playwright is the modern standard for e2e testing. Both are well-documented and recruiter-friendly. |
| Impact | 41 unit tests (Vitest) + 6 e2e tests (Playwright) covering KPI calculations, component rendering, and application smoke tests. |
| Status | Implemented |

### DEC-014: Synthetic Data Approach

| Field | Value |
|-------|-------|
| Decision ID | DEC-014 |
| Date | 2026-07-21 |
| Decision | Create deterministic synthetic data as static TypeScript modules |
| Options Considered | 1. Static TypeScript modules (chosen) — deterministic, type-safe, easy to maintain |
| | 2. JSON files — simpler but less integrated |
| | 3. Build-time generation — more complex, harder to debug |
| Rationale | Static TypeScript modules provide type safety, deterministic results for testing, and easy maintainability. The data is designed to demonstrate all KPI edge cases. |
| Impact | Dataset includes 42 shifts, 10 caregivers, 8 clients, 6 escalations, 22 documentation records, 7 service issues, and 7 follow-up records. All data uses fictional identifiers. |
| Status | Implemented |

### DEC-015: Static Export Configuration

| Field | Value |
|-------|-------|
| Decision ID | DEC-015 |
| Date | 2026-07-21 |
| Decision | Configure Next.js for static export (`output: "export"`) |
| Options Considered | 1. Static export (chosen) — no server needed, Vercel-ready |
| | 2. Server-rendered — unnecessary for a data-only demo |
| | 3. SSG with ISR — overengineered for this scope |
| Rationale | The application uses only static data (no API routes, no database). Static export is the simplest deployment model and supports zero-cost hosting on Vercel or any static host. |
| Impact | Build produces an `out/` directory with pure static HTML/CSS/JS. No server runtime needed. |
| Status | Implemented |

---

## Related Documents

- 25-change-log.md — Change history
- 23-definition-of-done.md — Completion criteria
