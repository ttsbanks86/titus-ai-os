# Titus Banks 8-Agent Operating Architecture
### The single page that defines your company, your roles, and how they ship together.

**Last updated:** 2026-06-05
**Time horizon:** 12 months (rolling)
**KPI:** Booked discovery calls per week
**Review cycle:** Friday 3:00 PM Pacific (weekly), first Friday 60-min (monthly), Day 30 90-min (retrospective)

---

## The Operating Model in One Sentence

> 8 roles. 1 company. 1 KPI. Every role ships something every week that moves the KPI.

The 8 agents are not 8 people. They are 8 **functions**. Some are filled by subagents today, some by you, some by a future hire. The architecture stays the same as the company grows. The agents behind each function change.

---

## The 8 Agents

### 1. CEO (you)
**Function:** Set direction. Approve strategy. Make the calls. Hold the brand.

**Tools you use:** OpenCode primary session. Subagents. This document. Weekly review.

**Weekly deliverables:**
- 1 Friday review (20 min)
- 1 monthly review (60 min, first Friday)
- 1 30-day retrospective (90 min, Day 30)
- 1 outreach batch (5-10 emails to new prospects)
- 1 booked call (minimum)

**KPI ownership:** Calls booked per week. Calls closed per month. Revenue per quarter. Brand integrity (no em-dashes, no banned words, no drift).

**Permission:** Final approval on all public-facing content. All paid decisions. All subagent configurations. The CEO is the only agent that can publish to LinkedIn, send emails, or spend money.

**Time allocation:** 60% on calls and relationships. 30% on strategic review. 10% on administration. The CEO should never spend more than 1 hour per day on email or social media.

---

### 2. Content
**Function:** Produce all written, visual, and video content. Maintain the brand voice. Ship 3 posts per week + 1 weekly email.

**Tools:** Subagent (engineer for HTML, documentation for long-form, claude-mem for past-context). Writeseed for first-draft iteration. VistaCreate for carousel design. Brand voice files in `my-voice.md`, `my-rules.md`, `BRAND-SYSTEM/`.

**Weekly deliverables:**
- 3 LinkedIn posts (Mon/Wed/Fri 8:30 AM Pacific)
- 1 weekly newsletter (Friday 8:30 AM Pacific, the 3-email rotation)
- 1 carousel or visual asset (for Mon post)
- 1 reply to every comment on your posts (within 24 hours)

**KPI ownership:** Engagement rate per post. Open rate per email. Click rate per email. Reply rate per email. Comments per post.

**Permission:** Drafts everything. Publishes nothing. All content requires CEO approval before going live.

**Compounding metric:** Reply rate trends up over time. Open rate stays above 30%. Comment count grows week over week. The audience compounds.

---

### 3. Research
**Function:** Web research, competitive analysis, market intelligence, technology scouting, due diligence on opportunities.

**Tools:** Perplexity (ask, reason, research, search), Firecrawl (scrape, agent, search), Brave Search, LinkedIn MCP, GitHub MCP. All findings logged to claude-mem.

**Weekly deliverables:**
- 1 industry signal report (1-2 findings worth knowing, 1 page)
- 1 competitor or peer scan (1-3 profiles, what they posted, what worked)
- 1 technology or tool research (when a decision is pending)
- Updates to `BRAND-SYSTEM/competitive-landscape.md` (when significant)

**KPI ownership:** Number of insights fed into Content, Marketing, or Operations per month. Quality of those insights (does the CEO use them).

**Permission:** Reads everything. Writes to claude-mem. Does not publish.

**Compounding metric:** The Research agent builds a knowledge base over time. Year 1: 100 insights. Year 2: 300 insights. Year 3: 800 insights. The 12-month strategic plan used Research as a primary input.

---

### 4. Video
**Function:** Produce short-form video for LinkedIn, Instagram Reels, TikTok, YouTube Shorts. Optional, only if CEO commits to video cadence.

**Tools:** Higgsfield Plus ($39/mo, in-stack) for AI video generation. Runway Gen-4.5 ($12/mo, backup). Optional: ComfyUI + Wan 2.7 (local, once hardware arrives). Optional: local webcam or phone footage for talking-head clips.

