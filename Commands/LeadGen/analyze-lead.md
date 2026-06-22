# Analyze Lead

## Purpose
Analyze lead quality, fit score, and engagement readiness.

## Inputs
- Lead information (company, contacts, firmographic data)
- Engagement history (website visits, email opens, content downloads)
- Deal history (if existing relationship)
- ICP criteria for scoring

## Outputs
- Lead quality score (0-100)
- Fit analysis against ICP
- Engagement level assessment
- Recommended next action
- Personalization angles

## Workflow
1. Gather lead data from CRM or enrichment sources
2. Score against ICP criteria:
   - Firmographic fit (industry, size, location)
   - Behavioral signals (engagement, intent)
   - Technographic fit (tools they use)
   - Timing signals (hiring, funding, pain indicators)
3. Calculate composite quality score
4. Determine engagement level:
   - Hot: Recent high engagement
   - Warm: Some engagement signals
   - Cold: No engagement, outbound only
5. Identify personalization angles from company news or triggers
6. Recommend specific outreach approach

## Example Execution
```
/analyze-lead --company "DataFlow" --contact "sarah@dataflow.io"

Output:
━━━ LEAD ANALYSIS: DataFlow ━━━

📊 QUALITY SCORE: 92/100

🎯 ICP FIT
  | Criterion         | Required      | Actual        | Match |
  |-------------------|---------------|---------------|-------|
  | Industry          | SaaS          | SaaS          | ✅    |
  | Company Size      | 50-200        | 85            | ✅    |
  | Revenue           | $5M+ ARR      | $12M ARR      | ✅    |
  | Location          | North America | SF, CA        | ✅    |
  | Tech Stack        | HubSpot       | HubSpot       | ✅    |
  | Funding Stage     | Series A-B    | Series B      | ✅    |

🔥 ENGAGEMENT LEVEL: Hot
  - Website visits: 12 in last 30 days
  - Content downloads: 2 (ROI calculator, case study)
  - Email opens: 4 of 5 recent emails
  - Pricing page visit: June 5, 2026

🏢 COMPANY SIGNALS
  - Just closed $15M Series B (May 2026)
  - Hiring 10 SDRs (posted June 1)
  - Expanded to EMEA market (Q2)
  - CEO quote: "Scaling sales operations" in recent interview

👤 CONTACT: Sarah Chen, VP Sales
  - Tenure: 2 years
  - Previously: HubSpot (Sales Manager)
  - LinkedIn: Active poster, sales ops content
  - Mutual connections: 3

💡 PERSONALIZATION ANGLES
  1. Reference their Series B and scaling journey
  2. Mention HubSpot background (shared platform knowledge)
  3. Connect to EMEA expansion (process documentation needs)
  4. Reference SDR hiring (onboarding workflow opportunity)

🎯 RECOMMENDED ACTION
  Priority: HIGH – Outreach within 24 hours
  Channel: LinkedIn connection + email
  Message angle: "Congrats on Series B – scaling sales ops is exactly what we help with"
  Best time: Tuesday-Thursday, 9-11am PT

📋 COMPETITIVE LANDSCAPE
  - Current vendor: Likely building internally
  - Alternative: Could evaluate Salesforce (but HubSpot user = lower switching cost)
  - Risk: May be too early in journey (just raised, not yet hiring ops)
```

## Validation Checks
- Confirm all data points are current (within 30 days)
- Verify ICP criteria are applied consistently
- Ensure engagement data is accurate and not inflated
- Check that personalization angles are genuine and relevant
- Validate that recommended action matches engagement level
