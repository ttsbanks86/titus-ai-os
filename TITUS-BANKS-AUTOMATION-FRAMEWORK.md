# Titus Banks Automation Framework
### 4 automation chains that run the business while you sleep.

**Last updated:** 2026-06-05
**Tool:** n8n (self-hosted, free) + MailerLite (email) + Notion (CRM) + GitHub (code)
**Principle:** Automate the repeatable. Keep the relational manual.

---

## The 4 Automation Chains

### Chain 1: Content Pipeline

**Trigger:** Monday 8:00 AM Pacific
**Goal:** 3 posts per week (Mon/Wed/Fri) + 1 Friday newsletter
**Agents involved:** Content Director → Script Writer → Thumbnail Designer → Publishing Agent → Social Media Manager

```
TRIGGER: Monday 8:00 AM
    ↓
[Script Writer] Draft post #1 (educational carousel)
    ↓
[Thumbnail Designer] Design 7-slide carousel
    ↓
[Content Director] Review and approve
    ↓
[Publishing Agent] Schedule for Mon 8:30 AM
    ↓
[Social Media Manager] Monitor engagement, reply within 24 hrs
    ↓
TRIGGER: Wednesday 8:00 AM
    ↓
[Script Writer] Draft post #2 (story or insight)
    ↓
[Content Director] Review and approve
    ↓
[Publishing Agent] Schedule for Wed 8:30 AM
    ↓
[Social Media Manager] Monitor engagement, reply within 24 hrs
    ↓
TRIGGER: Friday 8:00 AM
    ↓
[Script Writer] Draft post #3 (practical / framework)
    ↓
[Content Director] Review and approve
    ↓
[Publishing Agent] Schedule for Fri 8:30 AM
    ↓
[Email Specialist] Send weekly newsletter (A/B/C rotation)
    ↓
[Social Media Manager] Monitor engagement, reply within 24 hrs
    ↓
TRIGGER: Friday 3:00 PM
    ↓
[Analytics Agent] Pull weekly metrics (impressions, engagement, clicks)
    ↓
[Content Director] Weekly content review
    ↓
[CEO] Friday 20-min review
```

**Automation tools:**
- MailerLite: Newsletter scheduling and delivery
- n8n: Content pipeline orchestration (optional, can be manual for now)
- Notion: Content calendar, post tracker
- LinkedIn/Instagram native schedulers: Post scheduling

**Time saved:** ~3 hours per week (vs. manual content creation and posting)

---

### Chain 2: Lead Capture and Conversion

**Trigger:** Form submission on Gap Audit landing page
**Goal:** Convert subscribers into calls, calls into engagements
**Agents involved:** Marketing → Email Specialist → CMO → CEO

```
TRIGGER: Form submitted (Gap Audit)
    ↓
[MailerLite] Apply tags: gap-audit, stage-{{stage}}
    ↓
[MailerLite] Send Email 1 (Welcome) — immediate
    ↓
[MailerLite] Wait 2 days
    ↓
[MailerLite] Send Email 2 (Day 2 check-in)
    ↓
[MailerLite] Wait 3 days
    ↓
[MailerLite] Send Email 3 (Day 5 call invite)
    ↓
[MailerLite] Wait 9 days
    ↓
[MailerLite] Send Email 4 (Day 14 story)
    ↓
[MailerLite] Wait 16 days
    ↓
[MailerLite] Send Email 5 (Day 30 nurture)
    ↓
[MailerLite] Enter Friday newsletter rotation (A/B/C weekly)
    ↓
IF subscriber replies:
    ↓
[CEO] Personal reply within 24 hours
    ↓
IF subscriber books a call:
    ↓
[CEO] 30-minute call
    ↓
[CEO] Decision: close / follow-up / nurture
    ↓
IF closed:
    ↓
[COO] Onboard new client
    ↓
[Business Analyst] Deliver Gap Audit report
    ↓
[Knowledge Manager] Log to claude-mem and Notion CRM
```

**Automation tools:**
- MailerLite: 5-email automation + weekly newsletter
- Calendly: Booking and calendar management
- Notion: CRM (lead tracking, deal stages)
- claude-mem: Conversation logging

**Time saved:** ~5 hours per week (vs. manual email follow-up and CRM updates)

---

### Chain 3: Operations and Infrastructure

**Trigger:** Weekly Saturday 9:00 AM + event-based
**Goal:** Keep infrastructure healthy, automations running, costs tracked
**Agents involved:** COO → Workflow Designer → SOP Writer → Knowledge Manager

