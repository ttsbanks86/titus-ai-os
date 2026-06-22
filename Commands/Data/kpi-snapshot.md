# KPI Snapshot

## Purpose
Generate a KPI dashboard from data sources with trends and benchmarks.

## Inputs
- KPI definitions (name, target, current value, trend)
- Data source (spreadsheet, API, database, or manual input)
- Time period (daily, weekly, monthly, quarterly)
- Comparison period (previous period, same period last year)

## Outputs
- KPI summary table with status indicators
- Trend analysis (up/down/stable)
- Target vs actual comparison
- Visual chart data (if applicable)
- Alerts for underperforming KPIs

## Workflow
1. Ingest KPI data from specified source
2. Calculate current values and compare against targets
3. Determine status for each KPI:
   - 🟢 On Track: ≥90% of target
   - 🟡 Watch: 70-89% of target
   - 🔴 Alert: <70% of target
4. Calculate period-over-period change
5. Identify top movers (biggest positive/negative changes)
6. Generate summary with alerts and recommendations

## Example Execution
```
/kpi-snapshot --source "sales-data.csv" --period "June 2026" --compare "May 2026"

Output:
━━━ KPI SNAPSHOT: June 2026 vs May 2026 ━━━

| KPI                  | Target    | Actual    | Status | Δ vs Last Mo |
|----------------------|-----------|-----------|--------|--------------|
| Revenue              | $500K     | $523K     | 🟢     | +4.6%        |
| New Customers        | 120       | 108       | 🟡     | -2.1%        |
| Churn Rate           | <5%       | 3.2%      | 🟢     | -0.8%        |
| NPS Score            | 50        | 42        | 🟡     | -3.0         |
| Support Response     | <4h       | 2.1h      | 🟢     | -15min       |
| Pipeline Value       | $1.2M     | $1.4M     | 🟢     | +16.7%       |

🔥 TOP MOVERS:
  ↑ Pipeline Value: +$200K (new enterprise deals)
  ↓ New Customers: -12 (seasonal dip expected)

⚠️ ALERTS:
  NPS dropped below target – survey results suggest onboarding friction

💡 RECOMMENDATION:
  Consider onboarding flow improvements to recover NPS next month.
```

## Validation Checks
- Confirm data source is current and complete
- Verify calculations (percentages, deltas) are accurate
- Ensure status thresholds are applied consistently
- Flag any KPIs with missing or zero values
- Validate comparison period data exists
