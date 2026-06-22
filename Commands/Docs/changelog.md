# Changelog

## Purpose
Generate a changelog from git commits, task history, or development activity.

## Inputs
- Source: git repository, task tracker, or manual entries
- Version or date range
- Category filters (features, fixes, breaking changes, etc.)
- Output format (markdown, JSON, release notes)

## Outputs
- Structured changelog grouped by category
- Version tags and dates
- Contributor attributions
- Breaking change warnings

## Workflow
1. Pull commit/task data from specified source
2. Parse and categorize entries:
   - **Added**: New features or capabilities
   - **Changed**: Modifications to existing functionality
   - **Deprecated**: Features being phased out
   - **Removed**: Features or code removed
   - **Fixed**: Bug fixes
   - **Security**: Vulnerability patches
3. Group by version or date
4. Add contributor attributions if available
5. Highlight breaking changes with warnings
6. Format into standard changelog structure

## Example Execution
```
/changelog --source git --range "v2.3.0..v2.4.0" --format markdown

Output:
━━━ CHANGELOG: v2.3.0 → v2.4.0 ━━━

# Changelog

## [2.4.0] - 2026-06-07

### Added
- Real-time collaboration editing (feat #142)
- Dark mode toggle in settings
- Export to PDF functionality
- Webhook support for third-party integrations

### Changed
- Redesigned dashboard layout for better information density
- Upgraded authentication to OAuth 2.1
- Increased file upload limit from 10MB to 50MB

### Fixed
- Resolved intermittent timeout on large file imports (#398)
- Fixed CSV export encoding issue with special characters (#401)
- Corrected timezone display for international users (#405)

### Deprecated
- Legacy API v1 endpoints (will be removed in v3.0)

### Security
- Patched XSS vulnerability in comment rendering (#410)
- Updated dependencies to resolve CVE-2026-1234

---
**Contributors:** @sarah, @mike, @you
**Full diff:** [v2.3.0...v2.4.0](link)
```

## Validation Checks
- Confirm all commits/tasks in the range are included
- Verify version numbers follow semantic versioning
- Ensure breaking changes are clearly flagged
- Check contributor attributions match actual contributions
- Validate date accuracy against commit timestamps
