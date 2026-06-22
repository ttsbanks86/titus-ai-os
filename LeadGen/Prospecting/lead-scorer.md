# Lead Scorer

## Purpose
Apply consistent, data-driven scoring to qualify leads and prioritize outreach efforts on highest-probability opportunities.

## Required Inputs
- Raw lead list from lead-finder.md
- Scoring criteria weights (customizable)
- Threshold for "qualified" status (default: 6/10)

## Expected Outputs
- Scored lead list with detailed breakdown
- Prioritized outreach queue (top 20% highlighted)
- Disqualified leads with reasons
- Updated LEAD-TRACKER.csv with scores

## Step-by-Step Workflow

### 1. Load Scoring Framework
```
Default Scoring Model (100 points total):

Demographics (30 pts):
  - Industry match: 0-10
  - Company size fit: 0-10
  - Geography match: 0-10

Behavioral (30 pts):
  - Recent funding: 0-10
  - Active hiring: 0-10
  - Tech stack alignment: 0-10

Engagement (20 pts):
  - Website visits: 0-5
  - Content downloads: 0-5
  - Social engagement: 0-5
  - Email opens: 0-5

Fit (20 pts):
  - Decision-maker access: 0-10
  - Budget indicators: 0-10
```

### 2. Data Collection Per Lead
```
For each lead:
  1. Verify company data (size, industry, location)
  2. Check funding history (Crunchbase, news)
  3. Review hiring activity (LinkedIn, job boards)
  4. Assess tech stack (BuiltWith, job postings)
  5. Look for engagement signals (your site, content)
```

### 3. Score Calculation
```
For each lead:
  demographic_score = industry_match + size_fit + geo_match
  behavioral_score = funding + hiring + tech_alignment
  engagement_score = visits + downloads + social + email
  fit_score = decision_maker_access + budget_indicators
  
  total_score = (demographic_score + behavioral_score + engagement_score + fit_score) / 100 × 10
  
  qualification = total_score >= threshold ? "Qualified" : "Nurture"
```

### 4. Priority Ranking
```
Sort leads by total_score descending
Group into tiers:
  Tier 1 (8-10): Immediate outreach
  Tier 2 (6-7):  Priority queue
  Tier 3 (4-5):  Nurture sequence
  Tier 4 (1-3):  Disqualified / Archive
```

### 5. Output Results
```
For each lead:
  - Company, Contact, Score, Tier
  - Score breakdown (which categories drove the score)
  - Recommended action (call, email, LinkedIn, nurture)
  - Notes on scoring rationale
```

## Example Execution
```
Input: 25 leads from lead-finder.md, threshold=6

Execution:
Lead 1: Acme Corp
  - Industry: SaaS (10/10), Size: 150 emp (8/10), Geo: US (10/10) = 28
  - Funding: Series B 3mo ago (9/10), Hiring: 12 roles (8/10), Tech: Salesforce (7/10) = 24
  - Engagement: Visited pricing page (4/5), Downloaded ebook (3/5) = 7
  - Access: VP Sales on LinkedIn (8/10), Series B = budget (9/10) = 17
  - Total: 76/100 = 7.6 → Tier 2

Lead 2: Beta Inc
  - All categories low, Total: 32/100 = 3.2 → Tier 4 (Disqualified)

Output:
- 8 Tier 1 leads (immediate action)
- 10 Tier 2 leads (priority queue)
- 5 Tier 3 leads (nurture)
- 2 Tier 4 leads (archived)
```

## Validation Checks
- [ ] Every scored lead has rationale documented
- [ ] Scoring is consistent across similar lead profiles
- [ ] Top 20% of leads have clear next actions
- [ ] Disqualified leads have specific reasons noted
- [ ] Scores updated in LEAD-TRACKER.csv

## Tools Needed
| Tool | Purpose |
|------|---------|
| linkedin_get_company_profile | Company data verification |
| linkedin_get_person_profile | Contact verification |
| firecrawl_search | Funding and news verification |
| yahoo-finance_get_company_info | Financial data for larger companies |
| perplexity_perplexity_search | Quick company research |

## Scoring Configuration
Adjust weights based on your business:
```yaml
scoring_model:
  demographics:
    weight: 30
    factors:
      industry_match: 10
      company_size: 10
      geography: 10
  behavioral:
    weight: 30
    factors:
      recent_funding: 10
      active_hiring: 10
      tech_alignment: 10
  engagement:
    weight: 20
    factors:
      website_visits: 5
      content_downloads: 5
      social_engagement: 5
      email_engagement: 5
  fit:
    weight: 20
    factors:
      decision_maker_access: 10
      budget_indicators: 10
  qualified_threshold: 6
```

## Integration Notes
- Run after each lead-finder.md execution
- Results feed into lead-tracker.md for pipeline management
- Top-tier leads trigger immediate outreach (email-sequence.md)
- Nurture leads enter automated sequences
