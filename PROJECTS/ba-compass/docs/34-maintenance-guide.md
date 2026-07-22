# Maintenance Guide — BA Compass

How to maintain the BA Compass project for ongoing quality, updates, and future development.

---

## Local Development Setup

```bash
# Clone (if not already local)
git clone <repository-url>
cd PROJECTS/ba-compass

# Install dependencies
npm install

# Start development server
npm run dev

# Open http://localhost:3000
```

### Available Scripts

```bash
npm run dev          # Development server with hot reload
npm run build        # Production build (static export to out/)
npm run lint         # ESLint check
npm run typecheck    # TypeScript strict mode check (tsc --noEmit)
npm run test         # Run all 76 unit tests (Vitest)
npm run test:e2e     # Run all 14 Playwright e2e tests
npm run validate     # Full validation: typecheck + lint + test + build
```

Run `npm run validate` before every commit to catch issues early.

---

## Dependency Updates

### Regular Maintenance

```bash
# Check for outdated packages
npm outdated

# Update within semver ranges (package.json)
npm update

# Check for security vulnerabilities
npm audit
```

### Updating Specific Dependencies

```bash
# Update a single dependency to latest semver-compatible
npm update next

# Update to latest regardless of range
npm install next@latest

# Update dev dependencies
npm install -D typescript@latest
```

### Current Dependencies (v1.0.0)

| Package | Version | Purpose |
|---------|---------|---------|
| next | ^15.5.21 | Framework |
| react | ^19.1.0 | UI library |
| react-dom | ^19.1.0 | DOM rendering |
| recharts | ^2.15.3 | KPI charts |
| lucide-react | ^0.510.0 | Icons |
| class-variance-authority | ^0.7.1 | Component variants |
| clsx | ^2.1.1 | Class name utility |
| tailwind-merge | ^3.2.0 | Tailwind class merging |

### Dev Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| typescript | ^5.8.3 | Type checking |
| vitest | ^3.1.3 | Unit testing |
| @playwright/test | ^1.52.0 | E2E testing |
| @testing-library/react | ^16.3.0 | Component testing |
| @testing-library/jest-dom | ^6.6.3 | DOM matchers |
| eslint | ^9.26.0 | Linting |
| tailwindcss | ^3.4.17 | CSS framework |
| jsdom | ^26.1.0 | Test DOM environment |

### Security Vulnerability Policy

Run `npm audit` periodically. Document any vulnerabilities that cannot be resolved (e.g., no patch available) in the project's risk register and this maintenance guide.

---

## Testing Before Commits

Always run the validation pipeline before pushing:

```bash
npm run validate
```

This runs four stages in order:
1. `npm run typecheck` — TypeScript strict mode compilation
2. `npm run lint` — ESLint with Next.js config
3. `npm run test` — 76 unit tests across 3 test files
4. `npm run build` — Production static export

If any stage fails, fix the issue before committing. Do not bypass errors with `--noEmit` flags or lint-disabling comments without documented justification.

### Running Specific Tests

```bash
# Run only KPI calculation tests
npx vitest run src/tests/kpi-calculations.test.ts

# Run only validation tests
npx vitest run src/tests/validation.test.ts

# Run only app shell tests
npx vitest run src/tests/app-shell.test.tsx

# Run a single e2e test
npx playwright test --grep "landing page"
```

---

## Data Updates

All synthetic data lives in `src/data/synthetic/`. This is the authoritative dataset for all KPI calculations and dashboard content.

### Data Structure

```
src/data/synthetic/
  shifts.ts          — 42 shifts with status, timing, documentation flags
  caregivers.ts      — 10 caregiver profiles
  clients.ts         — 8 client accounts
  escalations.ts     — 6 escalation records
  documentation.ts   — 22 documentation records
  issues.ts          — 7 service issues
  followups.ts       — 7 follow-up records
  kpi-input.ts       — Aggregation layer: getAllShiftData(), getDocumentationCounts()
  index.ts           — Module exports with synthetic data disclaimer
```

### How to Modify Data

1. Edit the relevant file in `src/data/synthetic/`. Each file exports typed arrays matching the domain types in `src/types/`.

2. The aggregation layer in `kpi-input.ts` reads these arrays and produces the `KpiInput` object consumed by the KPI calculation engine. If you add or remove fields, update the aggregation logic.

3. Run the unit tests to confirm KPIs still calculate correctly:
   ```bash
   npm run test
   ```

4. Run the production build to confirm all pages render with updated data:
   ```bash
   npm run build
   ```

### Rules for Synthetic Data

- All data must remain **deterministic** — no randomness, no dates relative to "now", no seeded generation. Every run produces identical results.
- All data must remain **fictional** — no real person names, addresses, phone numbers, or identifying information.
- All files must include the synthetic data disclaimer header.
- All dates should fall within the synthetic date range (currently Jul 14–27, 2026).
- Each record must have a unique ID following the established pattern (e.g., `SH-001`, `CG-001`).
- Adding new data types requires updating the domain types in `src/types/` and the KPI input aggregation in `src/data/synthetic/kpi-input.ts`.