**Weekly deliverables (when video is active):**
- 1 short-form video (30-90 sec)
- 1 vertical cover image for the video
- Captions baked in (auto from transcript)

**KPI ownership:** Video views per post. Completion rate (>50% is good). Comments per video.

**Permission:** Drafts video concepts and scripts. Generates and edits clips. Publishes nothing. CEO approves scripts before generation.

**Status (June 2026):** Hold. The Content agent ships text + carousels first. Video agent activates month 2-3 when text cadence is consistent.

**Compounding metric:** Video library grows. Each video is a long-tail asset that drives traffic for 12-24 months. A 90-second video produced in month 2 is still generating leads in month 14.

---

### 5. Marketing
**Function:** Funnels, campaigns, lead generation, conversion optimization, brand positioning, offer design.

**Tools:** MailerLite (email automation). Linkpod (link in bio). Notion (CRM). LinkedIn (organic). Calendy (booking). Optional: Google Ads, Meta Ads (year 2+).

**Weekly deliverables:**
- 1 outreach batch (10-20 new contacts per week)
- 1 lead magnet promotion (Gap Audit, every 4-6 weeks)
- 1 funnel metric review (open rate, click rate, conversion rate, call booking rate)
- Updates to `LEAD-MAGNET/automation/` when conversion drops below threshold

**KPI ownership:** Funnel conversion rate (form-submit to call-booked). Cost per lead. Cost per call booked. Lifetime value per customer (when available).

**Permission:** Drafts campaigns. Builds automations. Sends emails only via MailerLite (not personal email). All list growth requires CEO approval.

**Compounding metric:** Email list size. Reply rate from outreach. Referrals from existing customers. The list is the asset. The list compounds. Year 1: 500 subscribers. Year 2: 2,000. Year 3: 6,000.

---

### 6. Operations
**Function:** Infrastructure, automation, deployment, monitoring, tooling, hardware, software, integrations.

**Tools:** PowerShell (Windows automation). Netlify (hosting). MailerLite (email). Notion (CRM). GitHub (code). Obsidian (knowledge base). claude-mem (memory). Local Python servers (when needed). RunPod or Vast.ai (cloud GPU, when needed).

**Weekly deliverables:**
- 1 infrastructure health check (all sites up, all automations running, all backups current)
- 1 automation or workflow improvement (small wins compound)
- 1 tool or process audit (is this tool still earning its cost?)

**KPI ownership:** Uptime (target: 99.5%). Cost per month (target: under $200 for year 1). Time saved per automation (target: 1+ hour per week per workflow).

**Permission:** Builds automations. Deploys code. Manages infrastructure. Does not write content. Does not send emails. Does not make purchases above $50 without CEO approval.

**Compounding metric:** Number of automations running. Hours saved per week. Cost per automation outcome. The compounding is in the time freed up for the CEO and Content agents.

---

### 7. Knowledge Manager
**Function:** Long-term memory, RAG, knowledge base, cross-agent context, institutional learning, decision history.

**Tools:** claude-mem (primary memory layer). Obsidian (human-readable knowledge graph). Notion (structured data). claude-mem corpora (project-scoped knowledge agents). GSD (Claude Code skill, for project decomposition). 

**Weekly deliverables:**
- 1 claude-mem corpus update (weekly reflection, decision log, learning log)
- 1 Obsidian note consolidation (merge related notes, archive stale ones)
- 1 decision recorded in `BRAND-SYSTEM/decisions.md`
- Daily journal entry (1 sentence per day, see `REVIEW/DAILY-JOURNAL.md`)

**KPI ownership:** Retrieval accuracy (does the right context come back when queried). Decision traceability (can the CEO find why a decision was made 6 months later). Time saved per query (vs. searching from scratch).

**Permission:** Reads everything. Writes to memory layers. Does not publish. Does not delete without CEO approval (memory is append-mostly).

