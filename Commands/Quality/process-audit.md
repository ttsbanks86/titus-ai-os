# Process Audit

## Purpose
Audit process compliance and identify improvement opportunities.

## Inputs
- Process name or identifier
- Compliance standards or checklist
- Process documentation (SOP, workflow)
- Audit period
- Sample size or scope

## Outputs
- Compliance score per process step
- Non-compliance findings with severity
- Root cause analysis for gaps
- Improvement recommendations
- Action plan with owners

## Workflow
1. Pull process documentation and expected steps
2. Gather evidence of actual execution (logs, records, interviews)
3. Compare actual vs expected at each step
4. Classify findings:
   - ✅ Compliant: Process followed as documented
   - ⚠️ Partial: Process followed with deviations
   - ❌ Non-compliant: Process step skipped or incorrect
5. For non-compliance, identify root cause (training, tooling, process design)
6. Generate audit report with findings and recommendations
7. Create action plan for remediation

## Example Execution
```
/process-audit --process "Client Onboarding" --period "Q2 2026" --sample 10

Output:
━━━ PROCESS AUDIT: Client Onboarding | Q2 2026 ━━━

📋 AUDIT SCOPE
  Process: Client Onboarding
  Period: April 1 – June 7, 2026
  Sample: 10 of 15 new clients (67%)
  Auditor: Operations AI

📊 COMPLIANCE SCORE: 78%

| Step                       | Expected        | Actual           | Status  |
|----------------------------|-----------------|------------------|---------|
| Welcome email sent         | T+0             | T+0 (avg)        | ✅ 100% |
| Workspace created          | T+1             | T+2.3 (avg)      | ⚠️ 70%  |
| Kickoff scheduled          | T+3             | T+4.1 (avg)      | ⚠️ 60%  |
| Team assigned              | T+1             | T+1.2 (avg)      | ✅ 90%  |
| Onboarding packet shared   | T+0             | T+0              | ✅ 100% |
| Tool access confirmed      | T+5             | T+7.8 (avg)      | ❌ 40%  |

🔴 NON-COMPLIANCE FINDINGS
  1. Workspace creation delayed (70% compliance)
     Root Cause: Notion automation failing for some client types
     Severity: Medium
     Owner: @mike
     Fix: Update automation to handle all client tiers

  2. Tool access delayed (40% compliance)
     Root Cause: No automated process — manual steps missed
     Severity: High
     Owner: @jess
     Fix: Create checklist in onboarding template

💡 IMPROVEMENTS
  1. Automate workspace creation trigger from CRM webhook
  2. Add tool access step to PM checklist (currently only in email)
  3. Create weekly compliance dashboard for onboarding team

📅 ACTION PLAN
  | Action                        | Owner | Due      | Status  |
  |-------------------------------|-------|----------|---------|
  | Fix Notion automation         | Mike  | June 15  | Pending |
  | Add access step to checklist  | Jess  | June 12  | Pending |
  | Build compliance dashboard    | Ops   | June 20  | Pending |
```

## Validation Checks
- Confirm audit sample is representative of the full population
- Verify evidence supports each compliance finding
- Ensure root causes are genuine (not surface-level guesses)
- Check that action items have owners and realistic deadlines
- Validate severity classifications match actual impact