```
TRIGGER: Saturday 9:00 AM
    ↓
[CTO] Infrastructure health check
    ├── Sites up? (Netlify status)
    ├── Automations running? (MailerLite status)
    ├── Costs within budget? (subscription check)
    └── Security clear? (no alerts)
    ↓
[Cost Tracker] Log weekly costs to Notion
    ↓
[Budget Analyst] Compare actual vs. budget
    ↓
IF costs > budget + 15%:
    ↓
[CFO] → CEO: escalation
    ↓
[Workflow Designer] Identify 1 automation improvement
    ↓
[Automation Agent] Implement improvement
    ↓
[SOP Writer] Document the improvement
    ↓
[Knowledge Manager] Update Obsidian knowledge base
```

**Event-based triggers:**
- New tool subscription → CFO approval → CTO implements → SOP Writer documents
- System outage → CTO restores → CTO logs incident → SOP Writer updates runbook
- Security alert → CTO investigates → CTO reports to CEO → Faith and Mission reviews if data involved

**Automation tools:**
- n8n: Scheduled health checks, cost monitoring
- Notion: Incident log, cost tracking
- GitHub: Code backups, deployment logs
- Obsidian: Knowledge base updates

**Time saved:** ~2 hours per week (vs. manual monitoring and documentation)

---

### Chain 4: Product Development

**Trigger:** New product idea + quarterly planning
**Goal:** Research, validate, build, launch products on a predictable cycle
**Agents involved:** Product Manager → Market Researcher → Course Developer → Launch Coordinator → CMO

```
TRIGGER: New product idea (from CEO or Product Manager)
    ↓
[Market Researcher] Validate demand (1 week)
    ├── Is there search volume?
    ├── Are competitors serving this?
    ├── Is the audience willing to pay?
    └── Does it align with the mission?
    ↓
[Product Manager] Go / No-Go decision
    ↓
IF Go:
    ↓
[Course Developer] Build product outline (1 week)
    ↓
[CEO] Review and approve outline
    ↓
[Course Developer] Build product content (2-4 weeks)
    ↓
[Thumbnail Designer] Design product visuals
    ↓
[Copywriter] Write product landing page
    ↓
[Funnel Builder] Build conversion funnel
    ↓
[Launch Coordinator] Plan launch sequence (1 week)
    ├── Email sequence (3-5 emails)
    ├── Social media posts (5-7 posts)
    └── Launch day checklist
    ↓
[CEO] Final approval
    ↓
[Launch Coordinator] Execute launch
    ↓
[Analytics Agent] Track launch metrics
    ↓
[Product Manager] Post-launch review (Day 7, Day 30)
    ↓
[Knowledge Manager] Log learnings to claude-mem
```

**Automation tools:**
- MailerLite: Launch email sequences
- Notion: Product pipeline, launch checklist
- LinkedIn/Instagram: Launch posts
- Calendly: Post-launch call booking

**Time saved:** ~10 hours per product launch (vs. manual project management)

---

## The Automation Priority Matrix

| Chain | Impact | Effort | Priority |
|---|---|---|---|
| Lead Capture and Conversion | High (direct revenue) | Low (MailerLite already set up) | **1. This week** |
| Content Pipeline | High (growth engine) | Medium (needs content calendar) | **2. This week** |
| Operations and Infrastructure | Medium (cost savings) | Low (mostly monitoring) | **3. Week 2** |
| Product Development | High (revenue scaling) | High (needs product to develop) | **4. Month 2** |

---

## What to automate vs. what to keep manual

| Automate | Keep Manual |
|---|---|
| Email sequences (drip campaigns) | Personal replies to emails |
| Content scheduling | Content creation (first draft) |
| Cost tracking | Strategic decisions |
| Health checks | Client calls |
| CRM updates | Relationship building |
| Newsletter delivery | Faith and Mission review |
| Form submissions → tags | Pricing decisions |
| Social media scheduling | Brand voice decisions |

**The rule:** Automate the logistics. Keep the humanity manual. The automation handles the repeatable so the human can handle the relational. The automation is the system. The human is the soul. Both are needed. Neither is optional.

---

## The single most important automation

**The 5-email sequence.** It runs forever. It converts subscribers into calls. It compounds over time. It is the highest-leverage automation in the system.

After the 5-email sequence, the second most important automation is the **Friday newsletter.** It runs forever. It keeps the brand warm. It converts subscribers into evangelists over 6-12 months.

After the newsletter, the third most important automation is the **Saturday health check.** It runs forever. It catches problems before they become outages. It keeps the infrastructure honest.

**The 3 automations that matter most:**
1. 5-email conversion sequence (revenue)
2. Friday newsletter (brand)
3. Saturday health check (infrastructure)

Everything else is optimization. Build these 3 first. Optimize later.
