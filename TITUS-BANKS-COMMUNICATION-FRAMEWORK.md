# Titus Banks Communication Framework
### How 41 agents talk to each other, delegate tasks, get approvals, and escalate issues.

**Last updated:** 2026-06-05
**Principle:** The CEO is the only agent that talks to external humans. Everything else is internal.
**Memory:** All decisions, context, and learnings flow through claude-mem and Obsidian.

---

## The 4 Communication Layers

### Layer 1: CEO ↔ Executives (Weekly + Ad Hoc)

**Cadence:** Weekly Friday review (20 min). Monthly first-Friday review (60 min). Ad hoc as needed.

**How it works:**
- CEO sets priorities on Monday morning (written, in Notion or Obsidian)
- Executives report progress on Friday afternoon (written, in Notion or Obsidian)
- CEO reviews, asks questions, adjusts priorities
- Decisions are logged in `decisions.md` with date, context, rationale, and expected outcome

**Delegation protocol:**
1. CEO writes a task brief (1-3 sentences: what, why, deadline)
2. CEO assigns to the appropriate executive
3. Executive acknowledges within 24 hours
4. Executive breaks the task into sub-tasks and assigns to sub-agents
5. Executive reports completion to CEO on Friday

**Approval protocol:**
- CEO approves: All public-facing content, all spending above $50, all new tools, all strategic decisions
- Executive approves: Sub-agent work within their department, routine operations, internal documentation
- No approval needed: Sub-agent work that is routine, documented, and within the executive's approved scope

### Layer 2: Executives ↔ Sub-Agents (Daily + Weekly)

**Cadence:** Daily task assignments. Weekly department review (15 min per department).

**How it works:**
- Executive breaks weekly priorities into daily tasks
- Executive assigns tasks to sub-agents with clear briefs
- Sub-agents execute and report back
- Executive reviews and approves before forwarding to CEO

**Delegation protocol:**
1. Executive writes a task brief (1-2 sentences: what, deliverable format, deadline)
2. Executive assigns to the appropriate sub-agent
3. Sub-agent acknowledges and begins work
4. Sub-agent delivers the artifact (file, report, draft)
5. Executive reviews, provides feedback, approves or requests revision

**Approval protocol:**
- Executive approves: All sub-agent output before it leaves the department
- Sub-agent self-approves: Routine tasks within their documented scope (e.g., daily cost tracking, routine code review)
- Escalation: If a sub-agent encounters a decision outside their scope, they escalate to the executive

### Layer 3: Sub-Agents ↔ Sub-Agents (Within Department)

**Cadence:** As needed. No fixed schedule.

**How it works:**
- Sub-agents within the same department can communicate directly
- They produce artifacts that other sub-agents consume (e.g., Research produces a report that Copywriter uses)
- No approval needed for intra-department communication
- All artifacts are stored in the shared knowledge base (Obsidian/Notion)

**Example workflows:**
- Research → Copywriter: "Here are 3 industry signals. Use them in this week's posts."
- Coding → QA: "Here is the code. Test it."
- Script Writer → Thumbnail Designer: "Here is the script. Design a thumbnail."
- Cost Tracker → Budget Analyst: "Here are this week's costs. Update the budget."

### Layer 4: Cross-Department Communication (Through Executives)

**Cadence:** As needed. Always goes through the executive layer.

**How it works:**
- Sub-agent A needs something from Sub-agent B in a different department
- Sub-agent A tells Executive A
- Executive A tells Executive B
- Executive B tells Sub-agent B
- Sub-agent B does the work
- The work flows back through the same chain

**Exception:** If the two executives have a standing agreement (documented in Notion), sub-agents can communicate directly for pre-approved tasks. But the default is: cross-department goes through executives.

**Why:** Without this rule, the org chart collapses into chaos. Every agent talking to every other agent creates noise. The executive layer filters noise into signal.

---

## The 3 Escalation Rules

### Rule 1: Time-Based Escalation

| Situation | Escalation Path | Timeline |
|---|---|---|
| Sub-agent blocked | → Executive | Within 4 hours |
| Executive blocked | → CEO | Within 24 hours |
| System outage | → CTO → CEO | Within 1 hour |
| Security concern | → CTO → CEO | Immediately |
| Revenue concern | → CFO → CEO | Within 24 hours |

