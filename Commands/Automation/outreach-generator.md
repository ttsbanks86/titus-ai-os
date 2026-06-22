# Outreach Generator

## Purpose
Generate personalized outreach messages (email and LinkedIn) based on lead research, company news, and identified pain points.

## Trigger
- **Primary**: Lead reaches "Ready for Outreach" status in `LEAD-TRACKER.csv`
- **Secondary**: On-demand via OpenCode command

## Input Sources
- `C:\Users\tbank\Desktop\Live Cowork\CRM\LEAD-TRACKER.csv` — Lead profile + enriched data
- `C:\Users\tbank\Desktop\Live Cowork\Commands\Templates\outreach-templates.json` — Message templates
- Firecrawl web search — Recent company news (last 7 days)
- LinkedIn profiles — Contact context

## Output Destinations
- `output/outreach-{company}-{date}.md` — Generated outreach messages
- `output/outreach-sequence-{company}.md` — Full follow-up sequence
- `C:\Users\tbank\Desktop\Live Cowork\CRM\LEAD-TRACKER.csv` — Update outreach status

## Step-by-Step Workflow

```
1. READ
   └─ Parse LEAD-TRACKER.csv for lead with status = "Ready for Outreach"
   └─ Load outreach-templates.json
   └─ Extract: company_name, contact_name, contact_title, industry,
      company_size, pain_points, recent_news, enrichment notes

2. NEWS RESEARCH
   └─ Firecrawl search: "{company_name} news last 7 days"
   └─ Firecrawl search: "{company_name} {industry} challenges 2026"
   └─ Extract: recent announcements, funding, product launches, pain points

3. PAIN POINT IDENTIFICATION
   └─ Map industry → common challenges
   └─ Map company size → scaling problems
   └─ Map title → role-specific concerns
   └─ Map recent news → timeliness hooks
   └─ Prioritize top 3 pain points for messaging

4. GENERATE EMAIL
   └─ Select base template from outreach-templates.json
   └─ Personalize:
      - Subject line (include company name or news hook)
      - Opening (reference specific pain point or news)
      - Value proposition (map to identified pain points)
      - Call to action (low-friction, e.g., "quick chat")
   └─ Keep under 150 words
   └─ Tone: professional, concise, value-first

5. GENERATE LINKEDIN MESSAGE
   └─ Shorter format (under 100 words)
   └─ More conversational tone
   └─ Reference mutual connections if available
   └─ Include soft CTA (e.g., "Would love to connect")

6. CREATE FOLLOW-UP SEQUENCE
   └─ Day 1: Initial outreach (email)
   └─ Day 2: LinkedIn connection request + note
   └─ Day 4: Follow-up email (different angle)
   └─ Day 7: Value-add share (article/resource)
   └─ Day 14: Final check-in

7. SAVE & UPDATE
   └─ Save messages to outreach-{company}-{date}.md
   └─ Save sequence to outreach-sequence-{company}.md
   └─ Update LEAD-TRACKER.csv: outreach_status = "Generated"
   └─ Update LEAD-TRACKER.csv: next_action = "Send Initial Outreach"
```

## MCP Tools Required
| Tool | Purpose |
|------|---------|
| `csv_read` / `csv_write` | Read/update LEAD-TRACKER.csv |
| `firecrawl_firecrawl_search` | Recent company news |
| `firecrawl_firecrawl_extract` | Extract structured news data |
| `linkedin_get_company_profile` | Company context |
| `file_read` | Load outreach templates |

## Message Templates Structure

```json
{
  "templates": [
    {
      "id": "saas-vp-engagement",
      "name": "SaaS VP Engagement",
      "industry": ["SaaS", "Technology"],
      "title": ["VP", "Director", "C-suite"],
      "subject": "{{company_name}} + {{pain_point}}",
      "body": "Hi {{contact_name}},\n\nI noticed {{company_name}} recently {{news_hook}}. This often means {{pain_point}} becomes a priority.\n\nWe've helped similar companies like {{reference_company}} solve this by {{value_prop}}.\n\nWould you be open to a 15-minute chat to explore if this could work for {{company_name}}?\n\nBest,\n{{sender_name}}",
      "linkedin_note": "Hi {{contact_name}} — saw {{news_hook}} at {{company_name}}. We've helped similar teams with {{pain_point}}. Would love to connect and share some insights."
    }
  ]
}
```

## Example Execution

**Input:**
```
Company: Acme Corp
Contact: Jane Doe, VP Engineering
Pain points: Scaling engineering team, managing remote developers
Recent news: Series B funding ($20M) in March 2026
```

**Generated email:**
```
Subject: Acme Corp + Engineering Scaling After Series B

Hi Jane,

Congratulations on Acme Corp's Series B! With $20M to deploy, scaling your
engineering team is likely top of mind.

We've helped companies like Notion and Linear manage rapid engineering growth
by streamlining developer onboarding and reducing time-to-productivity by 40%.

Would you be open to a 15-minute chat to explore how this could work for
Acme Corp's expansion?

Best,
Titus
```

## Error Handling
- **No news found**: Use industry-level pain points instead of news hooks
- **Template mismatch**: Fall back to generic value-first template
- **Missing contact info**: Flag for manual outreach, skip generation
- **Sequence overlap**: Check if outreach already generated today, skip duplicate

## Validation Checks
- [ ] Email is under 150 words
- [ ] LinkedIn message is under 100 words
- [ ] Contact name is correctly personalized (no placeholders)
- [ ] Subject line contains company name or news hook
- [ ] CTA is specific and low-friction
- [ ] No grammar errors or typos
- [ ] Outreach sequence has at least 3 touchpoints
- [ ] CSV status updated to "Generated"
