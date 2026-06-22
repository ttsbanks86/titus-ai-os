# CRM Sync

## Purpose
Sync lead data with CRM system, ensuring records are accurate and up-to-date.

## Inputs
- CRM system (HubSpot, Salesforce, Pipedrive, or CSV)
- Lead data source (new leads list, enrichment data, or manual entries)
- Sync direction (one-way push, two-way sync, or merge)
- Conflict resolution rules (CRM wins, source wins, newest wins)

## Outputs
- Sync report (created, updated, skipped, errored)
- Data quality issues identified
- Duplicate detection results
- Field mapping confirmation
- Sync audit log

## Workflow
1. Connect to CRM via API or import
2. Map source fields to CRM fields
3. For each lead:
   - Check if record exists (by email or company domain)
   - If exists: compare fields, apply conflict rules, update if needed
   - If new: create record with all available fields
4. Handle duplicates (merge or flag)
5. Validate required fields are populated
6. Generate sync report with statistics
7. Log all changes for audit

## Example Execution
```
/crm-sync --crm hubspot --source "new-leads-june.csv" --direction push --conflicts "newest"

Output:
━━━ CRM SYNC REPORT ━━━
CRM: HubSpot | Source: new-leads-june.csv | Direction: Push

📊 SYNC SUMMARY
  Total leads: 25
  Created: 18
  Updated: 4
  Skipped: 2
  Errors: 1

✅ CREATED (18 records)
  | Company      | Contact           | Email                    | HubSpot ID |
  |--------------|-------------------|--------------------------|------------|
  | DataFlow     | Sarah Chen        | sarah@dataflow.io        | 1001       |
  | CloudSync    | Mike Rodriguez    | mike@cloudsync.com       | 1002       |
  | TechPulse    | Lisa Wang         | lisa@techpulse.io        | 1003       |
  | ...          | ...               | ...                      | ...        |

📝 UPDATED (4 records)
  | Company      | Field Changed     | Old Value     | New Value     |
  |--------------|-------------------|---------------|---------------|
  | AnalyticsPro | Annual Revenue    | $15M          | $22M          |
  | DevStack     | Tech Stack        | HubSpot       | HubSpot, GCP  |
  | DataFlow     | Employee Count    | 60            | 85            |
  | CloudSync    | Last Contact Date | 2026-05-01    | 2026-06-07    |

⏭️ SKIPPED (2 records)
  | Company      | Reason                               |
  |--------------|--------------------------------------|
  | Acme Corp    | Already exists, CRM data is newer    |
  | GlobalCo     | Missing required field (email)       |

❌ ERRORS (1 record)
  | Company      | Error                                |
  |--------------|--------------------------------------|
  | Unknown      | Invalid email format in source data  |

🔍 DUPLICATE DETECTION
  Potential duplicates found: 2
  | Source Record     | CRM Record       | Match Type     | Action Taken  |
  |-------------------|------------------|----------------|---------------|
  | TechPulse (new)   | Tech Pulse Inc.  | Domain match   | Merged        |
  | DevStack (new)    | DevStack Labs    | Email match    | Skipped (CRM) |

📋 FIELD MAPPING
  | Source Field       | CRM Field           | Status |
  |--------------------|---------------------|--------|
  | company_name       | company name        | ✅     |
  | contact_email      | email               | ✅     |
  | contact_name       | name                | ✅     |
  | employee_count     | numberofemployees   | ✅     |
  | annual_revenue     | annualrevenue       | ✅     |
  | tech_stack         | tech_stack (custom) | ✅     |

📈 DATA QUALITY
  Completeness: 94% (1 record missing email)
  Accuracy: 98% (1 invalid email)
  Freshness: 100% (all records from last 30 days)

✅ SYNC COMPLETED: June 7, 2026 10:32 AM
Audit log: crm-sync-2026-06-07.log
```

## Validation Checks
- Confirm all records were processed (no silent drops)
- Verify field mappings are correct and complete
- Check that conflict resolution rules were applied consistently
- Ensure required fields are populated on all created records
- Validate that duplicate detection is accurate (no false merges)
