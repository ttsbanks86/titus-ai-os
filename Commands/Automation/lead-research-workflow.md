# Lead Research Workflow

## Purpose
Automatically research and enrich lead data from multiple sources when a new lead is added to the CRM.

## Trigger
- **Primary**: New row added to `LEAD-TRACKER.csv`
- **Secondary**: On-demand via OpenCode command or n8n webhook

## Input Sources
- `C:\Users\tbank\Desktop\Live Cowork\CRM\LEAD-TRACKER.csv` — Lead record
- Firecrawl web search — Company information
- Apollo API — Decision-maker discovery
- LinkedIn profiles — Professional context

## Output Destinations
- Updated `LEAD-TRACKER.csv` — Enriched fields (company size, industry, revenue, tech stack, key contacts)
- `output/research-{company}-{date}.md` — Detailed research brief

## Step-by-Step Workflow

```
1. READ
   └─ Parse LEAD-TRACKER.csv
   └─ Find row where status = "New" or enrichment = "Pending"
   └─ Extract: company_name, domain, contact_name, contact_email

2. COMPANY RESEARCH (Firecrawl)
   └─ Search: "{company_name} company info"
   └─ Scrape company website for about page, team page
   └─ Extract: industry, employee_count, revenue, headquarters, founded
   └─ Search: "{company_name} recent news" (last 30 days)

3. DECISION-MAKER DISCOVERY (Apollo/LinkedIn)
   └─ Search Apollo for contacts at company
   └─ Filter by title: VP, Director, Manager, C-suite
   └─ For top 3 contacts: get name, title, LinkedIn URL, email

4. CONTACT ENRICHMENT
   └─ Validate email format
   └─ Check LinkedIn profile for additional context
   └─ Identify: current role, tenure, education, mutual connections

5. UPDATE CSV
   └─ Write enriched fields to LEAD-TRACKER.csv
   └─ Set enrichment_status = "Complete"
   └─ Set last_researched = current_date

6. GENERATE RESEARCH BRIEF
   └─ Compile findings into markdown brief
   └─ Save to output/research-{company}-{date}.md
   └─ Include: company overview, key contacts, recent news, opportunities
```

## MCP Tools Required
| Tool | Purpose |
|------|---------|
| `firecrawl_firecrawl_search` | Web search for company info |
| `firecrawl_firecrawl_scrape` | Scrape company website pages |
| `firecrawl_firecrawl_extract` | Extract structured company data |
| `linkedin_search_people` | Find decision-makers at company |
| `linkedin_get_company_profile` | Get company LinkedIn data |
| `csv_read` / `csv_write` | Read/update LEAD-TRACKER.csv |

## Example Execution

**Input CSV row:**
```csv
company_name,domain,contact_name,contact_email,status,enrichment
Acme Corp,acme.com,John Smith,john@acme.com,New,Pending
```

**Research brief output:**
```markdown
# Acme Corp Research Brief
**Date**: 2026-06-07
**Industry**: SaaS / Project Management
**Employees**: 50-200
**Revenue**: $10M-$50M
**HQ**: San Francisco, CA

## Recent News
- Series B funding ($20M) announced March 2026
- Launched new AI feature in Q1 2026

## Key Decision Makers
1. Jane Doe — VP Engineering (jane@acme.com)
2. Bob Lee — Director of Product (bob@acme.com)

## Opportunities
- Expanding engineering team (hiring signals)
- Recently adopted new CRM (budget available)
```

## Error Handling
- **Website not found**: Skip company research, proceed with LinkedIn data only
- **Apollo rate limit**: Log error, retry after 60s, max 3 retries
- **LinkedIn profile private**: Skip, note as "Profile not accessible"
- **Invalid domain**: Flag for manual review, set enrichment = "Failed"

## Validation Checks
- [ ] Company name is not empty
- [ ] At least one decision-maker found
- [ ] Email format is valid (contains @ and domain)
- [ ] CSV update preserves existing non-empty fields
- [ ] Research brief contains at least company overview section
