---
title: Vault Intelligence Audit
date: 2026-07-12
status: review-required
tags:
  - vault/audit
  - knowledge-management
---

# Vault Intelligence & Information Architecture Audit

> [!warning] Audit only
> No existing note was moved, renamed, merged, deleted, or given metadata. Review and approve the migration plan before any migration.

## Executive summary

- Notes inventoried: **6,106**
- Overall health score: **32/100**
- Organization score: **42/100**
- Searchability score: **16/100**
- Knowledge quality score: **97/100**
- Exact duplicate percentage: **0.4%**
- Missing YAML metadata: **50.0%**
- Notes needing classification review: **2,373**
- Estimated cleanup effort: **231 person-hours** (triage estimate)

## Ownership classification

- Uncertain: 1,708
- AI System: 1,189
- Archive: 1,021
- Titus: 911
- Business: 514
- Reference Library: 452
- Shared Family: 303
- Bonolo: 8

## Information categories

- Daily Note: 2,810
- Uncertain: 923
- Education: 370
- Career: 317
- Business: 289
- Archive: 190
- Project: 188
- AI Agent: 184
- Health: 174
- Knowledge: 142
- Certification: 109
- Product: 98
- Finance: 92
- Family: 65
- SOP: 42
- Research: 30
- Reference: 26
- Template: 19
- Meeting: 17
- Goals: 14
- Identity: 7

## Problems found

- Exact duplicate groups: **10** (22 redundant copies)
- Same normalized-name groups: **2,577**
- Conflicting same-name groups: **2,569**
- Empty notes: **1**
- Orphaned notes: **3,514**
- Untagged notes: **3,120**
- Notes without outgoing links: **6,018**
- Potential broken wikilinks: **10,244**
- Unused templates (no backlinks): **3,234**
- Empty folders: **269**
- Large notes (3,000+ words): **894**
- Very small notes (1-40 words): **45**

## Relationship analysis

Most connected notes:

- `[[10-Archive/ChatGPT-Exports/ABOUT ME/PROJECTS/TEMPLATES/OUTPUTS/Resumes/Riipen-AeroCardia/About-Me/Notion Workspace Management/unzuppi/ChatGPT-KnowledgeVault-COMPLETE/Search-Indexes/keyword_index]]` — 2 backlinks, 2285 outgoing
- `[[10-Archive/ChatGPT-Exports/ABOUT ME/PROJECTS/TEMPLATES/OUTPUTS/Resumes/Riipen-AeroCardia/About-Me/Notion Workspace Management/unzuppi/ChatGPT-KnowledgeVault-COMPLETE/Metadata/duplicate_report]]` — 0 backlinks, 285 outgoing
- `[[10-Archive/ChatGPT-Exports/ABOUT ME/PROJECTS/TEMPLATES/OUTPUTS/Resumes/Riipen-AeroCardia/About-Me/Notion Workspace Management/unzuppi/ChatGPT-KnowledgeVault-COMPLETE/Master-Vault/knowledge_graph]]` — 0 backlinks, 225 outgoing
- `[[01-Dashboard/Home]]` — 5 backlinks, 43 outgoing
- `[[09-Knowledge/Knowledge-Index]]` — 17 backlinks, 20 outgoing
- `[[05-Career/Career]]` — 14 backlinks, 10 outgoing
- `[[10-Archive/ChatGPT-Exports/ABOUT ME/PROJECTS/TEMPLATES/OUTPUTS/Resumes/Riipen-AeroCardia/About-Me/Notion Workspace Management/unzuppi/ChatGPT-KnowledgeVault-COMPLETE/Master-Vault/DASHBOARD]]` — 14 backlinks, 9 outgoing
- `[[04-Products/Products]]` — 11 backlinks, 11 outgoing
- `[[09-Knowledge/Marketing/Marketing-Strategy]]` — 12 backlinks, 6 outgoing
- `[[05-Career/Business-Analyst-Path]]` — 9 backlinks, 7 outgoing
- `[[06-Projects/Projects]]` — 9 backlinks, 7 outgoing
- `[[09-Knowledge/Technology/Tech-Stack]]` — 10 backlinks, 5 outgoing
- `[[05-Career/Job-Search]]` — 8 backlinks, 6 outgoing
- `[[09-Knowledge/AI-Business/AI-Business-Models]]` — 1 backlinks, 13 outgoing
- `[[09-Knowledge/Finance/Income-Streams]]` — 7 backlinks, 7 outgoing
- `[[05-Career/Portfolio]]` — 7 backlinks, 6 outgoing
- `[[12-Reference/Reference-Index]]` — 7 backlinks, 6 outgoing
- `[[09-Knowledge/Marketing/Content-Strategy]]` — 7 backlinks, 6 outgoing
- `[[04-Products/Content-Income-System]]` — 7 backlinks, 5 outgoing
- `[[09-Knowledge/AI-Systems/OpenCode-Config]]` — 6 backlinks, 6 outgoing
- `[[09-Knowledge/Brand/Brand-Voice]]` — 6 backlinks, 6 outgoing
- `[[03-Businesses/Business-Ideas]]` — 5 backlinks, 6 outgoing
- `[[03-Businesses/Businesses]]` — 5 backlinks, 6 outgoing
- `[[09-Knowledge/AI-Systems/Provider-Architecture]]` — 6 backlinks, 5 outgoing
- `[[04-Products/NOLA-Voice]]` — 5 backlinks, 5 outgoing

