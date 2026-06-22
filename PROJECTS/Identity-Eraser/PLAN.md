# Identity Eraser — Comprehensive Plan

**Owner:** CEO (Titus Banks) with CDO/CIO + browser-agent support
**Status:** PLAN DRAFT 2026-06-06 — awaiting CEO sign-off
**Independent of:** Struck Down parked controls (separate workstream, separate budget, separate controls)
**Source skill (current, limited):** `~/.config/opencode/skills/identity-eraser/SKILL.md` (2,927 bytes, 4 brokers only)

---

## Why This Plan Exists

The current `identity-eraser` skill covers 4 brokers: Spokeo, Whitepages, Radaris, BeenVerified. The CEO has authorized a thorough expansion to cover the realistic universe of US data brokers, public records aggregators, marketing data registries, and supporting opt-outs. The new skill is a separate, independent workstream — it is not blocked by the Struck Down parked controls and has its own budget / approval flow.

---

## 1. Scope and Target Inventory

The realistic universe of US personal-data opt-out targets is **~120-150 distinct sites/services**, organized into 10 categories.

### Category 1 — People Search Engines / Public Records (the "scrapers")
The mainstream sites that surface in Google for name + city searches. **~30 sites.**

Already covered (4): Spokeo, Whitepages, Radaris, BeenVerified.
To add (~26): Intelius, MyLife, PeopleFinder, USSearch, TruthFinder, Instant Checkmate, Pipl, ThatsThem, FastPeopleSearch, FastPeopleSearch.app, Nuwber, ClustrMaps, FamilyTreeNow, Addresses.com, AnyWho, 411.com, PeekYou, PeopleLooker, Persopo, PublicRecords.com, PrivateEye, Rehold, SearchPeopleFree, SmartBackgroundChecks, Social Catfish, SpyFly.

### Category 2 — Background Check Services (the "premium" sites)
Subscription-walled, often owned by parent companies (PeopleConnect, etc.). **~18 sites.**

CheckPeople, Checkr, IDTrue, InfoTracer, LocatePeople, NetrOnline, PeopleBackgroundCheck, PeopleByName, PeopleByPhone, PeopleSearch123, PeopleWhiz, PersonLookUp, PublicRecordsNOW, RecordsFinder, SearchSystems, USA People Search, Vericora, Verispy.

### Category 3 — Phone Lookup Services
**~14 sites.**

