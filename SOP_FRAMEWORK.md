# SOP Framework

**Date:** 2026-06-21
**Purpose:** Define the standard operating procedure format, creation process, and enforcement rules for the Titus AI OS.

---

## Why SOPs

OpenCode agents should execute documented processes, not improvise. When an agent encounters a task, it checks for an SOP first. If one exists, it follows it. If one does not exist, it notes the gap.

SOPs eliminate:
- Reinventing approaches for repeat tasks
- Inconsistent quality across sessions
- Missing steps because "nobody remembered"
- The need for the user to explain the same process repeatedly

SOPs enable:
- Consistent, predictable execution
- Quality that compounds over time
- Easy delegation (any agent can follow a documented SOP)
- Continuous improvement (SOPs get refined with experience)

---

## SOP Template

Every SOP follows the same structure. The template lives at `11-Templates/SOP-Template.md`.

```markdown
# [SOP Name]

**Domain:** [Career / Content / Business / Development / Operations / Marketing]
**Last Updated:** YYYY-MM-DD
**Version:** 1.0
**Owner:** [Agent or person responsible for this SOP]

## Objective
[One sentence. What does this SOP accomplish?]

## When to Use
[Trigger conditions. When should an agent execute this SOP?]

## Prerequisites
- [What must be in place before starting?]
- [Required tools, access, information]

## Inputs
- [What information or assets does this SOP need?]
- [Files, URLs, credentials, context]

## Process

### Step 1: [Step Name]
[Description. What to do. Expected output.]

### Step 2: [Step Name]
[Description. What to do. Expected output.]

### Step 3: [Step Name]
[Description. What to do. Expected output.]

[...additional steps as needed...]

## Outputs
- [What does this SOP produce?]
- [Files, documents, decisions, actions]

## Quality Checks
- [ ] Check 1 — what to verify
- [ ] Check 2 — what to verify
- [ ] Check 3 — what to verify

## Common Issues
- **Issue:** [Description]
  - **Fix:** [Solution]
- **Issue:** [Description]
  - **Fix:** [Solution]

## Related
- [[Related-SOP]]
- [[Related-Master-Note]]
- [[Related-Template]]
```

---

## SOP Inventory by Domain

### Career SOPs (`07-SOPs/Career/`)

| SOP | Objective |
|---|---|
| [[Job-Application-SOP]] | Research company, tailor resume, write cover letter, submit application. |
| [[LinkedIn-Outreach-SOP]] | Find contacts, craft message, send connection request, track responses. |
| [[Interview-Preparation-SOP]] | Research role, prepare answers, practice questions, follow up. |
| [[Job-Search-Workflow-SOP]] | Daily job search routine: search, filter, apply, track. |
| [[Resume-Tailoring-SOP]] | Match resume keywords to job description, update versions. |

### Content SOPs (`07-SOPs/Content/`)

| SOP | Objective |
|---|---|
| [[Social-Media-Post-SOP]] | Write, review, schedule, and publish a social media post. |
| [[Newsletter-SOP]] | Write, edit, format, and send a newsletter. |
| [[Video-Script-SOP]] | Research topic, write script, review, finalize. |
| [[Content-Calendar-SOP]] | Plan content for the week/month across platforms. |
| [[Content-Repurposing-SOP]] | Take one piece of content and adapt it for multiple platforms. |

### Business SOPs (`07-SOPs/Business/`)

| SOP | Objective |
|---|---|
| [[Lead-Research-SOP]] | Find potential clients, gather contact info, qualify leads. |
| [[Email-Triage-SOP]] | Process inbox: categorize, respond, archive, delegate. |
| [[Meeting-Recap-SOP]] | Document meeting notes, action items, and follow-ups. |
| [[Competitor-Analysis-SOP]] | Research competitor, document findings, update strategy. |
| [[Client-Onboarding-SOP]] | Welcome new client, gather requirements, set expectations. |

### Development SOPs (`07-SOPs/Development/`)

| SOP | Objective |
|---|---|
| [[Feature-Development-SOP]] | Plan, implement, test, and deploy a new feature. |
| [[Code-Review-SOP]] | Review code changes for quality, security, and standards. |
| [[Deployment-SOP]] | Deploy changes to production safely. |
| [[Bug-Fix-SOP]] | Reproduce, diagnose, fix, and verify a bug. |

