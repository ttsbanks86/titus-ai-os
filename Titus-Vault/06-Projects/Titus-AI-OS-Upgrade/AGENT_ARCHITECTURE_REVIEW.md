# Agent Architecture Review — Agency Framework Comparison

**Date:** 2026-07-31
**Reviewed Projects:**
- `operand/agency` — Python Actor model framework
- `jenninexus/agency` — Specialized agent personas with audit protocols

---

## Executive Summary

Two distinct "Agency" frameworks were researched. Both offer architectural patterns that can improve the Titus AI OS agent system, but neither should replace our existing architecture wholesale. The best ideas should be merged into our platform.

**Recommendation: Adopt concepts from both, keep our provider-independent foundation.**

---

## Project 1: operand/agency

### Architecture
- **Pattern:** Actor model for agent communication
- **Language:** Python
- **Communication:** LocalSpace (in-process) or AMQPSpace (networked via RabbitMQ)
- **Actions:** Agents expose actions with access policies (PERMITTED, REQUESTED)
- **Callbacks:** before_action, after_action, after_add, before_remove
- **Concurrency:** Multiprocessing and multithreading support

### Key Features
1. **Access Policies** — CONTROLLED, PERMITTED, REQUESTED for action safety
2. **Space-based Communication** — Agents communicate through shared spaces
3. **Action Discovery** — Agents can discover and invoke actions at runtime
4. **Lifecycle Callbacks** — Hooks for agent lifecycle events
5. **AMQP Support** — Networked agent systems across machines

### Strengths
- Clean, minimal API
- Built-in safety through access policies
- Scalable from local to networked
- Good observability through callbacks

### Weaknesses
- No built-in prompt management
- No knowledge/memory integration
- No dashboard or UI
- Python-only (our system is provider/model agnostic)

### Adoptable Concepts
1. **Access Policies** — Implement action-level permissions for agent safety
2. **Space-based Communication** — Use for agent-to-agent messaging
3. **Lifecycle Callbacks** — Add hooks for agent state management

---

## Project 2: jenninexus/agency

### Architecture
- **Pattern:** Specialized agent personas with defined roles
- **Organization:** Agent profiles as markdown files
- **Communication:** Code comments, commit messages, cross-references
- **Audit System:** Weekly audits across 5 core areas
- **MCP Integration:** Server for agent discovery and invocation

### Key Features
1. **Agent Profiles** — Markdown files defining role, personality, ownership
2. **5 Core Audit Areas** — Theme, Layout, Content, Media, SEO/Performance
3. **Weekly Audit Cadence** — Automated scheduled audits
4. **File Ownership** — Each agent owns specific files
5. **Red Flags** — Explicit anti-patterns to catch drift
6. **MCP Server** — Programmatic agent discovery

### Strengths
- Excellent role separation
- Clear ownership model
- Automated quality gates
- MCP integration for tool use
- Visual identity per agent

### Weaknesses
- Focused on web development (design agents)
- No runtime agent execution
- No LLM integration
- Manual audit execution

### Adoptable Concepts
1. **Agent Profiles as Markdown** — Define agents in vault files
2. **File Ownership** — Assign agents to specific vault areas
3. **Audit Cadence** — Schedule automated quality checks
4. **Red Flags** — Define anti-patterns for each agent
5. **MCP Integration** — Expose agents as MCP tools

---

## Our Current System (Titus AI OS)

### Architecture
- **Pattern:** CEO agent orchestrating specialized subagents
- **Communication:** Direct delegation via task tool
- **Memory:** Obsidian vault with wiki-links
- **Model Routing:** Provider-independent fallback chains
- **Skills:** 50+ skills for specialized tasks

### Strengths
- Provider-independent (no vendor lock-in)
- Cost-optimized routing (premium never wasted)
- Rich skill ecosystem
- Vault-based knowledge system
- Strong safety guardrails

### Weaknesses
- No agent-to-agent communication
- No automated audit system
- No agent health monitoring
- No formal agent registry
- No MCP integration
- No visual dashboard

---

## Comparison Matrix

| Feature | operand/agency | jenninexus/agency | Titus AI OS | Winner |
|---------|----------------|-------------------|-------------|--------|
| Role separation | Basic | Excellent | Good | jenninexus |
| Communication | Actor model | Manual | Direct delegation | operand |
| Safety/Permissions | Access policies | Red flags | Guardrails | Tie |
| Knowledge/Memory | None | File ownership | Vault + wiki-links | Titus |
| Model routing | None | None | Provider-independent | Titus |
| Automation | None | Weekly audits | None | jenninexus |
| Dashboard | None | None | None | None |
| MCP Integration | None | Yes | None | jenninexus |
| Scalability | AMQP | Local only | Local only | operand |

---

## Adoption Plan

### Immediate (This Week)

1. **Agent Profiles in Vault** (from jenninexus)
   - Create agent profile markdown files in `08-Agents/`
   - Define role, responsibilities, ownership, red flags
   - Add to vault index

