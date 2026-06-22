# SOP Draft

## Purpose
Create a standard operating procedure from a process description.

## Inputs
- Process name and purpose
- Process steps (narrative or bullet form)
- Roles involved
- Tools or systems used
- Frequency (one-time, daily, weekly, monthly, on-demand)
- Compliance requirements (optional)

## Outputs
- Formatted SOP document
- Step-by-step procedure with responsible roles
- Tools and systems reference
- Compliance checklist (if applicable)
- Version history header

## Workflow
1. Gather process details from input
2. Structure into SOP format:
   - Header: Title, version, effective date, owner
   - Purpose statement
   - Scope (who this applies to)
   - Procedure steps with role assignments
   - Tools and systems required
   - Exceptions and edge cases
   - References and related documents
3. Add compliance checkpoints if applicable
4. Include version history and approval section
5. Output in markdown or specified document format

## Example Execution
```
/sop-draft --process "Client Onboarding" --steps "1. Send welcome email 2. Create workspace 3. Schedule kickoff 4. Assign team" --roles "Sales, PM, Engineering" --tools "HubSpot, Notion, Slack"

Output:
━━━ SOP: Client Onboarding ━━━

**Version:** 1.0 | **Effective:** June 7, 2026 | **Owner:** Operations Manager

**Purpose:** Ensure consistent, high-quality onboarding for every new client.

**Scope:** Applies to all new client engagements.

**Procedure:**
| Step | Action                          | Owner   | Tool      | Deadline     |
|------|--------------------------------|---------|-----------|--------------|
| 1    | Send welcome email             | Sales   | HubSpot   | T+0          |
| 2    | Create client workspace        | PM      | Notion    | T+1 business |
| 3    | Schedule kickoff call          | PM      | Calendly  | T+3 business |
| 4    | Assign project team            | PM      | Notion    | T+1 business |
| 5    | Share onboarding packet        | Sales   | Email     | T+0          |
| 6    | Confirm access to all tools    | PM      | Various   | T+5 business |

**Exceptions:**
- Enterprise clients: add legal review step before kickoff
- Retainer clients: skip welcome email, use renewal template

**References:**
- Client Welcome Email Template (Notion)
- Onboarding Packet (Google Drive)
```

## Validation Checks
- Confirm all steps are actionable and specific (no vague instructions)
- Verify role assignments match actual team structure
- Ensure tool names are accurate and currently in use
- Check compliance requirements are addressed if specified
- Validate deadline references are realistic