### Content Data

Presentation-layer content lives in `src/data/content/`:
```
src/data/content/
  gaps-data.ts           — 21 gap analysis items
  process-data.ts        — Current state (11 steps) and future state (8 improvements)
  requirements-data.ts   — 15 BRs, 18 FRs, 12 NFRs
  risks-data.ts          — 15 risks
  stakeholders.ts        — 10 stakeholders
```

These files provide textual content for pages. They reference but do not duplicate synthetic data. Modify these when updating documentation content or adding new pages.

---

## Export Verification

The export system (`src/lib/export/index.ts`) generates Markdown (.md) and CSV (.csv) files for requirements, risks, traceability, and executive summaries.

### Testing Exports

```bash
# Build the production site
npm run build

# Serve the static output
npx serve out -l 4173
```

Then manually test exports by navigating to each page and clicking export buttons:
- `/requirements` — MD + CSV
- `/risks` — MD + CSV
- `/traceability` — MD + CSV
- `/executive-summary` — MD
- `/brd` — MD

Verify each downloaded file:
- Contains correct content matching the page display
- Includes the synthetic data disclaimer
- Has correct file extension (.md or .csv)
- CSV files have proper headers and comma-separated values

---

## Browser Testing

Before any release, test in these browsers:
- **Google Chrome** (latest) — Primary development target
- **Mozilla Firefox** (latest) — Check for Gecko-specific rendering
- **Apple Safari** (latest) — Check for WebKit-specific issues
- **Microsoft Edge** (latest) — Chromium-based, usually mirrors Chrome

### Mobile Testing

Test at these widths using browser DevTools:
- 320px (small mobile)
- 375px (iPhone)
- 768px (tablet)
- 1024px (small desktop)

Key mobile behaviors to verify:
- Navigation menu opens and closes
- Dashboard charts resize
- Requirement tables scroll horizontally
- Tour steps fit the viewport
- All touch targets are at least 44x44px

---

## Release Procedure

### Patch Release (bug fix)

```bash
git checkout -b release/patch-v1.0.1
# Fix the issue
npm run validate          # Ensure all checks pass
npm version patch         # Update package.json version
# Update CHANGELOG.md
git add .
git commit -m "Release v1.0.1"
git checkout main
git merge release/patch-v1.0.1
git push origin main
```

### Minor Release (feature addition)

```bash
git checkout -b release/minor-v1.1.0
# Add feature, update docs, add tests
npm run validate          # Ensure all checks pass
npm version minor         # Update package.json version
# Update CHANGELOG.md
git add .
git commit -m "Release v1.1.0"
git checkout main
git merge release/minor-v1.1.0
git push origin main
```

### Pre-Release Checklist

1. Run `npm audit` — address or document any vulnerabilities
2. Run `npm run validate` — all four stages must pass
3. Run `npm run test:e2e` — all 14 Playwright tests must pass
4. Verify mobile responsiveness at 320px–1920px
5. Verify all exports generate correct content
6. Verify localStorage editing persists across reloads
7. Verify the production build output directory (`out/`) contains all expected HTML files

---

## Rollback Procedure

### Git Revert

If a deployed release causes issues:

```bash
# Find the commit to revert
git log --oneline -10

# Revert the release commit (safe — creates new commit undoing the changes)
git revert <commit-hash>

# Push the revert
git push origin main
```

This creates a new commit that undoes the release while preserving history. Do not use `git reset --hard` on a shared branch.

### Vercel Rollback

In the Vercel dashboard:
1. Go to your project > **Deployments**
2. Find the last known-good deployment
3. Click the three-dot menu > **Promote to Production**

No code change is needed for a Vercel-side rollback.

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push:

1. Checkout repository
2. Install dependencies
3. Run `npm run typecheck`
4. Run `npm run lint`
5. Run `npm run test`
6. Run `npm run build`

If any step fails, the workflow fails. Do not merge PRs with failing CI checks.

---

## Preserving Synthetic Data Rules

When modifying or extending the synthetic dataset:

1. **Never introduce randomness** — All data must be deterministic. Use hardcoded arrays, not random generators.
2. **Never use real data** — All names, dates, and scenarios must be fictional.
3. **Maintain data integrity** — Cross-reference counts (e.g., 42 shifts with 22 documentation records) must remain consistent. If you add shifts, verify documentation counts still align.
4. **Update aggregation logic** — If you add new data fields, update `kpi-input.ts` to aggregate them into the `KpiInput` structure.
5. **Update types** — If you add new entities, add their types in `src/types/` and update the domain types index.
6. **Update KPI functions** — If you add KPIs, add calculation functions in `src/lib/kpi/calculations.ts` and export from `src/lib/kpi/index.ts`.
7. **Write tests** — Every KPI function needs unit tests in `src/tests/kpi-calculations.test.ts`. At minimum: standard case, edge case (zero), on-target, warning, and critical status.
8. **Update content tests** — If you change content data counts, update the assertions in `src/tests/app-shell.test.tsx`.
