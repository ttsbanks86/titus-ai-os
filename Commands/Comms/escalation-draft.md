# Escalation Draft

## Purpose
Draft a professional escalation message for blockers, risks, or critical issues.

## Inputs
- Issue description or context
- Impact assessment (scope, timeline, cost)
- Escalation recipient (manager, client, stakeholder)
- Desired outcome or resolution requested
- Urgency level (high / critical)

## Outputs
- Escalation message draft
- Impact summary
- Recommended resolution path
- Supporting evidence or data points

## Workflow
1. Clarify the issue: what happened, when, and why it matters
2. Assess impact: who is affected, what is at risk, cost of inaction
3. Identify the escalation recipient and their likely concerns
4. Draft escalation message with:
   - Clear subject line indicating urgency
   - Problem statement (2-3 sentences)
   - Impact and business consequence
   - What has been tried so far
   - Specific ask or resolution requested
   - Deadline or urgency justification
5. Include supporting data points or evidence

## Example Execution
```
/escalation-draft --issue "Payment API integration blocked" --impact "2-week delay to launch" --recipient "CTO" --urgency critical

Output:
━━━ ESCALATION DRAFT ━━━

To: CTO
Subject: [CRITICAL] Payment API Integration Blocked – Launch at Risk

Hi [Name],

I need to escalate a blocker on the Acme payment integration.

**The Issue:**
Third-party payment provider (Stripe) has not provisioned our production API keys despite 3 requests over 10 days. Without these keys, we cannot complete payment flow testing.

**Impact:**
- 2-week delay to June 30 launch
- $45K in projected first-month revenue at risk
- Client trust impact if deadline slips

**What We've Tried:**
- 3 email requests to account manager (no response)
- Support ticket #48291 (opened June 2, no update)
- Attempted to contact via LinkedIn (no connection)

**Ask:**
Can you leverage your relationship with Stripe to expedite key provisioning? Alternatively, should we pivot to a backup processor?

Timeline: Need resolution by June 10 to stay on track.

Happy to jump on a call to discuss.
```

## Validation Checks
- Verify escalation recipient is appropriate for the severity level
- Ensure the issue description is factual and free of emotional language
- Confirm impact assessment is backed by data
- Check that the requested outcome is specific and actionable
- Avoid blaming individuals; focus on systemic issues
