# Slack Digest

## Purpose
Summarize Slack channels, highlight action items, and identify blockers.

## Inputs
- Channel list (specific channels or all workspace channels)
- Time range (default: last 24 hours)
- Filter keywords (optional)

## Outputs
- Channel-by-channel summary
- Action items list with owners
- Blockers and flagged messages
- Unread mention highlights

## Workflow
1. Connect to Slack workspace via API or export
2. Pull messages from specified channels within time range
3. For each channel:
   - Summarize key discussion threads
   - Extract action items (look for "TODO", "@mention + task", "I'll handle", "need to")
   - Identify blockers (look for "blocked", "waiting on", "stuck", "issue", "problem")
   - Highlight direct mentions of the user
4. Cross-reference action items to assign owners
5. Compile digest with channel summaries, action items, and blockers

## Example Execution
```
/slack-digest --channels engineering,general --range 24h

Output:
━━━ SLACK DIGEST ━━━

📢 #engineering (47 messages)
  Summary: Discussed deployment pipeline refactor. Three proposals surfaced.
  Action Items:
    • @sarah to prototype GitHub Actions workflow by Thursday
    • @mike to benchmark CircleCI vs Drone
  Blockers:
    ⚠️ Staging DB migration blocked on DevOps credentials

📢 #general (23 messages)
  Summary: Office closure announcement, team lunch planning.
  Action Items:
    • @jess to book restaurant for Friday lunch
  No blockers.

🔥 Your Mentions (3):
  1. @you Can you review the PR? (#engineering)
  2. @you Meeting moved to 3pm (#general)
```

## Validation Checks
- Confirm Slack API token has access to all requested channels
- Verify time range is valid and messages exist for that period
- Ensure action items have identifiable owners
- Flag threads where summary confidence is low for manual review
