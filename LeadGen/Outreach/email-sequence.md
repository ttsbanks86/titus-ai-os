# Email Sequence Builder

## Purpose
Create personalized, multi-touch email sequences that nurture leads from first contact through qualification and meeting booking.

## Required Inputs
- Target lead segment (from lead-scorer.md)
- Value proposition and key messages
- Sequence length (3-7 touches default)
- Timing between touches (2-5 business days)

## Expected Outputs
- Complete email sequence (subject + body for each touch)
- Personalization tokens for each lead
- Send schedule based on lead engagement
- A/B test variants for key emails

## Step-by-Step Workflow

### 1. Define Sequence Strategy
```
Sequence Types:
  - Cold Outreach: New lead, no prior relationship
  - Warm Follow-Up: Lead engaged but hasn't converted
  - Re-engagement: Dormant lead, bring back
  - Post-Demo: After demo, move toward close
  - Nurture: Long-term value building
```

### 2. Build Email Framework
```
Touch 1 (Day 0): Introduction
  - Personalized hook (research-based)
  - Value proposition (1 sentence)
  - Low-friction CTA (question, not meeting ask)
  
Touch 2 (Day 3): Value Add
  - Share relevant insight or content
  - Reference their specific situation
  - Soft CTA (resource, not ask)
  
Touch 3 (Day 7): Social Proof
  - Case study or result from similar company
  - Quantified outcome
  - CTA: "Would this work for [Company]?"
  
Touch 4 (Day 12): Direct Ask
  - Clear, specific meeting request
  - Time options provided
  - CTA: Calendar link or "reply with time"
  
Touch 5 (Day 18): Breakup (Optional)
  - Acknowledge they're busy
  - Offer to reconnect later
  - Final CTA: "Worth a 15-min chat?"
```

### 3. Personalization Engine
```
For each lead, personalize:
  - First name
  - Company name
  - Specific pain point (from research)
  - Relevant case study (by industry/size)
  - Mutual connection (if any)
  - Recent company news (if applicable)
  
Tokens:
  {{first_name}} - Contact first name
  {{company}} - Company name
  {{pain_point}} - Specific challenge identified
  {{case_study}} - Most relevant success story
  {{mutual_connection}} - LinkedIn mutual connection
  {{recent_news}} - Latest company development
```

### 4. A/B Testing Framework
```
Test one variable at a time:
  - Subject lines (curiosity vs. direct vs. question)
  - Opening lines (personalized vs. generic)
  - CTA type (question vs. meeting vs. resource)
  - Send time (morning vs. afternoon)
  - Email length (short vs. detailed)
  
Measure:
  - Open rate (subject line effectiveness)
  - Reply rate (message resonance)
  - Meeting book rate (CTA effectiveness)
```

### 5. Send Schedule Optimization
```
Best Practices:
  - Tuesday-Thursday for B2B
  - 8-10am or 2-4pm recipient time
  - Minimum 2 business days between touches
  - Pause sequence if lead replies
  - Skip touch if lead opens but doesn't reply (adjust timing)
```

## Example Execution
```
Input: Cold outreach to VPs of Sales at 50-200 employee SaaS companies

Touch 1 (Tuesday 9am):
Subject: Quick question about {{company}}'s sales process
Body:
Hi {{first_name}},

I noticed {{company}} recently raised Series B - congrats on the growth.

Quick question: as you scale the sales team, how are you handling {{pain_point}}?

We've helped companies like {{case_study}} solve this exact challenge.

Worth a 15-minute chat to see if we could help {{company}} too?

Best,
[Your name]

Touch 2 (Friday 9am):
Subject: Re: Quick question about {{company}}'s sales process
Body:
Hi {{first_name}},

Thought you might find this useful - we just published a case study on how {{case_study}} reduced their {{metric}} by 40%.

[Link to case study]

Happy to walk through how they did it if that's useful for {{company}}.

[Your name]

[Continue sequence...]
```

## Validation Checks
- [ ] Every email has personalized elements (not generic)
- [ ] Subject lines are under 50 characters
- [ ] CTAs are clear and single-action
- [ ] Sequence timing respects recipient timezone
- [ ] No more than 5 touches without response
- [ ] All links tracked and working

## Tools Needed
| Tool | Purpose |
|------|---------|
| filesystem_write_file | Save email templates |
| linkedin_get_person_profile | Research for personalization |
| linkedin_get_company_profile | Company intelligence for hooks |

## Sequence Template Library
```yaml
cold_outreach:
  name: "Cold Outreach - VPS Sales"
  touches: 5
  timing: [0, 3, 7, 12, 18]
  goal: Book discovery call
  
warm_followup:
  name: "Warm Follow-Up - Engaged Lead"
  touches: 3
  timing: [0, 2, 5]
  goal: Book demo
  
post_demo:
  name: "Post-Demo Follow-Up"
  touches: 3
  timing: [0, 2, 5]
  goal: Close deal
  
nurture:
  name: "Long-Term Nurture"
  touches: 6
  timing: [0, 7, 21, 45, 90, 180]
  goal: Stay top of mind
```

## Integration Notes
- Personalization data from lead-enrichment.md
- Lead scores from lead-scorer.md determine sequence type
- Engagement tracking updates lead-tracker.md status
- Successful replies trigger pipeline-manager.md updates
