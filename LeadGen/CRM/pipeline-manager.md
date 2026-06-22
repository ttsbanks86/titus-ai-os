# Pipeline Manager

## Purpose
Manage the overall sales pipeline health, forecast revenue, identify bottlenecks, and ensure consistent deal progression.

## Required Inputs
- Active deals from LEAD-TRACKER.csv (Status = PROPOSAL or later)
- Deal values and close dates
- Stage definitions and conversion rates

## Expected Outputs
- PIPELINE.csv with all active deals
- Pipeline value by stage
- Forecast report (weighted and unweighted)
- Bottleneck identification
- Recommended actions to accelerate deals

## Step-by-Step Workflow

### 1. Pipeline Stage Definition
```
Standard Stages (update to match your process):

Stage 1: PROSPECTING (0%)
  - Lead identified, initial research complete
  
Stage 2: QUALIFIED (10%)
  - Lead meets ICP, has budget and authority
  
Stage 3: DISCOVERY (20%)
  - Needs assessment call completed
  
Stage 4: PROPOSAL (40%)
  - Demo delivered, proposal sent
  
Stage 5: NEGOTIATION (60%)
  - Active deal discussions, terms being negotiated
  
Stage 6: COMMITTED (80%)
  - Verbal agreement, legal/procurement in progress
  
Stage 7: CLOSED_WON (100%)
  - Deal signed, payment received
  
Stage 8: CLOSED_LOST (0%)
  - Deal lost (with reason code)
```

### 2. Deal Data Collection
```
For each active deal:
  1. Current stage and date entered
  2. Deal value (annual contract value)
  3. Expected close date
  4. Probability (based on stage)
  5. Decision maker and champion
  6. Next action and owner
  7. Reason for last stage change
```

### 3. Pipeline Calculation
```
For each deal:
  Weighted Value = Deal Value × Stage Probability
  
Pipeline Metrics:
  - Total Pipeline Value (sum of all deal values)
  - Weighted Pipeline Value (sum of weighted values)
  - Average Deal Size
  - Average Sales Cycle Length (days in pipeline)
  - Win Rate (closed won / total closed)
  - Stage Conversion Rates
```

### 4. Bottleneck Analysis
```
Identify:
  1. Deals stuck in same stage > 2x average time
  2. Stages with low conversion rates
  3. Deals with no activity in 7+ days
  4. Owners with disproportionate workload
  5. Revenue concentration risk (few large deals)
```

### 5. Forecast Generation
```
Monthly Forecast:
  - Best Case: All committed + 50% of negotiation
  - Most Likely: All committed + 30% of negotiation + 10% of proposal
  - Conservative: All committed only
  
Weekly Changes:
  - New deals added
  - Stage progressions
  - Stage regressions
  - Deals closed (won/lost)
```

## Example Execution
```
Input: 15 active deals in LEAD-TRACKER.csv

Analysis:
  Total Pipeline: $1,250,000
  Weighted Pipeline: $485,000
  
  By Stage:
    Qualified (3 deals): $180,000 (weighted: $18,000)
    Discovery (4 deals): $320,000 (weighted: $64,000)
    Proposal (5 deals): $450,000 (weighted: $180,000)
    Negotiation (2 deals): $200,000 (weighted: $120,000)
    Committed (1 deal): $100,000 (weighted: $80,000)
  
  Bottlenecks:
    - 3 deals stuck in Proposal > 30 days
    - Proposal → Negotiation conversion only 40%
    - One AE has 60% of pipeline (capacity risk)
  
  Forecast:
    Conservative: $100,000
    Most Likely: $215,000
    Best Case: $300,000
```

## Validation Checks
- [ ] Every deal has a value and close date
- [ ] Stage probabilities match historical conversion rates
- [ ] Pipeline totals reconcile with LEAD-TRACKER.csv
- [ ] No deals without next actions
- [ ] Forecast aligns with historical win rates

## Tools Needed
| Tool | Purpose |
|------|---------|
| filesystem_read_file | Read LEAD-TRACKER.csv and PIPELINE.csv |
| filesystem_edit_file | Update pipeline records |
| filesystem_write_file | Save updated PIPELINE.csv |

## PIPELINE.csv Schema
```csv
DealName,Company,Value,Stage,CloseDate,Probability,Owner,Notes
Enterprise License,Acme Corp,120000,Negotiation,2026-07-15,60%,Titus,"Legal review in progress"
Team Plan,Beta Inc,24000,Proposal,2026-06-30,40%,Titus,"Demo completed, proposal sent 6/5"
```

## Pipeline Review Cadence
```
Daily:
  - Check overdue actions
  - Review deals moving stage today
  
Weekly:
  - Full pipeline review
  - Update all deal stages and close dates
  - Recalculate forecast
  - Identify at-risk deals
  
Monthly:
  - Stage conversion analysis
  - Win/loss review
  - Pipeline velocity trends
  - Forecast accuracy assessment
```

## Integration Notes
- Pulls deal data from LEAD-TRACKER.csv
- Feeds forecast to Reports/weekly-pipeline.md
- Alerts for stalled deals trigger outreach (follow-up.md)
- Stage changes update deal records automatically
