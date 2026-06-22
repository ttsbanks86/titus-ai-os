# Pipeline Report

## Purpose
Create a sales/pipeline report from CRM data with stage analysis and forecasts.

## Inputs
- CRM data source (HubSpot, Salesforce, spreadsheet)
- Pipeline stages definition
- Date range or snapshot date
- Forecast model (simple, weighted, AI-assisted)

## Outputs
- Pipeline summary by stage
- Deal velocity and conversion rates
- Weighted pipeline value
- Forecast projection
- At-risk deals and recommendations

## Workflow
1. Pull deals from CRM with current stage and value
2. Calculate pipeline metrics:
   - Total pipeline value
   - Value by stage
   - Average deal size
   - Win rate by stage
   - Average time in stage (velocity)
3. Apply forecast model to project revenue
4. Identify at-risk deals (stalled, past expected close date)
5. Flag top opportunities and quick wins
6. Generate report with visual stage breakdown

## Example Execution
```
/pipeline-report --source hubspot --range "Q2 2026" --forecast weighted

Output:
━━━ PIPELINE REPORT: Q2 2026 ━━━

📊 PIPELINE OVERVIEW
  Total Deals: 47
  Total Value: $2,840,000
  Weighted Value: $1,420,000

📈 BY STAGE
  | Stage        | Deals | Value     | Weighted  | Avg Days |
  |--------------|-------|-----------|-----------|----------|
  | Prospecting  | 15    | $450K     | $45K      | 12       |
  | Discovery    | 12    | $680K     | $170K     | 18       |
  | Proposal     | 10    | $890K     | $356K     | 22       |
  | Negotiation  | 7     | $520K     | $364K     | 15       |
  | Closed Won   | 3     | $300K     | $300K     | —        |

🎯 FORECAST
  Conservative: $1,100,000
  Weighted:     $1,420,000
  Optimistic:   $1,850,000

⚠️ AT-RISK DEALS (stalled >14 days):
  1. Acme Corp ($180K) – Last touch: 18 days ago
  2. TechStart ($95K) – Decision maker unresponsive

🏆 TOP OPPORTUNITIES:
  1. GlobalCo ($320K) – Proposal sent, positive signals
  2. DataInc ($210K) – Budget confirmed, moving to legal
```

## Validation Checks
- Confirm all deals in CRM are included in the report
- Verify stage values and percentages are accurate
- Ensure weighted calculations match the forecast model
- Check that velocity calculations use correct date ranges
- Flag deals with missing close dates or values
