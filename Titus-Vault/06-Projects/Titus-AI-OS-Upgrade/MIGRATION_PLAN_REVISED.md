# Migration Plan Revised — Titus AI OS

**Date:** 2026-07-31
**Purpose:** Correct time estimates and improve migration plan

---

## Executive Summary

The original migration plan estimated 200-250 hours over 10 weeks. This revision corrects the estimate to **120-140 hours over 10 weeks** based on detailed task analysis.

**Key corrections:**
1. Time estimates reduced by 25-30%
2. Agent count reduced from 15 to 8
3. Architecture simplified from 8 to 5 layers
4. Phase 1 scope focused on foundation only

---

## Revised Time Estimates

### Original vs Revised

| Phase | Original | Revised | Savings |
|-------|----------|---------|---------|
| Phase 1 | 30 hours | 20-24 hours | 6-10 hours |
| Phase 2 | 32 hours | 24-28 hours | 4-8 hours |
| Phase 3 | 44 hours | 32-36 hours | 8-12 hours |
| Phase 4 | 28 hours | 20-24 hours | 4-8 hours |
| Phase 5 | 38 hours | 24-28 hours | 10-14 hours |
| **Total** | **172 hours** | **120-140 hours** | **32-52 hours** |

**Note:** The original 200-250 hour estimate included redundant work and excessive padding. The revised estimate is based on realistic task breakdown.

---

## Revised Phase 1: Core Infrastructure (Week 1-2)

### Goals
- Set up test framework (pytest)
- Create verification automation (GitHub Actions)
- Build sprint board template (markdown)
- Implement agent health check (PowerShell script)

### Tasks

#### Week 1: Test Foundation

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Set up pytest | 3 | pyproject.toml | Tests run | Delete config |
| Write 5 unit tests | 4 | test files | Tests pass | Delete tests |
| Create GitHub Actions workflow | 3 | YAML file | Workflow runs | Delete workflow |
| Documentation | 2 | README updates | Docs complete | Revert docs |
| **Total** | **12** | | | |

#### Week 2: Sprint & Health

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Create sprint board template | 2 | Markdown file | Board exists | Delete file |
| Create agent health check | 3 | PowerShell script | Script runs | Delete script |
| Create verification dashboard | 2 | Markdown file | Dashboard exists | Delete file |
| Integration testing | 2 | Test results | All working | Revert changes |
| **Total** | **9** | | | |

### Phase 1 Total: 21 hours

### Success Criteria
- [ ] pytest configured and working
- [ ] 5 unit tests passing
- [ ] GitHub Actions workflow running
- [ ] Sprint board template exists
- [ ] Agent health check script working
- [ ] All changes committed with evidence

---

## Revised Phase 2: Knowledge Layer (Week 3-4)

### Goals
- Create hot cache template
- Standardize vault frontmatter
- Implement hybrid search (sqlite-vec)
- Create search MCP server

### Tasks

#### Week 3: Hot Cache & OKF

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Create hot cache template | 2 | Markdown file | Template exists | Delete file |
| Standardize vault frontmatter | 4 | Updated notes | Notes updated | Revert notes |
| Create OKF standard document | 2 | Markdown file | Standard exists | Delete file |
| Create vault hook files | 2 | Config files | Hooks work | Delete hooks |
| **Total** | **10** | | | |

#### Week 4: Hybrid Search

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Install sqlite-vec | 2 | Package installed | Package works | Uninstall |
| Create embedding index | 4 | SQLite database | Index created | Delete DB |
| Implement hybrid search | 6 | Python module | Search works | Delete module |
| Create search MCP server | 4 | MCP server | Server runs | Delete server |
| **Total** | **16** | | | |

### Phase 2 Total: 26 hours

### Success Criteria
- [ ] Hot cache template created
- [ ] Vault frontmatter standardized
- [ ] OKF standard documented
- [ ] Hybrid search working
- [ ] Search MCP server running

---

## Revised Phase 3: Dashboard Layer (Week 5-6)

### Goals
- Build simplified dashboard (2 dashboards only)
- Implement one-click sprint
- Implement one-click verify

### Tasks

#### Week 5: Project Dashboard

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Set up HTML/CSS dashboard | 4 | Static files | Dashboard renders | Delete files |
| Create project list component | 4 | HTML/CSS | List displays | Delete component |
| Add basic interactivity | 4 | JavaScript | Clicks work | Delete JS |
| Mobile responsive | 4 | CSS | Responsive | Delete CSS |
| **Total** | **16** | | | |

