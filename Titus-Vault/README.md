# Titus AI OS — Knowledge Base

**Version:** 0.1.0
**Status:** Phase 1 Complete

---

## Overview

This is the knowledge base for the Titus AI Operating System. It contains documentation, configurations, and operational procedures.

---

## Directory Structure

```
Titus-Vault/
├── 01-Dashboard/          # Home, goals, rules
├── 02-Daily-Notes/        # Daily logs
├── 03-Businesses/         # Business documents
├── 04-Products/           # Product documentation
├── 05-Career/             # Career resources
├── 06-Projects/           # Active projects
├── 07-SOPs/               # Standard operating procedures
├── 08-Agents/             # Agent profiles
├── 09-Knowledge/          # Domain knowledge
├── 10-Archive/            # Archived files
├── 11-Templates/          # Document templates
├── 12-Reference/          # Reference materials
├── tests/                 # Test suite
├── scripts/               # Utility scripts
└── .github/workflows/     # CI/CD pipelines
```

---

## Quick Start

### Run Tests

```bash
pytest tests/ -v
```

### Run Health Check

```powershell
.\scripts\agent-health-check.ps1
```

### View Verification Dashboard

```bash
cat VERIFICATION_DASHBOARD.md
```

---

## Testing

### Test Framework

- **Framework:** pytest
- **Version:** 9.1.1
- **Python:** 3.13.2

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov

# Run specific test file
pytest tests/test_vault.py -v
```

### Test Structure

```
tests/
├── __init__.py        # Package marker
├── conftest.py        # Test configuration
├── test_vault.py      # Vault structure tests
├── test_agents.py     # Agent configuration tests
└── test_config.py     # System configuration tests
```

---

## CI/CD

### GitHub Actions

**Workflow:** `.github/workflows/test.yml`

**Triggers:**
- Push to main/develop
- Pull request to main

**Jobs:**
- Run tests
- Generate coverage report

---

## Scripts

### Agent Health Check

**Location:** `scripts/agent-health-check.ps1`

**Usage:**
```powershell
.\scripts\agent-health-check.ps1
.\scripts\agent-health-check.ps1 -Verbose
```

**Output:**
- Agent status
- Health summary
- Check timestamp

---

## Documentation

### Key Files

| File | Purpose |
|------|---------|
| `01-Dashboard/Home.md` | Vault index |
| `01-Dashboard/My-Goals.md` | Goals and priorities |
| `07-SOPs/SOPs-Index.md` | Standard procedures |
| `08-Agents/Agents-Index.md` | Agent profiles |
| `SPRINT_BOARD.md` | Sprint tracking |
| `VERIFICATION_DASHBOARD.md` | Status display |

---

## Contributing

### Adding Tests

1. Create test file in `tests/`
2. Follow naming convention: `test_*.py`
3. Use pytest fixtures from `conftest.py`
4. Run tests before committing

### Updating Documentation

1. Follow markdown standards
2. Use wiki-links for cross-references
3. Update relevant index files

---

## License

MIT

---

## Contact

**Titus Banks** — Project Owner