**Compounding metric:** The knowledge base. Year 1: 500 observations. Year 2: 2,000. Year 3: 6,000. The base becomes the most valuable asset in the company. The CEO's thinking compounds because the Knowledge Manager never forgets.

---

### 8. Business Analyst
**Function:** Process maps, requirements, gap audits, client deliverables, strategic frameworks, customer research, data analysis.

**Tools:** Lucidchart or Miro (process maps). Excel or Google Sheets (analysis). Notion (deliverables). The Gap Audit PDF and tooling. The BA sub-brand design system.

**Weekly deliverables:**
- 1 client Gap Audit delivery (when calls convert to engagements)
- 1 process map or framework (for internal use or for a lead magnet)
- 1 competitive or industry analysis (in partnership with Research)
- 1 framework update (based on what is working in the field)

**KPI ownership:** Number of Gap Audits delivered per month. Number of process maps shipped per month. Client satisfaction score (informal, 1-10 in call debrief).

**Permission:** Delivers to clients. Publishes nothing publicly (Gap Audit is the public version; client deliverables are private). All client-facing deliverables require CEO approval before delivery.

**Compounding metric:** Number of frameworks, audits, and process maps in the library. Number of clients served. Number of referrals from clients. The BA library becomes a body of work. Year 1: 5 deliverables. Year 2: 25. Year 3: 80.

---

## The Handoff Protocol

This is how the 8 agents talk to each other. The protocol is the same as the company grows.

| From | To | Trigger | Artifact |
|---|---|---|---|
| CEO → Content | "Write me a post about X" | Decision to publish | Brief in `BRAND-SYSTEM/POST-PACKAGES/` |
| CEO → Research | "What do we know about Y" | Decision pending | 1-page report in `BRAND-SYSTEM/research/` |
| CEO → Marketing | "Run the gap audit funnel" | Launch decision | Campaign brief in `LEAD-MAGNET/campaigns/` |
| CEO → Operations | "Set up Z" | Tool decision | Workflow spec in `BRAND-SYSTEM/operations/` |
| Content → Research | "Verify this claim" | Draft review | Question + verified answer |
| Research → Content | "Use this insight" | Insight surfaces | Insight note + suggested post angle |
| Marketing → Knowledge Manager | "Log this conversion" | Lead converts | Entry in claude-mem + Notion CRM |
| Knowledge Manager → All | "Here is what we decided about X" | Query from any agent | Retrieved context |
| Business Analyst → Marketing | "Use this case study" | Client engagement closes | Anonymized case study in `BRAND-SYSTEM/case-studies/` |
| Operations → All | "Here is the new tool / workflow" | Tool ships | Documentation in `BRAND-SYSTEM/tooling/` |

