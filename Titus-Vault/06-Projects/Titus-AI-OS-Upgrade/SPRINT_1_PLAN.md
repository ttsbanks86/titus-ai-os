# Sprint 1 Plan — Titus AI OS

**Date:** 2026-07-31
**Sprint:** 1
**Duration:** 1 week
**Effort:** 19 hours

---

## Objective

Establish foundational engineering controls: test framework, verification automation, sprint tracking, and agent health monitoring.

---

## Exact Scope

1. pytest configuration
2. 10 unit tests
3. GitHub Actions workflow
4. Sprint board template
5. Agent health check script
6. Verification dashboard
7. Documentation updates
8. Integration testing

---

## Tasks

### Task 1: pytest Configuration (2 hours)

**Objective:** Set up Python test framework

**Files to change:**
- `pyproject.toml` (modify)
- `tests/__init__.py` (create)
- `tests/conftest.py` (create)

**Acceptance criteria:**
- [ ] pytest installed and configured
- [ ] Test directory structure created
- [ ] `pytest` command runs successfully

**Verification:**
```bash
pytest --version
pytest tests/ -v
```

**Evidence:** Command output showing pytest running

---

### Task 2: Unit Tests (5 hours)

**Objective:** Create 10 meaningful unit tests

**Files to change:**
- `tests/test_vault.py` (create)
- `tests/test_agents.py` (create)
- `tests/test_config.py` (create)

**Acceptance criteria:**
- [ ] 10 tests written
- [ ] All tests pass
- [ ] Tests cover vault, agents, config

**Verification:**
```bash
pytest tests/ -v
```

**Evidence:** Test output showing 10 tests passing

---

### Task 3: GitHub Actions Workflow (3 hours)

**Objective:** Set up CI/CD pipeline

**Files to change:**
- `.github/workflows/test.yml` (create)

**Acceptance criteria:**
- [ ] Workflow file created
- [ ] Workflow triggers on push
- [ ] Tests run in CI

**Verification:**
```bash
git push
# Check GitHub Actions tab
```

**Evidence:** GitHub Actions run showing tests passing

---

### Task 4: Sprint Board Template (2 hours)

**Objective:** Create sprint tracking template

**Files to change:**
- `SPRINT_BOARD.md` (create)

**Acceptance criteria:**
- [ ] Sprint board template exists
- [ ] Template is usable
- [ ] Template follows standard format

**Verification:**
```bash
cat SPRINT_BOARD.md
```

**Evidence:** File content showing sprint board structure

---

### Task 5: Agent Health Check (3 hours)

**Objective:** Create agent monitoring script

**Files to change:**
- `scripts/agent-health-check.ps1` (create)

**Acceptance criteria:**
- [ ] Script created
- [ ] Script runs successfully
- [ ] Script reports agent status

**Verification:**
```powershell
.\scripts\agent-health-check.ps1
```

**Evidence:** Script output showing agent status

---

### Task 6: Verification Dashboard (2 hours)

**Objective:** Create status display

**Files to change:**
- `VERIFICATION_DASHBOARD.md` (create)

**Acceptance criteria:**
- [ ] Dashboard exists
- [ ] Dashboard displays status
- [ ] Dashboard is readable

**Verification:**
```bash
cat VERIFICATION_DASHBOARD.md
```

**Evidence:** File content showing verification status

---

### Task 7: Documentation (1 hour)

**Objective:** Update documentation

**Files to change:**
- `README.md` (modify)

**Acceptance criteria:**
- [ ] Test instructions added
- [ ] Verification commands documented
- [ ] Changes committed

**Verification:**
```bash
git diff README.md
```

**Evidence:** Documentation changes

---

### Task 8: Integration Testing (1 hour)

**Objective:** Verify all components work together

**Acceptance criteria:**
- [ ] All tests pass
- [ ] CI pipeline works
- [ ] Health check works
- [ ] All files committed

**Verification:**
```bash
pytest tests/ -v
.\scripts\agent-health-check.ps1
git status
```

**Evidence:** All verification commands passing

---

## Dependencies

