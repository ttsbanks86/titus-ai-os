# Fraud Response Log

**This is a chronological log of fraud response actions.** Use this IN ADDITION to `_trackers/DISPUTES.csv` when fraud is suspected. Fraud response involves more than just credit disputes — it includes police reports, FTC reports, fraud alerts, freezes, and tracking the closure of fraudulent accounts.

---

## How to Use

Each significant action gets an entry. Use the format below. Save a copy of every document referenced (in your encrypted personal location, not in this project folder).

```
[YYYY-MM-DD HH:MM] [Action] [Outcome]
```

---

## Initial Discovery

**Date of discovery:** [Date]
**How discovered:** [e.g. "Pulled free credit report from Equifax. Noticed Chase account ending 1234 that I did not open."]

---

## Phase 1 — Immediate Actions (Within 24 Hours)

### Credit Freeze Placed

| Bureau | Date Placed | Confirmation # | PIN Location |
|--------|-------------|----------------|--------------|
| Equifax | [Date] | [Number] | [Encrypted location] |
| Experian | [Date] | [Number] | [Encrypted location] |
| TransUnion | [Date] | [Number] | [Encrypted location] |

### Police Report Filed

- **Agency:** [Police department or sheriff's office]
- **Date filed:** [Date]
- **Report #:** [Number]
- **Officer name:** [Name]
- **Location of report copy:** [Encrypted location]

### FTC Identity Theft Report Filed

- **Filed at:** `https://www.identitytheft.gov/`
- **Date filed:** [Date]
- **FTC report #:** [Number]
- **Location of report PDF:** [Encrypted location]

### Fraud Alert Placed

- **Bureau:** [Equifax, Experian, or TransUnion]
- **Type:** [90-day initial / 7-year extended]
- **Date placed:** [Date]
- **Confirmation #:** [Number]

### Other Immediate Actions

- [ ] IRS Form 14039 filed (if tax-related)
- [ ] SSN statement checked at SSA (earnings verification)
- [ ] Compromised real bank/credit accounts closed and replaced
- [ ] Passwords updated and 2FA enabled on all critical accounts
- [ ] Mail forwarded to a secure location (if mailbox compromised)

---

## Phase 2 — Dispute and Contact (Within 7 Days)

### Fraudulent Accounts Disputed with Bureaus

| Account | Bureau | Date Disputed | Dispute # | Status | Date Resolved |
|---------|--------|---------------|-----------|--------|---------------|
| [Account name] last 4 [XXXX] | Equifax | [Date] | [Number] | [Pending/Removed/Verified] | [Date] |
| [Account name] last 4 [XXXX] | Experian | [Date] | [Number] | [Pending/Removed/Verified] | [Date] |
| [Account name] last 4 [XXXX] | TransUnion | [Date] | [Number] | [Pending/Removed/Verified] | [Date] |

### Fraudulent Creditors Contacted

| Creditor | Date Called | Rep Name | Case # | Status | Date Resolved |
|----------|-------------|----------|--------|--------|---------------|
| [Creditor] | [Date] | [Name] | [Number] | [Open/Closed as Fraud/Other] | [Date] |
| [Creditor] | [Date] | [Name] | [Number] | [Open/Closed as Fraud/Other] | [Date] |

### Unauthorized Inquiries Disputed

| Inquiring Party | Date of Inquiry | Bureau | Date Disputed | Status | Date Resolved |
|------------------|-----------------|--------|---------------|--------|---------------|
| [Party] | [Date] | Equifax | [Date] | [Pending/Removed] | [Date] |
| [Party] | [Date] | Experian | [Date] | [Pending/Removed] | [Date] |
| [Party] | [Date] | TransUnion | [Date] | [Pending/Removed] | [Date] |

---

## Phase 3 — Follow-Up and Monitoring (Ongoing)

### 30-Day Check

- **Date:** [Date]
- **Equifax pull:** [Result: N items removed, N still present]
- **Experian pull:** [Result: N items removed, N still present]
- **TransUnion pull:** [Result: N items removed, N still present]
- **New fraudulent activity detected:** [Yes / No — if yes, list]
- **Action taken:** [Re-dispute / CFPB complaint / etc.]

### 60-Day Check

- **Date:** [Date]
- **Equifax pull:** [Result]
- **Experian pull:** [Result]
- **TransUnion pull:** [Result]
- **New fraudulent activity detected:** [Yes / No]
- **Action taken:** [ ]

### 90-Day Check

- **Date:** [Date]
- **Equifax pull:** [Result]
- **Experian pull:** [Result]
- **TransUnion pull:** [Result]
- **New fraudulent activity detected:** [Yes / No]
- **Action taken:** [ ]
- **Workstream status:** [Closed / Continuing]

### Quarterly Checks (After 90 Days)

| Quarter | Date | Result | New Activity | Action |
|---------|------|--------|--------------|--------|
| Q[X] | [Date] | [Summary] | [Yes/No] | [ ] |
| Q[X] | [Date] | [Summary] | [Yes/No] | [ ] |

---

## Identity-Eraser Acceleration (Optional)

If fraud indicates PII is exposed, accelerate the identity-eraser workstream.

- **Date accelerated:** [Date]
- **Disposable contact kit created:** [Yes / No]
- **Phase 1 (people search) completed:** [Date]
- **Phase 2 (background check + data broker registries) completed:** [Date]
- **Phase 3 (phone, address, search engine, social) completed:** [Date]

---

## Document Inventory

| Document | Date Created | Location |
|----------|--------------|----------|
| Police report | [Date] | [Encrypted location] |
| FTC Identity Theft Report | [Date] | [Encrypted location] |
| Initial credit reports (all 3) | [Date] | [Encrypted location] |
| All dispute letters | [Dates] | [Encrypted location] |
| All bureau responses | [Dates] | [Encrypted location] |
| Creditor fraud case correspondence | [Dates] | [Encrypted location] |
| Updated credit reports (30/60/90 day) | [Dates] | [Encrypted location] |

---

## Status

- **Current status:** [Active / Monitoring / Closed]
- **Last update:** [Date]
- **Last verified:** [Date of last credit report pull]

---

## Change Log

| Date | Change |
|------|--------|
| [Date] | Log created |
| [Date] | [Action taken: Phase 1 complete, etc.] |
| [Date] | [Action taken: 30-day follow-up complete] |
| [Date] | [Action taken: All fraudulent items confirmed removed — workstream closed] |
