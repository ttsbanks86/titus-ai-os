# Identity + Credit Workstream — Master Plan

**Owner:** CEO (Titus Banks) with CDO/CIO + browser-agent support
**Status:** STRUCTURE DRAFT 2026-06-06 — awaiting CEO first step
**Independent of:** Struck Down parked controls (separate workstream)
**Source documents:**
- `PROJECTS/Identity-Eraser/PLAN.md` (the original identity-eraser plan, retained for broker-level detail)
- New credit-repair layer (this document)

---

## 1. Why This Is One Workstream

The user has authorized a back-to-back, integrated workstream. The reason they integrate:

| Domain | Question | Tool |
|--------|----------|------|
| **Identity eraser** | Where is my data being sold? | Data broker opt-outs (~120-150 brokers) |
| **Credit repair** | What does my data say about me financially? | Credit report disputes + creditor negotiation |
| **The connection** | Both work on the same PII: name, addresses, phone numbers, SSN fragments | The credit report is the master map of where the user's PII lives. The data brokers are downstream copies of that map. |

**The credit report tells the identity-eraser where to look.** If the credit report shows addresses X, Y, and Z, those are exactly the addresses the identity-eraser needs to scrub from data brokers. If a debt collector is on the credit report, they have the user's PII too — removing from the data broker AND disputing on the credit report are both required.

**The identity-eraser tells the credit-repair where fraud happened.** If the credit audit reveals an account the user did not open, that's identity theft. The identity-eraser then becomes the legal/regulatory response (FTC report, police report, fraud affidavit, credit freeze, fraud alerts).

Running them together is faster, cheaper, and more thorough than running them separately.

---

## 2. The 7-Phase Integrated Workflow

The merged workstream runs as 7 phases. Each phase has a CEO checkpoint before the next phase starts.

### Phase 0 — Disposable Contact Kit (1 hour, free)
Set up the consumable contact channels that BOTH workstreams will use.

- Create a dedicated disposable email for this workstream (10-minute-mail alternative or ProtonMail alias). Used for all opt-out verifications and dispute follow-ups.
- Set up a free Google Voice number for any phone verifications. Voicemail off, transcribed only.
- Set up a separate, secure folder on the CEO's local machine for storing their own credit reports (NOT in this project folder — privacy). The user controls access.
- Decide on a session PII alias scheme: e.g. "T.S." for the user, addresses as "[redacted-A1]", "[redacted-A2]" in any saved file. Full PII stays in active chat context only.

### Phase 1 — Pull and Audit Credit Reports (1-2 weeks waiting, free)
**The first action. The user pulls the credit reports themselves.**

- Pull all 3 free reports via `AnnualCreditReport.com` (the only federally authorized free source). Note: not "FreeCreditReport.com" or any other site — AnnualCreditReport.com is the only legitimate one.
- Soft-pull current scores via Credit Karma (VantageScore) and the lender that provides FICO if available.
- For each of the 3 reports, audit every item:
  - **Account status** (open, closed, charged-off, collection, paid)
  - **Balance** vs what the user actually owes
  - **Payment history** (any 30/60/90-day lates the user did not make?)
  - **Personal info** (current and past addresses, employer, phone numbers)
  - **Inquiries** (any hard inquiries the user did not authorize?)
  - **Public records** (bankruptcies, judgments, tax liens)
- Mark every item: accurate / inaccurate / fraud / outdated / unverifiable.
- Build the dispute queue and the identity-eraser search-key inventory.
- **Fraud check:** Any account the user did not open = identity theft. If fraud is found, the workstream jumps to a Fraud Sub-Protocol (see section 4).

### Phase 2 — Credit Disputes (weeks 2-8, free under FCRA)
- File disputes with each bureau online (Equifax, Experian, TransUnion).
- Each bureau has 30 days to investigate under FCRA.
- Re-dispute items that come back "verified" but the user has evidence they are wrong.
- Escalate to CFPB complaints if bureaus fail to investigate properly.
- All disputes tracked in `_trackers/DISPUTES.csv`.

### Phase 3 — Identity Eraser Phase 1: People Search Engines (weeks 2-5, free)
**In parallel with credit disputes.**

