# Competitor Intelligence

## Purpose
Analyze competitors' positioning, pricing, messaging, and customer base to identify differentiation opportunities and find leads they're missing.

## Required Inputs
- List of 3-10 direct competitors (names or URLs)
- Your product/service description
- Target customer profile

## Expected Outputs
- Competitor profiles with strengths/weaknesses
- Pricing comparison matrix
- Gap analysis (what they don't serve well)
- List of 10-20 companies using competitors (potential switch leads)

## Step-by-Step Workflow

### 1. Competitor Website Analysis
```
For each competitor:
  - Scrape homepage for positioning and messaging
  - Extract pricing page details
  - Identify key features and differentiators
  - Note target audience claims
```

### 2. Customer Evidence Collection
Use firecrawl_search to find:
- Competitor customer reviews (G2, Capterra, TrustRadius)
- Case studies on their website
- Social proof mentions
- Community/forum complaints (Reddit, HN, Twitter)

### 3. Gap Identification
```
Compare competitor offerings against your value prop:
  - Features they lack
  - Segments they underserve
  - Price points they miss
  - Support/UX complaints from their users
```

### 4. Lead Signal Extraction
From competitor research, identify:
- Companies actively searching for alternatives (Reddit/forum posts)
- Companies using competitor tools (job postings for that tool, tech stack data)
- Companies that recently churned from competitors (review mentions)

### 5. Build Intelligence Brief
```
For each competitor:
  - Profile: What they do, who they serve
  - Strengths: Why customers choose them
  - Weaknesses: Where they fall short
  - Pricing: Their model and key price points
  - Customers: Named customers or estimated count
  - Switch Leads: Companies likely open to switching
```

## Example Execution
```
Input: Competitor="Acme CRM", Your product="Nimble CRM for startups"

Execution:
1. Scrape acmecrm.com → positioning: "Enterprise CRM for Fortune 500"
2. Scrape G2 reviews → 450 reviews, avg 4.2/5
3. Top complaints: "too complex for small teams", "expensive", "slow onboarding"
4. Search "Acme CRM alternative" → 15 discussion threads
5. Identify 20 companies complaining about Acme's pricing

Output:
- Acme CRM weakness: Pricing starts at $99/user/month, no startup tier
- Gap opportunity: Companies with 5-20 seats priced out
- Switch leads: 12 companies actively looking for alternatives
```

## Validation Checks
- [ ] Each competitor has pricing data (even estimated)
- [ ] At least 3 weaknesses identified per competitor
- [ ] Switch leads have verifiable intent signals
- [ ] Gaps directly map to your product strengths
- [ ] No outdated data (check publish dates)

## Tools Needed
| Tool | Purpose |
|------|---------|
| firecrawl_scrape | Competitor website analysis |
| firecrawl_search | Find reviews, discussions, customer evidence |
| perplexity_perplexity_search | Quick competitor fact-checking |
| linkedin_search_companies | Find companies using competitor tools |
| linkedin_get_company_profile | Deep-dive on competitor positioning |

## Output Template
```markdown
## Competitor: [Name]
- **Website:** [URL]
- **Positioning:** [One-liner]
- **Target Market:** [Who they sell to]
- **Pricing:** [Model + key tiers]
- **Strengths:** [Top 3]
- **Weaknesses:** [Top 3]
- **Customers:** [Named examples or count]
- **Switch Leads:** [Companies showing intent to switch]
```
