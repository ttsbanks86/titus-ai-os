# Automation Layer

## Purpose
Automates lead management, research, scoring, outreach, and reporting workflows. Reduces manual effort and ensures consistent, timely follow-up.

## Architecture
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Trigger     │────▶│   AI Agent   │────▶│    Output     │
│  (CSV/Time)  │     │ (Research)   │     │ (Update CSV)  │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Workflows

| Workflow | Trigger | File |
|----------|---------|------|
| Lead Research | New lead added | `lead-research-workflow.md` |
| Prospect Scoring | Lead updated | `prospect-scoring.md` |
| Outreach Generation | Ready for outreach | `outreach-generator.md` |
| Follow-up Reminders | Daily 9am / on-demand | `follow-up-reminder.md` |
| Weekly Reports | Friday 5pm / on-demand | `weekly-report-gen.md` |

## Data Flow
```
LEAD-TRACKER.csv
  ├── lead-research-workflow (enriches)
  ├── prospect-scoring (scores)
  ├── outreach-generator (generates messages)
  ├── follow-up-reminder (tracks dates)
  └── weekly-report-gen (aggregates)
```

## Shared Dependencies
- **CSV File**: `C:\Users\tbank\Desktop\Live Cowork\CRM\LEAD-TRACKER.csv`
- **Output Directory**: `C:\Users\tbank\Desktop\Live Cowork\Commands\Automation\output\`
- **Templates**: `C:\Users\tbank\Desktop\Live Cowork\Commands\Templates\`
- **MCP Tools**: Firecrawl, LinkedIn, Apollo, Gmail

## n8n Integration
All workflows can be implemented as n8n sub-workflows or triggered via OpenCode CLI commands. Use `workflow-orchestration` skill for chaining.

## Error Handling
- All workflows validate CSV structure before processing
- Failed enrichment attempts are logged, not retried
- Hot lead alerts always succeed even if scoring partially fails
- Weekly reports fall back to previous week if current data is empty
