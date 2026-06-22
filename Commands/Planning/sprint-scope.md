# Sprint Scope

## Purpose
Define sprint scope from backlog items, team capacity, and priorities.

## Inputs
- Backlog items (prioritized list)
- Team capacity (from capacity-check or manual input)
- Sprint duration (1 or 2 weeks)
- Sprint goal or theme
- Dependencies or blockers

## Outputs
- Sprint scope with committed items
- Capacity allocation by team member
- Sprint goal statement
- Risk items and mitigation plan
- Definition of done for each item

## Workflow
1. Pull prioritized backlog items
2. Pull team capacity for the sprint
3. Estimate each item (story points, hours, or t-shirt sizing)
4. Fill capacity top-down by priority:
   - Add items until capacity is reached
   - Reserve 20% for unplanned work, bugs, and overhead
5. Assign items to team members based on capacity and expertise
6. Identify dependencies and potential blockers
7. Define sprint goal and success criteria
8. Generate sprint scope document

## Example Execution
```
/sprint-scope --backlog "notion-backlog.csv" --capacity "engineering" --duration "2 weeks" --goal "Launch dashboard v2"

Output:
━━━ SPRINT SCOPE: Sprint 14 | June 8-19, 2026 ━━━

🎯 SPRINT GOAL
  Launch Dashboard v2 to production with full feature set

📋 COMMITTED ITEMS (87 of 104 available points)
  | # | Item                    | Points | Owner  | Status      |
  |---|-------------------------|--------|--------|-------------|
  | 1 | Dashboard API endpoints | 8      | Mike   | Ready       |
  | 2 | Dashboard frontend      | 13     | Sarah  | Ready       |
  | 3 | Real-time data sync     | 8      | Alex   | Ready       |
  | 4 | Dashboard testing       | 5      | Jess   | Ready       |
  | 5 | Dashboard deployment    | 3      | Casey  | Ready       |
  | 6 | Client feedback fixes   | 8      | Sarah  | Ready       |
  | 7 | Documentation update    | 3      | Jess   | Ready       |
  | 8 | Bug backlog (top 5)     | 21     | All    | Ready       |

📦 CAPACITY ALLOCATION
  | Member   | Capacity | Committed | Reserved | Available |
  |----------|----------|-----------|----------|-----------|
  | Sarah    | 36 pts   | 21 pts    | 7 pts    | 8 pts     |
  | Mike     | 38 pts   | 8 pts     | 8 pts    | 22 pts    |
  | Alex     | 30 pts   | 8 pts     | 6 pts    | 16 pts    |
  | Jess     | 38 pts   | 8 pts     | 8 pts    | 22 pts    |
  | Casey    | 38 pts   | 3 pts     | 8 pts    | 27 pts    |

⚠️ RISKS
  1. Real-time sync depends on third-party API (mitigation: mock available)
  2. Sarah's capacity tight — avoid adding unplanned work
  3. Testing may be bottleneck if dev completes late

🔄 DEFERRED (moved to Sprint 15)
  - Advanced analytics widget (13 pts)
  - Mobile responsive pass (8 pts)

✅ DEFINITION OF DONE
  - Code complete and reviewed
  - Tests passing
  - Documentation updated
  - Deployed to staging
  - Stakeholder demo completed
```

## Validation Checks
- Confirm total committed points don't exceed 80% of capacity
- Verify each item has an owner and estimate
- Check that dependencies are identified and have mitigation plans
- Ensure sprint goal is achievable with committed items
- Validate that deferred items are documented for next sprint
