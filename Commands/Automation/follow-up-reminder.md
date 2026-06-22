# Follow-up Reminder System

## Purpose
Track follow-up dates for all leads and generate timely reminders to prevent opportunities from falling through the cracks.

## Trigger
- **Primary**: Daily at 9:00 AM (scheduled)
- **Secondary**: On-demand via OpenCode command

## Input Sources
- `C:\Users\tbank\Desktop\Live Cowork\CRM\LEAD-TRACKER.csv` — All leads with follow-up dates
- Current date/time

## Output Destinations
- `output/follow-up-reminders-{date}.md` — Daily reminder list
- Desktop notification (if Hot leads overdue)
- Optional: Gmail draft for follow-up messages

## Step-by-Step Workflow

```
1. READ
   └─ Parse LEAD-TRACKER.csv
   └─ Extract: company_name, contact_name, contact_email,
      status, priority, next_follow_up, last_contacted,
      outreach_status, score

2. IDENTIFY OVERDUE FOLLOW-UPS
   └─ Filter: next_follow_up <= current_date AND status != "Closed"
   └─ Sort by priority (Hot first, then Warm, then Cold)
   └─ Categorize:
      - Overdue (> 1 day past due)
      - Due Today (due date = today)
      - Due This Week (due within 7 days)

3. CHECK ACTIVITY RECENCY
   └─ For each lead: days_since_last_contact = current_date - last_contacted
   └─ Flag "Stale" if > 14 days since last contact
   └─ Flag "At Risk" if > 30 days since last contact

4. GENERATE REMINDER LIST
   └─ Create markdown report with sections:
      - 🔴 OVERDUE (action needed today)
      - 🟡 DUE THIS WEEK
      - 🟢 ON TRACK
      - ⚠️ AT RISK (no contact in 30+ days)

5. GENERATE FOLLOW-UP MESSAGES
   └─ For overdue leads, draft follow-up email:
      - Reference last touchpoint
      - Reference any recent news
      - Include value-add or resource
      - Low-friction CTA
   └─ Save drafts to output/follow-up-drafts-{date}.md

6. SEND NOTIFICATIONS
   └─ If Hot leads are overdue: desktop notification
   └─ Save reminder list to output/follow-up-reminders-{date}.md
   └─ Log execution to output/workflow-log.md
```

## Priority Classification

| Priority | Criteria | Reminder Frequency |
|----------|----------|-------------------|
| Hot | Score ≥ 75 | Daily if overdue |
| Warm | Score 40-74 | Every 2 days if overdue |
| Cold | Score < 39 | Weekly if overdue |

## Follow-up Sequence Rules

| Status | Follow-up Cadence |
|--------|-------------------|
| New Lead | Contact within 24h of first outreach |
| Engaged | Follow up every 3-4 days |
| Proposal Sent | Follow up every 5-7 days |
| Negotiating | Follow up every 2-3 days |
| Stalled | Check-in every 14 days |
| Nurturing | Monthly value-add touch |

## Step-by-Step Workflow (Detailed)

```
Step 1: READ
  └─ Load LEAD-TRACKER.csv
  └─ Load today's date
  └─ Parse all rows into lead objects

Step 2: CLASSIFY
  For each lead:
    ├─ Is status in ["Closed", "Lost"]? → SKIP
    ├─ Is next_follow_up empty? → SKIP (no follow-up scheduled)
    ├─ Calculate days_until_follow_up
    │   └─ negative = overdue, 0 = today, positive = future
    ├─ Calculate days_since_last_contact
    └─ Assign urgency: Overdue | Due Today | This Week | On Track

Step 3: PRIORITIZE
  └─ Sort by: priority (Hot > Warm > Cold), then days_until_follow_up (most overdue first)
  └─ Deduplicate: one entry per lead (latest follow-up date)

Step 4: REPORT
  └─ Generate markdown with sections and lead summaries
  └─ For each overdue lead:
      ├─ Include: company, contact, days overdue, last contact date
      ├─ Include: score, priority, outreach status
      └─ Include: suggested action (email/LinkedIn/phone)

Step 5: DRAFT MESSAGES
  For overdue leads:
    └─ Generate follow-up email using templates:
        ├─ "Checking in" template
        ├─ "Sharing value" template (article/resource)
        ├─ "New angle" template (different pain point)
        └─ "Final outreach" template (last attempt)

Step 6: DELIVER
  └─ Save reminder list to output/follow-up-reminders-{date}.md
  └─ Save message drafts to output/follow-up-drafts-{date}.md
  └─ If any Hot leads overdue: trigger desktop notification
  └─ Log summary to output/workflow-log.md
```

## MCP Tools Required
| Tool | Purpose |
|------|---------|
| `csv_read` / `csv_write` | Read LEAD-TRACKER.csv |
| `file_write` | Save reminder list and drafts |
| `bash` | Desktop notification (PowerShell toast) |

## Example Execution

**Daily reminder output:**
```markdown
# Follow-up Reminders — 2026-06-07

## 🔴 OVERDUE
| Lead | Contact | Priority | Days Overdue | Last Contact | Action |
|------|---------|----------|-------------|--------------|--------|
| Acme Corp | Jane Doe | Hot | 3 days | 2026-06-01 | Email follow-up |
| Beta Inc | Bob Lee | Warm | 1 day | 2026-06-04 | LinkedIn message |

## 🟡 DUE THIS WEEK
| Lead | Contact | Priority | Due Date | Action |
|------|---------|----------|----------|--------|
| Gamma Co | Alice Smith | Hot | 2026-06-09 | Send proposal |

## ⚠️ AT RISK (30+ days no contact)
| Lead | Contact | Priority | Days Stale | Last Contact |
|------|---------|----------|-----------|--------------|
| Delta LLC | Carol White | Warm | 45 days | 2026-04-23 |
```

## Error Handling
- **Empty CSV**: Log warning, skip execution
- **No follow-ups due**: Log "All caught up", skip notifications
- **Malformed date**: Skip that lead, log error, continue with others
- **Duplicate leads**: Deduplicate by email, keep most recent

## Validation Checks
- [ ] Reminder list contains all overdue leads
- [ ] Leads sorted by priority (Hot first)
- [ ] No duplicate entries for same lead
- [ ] Follow-up drafts reference correct contact name
- [ ] Date calculations are accurate (no off-by-one errors)
- [ ] Closed/Lost leads are excluded
- [ ] At-risk leads (30+ days) are flagged
