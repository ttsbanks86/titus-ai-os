# File Cleanup

## Purpose
Identify and clean up duplicate, unused, and obsolete files.

## Inputs
- Directory or storage location to scan
- File age thresholds (e.g., files older than 90 days)
- Retention policies (which file types to preserve)
- Duplicate detection criteria (name, content hash, or both)

## Outputs
- Duplicate file groups with recommendations
- Unused files (not accessed in X days)
- Storage savings estimate
- Cleanup action plan
- Before/after storage summary

## Workflow
1. Scan target directory recursively
2. Identify duplicates:
   - Exact matches by content hash
   - Near-duplicates by name similarity
3. Identify unused files:
   - Not accessed in specified time period
   - Not referenced by any active project
4. Apply retention policies (preserve certain file types)
5. Calculate storage savings potential
6. Generate cleanup plan with safety checks

## Example Execution
```
/file-cleanup --path "C:\Projects" --age 90 --retention "keep:*.psd,*.ai" --duplicates hash

Output:
━━━ FILE CLEANUP REPORT: C:\Projects ━━━
Scan Date: June 7, 2026

📊 STORAGE OVERVIEW
  Total Size: 45.2 GB
  Total Files: 3,847
  Scanned Directories: 12

🔴 DUPLICATES FOUND: 23 groups (1.8 GB recoverable)
  | # | Files                     | Size Each | Total Waste | Action      |
  |---|---------------------------|-----------|-------------|-------------|
  | 1 | client-proposal-v2.pdf    | 124 MB    | 372 MB      | Keep latest |
  |   | client-proposal-v2(1).pdf | 124 MB    |             | Delete      |
  |   | client-proposal-v2(COPY).pdf | 124 MB |            | Delete      |
  | 2 | design-mockup.fig         | 89 MB     | 89 MB       | Keep latest |
  |   | design-mockup-old.fig     | 89 MB     |             | Delete      |
  | 3 | data-export-2026.csv      | 45 MB     | 180 MB      | Keep latest |
  |   | data-export-2026(2).csv   | 45 MB     |             | Delete      |
  |   | data-export-2026(3).csv   | 45 MB     |             | Delete      |
  |   | data-export-2026(final).csv | 45 MB  |             | Delete      |

🟡 UNUSED FILES (not accessed in 90+ days): 156 files (890 MB)
  Top candidates for removal:
  | File                            | Last Accessed | Size   |
  |---------------------------------|---------------|--------|
  | old-project-archive.zip         | Jan 12, 2026  | 234 MB |
  | temp-screenshots/ (47 files)    | Feb 3, 2026   | 156 MB |
  | deprecated-api-docs/            | Dec 15, 2025  | 89 MB  |

🟢 RETENTION PROTECTED: 23 files (PSD/AI preserved per policy)

💰 CLEANUP OPPORTUNITY
  Duplicates:    1.8 GB
  Unused files:  890 MB
  Total savings: 2.7 GB (6% of storage)

📋 CLEANUP PLAN
  1. Remove duplicate groups (23 groups, confirm each)
  2. Archive unused files >120 days to cold storage
  3. Delete temp-screenshots/ folder
  4. Review deprecated-api-docs/ for archival

⚠️ SAFETY CHECKS
  - Files marked for deletion will be moved to Recycle Bin first
  - Retention-protected files will NOT be deleted
  - Duplicates will keep the most recently modified version
  - Run: /file-cleanup --execute to apply
```

## Validation Checks
- Confirm scan covers all requested directories
- Verify duplicate detection accuracy (hash-based is exact)
- Ensure retention policies are applied correctly
- Check that "unused" files aren't actually referenced by active projects
- Validate that cleanup plan doesn't delete critical files