| Task | Depends On |
|------|------------|
| Task 1 | None |
| Task 2 | Task 1 |
| Task 3 | Task 2 |
| Task 4 | None |
| Task 5 | None |
| Task 6 | None |
| Task 7 | Tasks 1-6 |
| Task 8 | Tasks 1-7 |

---

## Files Expected to Change

### New Files

| File | Purpose |
|------|---------|
| `tests/__init__.py` | Package marker |
| `tests/conftest.py` | Test configuration |
| `tests/test_vault.py` | Vault tests |
| `tests/test_agents.py` | Agent tests |
| `tests/test_config.py` | Config tests |
| `.github/workflows/test.yml` | CI pipeline |
| `SPRINT_BOARD.md` | Sprint tracking |
| `scripts/agent-health-check.ps1` | Health check |
| `VERIFICATION_DASHBOARD.md` | Status display |

### Modified Files

| File | Change |
|------|--------|
| `pyproject.toml` | Add pytest config |
| `README.md` | Add test instructions |

---

## Acceptance Criteria

### Sprint 1 Complete When:

- [ ] pytest configured and working
- [ ] 10 unit tests passing
- [ ] GitHub Actions workflow running
- [ ] Sprint board template exists
- [ ] Agent health check script working
- [ ] Verification dashboard exists
- [ ] All changes committed
- [ ] Evidence generated
- [ ] Documentation updated
- [ ] Working tree clean

---

## Test Plan

### Unit Tests

1. `test_vault.py` — 4 tests for vault structure
2. `test_agents.py` — 3 tests for agent configuration
3. `test_config.py` — 3 tests for system configuration

**Total:** 10 tests

### Verification Commands

```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov

# Run health check
.\scripts\agent-health-check.ps1

# Check git status
git status
```

---

## Security Checks

### Before Commit

1. No secrets in code
2. No API keys in files
3. No sensitive data exposed
4. All changes reviewed

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

---

## Evidence Requirements

| Evidence | Location | Verified |
|----------|----------|----------|
| pytest configuration | `pyproject.toml` | [ ] |
| Unit test results | `tests/` output | [ ] |
| GitHub Actions workflow | `.github/workflows/test.yml` | [ ] |
| Sprint board template | `SPRINT_BOARD.md` | [ ] |
| Agent health check | `scripts/agent-health-check.ps1` | [ ] |
| Verification dashboard | `VERIFICATION_DASHBOARD.md` | [ ] |
| Git commit history | `git log` | [ ] |
| Documentation updates | `README.md` | [ ] |

---

## Rollback Procedure

### If Sprint 1 Fails

1. **Revert git changes**
   ```bash
   git revert HEAD
   ```

2. **Delete new files**
   ```bash
   rm -rf tests/
   rm -rf .github/workflows/
   rm SPRINT_BOARD.md
   rm scripts/agent-health-check.ps1
   rm VERIFICATION_DASHBOARD.md
   ```

3. **Restore original files**
   ```bash
   git checkout -- pyproject.toml README.md
   ```

4. **Document failure**
   - What failed
   - Why it failed
   - What was learned

---

## Hour Estimate

| Task | Hours |
|------|-------|
| Task 1: pytest configuration | 2 |
| Task 2: Unit tests | 5 |
| Task 3: GitHub Actions | 3 |
| Task 4: Sprint board | 2 |
| Task 5: Health check | 3 |
| Task 6: Verification dashboard | 2 |
| Task 7: Documentation | 1 |
| Task 8: Integration testing | 1 |
| **Total** | **19** |

---

## Definition of Done

Sprint 1 is complete only when:

1. The correct test framework is installed and configured
2. At least 10 meaningful tests exist
3. All new tests pass
4. Existing functionality still works
5. Continuous integration runs the tests
6. Verification commands are documented
7. Agent health validation works
8. The sprint template is complete
9. Rollback instructions are tested or verified
10. Documentation matches implementation
11. No secrets are exposed
12. The working tree is clean after the final commit
13. The final commit hash is recorded
14. Independent verification confirms the sprint

---

## Next Steps

1. Begin Task 1: pytest configuration
2. Complete tasks in order
3. Verify each task before proceeding
4. Generate evidence for each task
5. Commit after each task completion
6. Report progress daily
