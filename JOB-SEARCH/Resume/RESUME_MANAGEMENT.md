# Resume Management Workflow
**Titus Banks - Job Search System**
**Created:** June 6, 2026
**Status:** Active

---

## Purpose

This document defines how Titus Banks manages resumes across two AI systems:
- **Claude (browser at claude.ai)** - primary tool for narrative editing, content review, and content polishing
- **OpenCode (this CLI)** - primary tool for file organization, version control, job-tailoring, and tracker updates

Both systems share the same source-of-truth folder on disk. The goal is to keep one version of the truth, prevent drift, and make resume editing fast and auditable.

---

## Folder Map (Source of Truth)

```
C:\Users\tbank\Desktop\Live Cowork\JOB-SEARCH\Resume\
|
+-- Titus_Banks_MASTER_PM_Private.docx      <- private sector PM (current source of truth)
+-- Titus_Banks_MASTER_PM_Private.txt       <- extracted text (for grep, diff, AI review)
+-- Titus_Banks_MASTER_PM_Federal.docx      <- government / federal PM (current source of truth)
+-- Titus_Banks_MASTER_PM_Federal.txt       <- extracted text
+-- TITUS_BANKS_MASTER_BIO.md               <- personal bio source (faith, family, career, goals)
+-- Titus_Banks_BA_Tailored_DRAFT.md        <- BA-tailored draft (Markdown - easy to edit in Claude)
+-- Titus_Banks_BA_Tailored_DRAFT.docx      <- BA-tailored draft (DOCX - for applications)
+-- RESUME_MANAGEMENT.md                    <- this file
```

**All Tailored Versions (per job) Live In:**
```
C:\Users\tbank\Desktop\Live Cowork\JOB-SEARCH\Current Job Application\[Job Title]_[Company]\
+-- Resume_Tailored.docx
+-- Resume_Tailored.md
+-- Cover_Letter.md
+-- JD.md
+-- Match_Scorecard.md
+-- Application_Notes.md
```

**Archived Versions (per job, after submission):**
```
C:\Users\tbank\Desktop\Live Cowork\JOB-SEARCH\Archive\YYYY-MM\
+-- [Job Title]_[Company]\...
```

---

## Two-Resume Rule (DO NOT VIOLATE)

Titus maintains **two master PM resumes**. Never mix them.

| Use This | For These Roles |
|----------|-----------------|
| **Titus_Banks_MASTER_PM_Private.docx** | Private sector, public sector, non-profit, healthcare, financial services, retail, tech, startups. Any role that does not explicitly require federal resume format. |
| **Titus_Banks_MASTER_PM_Federal.docx** | Federal government, USAJobs.gov, military, intelligence agencies, government contractors, federal contractors. Roles that explicitly ask for "federal resume" format. |

**The rule:**
- If the job posting says "federal resume format" or "must follow USAJobs format" -> Federal.
- Anything else -> Private.
- When in doubt, ask before submitting.

---

## Three Versions Active

| Version | File | Purpose |
|---------|------|---------|
| **PM Private** | `Titus_Banks_MASTER_PM_Private.docx` | Default resume. PM/coordination roles in private/public/non-profit sectors. |
| **PM Federal** | `Titus_Banks_MASTER_PM_Federal.docx` | PM roles in federal government and government contractors. |
| **BA Tailored (DRAFT)** | `Titus_Banks_BA_Tailored_DRAFT.docx` | Business Analyst roles. Reframes same experience with BA language. Currently DRAFT - needs user review before promotion to MASTER_BA. |

**Future (planned, do not create yet):**
- **BA Federal** - if a federal BA role is targeted
- **IT Support Compact** - already exists at `Titus_Banks_IT_Resume_Compact.docx` - use for helpdesk/IT support roles only

---

## Standard Workflow (Resume Editing)

### When Tailoring a Resume for a Specific Job

```
Step 1: User (or OpenCode) finds a job posting.
         |
         v
Step 2: OpenCode saves JD to JOB-SEARCH/Current Job Application/[Title]_[Company]/JD.md
         |
         v
Step 3: OpenCode generates a Match Scorecard (requirements match analysis).
         |
         v
Step 4: User reviews scorecard. If strong match, proceed to tailoring.
         |
         v
Step 5: OpenCode creates the tailored package:
         - Resume_Tailored.md (Markdown draft from master)
         - Cover_Letter.md (cover letter draft)
         |
         v
Step 6: User opens Claude (browser) at claude.ai -> Project: "Job Search: Project Management" (or "About Me")
         - Pastes the JD + Resume_Tailored.md + asks Claude to refine narrative, tighten bullets, fix flow
         - Claude outputs refined content
         |
         v
Step 7: User copies refined content back to:
         JOB-SEARCH/Current Job Application/[Title]_[Company]/Resume_Tailored.md
         (overwrites the OpenCode draft)
         |
         v
Step 8: OpenCode converts the refined .md to .docx:
         Resume_Tailored.docx
         |
         v
Step 9: User reviews the .docx (typography, layout, one-page check).
         |
         v
Step 10: Final version used for application.
         Status logged in Tracker/APPLICATIONS.csv
         |
         v
Step 11: After application is submitted, entire [Title]_[Company] folder moves to:
         JOB-SEARCH/Archive/YYYY-MM/[Title]_[Company]/
```

### When Editing a Master Resume

**Master resumes are sacred. Edit them rarely and only with intent.**

