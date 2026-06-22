# Capacity Check

## Purpose
Analyze team capacity and workload distribution to prevent overload.

## Inputs
- Team member list
- Current assignments and hours committed
- Available hours (PTO, holidays, focus time)
- Upcoming deadlines
- Velocity or throughput data (optional)

## Outputs
- Per-person capacity summary
- Team utilization rate
- Overloaded and underloaded members
- Workload rebalancing suggestions
- Forecast for next 1-2 weeks

## Workflow
1. Calculate available hours per team member (40 hrs - PTO - meetings - admin)
2. Sum committed hours from current assignments
3. Calculate utilization: committed / available
4. Identify:
   - Overloaded: >85% utilization
   - Optimal: 65-85% utilization
   - Underloaded: <65% utilization
5. Map upcoming deadlines to capacity
6. Suggest rebalancing (move tasks, defer, or add resources)

## Example Execution
```
/capacity-check --team "engineering" --range "next 2 weeks"

Output:
━━━ CAPACITY CHECK: Engineering | June 8-19, 2026 ━━━

👥 TEAM CAPACITY
  | Member   | Available | Committed | Util | Status  |
  |----------|-----------|-----------|------|---------|
  | Sarah    | 72 hrs    | 68 hrs    | 94%  | 🔴 Over |
  | Mike     | 76 hrs    | 54 hrs    | 71%  | 🟢 OK   |
  | Jess     | 76 hrs    | 42 hrs    | 55%  | 🟡 Under|
  | Alex     | 60 hrs    | 62 hrs    | 103% | 🔴 Over |
  | Casey    | 76 hrs    | 38 hrs    | 50%  | 🟡 Under|

📊 TEAM SUMMARY
  Total Available: 360 hrs
  Total Committed: 264 hrs
  Team Utilization: 73%

🔴 OVERLOADED
  Sarah (94%): Dashboard launch + client support
  Alex (103%): PTO next week creating crunch this week

🟡 UNDERLOADED
  Jess (55%): Available for dashboard launch support
  Casey (50%): Available for Q2 doc research

💡 RECOMMENDATIONS
  1. Move 2 client tickets from Sarah to Jess (saves 8 hrs)
  2. Shift Alex's Q2 doc work to Casey (Alex at capacity)
  3. Consider deferring Casey's tech debt sprint to next cycle

⚠️ RISK
  Alex is at 103% and has PTO next week — needs immediate rebalancing
```

## Validation Checks
- Confirm PTO and holidays are factored in correctly
- Verify committed hours match actual task estimates
- Ensure utilization thresholds are applied consistently
- Check that recommendations don't create new overloads
- Validate that upcoming deadlines are accounted for in capacity
