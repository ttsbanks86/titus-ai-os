# LinkedIn Outreach

## Purpose
Execute targeted LinkedIn outreach campaigns to connect with decision-makers, build relationships, and generate qualified meetings.

## Required Inputs
- Target lead list with LinkedIn profiles
- Connection request message template
- Follow-up message sequence
- Content strategy for warming leads

## Expected Outputs
- Connection requests sent (with tracking)
- Message sequences for each lead type
- Response tracking and engagement metrics
- Meeting conversion data

## Step-by-Step Workflow

### 1. LinkedIn Profile Preparation
```
Before outreach, ensure your profile:
  - Has professional headshot
  - Clear headline (value proposition, not job title)
  - About section speaks to target audience
  - Recent activity shows engagement
  - Recommendations from relevant people
```

### 2. Connection Request Strategy
```
Personalization Levels:

Level 1 - Basic (30 second research):
  "Hi {{first_name}}, I see we're both in {{industry}}. Would love to connect."
  
Level 2 - Specific (2 minute research):
  "Hi {{first_name}}, congrats on {{recent_achievement}} at {{company}}. 
   I work with similar companies on {{topic}}. Let's connect."
  
Level 3 - Deep (5 minute research):
  "Hi {{first_name}}, I noticed {{company}} is {{specific_signal}}.
   We helped {{similar_company}} with the same challenge.
   Would love to share what worked for them."
  
Best Practice: Always use Level 2 or 3 when possible
```

### 3. Post-Connection Follow-Up
```
Day 0 (Same day as connection accepted):
  - Thank them for connecting
  - Brief value statement
  - Ask a question (don't sell)
  
Day 3-5:
  - Share relevant content (article, case study)
  - Reference their specific situation
  - No ask, pure value
  
Day 7-10:
  - Direct ask for meeting/call
  - Clear agenda and time options
  - Make it easy to say yes
```

### 4. Content Warming Strategy
```
Before direct outreach:
  1. Engage with their posts (like, comment thoughtfully)
  2. Share content relevant to their challenges
  3. Tag them in relevant discussions (sparingly)
  4. Send connection request after 2-3 interactions
  
This "warms" the lead before you message them directly.
```

### 5. Message Templates by Scenario
```
Scenario 1: Cold Connection
  Connection: "Hi [Name], I work with [industry] companies on [topic]. 
              Would love to connect and share insights."
  Follow-up 1: "Thanks for connecting! Quick question - how is [company] 
                handling [pain point]?"
  Follow-up 2: "We just helped [similar company] solve that exact challenge.
                Mind if I share what worked?"

Scenario 2: Mutual Connection
  Connection: "Hi [Name], I see we're both connected to [mutual]. 
              I work with [industry] companies on [topic]. Let's connect!"
  Follow-up: "[Mutual] mentioned you might be interested in [topic]. 
              Would love to share what we've learned."

Scenario 3: Post-Event
  Connection: "Hi [Name], great [talk/post] at [event]. 
              I agree with your point about [topic]. Let's connect!"
  Follow-up: "Your point about [topic] really resonated. 
              We're seeing the same trend with our clients."
```

## Example Execution
```
Input: 10 VPs of Sales at Series B SaaS companies

Execution:
1. Research each profile (5 min each, 50 min total)
2. Engage with 2 posts from each (like + comment)
3. Send personalized connection requests
4. Track accept rate and response rate
5. Follow up with accepted connections

Results:
  - 10 connection requests sent
  - 7 accepted (70% accept rate)
  - 4 replied to follow-up (57% reply rate)
  - 2 meetings booked (29% meeting rate)
```

## Validation Checks
- [ ] All connection requests personalized (no generic templates)
- [ ] Follow-ups reference specific research, not templates
- [ ] Response time under 24 hours for replies
- [ ] No more than 20 connection requests per day (LinkedIn limits)
- [ ] All conversations logged in lead-tracker.md

## Tools Needed
| Tool | Purpose |
|------|---------|
| linkedin_connect_with_person | Send connection requests |
| linkedin_send_message | Send follow-up messages |
| linkedin_get_person_profile | Research before outreach |
| linkedin_get_company_profile | Company intelligence |
| linkedin_search_people | Find additional contacts |

## LinkedIn Limits and Best Practices
```
Daily Limits (avoid account restriction):
  - Connection requests: 20-25/day (new accounts: 10-15)
  - Messages to non-connections: 50/day
  - Profile views: 80-100/day
  - Post engagements: 50/day

Timing:
  - Send during business hours (8am-6pm recipient time)
  - Space messages 2-3 minutes apart
  - Don't send on weekends
  - Take 1-2 days off per week from outreach
```

## Performance Tracking
```csv
Name,ConnectionSent,ConnectionAccepted,FollowUpSent,Replied,MeetingBooked
Jane Smith,2026-06-01,2026-06-02,2026-06-02,2026-06-04,2026-06-05
Bob Jones,2026-06-01,2026-06-01,2026-06-02,,
```

## Integration Notes
- Research from lead-enrichment.md for personalization
- Lead scores from lead-scorer.md determine outreach priority
- All interactions logged to lead-tracker.md
- Meetings created feed into pipeline-manager.md