2. **Access Policies** (from operand)
   - Add permission levels to agent actions
   - Implement safety gates for destructive operations
   - Log all agent actions

3. **File Ownership** (from jenninexus)
   - Assign vault areas to specific agents
   - Prevent cross-agent conflicts
   - Track ownership in agent registry

### Short-term (Week 2-3)

4. **Agent Communication** (from operand)
   - Implement message passing between agents
   - Add agent-to-agent delegation
   - Create agent inbox/outbox system

5. **Audit System** (from jenninexus)
   - Define audit checklists per agent
   - Schedule automated audits
   - Generate audit reports

6. **Agent Health Monitoring**
   - Track agent uptime, error rates, response times
   - Create health dashboard
   - Alert on failures

### Medium-term (Week 4-6)

7. **MCP Integration**
   - Expose agents as MCP tools
   - Enable external tool access
   - Build agent discovery service

8. **Dashboard**
   - Build agent status dashboard
   - Show active agents, health, recent actions
   - Integration with vault data

---

## Recommended Agent Architecture

### Tier 1: Orchestration
- **CEO Agent** — Strategic planning, delegation, review
- **Workflow Orchestrator** — Multi-step task execution

### Tier 2: Specialized Executives
- **Architect** — System design, architecture decisions
- **Business Analyst** — Requirements, analysis, documentation
- **Planner** — Sprint planning, task breakdown
- **Project Manager** — Timeline, progress, coordination

### Tier 3: Engineering
- **Developer** — Code implementation
- **Frontend Engineer** — UI/UX implementation
- **Backend Engineer** — API, database, infrastructure
- **QA Engineer** — Testing, verification
- **Security Engineer** — Security review, scanning
- **Documentation Engineer** — Docs, READMEs, guides

### Tier 4: Research & Knowledge
- **Research Agent** — Web research, information gathering
- **Knowledge Curator** — Vault management, organization
- **Code Reviewer** — PR review, quality gates

### Tier 5: Operations
- **Release Manager** — Versioning, changelogs, deployment
- **Performance Engineer** — Optimization, profiling
- **DevOps Engineer** — CI/CD, infrastructure

---

## Implementation Specification

### Agent Profile Template

```markdown
---
agent_id: developer
name: Developer Agent
tier: engineering
status: active
owner: [projects/, src/]
---

# Developer Agent

## Purpose
Implement code features according to specifications.

## Responsibilities
- Write clean, tested code
- Follow coding standards
- Create unit tests
- Document changes

## Tools
- Code editor
- Test runner
- Linter
- Git

## Constraints
- Never commit without tests
- Never push without verification
- Always create PRs for review

## Definition of Done
- Code implements spec
- Tests pass
- Documentation updated
- PR created

## Red Flags
- Skipping tests
- Committing directly to main
- No documentation
```

### Agent Registry

```json
{
  "agents": [
    {
      "id": "ceo",
      "name": "CEO Agent",
      "tier": "orchestration",
      "status": "active",
      "model": "opencode-go/mimo-v2.5"
    },
    {
      "id": "developer",
      "name": "Developer Agent",
      "tier": "engineering",
      "status": "active",
      "model": "opencode-go/mimo-v2.5"
    }
  ]
}
```

### Agent Communication Protocol

```json
{
  "message": {
    "from": "ceo",
    "to": "developer",
    "type": "task",
    "payload": {
      "task": "Implement login feature",
      "spec": "...",
      "deadline": "2026-08-01"
    },
    "priority": "high",
    "timestamp": "2026-07-31T10:00:00Z"
  }
}
```

---

## Benefits

1. **Clearer role separation** — Each agent knows exactly what it owns
2. **Better coordination** — Agent-to-agent communication reduces CEO bottleneck
3. **Automated quality** — Audit system catches drift early
4. **Better observability** — Health monitoring shows system status
5. **MCP integration** — External tools can access our agents

## Trade-offs

1. **Complexity** — More moving parts to maintain
2. **Overhead** — Communication adds latency
3. **Learning curve** — New patterns to understand
4. **Maintenance** — More code to keep updated

## Migration Effort

- **Agent profiles:** 2-3 hours to create all profiles
- **Agent registry:** 4-6 hours to implement
- **Communication layer:** 8-12 hours to implement
- **Audit system:** 6-8 hours to implement
- **Health monitoring:** 4-6 hours to implement
- **Dashboard:** 8-12 hours to implement

**Total estimated effort: 32-47 hours**

## Risks

1. **Over-engineering** — Don't build what we don't need yet
2. **Performance** — Communication overhead could slow things down
3. **Maintenance burden** — More code means more bugs
4. **Complexity** — Harder to understand and debug

## Recommendation

**Adopt incrementally.** Start with agent profiles and file ownership (low effort, high value). Add communication and audit system in phase 2. Defer dashboard and MCP integration until core is solid.

---

## Next Steps

1. Create agent profile templates in vault
2. Implement agent registry
3. Add access policies to agent actions
4. Create audit checklists
5. Build health monitoring