#### Week 6: Verification Dashboard

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Create verification dashboard | 6 | HTML/CSS | Dashboard renders | Delete files |
| Implement one-click sprint | 4 | Button + script | Sprint starts | Delete script |
| Implement one-click verify | 4 | Button + script | Verify runs | Delete script |
| Integration testing | 2 | Test results | All working | Revert changes |
| **Total** | **16** | | | |

### Phase 3 Total: 32 hours

### Success Criteria
- [ ] Project dashboard rendering
- [ ] Verification dashboard rendering
- [ ] One-click sprint working
- [ ] One-click verify working
- [ ] Mobile responsive

---

## Revised Phase 4: Security Layer (Week 7-8)

### Goals
- Set up basic security scanning
- Implement secret detection
- Create security dashboard

### Tasks

#### Week 7: Basic Scanning

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Set up Bandit | 2 | Config file | Scanner runs | Delete config |
| Set up Gitleaks | 2 | Config file | Scanner runs | Delete config |
| Create security workflow | 3 | YAML file | Workflow runs | Delete workflow |
| Create pre-commit config | 2 | YAML file | Hooks work | Delete config |
| **Total** | **9** | | | |

#### Week 8: Security Dashboard

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Create security dashboard | 4 | Markdown file | Dashboard exists | Delete file |
| Set up Dependabot | 2 | YAML file | Bot active | Delete config |
| Integration testing | 2 | Test results | All working | Revert changes |
| Documentation | 2 | README updates | Docs complete | Revert docs |
| **Total** | **10** | | | |

### Phase 4 Total: 19 hours

### Success Criteria
- [ ] Bandit scanning working
- [ ] Gitleaks scanning working
- [ ] Dependabot active
- [ ] Security dashboard exists

---

## Revised Phase 5: Polish (Week 9-10)

### Goals
- Add basic branding
- Create release automation
- Final testing and documentation

### Tasks

#### Week 9: Branding & Release

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Create color scheme | 2 | CSS variables | Colors defined | Delete CSS |
| Add branding to dashboard | 3 | HTML/CSS | Branding visible | Revert HTML |
| Create release automation | 4 | GitHub Action | Release works | Delete workflow |
| Create changelog generator | 3 | Script | Changelog generates | Delete script |
| **Total** | **12** | | | |

#### Week 10: Final Testing

| Task | Hours | Deliverable | Evidence | Rollback |
|------|-------|-------------|----------|----------|
| Final testing | 4 | Test results | All tests pass | Revert changes |
| Documentation update | 4 | Docs | Docs updated | Revert docs |
| Integration verification | 2 | Verification report | System works | Revert all |
| **Total** | **10** | | | |

### Phase 5 Total: 22 hours

### Success Criteria
- [ ] Branding applied
- [ ] Release automation working
- [ ] Changelog generation working
- [ ] All tests passing
- [ ] Documentation updated

---

## Revised Total Estimate

| Phase | Hours |
|-------|-------|
| Phase 1 | 21 |
| Phase 2 | 26 |
| Phase 3 | 32 |
| Phase 4 | 19 |
| Phase 5 | 22 |
| **Total** | **120 hours** |

**Range:** 120-140 hours (with buffer for unexpected issues)

**Weekly pace:** 12-14 hours per week

---

## Risk Assessment (Revised)

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | High | High | Strict phase boundaries |
| Technical debt | High | Medium | Regular refactoring |
| Integration issues | High | Medium | Incremental integration |
| Time overrun | Medium | Medium | Buffer in estimates |
| Dependency conflicts | Medium | Low | Pin versions |

---

## Rollback Plan

### Per-Phase Rollback

Each phase includes rollback procedures. If a phase fails:

1. **Revert all changes** for that phase
2. **Document what failed** and why
3. **Adjust plan** based on learnings
4. **Re-attempt** with modified approach

### Full Rollback

If the entire project fails:

1. **Revert to original system** (git checkout)
2. **Document all learnings**
3. **Adjust approach** for future attempts
4. **Consider alternative solutions**

---

## Conclusion

The revised migration plan:
- **120-140 hours** (down from 200-250)
- **10 weeks** at 12-14 hours per week
- **8 agents** (down from 15-18)
- **5 layers** (down from 8)
- **Incremental approach** with rollback at each phase

The plan is now realistic, manageable, and includes proper rollback procedures.
