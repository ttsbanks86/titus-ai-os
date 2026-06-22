# Inbox Triage

## Purpose
Scan inbox, categorize emails by priority, and draft responses for urgent items.

## Inputs
- Email source (Gmail, Outlook, or raw email dump)
- Priority rules or labels (optional)
- Response templates (optional)

## Outputs
- Categorized email list (Urgent / Needs Reply / FYI / Newsletter / Spam)
- Draft responses for urgent and reply-required emails
- Summary count per category

## Workflow
1. Ingest email list from source (last 24 hours or specified range)
2. Parse each email: sender, subject, timestamp, body preview
3. Classify each email against priority rules:
   - **Urgent**: Contains deadline, escalation language, or is from key stakeholders
   - **Needs Reply**: Requires action or response from user
   - **FYI**: Informational, no action needed
   - **Newsletter/Marketing**: Bulk-sent content
   - **Spam/Junk**: Irrelevant or phishing attempts
4. For emails marked Urgent or Needs Reply, draft a response using context from the email body
5. Generate summary report with counts and top-priority items

## Example Execution
```
/inbox-triage --source gmail --range 24h

Output:
━━━ INBOX TRIAGE (Last 24h) ━━━
🔴 Urgent (2):
  1. From: CEO - "Board deck review needed by EOD" → Draft: "Got it, reviewing now. Will send by 4pm."
  2. From: Client (Acme) - "Invoice discrepancy" → Draft: "Thanks flagging. Pulling records now, will respond within 2 hours."

🟡 Needs Reply (5):
  3. From: HR - "Benefits enrollment deadline Friday"
  ...

🟢 FYI (12) | ⚪ Newsletter (8) | ❌ Spam (3)
```

## Validation Checks
- Verify email source connection is active
- Ensure no emails were skipped or dropped during parsing
- Confirm drafted responses match the tone and context of the original email
- Flag any emails that could not be classified for manual review
