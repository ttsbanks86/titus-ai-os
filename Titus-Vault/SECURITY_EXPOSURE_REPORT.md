# Security Exposure Report

## Date: 2026-07-31

## Summary

During the Titus AI OS upgrade, three credentials were found exposed in the Git history:

1. **OpenRouter API Key** - `run_gateway.py`
2. **Hermes Telegram Token** - `run_gateway.py`
3. **Notion API Token** - `Reports/MCP_Installation_Report.md`

## Exposure Details

### OpenRouter API Key
- **File**: `run_gateway.py`
- **Commit**: `6417c4f` (vault migration phase 4-8)
- **Value**: `[REDACTED - see SECRET_ROTATION_REPORT.md]`
- **Status**: REVOKED

### Hermes Telegram Token
- **File**: `run_gateway.py`
- **Commit**: `6417c4f` (vault migration phase 4-8)
- **Value**: `[REDACTED - see SECRET_ROTATION_REPORT.md]`
- **Status**: REVOKED

### Notion API Token
- **File**: `Reports/MCP_Installation_Report.md`
- **Commit**: `6417c4f` (vault migration phase 4-8)
- **Value**: `[REDACTED - see SECRET_ROTATION_REPORT.md]`
- **Status**: REVOKED

## Impact Assessment

- **Duration**: Credentials were in history from initial commit until cleanup
- **Access**: Repository was private, limiting exposure
- **Breach**: No evidence of unauthorized access found
- **Damage**: Low - credentials were for development services

## Remediation

1. All credentials revoked through service dashboards
2. Git history rewritten to remove exposed values
3. New credentials stored in environment variables only
4. Prevention controls implemented

## Additional Findings

### AWS Access Keys in Vault Inventory
- **File**: `01-Dashboard/Vault-Audit-2026-07-12/vault-inventory.csv`
- **Context**: S3 presigned URLs from ChatGPT conversation exports
- **Status**: Likely expired (October 2024 URLs)
- **Action**: Monitoring - not actively used

### Documentation Examples
- **Files**: Archived skill documentation
- **Context**: Example code showing what NOT to do
- **Status**: False positives - not real credentials
- **Action**: None required

## Recommendations

1. Enable GitHub secret scanning on repository
2. Implement pre-commit hooks for local development
3. Regular security audits of Git history
4. Automated credential rotation where possible
