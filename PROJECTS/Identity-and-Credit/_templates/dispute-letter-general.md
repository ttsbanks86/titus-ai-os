# General Dispute Letter Template (FCRA)

**Use this template when disputing an item that should not be on your credit report.** Each dispute is sent to the bureau that is reporting the item. Send to all 3 bureaus (Equifax, Experian, TransUnion) if the item appears on all 3.

**Legal basis:** Fair Credit Reporting Act (FCRA), 15 U.S.C. § 1681i. Bureaus have 30 days to investigate. If they cannot verify the item, they must remove it.

---

## Letter Body

```
[Date]

[Your Name]
[Your Address]
[Your City, State, ZIP]
[Last 4 of SSN: XXX-XX-XXXX]

[Bureau Name]
[Bureau Address]

Re: Dispute of Inaccurate Information
    [Account number, last 4 digits only]

To Whom It May Concern:

I am writing to dispute the following information on my credit report. The item
listed below is [inaccurate / incomplete / unverifiable]. I have enclosed
supporting documentation.

Item disputed:
- Account: [Name of creditor, last 4 of account]
- Reason: [inaccurate / not mine / outdated / balance wrong / etc.]
- Details: [1-2 sentence explanation]

I am requesting that you:
1. Investigate this item with the original furnisher.
2. Remove or correct the item.
3. Provide me with an updated copy of my credit report.

Per the Fair Credit Reporting Act, 15 U.S.C. § 1681i, you have 30 days from
receipt of this dispute to investigate and respond. If the furnisher cannot
verify the disputed information, it must be removed.

Please send your response to my address above.

Sincerely,

[Your Signature]
[Your Printed Name]

Enclosures:
- Copy of government-issued ID
- Copy of utility bill or bank statement (proof of address)
- [Any other supporting documentation, e.g. account statements, payment records]
```

---

## Bureau Addresses (Current as of 2026)

**Equifax**
Dispute Department
P.O. Box 740256
Atlanta, GA 30374

Online: `https://www.equifax.com/personal/credit-report-services/credit-dispute/`

**Experian**
Dispute Department
P.O. Box 4500
Allen, TX 75013

Online: `https://www.experian.com/disputes/main.html`

**TransUnion**
Consumer Dispute Center
P.O. Box 2000
Chester, PA 19016

Online: `https://service.transunion.com/dss/orderStep1_form.page`

---

## Filing Methods

| Method | Pros | Cons |
|--------|------|------|
| Online portal | Fast (days vs weeks) | Less paper trail. Some items get "auto-verified" without real investigation. |
| Certified mail (return receipt) | Strong paper trail. Proof of delivery. | Slower. Costs $5-15 per letter. |
| Fax | Fast + paper trail | Receipt confirmation varies. |

**Recommendation:** For serious disputes (large balances, accounts the user did not open, items approaching statute of limitations), use certified mail. For routine items, online is fine.

---

## Tips

- **Be specific.** "This account is not mine" is better than "I dispute this account."
- **Include proof.** Bank statements, account closure letters, police reports for fraud.
- **Don't overshare.** The bureau doesn't need your full SSN, DOB, or full account number. Last 4 is enough.
- **Keep copies.** Always keep a copy of every dispute letter + enclosures.
- **Track in `_trackers/DISPUTES.csv`.** Add a row for each dispute filed.
- **Re-dispute if "verified."** If the bureau comes back "verified" and you have evidence the item is still wrong, dispute again with the new evidence. Repeat.
- **Escalate to CFPB.** If the bureau fails to investigate properly, file a complaint at `https://www.consumerfinance.gov/complaint/`. Bureaus are legally required to respond to CFPB complaints.
