# Specific Dispute Letter Templates

**These are templates for SPECIFIC dispute scenarios.** Use `dispute-letter-general.md` for routine errors. Use the templates below for situations that require specific legal language.

---

## 1. Not-My-Account Dispute (Fraud or Mixed File)

**Use when:** An account appears on your report that you did not open. Could be identity theft, could be a mixed-file error (someone with a similar name or SSN).

```
[Date]

[Bureau Name]
[Bureau Address]

Re: Dispute — Account Not Opened by Consumer
    Account: [Creditor Name], last 4 [XXXX]

To Whom It May Concern:

The account listed above on my credit report is NOT my account. I did not
open this account, and I have no knowledge of it. I am formally disputing
this item and requesting immediate removal.

I have enclosed a copy of my government-issued ID and proof of my current
address for verification.

I am also requesting:
1. The full name, address, and contact information of the original
   creditor.
2. The date the account was opened.
3. The application used to open the account, including the IP address
   and device information.
4. Verification of the chain of custody for this account from
   origination to current furnisher.

If this account is the result of identity theft, I am also requesting:
1. A fraud alert be placed on my credit file (90-day initial, renewable).
2. A security freeze to be placed on my credit file.
3. Notification to all furnishisher of the suspected fraudulent account
   that the account is disputed and being investigated.
4. Removal of all inquiries associated with this fraudulent account.

I am aware that under the Fair Credit Reporting Act, 15 U.S.C. § 1681i,
you are required to investigate this dispute within 30 days. If the
furnisher cannot verify this account, it must be removed.

Sincerely,

[Your Signature]
[Your Printed Name]
[SSN last 4: XXXX]
```

**Action items if this is suspected identity theft:**
1. File the dispute letter above with all 3 bureaus
2. File a police report with local law enforcement
3. File a report at `https://www.identitytheft.gov/` (FTC)
4. Place a credit freeze with all 3 bureaus (free, no expiration)
5. Place a fraud alert with one bureau (the other two are required to honor it)
6. Track in `_trackers/DISPUTES.csv` AND `_trackers/FRAUD-RESPONSE.md`

---

## 2. Balance Discrepancy Dispute

**Use when:** The balance shown on your credit report does not match what you actually owe.

```
[Date]

[Bureau Name]
[Bureau Address]

Re: Dispute — Balance Inaccuracy
    Account: [Creditor Name], last 4 [XXXX]

To Whom It May Concern:

I am disputing the balance reported on the above-referenced account. The
credit report shows a balance of [$X,XXX.XX] as of [report date]. My
records show an actual balance of [$X,XXX.XX], a discrepancy of
[$X,XXX.XX].

I have enclosed the following supporting documentation:
- Most recent account statement from [Creditor Name] dated [date]
- Payment records showing payments of [$amount] on [date], [$amount] on
  [date], etc.
- Any written correspondence regarding the account

I am requesting:
1. Investigation of the balance discrepancy with the original furnisher.
2. Correction of the balance on my credit report to reflect the
   accurate amount.
3. Re-aging of the account if appropriate based on the corrected
   balance and most recent payment.

Per the Fair Credit Reporting Act, 15 U.S.C. § 1681i, please investigate
and respond within 30 days.

Sincerely,

[Your Signature]
[Your Printed Name]
```

---

## 3. Outdated Account Dispute (Past Reporting Period)

**Use when:** A closed or paid account is still being reported as active, or an account is being reported beyond the maximum reporting period (typically 7 years from date of first delinquency for negative items, 10 years for bankruptcy).

```
[Date]

[Bureau Name]
[Bureau Address]

Re: Dispute — Item Past Maximum Reporting Period
    Account: [Creditor Name], last 4 [XXXX]

To Whom It May Concern:

The account listed above on my credit report was [paid in full / closed /
charged off] on [date]. Under the Fair Credit Reporting Act,
15 U.S.C. § 1681c, negative information cannot be reported for more than
[7 years from the date of first delinquency / 10 years for bankruptcy].

The date of first delinquency on this account was [date]. The maximum
reporting period therefore expired on [date + 7 years]. This account
should be removed from my credit report.

I am requesting:
1. Immediate removal of this account from my credit report.
2. Confirmation in writing that the account has been removed.

Sincerely,

[Your Signature]
[Your Printed Name]
```

---

## 4. Duplicate Account Dispute

**Use when:** The same account appears more than once on your credit report (often with slightly different creditor names due to a sale or transfer).

```
[Date]

[Bureau Name]
[Bureau Address]

Re: Dispute — Duplicate Account Reporting
    Accounts: [Creditor Name 1] and [Creditor Name 2], both last 4 [XXXX]

To Whom It May Concern:

My credit report lists the above-referenced account twice, under two
different creditor names. Both accounts share the same account number
ending in [XXXX], the same opening date, and the same balance.

This is a duplicate entry. The same debt cannot be reported twice. I am
requesting:
1. Investigation to confirm this is a duplicate.
2. Removal of one of the duplicate entries from my credit report.
3. Updated credit report reflecting the correction.

Sincerely,

[Your Signature]
[Your Printed Name]
```

---

## Track all specific disputes in `_trackers/DISPUTES.csv`.
