# Follow-Up Automation

## Purpose
Systematically follow up with leads who haven't responded, ensuring no opportunity falls through the cracks and maximizing response rates.

## Required Inputs
- Leads with overdue NextAction dates
- Leads with no response after initial outreach
- Follow-up templates by scenario
- Timing rules for follow-up frequency

## Expected Outputs
- Prioritized follow-up queue
- Personalized follow-up messages
- Updated lead statuses and next actions
- Follow-up effectiveness metrics

## Step-by-Step Workflow

### 1. Identify Follow-Up Candidates
```
Daily Scan:
  1. Leads where NextAction date has passed
  2. Leads with Status=CONTACTED but no response >3 days
  3. Leads with Status=ENGAGED but no response >7 days
  4. Leads in NEGOTIATION with stalled progress
  
Sort by:
  - Lead Score (highest first)
  - Days since last contact (longest first)
  - Deal value (largest first)
```

### 2. Categorize Follow-Up Type
```
Type 1: No Response
  - Initial outreach sent, no reply
  - Follow-up approach: Add value, don't just "checking in"
  
Type 2: Engaged but Stalled
  - Lead showed interest, then went quiet
  - Follow-up approach: Re-engage with new angle
  
Type 3: Proposal Sent
  - Demo/proposal delivered, waiting for decision
  - Follow-up approach: Address objections, create urgency
  
Type 4: Negotiation Stuck
  - Deal in negotiation but not progressing
  - Follow-up approach: Remove blockers, escalate
```

### 3. Generate Follow-Up Messages
```
Template: No Response (Touch 2)
Subject: Re: [Original Subject]
Body:
Hi {{first_name}},

Wanted to follow up on my note about {{topic}}.

I found this [relevant resource] that might be helpful for {{company}}:
[Link]

Would a quick 15-minute call be useful to discuss how this applies to your situation?

Template: No Response (Touch 3 - Breakup)
Subject: Should I close your file?
Body:
Hi {{first_name}},

I've reached out a few times about {{topic}} and haven't heard back.

I completely understand if the timing isn't right. Should I close your file for now, 
or is this something worth revisiting in a few months?

Template: Engaged but Stalled
Body:
Hi {{last_name}},

I know things can get busy. Last we spoke, you were interested in {{topic}}.

Has anything changed on your end? Happy to pick up where we left off 
if the timing still works.

Template: Proposal Sent
Body:
Hi {{first_name}},

Following up on the proposal we sent over. Any questions or concerns I can address?

I know {{company}} is evaluating options, so happy to jump on a quick call 
to walk through any specifics.
```

### 4. Execute Follow-Ups
```
For each lead in queue:
  1. Select appropriate template
  2. Personalize with latest research/news
  3. Send via appropriate channel (email/LinkedIn)
  4. Update LastContact date
  5. Set new NextAction based on expected response time
  6. Log interaction in Notes
```

### 5. Track Follow-Up Effectiveness
```
Metrics to Track:
  - Response rate by follow-up number (1st, 2nd, 3rd)
  - Response rate by channel (email vs LinkedIn)
  - Meeting book rate from follow-ups
  - Time-to-response after follow-up
  - Breakup email response rate (often highest!)
```

## Example Execution
```
Input: 12 overdue leads, 8 with no response >3 days

Execution:
Lead 1: Acme Corp (Score: 8, No response 5 days)
  - Type: No Response (Touch 2)
  - Action: Send value-add email with relevant case study
  - NextAction: 2026-06-11 - Breakup email if no response

Lead 2: Beta Inc (Score: 7, Engaged then silent 10 days)
  - Type: Engaged but Stalled
  - Action: LinkedIn message with new industry insight
  - NextAction: 2026-06-09 - Check for response

Results after 1 week:
  - 12 follow-ups sent
  - 5 replies (42% response rate)
  - 3 meetings booked (25% meeting rate)
  - 2 breakup emails sent, 1 replied
```

## Validation Checks
- [ ] Every overdue lead has follow-up scheduled
- [ ] Follow-ups are personalized (not copy-paste)
- [ ] Timing respects lead's preferred channel
- [ ] No lead followed up with more than 3 times without response
- [ ] Breakup email sent as final touch (not endless follow-up)

## Tools Needed
| Tool | Purpose |
|------|---------|
| filesystem_read_file | Read LEAD-TRACKER.csv for overdue leads |
| filesystem_edit_file | Update lead records after follow-up |
| linkedin_send_message | LinkedIn follow-ups |
| linkedin_get_person_profile | Re-research before follow-up |

## Follow-Up Rules
```yaml
rules:
  no_response:
    touches: 3
    timing: [0, 3, 7]
    channels: [email, linkedin, email]
    final_action: "Breakup email, then nurture"
  
  engaged_stalled:
    touches: 2
    timing: [0, 5]
    channels: [email, linkedin]
    final_action: "Schedule call or move to nurture"
  
  proposal_sent:
    touches: 3
    timing: [0, 3, 7]
    channels: [email, phone, email]
    final_action: "Escalate or close lost"
  
  negotiation_stuck:
    touches: 2
    timing: [0, 3]
    channels: [phone, email]
    final_action: "Executive sponsor outreach"
```

## Integration Notes
- Pulls overdue leads from lead-tracker.md
- Updates lead status and next actions after each follow-up
- Metrics feed into Reports/conversion-report.md
- Successful responses update pipeline-manager.md