- Use the addresses, phone numbers, and aliases identified in the credit audit as the master search keys.
- Hit the highest-leverage people-search engines (Spokeo, Whitepages, Radaris, BeenVerified, Intelius, MyLife, PeopleFinder, USSearch, TruthFinder, Instant Checkmate, Pipl, ThatsThem, FastPeopleSearch, Nuwber, ClustrMaps, FamilyTreeNow, Addresses.com, AnyWho, 411.com, PeekYou, PeopleLooker, Persopo, PublicRecords.com, PrivateEye, Rehold, SearchPeopleFree, SmartBackgroundChecks, Social Catfish, SpyFly — 30 sites).
- All opt-outs tracked in `_trackers/OPT-OUT-TRACKER.csv`.

### Phase 4 — Identity Eraser Phase 2: Background Check Services + Data Broker Registries (weeks 4-10, free)
- Background check services (~18 sites): CheckPeople, IDTrue, InfoTracer, etc.
- Data broker registries (~14 companies, CCPA opt-out): Acxiom, Oracle Data Cloud, Epsilon, LiveRamp, LexisNexis, etc.
- Many of these share parent companies (PeopleConnect, etc.) so a single CCPA request can cover 3-4 sites.
- The 30-45 day CCPA response window overlaps with the credit dispute window — this is the "back-to-back" the user described.

### Phase 5 — Credit Repair Negotiation Layer (weeks 4-12, free)
- Goodwill letters for late payments the user did make (asking creditor to remove as a courtesy).
- Pay-for-delete agreements for collections (offer to pay in exchange for deletion).
- Debt validation requests under FDCPA for any collection account (force the collector to prove they own the debt).
- Settlement offers for charged-off accounts (pay less than full balance, get written agreement first).
- All negotiations tracked in `_trackers/GOODWILL-LETTERS.csv` and `_trackers/PAY-FOR-DELETE.csv` and `_trackers/DEBT-VALIDATION.csv`.

### Phase 6 — Identity Eraser Phase 3: Phone, Address, Search Engine Suppression, Social Hardening (weeks 8-16, free)
- Phone lookup services (~14 sites).
- Address lookup services (~8 sites).
- Google "Results about you" suppression.
- Bing content removal.
- Social media privacy hardening (Facebook, Instagram, LinkedIn, Twitter/X).
- Cross-reference with credit report: when an old address is removed from a broker, the next credit report should also stop showing that address.

