# Week Plan

## Purpose
Create a weekly plan from priorities, calendar events, and team capacity.

## Inputs
- Priorities or goals for the week
- Calendar events and meetings
- Carry-over tasks from previous week
- Team availability
- Deadlines and milestones

## Outputs
- Daily plan with time blocks
- Priority-ranked task list
- Meeting impact analysis
- Focus time allocations
- Risk items (overloaded days)

## Workflow
1. Pull calendar events for the week
2. Identify fixed commitments (meetings, deadlines, events)
3. Calculate available work hours after meetings
4. Rank priorities and assign to available time blocks
5. Identify:
   - Focus-heavy days (fewer meetings)
   - Meeting-heavy days (less deep work)
   - Overloaded days (capacity exceeded)
6. Generate daily and weekly plan with time blocks
7. Flag capacity risks and suggest rebalancing

## Example Execution
```
/week-plan --priorities "Dashboard launch, Q2 doc, 3 client calls" --calendar "google-cal"

Output:
━━━ WEEK PLAN: June 8-12, 2026 ━━━

🎯 PRIORITIES
  1. Dashboard v2 launch (deadline: Thursday)
  2. Q2 planning document (deadline: Friday)
  3. Client calls: Acme (Tue), GlobalCo (Wed), DataInc (Fri)

📅 DAILY BREAKDOWN

MONDAY (June 8) – Focus Day
  ✅ 9:00–11:00 Dashboard final testing
  ✅ 11:00–12:00 Q2 doc outline
  ✅ 1:00–3:00 Dashboard code review
  ✅ 3:00–5:00 Q2 doc draft

TUESDAY (June 9) – Mixed Day
  ✅ 9:00–10:00 Dashboard deploy prep
  🔵 10:30–11:30 Client: Acme
  ✅ 1:00–3:00 Q2 doc sections 1-2
  ✅ 3:00–5:00 Dashboard bug fixes

WEDNESDAY (June 10) – Meeting Heavy ⚠️
  🔵 9:00–10:00 Client: GlobalCo
  🔵 10:30–11:30 Team standup
  🔵 2:00–3:00 Sprint planning
  ✅ 3:30–5:00 Q2 doc sections 3-4

THURSDAY (June 11) – Launch Day
  ✅ 9:00–11:00 Dashboard launch
  🔵 11:30–12:00 Launch retrospective
  ✅ 1:00–3:00 Q2 doc finalization
  ✅ 3:00–5:00 Buffer / overflow

FRIDAY (June 12) – Wrap Day
  🔵 9:00–10:00 Client: DataInc
  ✅ 10:30–12:00 Q2 doc review
  ✅ 1:00–3:00 Weekly review & next week prep
  ✅ 3:00–5:00 Buffer

⚠️ CAPACITY ALERT
  Wednesday is meeting-heavy (3 meetings, 3 hrs). Consider moving Q2 doc work to Thursday.

💡 TIP: Block Tuesday 1–3pm and Friday 1–3pm for deep work on Q2 doc.
```

## Validation Checks
- Confirm all calendar events are included
- Verify time blocks don't overlap
- Check that total assigned hours don't exceed available capacity
- Ensure deadlines are achievable within the plan
- Flag any days with <2 hours of focus time
