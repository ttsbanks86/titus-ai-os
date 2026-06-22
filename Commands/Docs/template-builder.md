# Template Builder

## Purpose
Generate a document template from requirements and specifications.

## Inputs
- Document type (proposal, report, brief, contract, etc.)
- Required sections or fields
- Brand guidelines (optional)
- Example or reference document (optional)
- Output format (markdown, Word, PDF, HTML)

## Outputs
- Structured document template
- Placeholder text with instructions
- Section-by-section guidance
- Format-ready file

## Workflow
1. Identify document type and its standard structure
2. Map required sections to the template
3. Add placeholder text with clear instructions for each field
4. Include formatting guidelines and style notes
5. Add conditional sections (if/when applicable)
6. Generate in specified output format
7. Include a "How to Use" header for template consumers

## Example Execution
```
/template-builder --type "proposal" --sections "exec-summary,scope,timeline,pricing,terms" --format markdown

Output:
━━━ TEMPLATE: Client Proposal ━━━

# [Company Name] Proposal for [Client Name]

**Prepared by:** [Your Name]
**Date:** [Date]
**Version:** [1.0]

---

## Executive Summary
[2-3 sentences summarizing what we're proposing, why it matters, and the expected outcome. Be specific to the client's situation.]

## Scope of Work
### In Scope
- [Deliverable 1]: [Brief description]
- [Deliverable 2]: [Brief description]
- [Deliverable 3]: [Brief description]

### Out of Scope
- [Item 1]
- [Item 2]

## Timeline
| Phase         | Duration    | Milestone              |
|---------------|-------------|------------------------|
| Discovery     | [X weeks]   | Requirements sign-off  |
| Build         | [X weeks]   | First draft delivery   |
| Review        | [X weeks]   | Client feedback round  |
| Launch        | [X weeks]   | Go-live                |

## Investment
| Item              | Description          | Cost        |
|-------------------|----------------------|-------------|
| [Service 1]       | [What's included]    | $[Amount]   |
| [Service 2]       | [What's included]    | $[Amount]   |
| **Total**         |                      | **$[Total]**|

## Terms & Conditions
[Standard payment terms, NDA reference, revision policy]

---
*This proposal is valid for 30 days from the date above.*
```

## Validation Checks
- Confirm all required sections are present
- Verify placeholder text is clear and actionable
- Ensure formatting is consistent across sections
- Check that conditional sections are properly marked
- Validate that template matches the specified output format
