# Lead Finder

## Purpose
Discover and list potential lead companies and contacts matching your Ideal Customer Profile (ICP).

## Required Inputs
- ICP definition (industry, size, geography, tech stack, funding stage)
- Source channels to search (LinkedIn, Crunchbase, directories, job boards)
- Maximum leads to find per run (default: 50)

## Expected Outputs
- List of qualified companies with key data points
- Primary contact info per company (name, title, email, LinkedIn)
- Initial qualification score
- Source attribution for each lead

## Step-by-Step Workflow

### 1. Define ICP Parameters
```
ICP Template:
  Industry: [vertical]
  Company Size: [employees] OR [revenue range]
  Geography: [region]
  Tech Stack: [tools they use]
  Funding Stage: [pre-seed/seed/Series A+]
  Pain Signals: [specific problems they have]
  Disqualification: [who NOT to target]
```

### 2. Multi-Channel Search
```
Channel 1 - LinkedIn:
  - linkedin_search_companies with ICP filters
  - linkedin_search_people for decision-makers
  
Channel 2 - Web:
  - firecrawl_search "[ICP keywords] companies"
  - firecrawl_search "[industry] startup funding 2026"
  
Channel 3 - Directories:
  - firecrawl_scrape G2/Capterra category pages
  - firecrawl_scrape Crunchbase lists
  
Channel 4 - Job Boards:
  - firecrawl_search "site:indeed.com [role] [industry]"
  - Hiring signals indicate growth and budget
```

### 3. Data Enrichment
For each discovered company:
```
  - Company size and revenue estimate
  - Key decision-makers (CEO, VP Sales, Head of Ops)
  - Contact info (email patterns, LinkedIn profiles)
  - Recent activity (funding, hiring, product launches)
  - Tech stack indicators
```

### 4. Initial Qualification
Score each lead (1-10):
```
  ICP Fit (0-3): How closely they match ideal profile
  Timing (0-3): Are they in a buying window?
  Accessibility (0-2): Can we reach decision-makers?
  Potential (0-2): Deal size and expansion potential
```

### 5. Build Lead List
Export qualified leads to CSV format:
```
Company, Contact, Title, Email, Phone, Source, Score, ICP_Fit, Notes
Acme Corp, Jane Smith, VP Sales, jane@acme.com, 555-0101, LinkedIn, 8, High, Series B, hiring AEs
```

## Example Execution
```
Input: ICP="B2B SaaS, 50-200 employees, US, Series A+, uses Salesforce"

Execution:
1. LinkedIn search "B2B SaaS Series A Salesforce" → 30 companies
2. Crunchbase search "SaaS Series A 2025 2026" → 25 companies
3. Cross-reference, deduplicate → 40 unique companies
4. Enrich top 20 with contact info
5. Score each, filter score >= 6

Output:
- 15 qualified leads (avg score 7.2)
- 8 with verified email addresses
- 5 with direct LinkedIn connections
- 2 with active hiring signals
```

## Validation Checks
- [ ] Each lead has company name and at least one contact
- [ ] Contact info verified (email format valid, LinkedIn profile exists)
- [ ] ICP score is justified with specific data points
- [ ] No duplicates across company names
- [ ] Leads exported to LEAD-TRACKER.csv

## Tools Needed
| Tool | Purpose |
|------|---------|
| linkedin_search_companies | Find target companies |
| linkedin_search_people | Find decision-makers |
| firecrawl_search | Web-based lead discovery |
| firecrawl_scrape | Directory and listing scraping |
| perplexity_perplexity_search | Company research and validation |
| linkedin_get_company_profile | Deep company research |

## ICP Scoring Rubric
| Score | ICP Fit | Timing | Accessibility | Potential |
|-------|---------|--------|---------------|-----------|
| 3 | Perfect match | Active pain signal | Direct connection | Enterprise deal |
| 2 | Strong match | Budget cycle aligns | Mutual connection | Mid-market deal |
| 1 | Partial match | Neutral timing | Cold outreach | SMB deal |
| 0 | Poor match | Bad timing | No path in | Low value |

## Integration Notes
- Run 2-3x per week to maintain lead flow
- Feeds leads into `lead-scorer.md` for deeper qualification
- Qualified leads go to `lead-tracker.md` for pipeline tracking
- Source data from `market-scanner.md` and `trend-analyzer.md`
