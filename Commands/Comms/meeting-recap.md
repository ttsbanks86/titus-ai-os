# Meeting Recap

## Purpose
Create a meeting summary with action items, owners, and deadlines.

## Inputs
- Meeting transcript, notes, or audio recording
- Attendee list
- Meeting title and date
- Follow-up deadline (optional)

## Outputs
- Meeting summary (3-5 sentences)
- Key decisions made
- Action items with owners and due dates
- Open questions requiring follow-up

## Workflow
1. Ingest meeting content (transcript, notes, or recording)
2. Identify key topics discussed
3. Extract decisions that were made (look for "agreed", "decided", "going with", "approved")
4. Extract action items (look for "will do", "taking", "owner", "due by", "@mention + task")
5. Identify open questions or unresolved items
6. Format into structured recap

## Example Execution
```
/meeting-recap --transcript "meeting-notes-0607.txt" --attendees "Sarah, Mike, You"

Output:
━━━ MEETING RECAP: Q2 Planning Sync ━━━
📅 June 7, 2026 | 👥 Sarah, Mike, You

📝 Summary:
Team aligned on Q2 priorities. Product roadmap finalized with three key launches. Engineering capacity confirmed for all initiatives.

✅ Decisions:
  1. Launch new dashboard by June 30 (approved by Sarah)
  2. Deprecate legacy API v1 by end of Q3
  3. Hire 2 contractors for summer surge

📋 Action Items:
  | Task                        | Owner  | Due      |
  |-----------------------------|--------|----------|
  | Draft contractor JDs        | You    | June 9   |
  | Set up dashboard CI/CD      | Mike   | June 14  |
  | Send stakeholder update     | Sarah  | June 10  |

❓ Open Questions:
  - Budget approval for contractors pending CFO sign-off
  - Which monitoring tool for new dashboard?
```

## Validation Checks
- Confirm all attendees are accounted for
- Verify each action item has an owner and reasonable due date
- Ensure decisions are unambiguous and clearly stated
- Flag any action items with due dates that fall on weekends or holidays
