# Obsidian Vault Structure

**Author:** Titus AI OS
**Date:** 2026-06-21
**Purpose:** Define the canonical vault folder structure for the OpenCode Obsidian knowledge system.

---

## Design Principles

1. **Every folder has a clear purpose.** If a folder does not serve a distinct function, it does not exist.
2. **Flat where possible, nested where necessary.** Prefer fewer levels. Only nest when the content volume demands subdivision.
3. **Numbers enforce sort order.** Folders are prefixed with `01-`, `02-`, etc. to maintain consistent ordering regardless of tool.
4. **Master notes are the entry point.** Every major area has one master note that links to everything beneath it.
5. **Archive, never delete.** `12-Archive` is the final destination for everything that ages out.

---

## Vault Structure

```
📁 Titus-Vault/
│
├── 📁 01-Dashboard/
│   ├── Home.md                          ← Vault dashboard. Index of everything.
│   ├── Personal-Context.md              ← Consolidated from my-context.md
│   ├── My-Rules.md                      ← Consolidated from my-rules.md
│   ├── My-Goals.md                      ← Consolidated from my-goals.md
│   └── My-Voice.md                      ← Consolidated from my-voice.md
│
├── 📁 02-Daily-Notes/
│   ├── 2026-06-21.md                    ← Daily log (one per day)
│   ├── 2026-06-22.md
│   └── ...                              ← Format: YYYY-MM-DD.md
│
├── 📁 03-Businesses/
│   ├── Businesses.md                    ← Master index of all businesses
│   ├── CareNotes-Pro.md                 ← Master note
│   ├── Business-Ideas.md                ← Active ideas and evaluation
│   └── Legacy-Businesses.md             ← Reference to archived businesses
│
├── 📁 04-Products/
│   ├── Products.md                      ← Master index of all products
│   ├── Content-Income-System.md         ← Master note
│   ├── Personal-AI-Operator.md          ← Master note
│   ├── EchoKeys.md                      ← Voice dictation tool
│   ├── NOLA-Voice.md                    ← Voice assistant
│   ├── Whisper-Pro.md                   ← Speech recognition
│   ├── Floating-AI-Tutor.md             ← Desktop tutor overlay
│   ├── DocFlow.md                       ← Document automation
│   └── Hermes-Gateway.md               ← API gateway
│
├── 📁 05-Career/
│   ├── Career.md                        ← Master index
│   ├── Job-Search.md                    ← Active search tracking
│   ├── Resume.md                        ← Resume strategy and versions
│   ├── LinkedIn-Strategy.md             ← Profile and outreach
│   ├── Portfolio.md                     ← PM portfolio projects
│   ├── Certifications.md                ← Completed and planned
│   ├── Education.md                     ← Degrees and coursework
│   └── Business-Analyst-Path.md         ← BA career development
│
├── 📁 06-Projects/
│   ├── Projects.md                      ← Master index of all projects
│   ├── AeroCardia.md                    ← Riipen micro-internship
│   ├── Bonolo-Book-Marketing.md         ← Book marketing project
│   ├── Book-Launch-Struck-Down.md       ← Book project 1
│   ├── Book-Launch-Crown-of-Victory.md  ← Book project 2
│   ├── PM-Portfolio.md                  ← PM portfolio development
│   ├── Ministry-Return.md               ← Ministry relaunch planning
│   └── Local-Business-AI-Services.md    ← Business service project
│
├── 📁 07-SOPs/
│   ├── SOPs-Index.md                    ← Master index of all SOPs
│   ├── Career/
│   │   ├── Job-Application-SOP.md
│   │   ├── LinkedIn-Outreach-SOP.md
│   │   └── Interview-Preparation-SOP.md
│   ├── Content/
│   │   ├── Social-Media-Post-SOP.md
│   │   ├── Newsletter-SOP.md
│   │   └── Video-Script-SOP.md
│   ├── Business/
│   │   ├── Lead-Research-SOP.md
│   │   ├── Email-Triage-SOP.md
│   │   └── Meeting-Recap-SOP.md
│   ├── Development/
│   │   ├── Feature-Development-SOP.md
│   │   ├── Code-Review-SOP.md
│   │   └── Deployment-SOP.md
│   ├── Operations/
│   │   ├── Daily-Workflow-SOP.md
│   │   ├── Weekly-Review-SOP.md
│   │   └── Monthly-Planning-SOP.md
│   └── Marketing/
│       ├── Campaign-Launch-SOP.md
│       ├── Competitor-Analysis-SOP.md
│       └── Content-Calendar-SOP.md
│
├── 📁 08-Agents/
│   ├── Agents-Index.md                  ← Master index of all agents
│   ├── Agent-System-Architecture.md     ← How agents work together
│   ├── Agent-Skill-Registry.md          ← Which skills each agent uses
│   ├── CEO-Agent.md                     ← CEO orchestrator profile
│   ├── Engineer-Agent.md                ← Engineering agent profile
│   └── ...                              ← One note per active agent
│
├── 📁 09-Knowledge/
│   ├── Knowledge-Index.md               ← Master index of knowledge areas
│   ├── AI-Systems/
│   │   ├── OpenCode-Config.md           ← OpenCode configuration reference
│   │   ├── Model-Routing.md             ← Which model for which task
│   │   ├── API-Keys.md                 ← Key inventory (no values stored)
│   │   └── Provider-Architecture.md     ← How providers are connected
│   ├── Brand/
│   │   ├── Brand-Voice.md               ← Brand voice and tone
│   │   ├── Brand-Assets.md              ← Logos, colors, fonts
│   │   └── Content-Guidelines.md        ← Platform-specific content rules
│   ├── Marketing/
│   │   ├── Marketing-Strategy.md        ← Overall marketing approach
│   │   ├── Content-Strategy.md          ← Content marketing plan
│   │   └── Growth-Engineering.md        ← Growth tactics and experiments
│   ├── Technology/
│   │   ├── Tech-Stack.md                ← Current technology choices
│   │   ├── Infrastructure.md            ← Hosting, servers, deployment
│   │   └── Tools-Reference.md           ← Tools and subscriptions
│   └── Finance/
│       ├── Budget.md                    ← Current budget snapshot
│       ├── Income-Streams.md            ← Active and planned income
│       └── Tax-Reference.md             ← Tax-related information
│
├── 📁 10-Archive/
│   ├── Archive-Index.md                 ← Master index of archived content
│   ├── ChatGPT-Exports/                 ← Archived ABOUT ME/ content
│   ├── Legacy-Agents/                   ← Archived Claude agents
│   ├── Legacy-Skills/                   ← Archived Claude skills
│   ├── Legacy-Commands/                 ← Archived Claude commands
│   ├── Legacy-Rules/                    ← Archived Claude rules
│   ├── Staging/                         ← Archived staging content
│   └── Deprecated-Projects/            ← Old project files
│
├── 📁 11-Templates/
│   ├── Templates-Index.md               ← Master index of all templates
│   ├── Daily-Note-Template.md           ← Template for 02-Daily-Notes
│   ├── Master-Note-Template.md          ← Template for any master note
│   ├── SOP-Template.md                  ← Template for standard operating procedures
│   ├── Project-Note-Template.md         ← Template for project notes
│   ├── Decision-Record-Template.md      ← Template for decision documentation
│   ├── Meeting-Note-Template.md         ← Template for meeting notes
│   └── Research-Note-Template.md        ← Template for research findings
│
└── 📁 12-Reference/
    ├── Reference-Index.md               ← Master index of reference material
    ├── Books/                           ← Book notes and summaries
    ├── Courses/                         ← Course notes and certificates
    ├── Papers/                          ← Research papers and articles
    ├── People/                          ← Contact notes and network
    └── Learning-Captures/               ← Symbolic link to captured repos (read-only)
```

