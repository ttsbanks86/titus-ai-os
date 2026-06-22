# Morning Brief

## Purpose
Generate a daily briefing with priorities, schedule, and key context.

## Inputs
- Calendar for today
- Priority tasks or goals
- Pending items from yesterday
- Weather (optional)
- News or industry updates (optional)

## Outputs
- Today's schedule overview
- Top 3 priorities
- Pending items carrying over
- Context for meetings
- Suggested focus blocks

## Workflow
1. Pull today's calendar events
2. Identify priority tasks for the day
3. Pull pending items from yesterday's wrap
4. Gather context for any meetings (attendees, agenda, prep needed)
5. Calculate available focus time
6. Generate morning brief with schedule, priorities, and context

## Example Execution
```
/morning-brief --date "June 8, 2026"

Output:
━━━ MORNING BRIEF: Monday, June 8, 2026 ━━━

☀️ Good morning! Here's your day at a glance.

📅 SCHEDULE
  9:00  — Focus block (no meetings)
  10:00 — Standup (15 min)
  10:30 — Focus block
  12:00 — Lunch
  1:00  — Focus block
  2:30 — Client: Acme (30 min) — Prep: review wireframes
  3:00  — Focus block
  5:00 — EOD

🎯 TOP 3 PRIORITIES
  1. Dashboard v2: Final testing and bug fixes
  2. Q2 planning doc: Start outline and first sections
  3. Acme meeting prep: Review wireframes, confirm feedback

📌 CARRYING OVER FROM YESTERDAY
  • Review @sarah's PR (est. 30 min)
  • Respond to HR benefits email

💡 FOCUS BLOCKS
  Morning: 9:00–10:00 (1 hr) — Deep work on dashboard
  Late morning: 10:30–12:00 (1.5 hrs) — Dashboard continues
  Afternoon: 1:00–2:30 (1.5 hrs) — Q2 doc draft
  Late afternoon: 3:00–5:00 (2 hrs) — Buffer / overflow

📊 YESTERDAY'S WRAP
  Completed: 3 tasks | Blocked: 1 (resolved) | Overdue: 0

🌤️ Weather: 72°F, Sunny — Good day for a walk at lunch

Have a productive day!
```

## Validation Checks
- Confirm calendar is pulled for the correct date
- Verify meeting prep context is accurate and current
- Ensure carry-over items are genuinely pending (not completed)
- Check that focus blocks don't conflict with meetings
- Validate that priorities align with weekly goals