### Operations SOPs (`07-SOPs/Operations/`)

| SOP | Objective |
|---|---|
| [[Daily-Workflow-SOP]] | Morning routine: check daily note, review tasks, execute priorities. |
| [[Weekly-Review-SOP]] | Review week's progress, update project notes, plan next week. |
| [[Monthly-Planning-SOP]] | Review monthly goals, update roadmaps, adjust priorities. |
| [[Session-Handoff-SOP]] | End a session: update daily note, update project notes, verify completion. |

### Marketing SOPs (`07-SOPs/Marketing/`)

| SOP | Objective |
|---|---|
| [[Campaign-Launch-SOP]] | Plan, build, test, and launch a marketing campaign. |
| [[Email-Campaign-SOP]] | Write, design, test, and send an email campaign. |
| [[A-B-Test-SOP]] | Design, run, and analyze an A/B test. |

---

## SOP Creation Process

When a new process needs an SOP:

1. **Identify the trigger.** When would an agent need this SOP?
2. **Document the current best approach.** How is it done right now?
3. **Write the SOP using the template.** Follow the standard structure.
4. **Link it to the master note.** The SOP should be reachable from its domain master note.
5. **Update the SOPs index.** Add it to `07-SOPs/SOPs-Index.md`.
6. **Test it.** Execute the SOP once manually. Fix any gaps.
7. **Version it.** Start at 1.0. Increment when the process changes.

---

## SOP Enforcement

### For OpenCode Agents

When an agent receives a task that matches a known domain:

1. **Check `07-SOPs/SOPs-Index.md`** for a relevant SOP.
2. **If SOP exists:** Load it. Follow it step by step. Do not skip steps.
3. **If SOP does not exist:** Note the gap. Execute with best judgment. Flag for SOP creation in the daily note.
4. **If SOP exists but is outdated:** Follow it as written. Flag the gap in the daily note. Do not improvise a new process mid-execution.

### For the User

The user can request:
- "Follow the [SOP Name]" — agent loads and executes that SOP.
- "Create an SOP for [process]" — agent documents the current best approach as a new SOP.
- "Update [SOP Name]" — agent reviews and refines the existing SOP.
- "What SOPs exist for [domain]?" — agent lists relevant SOPs.

---

## Anti-Bloat Rules for SOPs

1. **One SOP per process.** Do not create multiple SOPs for the same task.
2. **Keep SOPs concise.** If an SOP exceeds 3 pages, it is too granular. Split into sub-SOPs linked from the main SOP.
3. **Do not create SOPs for one-off tasks.** SOPs are for repeatable processes.
4. **Review SOPs quarterly.** If an SOP has not been used in 90 days, archive it.
5. **Update SOPs when the process changes.** Outdated SOPs are worse than no SOPs.

---

## Migration from Existing SOPs

Existing SOPs in `Knowledge_Base/SOPs/` and `AI_Agents/09_SOPs/` will be reviewed, updated to the new template, and migrated to `07-SOPs/`. The old locations will be archived.

| Existing SOP | New Location | Status |
|---|---|---|
| `Knowledge_Base/SOPs/email-triage-sop.md` | `07-SOPs/Business/Email-Triage-SOP.md` | Needs template update |
| `Knowledge_Base/SOPs/lead-management-sop.md` | `07-SOPs/Business/Lead-Research-SOP.md` | Needs template update |
| `Knowledge_Base/SOPs/meeting-recap-sop.md` | `07-SOPs/Business/Meeting-Recap-SOP.md` | Needs template update |
| `Knowledge_Base/SOPs/reporting-sop.md` | `07-SOPs/Operations/Weekly-Review-SOP.md` | Needs template update |
| `Knowledge_Base/Workflows/daily-workflow.md` | `07-SOPs/Operations/Daily-Workflow-SOP.md` | Needs template update |
| `AI_Agents/09_SOPs/LOCAL_AGENT_WORKFLOW.md` | `07-SOPs/Operations/Local-Agent-Workflow-SOP.md` | Needs template update |

---

This framework ensures every repeatable process is documented, every agent follows it, and quality compounds over time.
