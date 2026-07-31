# Rollback Plan — Titus AI OS

**Date:** 2026-07-31
**Version:** 1.0
**Status:** Phase 1

---

## Executive Summary

This document defines the rollback procedures for the Titus AI OS. Rollback ensures that if something goes wrong, we can safely revert to a known good state.

---

## Rollback Principles

1. **Never lose data** — Archive before delete
2. **Always have a backup** — Git provides version control
3. **Test rollback** — Verify rollback works
4. **Document everything** — Record what was rolled back and why

---

## Rollback Levels

### Level 1: File Rollback

**Purpose:** Revert a single file change

**Method:** `git checkout -- <file>`

**When to use:**
- File accidentally modified
- Configuration error
- Test failure

**Example:**
```bash
git checkout -- pyproject.toml
```

---

### Level 2: Commit Rollback

**Purpose:** Revert a single commit

**Method:** `git revert <commit-hash>`

**When to use:**
- Commit introduced bug
- Commit broke tests
- Commit was premature

**Example:**
```bash
git revert a554987
```

---

### Level 3: Phase Rollback

**Purpose:** Revert all changes in a phase

**Method:** `git revert HEAD~N..HEAD` (where N is number of commits)

**When to use:**
- Phase failed completely
- Phase introduced critical issues
- Phase needs to be redone

**Example:**
```bash
# Revert last 5 commits
git revert HEAD~5..HEAD
```

---

### Level 4: Full Rollback

**Purpose:** Revert to initial state

**Method:** `git reset --hard <initial-commit>`

**When to use:**
- Complete failure
- Need to start over
- Critical security issue

**Example:**
```bash
git reset --hard a554987
```

**Warning:** This loses all uncommitted changes!

---

## Phase 1 Rollback Procedures

### Procedure 1: Test Framework Rollback

**Trigger:** pytest configuration fails

**Steps:**
1. Revert pyproject.toml changes
2. Delete tests directory
3. Verify original state

```bash
git checkout -- pyproject.toml
rm -rf tests/
git status
```

---

### Procedure 2: Unit Tests Rollback

**Trigger:** Tests fail and cannot be fixed

**Steps:**
1. Delete test files
2. Revert any modified files
3. Verify original state

```bash
rm -rf tests/
git status
```

---

### Procedure 3: CI Pipeline Rollback

**Trigger:** GitHub Actions workflow fails

**Steps:**
1. Delete workflow file
2. Revert any modified files
3. Verify original state

```bash
rm -rf .github/workflows/
git status
```

---

### Procedure 4: Sprint Infrastructure Rollback

**Trigger:** Sprint board or health check fails

**Steps:**
1. Delete sprint files
2. Revert any modified files
3. Verify original state

```bash
rm SPRINT_BOARD.md
rm scripts/agent-health-check.ps1
rm VERIFICATION_DASHBOARD.md
git status
```

---

### Procedure 5: Full Phase 1 Rollback

**Trigger:** Phase 1 fails completely

**Steps:**
1. Revert all commits in Phase 1
2. Delete all new files
3. Verify original state

```bash
# Find Phase 1 start commit
git log --oneline

# Revert all Phase 1 commits
git revert <start-commit>..HEAD

# Delete any remaining new files
rm -rf tests/
rm -rf .github/workflows/
rm SPRINT_BOARD.md
rm scripts/
rm VERIFICATION_DASHBOARD.md

# Verify clean state
git status
```

---

## Rollback Verification

### After Every Rollback

1. **Check git status** — Confirm clean working tree
2. **Run tests** — Confirm existing functionality works
3. **Check health** — Confirm system is healthy
4. **Document** — Record what was rolled back and why

### Verification Commands

```bash
# Check git status
git status

# Run existing tests (if any)
pytest tests/ -v

# Check health
.\scripts\agent-health-check.ps1

# View git log
git log --oneline -5
```

---

## Rollback Documentation

### What to Record

1. **Timestamp** — When rollback happened
2. **Trigger** — What caused the rollback
3. **Commits reverted** — Which commits were undone
4. **Files deleted** — Which files were removed
5. **Reason** — Why rollback was necessary
6. **Learnings** — What was learned from the failure

### Rollback Log Format

```markdown
# Rollback Log

## Rollback: YYYY-MM-DD HH:MM

**Trigger:** [What caused rollback]
**Commits reverted:** [List commits]
**Files deleted:** [List files]
**Reason:** [Why rollback was needed]
**Learnings:** [What was learned]
**Status:** [Rollback successful/failed]
```

---

## Rollback Testing

### Test Rollback Procedures

Before implementing Phase 1, test that rollback procedures work:

1. **Create test branch**
   ```bash
   git checkout -b test-rollback
   ```

2. **Make test changes**
   ```bash
   echo "test" > test-file.txt
   git add test-file.txt
   git commit -m "test: add test file"
   ```

3. **Rollback changes**
   ```bash
   git revert HEAD
   rm test-file.txt
   ```

4. **Verify rollback**
   ```bash
   git status
   # Should show clean working tree
   ```

5. **Delete test branch**
   ```bash
   git checkout main
   git branch -d test-rollback
   ```

---

## Emergency Rollback

### Critical Failure

If a critical failure occurs:

1. **Stop immediately** — Do not continue
2. **Assess damage** — What is affected?
3. **Execute rollback** — Use appropriate level
4. **Verify** — Confirm system is healthy
5. **Document** — Record everything
6. **Escalate** — Notify user

### Emergency Commands

```bash
# Immediate rollback to last known good
git reset --hard HEAD~1

# Or rollback to specific commit
git reset --hard <commit-hash>

# Clean untracked files
git clean -fd
```

**Warning:** Emergency rollback loses uncommitted changes!

---

## Conclusion

The rollback plan ensures that if anything goes wrong during Phase 1, we can safely revert to a known good state. All rollback procedures have been documented and should be tested before implementation.
