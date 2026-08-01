# Verification Strategy — Titus AI OS

**Date:** 2026-07-31
**Version:** 1.0
**Status:** Phase 1

---

## Executive Summary

This document defines the verification strategy for the Titus AI OS. Verification ensures that every deliverable meets quality standards before marking complete.

---

## Verification Levels

### Level 1: Command Verification (Phase 1)

**Purpose:** Confirm commands execute successfully

**Method:** Run commands and check output

**Examples:**
- `pytest tests/ -v` — Tests pass
- `git status` — Working tree clean
- `.scripts/agent-health-check.ps1` — Script runs

---

### Level 2: Output Verification (Phase 1)

**Purpose:** Confirm outputs match expectations

**Method:** Compare actual output to expected output

**Examples:**
- Test count matches expected
- File contents match specification
- Configuration is valid

---

### Level 3: Integration Verification (Phase 2)

**Purpose:** Confirm components work together

**Method:** Run end-to-end workflows

**Examples:**
- Agent delegation works
- Knowledge retrieval works
- Sprint execution works

---

## Verification Commands

### Test Verification

```bash
# Run all tests
pytest tests/ -v

# Expected output:
# tests/test_vault.py::test_vault_directories_exist PASSED
# tests/test_vault.py::test_vault_index_exists PASSED
# ...
# 10 passed in 0.15s
```

---

### Git Verification

```bash
# Check working tree
git status

# Expected output:
# nothing to commit, working tree clean

# Check commit history
git log --oneline -5

# Expected output:
# <hash> feat: add Phase 1 test infrastructure
# <hash> ...previous commits...
```

---

### Health Check Verification

```powershell
# Run health check
.\scripts\agent-health-check.ps1

# Expected output:
# Agent Health Status
# ==================
# CEO Agent: OK
# Developer Agent: OK
# QA Agent: OK
# ...
# All agents healthy
```

---

## Verification Checklist

### Phase 1 Verification

| Item | Command | Expected Result | Verified |
|------|---------|-----------------|----------|
| pytest installed | `pytest --version` | Version displayed | [ ] |
| Tests pass | `pytest tests/ -v` | 10 tests pass | [ ] |
| CI configured | `.github/workflows/test.yml` | File exists | [ ] |
| Sprint board exists | `cat SPRINT_BOARD.md` | Content displayed | [ ] |
| Health check works | `.\scripts\agent-health-check.ps1` | Status displayed | [ ] |
| Verification dashboard | `cat VERIFICATION_DASHBOARD.md` | Content displayed | [ ] |
| Working tree clean | `git status` | Nothing to commit | [ ] |
| Documentation updated | `git diff README.md` | Changes shown | [ ] |

---

## Evidence Collection

### What to Capture

1. **Command output** — Copy terminal output
2. **File contents** — Show file exists and is correct
3. **Git history** — Show commits
4. **Test results** — Show test output

### How to Capture

1. **Screenshots** — For visual verification
2. **Command output** — Copy/paste terminal
3. **File listing** — Show directory structure
4. **Git log** — Show commit history

### Where to Store

1. **SPRINT_1_EVIDENCE.md** — Main evidence file
2. **Git commits** — Permanent record
3. **GitHub Actions** — CI/CD evidence

---

## Verification Gates

### Gate 1: Test Framework

**Criteria:**
- [ ] pytest installed
- [ ] Tests directory exists
- [ ] `pytest` command works

**Gate passes when:** All criteria met

---

### Gate 2: Unit Tests

**Criteria:**
- [ ] 10 tests written
- [ ] All tests pass
- [ ] Tests cover vault, agents, config

**Gate passes when:** All criteria met

---

### Gate 3: CI Pipeline

**Criteria:**
- [ ] Workflow file exists
- [ ] Workflow triggers on push
- [ ] Tests run in CI

**Gate passes when:** All criteria met

---

### Gate 4: Sprint Infrastructure

**Criteria:**
- [ ] Sprint board template exists
- [ ] Health check script works
- [ ] Verification dashboard exists

**Gate passes when:** All criteria met

---

### Gate 5: Final Verification

**Criteria:**
- [ ] All tests pass
- [ ] Working tree clean
- [ ] Documentation updated
- [ ] Evidence collected

**Gate passes when:** All criteria met

---

## Verification Report Format

```markdown
# Verification Report

**Date:** YYYY-MM-DD
**Sprint:** 1
**Verifier:** [Name]

## Results

| Item | Status | Evidence |
|------|--------|----------|
| Tests pass | PASS | [output] |
| CI works | PASS | [link] |
| Health check | PASS | [output] |
| Working tree | CLEAN | [git status] |

## Conclusion

Sprint 1 verification: PASS/FAIL

**Evidence:** [List evidence files]
```

---

## Conclusion

The verification strategy ensures that every deliverable is validated before marking complete. Phase 1 focuses on command and output verification, with integration verification in subsequent phases.
