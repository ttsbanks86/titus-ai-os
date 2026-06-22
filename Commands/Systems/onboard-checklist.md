# Onboard Checklist

## Purpose
Generate a comprehensive onboarding checklist for a new team member.

## Inputs
- Role and department
- Start date
- Team members they'll work with
- Tools and systems they'll need access to
- Company-specific policies or procedures

## Outputs
- Pre-boarding checklist (before day 1)
- Day 1 checklist
- First week checklist
- 30-day milestones
- 90-day milestones
- Assignments for onboarding buddy/manager

## Workflow
1. Generate pre-boarding items (account setup, equipment, welcome materials)
2. Create day 1 checklist (orientation, introductions, workspace setup)
3. Build first week plan (training, shadowing, initial tasks)
4. Define 30-day milestones (independence, initial contributions)
5. Define 90-day milestones (full integration, performance baseline)
6. Assign responsible parties for each section

## Example Execution
```
/onboard-checklist --role "Software Engineer" --start "June 15, 2026" --team "Engineering" --tools "GitHub,Notion,Slack,Linear"

Output:
━━━ ONBOARDING CHECKLIST: Software Engineer ━━━
Start Date: June 15, 2026 | Buddy: @mike

📦 PRE-BOARDING (Before Day 1)
  | Task                              | Owner    | Due       | Done |
  |-----------------------------------|----------|-----------|------|
  | Create GitHub account             | IT       | June 12   | ☐    |
  | Set up Notion workspace           | PM       | June 13   | ☐    |
  | Create Slack account              | IT       | June 12   | ☐    |
  | Create Linear account             | PM       | June 13   | ☐    |
  | Order laptop and peripherals      | Ops      | June 8    | ☐    |
  | Prepare welcome package           | HR       | June 13   | ☐    |
  | Send team intro email             | Manager  | June 14   | ☐    |

📅 DAY 1 (June 15)
  | Time    | Activity                          | Owner    |
  |---------|-----------------------------------|----------|
  | 9:00    | Welcome & office tour             | Manager  |
  | 10:00   | HR orientation                    | HR       |
  | 11:00   | Tool setup & access verification  | IT       |
  | 12:00   | Team lunch                        | Buddy    |
  | 1:00    | Meet the team (1:1s)              | Manager  |
  | 2:30    | Codebase walkthrough              | Buddy    |
  | 4:00    | First task assignment             | Manager  |

📆 FIRST WEEK (June 15-19)
  | Day    | Focus                  | Activities                        |
  |--------|------------------------|-----------------------------------|
  | Mon    | Orientation            | Setup, meet team, codebase tour   |
  | Tue    | Tooling                | Dev environment, CI/CD, workflows |
  | Wed    | First contribution     | Small bug fix or documentation    |
  | Thu    | Process                | Standup, sprint planning, retros  |
  | Fri    | Review                 | 1:1 with manager, week 1 feedback |

🎯 30-DAY MILESTONES
  - Complete onboarding training modules
  - Make 5+ code contributions
  - Understand team architecture
  - Participate in sprint planning
  - Build relationships with key stakeholders

🎯 90-DAY MILESTONES
  - Work independently on features
  - Participate in code reviews
  - Contribute to sprint planning
  - Complete first project delivery
  - Receive positive peer feedback
```

## Validation Checks
- Confirm all required tool accounts are included
- Verify onboarding buddy is assigned and available
- Check that timeline is realistic for the role
- Ensure 30/90-day milestones are measurable
- Validate that responsible parties are available on the listed dates
