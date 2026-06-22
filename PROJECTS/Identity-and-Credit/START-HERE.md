# START HERE — Identity + Credit Workstream

**This is your entry point.** Master plan is in `PLAN.md` (read it when you have time). This file is just the first action.

---

## Step 1 — Pull Your Free Credit Reports

The user (Titus Banks) pulls these themselves. OpenCode cannot do this on your behalf — the site requires identity verification with your SSN, DOB, and answers to knowledge-based questions.

### Where to Go

**The only federally authorized free source:** `https://www.AnnualCreditReport.com`

> Important: Do NOT use "FreeCreditReport.com" (a different site, despite the name) or any site that asks for a credit card. `AnnualCreditReport.com` is free, federally authorized, and requires no payment.

### What to Request

- **Equifax** — full report
- **Experian** — full report
- **TransUnion** — full report

You are entitled to **1 free report per bureau per week** under federal law (not just 1 per year — that's a common misunderstanding). For this workstream, request all 3 now.

### State-Specific Free Reports

Several US states entitle you to additional free reports beyond the federal minimum. The user is in **Washington** (Seattle) and has strong **Texas** (Dallas) ties. The relevant states are:

- **WA**: 1 free report per bureau per year from each bureau directly (in addition to AnnualCreditReport.com)
- **TX**: 1 free report per bureau per year from each bureau directly

So you may be entitled to up to **2 free Equifax + 2 free Experian + 2 free TransUnion reports per year** — 6 free per year, plus 12 per year from AnnualCreditReport.com. Total potentially 18 free per year.

### How to Verify Your Identity

AnnualCreditReport.com uses **knowledge-based authentication** — questions about your credit history that only you should know (e.g. "Which of these addresses have you lived at?", "Which of these cars have you financed?"). This is the standard way to verify.

If you fail the KBA questions (which can happen if fraud has already happened), the site allows you to mail in a request form with a copy of your ID. We can draft that form if needed.

### What to Do Once You Have the Reports

You have options:

**Option A — Self-audit (private, fastest).** Review each report yourself. Use the dispute templates in `_templates/` to file disputes directly. Use the master dispute queue in `_trackers/DISPUTES.csv` (the headers are pre-staged; you fill in the rows). OpenCode stays out of the PII entirely.

**Option B — Audit with OpenCode (slower, more support).** Open the report PDFs. Summarize in chat using redacted references (e.g. "Account 1: late payment 03/2024, disputed" instead of "Account 1: Chase Sapphire Visa ending 1234"). OpenCode helps identify which items to dispute, drafts the letter templates, and tracks the queue. PII stays in chat context only, never on disk.

**Option C — Hybrid.** You do the heavy audit. You flag items you want help with. OpenCode drafts the letter templates and tracks the queue. PII stays redacted unless you choose to share specifics for a particular item.

**Pick A, B, or C when you have the reports.**

---

## Step 2 — Build the Disposable Contact Kit (Optional, but Recommended)

Before any automated work begins, set up the consumable contact channels that BOTH workstreams will use. The Identity-Eraser needs them for opt-out verifications. The Credit-Repair needs them for creditor follow-ups.

### Disposable Email

- **Option 1 (free, less reliable):** Use a 10-minute-mail service. Sessions expire. Fine for a single afternoon of opt-outs.
- **Option 2 (free, more reliable):** Create a new Gmail or ProtonMail account specifically for this workstream. Forward to your real email if you want. Disable after the workstream completes.
- **Option 3 (paid, most reliable):** SimpleLogin or AnonAddy alias ($0-30/year). Each alias forwards to your real email, can be disabled per-alias.

**Recommendation:** Option 2 (new Gmail or ProtonMail account). Cost $0. Reliable. You can disable after.

### Google Voice Number (Free)

- Go to `voice.google.com`
- Sign in with your Google account
- Pick a number (any US area code)
- Use it ONLY for this workstream's verifications
- Set voicemail off, transcribed only
- Discard after the workstream completes

**Why:** Some creditors, debt collectors, and data brokers use phone verification. You do not want to give your real phone to debt collectors. Google Voice gives you a free disposable number.

### Session Alias Scheme

Decide on aliases you'll use in this project folder (NOT in chat — in saved files):

| Real PII | Alias |
|----------|-------|
| Titus Banks | T.B. (or T.S. for "Titus Sangare") |
| Seattle address | [redacted-A1] |
| Dallas/Fort Worth address | [redacted-A2] |
| Past address | [redacted-A3] |
| Personal cell | [redacted-P1] |
| Personal email | [redacted-E1] |
| Work email | [redacted-E2] |
| SSN | [redacted-S1] (last 4 only) |
| DOB | [redacted-D1] |

Files in this project folder use the aliases. Real PII lives in your head, in chat context, and in the credit report PDFs you keep in a private location outside this project.

---

## Step 3 — Tell OpenCode You're Ready

Reply with one of:

- "I have the reports. I want Option A / B / C."
- "I haven't pulled them yet. I need to set aside time."
- "Hold the workstream. I have something more urgent."
- "Skip the credit pull and start with the identity-eraser only."
- "I want a different scope. [describe]"

---

## What's Set Up So Far

| Asset | Path | Status |
|-------|------|--------|
| Master plan | `PROJECTS/Identity-and-Credit/PLAN.md` | Written |
| This file | `PROJECTS/Identity-and-Credit/START-HERE.md` | Written |
| Tracker folder | `PROJECTS/Identity-and-Credit/_trackers/` | Empty stubs ready |
| Template folder | `PROJECTS/Identity-and-Credit/_templates/` | Empty stubs ready |
| Log folder | `PROJECTS/Identity-and-Credit/_logs/` | Empty stubs ready |
| Original Identity-Eraser plan | `PROJECTS/Identity-Eraser/PLAN.md` | Retained for reference |
| PROJECT-RADAR | `PROJECT-RADAR.md` | Will be updated after this file |

---

## What Stays Locked Until You Move

- **No PII requested.** OpenCode has not asked for your SSN, DOB, addresses, phone, or email.
- **No browser automation.** Nothing is touched.
- **No execution.** No opt-outs filed. No disputes filed. No letters sent.
- **$0 spend.** Nothing authorized.
- **Struck Down parked controls still held.** Different workstream. Same discipline.

The system is parked. The workstream is ready. You drive.

---

**Last updated:** 2026-06-06
**Next action:** CEO pulls credit reports via AnnualCreditReport.com, then replies to OpenCode.
