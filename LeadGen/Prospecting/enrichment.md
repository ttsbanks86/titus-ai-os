# Lead Enrichment

## Purpose
Enhance basic lead records with deeper intelligence: verified contacts, company details, tech stack, intent signals, and organizational charts.

## Required Inputs
- Basic lead list (company name + primary contact at minimum)
- Enrichment fields to populate (configurable)
- Data quality requirements (verification level)

## Expected Outputs
- Enriched lead records with 15+ data fields
- Verified email addresses and phone numbers
- Organizational context (reporting structure, team size)
- Technology and vendor landscape
- Intent and readiness signals

## Step-by-Step Workflow

### 1. Define Enrichment Schema
```
Core Fields (always enrich):
  - Verified work email
  - Direct phone number
  - LinkedIn profile URL
  - Job title and seniority level
  - Company LinkedIn URL

Company Fields:
  - Employee count (exact)
  - Annual revenue estimate
  - Founded year
  - Funding total and last round
  - Industry and sub-industry
  - Headquarters location

Technology Fields:
  - Current CRM system
  - Current marketing automation
  - Cloud provider (AWS/GCP/Azure)
  - Key SaaS tools in stack

Intent Fields:
  - Recent job postings (signal of need)
  - Technology changes (new tools = budget)
  - Content consumption (what they're researching)
  - Social mentions (pain points expressed)
```

### 2. Multi-Source Enrichment
```
For each lead:
  Source 1 - LinkedIn:
    - Get company profile → employee count, industry, description
    - Get contact profile → title, tenure, connections
    
  Source 2 - Web:
    - firecrawl_scrape company website → about page, team page
    - firecrawl_search "[company] funding" → financial data
    - firecrawl_search "[company] reviews" → employee/customer sentiment
    
  Source 3 - Directories:
    - firecrawl_scrape Crunchbase → funding, investors, key people
    - firecrawl_scrape G2/Capterra → product reviews and alternatives
```

### 3. Contact Verification
```
For each contact:
  1. Verify email format: [first].[last]@[domain]
  2. Check MX records for domain validity
  3. Verify LinkedIn profile exists and is current
  4. Cross-reference title across sources
  5. Flag unverified data points
```

### 4. Intent Signal Analysis
```
Look for buying signals:
  - Job postings for roles your product serves
  - Tech stack changes (migration indicators)
  - Competitor mentions in reviews/forums
  - Executive mentions of pain points on social
  - Content downloads or webinar attendance
```

### 5. Build Enriched Record
```
For each lead:
  - Merge all enriched data into unified record
  - Calculate data confidence score (% verified)
  - Flag missing critical fields
  - Output in structured format
```

## Example Execution
```
Input: Basic lead="Acme Corp, John Smith, CEO"

Enrichment:
  LinkedIn: John Smith, CEO at Acme Corp, 2 years tenure
  Email: john.smith@acme.com (verified, MX valid)
  Phone: +1-555-0123 (from company website)
  Company: 180 employees, $25M revenue, Series B
  Tech: Salesforce, HubSpot, AWS
  Intent: Posted 3 sales roles (growing team), mentioned "scaling challenges" on LinkedIn

Output: Enriched record with 18/20 fields populated, 90% confidence
```

## Validation Checks
- [ ] Email addresses verified (MX check or pattern match)
- [ ] LinkedIn profiles exist and are current (within 6 months)
- [ ] Company data matches across at least 2 sources
- [ ] No placeholder or fake data in enriched fields
- [ ] Data confidence score calculated and >70% for qualified leads

## Tools Needed
| Tool | Purpose |
|------|---------|
| linkedin_get_company_profile | Company intelligence |
| linkedin_get_person_profile | Contact verification |
| linkedin_search_people | Find additional contacts |
| firecrawl_scrape | Website data extraction |
| firecrawl_search | Cross-reference verification |
| perplexity_perplexity_search | Quick fact-checking |

## Enrichment Quality Levels
| Level | Fields | Verification | Use Case |
|-------|--------|--------------|----------|
| Basic | 5-8 fields | Pattern match only | Initial screening |
| Standard | 12-15 fields | 1 source verified | Priority outreach |
| Premium | 18-20 fields | Multi-source verified | Enterprise deals |

## Batch Processing
For large lead lists (50+):
```
1. Group leads by enrichment level needed
2. Process Standard level first (80/20 rule)
3. Only Premium enrich Tier 1 leads
4. Queue Basic leads for nurture
5. Run enrichment in batches of 10 to avoid rate limits
```

## Integration Notes
- Run after lead-scorer.md identifies qualified leads
- Enriched data updates lead scores in LEAD-TRACKER.csv
- Intent signals feed into outreach timing (email-sequence.md)
- Tech stack data enables product-specific messaging
