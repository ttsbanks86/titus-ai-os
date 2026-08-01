# Phase 1 Implementation Specification — Titus AI OS

**Date:** 2026-07-31
**Purpose:** Detailed specification for Phase 1 implementation

---

## Executive Summary

Phase 1 focuses on foundational capabilities: test framework, verification automation, sprint system, and baseline telemetry. This is the foundation upon which all subsequent phases build.

**Scope:** Test framework + verification + sprint template + agent health check
**Duration:** 2 weeks
**Effort:** 21 hours

---

## Exact Scope

### In Scope

1. **pytest configuration** — Python test framework
2. **5 unit tests** — Basic test coverage
3. **GitHub Actions workflow** — CI/CD pipeline
4. **Sprint board template** — Markdown-based sprint tracking
5. **Agent health check** — PowerShell monitoring script
6. **Verification dashboard** — Markdown-based status display

### Out of Scope

- Dashboard (Phase 3)
- Branding (Phase 5)
- Advanced memory (Phase 2)
- Security automation (Phase 4)
- Hybrid search (Phase 2)
- MCP integration (deferred)

---

## Architecture

### System Architecture (Phase 1)

```
┌─────────────────────────────────────────────────────────────┐
│                    TITUS AI OS - PHASE 1                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Test Framework                         │   │
│  │    (pytest + unit tests + coverage)                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Verification Layer                     │   │
│  │    (GitHub Actions + pre-commit hooks)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Planning Layer                         │   │
│  │    (Sprint board template + health check)           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Component Details

#### 1. Test Framework

**Technology:** pytest (Python)
**Location:** `tests/` directory
**Configuration:** `pyproject.toml`

**Files:**
- `pyproject.toml` — pytest configuration
- `tests/__init__.py` — Package marker
- `tests/test_vault.py` — Vault operation tests
- `tests/test_agents.py` — Agent system tests
- `tests/test_config.py` — Configuration tests

#### 2. Verification Layer

**Technology:** GitHub Actions
**Location:** `.github/workflows/`

**Files:**
- `.github/workflows/test.yml` — Test pipeline
- `.github/workflows/security.yml` — Security scanning (basic)

#### 3. Planning Layer

**Technology:** Markdown + PowerShell
**Location:** `Titus-Vault/06-Projects/Titus-AI-OS-Upgrade/`

**Files:**
- `SPRINT_BOARD.md` — Sprint tracking template
- `scripts/agent-health-check.ps1` — Agent monitoring
- `VERIFICATION_DASHBOARD.md` — Status display

---

## Files Expected to Change

### New Files

| File | Purpose | Lines |
|------|---------|-------|
| `pyproject.toml` | pytest configuration | ~30 |
| `tests/__init__.py` | Package marker | ~1 |
| `tests/test_vault.py` | Vault tests | ~50 |
| `tests/test_agents.py` | Agent tests | ~50 |
| `tests/test_config.py` | Config tests | ~30 |
| `.github/workflows/test.yml` | CI pipeline | ~40 |
| `.github/workflows/security.yml` | Security scan | ~30 |
| `SPRINT_BOARD.md` | Sprint template | ~50 |
| `scripts/agent-health-check.ps1` | Health check | ~60 |
| `VERIFICATION_DASHBOARD.md` | Status display | ~40 |

**Total new files:** 10
**Total new lines:** ~381

### Modified Files

| File | Change | Lines Changed |
|------|--------|---------------|
| `README.md` | Add test instructions | ~10 |
| `CLAUDE.md` | Add test commands | ~5 |

**Total modified files:** 2
**Total lines changed:** ~15

---

## Test Plan

### Unit Tests

#### 1. Vault Operation Tests (`tests/test_vault.py`)

```python
# Test vault structure
def test_vault_directories_exist():
    """Verify all 10 vault directories exist"""
    pass

def test_vault_index_exists():
    """Verify Home.md exists and is readable"""
    pass

def test_wiki_links_valid():
    """Verify all wiki-links resolve to existing files"""
    pass

def test_frontmatter_valid():
    """Verify YAML frontmatter is valid"""
    pass
```

#### 2. Agent System Tests (`tests/test_agents.py`)

```python
# Test agent configuration
def test_agent_routing_defined():
    """Verify 16 agents are defined in CLAUDE.md"""
    pass