Primary clusters inferred from content and location:

- **Daily Note:** 2,810 notes
- **Uncertain:** 923 notes
- **Education:** 370 notes
- **Career:** 317 notes
- **Business:** 289 notes
- **Archive:** 190 notes
- **Project:** 188 notes
- **AI Agent:** 184 notes
- **Health:** 174 notes
- **Knowledge:** 142 notes
- **Certification:** 109 notes
- **Product:** 98 notes
- **Finance:** 92 notes
- **Family:** 65 notes
- **SOP:** 42 notes
- **Research:** 30 notes
- **Reference:** 26 notes
- **Template:** 19 notes
- **Meeting:** 17 notes
- **Goals:** 14 notes
- **Identity:** 7 notes

Missing-link candidates are concentrated among same-name groups and notes sharing a category but having no links. These require human review because similarity alone does not prove a relationship.

## Proposed architecture

- **Titus-Vault:** Dashboard, Identity, Daily, Projects, Businesses, Career, Education, Knowledge, Journal, Agents.
- **Bonolo-Vault:** Dashboard, Identity, Career, Education, Health, Projects, Daily, Archive.
- **Family-Vault:** Finances, Kids, Household, Vehicles, Travel, Shared Goals, Important Documents, Planning.
- **Businesses:** independent product/company knowledge, separated by business.
- **AI-Systems:** JARVIS, agents, prompts, automations, and AI infrastructure.
- **Reference-Library:** inactive source/reference material.
- **Archive:** obsolete or historical material retained for traceability.

## Quick wins

1. Review the uncertain-owner queue before moving anything.
2. Resolve broken links, beginning with notes that have many backlinks.
3. Add a standard metadata schema to active notes only after classification approval.
4. Review exact duplicates by group; retain the best-connected canonical note.
5. Create evergreen hub notes for repeated idea families instead of adding more fragments.

## Long-term recommendations

- Use one primary owner and one primary category per note.
- Add `owner`, `area`, `status`, `project`, `priority`, `created`, `updated`, `related`, and `tags` properties.
- Require an ownership decision before note creation or migration.
- Prefer updating an evergreen note when an idea already has a durable home.
- Run this audit periodically and compare results over time.

## Deliverables

- [[vault-inventory.csv]] — complete machine-readable inventory.
- [[migration-plan.csv]] — proposed destination, confidence, and risk for every note.
- [[problem-details.md]] — duplicate, broken-link, orphan, empty, large, and merge-candidate details.

## Approval gate

> [!todo] Decision required
> Review the migration plan. No migration should begin until ownership uncertainties and high-risk rows are approved.