### Rule 2: Threshold-Based Escalation

| Situation | Threshold | Escalation |
|---|---|---|
| Expense | > $50 | CEO approval required |
| New tool subscription | > $20/month | CEO approval required |
| Content published externally | Any | CEO approval required |
| Pricing change | Any | CEO approval required |
| New product/service | Any | CEO approval required |
| Budget variance | > 15% | CFO → CEO |
| Revenue drop | > 20% month-over-month | CFO → CEO |

### Rule 3: Values-Based Escalation

| Situation | Escalation |
|---|---|
| Content could be perceived as exploiting faith | Faith and Mission → CEO immediately |
| Scripture reference is inaccurate | Faith and Mission → CEO immediately |
| Brand voice drifts from stated identity | Faith and Mission → CEO |
| Strategic decision conflicts with mission | Faith and Mission → CEO |
| Customer complaint about brand values | CEO (direct, no delegation) |

---

## The Reporting Structure

### Daily
- Sub-agents: Execute tasks, produce artifacts, log to knowledge base
- Executives: Review sub-agent output, assign next day's tasks

### Weekly (Friday 3:00 PM Pacific)
- CEO: 20-minute review with all 7 executives
- Each executive: 3 questions (What shipped? What is blocked? What is next?)
- CEO: Adjusts priorities, approves next week's plan
- Knowledge Manager: Updates claude-mem corpora, logs decisions

### Monthly (First Friday, 60 min)
- CEO: Monthly review with all 7 executives
- CFO: Financial summary (revenue, expenses, net, forecast)
- CMO: Marketing metrics (engagement, leads, conversion)
- Content Director: Content metrics (posts, engagement, growth)
- Product Manager: Product status (launches, revenue, pipeline)
- COO: Operations metrics (automations running, time saved)
- CTO: Tech status (infrastructure health, tool costs, security)
- Faith and Mission: Values audit (brand alignment, mission drift)

### Quarterly (First Friday of Q, 3 hrs)
- CEO: Strategic planning session with all executives
- Review 12-month strategic plan, adjust targets
- Approve new initiatives, sunset underperformers
- Update 8-agent architecture if needed

---

## The Memory Architecture

All 41 agents write to and read from a shared memory system:

| Layer | Tool | Purpose | Who Writes | Who Reads |
|---|---|---|---|---|
| **Decisions** | `decisions.md` in Obsidian | Why we did what we did | CEO, Executives | All |
| **Context** | claude-mem | What we know right now | All agents | All |
| **Documents** | Obsidian vault | What we have built | All agents | All |
| **Tasks** | Notion | What needs to happen | CEO, Executives | All |
| **Metrics** | Notion + Google Sheets | How we are performing | CFO, CMO, Analytics | CEO, Executives |
| **Journals** | `DAILY-JOURNAL.md` | What we learned today | CEO | CEO |

**The memory rule:** If it is not written down, it did not happen. Every decision, every learn, every metric goes into the memory system. The memory system is the company's brain. The brain compounds.

---

## The Communication Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | The Fix |
|---|---|---|
| CEO talks to sub-agents directly | Bypasses executive layer, creates confusion | Always go through the executive |
| Sub-agents skip approval | Output goes live with errors | Executive reviews before forwarding |
| Cross-department direct communication | Creates dependency chaos | Route through executives |
| No documentation of decisions | Same debate repeated monthly | Log every decision in `decisions.md` |
| No escalation timeline | Issues fester for weeks | Use the time-based escalation rules |
| No memory write | Knowledge walks out the door when agent context resets | Always write to claude-mem |

---

## The Single Rule

**Every communication must produce an artifact.**

If you had a meeting, write 3 bullets about what was decided. If you reviewed a document, write 1 sentence about what you found. If you completed a task, write 1 sentence about what shipped.

The artifact is the proof that the communication happened. Without the artifact, the communication did not happen. Without the communication, the company does not exist.

The discipline of writing it down is the discipline of the company existing.