def test_fallback_chains_complete():
    """Verify all agents have fallback chains"""
    pass

def test_safety_guardrails_defined():
    """Verify safety guardrails are documented"""
    pass
```

#### 3. Configuration Tests (`tests/test_config.py`)

```python
# Test system configuration
def test_provider_independence():
    """Verify no single provider is required"""
    pass

def test_cost_optimization():
    """Verify premium models not used for agentic loops"""
    pass

def test_reasoning_chain_defined():
    """Verify mandatory reasoning chain exists"""
    pass
```

### Test Execution

**Command:** `pytest tests/ -v`

**Expected output:**
```
tests/test_vault.py::test_vault_directories_exist PASSED
tests/test_vault.py::test_vault_index_exists PASSED
tests/test_vault.py::test_wiki_links_valid PASSED
tests/test_vault.py::test_frontmatter_valid PASSED
tests/test_agents.py::test_agent_routing_defined PASSED
tests/test_agents.py::test_fallback_chains_complete PASSED
tests/test_agents.py::test_safety_guardrails_defined PASSED
tests/test_config.py::test_provider_independence PASSED
tests/test_config.py::test_cost_optimization PASSED
tests/test_config.py::test_reasoning_chain_defined PASSED

============================== 10 passed in 0.15s ==============================
```

---

## Security Requirements

### Phase 1 Security

1. **No secrets in code** — API keys in environment variables only
2. **No auto-posting** — All external actions require approval
3. **No auto-spending** — No financial transactions without approval
4. **No destructive operations** — Archive before delete
5. **Read-only default** — Write operations require explicit permission

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

## Definition of Done

### Phase 1 Complete When:

- [ ] pytest configured and working
- [ ] 10 unit tests passing
- [ ] GitHub Actions workflow running
- [ ] Sprint board template exists
- [ ] Agent health check script working
- [ ] Verification dashboard exists
- [ ] All changes committed
- [ ] Evidence generated
- [ ] Documentation updated

---

## Evidence Checklist

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

## Rollback Process

### If Phase 1 Fails:

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
   git checkout -- pyproject.toml README.md CLAUDE.md
   ```

4. **Document failure**
   - What failed
   - Why it failed
   - What was learned
   - How to prevent in future

5. **Adjust plan**
   - Modify approach
   - Reduce scope
   - Extend timeline

---

## Estimated Hours

| Task | Hours |
|------|-------|
| pytest configuration | 3 |
| Unit tests (10) | 6 |
| GitHub Actions workflow | 3 |
| Sprint board template | 2 |
| Agent health check | 3 |
| Verification dashboard | 2 |
| Documentation | 1 |
| Integration testing | 1 |
| **Total** | **21** |

---

## Acceptance Criteria

### Must Have

- [ ] pytest runs successfully
- [ ] All 10 tests pass
- [ ] GitHub Actions workflow triggers on push
- [ ] Sprint board template is usable
- [ ] Agent health check script runs
- [ ] Verification dashboard displays status

### Should Have

- [ ] Test coverage reported
- [ ] Pre-commit hooks configured
- [ ] Documentation complete
- [ ] Evidence generated

### Nice to Have

- [ ] Performance benchmarks
- [ ] Additional test cases
- [ ] More detailed health checks

---

## Dependencies

### External Dependencies

| Dependency | Version | Required For |
|------------|---------|--------------|
| Python | 3.11+ | pytest |
| pytest | 7.0+ | Testing |
| GitHub Actions | Latest | CI/CD |
| PowerShell | 5.1+ | Health check |

### Internal Dependencies

| Dependency | Required For |
|------------|--------------|
| Vault structure | Vault tests |
| CLAUDE.md | Agent tests |
| Configuration | Config tests |

---

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| pytest installation fails | High | Low | Use alternative test runner |
| GitHub Actions quota exceeded | Medium | Low | Use local testing |
| PowerShell script errors | Low | Medium | Test on multiple systems |
| Test coverage insufficient | Medium | Medium | Add more tests in Phase 2 |

---

## Conclusion

Phase 1 is ready to begin. The specification is:
- **Clear** — Exact scope and deliverables defined
- **Testable** — Acceptance criteria documented
- **Rollbackable** — Rollback process defined
- **Evidence-based** — Evidence checklist included

**Recommended start date:** Immediately after approval
**Recommended pace:** 2-3 hours per day for 7-10 days
