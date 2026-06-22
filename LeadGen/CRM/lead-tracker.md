# Lead Tracker

## Purpose
Maintain a single source of truth for all leads, their status, interactions, and next actions throughout the sales process.

## Required Inputs
- New lead records (from lead-finder.md or manual entry)
- Status updates from team
- Interaction logs (emails, calls, meetings)
- Lead score updates (from lead-scorer.md)

## Expected Outputs
- Updated LEAD-TRACKER.csv with current status
- Leads requiring immediate action
- Overdue follow-up alerts
- Pipeline health summary

## Step-by-Step Workflow

### 1. Add New Leads
```
When new lead identified:
  1. Check for duplicates in existing tracker
  2. If new: Add row with all known fields
  3. If exists: Update with new information, don't duplicate
  
New Lead Record:
  Company, Contact, Email, Phone, Source, Status, 
  Score, LastContact, NextAction, Notes
```

### 2. Status Management
```
Status Values (use consistently):
  - NEW: Just added, not yet contacted
  - CONTACTED: Initial outreach sent
  - ENGAGED: Lead responded or showed interest
  - QUALIFIED: Meets all criteria, ready for sales
  - PROPOSAL: Proposal or demo delivered
  - NEGOTIATION: In active deal discussions
  - CLOSED_WON: Deal closed successfully
  - CLOSED_LOST: Deal lost (with reason)
  - NURTURE: Not ready now, keep warm
  - DISQUALIFIED: Doesn't fit ICP (with reason)
```

### 3. Interaction Logging
```
For each interaction:
  1. Update LastContact date
  2. Log interaction type in Notes
  3. Set NextAction based on interaction
  4. Update Status if changed
  
Format: [DATE] [TYPE] [SUMMARY]
Example: [2026-06-01] [EMAIL] Sent intro, requested demo call
```

### 4. Action Queue Management
```
Daily Review:
  1. Sort leads by NextAction date
  2. Flag overdue actions (NextAction < today)
  3. List today's planned actions
  4. List upcoming actions (next 7 days)
  
Action Types:
  - CALL: Phone call scheduled
  - EMAIL: Email to send
  - LINKEDIN: LinkedIn message to send
  - DEMO: Demo to schedule/conduct
  - FOLLOWUP: General follow-up
  - MEETING: In-person or virtual meeting
```

### 5. Reporting
```
Weekly Metrics:
  - Total leads in pipeline
  - New leads added this week
  - Leads moved to next stage
  - Leads closed (won/lost)
  - Average time in each stage
  - Conversion rate by source
```

## Example Execution
```
Input: New lead "Acme Corp" from lead-finder.md

Tracker Update:
  Company: Acme Corp
  Contact: Jane Smith
  Email: jane@acme.com
  Phone: 555-0101
  Source: LinkedIn
  Status: NEW
  Score: 8
  LastContact: (empty)
  NextAction: 2026-06-08 - Send intro email
  Notes: Series B, hiring AEs, uses Salesforce

After outreach:
  Status: CONTACTED
  LastContact: 2026-06-08
  NextAction: 2026-06-11 - Follow up if no response
  Notes: [2026-06-08] [EMAIL] Sent personalized intro, mentioned their SF migration

After response:
  Status: ENGAGED
  LastContact: 2026-06-09
  NextAction: 2026-06-10 - Schedule demo call
  Notes: [2026-06-09] [EMAIL] Replied interested in demo, available Thursday 2pm
```

## Validation Checks
- [ ] No duplicate companies in tracker
- [ ] Every lead has a NextAction assigned
- [ ] Status values are consistent (no custom values)
- [ ] LastContact dates are accurate
- [ ] Overdue leads flagged and reviewed

## Tools Needed
| Tool | Purpose |
|------|---------|
| filesystem_read_file | Read current LEAD-TRACKER.csv |
| filesystem_edit_file | Update lead records |
| filesystem_write_file | Save updated tracker |

## LEAD-TRACKER.csv Schema
```csv
Company,Contact,Email,Phone,Source,Status,Score,LastContact,NextAction,Notes
Acme Corp,Jane Smith,jane@acme.com,555-0101,LinkedIn,NEW,8,,2026-06-08 - Send intro,"Series B, hiring AEs"
Beta Inc,Bob Jones,bob@beta.com,555-0102,Crunchbase,CONTACTED,7,2026-06-05,2026-06-08 - Follow up,"[2026-06-05] [EMAIL] Sent intro"
```

## Automation Rules
```
Auto-actions:
  - When Score changes → Update LEAD-TRACKER.csv Score field
  - When Status = CLOSED_LOST → Move to archive, remove from active view
  - When NextAction is today → Add to daily action queue
  - When LastContact > 14 days → Flag for follow-up check
```

## Integration Notes
- Central hub connecting all LeadGen components
- Receives leads from lead-finder.md and lead-scorer.md
- Triggers outreach via email-sequence.md
- Feeds data to Reports/weekly-pipeline.md
- Updates shared with team via pipeline-manager.md
