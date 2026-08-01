# M5 Workflow Analysis

**Milestone 5:** Autonomous Execution Engine
**Phase:** A (Current Workflow Analysis)
**Date:** 2026-08-01
**Status:** ✅ COMPLETE

---

## 1. Purpose

Document every manual step in the current Titus AI OS milestone workflow, classify what can become automatic, and drive the design of the M5 autonomous execution engine. This is the baseline against which M5 success is measured: **the owner should go from many interventions per milestone to zero, except at predefined governance gates.**

## 2. How Titus Works Today (M1–M4 pattern)

The verified pattern from M1 through M4:

1. Owner pastes a full **mission prompt** (objective, phases, success criteria, status vocabulary).
2. CEO agent reads vault records (CURRENT_MILESTONE, PROJECT_STATUS, ROADMAP, SOURCE_OF_TRUTH, daily notes).
3. CEO manually plans phases and writes docs (design → implement → test → document).
4. CEO executes each phase as one continuous session, but the **session has a context window limit** — long milestones risk hitting it mid-work.
5. Verification is done manually (test suites run by hand, evidence collected by hand).
6. Work is committed manually at milestone end, on a docs branch.
7. Owner must approve: pushing the branch, creating the PR, merging the PR, tagging.
8. Owner pastes a **second mission prompt** for the closure workflow (verify merge, tag, sync, records PR).
9. Owner pastes a **third prompt** for the post-closure records PR (push, PR, CI, merge).
10. The cycle repeats for the next milestone.

## 3. Every Manual Approval (current)

| # | Approval | Frequency | Level today | M5 level | Can automate? |
|---|----------|-----------|-------------|----------|---------------|
| 1 | Milestone mission prompt pasted by owner | 1×/milestone | — | — | No — this IS the governance gate |
| 2 | Owner approves M4 branch push | 1×/milestone | HIGH | MEDIUM | Yes after verification |
| 3 | Owner creates/approves PR | 1×/milestone | HIGH | MEDIUM | Yes after CI-green |
| 4 | Owner merges PR | 1×/milestone | HIGH | MEDIUM | Yes (non-breaking docs/features) |
| 5 | Owner approves tag creation | 1×/milestone | HIGH | MEDIUM | Yes |
| 6 | Owner approves records update PR | 1×/milestone | LOW | LOW | Yes |
| 7 | Any external action (post, apply, spend, upload) | ad hoc | CRITICAL | CRITICAL | **Never** — safety rule |
| 8 | Destructive ops (delete, reset, rewrite) | ad hoc | CRITICAL | CRITICAL | **Never** — safety rule |

**Observation:** 6 of 8 approvals are routine bookkeeping that can be gated automatically (verification + CI + diff-scope checks substitute for human review on LOW/MEDIUM work). Only the mission prompt and genuinely risky operations stay human-gated.

## 4. Every Repeated Prompt

| # | Repeated prompt | Cause | M5 automation |
|---|-----------------|-------|---------------|
| 1 | "Continue M4" / "Continue M5" | Session ends mid-milestone | Checkpoint + resume restores state; agent continues from checkpoint |
| 2 | Closure mission prompt (verify merge/tag/sync) | Milestone completion ceremony | Runner performs closure steps automatically after final verification |
| 3 | Post-closure records prompt (PR + merge records) | Docs update ceremony | Runner commits records and raises PR automatically |
| 4 | "What did we do so far?" | Context reload on new session | titus_resume (M4) + Project Memory (M5) restores full context |
| 5 | Re-verification commands | No persistent evidence store | Verification evidence persisted in checkpoints + event log |

## 5. Every Repeated Verification

| # | Verification | Repeated because | M5 fix |
|---|--------------|------------------|--------|
| 1 | Dashboard pytest suite | Run per milestone | Auto-run at sprint gates, evidence persisted |
| 2 | Knowledge engine tests | Run per milestone | Same |
| 3 | Full vault suite | Timed out once | Chunked with retry logic |
| 4 | Theme/plugin/launcher smoke checks | Manual script runs | Engine `verify_sprint()` steps + health checks |
| 5 | Git state checks (clean tree, branch, tags) | Manual commands | `git_state()` verified before every commit |
| 6 | CI status polling | Manual API calls | Engine polls CI run status, proceeds on green |

## 6. Every Repeated Report

