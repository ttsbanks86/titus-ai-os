# Weekly Pipeline Report

## Purpose
Generate a comprehensive weekly snapshot of pipeline health, deal progression, team performance, and key metrics to inform decision-making.

## Required Inputs
- LEAD-TRACKER.csv (current state)
- PIPELINE.csv (active deals)
- Activity logs from the past 7 days
- Prior week's report for comparison

## Expected Outputs
- Weekly pipeline summary dashboard
- Deal progression analysis
- Activity and performance metrics
- Risk flags and recommended actions
- Next week's priorities

## Step-by-Step Workflow

### 1. Data Collection
```
Gather from LEAD-TRACKER.csv:
  - Total leads by status
  - New leads added this week
  - Leads that moved stage
  - Leads that exited (won/lost/nurture)

Gather from PIPELINE.csv:
  - All active deals with current values
  - Deals that changed stage this week
  - Deals closed this week
  - Overdue deals (past expected close date)
```

### 2. Calculate Key Metrics
```
Pipeline Metrics:
  - Total Pipeline Value: $______
  - Weighted Pipeline Value: $______
  - Number of Active Deals: __
  - Average Deal Size: $______
  - Average Days in Pipeline: __
  - Win Rate (trailing 30 days): ___%

Activity Metrics:
  - New Leads Added: __
  - Outreach Sent: __
  - Meetings Booked: __
  - Demos Conducted: __
  - Proposals Sent: __
  - Deals Closed: __

Conversion Metrics:
  - Lead → Contacted: ___%
  - Contacted → Engaged: ___%
  - Engaged → Qualified: ___%
  - Qualified → Proposal: ___%
  - Proposal → Closed Won: ___%
```

### 3. Week-over-Week Comparison
```
Compare to last week:
  - Pipeline value change: +$______ / -$______ (___%)
  - Deal count change: +__ / -__
  - Win rate trend: improving / stable / declining
  - Activity trend: up / flat / down
  - Key wins: [list]
  - Key losses: [list]
```

### 4. Risk Assessment
```
Flag risks:
  - Deals past expected close date (aging)
  - Pipeline concentration (few large deals)
  - Conversion rate drops by stage
  - Activity declining week-over-week
  - Single points of failure (one rep holding key deals)
```

### 5. Generate Report
```markdown
# Weekly Pipeline Report - [Date]

## Executive Summary
[2-3 sentence overview of pipeline health]

## Pipeline Snapshot
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Total Pipeline | $X | $Y | +Z% |
| Weighted Pipeline | $X | $Y | +Z% |
| Active Deals | X | Y | +Z |
| Win Rate | X% | Y% | +Z pp |

## Deal Progression
### Moved Forward (List)
- [Deal] moved from [Stage] to [Stage]

### At Risk (List)
- [Deal] stuck in [Stage] for X days

### Closed
- Won: [Deal] - $X
- Lost: [Deal] - $X (reason)

## Activity Summary
- Outreach: X sent
- Meetings: X booked
- Demos: X conducted
- Proposals: X sent

## Conversion Funnel
| Stage | Count | Rate | Trend |
|-------|-------|------|-------|
| New → Contacted | X | X% | ↑/↓/→ |
| Contacted → Engaged | X | X% | ↑/↓/→ |
| Engaged → Qualified | X | X% | ↑/↓/→ |

## Risks & Actions
1. [Risk]: [Recommended Action]
2. [Risk]: [Recommended Action]

## Next Week Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```

## Example Execution
```
Input: LEAD-TRACKER.csv and PIPELINE.csv as of 2026-06-07

Report Output:
# Weekly Pipeline Report - 2026-06-07

## Executive Summary
Pipeline healthy at $1.25M total, $485K weighted. 3 deals progressing well, 
1 deal at risk (Acme Corp stalled in negotiation). Win rate stable at 28%.

## Pipeline Snapshot
| Metric | This Week | Last Week | Change |
|--------|-----------|-----------|--------|
| Total Pipeline | $1,250,000 | $1,180,000 | +5.9% |
| Weighted Pipeline | $485,000 | $445,000 | +9.0% |
| Active Deals | 15 | 14 | +1 |
| Win Rate | 28% | 27% | +1 pp |

## Deal Progression
### Moved Forward
- Beta Inc: Proposal → Negotiation ($24K)
- Gamma Co: Discovery → Proposal ($45K)

### At Risk
- Acme Corp: Stuck in Negotiation 14 days (avg: 10)
```

## Validation Checks
- [ ] All numbers reconcile with source CSVs
- [ ] Week-over-week comparisons are accurate
- [ ] Risks are actionable, not just informational
- [ ] Next week priorities are specific and assigned
- [ ] Report generated same day each week

## Tools Needed
| Tool | Purpose |
|------|---------|
| filesystem_read_file | Read CSV data sources |
| filesystem_write_file | Save report |

## Report Schedule
```
Weekly:
  - Generate report every Friday at 4pm
  - Share with team by 5pm Friday
  - Use for Monday morning pipeline review
  
Monthly:
  - Aggregate 4 weekly reports
  - Identify monthly trends
  - Feed into strategic planning
```

## Integration Notes
- Data sourced from lead-tracker.md and pipeline-manager.md
- Activity metrics from email-sequence.md and linkedin-outreach.md
- Insights inform next week's lead-finder.md priorities
- Risks trigger follow-up.md actions
