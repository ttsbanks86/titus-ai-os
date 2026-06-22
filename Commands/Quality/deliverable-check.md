# Deliverable Check

## Purpose
Validate a deliverable against a requirements checklist before submission.

## Inputs
- Deliverable (file, document, or link)
- Requirements checklist or acceptance criteria
- Stakeholder expectations (optional)
- Quality standards or brand guidelines (optional)

## Outputs
- Pass/Fail status for each requirement
- Overall readiness score
- Issues and gaps identified
- Remediation suggestions
- Go/No-Go recommendation

## Workflow
1. Ingest deliverable and requirements checklist
2. For each requirement:
   - Check if the deliverable meets the criterion
   - Assign status: ✅ Pass, ⚠️ Partial, ❌ Fail
   - Add notes for partial or failed items
3. Calculate overall readiness score (pass / total requirements)
4. Identify critical failures vs nice-to-haves
5. Generate remediation suggestions for failed items
6. Provide Go/No-Go recommendation

## Example Execution
```
/deliverable-check --file "acme-proposal-v3.pdf" --checklist "proposal-requirements.md"

Output:
━━━ DELIVERABLE CHECK: Acme Proposal v3 ━━━

📋 REQUIREMENTS CHECKLIST

| # | Requirement                      | Status | Notes                    |
|---|----------------------------------|--------|--------------------------|
| 1 | Executive summary included       | ✅     | —                        |
| 2 | Scope clearly defined            | ✅     | —                        |
| 3 | Timeline with milestones         | ✅     | —                        |
| 4 | Pricing breakdown                | ⚠️     | Missing line items       |
| 5 | Terms and conditions             | ✅     | —                        |
| 6 | Case studies (2 minimum)         | ❌     | Only 1 included          |
| 7 | Client-specific customization    | ✅     | —                        |
| 8 | Brand guidelines compliance      | ⚠️     | Font size off on headers |
| 9 | Proofread for errors             | ❌     | 3 typos found            |
|10 | PDF format, max 10 pages         | ✅     | 8 pages                  |

📊 SCORE: 6/10 (60%)

🔴 CRITICAL ISSUES (must fix before submission)
  1. Case study missing — add 1 more relevant example
  2. Typos found on pages 2, 5, 7 — run spell check

🟡 MINOR ISSUES (fix if time permits)
  1. Add pricing line items for clarity
  2. Adjust header font size to match brand guide

🚦 RECOMMENDATION: NO-GO
  Fix 2 critical issues before submission. Estimated fix time: 45 minutes.
```

## Validation Checks
- Confirm deliverable file is accessible and readable
- Verify checklist is complete and each item is testable
- Ensure status assessments are objective (not subjective)
- Check that critical issues are genuinely blocking
- Validate that remediation suggestions are actionable