```
Step 1: User decides a master needs a new skill, cert, or experience.
         |
         v
Step 2: User opens Claude (browser) -> Project: "About Me"
         - Tells Claude what to add (e.g., "Add Google Data Analytics Certificate to core competencies")
         - Asks Claude to return the full updated resume in clean Markdown
         |
         v
Step 3: User saves Claude's output to:
         JOB-SEARCH/Resume/TITUS_BANKS_MASTER_BIO.md (bio source)
         OR
         JOB-SEARCH/Resume/Titus_Banks_[Version]_SOURCE.md (text-only working copy)
         |
         v
Step 4: User tells OpenCode: "Promote this content to MASTER_[X]"
         OpenCode overwrites the .docx after user approval.
         |
         v
Step 5: Old version is auto-archived to:
         JOB-SEARCH/Resume/_archive/Titus_Banks_[Version]_[YYYY-MM-DD].docx
```

---

## The Two-Edit Principle

For every resume touch, ask:

1. **Is this a per-job tailoring?** -> Save in `Current Job Application/.../Resume_Tailored.docx`. Master resumes are NOT modified.
2. **Is this a permanent change to my career story?** (new cert, new job, new skill) -> Edit master. Promote through Claude. Save as new master version. Old version auto-archived.

If the change is neither, don't touch any file.

---

## Claude Project Mapping

User has two relevant Claude projects. Each maps to specific file sources.

| Claude Project | Primary Use | Source Files (paste into project) |
|----------------|-------------|------------------------------------|
| **About Me** | Master bio, career story, base resume content | `TITUS_BANKS_MASTER_BIO.md` |
| **Job Search: Project Management** | PM/BA resume tailoring, cover letters, application narrative | `TITUS_BANKS_MASTER_BIO.md` + relevant master resume .md |

**Recommended Claude Project Instructions:**

For the **About Me** project, paste something like:

> You are helping Titus Banks maintain a master professional bio and career story. The source of truth is the attached about-me.md file. When I ask you to update the bio, return the FULL updated file in Markdown, not a diff. Never invent facts. If I tell you about a new cert or job, ask clarifying questions before adding it. Voice: clear, direct, warm, practical, grounded, human. No generic AI, corporate filler, or hype. No emojis. No em dashes.

For the **Job Search: Project Management** project, paste something like:

> You are helping Titus Banks (Titus Belmond Sangare) tailor his resume and cover letters for PM/BA roles in Seattle, Dallas, and remote US-wide. Salary target $75-95K base. Read the attached bio and PM master resume. When I paste a job description, recommend tailored bullet points, keywords to add, and which experience to emphasize. Return edits in Markdown. Voice: clear, direct, warm, practical. No generic AI, corporate filler, or hype. No emojis. No em dashes. No banned words: "elevate", "seamless", "unleash", "next-gen".

---

## OpenCode Resume Commands (proposed)

These are commands OpenCode (this CLI) can run on request.

| Command | Action |
|---------|--------|
| `tailor [job-posting-url]` | Fetch JD, score match, generate tailored package in `Current Job Application/...` |
| `promote-master [path-to-md]` | Convert .md to .docx, archive old master, save as new master |
| `tailor-from-claude [path-to-md]` | Take Claude's refined .md output, convert to .docx, file in `Current Job Application/...` |
| `score-match [job-url]` | Run match scoring against master resume, return scorecard |
| `list-applications` | Show all in-flight applications and their status |
| `archive [job-title]` | Move application folder from Current to Archive/YYYY-MM/ |
| `extract-resume [path]` | Convert .docx to .txt for grep/AI review |
| `diff-masters` | Show line-by-line diff between two master versions |

These are not yet implemented as slash commands. To use them, ask OpenCode in plain language:
- "OpenCode, tailor this job: [URL]"
- "OpenCode, promote this file to master PM Private"
- "OpenCode, score match for this JD"

---

## File Conventions

**Naming:**
- Master resumes: `Titus_Banks_MASTER_[ROLE]_[SECTOR].docx`
- Tailored resumes: `Resume_Tailored.docx` (inside the job folder)
- DRAFT: anything ending in `_DRAFT.md` or `_DRAFT.docx`
- SOURCE: anything ending in `_SOURCE.md` (text-only working copy, before .docx promotion)
- Archive: prefix with date `YYYY-MM-DD_`

**Format:**
- Always keep the `.md` source alongside the `.docx`
- `.docx` is for applications (and ATS systems)
- `.md` is for editing and AI review
- `.txt` is for grep/diff

**Encoding:**
- All text files: UTF-8
- Markdown files: line breaks LF or CRLF (Windows default OK)

---

## What This Workflow Prevents

- **Drift:** Only one master PM Private, one master PM Federal, one master BA. Everything else is derived.
- **Overwriting live work:** Tailored versions live in their own job folder, never in `Resume/`.
- **Federal/private mix-up:** Two separate masters, clear rule for which to use.
- **Lost history:** Archived versions preserved with date prefix.
- **Resume inflation:** Master changes require Claude review + user approval, not just OpenCode overwrite.

---

## Review Cadence

| Action | Frequency |
|--------|-----------|
| Update `TITUS_BANKS_MASTER_BIO.md` | When new cert, job, project, or skill is earned |
| Review all master resumes for accuracy | Quarterly (every 3 months) |
| Archive old master before promoting new | Always (one-time, automatic) |
| Refresh `Tracker/APPLICATIONS.csv` | After every status change |
| Backup `JOB-SEARCH/` to cloud | Weekly |

---

## Next Steps

1. **User reviews `Titus_Banks_BA_Tailored_DRAFT.md`** and tells OpenCode what to adjust.
2. Once approved, OpenCode renames `*_DRAFT.md` and `*_DRAFT.docx` to `TITUS_BANKS_MASTER_BA.docx` and `.md`.
3. **User pastes `TITUS_BANKS_MASTER_BIO.md` into the Claude "About Me" project** for first sync.
4. **User pastes master PM Private + master BA + master bio into the "Job Search: Project Management" project** for first sync.
5. OpenCode runs first real job tailoring test.

---

*End of RESUME_MANAGEMENT.md*
