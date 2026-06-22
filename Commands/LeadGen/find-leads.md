# Find Leads

## Purpose
Discover potential leads from multiple sources based on ideal customer profile.

## Inputs
- Ideal customer profile (industry, size, location, pain points)
- Source preferences (LinkedIn, web, directories, referrals)
- Lead count target
- Budget for lead generation (optional)
- Exclusion criteria (existing customers, competitors)

## Outputs
- Lead list with contact information
- Lead score per prospect
- Source attribution
- Enrichment data (company size, tech stack, recent activity)
- Outreach readiness assessment

## Workflow
1. Define ideal customer profile from inputs
2. Search across specified sources:
   - LinkedIn: Company search + employee filtering
   - Web: Industry directories, review sites, job boards
   - Referrals: Existing network connections
3. Enrich leads with additional data:
   - Company size and revenue
   - Tech stack and tools used
   - Recent funding, hiring, or news
4. Score leads against ICP criteria
5. De-duplicate and verify contact information
6. Rank by fit score and outreach readiness

## Example Execution
```
/find-leads --icp "SaaS, 50-200 employees, Series A-B, uses HubSpot" --sources "linkedin,web" --count 25

Output:
━━━ LEAD FIND: 25 Qualified Leads ━━━

🎯 ICP: SaaS | 50-200 employees | Series A-B | HubSpot user

📊 LEAD LIST
| # | Company      | Size | Revenue  | Tech Stack     | Score | Source   |
|---|--------------|------|----------|----------------|-------|----------|
| 1 | DataFlow     | 85   | $12M ARR | HubSpot, AWS   | 92    | LinkedIn |
| 2 | CloudSync    | 120  | $18M ARR | HubSpot, GCP   | 88    | Web      |
| 3 | TechPulse    | 65   | $8M ARR  | HubSpot, Azure | 85    | LinkedIn |
| 4 | AnalyticsPro | 150  | $22M ARR | HubSpot, AWS   | 82    | Web      |
| 5 | DevStack     | 72   | $10M ARR | HubSpot, GCP   | 80    | LinkedIn |

🔍 LEAD DETAILS (Top 5)
  1. DataFlow (Score: 92)
     Contact: Sarah Chen, VP Sales (sarah@dataflow.io)
     Signal: Just raised Series B ($15M), hiring 10 SDRs
     Tech: HubSpot (active user), AWS stack
     Why fit: Scaling sales team, likely needs workflow automation

  2. CloudSync (Score: 88)
     Contact: Mike Rodriguez, CRO (mike@cloudsync.com)
     Signal: Expanded to new market, 3 job posts for sales ops
     Tech: HubSpot (enterprise tier), GCP
     Why fit: Market expansion = process documentation needs

📋 NEXT STEPS
  1. Enrich top 10 with email addresses (Clearbit/Apollo)
  2. Personalize outreach for each
  3. Begin sequence for leads with score >85

📊 SUMMARY
  Total found: 47 | Qualified: 25 | Score >80: 12
  Estimated response rate: 15-20%
  Pipeline value potential: $180K-$240K
```

## Validation Checks
- Confirm leads match ICP criteria (industry, size, funding stage)
- Verify contact information is current and accurate
- Ensure no duplicates with existing CRM records
- Check that excluded companies (competitors, existing customers) are filtered
- Validate lead scores are based on objective criteria