**The CEO is the only agent that talks to external humans (except for Marketing, which sends emails on the CEO's behalf).** All other agents talk to each other through artifacts in the file system or through claude-mem.

---

## The Weekly Cadence

The cadence is the spine. Every week follows the same rhythm. Consistency compounds.

| Day | Time (Pacific) | Agent | Action |
|---|---|---|---|
| Monday | 8:30 AM | Content | LinkedIn post #1 publishes (educational carousel) |
| Monday | 9:00 AM | CEO | Reply to comments from weekend posts |
| Monday | 12:00 PM | CEO | 1 client call (if booked) |
| Monday | 4:00 PM | Knowledge Manager | Update claude-mem corpora with week's first learnings |
| Tuesday | 8:00 AM | Marketing | Outreach batch #1 (5-10 new contacts) |
| Tuesday | 12:00 PM | CEO | 1 client call (if booked) |
| Wednesday | 8:30 AM | Content | LinkedIn post #2 publishes (story or insight) |
| Wednesday | 12:00 PM | CEO | 1 client call (if booked) |
| Wednesday | 4:00 PM | Research | 1 industry signal report |
| Thursday | 8:00 AM | Marketing | Outreach batch #2 (5-10 new contacts) |
| Thursday | 12:00 PM | CEO | 1 client call (if booked) |
| Friday | 8:30 AM | Content | LinkedIn post #3 publishes (practical / framework) + weekly newsletter |
| Friday | 12:00 PM | CEO | 1 client call (if booked) |
| Friday | 3:00 PM | CEO | Weekly review (20 min, metrics + 3 questions) |
| Friday | 4:00 PM | Knowledge Manager | Weekly retrospective, decision log, Obsidian sync |
| Saturday | 9:00 AM | Operations | Infrastructure health check, automation improvements |
| Sunday | (off) | (none) | (rest) |

**Total CEO time per week:** ~6-8 hours of calls + 20 min review + 30 min outreach + 15 min approvals = **~8-10 hours per week** of focused work.

The rest of the time is automated. The agents ship in the background. The CEO ships relationships and decisions.

---

## Monthly and Quarterly Cadence

| Frequency | Action | Duration | Agent |
|---|---|---|---|
| Weekly (Friday) | Weekly review | 20 min | CEO |
| Monthly (first Friday) | Monthly review | 60 min | CEO + Knowledge Manager |
| Quarterly (first Friday of Q) | Quarterly planning | 3 hrs | CEO + all subagents |
| Every 30 days | 30-day retrospective | 90 min | CEO + Knowledge Manager |
| Every 90 days | 12-month plan review | 2 hrs | CEO + Research + Operations |
| Every 365 days | Annual strategic refresh | 1 day | CEO + all subagents |

The quarterly and annual reviews are where the strategic plan gets re-balanced. The 12-month strategic plan lives at `TITUS-BANKS-AI-INFRASTRUCTURE-12-MONTH-STRATEGIC-PLAN.md` and gets reviewed on this cadence.

---

## The One-Page Cheat Sheet

Print this. Pin it above your desk. Reference it every Friday.

```
TITUS BANKS 8-AGENT OPERATING MODEL
===================================

CEO          →  Set direction, approve, hold the brand
CONTENT      →  3 posts/wk + Friday newsletter
RESEARCH     →  1 signal + 1 scan per week
VIDEO        →  HOLD until month 2-3
MARKETING    →  Funnels, outreach, conversion
OPERATIONS   →  Infra, automation, deployment
KNOWLEDGE    →  Memory, decisions, journals
BUSINESS     →  Gap audits, process maps, deliverables

KPI:         Booked discovery calls per week
TARGET:      Day 14 → 2 calls. Day 90 → 8 calls/month.
CADENCE:     M/W/F posts 8:30 AM PT. F review 3:00 PM.
REVIEW:      Weekly 20m. Monthly 60m. 30-day 90m. Quarterly 3h.

THE 3 WEEKLY QUESTIONS:
1. Did the gap between what is and what should be get smaller?
2. Did 1 new relationship get warmer?
3. Did 1 new piece of work get shipped?

THE 1 RULE:
Show up. Every Monday. Every Wednesday. Every Friday.
For 52 weeks. Even when you do not feel like it.
```

---

## What This Is Not

This is not a corporate org chart. It is not a RACI matrix. It is not a SWOT analysis. It is a **functional operating model** for a one-person company that wants to behave like a 20-person company.

The 8 agents are roles, not hires. They are functions, not job titles. They are the categories of work that need to get done, not the people who do them. Some of them are filled by subagents today. Some are filled by you. Some will be filled by a future hire. The architecture stays the same. The agents behind it evolve.

**The discipline is the function, not the agent.** The discipline of showing up every Friday is the function of the CEO. The discipline of writing 3 posts a week is the function of Content. The discipline of replying within 24 hours is the function of the CEO again. The functions are stable. The agents are replaceable. The compounding is in the function, not the agent.

---

## The single most important sentence in this document

> The CEO is the only agent that talks to external humans.

Everything else is internal. Everything else is automation. Everything else is compounding in the background. The CEO's job is to ship relationships and decisions. The CEO's job is not to write code, design carousels, run outreach, or manage infrastructure. Those are functions the CEO delegates to the appropriate agent.

When the CEO finds themselves doing work that is not relationships or decisions, that work is a candidate for delegation. The 8-agent model exists to make that delegation explicit. The 8-agent model exists so the CEO never does work an agent could do.

**The CEO's job is the work only the CEO can do.**