| # | Report | Written by | M5 fix |
|---|--------|-----------|--------|
| 1 | M_COMPLETION_REPORT.md | Hand per milestone | Generated from evidence + checkpoint data |
| 2 | Phase docs (analysis/design) | Hand per phase | Templates + engine writing step |
| 3 | FINAL_REPORT.md updates | Hand | Generated summary from milestone state |
| 4 | PROJECT_STATUS / ROADMAP / SOURCE_OF_TRUTH updates | Hand | Engine update step at milestone end |
| 5 | Closure record updates | Hand | Engine post-merge record step |

## 7. Every Unnecessary Interruption

| # | Interruption | Why it happens | M5 fix |
|---|--------------|----------------|--------|
| 1 | Owner must approve routine bookkeeping | No approval-level model | Approval levels: LOW/MEDIUM auto; HIGH/CRITICAL gate |
| 2 | Session ends; work halts | No persistent runner | Runner continues across sessions via checkpoints |
| 3 | Context window pressure | No checkpointing mid-milestone | Checkpoints let work resume with compact context |
| 4 | Manual CI polling | No event engine | Events fire on CI status; runner reacts |
| 5 | Manual git ceremony | No orchestrated git steps | Runner performs commit/branch/PR as queued steps |

## 8. Every Context Reload

| # | Reload | Cost | M5 fix |
|---|--------|------|--------|
| 1 | Session start: read Home, Rules, Goals, daily note | ~5 reads | Project Memory restores once, cached |
| 2 | Mid-milestone resume: re-read all M-docs | Large | Checkpoint restores exact state, no re-read |
| 3 | Dashboard/OpenCode restart | Full re-init | Heartbeat + state files survive restart |
| 4 | Switching projects | Manual vault navigation | Project Memory stores per-project context |

## 9. Classification: What Can Safely Become Automatic

### Automatic (LOW) — no owner interaction
- Documentation updates (records, reports, daily notes)
- Test execution and evidence collection
- Formatting, safe refactoring, linting
- Routine commits (docs, non-breaking changes)
- Report generation from persisted evidence
- CI polling and progress transitions
- Checkpoint creation after every sprint
- Event logging
- Queue processing for LOW tasks

### Automatic after verification (MEDIUM) — proceeds when verification passes
- New modules that pass full test suite
- Safe configuration changes
- Branch push after green verification
- PR creation after diff-scope check (no secrets, docs-only or feature-scoped)
- Merge after CI green AND scope check (no CRITICAL-scope changes)
- Tag creation on verified merge

### Requires owner approval (HIGH)
- Architecture decisions (new layers, engine redesign)
- Security-sensitive changes
- Database/schema changes
- Breaking changes to existing APIs

### Owner approval mandatory (CRITICAL)
- Repository rewrite / force push / history changes
- Credential or API key changes
- Production deployment
- Any external action (post, apply, send, spend, upload)
- Deleting files (archive instead)

## 10. Guardrails Already in Place (reuse, don't duplicate)

From `api/guardrails/` (M2/M3 era, verified):
- `AutomationGuardrails` with `Operation`, `OperationType`, `SafetyLevel`
- Safety levels already exist as a concept — M5 approval model must align with it

From M4:
- `titus_status` / `titus_resume` / `titus_health` plugin tools (read-only)
- Dashboard live vault-read pattern
- Unified launcher with idempotent startup

## 11. Design Consequences for M5

1. **Extend `MilestoneRunner`, don't build a new one.** It already has: milestones, sprints, statuses, safeguards (MAX_RETRIES, TIMEOUT_HOURS, MAX_SPRINTS), save/load state, evidence, report generation. M5 adds: auto sprint transitions, retry execution, persistent checkpoints (with pause/resume/rollback), an execution queue, approval levels, event bus, safety/heartbeat, and project memory — layered on the existing model.
2. **Alignment with guardrails:** M5 approval levels map to existing `SafetyLevel`; CRITICAL operations always route to the existing guardrails module.
3. **Provider independence preserved:** the engine is Python + vault markdown; OpenCode integration via the M4 hybrid plugin pattern (read-only tools + state files), no fork, no external service dependency.
4. **The runner stops only for:** destructive operations, architecture decisions, owner approval gates (HIGH/CRITICAL), failed verification (after retries), security concerns.

## 12. Measure of Success

- M5 itself should demonstrate the model: plan → execute sprints → verify → commit → continue → final report.
- The number of owner interventions for a milestone should drop from ~10 (mission + 6 approvals + closure prompts + records prompt) to **1 (the milestone mission prompt) + CRITICAL-gate approvals only**.
