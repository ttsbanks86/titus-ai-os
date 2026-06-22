# Prospect Scoring

## Purpose
Automatically score leads based on fit (ICP alignment) and intent (buying signals), then assign priority tiers.

## Trigger
- **Primary**: Lead data updated in `LEAD-TRACKER.csv` (enrichment completed)
- **Secondary**: On-demand via OpenCode command

## Input Sources
- `C:\Users\tbank\Desktop\Live Cowork\CRM\LEAD-TRACKER.csv` — Lead data with enriched fields
- ICP criteria from `C:\Users\tbank\Desktop\Live Cowork\Commands\Automation\icp-criteria.json` (optional override)

## Output Destinations
- Updated `LEAD-TRACKER.csv` — `score` (0-100), `priority` (Hot/Warm/Cold)
- Alert notification for Hot leads (email or desktop notification)
- `output/scoring-log-{date}.md` — Scoring audit trail

## Scoring Criteria

### Fit Score (0-50)
| Criterion | Points | Source |
|-----------|--------|--------|
| Company size 50-500 employees | +15 | Enriched data |
| Company size 500-5000 employees | +10 | Enriched data |
| SaaS/Technology industry | +15 | Enriched data |
| Decision-maker title (VP/Director/C-suite) | +10 | Apollo/LinkedIn |
| Annual revenue > $5M | +10 | Enriched data |

### Intent Score (0-50)
| Criterion | Points | Source |
|-----------|--------|--------|
| Recent funding (last 6 months) | +15 | News research |
| Hiring signals (job postings) | +10 | LinkedIn/web |
| Website mentions of relevant keywords | +10 | Firecrawl scrape |
| Recently adopted competitor tool | +10 | News/research |
| Engaged with content (LinkedIn) | +5 | LinkedIn data |

### Priority Tiers
- **Hot** (75-100): Immediate outreach — personal outreach within 24h
- **Warm** (40-74): Nurture — scheduled outreach within 1 week
- **Cold** (0-39): Monitor — monthly check-in, no active outreach

## Step-by-Step Workflow

```
1. READ
   └─ Parse LEAD-TRACKER.csv
   └─ Find rows where score = "" or score needs refresh
   └─ Extract all enriched fields for scoring

2. FIT SCORING
   └─ Evaluate company_size against ICP thresholds
   └─ Evaluate industry against target list
   └─ Evaluate decision-maker seniority
   └─ Evaluate revenue range
   └─ Sum fit_points (max 50)

3. INTENT SCORING
   └─ Check recent funding news (last 6 months)
   └─ Check hiring activity
   └─ Check website keyword mentions
   └─ Check competitor adoption signals
   └─ Sum intent_points (max 50)

4. CALCULATE TOTAL
   └─ total_score = fit_points + intent_points
   └─ Assign priority tier based on thresholds

5. UPDATE CSV
   └─ Write score and priority to LEAD-TRACKER.csv
   └─ Set scored_date = current_date

6. ALERT (if Hot lead)
   └─ Generate alert with lead summary
   └─ Send notification (email/desktop)
   └─ Log to scoring-log.md

7. LOG
   └─ Append scoring details to scoring-log-{date}.md
   └─ Include: lead name, score breakdown, priority, timestamp
```

## MCP Tools Required
| Tool | Purpose |
|------|---------|
| `csv_read` / `csv_write` | Read/update LEAD-TRACKER.csv |
| `perplexity_perplexity_search` | Quick company news check |
| `firecrawl_firecrawl_search` | Detailed research if needed |
| `sequential-thinking_sequentialthinking` | Score calculation reasoning |

## Example Execution

**Input lead:**
```csv
company_name,employee_count,industry,contact_title,revenue,funding_date,has_hiring_signals
Acme Corp,150,SaaS,VP Engineering,$10M,2026-03-01,true
```

**Scoring output:**
```
Fit Score: 40/50
  - Company size (50-500): +15
  - SaaS industry: +15
  - VP title: +10
  - Revenue > $5M: (not verified, 0)

Intent Score: 35/50
  - Recent funding: +15
  - Hiring signals: +10
  - Website keywords: +10

Total: 75/100 → Priority: HOT 🔥
Action: Immediate personal outreach within 24h
```

## Error Handling
- **Missing enriched data**: Score with available fields, flag as "Partial Score"
- **Duplicate scoring**: Skip if scored_date is today, force re-score only on-demand
- **All criteria fail**: Assign Cold priority, log reason
- **Alert delivery failure**: Log error, still update CSV

## Validation Checks
- [ ] Score is between 0 and 100
- [ ] Priority matches score thresholds
- [ ] All available criteria are evaluated
- [ ] CSV update does not overwrite non-scoring fields
- [ ] Hot lead alert contains lead name and contact info
- [ ] Scoring log includes score breakdown
