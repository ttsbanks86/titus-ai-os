# Expense Scan

## Purpose
Analyze expenses, flag anomalies, and suggest optimizations.

## Inputs
- Expense data (spreadsheet, accounting software export, or manual entries)
- Budget baseline or historical average
- Category definitions
- Threshold for anomalies (e.g., >20% above average)

## Outputs
- Expense summary by category
- Anomaly flags with explanations
- Budget variance analysis
- Optimization recommendations
- Trend analysis

## Workflow
1. Ingest expense data and categorize entries
2. Calculate totals by category and time period
3. Compare against budget baseline or historical average
4. Flag anomalies:
   - Single transactions significantly above average
   - Categories exceeding budget
   - Unusual vendor patterns
   - Duplicate or near-duplicate entries
5. Identify optimization opportunities:
   - Redundant subscriptions
   - Underutilized services
   - Volume discount opportunities
6. Generate report with actionable recommendations

## Example Execution
```
/expense-scan --data "expenses-q2.csv" --budget "budget-q2.csv" --threshold 20

Output:
━━━ EXPENSE SCAN: Q2 2026 ━━━

💰 TOTAL SPEND: $127,450 (Budget: $130,000 | Under by $2,550)

📊 BY CATEGORY
  | Category        | Spent    | Budget   | Variance | Status |
  |-----------------|----------|----------|----------|--------|
  | Software        | $34,200  | $30,000  | +14.0%   | 🟡     |
  | Contractors     | $42,800  | $45,000  | -4.9%    | 🟢     |
  | Marketing       | $28,500  | $30,000  | -5.0%    | 🟢     |
  | Travel          | $12,450  | $15,000  | -17.0%   | 🟢     |
  | Office          | $9,500   | $10,000  | -5.0%    | 🟢     |

🔴 ANOMALIES:
  1. Adobe Creative Suite: $899/mo (was $549/mo) – Unplanned license increase
  2. AWS EC2: $4,200 one-time charge – Unbudgeted instance spin-up
  3. Duplicate: WeWork invoice $1,200 posted twice (June 3 & June 5)

💡 OPTIMIZATIONS:
  1. Cancel unused Figma Enterprise license ($45/mo saved)
  2. Switch Zoom → Google Meet (saves $180/mo)
  3. Bundle Adobe licenses for volume discount (est. $120/mo saved)

📈 TREND: Software spend up 23% QoQ – review all SaaS subscriptions
```

## Validation Checks
- Confirm all expense entries are categorized correctly
- Verify budget numbers match the approved budget document
- Ensure anomalies are genuinely unusual (not just high-value legitimate purchases)
- Check for duplicate entries across the dataset
- Validate that recommendations are realistic and implementable
