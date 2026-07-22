# Production Smoke Test — BA Compass v1.0.0

Post-deployment verification checklist. Complete this after deploying to Vercel or any hosting platform.

---

## Prerequisites

- Deployed URL (e.g., `https://ba-compass.vercel.app`)
- Modern browser (Chrome 120+, Firefox 115+, Safari 17+)
- Mobile device or browser dev tools for responsive testing
- Internet connection

---

## Route Verification

Open each route directly by entering the URL in the address bar (do not navigate by clicking links — test deep linking).

| # | Route | Expected Content | Pass/Fail |
|---|-------|-----------------|-----------|
| 1 | `/` | Landing page with BA Compass title, KPI snapshot (8 metric cards), "Explore the Case Study" and "View the Dashboard" buttons, "Start 5-Minute Tour" link | |
| 2 | `/overview` | Project background, business scenario overview, objectives and scope boundaries | |
| 3 | `/stakeholders` | 10 stakeholder roles, power-interest matrix, expandable profiles with pain points and communication needs | |
| 4 | `/current-state` | 11-step current-state process flow with actor, delay, failure point for each step; channel reliability table | |
| 5 | `/analysis` | Gap analysis with 9 business dimensions, severity counts, dimension filtering | |
| 6 | `/dashboard` | 8 KPI metric cards, time-period filter buttons (All / Week 1 / Week 2), shift distribution pie chart, KPI target comparison bar chart, escalation/service-issue/follow-up mini charts, KPI definitions table | |
| 7 | `/future-state` | 8 future-state improvements in side-by-side comparison with current state | |
| 8 | `/requirements` | 45 requirements across 3 categories, type/priority/search filters, Edit Demo button, MD/CSV/Print export buttons, user stories toggle | |
| 9 | `/brd` | Business Requirements Document with table of contents, 12 sections (Background, Scope, BRs, FRs, NFRs, User Stories, Acceptance Criteria, Traceability, Risks, KPIs, Recommendations, Next Steps), export button | |
| 10 | `/traceability` | Traceability matrix with 15 traceability links, search input, status filter, coverage summary | |
| 11 | `/executive-summary` | Five strongest findings, KPI summary cards, top risks, priority recommendations, export button | |
| 12 | `/risks` | 15 risks with likelihood, impact, score columns; risk heatmap, category filtering, MD/CSV export buttons | |
| 13 | `/recommendations` | 11 prioritized recommendations across Immediate / Near-Term / Future categories | |
| 14 | `/project` | About the project page, 12 BA work items displayed, tools section, testing and privacy information | |
| 15 | `/responsible-ai` | AI ethics documentation, 10-item checklist, risk considerations, data ethics, transparency note | |
| 16 | `/tour` | 5-minute recruiter tour with 10 steps, progress bar, prev/next navigation, "Open full page" links | |

### 404 Handling

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| Navigate to `/this-route-does-not-exist` | Custom 404 page renders, not a browser default error page | |

---

## Interactive Feature Tests

### Requirements Editing

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| Click "Edit Demo" button | Edit mode activates, textareas and dropdowns appear for BR items | |
| Edit a BR statement field | Changes appear in the textarea | |
| Change a priority dropdown | Priority updates immediately | |
| Change a status dropdown | Status updates immediately | |
| Click "Reset" on an individual requirement | That requirement reverts to its original value | |
| Click "Done Editing" | Edit mode deactivates, table shows updated values | |
| Reload the page | Edited values persist (stored in localStorage) | |
| Click "Reset All" | Confirmation dialog appears | |
| Click "Cancel" on confirmation | Dialog closes, no data reset | |
| Click "Reset All" then confirm | All requirements revert to defaults, confirmation closes | |

### KPI Dashboard

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| Click "Week 1" filter | Charts and metrics recalculate for Jul 14–20 | |
| Click "Week 2" filter | Charts and metrics recalculate for Jul 21–27 | |
| Click "All" filter | Charts and metrics show full period (Jul 14–27) | |
| Click a metric card (e.g., Shift Fill Rate) | Drill-down table appears below the cards showing contributing records | |
| Click the same metric card again | Drill-down table closes | |
| Navigate to dashboard directly with `/dashboard#week1` | Page loads with Week 1 data (URL hash should be respected on load) | |

