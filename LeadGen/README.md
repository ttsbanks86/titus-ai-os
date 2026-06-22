# LeadGen System

A complete AI-powered lead generation subsystem for identifying, qualifying, tracking, and converting B2B leads through a structured sales pipeline.

## System Overview

LeadGen provides end-to-end lead management across five modules:

```
┌─────────────┐    ┌──────────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐
│  Research    │───>│ Prospecting  │───>│   CRM   │───>│ Outreach │───>│ Reports │
│ (Find)       │    │ (Qualify)    │    │ (Track) │    │ (Convert)│    │ (Analyze)│
└─────────────┘    └──────────────┘    └─────────┘    └──────────┘    └─────────┘
```

## Quick Start

### 1. Initial Setup
```bash
# Navigate to LeadGen directory
cd "C:\Users\tbank\Desktop\Live Cowork\LeadGen"

# Verify structure
ls -R
```

### 2. Define Your ICP (Ideal Customer Profile)
Edit the ICP parameters in `Prospecting/lead-finder.md`:
```yaml
ICP:
  Industry: "Your target industry"
  Company Size: "50-200 employees"
  Geography: "US"
  Funding Stage: "Series A+"
  Tech Stack: "Salesforce, HubSpot"
```

### 3. Run Your First Lead Generation Cycle
```
Step 1: Research
  → Run Research/market-scanner.md
  → Run Research/competitor-intel.md
  
Step 2: Prospect
  → Run Prospecting/lead-finder.md
  → Run Prospecting/lead-scorer.md
  → Run Prospecting/enrichment.md
  
Step 3: Track
  → Add leads to LEAD-TRACKER.csv
  → Add deals to PIPELINE.csv
  
Step 4: Outreach
  → Run Outreach/email-sequence.md
  → Run Outreach/linkedin-outreach.md
  
Step 5: Follow Up
  → Run Outreach/follow-up.md daily
  
Step 6: Report
  → Run Reports/weekly-pipeline.md weekly
  → Run Reports/conversion-report.md monthly
```

## Module Reference

### Research Module
| Command | Purpose | Frequency |
|---------|---------|-----------|
| `market-scanner.md` | Identify market opportunities | Weekly |
| `competitor-intel.md` | Analyze competitor gaps | Bi-weekly |
| `trend-analyzer.md` | Spot buying signals | Bi-weekly |

### Prospecting Module
| Command | Purpose | Frequency |
|---------|---------|-----------|
| `lead-finder.md` | Discover new leads | 2-3x/week |
| `lead-scorer.md` | Score and prioritize | After each find |
| `enrichment.md` | Deep-dive lead data | For qualified leads |

### CRM Module
| Command | Purpose | Frequency |
|---------|---------|-----------|
| `lead-tracker.md` | Manage lead records | Daily |
| `pipeline-manager.md` | Forecast and analyze | Weekly |

### Outreach Module
| Command | Purpose | Frequency |
|---------|---------|-----------|
| `email-sequence.md` | Build email campaigns | As needed |
| `linkedin-outreach.md` | LinkedIn engagement | Daily |
| `follow-up.md` | Systematic follow-ups | Daily |

### Reports Module
| Command | Purpose | Frequency |
|---------|---------|-----------|
| `weekly-pipeline.md` | Pipeline health report | Weekly (Friday) |
| `conversion-report.md` | Conversion analysis | Monthly |

## Required API Keys & Setup

### Essential (Day 1)
| Service | Purpose | Setup |
|---------|---------|-------|
| LinkedIn (via MCP) | Lead research, outreach | LinkedIn MCP server configured |
| Firecrawl | Web research, scraping | FIRECRAWL_API_KEY in .env |
| Perplexity | Quick research | PERPLEXITY_API_KEY in .env |

### Recommended (Week 1)
| Service | Purpose | Setup |
|---------|---------|-------|
| Crunchbase | Funding data | Manual research or API |
| G2/Capterra | Competitor reviews | firecrawl_scrape |

### Optional (Scale)
| Service | Purpose | Setup |
|---------|---------|-------|
| Apollo.io | Contact enrichment | API key |
| Clearbit | Company data | API key |
| Hunter.io | Email verification | API key |

## Integration with OpenCode

LeadGen is designed to work seamlessly with OpenCode agents:

### Agent Roles
```
exec-ceo:      Strategic lead prioritization, deal decisions
exec-cmo:      Outreach messaging, content strategy
exec-coo:      Process optimization, workflow efficiency
engineer:      Technical integrations, API connections
research:      Market intelligence, competitor analysis
```

### Running Commands
```bash
# In OpenCode, reference the LeadGen files directly:
# Example: "Run the market scanner for AI SaaS companies"
# Example: "Score the new leads in LEAD-TRACKER.csv"
# Example: "Generate this week's pipeline report"
```

### MCP Server Integration
The following MCP servers enhance LeadGen capabilities:
- **LinkedIn MCP**: Profile research, messaging, connection requests
- **Firecrawl MCP**: Web scraping, search, content extraction
- **Perplexity MCP**: Quick research and fact-checking

## CSV Templates

### LEAD-TRACKER.csv
Tracks individual leads through the pipeline:
```csv
Company,Contact,Email,Phone,Source,Status,Score,LastContact,NextAction,Notes
Acme Corp,Jane Smith,jane@acme.com,555-0101,LinkedIn,NEW,8,,2026-06-08 - Send intro,"Series B, hiring"
```

### PIPELINE.csv
Manages active deals and forecasting:
```csv
DealName,Company,Value,Stage,CloseDate,Probability,Owner,Notes
Enterprise License,Acme Corp,120000,Negotiation,2026-07-15,60%,Titus,"Legal review"
```

## Workflow Automation

### Daily Routine (15 minutes)
1. Check overdue actions in lead-tracker.md
2. Send follow-ups from follow-up.md queue
3. Respond to LinkedIn messages
4. Update lead statuses

### Weekly Routine (1 hour)
1. Generate weekly-pipeline.md report
2. Run lead-finder.md for new prospects
3. Score and enrich new leads
4. Review pipeline-manager.md for stalled deals

### Monthly Routine (2 hours)
1. Run conversion-report.md analysis
2. Update competitor-intel.md
3. Refresh trend-analyzer.md
4. Optimize email-sequence.md based on data

## Metrics to Track

### Leading Indicators
- Leads generated per week
- Outreach sent per week
- Response rate
- Meeting book rate

### Lagging Indicators
- Pipeline value
- Win rate
- Average deal size
- Sales cycle length

### Source Metrics
- Conversion rate by channel
- Cost per lead by channel
- Time to close by channel

## Tips for Success

1. **Start Small**: Focus on one industry vertical first
2. **Be Consistent**: Daily outreach beats weekly bursts
3. **Personalize Everything**: Generic messages don't work
4. **Track religiously**: Data drives optimization
5. **Follow up**: 80% of sales require 5+ follow-ups
6. **Learn from losses**: Track why deals are lost

## File Maintenance

- **LEAD-TRACKER.csv**: Update after every interaction
- **PIPELINE.csv**: Update weekly at minimum
- **All .md files**: Review and customize for your business
- **Reports**: Archive monthly, track trends quarterly

## Support

For issues with the LeadGen system:
1. Check the specific .md file's Validation Checks section
2. Review the Tools Needed for MCP server status
3. Verify API keys in .env are valid
4. Check LEAD-TRACKER.csv for data consistency
