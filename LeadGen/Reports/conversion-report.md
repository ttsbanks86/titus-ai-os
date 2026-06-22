# Conversion Analysis Report

## Purpose
Analyze conversion rates across the entire lead lifecycle to identify bottlenecks, optimize messaging, and improve overall pipeline velocity.

## Required Inputs
- Historical LEAD-TRACKER.csv data (30-90 days)
- Pipeline stage definitions and probabilities
- Campaign/source attribution data
- A/B test results from email-sequence.md

## Expected Outputs
- Full-funnel conversion rates by stage
- Conversion trends over time
- Bottleneck identification with root causes
- Source/channel effectiveness comparison
- Recommended optimizations with expected impact

## Step-by-Step Workflow

### 1. Funnel Conversion Calculation
```
Calculate stage-to-stage conversion rates:

Lead → Contacted
  Formula: (Leads Contacted / Total Leads) × 100
  Benchmark: 40-60%
  
Contacted → Engaged
  Formula: (Leads Engaged / Leads Contacted) × 100
  Benchmark: 20-35%
  
Engaged → Qualified
  Formula: (Leads Qualified / Leads Engaged) × 100
  Benchmark: 40-60%
  
Qualified → Proposal
  Formula: (Proposals Sent / Leads Qualified) × 100
  Benchmark: 50-70%
  
Proposal → Closed Won
  Formula: (Deals Won / Proposals Sent) × 100
  Benchmark: 20-40%
  
Overall Lead → Won
  Formula: (Deals Won / Total Leads) × 100
  Benchmark: 2-8%
```

### 2. Source Attribution Analysis
```
For each lead source:
  - Lead volume by source
  - Conversion rate by source
  - Average deal size by source
  - Time-to-close by source
  - Cost-per-lead by source (if available)
  
Compare sources:
  - LinkedIn vs Email vs Referral vs Inbound
  - Identify highest-ROI channels
  - Reallocate resources to top performers
```

### 3. Bottleneck Identification
```
Find the weakest conversion stage:
  - Stage with lowest conversion rate
  - Stage with longest average time
  - Stage with highest drop-off volume
  
Root cause analysis:
  - Message-market fit issues
  - Timing problems
  - Qualification criteria too loose/tight
  - Process friction
  - Competitive losses
```

### 4. Trend Analysis
```
Track over time (weekly/monthly):
  - Overall conversion rate trend
  - Stage-specific conversion trends
  - Activity-to-conversion correlation
  - Seasonal patterns
  
Identify:
  - Improving stages (double down)
  - Declining stages (investigate)
  - Stable stages (optimize for lift)
```

### 5. Optimization Recommendations
```
For each bottleneck:
  1. Diagnose root cause
  2. Propose specific fix
  3. Estimate expected impact
  4. Define measurement plan
  
Priority matrix:
  - High Impact + Low Effort: Do first
  - High Impact + High Effort: Plan carefully
  - Low Impact + Low Effort: Quick wins
  - Low Impact + High Effort: Skip or defer
```

## Example Execution
```
Input: 90 days of LEAD-TRACKER.csv data, 200 leads

Analysis:
  Lead → Contacted: 45% (90/200) - Benchmark: 40-60% ✓
  Contacted → Engaged: 22% (20/90) - Benchmark: 20-35% ✓
  Engaged → Qualified: 55% (11/20) - Benchmark: 40-60% ✓
  Qualified → Proposal: 64% (7/11) - Benchmark: 50-70% ✓
  Proposal → Won: 43% (3/7) - Benchmark: 20-40% ✓
  
  Overall: 1.5% (3/200) - Below benchmark (2-8%)

  Source Analysis:
    LinkedIn: 40% contact rate, 3.2% overall conversion
    Email: 35% contact rate, 1.8% overall conversion
    Referral: 80% contact rate, 8.5% overall conversion

  Bottleneck: Contacted → Engaged (22% is low end of benchmark)
    Root cause: Generic follow-up messaging
    Fix: Personalize Touch 2 with specific pain points
    Expected impact: +10% engagement rate = +2 more qualified leads/month
```

## Validation Checks
- [ ] Conversion rates calculated from actual data (not estimates)
- [ ] Sample sizes noted (small samples = unreliable rates)
- [ ] Benchmarks are relevant to industry/company stage
- [ ] Recommendations are specific and measurable
- [ ] Trends are statistically significant (not noise)

## Tools Needed
| Tool | Purpose |
|------|---------|
| filesystem_read_file | Read historical CSV data |
| filesystem_write_file | Save analysis report |

## Conversion Dashboard Template
```markdown
## Conversion Funnel - [Period]

[LEAD] ──45%──> [CONTACTED] ──22%──> [ENGAGED] ──55%──> [QUALIFIED]
                                                           │
                                                        64%
                                                           │
                                                    [PROPOSAL]
                                                           │
                                                        43%
                                                           │
                                                    [CLOSED WON]

Bottleneck: Contacted → Engaged (22%)
Recommended Action: Personalize follow-up messages
Expected Impact: +10% engagement rate
```

## Optimization Playbook
```yaml
low_engagement:
  symptoms: "Contacted → Engaged < 20%"
  fixes:
    - "Improve subject lines (test curiosity vs direct)"
    - "Personalize opening with specific research"
    - "Share relevant content in Touch 2"
    - "Try LinkedIn instead of email"
  
low_qualified:
  symptoms: "Engaged → Qualified < 30%"
  fixes:
    - "Tighten ICP criteria in lead-finder"
    - "Add qualification questions in Discovery call"
    - "Score leads more aggressively"
  
low_close_rate:
  symptoms: "Proposal → Won < 20%"
  fixes:
    - "Improve demo quality"
    - "Address objections earlier in process"
    - "Offer pilot/trial programs"
    - "Involve executive sponsor"
```

## Integration Notes
- Data sourced from lead-tracker.md and pipeline-manager.md
- Insights inform email-sequence.md A/B testing priorities
- Source analysis guides lead-finder.md channel allocation
- Optimization recommendations feed weekly-pipeline.md priorities