SpyDialer, USPhoneBook, ThatsThem (also in #1), NumLookup, Zlookup, CallerSmart, CellRevealer, LeadFerret, LeadsPlease, NeighborWho, Ownerly, ReversePhoneLookup.com, SpyFly (also in #1), TextMagic Reverse.

### Category 4 — Address Lookup Services
**~8 sites.**

Homemetry, NeighborWho (also in #3), Addresses.com (also in #1), FamilyTreeNow (also in #1), Ownerly (also in #3), PeopleFinders (also in #1), Rehold (also in #1), Whitepages (also in #1).

### Category 5 — Data Broker Registries (CCPA / GDPR opt-out targets)
The big marketing-data companies that sell consumer profiles. **~14 companies.**

Acxiom, Oracle Data Cloud (formerly Datalogix), Epsilon, LiveRamp, Factual, TowerData, DataLogix, Experian Marketing Services, TransUnion Consumer View, Equifax Consumer Services, Innovis, LexisNexis, Gravy Analytics, VenPath.

### Category 6 — Credit Bureau Opt-Outs (marketing lists)
**4 bureaus + 1 consolidated.**

Equifax, Experian, TransUnion, Innovis, plus Opt-OutPrescreen.com (the consolidated 5-year opt-out for credit/insurance offers).

### Category 7 — Social Media Hardening
**4 platforms.**

Facebook (off-Facebook activity, search visibility, profile discoverability), Instagram (account visibility, search history), LinkedIn (public profile visibility, search appearance, recruiter visibility), Twitter/X (discoverability, photo tagging).

### Category 8 — Search Engine Suppression
**2-3 services.**

Google "Results about you" tool, Bing Content Removal form, optionally DuckDuckGo (no public form; relies on upstream source removal).

### Category 9 — Public Records Aggregators
**~6 sites.**

Ancestry.com, MyHeritage, FindAGrave (if relevant), FamilySearch, Archives.com, Geneanet.

### Category 10 — Long Tail (niche / smaller sites)
**~30-50 sites.** These are the deep tail that shows up in name searches but aren't critical to start with. Examples: 411.info, AddressesPlus, AdvancedBackgroundChecks, AnyWho, Archives.com, BatchLeads, Bumper, Carphones, CellRegistry, CheckPeople, Classmates, CoFinder, ConfidentialPhoneLookup, CorpChecks, Cubib, DataVeria, Dun & Bradstreet, EmailFinder, FreeBackgroundChecks, FreePeopleSearch, GoLookUp, GreatPeopleSearch, Hagee, HometownLocator, HUD Public Housing Records, InfoBel, JailBase, JigSaw, LinkedIn Sales Navigator (opt-out of "viewed by"), LookupAnyone, LookupUK, MarketingProfs, MelissaData, NextDoor, OpenCorporates, Persopo, PhoneBook, PhoneLookup, PublicEmailRecords, QuickPeopleTrace, SalesSpider, SearchBug, Social-Searcher, SpyTox, TLO, TraceAnyone, TrueCaller, USRecords, VehicleRecords, VoterRecords, YellowPages, Yelp, Zabasearch, ZoomInfo.

### Category 11 — Paid Service Comparison (optional, separate)
**3-5 services.** This is research, not opt-out execution. Compare DIY cost (time) vs paid services.

DeleteMe ($129/yr per person), Incogni ($89.88/yr per person), Optery ($29.99-$129.99/yr), Kanary ($99-$149/yr), PrivacyDuck ($499 one-time + $99/yr monitoring).

---

## 2. Total Scope

| Category | Sites | Priority |
|----------|------:|----------|
| 1. People search engines | 30 | **HIGH** — most visible in Google results |
| 2. Background check services | 18 | **HIGH** — used by recruiters, landlords, dates |
| 3. Phone lookup | 14 | **MEDIUM** — niche but leaks phone number |
| 4. Address lookup | 8 | **MEDIUM** — niche but leaks address |
| 5. Data broker registries | 14 | **HIGH** — sold to advertisers, insurers, data buyers |
| 6. Credit bureau opt-outs | 5 | **MEDIUM** — stops preapproved credit offers |
| 7. Social media hardening | 4 | **MEDIUM** — limits platform-level exposure |
| 8. Search engine suppression | 3 | **MEDIUM** — pushes results down over time |
| 9. Public records aggregators | 6 | **LOW** — genealogy, voter records |
| 10. Long tail | 30-50 | **LOW** — diminishing returns |
| 11. Paid service comparison | 5 | **RESEARCH** — not opt-out execution |
| **TOTAL (categories 1-10)** | **~120-150** | |

---

## 3. Phased Execution Plan

The "thorough job" is staged so the CEO sees the highest-leverage removals first. Each phase ends with a status report and CEO checkpoint before moving on.

### Phase 1 — Core People Search Engines (Category 1)
**30 sites, expected time 2-3 hours of automation.** Targets the most visible in Google results. Includes the 4 already in the skill.

### Phase 2 — Background Check Services (Category 2)
**18 sites, expected time 1.5-2 hours.** Many share parent companies (PeopleConnect, etc.) so a single CCPA request can cover 3-4 sites.

### Phase 3 — Phone + Address Lookup (Categories 3-4)
**22 sites, expected time 1-1.5 hours.** Mostly fast opt-outs.

### Phase 4 — Data Broker Registries (Category 5)
**14 companies, expected time 2-3 hours.** These are the slowest because most require written CCPA/GDPR request letters (email or web form), with 30-45 day response windows per law.

### Phase 5 — Credit Bureau Opt-Outs (Category 6)
**5 opt-outs, expected time 30-60 min total.** Fast: phone or web form. Opt-OutPrescreen is the single most impactful (5-year block on preapproved credit offers).

### Phase 6 — Social Media Hardening (Category 7)
**4 platforms, expected time 30-60 min total.** Settings changes, not opt-outs. The CEO does these directly in their own social media accounts (the skill can guide step-by-step).

### Phase 7 — Search Engine Suppression (Category 8)
**2-3 services, expected time 30-60 min total.** Google "Results about you" requires Google's verification. Bing has a form. This is async — Google's review can take weeks.

### Phase 8 — Public Records + Long Tail (Categories 9-10)
**36-56 sites, expected time 2-4 hours.** The diminishing-returns phase. Do this if the CEO wants comprehensive coverage; skip if diminishing returns feel wasteful.

### Phase 9 (optional) — Paid Service Comparison Research (Category 11)
**Research, not execution. Expected time 1-2 hours of research.** Compare DIY time cost vs paid services. If the CEO decides a paid service is worth it, that's a separate decision.

### Phase 10 (optional) — Periodic Re-Scan
**Ongoing, 30-60 min per quarter.** After all opt-outs are submitted, the data often re-appears (different sites re-scrape, new sites go live, etc.). Quarterly re-scan catches re-appearances and re-submits opt-outs.

---

## 4. Workflow (Session Memory Only — No PII to Disk)

The CEO's PII is the most sensitive data this workstream handles. The plan follows the existing skill's safety rules, with refinements.

### Inputs (provided by CEO at session start, held in active context only)

The CEO provides the following ONCE at the start of a session:
1. **Full legal name** (variants: nickname, married/maiden, middle initial)
2. **Age or birth year** (for exact-match disambiguation)
3. **Current city + state**
4. **Past cities + states** (where the CEO has lived)
5. **Email(s) to search** (personal, work — for cross-broker matching)
6. **Phone number(s) to search** (mobile, landline, past)
7. **Disposable email** for opt-out verifications (e.g. a 10-minute-mail address)
8. **Optional:** relatives' names (some brokers list relatives and create a graph)

### Data handling rules

- **No PII is written to disk in this project folder.** Search history, profile URLs, opt-out confirmations, and email contents are kept in active session memory only.
- **Audit trail (no PII):** The OPT-OUT-TRACKER.csv logs only: broker name, category, opt-out URL, date submitted, status (pending / confirmed / failed), confirmation reference (if any), and notes. NO name, address, email, phone, or DOB is written to disk.
- **Email contents:** Disposable email contents are read in-session for verification links. The disposable email account is created fresh per session and discarded at session end.
- **Browser automation:** All browsing happens via the browser agent. The CEO does not need to manually visit any site (except for social media hardening, which is the CEO's own account).

### Per-broker execution pattern

For each broker in the active phase:

1. Search the broker's site for the CEO's name + city/state.
2. Identify the correct matching profile (often multiple "John Smith" results — disambiguate by age, relatives, past cities).
3. Capture the profile URL (kept in session memory, not written to disk).
4. Navigate to the opt-out page.
5. Submit the opt-out with the disposable email.
6. Capture the confirmation message / reference number (in session memory).
7. Log the result in OPT-OUT-TRACKER.csv (no PII, only broker name + status).
8. Prompt the CEO if the broker requires a verification step (email link, phone code, photo ID).

### Safety gating

- **Before clicking Submit on any opt-out:** the browser agent presents a summary of what will be submitted, and the CEO confirms. This is per the existing skill's safety rule.
- **Before any action that requires the CEO's real account** (social media hardening), the skill presents step-by-step instructions and the CEO does it themselves.
- **Before any spend** (paid services research, mailing physical opt-out letters, hiring a service): explicit CEO authorization.
- **No PII to disk, ever.** If the session is interrupted, in-memory PII is lost. The CEO re-provides it at the next session start.

---

## 5. Workstream Controls (Independent of Struck Down)

This is a separate workstream. It has its own controls, not the Struck Down parked controls.

| Control | State | Notes |
|---------|-------|-------|
| Browser automation (Playwright) | **ALLOWED** for this workstream | The CEO lifted the parked "no browser" control for identity-eraser. |
| AI image generation | **NOT RELEVANT** | This workstream doesn't generate images. |
| Spend | **$0 BY DEFAULT** | Paid services are an optional Phase 9 research item. No spend without CEO sign-off. |
| PII to disk | **PROHIBITED** | Session memory only. Audit trail has broker names + status, no PII. |
| External logs | **PROHIBITED** | No PII to console, log files, or external services. |
| CEO checkpoints | **PER BROKER SAFETY GATE** | Confirm before submit. Confirm on verification steps. |
| Phase gates | **PER PHASE** | CEO reviews phase results before next phase starts. |
| Audit trail | **OPT-OUT-TRACKER.csv + EXECUTION-LOG.md** | Broker-level only. No PII. |

---

## 6. Deliverables (in this project folder)

| File | Purpose | PII? |
|------|---------|------|
| `PLAN.md` (this file) | Comprehensive plan, scope, phases, controls | No |
| `BROKER-LIST.md` | The master list of ~120-150 brokers by category with opt-out URL | No |
| `OPT-OUT-TRACKER.csv` | Running tracker: broker, category, URL, date, status, reference | No |
| `EXECUTION-LOG.md` | Chronological log of phase starts/ends, completions, issues | No |
| `RESULTS.md` | End-of-workstream summary: what was removed, what failed, what to re-try, what to monitor | No |
| `PAID-SERVICES-COMPARISON.md` (optional, Phase 9) | DIY cost vs DeleteMe / Incogni / Optery / Kanary / PrivacyDuck | No |

**Refined SKILL.md (system location, after CEO approval):** `~/.config/opencode/skills/identity-eraser/SKILL.md` — expanded from 2,927 bytes / 4 brokers to ~25-35 KB / 120-150 brokers, organized by category, with phase markers.

---

## 7. Timeline Estimate

| Phase | Time (CDO + browser agent) | CEO time |
|-------|---------------------------:|---------:|
| Phase 1 (Category 1) | 2-3 hours automation | 30-45 min verifications + 2-3 CEO checkpoints |
| Phase 2 (Category 2) | 1.5-2 hours | 30 min verifications |
| Phase 3 (Categories 3-4) | 1-1.5 hours | 20-30 min verifications |
| Phase 4 (Category 5) | 2-3 hours | 1-2 hours writing CCPA request letters |
| Phase 5 (Category 6) | 30-60 min | 15-30 min (CEO makes phone calls or submits forms) |
| Phase 6 (Category 7) | 30-60 min (skill guides) | 30-60 min (CEO does their own accounts) |
| Phase 7 (Category 8) | 30-60 min (submission) | Async (Google review can take 2-4 weeks) |
| Phase 8 (Categories 9-10) | 2-4 hours | 30-60 min verifications |
| Phase 9 (optional) | 1-2 hours research | 1 hour review |
| **TOTAL (Phases 1-8, "thorough job")** | **~10-15 hours automation** | **~3-5 hours CEO time** |
| Phase 10 (ongoing) | 30-60 min per quarter | 15-30 min per quarter |

The "thorough job" is ~13-20 hours of work total, spread over 1-2 weeks (so the CEO can do verifications as they come in). Phases 1-3 alone (the highest-leverage) is ~4-5 hours and removes the most visible Google results.

---

## 8. Cost Analysis (Default: $0 Spend)

| Option | Cost | Notes |
|--------|-----:|-------|
| **DIY (Phases 1-8)** | **$0** | Time cost only. CEO time + CDO/agent time. |
| **DIY + disposable emails** | **$0-10** | Some disposable email services charge a few dollars for persistent inboxes. |
| **DIY + physical mail (if a broker requires it)** | **$5-15** | Postage for 1-2 letters. |
| **Paid service (Phase 9 research)** | **$89-499/yr** | DeleteMe, Incogni, Optery, Kanary, PrivacyDuck. |
| **Notary / photo ID (if a broker requires ID verification)** | **$0-25** | Most accept a redacted utility bill or passport scan. |

The default plan is **$0 spend**. Paid services are an optional Phase 9 comparison; if the CEO decides to subscribe to one, that's a separate decision and spend authorization.

---

## 9. Risks and Open Questions

### Risks

1. **Re-scraping.** Even after successful opt-out, some brokers re-scrape public records and re-list the CEO within 6-12 months. The Phase 10 re-scan mitigates this.
2. **CCPA request denials.** Some data brokers honor CCPA only for California residents. For other states, they may require different legal grounds (GDPR for EU, state-specific privacy laws). The skill will draft the strongest available request per state.
3. **Identity verification friction.** Some brokers require photo ID, utility bill, or phone verification. The skill flags these and asks the CEO to provide what's needed.
4. **New sites going live.** New people-search sites launch every month. A "thorough job" today is not thorough in 12 months. The Phase 10 re-scan + ongoing maintenance is the long-term answer.
5. **The skill itself is sensitive.** An expanded identity-eraser skill contains a detailed playbook of every US data broker and how to remove yourself. It's defensive (used by the CEO for their own data), but it should be kept private to the CEO's OpenCode instance.

### Open questions for CEO sign-off

1. **Scope:** Run all 8 categories (1-8, ~100 sites) for "thorough" or stop at Phase 3 (highest-leverage ~52 sites)?
2. **Phase 4 (CCPA request letters):** OK to draft and send letters on the CEO's behalf? (Most data brokers accept email; some need certified mail.)
3. **Phase 6 (social media hardening):** OK for the skill to give the CEO step-by-step instructions, or does the CEO prefer to harden accounts entirely on their own with no skill involvement?
4. **Phase 9 (paid service research):** Skip for now, or research in parallel with Phases 1-8?
5. **Phase 10 (quarterly re-scan):** Add to the project as an ongoing maintenance task?
6. **Disposable email service:** Use a free 10-minute-mail service (less reliable, sessions expire) or set up a dedicated 10-minute-mail alternative (small cost, more reliable)?
7. **PII in session memory:** Confirm OK for the CEO to provide PII in chat (active context only, no disk writes) for the duration of the workstream sessions.

---

## 10. CEO Sign-Off Required

Before the skill is refined and any execution begins, the CEO confirms:

- [ ] **Scope:** ___________ (Phase 1-3 only / Phase 1-8 / Phase 1-8 + 9 / Phase 1-10)
- [ ] **CCPA letters:** ___________ (CDO drafts and sends on CEO's behalf / CEO signs and sends / Skip Phase 4)
- [ ] **Social media hardening:** ___________ (Skill provides step-by-step / CEO does entirely alone / Skip Phase 6)
- [ ] **Paid service research:** ___________ (Skip / Run in parallel / Run after Phase 8)
- [ ] **Quarterly re-scan:** ___________ (Yes / No)
- [ ] **Disposable email:** ___________ (Free 10-min-mail / Dedicated service / CEO's choice per session)
- [ ] **PII in session memory:** ___________ (Confirmed OK / Use redacted aliases / Other)

**Once these are signed off, the CDO will:**

1. Refine `~/.config/opencode/skills/identity-eraser/SKILL.md` with the comprehensive broker list organized by category.
2. Create the `BROKER-LIST.md` master file in this project folder.
3. Initialize `OPT-OUT-TRACKER.csv` and `EXECUTION-LOG.md`.
4. Begin Phase 1 with the CEO's first session (PII input → first 5-10 opt-outs).

**Until sign-off is received, the system is in observation mode. No PII requested. No execution. No skill refinement.**

---

**Last updated:** 2026-06-06
**Owner:** CDO/CIO with CEO sign-off
**Next action:** CEO reviews and signs off on the 7 items in section 10. CDO refines skill and starts Phase 1 only after sign-off.
