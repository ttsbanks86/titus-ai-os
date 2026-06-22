# Access Audit

## Purpose
Audit system access permissions and identify security risks.

## Inputs
- System list (SaaS tools, databases, cloud platforms)
- Employee list with roles
- Access matrix or role-based access definitions
- Last access date (optional)

## Outputs
- Access matrix by employee and system
- Over-provisioned access flags
- Under-provisioned access flags
- Unused access (dormant accounts)
- Recommendations for access cleanup

## Workflow
1. Pull current access list from each system
2. Map access against role-based access definitions
3. Identify anomalies:
   - Over-provisioned: Access above role requirements
   - Under-provisioned: Missing required access
   - Dormant: No login in 30+ days
   - Orphaned: Access for deactivated employees
4. Calculate risk score per system
5. Generate audit report with remediation recommendations

## Example Execution
```
/access-audit --systems "GitHub,Notion,Slack,AWS" --employees "engineering-team.csv"

Output:
━━━ ACCESS AUDIT: Engineering Team ━━━
Audit Date: June 7, 2026 | Systems: 4

📊 ACCESS SUMMARY
  | System   | Total Users | Over-Priv | Under-Priv | Dormant | Orphaned |
  |----------|-------------|-----------|------------|---------|----------|
  | GitHub   | 8           | 1         | 0          | 1       | 0        |
  | Notion   | 8           | 2         | 1          | 0       | 0        |
  | Slack    | 8           | 0         | 0          | 0       | 0        |
  | AWS      | 5           | 2         | 0          | 1       | 1        |

🔴 HIGH RISK FINDINGS
  1. AWS: @alex has admin access (role: engineer, should be developer)
  2. AWS: @former-employee still has active credentials (orphaned)
  3. GitHub: @casey has org admin (role: engineer, should be write)

🟡 MEDIUM RISK FINDINGS
  1. Notion: @sarah & @mike have full workspace admin
  2. Notion: @alex missing "Engineering" team access
  3. GitHub: @jess hasn't logged in 45 days (dormant)

🟢 LOW RISK FINDINGS
  1. Slack: All access levels appropriate
  2. Notion: Minor permission discrepancies

📋 REMEDIATION PLAN
  | System   | Action                              | Owner | Priority | Due      |
  |----------|-------------------------------------|-------|----------|----------|
  | AWS      | Remove orphaned credentials         | IT    | Critical | June 8   |
  | AWS      | Downgrade @alex to developer role    | IT    | High     | June 10  |
  | GitHub   | Downgrade @casey to write access     | IT    | High     | June 10  |
  | GitHub   | Review @jess dormant access          | Mgr   | Medium   | June 14  |
  | Notion   | Remove admin from @sarah & @mike     | Ops   | Medium   | June 14  |
  | Notion   | Add @alex to Engineering team        | Ops   | Medium   | June 12  |

📈 RISK SCORE: 6.2/10 (Medium-High)
  Primary concern: AWS orphaned credentials (critical)
```

## Validation Checks
- Confirm all systems in scope are included
- Verify access levels match actual role requirements
- Check that dormant accounts are genuinely unused (not PTO)
- Ensure orphaned accounts are for actually deactivated employees
- Validate that remediation actions don't break required workflows
