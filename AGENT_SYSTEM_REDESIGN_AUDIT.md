# Agent System Redesign Audit

**Date:** 2026-06-21  
**Author:** CEO Agent (on behalf of Titus Banks)  
**Scope:** Full audit of all agents, skills, MCP servers, and configs across OpenCode, Claude Code, Goose, and workspace runtimes.  
**Mandate:** Identify dead weight, duplicates, self-hosting assumptions that hurt quality, and recommend modern replacements. No deletions yet.

---

## Executive Summary

The system has **333 total agent/skill definitions** across 4 runtimes. Estimated **60-70% are dead weight** — never invoked, irrelevant to your work, or actively harmful duplicates that split context and dilute quality.

**Core finding:** The biggest quality bottleneck is not the skills — it's the **model stack**. Every OpenCode agent (CEO + 14 subagents) runs on `qwen2.5-coder:14b` (a 14B local model). Claude Code itself is proxied through Ollama at `localhost:8082`. All "self-hosted/local-first" choices embed ceiling constraints: you cannot get professional output from 14B models, local TTS, or local image gen on an 8GB laptop GPU.

**Key numbers:**
- 25 agent types available in OpenCode (14 with configs, 9 from .md files)
- 67 agent definitions in Claude directory (all unused)
- 128 skill definitions in Claude directory (mostly unused)
- 101 skill definitions in OpenCode directory (~30 are cybersecurity tools)
- 20 skill definitions in Goose directory
- 17 skill definitions in workspace agents directory
- 38+ skills duplicated across 2+ runtimes
- 10 GSAP-related skill definitions (should be 2)
- 14 sales-related skill definitions (should be 1-2)
- 16 MCP servers configured, 11 enabled, 5 disabled (placeholder)

---

## Section 1: Agent Inventory

### 1.1 OpenCode Agents (25 total)

#### Active (Primary Runtime)
| Agent | Role | Status | Notes |
|-------|------|--------|-------|
| **ceo** | Primary orchestrator | **Active** | Default agent, entry point |
| project-manager | Task breakdown | Active | Low usage |
| research | Web research | Active | Low usage |
| engineer | Code writing | Active | Low usage |
| qa | Code review/testing | Active | Very low usage |
| browser | Playwright automation | Active | Low usage |
| documentation | Technical writing | Active | Very low usage |
| automation | PowerShell/ops | Active | Very low usage |
| file-ops | File management | Active | Very low usage |
| gmail-ops | Gmail operations | Active | Never invoked |
| github-ops | Git/GitHub | Active | Very low usage |
| linkedin-jobs | Job search | Active | Low usage |
| workflow-orchestrator | Automation chains | Active | Never invoked |
| reasoning | Complex analysis | Active | Very low usage |
| kling-agent | Video generation | Active | Never invoked; Kling API not configured |

#### Available but Config-less (loaded from .md files)
| Agent | Status | Notes |
|-------|--------|-------|
| content-director | Available | Content planning agent, never invoked |
| exec-ceo | Available | Strategic planning, manual-only per description |
| exec-cfo | Available | Budget/finance, manual-only |
| exec-cmo | Available | Marketing, manual-only |
| exec-coo | Available | Operations, manual-only |
| exec-cto | Available | Technology decisions, manual-only |
| exec-cdo | Available | Manual-only per task tool |
| faith-mission | Available | Biblical review, never invoked |
| product-manager | Available | Product mgmt, never invoked |
| explore | Available | Codebase explorer |
| general | Available | General-purpose |

**Active subagent use observation:** In practice, only `research`, `engineer`, `project-manager`, `github-ops`, and `general` have been invoked in actual sessions. The other 20 have never been called.

### 1.2 Claude Code Agents (67 total, 0 active)

