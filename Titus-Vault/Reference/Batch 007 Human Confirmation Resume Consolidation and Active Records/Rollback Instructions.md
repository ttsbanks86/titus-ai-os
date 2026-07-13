---
owner: Titus
domain: Reference
status: Active
priority: High
project: TKOS Batch 007
area: Migration
created: 2026-07-12
updated: 2026-07-12
reviewed: 2026-07-12
related:
  - "[[Reference/Batch 007 Human Confirmation Resume Consolidation and Active Records/Completion Report|Batch 007 Completion Report]]"
  - "[[Governance/Migration History|Migration History]]"
tags:
  - tkos/batch-007
  - rollback
---
# Batch 007 Rollback Instructions

## Recovery points

- Pre-Batch 007 validation seal: `7e5efa9`
- Batch 006 evidence checkpoint: `983710f`
- Batch 007 content checkpoint: `1e38dea87e51496fc1ec265534fca9c2394b3391`

## Safe rollback procedure

1. Preserve the current working tree and any unrelated user changes.
2. Inspect the Batch 007 commit before reverting it.
3. Revert only the Batch 007 commit(s) with a new Git revert commit; do not use a destructive reset.
4. Confirm that no source evidence file outside `Titus-Vault` is included in the revert.
5. Reload Obsidian and rerun metadata, unresolved-link, and runtime-error validation.

Batch 007 changed governed Markdown records only. It did not move, rename, overwrite, delete, or import original evidence artifacts.
