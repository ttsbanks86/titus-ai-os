# Titus AI Operating System — Architecture Design

**Date:** 2026-07-31
**Version:** 1.0
**Status:** Design Phase

---

## Executive Summary

The Titus AI OS is a production-grade AI operating system built on OpenCode. It combines the best ideas from Agency frameworks, knowledge systems, and security pipelines into a unified platform.

**Core Principles:**
1. Provider-independent (no vendor lock-in)
2. Cost-optimized (premium models never wasted)
3. Vault-based knowledge (human-readable, git-friendly)
4. Safety-first (guardrails, verification, evidence)
5. Incremental adoption (build what we need, when we need it)

---

## System Architecture

### High-Level Overview (5 Layers)

```
┌─────────────────────────────────────────────────────────────┐
│                    TITUS AI OPERATING SYSTEM                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Interface Layer                         │   │
│  │    (Dashboard + Planning + Sprint Board)             │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Intelligence Layer                      │   │
│  │    (Knowledge + Memory + Search + Hot Cache)         │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Orchestration Layer                     │   │
│  │    (CEO Agent + Workflow Engine + Agent Registry)    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Execution Layer                         │   │
│  │    (Code + Testing + Security + Documentation)       │   │
│  └─────────────────────────────────────────────────────┘   │
│                          │                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Integration Layer                       │   │
│  │    (Git + CI/CD + MCP + External Tools)              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Layer 1: Interface Layer

**Purpose:** Visual interface, planning, and sprint management

**Components:**
- **Project Dashboard** — Active projects, progress, milestones
- **Sprint Board** — Current sprint, tasks, velocity
- **Verification Dashboard** — Test results, security scans, evidence
- **Goal Tracker** — Long-term objectives
- **Milestone Tracker** — Project milestones

**Implementation:**
- Markdown-based (Phase 1)
- Web-based dashboard (Phase 3)
- Mobile-responsive design
- Dark/light theme support

### Layer 2: Intelligence Layer

**Purpose:** Knowledge management, memory, and search

**Components:**
- **Vault Storage** — Obsidian vault with wiki-links
- **Hybrid Search** — Vector + keyword search
- **Hot Cache** — Immediate context for sessions
- **Session Memory** — Current session context
- **Long-term Memory** — Persistent knowledge

**Implementation:**
- SQLite with vector embeddings (sqlite-vec)
- OKF frontmatter standard
- File watcher for auto-indexing
- Search-before-answer pattern

### Layer 3: Orchestration Layer

**Purpose:** Agent coordination and task execution

**Components:**
- **CEO Agent** — Strategic planning, delegation, review
- **Workflow Engine** — Multi-step task execution
- **Agent Registry** — Agent profiles, health, capabilities
- **Communication Bus** — Agent-to-agent messaging
- **Audit System** — Automated quality checks

**Implementation:**
- Task queue with priority
- Agent health monitoring
- Automated audit scheduling
- MCP integration for tool access

### Layer 4: Execution Layer

**Purpose:** Code implementation, testing, security, and documentation

**Components:**
- **Developer Agent** — Code implementation
- **QA Agent** — Testing and verification
- **Security Agent** — Security review
- **Documentation Agent** — Docs and guides
- **Release Agent** — Versioning and deployment

**Implementation:**
- Test framework (pytest)
- Linting and formatting
- Type checking
- Evidence collection

### Layer 5: Integration Layer

**Purpose:** External tool and service connectivity

**Components:**
- **Git Integration** — GitHub, GitLab, Bitbucket
- **CI/CD Integration** — GitHub Actions
- **MCP Servers** — Tool access via Model Context Protocol
- **API Gateway** — External service access
- **Webhooks** — Event-driven automation

**Implementation:**
- GitHub API integration
- MCP server/client
- Webhook handlers
- API rate limiting

---

## Threat Model

### Identified Threats

| Threat | Risk | Mitigation |
|--------|------|------------|
| Data exposure | High | Encryption at rest and in transit |
| Privilege escalation | High | Role-based access control |
| Injection attacks | Medium | Input validation and sanitization |
| Denial of service | Medium | Rate limiting and resource limits |
| Supply chain attacks | Medium | Dependency scanning and verification |
| Secrets exposure | High | Never commit secrets, use env vars |
| Unauthorized access | High | Authentication and authorization |
| Data loss | Medium | Regular backups and version control |

### Security Controls

| Control | Implementation |
|---------|----------------|
| Authentication | API keys in environment variables |
| Authorization | Role-based access (agent permissions) |
| Encryption | TLS for network, encryption at rest |
| Logging | Audit trail for all actions |
| Monitoring | Health checks and alerting |
| Backup | Git version control, vault backups |
| Recovery | Rollback procedures documented |

---

## Failure Handling

### Failure Scenarios

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| Agent failure | Health check | Restart agent |
| API failure | Error response | Fallback to alternative |
| Database corruption | Integrity check | Restore from backup |
| Network failure | Timeout | Retry with backoff |
| Deployment failure | Build failure | Rollback to previous |
| Security breach | Alert | Isolate and investigate |

### Recovery Procedures

1. **Agent failure:** Restart agent, replay last task
2. **API failure:** Fall back through provider chain
3. **Database corruption:** Restore from backup, rebuild index
4. **Network failure:** Retry with exponential backoff
5. **Deployment failure:** Rollback to last known good
6. **Security breach:** Isolate, investigate, remediate

---

## Logging

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed diagnostic information |
| INFO | General operational information |
| WARNING | Unexpected but recoverable |
| ERROR | Operation failed |
| CRITICAL | System-level failure |

### Log Format

```
[timestamp] [level] [component] [message] [context]
```

### Log Storage

- **Location:** `logs/` directory
- **Rotation:** Daily
- **Retention:** 30 days
- **Format:** JSON

---

## Audit Trail

### Audited Events

| Event | Data Logged |
|-------|-------------|
| Agent action | Agent ID, action, result, timestamp |
| File change | Path, user, change type, timestamp |
| Security scan | Scanner, results, timestamp |
| Deployment | Version, environment, result, timestamp |
| Configuration change | Setting, old value, new value, timestamp |

### Audit Log Format

```json
{
  "timestamp": "2026-07-31T10:00:00Z",
  "event": "agent.action",
  "agent_id": "developer",
  "action": "code.commit",
  "result": "success",
  "details": {
    "files_changed": 3,
    "tests_passed": true
  }
}
```

---

## Rollback Strategy

### Rollback Triggers

| Trigger | Action |
|---------|--------|
| Test failure | Revert changes |
| Security vulnerability | Revert and fix |
| Performance degradation | Revert and optimize |
| User-reported issue | Revert and investigate |

### Rollback Procedures

1. **Code rollback:** `git revert HEAD`
2. **Database rollback:** Restore from backup
3. **Configuration rollback:** Restore config files
4. **Deployment rollback:** Redeploy previous version

### Rollback Verification

1. Verify rollback completed
2. Run tests to confirm stability
3. Document what was rolled back and why
4. Investigate root cause

---

## Agent Architecture

### Tier 1: Orchestration

| Agent | Purpose | Model | Fallback |
|-------|---------|-------|----------|
| CEO Agent | Strategic planning, delegation | OpenCodeGo | DeepSeek |
| Workflow Orchestrator | Multi-step execution | OpenCodeGo | DeepSeek |

### Tier 2: Specialized Executives

| Agent | Purpose | Model | Fallback |
|-------|---------|-------|----------|
| Architect | System design | OpenCodeGo | DeepSeek |
| Business Analyst | Requirements | OpenCodeGo | DeepSeek |
| Planner | Sprint planning | OpenCodeGo | DeepSeek |
| Project Manager | Timeline, coordination | OpenCodeGo | DeepSeek |

### Tier 3: Engineering

| Agent | Purpose | Model | Fallback |
|-------|---------|-------|----------|
| Developer | Code implementation | OpenCodeGo | DeepSeek |
| Frontend Engineer | UI/UX | OpenCodeGo | DeepSeek |
| Backend Engineer | API, database | OpenCodeGo | DeepSeek |
| QA Engineer | Testing | OpenCodeGo | DeepSeek |
| Security Engineer | Security review | OpenCodeGo | DeepSeek |
| Documentation Engineer | Docs | OpenCodeGo | DeepSeek |

### Tier 4: Research & Knowledge

| Agent | Purpose | Model | Fallback |
|-------|---------|-------|----------|
| Research Agent | Web research | OpenCodeGo | DeepSeek |
| Knowledge Curator | Vault management | OpenCodeGo | DeepSeek |
| Code Reviewer | PR review | OpenCodeGo | DeepSeek |

### Tier 5: Operations

| Agent | Purpose | Model | Fallback |
|-------|---------|-------|----------|
| Release Manager | Versioning | OpenCodeGo | DeepSeek |
| Performance Engineer | Optimization | OpenCodeGo | DeepSeek |
| DevOps Engineer | CI/CD | OpenCodeGo | DeepSeek |

---

## Data Flow

### Task Execution Flow

```
User Request
    ↓
