# Fraud Response Protocol & Template

**This is a checklist + template for responding to suspected identity theft or fraudulent activity on credit reports.** Triggers are in the master plan — any account you did not open, any hard inquiry you did not authorize, or any incorrect personal information (wrong DOB, wrong SSN) in the personal info section.

---

## Phase 1 — Immediate Actions (Within 24 Hours of Discovery)

### Step 1.1: Freeze Your Credit with All 3 Bureaus

Credit freezes are free, immediate, and prevent anyone (including you) from opening new credit in your name. You must contact all 3 bureaus.

**Equifax freeze:** `https://www.equifax.com/personal/credit-report-services/credit-freeze/`
**Experian freeze:** `https://www.experian.com/freeze/center.html`
**TransUnion freeze:** `https://service.transunion.com/dss/orderStep1_form.page`

Or by phone:
- Equifax: 1-800-685-1111
- Experian: 1-888-397-3742
- TransUnion: 1-888-909-8872

Save your freeze PINs in a secure location. You will need them to lift the freeze when you want to apply for new credit.

### Step 1.2: File a Police Report

Go to your local police department (or sheriff's office) and file a report. Bring:
- Government-issued photo ID
- Proof of address
- Any evidence of fraud (credit report, fraudulent account statements, collection notices, etc.)
- The FTC Identity Theft Report (see Step 1.3)

Get a copy of the police report. Note the **report number** — you will need it for the FTC, the bureaus, and the creditors.

### Step 1.3: File an FTC Identity Theft Report

Go to `https://www.identitytheft.gov/` and click "Get Started." Answer the questions about what happened. The site will generate:
- An **Identity Theft Report** (official FTC document)
- A **Recovery Plan** with personalized steps
- Pre-filled letters to send to bureaus, creditors, debt collectors, etc.

**Print and save both documents.** The Identity Theft Report is your proof to give to creditors that you are a victim of identity theft.

### Step 1.4: Place a Fraud Alert with One Bureau

You only need to place a fraud alert with ONE bureau — the other two are legally required to honor it. Initial fraud alert lasts 90 days (free). Extended fraud alert lasts 7 years (free, requires Identity Theft Report or police report).

**Equifax fraud alert:** `https://www.equifax.com/personal/credit-report-services/credit-fraud-alert/`
**Experian fraud alert:** `https://www.experian.com/fraud/center.html`
**TransUnion fraud alert:** `https://service.transunion.com/dss/orderStep1_form.page`

---

## Phase 2 — Dispute All Fraudulent Items (Within 7 Days)

### Step 2.1: Dispute Each Fraudulent Account with the Bureau

Use the **Not-My-Account Dispute** template in `dispute-letter-specific.md` for each fraudulent account. Send to all 3 bureaus that report the account.

### Step 2.2: Contact Each Fraudulent Creditor Directly

For each fraudulent account, call the creditor's fraud department. Ask for:
- Verification of the account (do they have an application with your name and SSN?)
- Closure of the fraudulent account
- A "fraud victim" status on the account (not just "closed")
- A written confirmation that you are not liable for the account
- Removal of the account from your credit reports

Document each call: date, time, name of representative, what was said, what was promised, when follow-up is expected.

### Step 2.3: Dispute Fraudulent Inquiries

If the credit report shows hard inquiries you did not authorize, dispute them with the bureaus. Use the bureau's online dispute portal or send a letter specifying "this inquiry was not authorized by me."

---

## Phase 3 — Ongoing Protection (Within 30 Days)

### Step 3.1: Place a Credit Freeze (Already Done in Step 1.1, Confirm)

A credit freeze is stronger than a fraud alert. Confirm all 3 are in place.

### Step 3.2: File IRS Identity Theft Affidavit (Form 14039) If Tax-Related

If the fraud involves your SSN and someone may have filed or could file a tax return in your name, file IRS Form 14039 (Identity Theft Affidavit). Submit it with your next tax return. Available at `https://www.irs.gov/pub/irs-pdf/f14039.pdf`.

### Step 3.3: Check Your Social Security Statement

Go to `https://www.ssa.gov/myaccount/` and verify that your reported earnings match your actual work history. If there are earnings you did not earn, someone may be using your SSN for employment.

### Step 3.4: Contact Your Bank and Credit Card Companies

If any of your real accounts were compromised (debit card, credit card, bank account), contact the issuing institution's fraud department. Close compromised accounts and open new ones. Update automatic payments and direct deposits to the new accounts.

### Step 3.5: Update Passwords and Enable 2FA

If the fraud involved online accounts (email, financial, social media), change passwords immediately. Enable two-factor authentication (2FA) on every account that supports it. Use an authenticator app (Authy, Google Authenticator) — not SMS.

---

## Phase 4 — Documentation & Tracking

### What to Save

Save copies of EVERYTHING:
- Police report (with report number)
- FTC Identity Theft Report
- All credit reports (Equifax, Experian, TransUnion)
- All dispute letters and responses
- All correspondence with fraudulent creditors
- All correspondence with bureaus
- All call logs (date, time, rep name, summary, follow-up date)

### Where to Save

NOT in this project folder. PII must not be on disk. Save to an encrypted location of your choice:
- Encrypted USB drive
- Encrypted cloud storage (Tresorit, Sync.com, or a VeraCrypt container on OneDrive)
- Password manager with secure notes (1Password, Bitwarden)

The trackers in this folder will use aliases, not real PII. The actual documents live in your private encrypted location.

### Tracking

Update `_trackers/FRAUD-RESPONSE.md` with the chronological fraud response log.

---

## Phase 5 — Identity Eraser Acceleration (Optional, Recommended)

If the fraud indicates someone has enough of your PII to open accounts in your name, accelerate the Identity-Eraser workstream immediately. The PII may be circulating in data broker databases, on the dark web, or on people-search sites. Get ahead of it.

Use the Identity-Eraser Phase 1 (people search engines) and Phase 2 (background check + data broker registries) from the Identity-and-Credit master plan. The disposable contact kit (Phase 0) is essential here.

---

## Phase 6 — Follow-Up Cadence

- **30 days after initial dispute:** Pull all 3 credit reports. Verify fraudulent items are removed. If not, re-dispute.
- **60 days:** Verify again. If items still present, escalate to CFPB complaint.
- **90 days:** Re-dispute any remaining items with additional evidence.
- **Annually:** Pull all 3 reports. Verify no new fraudulent activity.
- **Ongoing:** Monitor credit reports monthly (free at AnnualCreditReport.com).

---

## Contact Information for Key Agencies

| Agency | Purpose | Contact |
|--------|---------|---------|
| FTC | Federal identity theft report | `https://www.identitytheft.gov/` |
| IRS | Tax-related identity theft | `https://www.irs.gov/identity-theft-central` |
| SSA | Social Security fraud | 1-800-269-0271 |
| CFPB | Credit reporting disputes | `https://www.consumerfinance.gov/complaint/` |
| FBI IC3 | Internet crime | `https://www.ic3.gov/` |
| US Postal Inspection Service | Mail theft | `https://www.uspis.gov/` |
| State Attorney General | State-level fraud | Search "[your state] attorney general consumer protection" |

---

## Track in `_trackers/FRAUD-RESPONSE.md` with the full chronology.
