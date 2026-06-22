# Client Update

## Purpose
Generate a professional client status update from project data.

## Inputs
- Client name or project identifier
- Project data source (PM tool, spreadsheet, or manual notes)
- Update format preference (email, Slack, or document)
- Tone preference (formal, friendly, concise)

## Outputs
- Client status update message
- Progress summary with milestones
- Upcoming milestones and deadlines
- Risks or blockers (if any)

## Workflow
1. Pull project data: tasks completed, in-progress, and upcoming
2. Calculate completion percentage against timeline
3. Identify key accomplishments since last update
4. Flag any blockers, risks, or delays
5. Draft update message in specified tone and format
6. Include: progress, what's next, any asks or flags

## Example Execution
```
/client-update --project "Acme Website Redesign" --format email --tone friendly

Output:
━━━ CLIENT UPDATE: Acme Website Redesign ━━━

Subject: Weekly Update – Acme Website Redesign (June 7)

Hi Team,

Here's your weekly progress update:

✅ Completed This Week:
  • Homepage wireframes approved
  • Content migration for About & Services pages
  • Mobile responsive testing (95% pass rate)

🔄 In Progress:
  • E-commerce integration (60% complete)
  • Brand asset implementation

📅 Coming Up:
  • Design review – June 12
  • Staging site launch – June 18

⚠️ Heads Up:
  • Third-party payment API delayed by 2 days (mitigating with mock)

Overall we're on track for the June 28 delivery. Let me know if you have questions!

Best,
[Your Name]
```

## Validation Checks
- Confirm project data is current (within last 7 days)
- Verify completion percentages are mathematically correct
- Ensure blockers are real and not duplicates of resolved items
- Check tone matches client relationship and communication history
