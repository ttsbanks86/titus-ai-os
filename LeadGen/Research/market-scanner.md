# Market Scanner

## Purpose
Scan target markets to identify new business opportunities, emerging niches, and underserved segments for lead generation.

## Required Inputs
- Target industry vertical (e.g., "SaaS", "E-commerce", "Healthcare Tech")
- Geographic focus (e.g., "US", "UK", "DACH region")
- Company size filter (e.g., "50-500 employees", "$10M-$100M revenue")
- Budget range for targeting (optional)

## Expected Outputs
- List of 20-50 qualified market segments
- Opportunity size estimates per segment
- Competitive density score (low/medium/high)
- Recommended top 10 segments to target

## Step-by-Step Workflow

### 1. Define Search Parameters
```
Set industry = [target_industry]
Set geography = [target_region]
Set company_size = [employee_count_range]
Set revenue_range = [revenue_bracket]
```

### 2. Market Data Collection
Use firecrawl_search to gather:
- Industry reports (IBISWorld, Statista, Gartner)
- Recent funding rounds in the vertical (Crunchbase, PitchBook data)
- Job posting trends (Indeed, LinkedIn job data signals growth)
- Conference attendee lists (events.signal.com, Luma)

### 3. Segment Identification
For each potential segment:
- Count total addressable market (TAM) companies
- Assess willingness-to-pay signals (recent funding, job posts for sales roles)
- Evaluate competitive landscape density
- Score segment attractiveness (1-10)

### 4. Opportunity Mapping
```
For each segment:
  - Calculate: Segment Score = (TAM_size × Funding_activity × Low_competition) / Market_saturation
  - Rank segments by score
  - Flag top 10 for immediate prospecting
```

### 5. Generate Report
Output a structured markdown report with:
- Executive summary
- Top 10 segments ranked
- Key signals per segment
- Recommended next actions

## Example Execution
```
Input: Industry="AI/ML SaaS", Geography="US", Size="20-200 employees"

Execution:
1. Search "AI SaaS companies Series A funding 2025 2026" → 15 results
2. Search "machine learning startups hiring sales" → 12 results
3. Search "AI SaaS market size growth forecast" → 8 results
4. Cross-reference findings, identify 8 distinct segments
5. Score each segment, rank top 3

Output:
- Segment 1: AI-powered customer support tools (Score: 9.2)
  - TAM: ~450 companies
  - Signal: 23 recent funding rounds, 180+ sales job posts
- Segment 2: AI compliance automation (Score: 8.7)
  - TAM: ~200 companies
  - Signal: 11 funding rounds, regulatory tailwinds
- [etc.]
```

## Validation Checks
- [ ] Results include at least 5 distinct market segments
- [ ] Each segment has supporting data points (not guessed)
- [ ] Competitive density is assessed with real competitor count
- [ ] Top segments align with company's ICP (Ideal Customer Profile)
- [ ] No duplicate companies across segments

## Tools Needed
| Tool | Purpose |
|------|---------|
| firecrawl_search | Web research for market data |
| firecrawl_scrape | Deep-dive on specific reports |
| perplexity_perplexity_search | Quick market size validation |
| linkedin_search_companies | Verify company counts in segments |
| yahoo-finance_get_company_info | Financial data on public comps |

## Integration Notes
- Run weekly to keep market map current
- Output feeds into `lead-finder.md` for actual prospecting
- Share top segments with team via Reports/weekly-pipeline.md