### Phase 7 — Credit Building + Ongoing Monitoring (months 2-12, then ongoing)
- Pay all bills on time (35% of FICO).
- Keep credit utilization under 10% on revolving accounts (30%).
- Don't close old credit cards (15% length of history).
- Diversify credit mix if it makes sense (10%).
- Limit new applications (10% new credit).
- Pull all 3 reports quarterly (you get 1 free per bureau per week — that's 12 free per year per bureau, not 1).
- Watch for re-appearances of removed items.
- For identity: re-scan data brokers quarterly for new sites or re-appearances.

---

## 3. Cross-Reference Map (How the Two Workstreams Connect)

| Credit audit finding | Identity-eraser action |
|----------------------|------------------------|
| Old address on credit report (e.g. 2018 Seattle apartment) | Search that address on Spokeo, Whitepages, etc. Submit opt-out. |
| Phone number on credit report | Search that number on SpyDialer, USPhoneBook, etc. Submit opt-out. |
| Debt collector listed (e.g. Midland Funding) | Search "Midland Funding" data holdings. Submit CCPA request. |
| Authorized user account the user did not request | If fraud: trigger fraud sub-protocol. If just unwanted: dispute as not the user's. |
| Employer name on credit report (often incorrect) | Note as a credit dispute item. May also need to be removed from data broker listings. |
| Inquiries from companies the user did not apply to | Likely identity theft — trigger fraud sub-protocol. |
| Personal info section showing wrong DOB/SSN | Major red flag for identity theft. Trigger fraud sub-protocol. |
| Bankruptcy or judgment > 7-10 years old | Dispute on credit report. May also need to be removed from public records sites. |

| Identity-eraser finding | Credit-repair action |
|-------------------------|----------------------|
| Profile on Spokeo with old address | Note: that address will likely appear on credit report. Pre-emptively dispute if not the current address. |
| Profile on BeenVerified with current phone | Note: collectors may use that phone. Set up fraud alert to verify any new credit application. |
| Debt collector listing the user on a people-search site | Cross-check credit report. If collection is on the report, dispute AND request validation. |
| Fraud alert placed after identity-eraser discovery | All three bureaus issue fraud alert. New credit applications require extra verification. |
| Credit freeze placed | All three bureaus lock the credit file. No new accounts can be opened without the user lifting the freeze. |

The two workstreams use the **same disposable contact kit** (Phase 0) and the **same audit log** (`_logs/EXECUTION-LOG.md`).

---

## 4. Fraud Sub-Protocol (If Credit Audit Reveals Identity Theft)

If any of these are found in Phase 1, the workstream jumps to this sub-protocol BEFORE continuing:

1. **File a police report** with local law enforcement (in the CEO's jurisdiction, e.g. Seattle or Dallas).
2. **File an FTC identity theft report** at `IdentityTheft.gov`. Get the FTC Identity Theft Report PDF.
3. **Place a fraud alert** with one of the three bureaus (they are required to notify the other two). Free. 1-year duration. Renewable.
4. **Consider a credit freeze** with all three bureaus. Free. No expiration. Lift temporarily when applying for new credit.
5. **File fraud disputes** with each bureau for every fraudulent account, attaching the FTC report and police report.
6. **Contact each fraudulent creditor directly** with the FTC report and police report, demanding account closure and written confirmation.
7. **Get a new Social Security number** ONLY if SSN was used to commit major fraud and the original is permanently compromised. This is rare and requires an in-person SSA appointment.
8. **Trigger Phase 1 of identity-eraser** with the fraudulent PII profile (addresses the thief used, phone numbers, etc.).
9. **Set up a credit monitoring service** (Credit Karma free, or myFICO $30/month) with real-time alerts.
10. **Document everything** in `_logs/EXECUTION-LOG.md` and `_logs/FRAUD-RESPONSE.md` (new file if triggered).

**If no fraud is found, the sub-protocol is skipped and the workstream proceeds to Phase 2.**

---

## 5. Workstream Controls (Independent of Struck Down)

| Control | State | Notes |
|---------|-------|-------|
| Browser automation (Playwright) | **ALLOWED** for this workstream | Per CEO sign-off on Identity-Eraser, extended to the merged workstream. |
| AI image generation | **NOT RELEVANT** to this workstream | |
| Spend | **$0 BY DEFAULT** | Postage ($0-15) only. Paid services are an optional Phase 9. No spend without CEO authorization. |
| PII to disk | **PROHIBITED** | Session memory only. Files in this project folder use aliases (T.S., redacted-A1, etc.). |
| External logs | **PROHIBITED** | No PII to console, log files, or external services. |
| Disposable contact kit | **REQUIRED** for any automated work. | Set up in Phase 0. |
| CEO checkpoints | **Per phase.** Confirm before next phase starts. | |
| Audit trail | `_logs/EXECUTION-LOG.md` + per-tracker CSVs. **No PII on disk.** | |
| Struck Down parked controls | **STILL HELD** | This workstream does not affect the Struck Down parked state. |

---

## 6. Deliverables (File Map)

```
PROJECTS/Identity-and-Credit/
├── PLAN.md                              (this file — master plan)
├── START-HERE.md                        (entry point — first actions)
├── _trackers/
│   ├── DISPUTES.csv                     (credit dispute queue)
│   ├── GOODWILL-LETTERS.csv             (goodwill letter queue)
│   ├── PAY-FOR-DELETE.csv               (collection negotiation queue)
│   ├── DEBT-VALIDATION.csv              (FDCPA debt validation queue)
│   ├── OPT-OUT-TRACKER.csv              (data broker opt-out queue)
│   ├── FRAUD-RESPONSE.md                (only created if fraud found)
│   └── INQUIRY-AUDIT.csv                 (hard inquiry review)
├── _templates/
│   ├── dispute-letter-general.md
│   ├── dispute-letter-specific.md
│   ├── goodwill-letter.md
│   ├── pay-for-delete-letter.md
│   ├── debt-validation-request.md
│   ├── fraud-affidavit.md
│   ├── ftc-identity-theft-summary.md
│   ├── cfpb-complaint.md
│   ├── cspa-opt-out-letter.md
│   ├── goodwill-letter-template.md
│   └── cease-and-desist-collector.md
├── _logs/
│   └── EXECUTION-LOG.md                 (chronological action log)
└── RESULTS.md                           (created at end of workstream — score deltas, removal counts)
```

**External storage (NOT in this folder):**
- The CEO's actual credit reports (PDFs) go in a private, encrypted location on the CEO's machine. They are not part of this project.
- The CEO's actual identity-eraser session memory (PII) is held in active chat context only.

---

## 7. Cost and Time

| Item | Cost | Time |
|------|-----:|------|
| Annual credit reports (3 bureaus) | **$0** | 7-21 days for processing |
| Soft-pull scores | **$0** (Credit Karma) | Instant |
| Disposable email | **$0-5** | 15 min to set up |
| Google Voice number | **$0** | 10 min to set up |
| Credit dispute filings | **$0** (FCRA right) | 30 days per dispute |
| Certified mail for disputes | **$5-15 per letter** | 1 hour to draft, 5 min to mail |
| Goodwill letters | **$0** + postage | 1-2 hours to draft |
| Pay-for-delete negotiations | **$0** (only pay if accepted) | Varies by collector |
| Data broker opt-outs (DIY) | **$0** | 13-20 hours over 1-2 weeks |
| Identity-eraser (with paid service, optional) | **$30-499** | 0-5 hours CEO time |
| **Total realistic cost (DIY)** | **$0-50** | **15-25 hours CEO time over 3-6 months** |
| **Total realistic cost (DIY + Optery)** | **$30-80** | **5-10 hours CEO time over 3-6 months** |

---

## 8. Sign-Off Questions (Reaffirmed from Individual Workstream Sign-Offs)

Both prior sign-off question sets are now consolidated. Please confirm:

1. **Scope:** Run all 7 phases (full 3-6 month workstream) or stop at Phase 1 (credit audit) and decide based on what's found?

2. **Disposable email service:** Free 10-min-mail (less reliable, sessions expire) or ProtonMail alias / dedicated alternative (more reliable, small cost)?

3. **PII in session memory:** Confirmed OK to provide in chat (active context only, no disk writes) — same rule as Identity-Eraser? Or use redacted aliases (e.g. "T.S., Seattle, ~40, addresses [redacted-A1, A2, A3]")?

4. **Mail or online disputes:** Online dispute forms (faster, less paper trail) or certified mail (slower, stronger paper trail, +$5-15 per letter)?

5. **Credit monitoring:** Free (Credit Karma VantageScore) or paid (myFICO $30/month for FICO + 3-bureau monitoring)?

6. **Paid service backup:** OK to have Optery/Incogni/DeleteMe/PrivacyDuck as a fallback option for hard-to-remove items, or strictly DIY?

7. **Fraud sub-protocol:** Pre-authorize the fraud sub-protocol (file police report, FTC report, fraud alert, credit freeze, dispute fraudulent accounts) if Phase 1 reveals identity theft, or pause and ask before each step?

---

## 9. What I'm Waiting For

The user said: "We're going to start by pulling the credit, then move step-by-step to ensure everything is set up."

The structure is set up. The next action is for the user to:

1. Go to `AnnualCreditReport.com` (the only federally authorized free source)
2. Request all 3 reports (Equifax, Experian, TransUnion)
3. Optionally request free reports for additional states (CA, CO, CT, GA, IL, ME, MD, MA, MN, NJ, NY, NC, OR, PA, RI, TX, VT, VA, WA — if applicable, the user gets even more free reports)
4. Wait 7-21 days for processing
5. Review the reports (no need to share full contents with OpenCode — the user can do their own audit, OR they can summarize in chat for help)
6. Tell OpenCode "I have the reports" or "I'm starting the audit" and we begin Phase 1

**Until the user pulls the reports and provides go-signal, the workstream is in observation mode:**
- No PII requested
- No browser automation
- No execution
- $0 spend

**Struck Down parked controls still held.** 0 AI generations performed. 0 spend authorized. 0 browser automation. Quality above speed.

---

## 10. Change Log

- 2026-06-06 — Plan drafted. Integrated Identity-Eraser (Phases 1-3 from `PROJECTS/Identity-Eraser/PLAN.md`) with new Credit-Repair layer. Cross-reference map added. Fraud sub-protocol added. File structure created. Awaiting CEO first step (credit pull).

---

**Last updated:** 2026-06-06
**Owner:** CDO/CIO with CEO sign-off
**Next action:** CEO pulls credit reports via AnnualCreditReport.com. Or CEO answers the 7 sign-off questions. Or CEO issues a "hold" or a "change of plans."