CEO Agent (parse, plan, delegate)
    ↓
Workflow Engine (break into tasks)
    ↓
Agent Registry (select agent)
    ↓
Execution Layer (implement)
    ↓
Verification Layer (test, scan)
    ↓
Evidence Collection (document)
    ↓
Result Delivery
```

### Knowledge Flow

```
User Question
    ↓
Search Layer (hybrid search)
    ↓
Hot Cache (immediate context)
    ↓
Vault (long-term knowledge)
    ↓
Agent (synthesize answer)
    ↓
Write Layer (update knowledge)
    ↓
Index Layer (update search)
```

### Security Flow

```
Code Change
    ↓
Pre-commit Hook (secret detection)
    ↓
PR Creation (triggers CI)
    ↓
Security Scan (static analysis)
    ↓
Dependency Scan (vulnerability check)
    ↓
Code Review (automated + human)
    ↓
Merge (if passes)
    ↓
Deploy (if main branch)
```

---

## Dashboard Design

### Project Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT DASHBOARD                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Active     │  │  Milestones │  │  Velocity   │        │
│  │  Projects   │  │  Progress   │  │  Trend      │        │
│  │     5       │  │    72%      │  │   +15%      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   PROJECT LIST                       │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Project      │ Status    │ Progress │ Next Milestone│   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Titus AI OS  │ Active    │ 45%      │ Dashboard v1  │   │
│  │ CareNotes    │ Planning  │ 10%      │ MVP           │   │
│  │ Content Sys  │ Active    │ 60%      │ Automation    │   │
│  │ Portfolio    │ Active    │ 80%      │ Final Review  │   │
│  │ Ministry     │ Research  │ 20%      │ Strategy      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Sprint Board

```
┌─────────────────────────────────────────────────────────────┐
│                     SPRINT BOARD                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sprint 12: Jul 28 - Aug 11 (Day 4/14)                     │
│  Velocity: 42 points | Remaining: 28 points                 │
│                                                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │
│  │   BACKLOG │  │   TO DO   │  │ IN PROGRESS│  │  DONE   │ │
│  ├───────────┤  ├───────────┤  ├───────────┤  ├─────────┤ │
│  │ [8] Doc   │  │ [5] Search│  │ [13] Dash │  │ [3] Hot │ │
│  │ [5] Test  │  │ [3] Index │  │   board   │  │   Cache │ │
│  │ [3] Auth  │  │           │  │           │  │ [5] OKF │ │
│  └───────────┘  └───────────┘  └───────────┘  └─────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Agent Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT DASHBOARD                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   Active    │  │   Healthy   │  │  Tasks      │        │
│  │   Agents    │  │   Status    │  │  Completed  │        │
│  │     12      │  │    100%     │  │    156      │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   AGENT STATUS                       │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Agent        │ Status  │ Tasks │ Errors │ Last Active│   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ CEO          │ Active  │   45  │   0    │ 2 min ago  │   │
│  │ Developer    │ Active  │   32  │   2    │ 5 min ago  │   │
│  │ QA           │ Active  │   28  │   1    │ 8 min ago  │   │
│  │ Security     │ Active  │   15  │   0    │ 12 min ago │   │
│  │ Research     │ Idle    │   18  │   0    │ 1 hr ago   │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Verification Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                   VERIFICATION DASHBOARD                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    Tests    │  │  Security   │  │  Coverage   │        │
│  │   Passing   │  │    Clear    │  │    87%      │        │
│  │   142/142   │  │  0 Critical │  │             │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 RECENT EVIDENCE                      │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Time       │ Type      │ Status  │ Details          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 10:30 AM   │ Tests     │ Pass    │ 142/142 tests    │   │
│  │ 10:28 AM   │ Security  │ Clear   │ No vulnerabilities│  │
│  │ 10:25 AM   │ Lint      │ Pass    │ 0 errors         │   │
│  │ 10:20 AM   │ Build     │ Success │ Deployed to dev  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1-2)

