# CEO Final Decision Checklist — 2026-06-06 (POST-APPROVAL)

**Purpose:** Single source of truth for every decision the CEO has made on the Struck Down But Not Destroyed book launch. Supersedes the 2026-06-06 v0.2 placeholder decision card.

**Status:** 3 of 4 CEO decisions are FINAL and LOCKED. 1 remains BLOCKED pending separate approval.

---

## Block 1 — FINAL AND LOCKED (3 of 4)

| # | Decision | FINAL Value | Locked at | Used by |
|---|----------|-------------|-----------|---------|
| 1 | **Type family** | Display: **Playfair Display** / Body: **Inter** | 2026-06-06 | All Priority A assets, email headers, concept test variations. No re-render required. |
| 2 | **Campaign tagline** | **"You're not done yet"** | 2026-06-06 | All 5 IG story frames, all email subject lines, all FB ad copy, all landing page hero text, all 3 concept test variations. Options B–E retired. |
| 4 | **Paid ad sales scenario** | **Scenario B** ($750–1,500 ad spend → 269 books) | 2026-06-06 | All KPI targets, budget tables, performance plan cadence. Scenarios A (216 books, $0 ads) and C (435 books, $3,000 ads) retained as sensitivity ranges. |

---

## Block 2 — BLOCKED, PENDING SEPARATE CEO APPROVAL (1 of 4)

| # | Decision | Current state | What unblocks it | When it would be decided |
|---|----------|---------------|------------------|--------------------------|
| 3 | **Author photo session (A13, A14, A15)** | NOT APPROVED. No photographer contacted. No money to be spent. | Separate, explicit CEO approval to commission a 1-hour session at $300–800 | After v0.3 → concept test → Priority A production planning is locked. Likely Day 7-10 of the launch sprint. |

---

## Block 3 — INTERNAL INCONSISTENCY FIXES (ALL APPLIED IN v0.3)

All 6 CEO-mandated corrections are integrated into v0.3. None remains.

| # | Fix | v0.2 state | v0.3 state |
|---|-----|------------|------------|
| 1 | Priority A AI generation count | Stated 3 ways (11-13 / 14-17 / 8-10) | Unified to **14-17** everywhere. Phase 2 subset adjusted to 8-9 to reconcile math (6-8 Phase 0 + 8-9 Phase 2 = 14-17 total). |
| 2 | Concept test duration | "3-4 days" in 1 place, "5 days" in 2 places | Unified to **5 days** everywhere |
| 3 | Concept test generation count | "6" in 2 places, "6-8" in 6 places | Unified to **6-8** everywhere |
| 4 | Scenario totals (A / B / C) | Narrative 219 / 275 / 450 vs table 216 / 269 / 435 | Narrative corrected to **216 / 269 / 435** to match table. Email-driven sales co-fix: 6 / 9 / 15 (not 9 / 15 / 30) |
| 5 | "+ 12 author-brand assets" | Approval Checklist said +12 | Corrected to **+ 3 author-brand assets** (A13, A14, A15) |
| 6 | Vestigial v0.9 references | 4 occurrences | All replaced with v0.3 (or "RESOLVED in v0.3" where item is now locked) |

---

## Block 4 — DOWNSTREAM PROPAGATION FIXES (ALL APPLIED IN v0.3)

The consistency audit also flagged 2 downstream tables that referenced the v0.2 numbers, not the v0.3 numbers. Both fixed.

| # | Section | Was | Now |
|---|---------|-----|-----|
| 1 | Section 10 Performance Plan — Primary KPIs table | `Total copies sold \| 300 in 90 days` | `269 in 90 days (Scenario B baseline); 216 floor (Scenario A); 435 stretch (Scenario C)` |
| 2 | Section 15 Sales targets table | `Books sold in 90 days \| 300 \| 200-400 (midpoint 300)` | `269 \| 216-435 (midpoint 269; Scenario B baseline)` |

---

## Block 5 — v0.2 BRIEF STATUS

| File | Status |
|------|--------|
| `CDO-Struck-Down-Full-Brief-v0.2.md` | **SUPERSEDED** — header updated with "Superseded by v0.3" note. Retained for history. |
| `CDO-Struck-Down-Full-Brief-v0.3.md` | **CURRENT** — APPROVED WITH REVISIONS, 6 corrections applied, ready for production handoff |
| `CDO-Struck-Down-Full-Brief-v0.1.md` | SUPERSEDED — retained for history |
| `BRAND\Reports\CEO-ACTION-REQUIRED-2026-06-06.md` | SUPERSEDED — replaced by this checklist |
| `BRAND\Reports\hyperframes-doctor-2026-06-06.log` | KEPT — production environment ready confirmation |

---

## Block 6 — REMAINING CEO ACTIONS (POST-APPROVAL)

| # | Action | When | Status |
|---|--------|------|--------|
| 1 | Execute Figma Foundation Setup (60–90 min, `BRAND\Figma-Setup\CEO-Playbook.md`) | Before Priority A production | PENDING — CEO session required |
| 2 | Review 3-concept test prompt pack | When CDO delivers | PENDING — CDO delivers next |
| 3 | Commission author photo session (separate approval) | Before A13-A15 production | BLOCKED — pending separate approval |
| 4 | Review BA Tailored DRAFT resume | When convenient | PENDING — earlier item |
| 5 | Decide on superseded `01-Job-Search-PM.md` file | When convenient | PENDING — earlier item |
| 6 | BA Carousel slide 1 swap in VistaCreate (5–10 min) | When convenient | PENDING — earlier item |

---

## Generation Budget Tracking

| Item | Planned | Consumed | Remaining |
|------|---------|----------|-----------|
| Concept test generations (Phase 0) | 6-8 | 0 | 6-8 |
| Priority A production (Phase 2) | 8-9 | 0 | 8-9 |
| **Total Priority A budget (Phase 0 + 2)** | **14-17** | **0** | **14-17** |
| Priority B (Phase 4) | 11-13 | 0 | 11-13 (not started; CEO approval required) |
| **Grand total all phases (A + B)** | **25-30** | **0** | **25-30** |

**Vendor allocation (CDO V3.1 budget):**
- Leonardo.ai: 5 of remaining 134 tokens
- DALL-E (ChatGPT): 9 of remaining 24/10-window (10/24h reset)
- Midjourney: 0 (not subscribed)
- **Total Phase 0 + 2 budget = 14 generations across 3 vendors**

---

**Last updated:** 2026-06-06
**Owner:** CEO (Titus Banks)
**Source of truth:** `BOOK-PROJECTS\Struck Down but Not Destroyed\CDO-Struck-Down-Full-Brief-v0.3.md`
