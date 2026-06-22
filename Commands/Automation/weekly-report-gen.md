# Weekly Report Generator

## Purpose
Generate a comprehensive weekly pipeline and activity report summarizing lead status, conversion rates, bottlenecks, and next-week priorities.

## Trigger
- **Primary**: Friday at 5:00 PM (scheduled)
- **Secondary**: On-demand via OpenCode command

## Input Sources
- `C:\Users\tbank\Desktop\Live Cowork\CRM\LEAD-TRACKER.csv` — All leads
- `output/scoring-log-*.md` — Weekly scoring activity
- `output/research-*.md` — Weekly research activity
- `output/follow-up-reminders-*.md` — Weekly follow-up activity

## Output Destinations
- `output/weekly-report-{date}.md` — Formatted weekly report
- Email summary to stakeholders (optional)
- Dashboard update (if applicable)

## Report Structure

```markdown
# Weekly Report — Week of {start_date} to {end_date}

## Pipeline Summary
- Total Leads: X
- New Leads: X
- Active Pipeline: X
- Closed Won: X
- Closed Lost: X

## Lead Status Breakdown
| Status | Count | Change vs Last Week |
|--------|-------|-------------------|
| New | X | +X / -X |
| Researched | X | +X / -X |
| Scored | X | +X / -X |
| Outreach Generated | X | +X / -X |
| Engaged | X | +X / -X |
| Proposal Sent | X | +X / -X |
| Negotiating | X | +X / -X |
| Closed Won | X | +X / -X |
| Closed Lost | X | +X / -X |

## Priority Distribution
| Priority | Count | Avg Score |
|----------|-------|-----------|
| Hot | X | XX |
| Warm | X | XX |
| Cold | X | XX |

## Conversion Metrics
- New → Researched: X%
- Researched → Scored: X%
- Scored → Outreach: X%
- Outreach → Engaged: X%
- Engaged → Closed Won: X%
- Overall: X% (New → Closed Won)

## This Week's Activity
- Leads researched: X
- Leads scored: X
- Outreach generated: X
- Follow-ups sent: X
- Follow-ups overdue: X

## Bottlenecks
- [List any pipeline stages with unusual drop-off]

## Top Hot Leads (Action Required)
| Lead | Score | Status | Next Action |
|------|-------|--------|-------------|
| ... | ... | ... | ... |

## Next Week Priorities
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

## Recommendations
- [AI-generated insights based on pipeline data]
```

## Step-by-Step Workflow

```
1. READ DATA
   └─ Parse LEAD-TRACKER.csv (all rows)
   └─ Load this week's scoring logs
   └─ Load this week's research logs
   └─ Load this week's follow-up reminders

2. AGGREGATE STATISTICS
   └─ Count leads by status
   └─ Count leads by priority
   └─ Calculate this week's changes:
      ├─ New leads added this week
      ├─ Status transitions this week
      └─ Leads closed this week

3. CALCULATE CONVERSION RATES
   └─ For each pipeline stage:
      ├─ Input count (leads entering stage)
      ├─ Output count (leads advancing)
      └─ Conversion rate = output / input * 100
   └─ Calculate overall conversion rate

4. IDENTIFY BOTTLENECKS
   └─ Find stages with > 30% drop-off
   └─ Find stages where leads linger > 7 days average
   └─ Flag stages with 0 activity this week

5. GENERATE INSIGHTS
   └─ Analyze hot lead distribution
   └─ Identify at-risk leads (stale for 30+ days)
   └─ Suggest next-week priorities based on:
      ├─ Hot leads needing immediate action
      ├─ Leads approaching follow-up dates
      └─ Pipeline stage imbalances

6. FORMAT REPORT
   └─ Populate report template with aggregated data
   └─ Add trend indicators (+/- vs last week)
   └─ Include bottleneck analysis
   └─ Include AI recommendations

7. SAVE & DELIVER
   └─ Save to output/weekly-report-{date}.md
   └─ If stakeholders configured: email summary
   └─ Log execution to output/workflow-log.md
```

## MCP Tools Required
| Tool | Purpose |
|------|---------|
| `csv_read` | Read LEAD-TRACKER.csv |
| `file_read` | Load activity logs |
| `file_write` | Save weekly report |
| `sequential-thinking_sequentialthinking` | Insight generation |
| `bash` | Email notification (optional) |

## Example Execution

**Pipeline summary output:**
```markdown
# Weekly Report — Week of 2026-06-01 to 2026-06-07

## Pipeline Summary
- Total Leads: 45
- New Leads This Week: 12
- Active Pipeline: 38
- Closed Won: 3
- Closed Lost: 2

## Lead Status Breakdown
| Status | Count | vs Last Week |
|--------|-------|-------------|
| New | 12 | +5 |
| Researched | 8 | +3 |
| Scored | 6 | +2 |
| Engaged | 4 | -1 |
| Closed Won | 3 | +1 |

## Conversion Metrics
- New → Researched: 67%
- Researched → Scored: 75%
- Scored → Engaged: 67%
- Engaged → Closed Won: 75%
- Overall: 25% (New → Closed Won)

## Bottlenecks
- ⚠️ Scored → Engaged: 33% drop-off (leads stalling after outreach)
  - Recommendation: Review outreach messaging, test new angles

## Top Hot Leads
| Lead | Score | Status | Next Action |
|------|-------|--------|-------------|
| Acme Corp | 85 | Engaged | Send proposal by Monday |
| Beta Inc | 78 | Scored | Send initial outreach |
```

## Error Handling
- **Empty CSV**: Generate report with "No data available" placeholders
- **Missing activity logs**: Skip log-dependent sections, note as "Data unavailable"
- **Division by zero**: Set conversion rate to 0%, note as "No leads in stage"
- **Email delivery failure**: Log error, report still saved to file

## Validation Checks
- [ ] Total lead count matches CSV row count
- [ ] Status counts sum to total (excluding Closed)
- [ ] Conversion rates are between 0% and 100%
- [ ] Trend indicators are accurate (+/- vs last week)
- [ ] Hot leads list contains only Hot priority leads
- [ ] Recommendations are specific and actionable
- [ ] Report date range is correct (Monday-Friday)
- [ ] All pipeline stages are represented
