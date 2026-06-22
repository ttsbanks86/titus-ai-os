# Trend Analyzer

## Purpose
Identify emerging market trends, buying signals, and seasonal patterns that create lead generation windows.

## Required Inputs
- Industry vertical(s)
- Time horizon (30/60/90 days)
- Signal types to monitor (funding, hiring, tech adoption, regulatory)

## Expected Outputs
- Top 5-10 active trends with lead generation implications
- Buying signal calendar (when leads are most receptive)
- Trend-to-action mapping (which trends create which types of leads)

## Step-by-Step Workflow

### 1. Trend Discovery
```
Search for recent developments:
  - "[Industry] trends 2026"
  - "[Technology] adoption rate [industry]"
  - "[Regulation] impact on [industry]"
  - "[Funding category] investment 2026"
```

### 2. Signal Classification
Categorize each trend by signal type:
- **Funding signals:** New rounds, IPOs, acquisitions
- **Hiring signals:** Sales team expansion, new C-suite
- **Tech signals:** New tool adoption, migration projects
- **Regulatory signals:** Compliance deadlines, new requirements
- **Seasonal signals:** Budget cycles, fiscal year ends

### 3. Lead Implication Analysis
```
For each trend:
  - Who benefits? (potential leads)
  - Who is disrupted? (leads needing solutions)
  - What timing? (when to reach out)
  - What messaging? (angle to use)
```

### 4. Buying Window Mapping
Create a calendar of optimal outreach windows:
- Q1: Annual planning, new budgets
- Q2: Mid-year reviews, pain point reassessment
- Q3: Pre-fiscal-year prep (for Jan FY companies)
- Q4: Budget flush, year-end renewals

### 5. Generate Trend Brief
Compile actionable intelligence:
- Trend description and evidence
- Lead generation opportunity
- Recommended action and timing
- Supporting data sources

## Example Execution
```
Input: Industry="Fintech", Horizon="Q2 2026"

Execution:
1. Search "fintech trends 2026" → AI-powered fraud detection trending
2. Search "B2B fintech funding Q1 2026" → $2.1B invested, up 34%
3. Search "fintech compliance changes 2026" → New AML regulations effective July
4. Analyze implications for each trend
5. Map to lead gen opportunities

Output:
- Trend 1: AI Fraud Detection (High Impact)
  - Signal: 15 fintechs raised Series A for this in Q1
  - Leads: Companies implementing AI fraud need integration partners
  - Timing: Now through July (before regulation hits)
  - Message: "Ready for the July AML deadline?"

- Trend 2: Open Banking Expansion (Medium Impact)
  - Signal: PSD3 discussions advancing in EU
  - Leads: Banks needing API integration
  - Timing: 6-12 month horizon
  - Message: "Future-proof your open banking stack"
```

## Validation Checks
- [ ] Trends backed by at least 3 data sources
- [ ] Lead implications are specific and actionable
- [ ] Timing recommendations include concrete dates
- [ ] No stale trends (all from last 90 days)
- [ ] Each trend maps to a reachable audience

## Tools Needed
| Tool | Purpose |
|------|---------|
| firecrawl_search | Trend discovery and data collection |
| perplexity_perplexity_search | Quick trend validation |
| websearch | Real-time trend checking |
| linkedin_search_companies | Find companies affected by trends |
| yahoo-finance_get_news | Industry news and signals |

## Trend Tracking Template
```markdown
| Trend | Signal Strength | Lead Type | Best Outreach Window | Message Angle |
|-------|----------------|-----------|---------------------|---------------|
| AI Fraud Detection | High | Integration partners | Now - July | Compliance readiness |
| Open Banking PSD3 | Medium | Banks, fintechs | Q3-Q4 | Future-proofing |
| [Trend] | [H/M/L] | [Type] | [Window] | [Angle] |
```

## Integration Notes
- Run bi-weekly to catch emerging trends early
- Feeds into `market-scanner.md` for segment prioritization
- Update `email-sequence.md` with trend-based messaging angles
- Share quarterly trend reports with sales team