### Export Downloads

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| On `/requirements`, click "MD" button | Markdown file downloads with all requirements content, synthetic data notice included | |
| On `/requirements`, click "CSV" button | CSV file downloads with proper headers and comma-separated values | |
| On `/risks`, click "MD" button | Markdown file downloads with risk register content | |
| On `/risks`, click "CSV" button | CSV file downloads with risk data | |
| On `/executive-summary`, click "Export MD" | Markdown file downloads with executive summary content | |
| On `/brd`, click "Export MD" | Markdown file downloads with full BRD content | |
| On `/traceability`, click "MD" button | Markdown file downloads with traceability matrix | |
| On `/traceability`, click "CSV" button | CSV file downloads with traceability data | |

### Demo Reset

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| On `/requirements`, make edits then click "Reset All" | Confirmation dialog appears with "Cancel" and "Confirm" options | |
| Confirm the reset | All requirements revert to originals, localStorage is cleared, edited count shows 0 | |
| Reload the page after reset | Default data loads, no edits remain | |

### Recruiter Tour

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| Navigate to `/tour` | Tour starts at step 1 of 10, progress bar shows 10% | |
| Click "Next" 9 times | All 10 steps display correct content | |
| Click "Previous" | Returns to the previous step | |
| Click "Open full page" on any step | Navigates to the corresponding content page | |
| Click "Finish tour" on the last step | Returns to the landing page | |
| Click "Exit" on any step | Returns to the landing page | |

---

## localStorage Tests

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| Open browser dev tools > Application > Local Storage | Key `ba-compass-requirements-edits` exists (after editing) or is absent (after reset) | |
| Make an edit on `/requirements`, verify the localStorage value | The stored JSON contains the edited requirement ID and updated fields | |
| Clear localStorage manually, reload the page | Requirements load from default data, no edit indicators | |
| Edit some requirements, close and reopen the browser tab | Edits persist and are restored on load | |
| Make edits, reset all, verify localStorage | Key is removed from localStorage | |

Check the following notice is visible on the requirements page after making edits:
> "Demo Edit Mode: Changes are stored locally in your browser. They do not modify the source project files."

---

## Mobile Testing

Test on a device or using browser DevTools responsive mode (320px–768px width).

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| View landing page at 375px width | Content reflows to single column, no horizontal scroll | |
| Open mobile navigation menu (hamburger icon) | Navigation links are accessible and tappable | |
| Navigate to a content page | Content is readable without zoom | |
| Navigate to `/dashboard` at 375px | KPI cards display in 2-column grid, charts resize correctly | |
| Navigate to `/requirements` at 375px | Filter buttons wrap, table has horizontal scroll, edit mode fields are usable | |
| Navigate to `/tour` at 375px | Tour content fits within viewport, prev/next buttons are tappable | |
| Test touch targets | All buttons and links are at least 44x44px (WCAG minimum) | |
| Test orientation change (portrait to landscape) | Layout adjusts correctly | |
| Text is not cut off or overlapping at any breakpoint | All content is readable | |

---

## Browser Testing

Test on at least two of the following browser engines:

| Browser | Test Date | Status |
|---------|-----------|--------|
| Google Chrome (latest) | | |
| Mozilla Firefox (latest) | | |
| Apple Safari (latest) | | |
| Microsoft Edge (latest) | | |

For each browser:
- Verify all 16 routes load without errors
- Verify interactive features (editing, filters, exports)
- Verify charts render using SVG (Recharts generates SVG)
- Open browser console — there should be zero errors or warnings
- Verify no mixed content warnings (all assets served over HTTPS)

---

## Visual Tests

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| Social preview | When sharing the URL on LinkedIn/X/Facebook, the title, description, and preview image appear correctly | |
| Favicon | Browser tab shows the BA Compass favicon | |
| Print page (Ctrl+P) on any route | Navigation and interactive controls are hidden, content is clean for printing | |
| Page title | Browser tab shows "BA Compass — AI-Assisted Business Process and Requirements Analyzer" | |

---

## Console and Network Tests

| Test | Expected | Pass/Fail |
|------|----------|-----------|
| Open browser console on landing page | No errors, no warnings | |
| Open browser console on dashboard | No errors, no warnings | |
| Open browser console on requirements | No errors, no warnings | |
| Open Network tab, reload the site | All assets return 200, no 404s | |
| Verify all chunks load | No failed JavaScript or CSS requests | |
| Check for mixed content warnings | All resources served over HTTPS | |

---

## Sign-Off

| Item | Name | Date |
|------|------|------|
| Routes verified | | |
| Interactive features tested | | |
| Exports verified | | |
| Mobile testing complete | | |
| Browser testing complete | | |
| Console errors (if any) | | |

**Signed off by:** ________________________

**Date:** ________________________

**Deployed URL:** ________________________