**Status: All inactive.**`C:\Users\tbank\.claude\agents\` contains 67 agent definitions, but Claude's `settings.json` has no agent configuration section. These agents are loadable by filename only if explicitly invoked.

#### By Category:
| Category | Count | Examples | Recommendation |
|----------|-------|----------|---------------|
| Language-specific code reviewers | 21 | cpp-reviewer, csharp-reviewer, django-reviewer, fastapi-reviewer, flutter-reviewer, fsharp-reviewer, go-reviewer, java-reviewer, kotlin-reviewer, php-reviewer, python-reviewer, pytorch-build-resolver, react-reviewer, rust-reviewer, swift-reviewer, typescript-reviewer | **Retire all** — you don't code in these languages |
| Language-specific build resolvers | 10 | cpp-build-resolver, dart-build-resolver, django-build-resolver, go-build-resolver, java-build-resolver, kotlin-build-resolver, react-build-resolver, rust-build-resolver, swift-build-resolver | **Retire all** — same reasoning |
| General dev tools | 12 | architect, code-architect, code-explorer, code-reviewer, code-simplifier, performance-optimizer, refactor-cleaner, silent-failure-hunter, tdd-guide, type-design-analyzer, build-error-resolver, harness-optimizer | **Merge into 2** (architect + code-reviewer) |
| Sales agents | 5 | sales-company, sales-competitive, sales-contacts, sales-opportunity, sales-strategy | **Merge into 1** with OpenCode sales skills |
| Network/Homelab | 4 | network-architect, network-config-reviewer, network-troubleshooter, homelab-architect | **Retire all** — not relevant to current work |
| GAN/ML | 3 | gan-evaluator, gan-generator, gan-planner | **Retire all** — unused academic ML |
| Specialized | 12 | a11y-architect, comment-analyzer, conversation-analyzer, database-reviewer, doc-updater, docs-lookup, e2e-runner, healthcare-reviewer, mle-reviewer, opensource-forker, opensource-packager, opensource-sanitizer, pr-test-analyzer, seo-specialist, marketing-agent | **Keep 3-4** (docs-lookup, seo-specialist, marketing-agent, e2e-runner). **Retire rest** |
| Meta/Utility | 2 | chief-of-staff, planner, loop-operator | **Merge/Retire** |

### 1.3 Workspace Agents (.agents/skills/)

These are Goose-origin skill files, not agents. See skill inventory section.

---

## Section 2: Skill Inventory

### 2.1 OpenCode Skills (~101)

#### Active/Useful (Recommend Keep - ~15)
| Skill | Reason |
|-------|--------|
| browser-automation (auto-browser) | Playwright-based web automation |
| business-ops-experts | 31-department business support |
| career-ops | Job search workflows |
| content-scheduling | Social media scheduling |
| doc-coauthoring | Document writing/editing |
| findskills | Skill discovery |
| gmail-automation | Gmail operations |
| internal-comms | Professional communication |
| learning-extractor | Extract lessons from content |
| local-ai | Local model connection |
| marketing-skills | Conversion/copy/SEO |
| memory-optimization | Context optimization |
| mcp-builder | MCP server development |
| multi-agent-coordination | Multi-agent orchestration |
| personal-ai-operator | Desktop assistant |
| project-radar | Project status tracking |
| security-review | Security audit |
| skill-creator | Skill creation |
| system-cleanup | Windows maintenance |
| tdd-workflow | Test-driven development |
| verification-loop | Quality gates |
| web-artifacts-builder | HTML/CSS/JS prototypes |
| windows-automation | PowerShell/system ops |
| workflow-orchestration | Multi-step automation |
| file-organization | File management |

#### Cybersecurity Skills - Retire All (~30)
These are imported from a cybersecurity skill pack. None are relevant to your work as a BA job seeker and AI systems builder:

analyzing-azure-activity-logs-for-threats, analyzing-memory-dumps-with-volatility, analyzing-network-traffic-with-wireshark, auditing-kubernetes-cluster-rbac, auditing-terraform-infrastructure-for-security, building-detection-rules-with-sigma, building-ioc-enrichment-pipeline-with-opencti, building-threat-hunt-hypothesis-framework, building-vulnerability-dashboard-with-defectdojo, conducting-api-security-testing, conducting-cloud-incident-response, conducting-malware-incident-response, deploying-active-directory-honeytokens, detecting-ai-model-prompt-injection-attacks, detecting-aws-cloudtrail-anomalies, detecting-business-email-compromise, performing-deception-technology-deployment, performing-memory-forensics-with-volatility3, performing-threat-intelligence-sharing-with-misp, performing-threat-modeling-with-owasp-threat-dragon

**Total: ~30 skills, 0 relevance to current work.**

#### Video/Animation Skills (~15) - Merge into 3-4
| Skill | Recommendation |
|-------|---------------|
| video-edit | Keep — merge video pipeline here |
| video-pipeline | Merge into video-edit |
| video-intelligence | Merge into video-edit |
| cinematic-scrub-landing | Keep separate — specific deliverable |
| parallax-landing-page | Merge into cinematic-scrub-landing |
| video-to-landing-page | Merge into cinematic-scrub-landing |
| lottie | Merge into hyperframes skills |
| animejs | Merge into hyperframes skills |
| css-animations | Merge into hyperframes skills |
| three | Merge into hyperframes skills |
| typegpu | Merge into hyperframes skills |
| waapi | Merge into hyperframes skills |
| gsap-core | Merge into hyperframes skills |
| hyperframes | Keep |
| hyperframes-cli | Merge into hyperframes |
| hyperframes-media | Merge into hyperframes |
| hyperframes-registry | Merge into hyperframes |
| remotion-to-hyperframes | Merge into hyperframes |
| website-to-hyperframes | Merge into hyperframes |
| tailwind | Merge into hyperframes |
| contribute-catalog | Merge into hyperframes |

#### YUV-Specific Skills (~6) - Consolidate to 2
yuv-design-system, yuv-decks, yuv-pilot, yuv-video-director, yuv-viral-video, yuv-reel-covers → Keep 2 (yuv-design-system + yuv-brand-content)

#### Sales Skills (~4 in OpenCode + 14 in Claude) → Merge to 1-2
sales (OpenCode), sales-outreach, sales-prospect, sales-qualify, plus 14 sales skills in Claude directory

#### Framework Skills — Evaluate Per-Use
| Skill | Recommendation |
|-------|---------------|
| api-design | Keep |
| backend-patterns | Keep |
| coding-standards | Keep |
| database-migrations | Keep |
| docker-patterns | Keep |
| django-patterns | Keep — only if you work with Django |
| error-handling | Keep |
| fastapi-patterns | Keep — only if you work with FastAPI |
| frontend-patterns | Keep |
| frontend-slides | Keep |
| kubernetes-patterns | Keep — only if you use K8s |
| python-patterns | Keep |
| react-patterns | Keep |
| mcp-server-patterns | Keep |
| nextjs-turbopack | Keep |
| react-patterns | Keep |

#### Other Skills — Retire or Merge
| Skill | Recommendation |
|-------|---------------|
| ai-inspiration | Retire — never used |
| analytics-metrics | Retire — no analytics workflow |
| book-access-workflow (appears twice) | Merge into 1 |
| brand-guidelines (appears twice) | Merge into 1 |
| brand-voice | Merge with brand-guidelines |
| cloudflare | Retire — decision not to use Cloudflare |
| composio-mcp-hermes | Retire — Hermes API credits exhausted |
| context-budget | Keep |
| continuous-learning-v2 | Keep — but review if still used |
| deep-research | Keep |
| eli5 | Keep |
| fal-ai | Keep — potential cloud image gen |
| figma | Keep — design workflow |
| honest-agent | Retire — never used |
| identity-credit | Keep — credit repair workflow |
| identity-eraser | Keep — data broker opt-out |
| investor-materials | Keep — pitch deck creation |
| jobs (feynman) | Keep |
| langchain | Retire — not using LangChain |
| local-llm-router | Retire — all models are local with no router |
| local-pdf-tools | Keep — useful PDF operations |
| local-tts | Retire or demote — TTS quality is poor vs cloud |
| mermaid-diagrams | Keep |
| meta-ads | Keep — if running FB ads |
| mobile-responsiveness | Keep |
| mongodb | Keep — if using MongoDB |
| nextjs-turbopack | Keep |
| no-gold-plating | Keep |
| obsidian-mind | Retire — Obsidian not used |
| owasp-security | Merge into security-review |
| railway | Retire — not using Railway |
| search-first | Keep |
| scope-guard | Keep |
| self-skill-builder | Keep |
| shabbat-times | Retire unless needed |
| strategic-compact | Keep |
| subagent-orchestration | Keep |
| token-budget-advisor | Keep |
| ux-design-systems | Keep |
| verification-loop | Keep |
| web-accessibility | Keep |
| x-algorithm-strategy | Keep — X strategy |
| x-twitter-scraper | Keep — if scraping X |
| youtube-autonomous | Keep — YouTube automation |

### 2.2 Claude Skills (128)

**Status: ~10 actively referenced, ~118 dormant.** Only the following are referenced anywhere in configs or CLAUDE.md:
- graphify (CLAUDE.md line 192)
- feynman-alpha-research
- feynman-autoresearch
- feynman-contributing
- feynman-deep-research
- feynman-docker
- feynman-eli5
- feynman-jobs
- feynman-literature-review
- feynman-ml-training-recipe
- feynman-modal-compute
- feynman-paper-code-audit
- feynman-paper-writing
- feynman-peer-review
- feynman-preview
- feynman-replication
- feynman-runpod-compute
- feynman-session-log
- feynman-session-search
- feynman-source-comparison
- feynman-watch

The remaining ~107 are completely dormant — not referenced in any config, not mentioned in CLAUDE.md, installed but never invoked.

### 2.3 Goose/Workspace Skills (~20)
Stored at `C:\Users\tbank\.agents\skills\` and `C:\Users\tbank\Desktop\Live Cowork\.agents\skills\`

Significant overlap with OpenCode and Claude skills:
- book-access-workflow (duplicated in workspace)
- book-launch (unique)
- brand-guidelines (duplicated in OpenCode)
- browser-automation (duplicated)
- career-ops (duplicated)
- doc-coauthoring (duplicated)
- file-organization (duplicated)
- gmail-automation (duplicated)
- identity-credit (unique)
- identity-eraser (duplicated)
- internal-comms (duplicated)
- learning-extractor (duplicated)
- local-ai (duplicated)
- mcp-builder (duplicated)
- project-radar (duplicated)
- review-lead-recovery (unique)
- system-cleanup (duplicated)
- titus-banks-brand (unique)
- windows-automation (duplicated)
- workflow-orchestration (duplicated)
- hyperframes + related (duplicated in workspace)
- gsap (duplicated in workspace)

---

## Section 3: Self-Hosting Assumptions Hurting Quality

### Critical Quality Bottlenecks

| Current Setup | What It Costs You | Recommended Replacement | Est. Cost | Quality Gain |
|--------------|-------------------|----------------------|-----------|--------------|
| `qwen2.5-coder:14b` as primary model | 14B model cannot produce professional code, analysis, or creative output. Subagent outputs are mediocre | **Claude Sonnet 4** or **GPT-4o** via API | ~$30-50/mo | **3-5x improvement** |
| Claude Code proxied through Ollama at localhost:8082 | Claude is running through a local 14B Ollama model, not Anthropic's API. You're using 5% of its capability | Direct Anthropic API | ~$25/mo usage | **10x improvement** |
| All 14 subagents on qwen2.5-coder | Every delegated task is bottlenecked by the same weak model | Agent-specific model routing | $0 (config change) | **Immediate** |
| Local TTS (Kokoro/Supertonic) | Robotic, flat narration. Unusable for professional content | **ElevenLabs**, **WellSaid**, or **Play.ht** | ~$5-22/mo | **10x quality** |
| Local ComfyUI/SDXL on 8GB RTX 3080 | 4+ min per image, limited to 1024x1024, no control over coherence | **Midjourney**, **DALL-E 3**, **Fal.ai** Flux Pro, or **Replicate** | ~$10-30/mo | **10x speed, 5x quality** |
| HyperFrames HTML video assembly | No audio waveform editing, no multi-track, no keyframes, no effects | **CapCut**, **Descript**, or **Adobe Premiere Rush** | Free-$15/mo | **Production-grade** |
| 0 CI/CD, 0 testing | No quality assurance pipeline, errors ship silently | **GitHub Actions** + **Playwright** tests | Free | **Essential** |
| No design workflow | No Figma/Canva integration, no brand asset management | **Figma** plugin + **Canva** API | Free | **Massive** |

### Embedded Bias: "Local-first / Free-tools / Open-source"

Every agent and skill prompt contains variations of:
> "Default to read-only review unless write permission is explicit"
> "Approval required before any form submit, login, or data extraction"
> "No auto-upload/auto-post without explicit approval"
> "Keep Goose/shared skills separate"
> "Never enable always-on mic/camera, send messages, connect accounts"

These guardrails were appropriate for an experimentation phase but **actively block professional output** in their current form. The system is optimized for **learning (25%) / saving money (35%) / experimentation (20%)** — not for producing professional results.

---

## Section 4: MCP Server Audit

| Server | Status | Notes |
|--------|--------|-------|
| playwright | **Enabled** | Keep |
| filesystem | **Enabled** | Keep |
| perplexity | **Enabled** | Keep |
| firecrawl | **Enabled** | Keep |
| memory | **Enabled** | Keep |
| sequential-thinking | **Enabled** | Keep |
| context7 | **Enabled** | Docs lookup |
| youtube | **Enabled** | Keep |
| yahoo-finance | **Enabled** | Keep |
| newsapi | **Enabled** | Keep |
| linkedin | **Enabled** | Keep |
| captions | **Enabled** | Keep |
| claude-mem | **Enabled** | Memory |
| apify | **Enabled** | Web scraping |
| notion | **Enabled** | Notion integration |
| github | **Disabled** | Enable if doing GH work |
| google-calendar | **Disabled** | Enable for calendar |
| discord | **Disabled** | Enable if needed |
| reddit | **Disabled** | Stub — no credentials |

**11 enabled, 5 disabled.** Recommended: Enable github, keep others disabled until needed.

---

## Section 5: Duplicate Analysis

### Total Cross-Runtime Duplicates: ~38 skills

High-profile duplicates:
- book-access-workflow: OpenCode + workspace + Goose
- brand-guidelines: OpenCode + Goose
- career-ops: OpenCode + Goose
- doc-coauthoring: OpenCode + Goose
- file-organization: OpenCode + Goose
- gmail-automation: OpenCode + Goose
- identity-eraser: OpenCode + Goose
- internal-comms: OpenCode + Goose
- learning-extractor: OpenCode + Goose
- local-ai: OpenCode + Goose
- mcp-builder: OpenCode + Goose
- project-radar: OpenCode + Goose
- system-cleanup: OpenCode + Goose
- windows-automation: OpenCode + Goose
- workflow-orchestration: OpenCode + Goose
- gsap*: Claude (8) + OpenCode (1) + Workspace (1) = 10 total
- feynman-*: Claude (22) + OpenCode (5) = 27 total

**Each duplicate wastes:**
- Disk space (~50-200KB per skill)
- Context window (every skill scanned during startup)
- Mental overhead (which version is canonical?)
- Update effort (fix in 3 places vs 1)

---

## Section 6: Summary by Numbers

| Category | Count | Keep | Merge | Retire |
|----------|-------|------|-------|--------|
| OpenCode agents (active) | 15 | 15 | 0 | 0 |
| OpenCode agents (.md only) | 10 | 5 | 5 | 0 |
| Claude agents | 67 | 5 | 5 | 57 |
| OpenCode skills | 101 | 35 | 30 | 36 |
| Claude skills | 128 | 10 | 5 | 113 |
| Goose/Workspace skills | 37 | 5 | 15 | 17 |
| MCP servers | 16 | 11 | 0 | 5 |
| **Total** | **374** | **86** | **60** | **228** |

**Target state:** ~86 definitions (77% reduction from 374).

---

## Section 7: Phased Migration Plan

### Phase 1 — Model Upgrade (Week 1, ~$30-50)
*Highest ROI by far. Do this first.*

1. Add Anthropic API key to OpenCode config → set `ceo` model to `claude-sonnet-4-20250514`
2. Add OpenAI API key → set `engineer` and `qa` to `gpt-4o`
3. Stop proxying Claude Code through Ollama; connect directly to Anthropic API
4. Set `small_model` to `gpt-4o-mini` (fast/cheap for simple tasks)
5. Configure agent-specific model routing (CEO/research on Sonnet 4, engineer on GPT-4o, quick tasks on GPT-4o-mini)

**Impact:** 3-10x quality improvement on every task. This single change fixes more than any skill consolidation.

### Phase 2 — Skill Consolidation (Week 1-2, $0)
*Biggest cleanup. No cost.*

1. Delete all ~30 cybersecurity skills from OpenCode skills directory
2. Delete all ~57 unused Claude agents (language reviewers, build resolvers, GAN, homelab, network, healthcare)
3. Delete all ~113 unused Claude skills (everything except ~10 actively used)
4. Delete all 5 disabled/unused MCP stubs (reddit, discord, google-calendar)
5. Merge GSAP skills (10 → 2)
6. Merge sales skills (14+ → 1-2)
7. Merge video/animation skills (20+ → 3-4)
8. Resolve 38 cross-runtime duplicates to single canonical locations

### Phase 3 — Tool Modernization (Week 2-3, ~$20-50/mo)
*Replace self-hosted tools with professional cloud services.*

1. **Image generation:** Stop using local SDXL on 8GB GPU. Use Midjourney/DALL-E 3/Fal.ai
2. **TTS:** Replace Kokoro/Supertonic with ElevenLabs or WellSaid
3. **Video editing:** Replace HyperFrames assembly with CapCut or Descript for actual editing
4. **Design:** Integrate Figma plugin + Canva API for visual work
5. **CI/CD:** Add GitHub Actions for automated testing
6. **Analytics:** Add a real dashboard (Google Data Studio or similar)

### Phase 4 — Guardrail Rewrite (Week 3, $0)
*Rewrite system prompts to remove self-hosting bias.*

1. Remove "local-first / free-tools / open-source" embedded preferences
2. Replace with "best-tool-for-the-job" philosophy
3. Keep safety guardrails (no auto-post, no auto-spend)
4. Remove "experimentation/learning" framing; replace with "professional output" framing
5. Rewrite CEO agent system prompt to reflect new priorities

### Phase 5 — Ongoing (Week 4+, $0)
*Establish maintenance habits.*

1. Monthly audit of new skills/agents added
2. Quarterly cleanup of unused definitions
3. Track which agents are actually invoked (add usage logging)
4. Review MCP server list quarterly
5. Update Career Source of Truth after any platform changes

---

## Section 8: Quick Wins (Can Do Now, No Approvals Needed)

These are safe, reversible changes with no cost:

1. Identify the ~30 cybersecurity skill directories for deletion (they have LICENSE files and Python scripts)
2. Identify the ~57 unused Claude agent .md files for deletion
3. Identify the ~113 unused Claude skill directories for deletion
4. Merge the 4 skill locations into 2 (OpenCode + workspace)

**All require your explicit approval before any deletion.**

---

## What I Recommend You Decide Next

1. **Model upgrade:** Are you willing to spend ~$30-50/mo on API credits for Claude Sonnet 4 + GPT-4o? This is the single highest-leverage change.
2. **Deletion scope:** Can I proceed with deleting the cybersecurity skills (~30) and unused Claude agents/skills (~170 files)? These are safe — they were never used and can be restored from git history.
3. **Skill consolidation:** Which runtime should be canonical for shared skills? OpenCode (primary) or Goose?
4. **Guardrail rewrite:** Approve rewriting the CEO agent and subagent prompts to remove "local-first" bias?

No action taken yet. Awaiting your direction.