**Goals:**
- Set up test framework
- Create verification automation
- Build sprint system
- Implement agent health monitoring

**Deliverables:**
- Jest/Vitest configuration
- pytest configuration
- GitHub Actions workflows
- Sprint board markdown
- Agent health check script

### Phase 2: Knowledge Layer (Week 3-4)

**Goals:**
- Integrate hybrid search
- Build hot cache system
- Create knowledge dashboard
- Implement auto-indexing

**Deliverables:**
- SQLite vector index
- Hot cache template
- Search MCP server
- Knowledge dashboard

### Phase 3: Dashboard Layer (Week 5-6)

**Goals:**
- Build project dashboard
- Create verification dashboard
- Implement one-click workflows
- Build agent dashboard

**Deliverables:**
- React/Vue dashboard
- WebSocket real-time updates
- Mobile-responsive design
- Dark/light themes

### Phase 4: Security Layer (Week 7-8)

**Goals:**
- Set up security scanning
- Implement dependency scanning
- Add secret detection
- Build security dashboard

**Deliverables:**
- GitHub Actions security workflows
- Pre-commit hooks
- Security dashboard
- Compliance reports

### Phase 5: Polish (Week 9-10)

**Goals:**
- Add Titus branding
- Create custom themes
- Build release automation
- Implement changelog generation

**Deliverables:**
- Custom logos and colors
- Theme system
- Release automation
- Changelog generation

---

## Success Criteria

1. **All tests pass** — 100% test coverage for critical paths
2. **Security scans pass** — No critical vulnerabilities
3. **Documentation updated** — All features documented
4. **Evidence generated** — Every change has verification evidence
5. **Working tree clean** — No uncommitted changes
6. **Independent verification** — Someone else can run the system
7. **Performance acceptable** — Dashboard loads in <2s, search in <500ms
8. **User can operate** — Titus can use the system without assistance

---

## Next Steps

1. Review and approve architecture
2. Create implementation plan
3. Set up development environment
4. Begin Phase 1 implementation
5. Weekly progress reviews
