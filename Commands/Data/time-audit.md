# Time Audit

## Purpose
Analyze time tracking data to identify productivity patterns and optimization opportunities.

## Inputs
- Time tracking data (Toggl, Harvest, Clockify, or spreadsheet)
- Team members to include (or all)
- Date range
- Project/category definitions

## Outputs
- Time breakdown by project, category, and team member
- Utilization rates
- Productivity patterns (peak hours, focus time)
- Billable vs non-billable analysis
- Recommendations for time optimization

## Workflow
1. Ingest time tracking data for specified range
2. Categorize entries (billable, non-billable, meetings, admin, focus)
3. Calculate:
   - Total hours logged vs expected hours
   - Utilization rate (billable / total)
   - Average hours per day per person
   - Time distribution across projects
4. Identify patterns:
   - Peak productive hours
   - Meeting-heavy days
   - Focus time blocks
   - Overtime trends
5. Generate audit report with insights and recommendations

## Example Execution
```
/time-audit --source toggl --range "June 1-7, 2026" --team "engineering"

Output:
━━━ TIME AUDIT: Engineering Team | June 1-7, 2026 ━━━

⏰ OVERVIEW
  Total Hours Logged: 320 (Expected: 320)
  Team Size: 8 | Avg Hours/Person: 40

📊 BY CATEGORY
  | Category      | Hours | % Total | Trend   |
  |---------------|-------|---------|---------|
  | Development   | 192   | 60.0%   | ↑ +5%   |
  | Meetings      | 56    | 17.5%   | ↑ +8%   |
  | Code Review   | 32    | 10.0%   | → same  |
  | Admin         | 24    | 7.5%    | ↓ -3%   |
  | Learning      | 16    | 5.0%    | → same  |

📈 UTILIZATION
  Billable (client work): 72%
  Internal projects: 18%
  Overhead: 10%

🕐 PATTERNS
  Peak productivity: Tuesday-Thursday, 9am-12pm
  Meeting overload: Wednesday (4.5 hrs avg per person)
  Focus time: Monday & Friday afternoons (least interrupted)

💡 RECOMMENDATIONS
  1. Block Wednesday mornings for focus time (currently 60% meetings)
  2. Shift code reviews to async (save ~4 hrs/week per team)
  3. Batch admin tasks to Friday afternoon (currently spread across week)

⚠️ FLAGGED
  @sarah: 48 hours logged (potential burnout risk)
  @mike: 32 hours logged (may be underreporting)
```

## Validation Checks
- Confirm time entries are complete for the date range
- Verify billable/non-billable categorizations are accurate
- Check that utilization calculations exclude PTO and holidays
- Flag team members with unusually high or low hours
- Ensure project assignments match current active projects
