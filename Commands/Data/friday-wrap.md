# Friday Wrap

## Purpose
Generate a weekly summary with wins, blockers, and next week's plan.

## Inputs
- Project management tool data (Notion, Asana, Jira)
- Completed tasks this week
- In-progress items
- Calendar for next week
- Team updates or standup notes

## Outputs
- Weekly wins summary
- Blockers and resolutions
- Key metrics update
- Next week priorities
- Team shoutouts

## Workflow
1. Pull completed tasks from PM tool for the week
2. Pull in-progress items and their status
3. Identify any blockers that arose or were resolved
4. Pull next week's calendar for scheduled commitments
5. Compile into structured weekly wrap
6. Include team recognition for notable contributions

## Example Execution
```
/friday-wrap --source notion --week "June 1-7, 2026"

Output:
━━━ FRIDAY WRAP: Week of June 1, 2026 ━━━

🏆 WINS
  1. Launched Acme website redesign – client ecstatic
  2. Closed $180K deal with GlobalCo
  3. Reduced build time by 40% (CI/CD optimization)
  4. Onboarded 2 new team members (Sarah & Mike)

🚧 BLOCKERS RESOLVED
  1. Stripe API access – escalated and resolved Wednesday
  2. Design system inconsistencies – new component library deployed

⚠️ CURRENT BLOCKERS
  1. Legal review delay on DataInc contract
  2. Staging environment performance issues

📊 METRICS
  Revenue closed: $210K (Target: $200K) ✅
  New leads: 18 (Target: 15) ✅
  Support tickets resolved: 94% within SLA ✅
  Sprint velocity: 42 points (Target: 40) ✅

📅 NEXT WEEK PRIORITIES
  1. DataInc contract finalization
  2. Dashboard v2 launch (Thursday)
  3. Q2 planning document delivery
  4. Performance optimization sprint

👏 SHOUTOUTS
  @sarah for crushing the Acme launch under tight timeline
  @mike for proactively fixing the CI/CD pipeline without being asked
  @jess for handling 3 client escalations gracefully
```

## Validation Checks
- Confirm all completed tasks are captured from PM tool
- Verify blockers are current and not already resolved
- Ensure next week's priorities align with team capacity
- Check metrics calculations are accurate
- Validate that shoutouts are genuine and specific