---

## Folder Purposes

### 01-Dashboard
The entry point. Every OpenCode session starts here. Contains the vault-wide index (`Home.md`) and all personal identity/context files. This folder answers "who am I, what do I believe, where am I going."

### 02-Daily-Notes
Chronological session logs. One file per day. Each note captures decisions made, work completed, open tasks, problems encountered, and follow-up actions. This is the operational memory of the system.

### 03-Businesses
Every active or planned business lives here. Each business gets one master note. Sub-notes for specific aspects (pricing, marketing, features) link back to the master. Legacy businesses move to `10-Archive`.

### 04-Products
Every software product, tool, or system built by Titus AI OS. This is distinct from Businesses (a business may have multiple products). Each product gets a master note with linked sub-notes.

### 05-Career
Everything related to professional development: job search, resume, LinkedIn, portfolio, education, certifications, and career path planning. The `Job-Search.md` master note tracks all active applications.

### 06-Projects
Time-bound initiatives. Unlike Businesses (ongoing) or Products (shipped), Projects have a start and end. Active projects stay here. Completed projects move to `10-Archive`.

### 07-SOPs
Standard operating procedures organized by domain. OpenCode reads these before executing tasks in that domain. SOPs replace ad-hoc improvisation with structured execution.

### 08-Agents
Documentation for every OpenCode agent: what it does, which model it uses, which skills it loads, its fallback chain, and how it interacts with other agents.

### 09-Knowledge
Permanent reference knowledge organized by domain. This is not operational memory (that is 02-Daily-Notes). This is the long-term understanding of how things work: brand voice, tech stack, marketing strategy, financial plan.

### 10-Archive
Everything that ages out. Nothing is ever deleted. The archive maintains a restore log so any file can be recovered. This folder is expected to grow over time.

### 11-Templates
Reusable note templates. Every new note starts from a template to ensure consistent structure. Templates enforce the wiki-link architecture and memory rules.

### 12-Reference
External reference material: book notes, course notes, research papers, contact information. This is a library, not operational memory. Learning-Captures/ is a symbolic link to the existing cloned repos.

---

## Migration from Existing OBSIDIAN-AI-OS

The existing `OBSIDIAN-AI-OS/` directory will be retired. Its content maps as follows:

| Current Location | New Location |
|---|---|
| `00-Dashboard.md` | `01-Dashboard/Home.md` |
| `01-Projects/` | `06-Projects/` |
| `02-Agents/` | `08-Agents/` |
| `03-Skills/` | `09-Knowledge/AI-Systems/` |
| `04-Troubleshooting/` | `10-Archive/Legacy-Troubleshooting/` |
| `05-Decisions/` | Integrated into relevant project notes |
| `06-Daily-Logs/` | `02-Daily-Notes/` |

The old `OBSIDIAN-AI-OS/` directory will be archived after migration is verified.

---

## What This Structure Enables

1. **OpenCode starts every session at `01-Dashboard/Home.md`** and follows wiki-links to gather context.
2. **Daily notes create session continuity** — any OpenCode instance can read yesterday's note and continue.
3. **SOPs eliminate improvisation** — agents follow documented processes instead of inventing approaches.
4. **Master notes collapse complexity** — one note links to everything about a topic. Follow the links.
5. **Archive preserves history** — nothing is lost, but dead weight does not slow retrieval.
6. **Templates enforce consistency** — every note follows the same structure, making them machine-readable.
