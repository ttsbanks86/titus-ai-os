# Vendor Compare

## Purpose
Compare vendors on weighted criteria and create a recommendation.

## Inputs
- Vendor list (2-5 vendors)
- Evaluation criteria (features, pricing, support, etc.)
- Weight per criterion (optional, defaults to equal)
- Must-have requirements (disqualifiers)
- Budget range

## Outputs
- Side-by-side comparison table
- Weighted scoring matrix
- Pros and cons for each vendor
- Final recommendation with rationale
- Decision summary

## Workflow
1. Define evaluation criteria and weights
2. Score each vendor on each criterion (1-10)
3. Calculate weighted total scores
4. Identify must-have disqualifiers (fail = eliminated)
5. Compare pros and cons qualitatively
6. Generate recommendation based on score and fit
7. Include pricing comparison and TCO analysis

## Example Execution
```
/vendor-compare --vendors "HubSpot,Salesforce,Pipedrive" --criteria "price,features,crm,ease-of-use,support" --budget "$500/mo"

Output:
━━━ VENDOR COMPARISON: CRM Platforms ━━━

📊 WEIGHTED SCORING MATRIX
  | Criterion     | Weight | HubSpot | Salesforce | Pipedrive |
  |---------------|--------|---------|------------|-----------|
  | Price         | 25%    | 8       | 4          | 9         |
  | Features      | 25%    | 7       | 9          | 6         |
  | CRM           | 20%    | 8       | 9          | 7         |
  | Ease of Use   | 15%    | 9       | 5          | 8         |
  | Support       | 15%    | 7       | 6          | 7         |
  |---------------|--------|---------|------------|-----------|
  | WEIGHTED TOTAL| 100%   | 7.7     | 6.6        | 7.4       |

💰 PRICING (per user/month)
  | Vendor       | Base    | Premium | Enterprise | Fits Budget? |
  |--------------|---------|---------|------------|--------------|
  | HubSpot      | $45     | $90     | $150       | ✅ Yes       |
  | Salesforce   | $75     | $150    | $300       | ⚠️ Tight    |
  | Pipedrive    | $39     | $69     | $99        | ✅ Yes       |

✅ MUST-HAVES CHECK
  | Requirement              | HubSpot | Salesforce | Pipedrive |
  |--------------------------|---------|------------|-----------|
  | API access               | ✅      | ✅         | ✅        |
  | Email integration        | ✅      | ✅         | ✅        |
  | Custom fields            | ✅      | ✅         | ⚠️ Limited|
  | Automation workflows     | ✅      | ✅         | ✅        |

📋 PROS & CONS
  HubSpot
    Pros: Best ease of use, strong free tier, excellent onboarding
    Cons: Advanced features require higher tiers, limited customization

  Salesforce
    Pros: Most powerful CRM, extensive integrations, enterprise-grade
    Cons: Steep learning curve, expensive, overkill for small teams

  Pipedrive
    Pros: Best price, clean UI, sales-focused pipeline
    Cons: Limited custom fields, weaker reporting, fewer integrations

🏆 RECOMMENDATION: HubSpot
  Rationale: Highest weighted score (7.7), fits budget, best ease of use
  for the team size. Salesforce is overkill; Pipedrive lacks features.

  Suggested Plan: HubSpot Professional ($90/user/mo)
  Total for 5 users: $450/mo ✅ Within budget
```

## Validation Checks
- Confirm all vendors meet must-have requirements (or note disqualifications)
- Verify pricing data is current and accurate
- Check that weights sum to 100%
- Ensure scores are objective and backed by evidence
- Validate that recommendation aligns with stated priorities
