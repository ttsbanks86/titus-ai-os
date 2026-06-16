# Titus AI OS Brain — Visual System Map Research + Build Plan

Date: 2026-06-16
Goal: Create a simple local app where Titus can see how the AI OS is connected: agents, skills, projects, files, tools, workflows, memory, apps, bots, and running services.

---

## 1. The Idea

Build a local “system brain” app that turns the AI OS into an interactive map.

Instead of remembering folders, agents, skills, bots, projects, and troubleshooting notes manually, the app shows:

- What agents exist
- What skills exist
- Which runtime owns each skill
- Which projects use which skills
- Which apps/scripts belong to each project
- Which files are important
- Which workflows connect tools together
- Which systems are active/running
- What broke before and how it was fixed
- What the next action is for each project

This should feel less like a generic dashboard and more like a living map of the operating system.

Working name: **Titus AI OS Brain**.

---

## 2. Research Inspiration

### 2.1 LangGraph Studio

Source inspiration: LangGraph Studio is described by LangChain as an agent IDE for visualizing, interacting with, and debugging complex agentic applications.

What to copy:

- Graph-based view of agent flow
- Nodes and edges for agent steps
- Debug/inspect each node
- Stateful agent thinking: memory, human-in-the-loop, long-running workflows

How it applies:

For Titus AI OS Brain, every agent/skill/project/tool becomes a node. Connections show how the system actually works.

### 2.2 Dify

Dify positions itself as an agentic workflow builder for autonomous agents, RAG pipelines, and LLM apps.

What to copy:

- Visual workflow canvas
- Clear blocks for models, tools, knowledge, and outputs
- App-level management: build, deploy, monitor

How it applies:

Use Dify-style workflow blocks for things like:

- “User request → CEO agent → engineer → QA → verification”
- “Reel link → learning extractor → repo capture → project note → adoption decision”
- “Gateway logs → Telegram bot → Command Center status”

### 2.3 Flowise

Flowise is an open-source visual platform for AI agents and LLM orchestration.

What to copy:

- Drag-and-drop workflow feel
- Component cards
- Local/self-hostable mindset
- LLM workflow debugging

How it applies:

The first version does not need drag-and-drop editing, but it should visually display flows as if they are editable blocks.

### 2.4 n8n

n8n is a workflow automation tool that connects triggers, conditions, apps, and actions.

What to copy:

- Trigger → action → condition → action mental model
- Executions/history panel
- Node health and status
- Easy visual explanation of automation chains

How it applies:

For AI OS Brain:

- Trigger: user prompt, scheduled task, file change, email, bot message
- Agent: CEO/research/engineer/browser
- Tool: PowerShell, browser, filesystem, GitHub, Gmail
- Output: file, report, app change, notification

### 2.5 Langfuse / LangSmith / Braintrust / Arize Phoenix / Helicone

These tools focus on LLM tracing, observability, evaluation, latency, cost, prompts, and runs.

What to copy:

- Trace timeline
- Runs table
- Span hierarchy: request → agent → tool → output
- Cost/latency/status metadata
- Debugging by looking at real events, not vibes

How it applies:

Titus AI OS Brain should eventually show:

- What happened in the latest session
- Which agent/tool ran
- Which files changed
- What verification passed/failed
- Which project memory was updated

### 2.6 Obsidian Graph View

Obsidian shows notes as a linked graph.

What to copy:

- Human-readable notes as source of truth
- Graph view of project/decision/troubleshooting notes
- Backlinks
- Local-first storage

How it applies:

The app should treat the Obsidian-style vault as the narrative memory layer, while the graph app shows the structural map.

### 2.7 Neo4j Bloom / Graphistry / Cytoscape-style graph tools

Knowledge graph tools show entities and relationships visually.

What to copy:

- Entity types with colors/shapes
- Relationship labels
- Search and filter
- Click node → inspect details
- Path finding: “how is this connected to that?”

How it applies:

Question examples:

- “How is Command Center connected to Telegram?”
- “Which skills can delete files?”
- “Which projects use HyperFrames?”
- “Which agent owns GitHub work?”
- “What broke in DocFlow before?”

### 2.8 Open WebUI / Local AI Dashboards

Open WebUI-style apps show models, tools, users, knowledge, and settings in one place.

What to copy:

- Simple admin sidebar
- Local-first dashboard
- Model/tool visibility
- Settings separated from chat

How it applies:

The AI OS Brain should have an admin-style sidebar:

- Map
- Agents
- Skills
- Projects
- Workflows
- Memory
- Apps
- Risks
- Logs

### 2.9 AgentField / Kubernetes-for-agents idea

AgentField inspiration: manage agents like deployed services.

What to copy:

- Agent as deployable unit
- Health/status per agent
- Runtime boundaries
- Service inventory

How it applies:

Treat each runtime as a cluster:

- OpenCode cluster
- Claude cluster
- Goose cluster
- Workspace/media cluster
- Gateway/bots cluster

### 2.10 awesome-ai-apps repository

The awesome-ai-apps repo organizes practical AI apps into categories: starter agents, MCP agents, memory agents, RAG apps, advanced agents, voice agents, and more. It also points to AI observability and agent infrastructure projects.

What to copy:

- Category organization
- App examples as reference patterns
- Memory agents + MCP agents as relevant categories
- Observability/platform tools as inspiration

How it applies:

The AI OS Brain is not just a chat app. It is part memory agent, part MCP/tool map, part workflow graph, part observability dashboard.

---

## 3. Recommended Product Shape

### The app should answer five questions visually

1. **What exists?**
   - Agents, skills, projects, apps, repos, memory notes, workflows.

2. **Where does it live?**
   - Exact folder paths and runtime ownership.

3. **How is it connected?**
   - Graph edges between agents, skills, projects, files, tools, apps.

4. **What is active or risky?**
   - Running services, approval-gated skills, exposed-token warnings, stale indexes, archive candidates.

5. **What do I do next?**
   - Next actions per project and system cleanup queue.

---

## 4. MVP: Simple Local App First

Do not start with a giant platform. Start with a local visual app that reads files and generates a graph.

### MVP Name

**AI OS Brain Viewer**

### MVP Stack Recommendation

Best fast local stack:

- Backend/indexer: Python
- Data store: SQLite + JSON export
- Frontend: single-page HTML/JS using Cytoscape.js or React Flow
- Launch: button from Command Center or local `python app.py`

Why this stack:

- Works on Windows
- Easy to inspect folders
- Easy to ship as EXE later
- No cloud dependency
- Simple enough to build quickly

### MVP Data Sources

1. `C:\Users\tbank\.config\opencode\agent`
2. `C:\Users\tbank\.config\opencode\skills`
3. `C:\Users\tbank\.claude\agents`
4. `C:\Users\tbank\.claude\skills`
5. `C:\Users\tbank\.agents\skills`
6. `C:\Users\tbank\Desktop\Live Cowork\.agents\skills`
7. `C:\Users\tbank\Desktop\Live Cowork\AI-OS-GOVERNANCE`
8. `C:\Users\tbank\Desktop\Live Cowork\OBSIDIAN-AI-OS`
9. Key project folders: DocFlow, Business Suite, learning captures, gateway/bot folders

### MVP Node Types

- Runtime
- Agent
- Skill
- Project
- App
- Workflow
- File
- Memory note
- Troubleshooting lesson
- Repo
- Risk / approval gate

### MVP Edge Types

- `contains`
- `uses`
- `belongs_to`
- `duplicates`
- `documents`
- `fixes`
- `runs`
- `depends_on`
- `approval_required`

### MVP Views

#### 1. Global Map

Interactive graph of all systems.

Clusters:

- OpenCode
- Claude
- Goose
- Workspace Skills
- Command Center
- Bots/Gateway
- Memory/Brain
- Business Apps

#### 2. Agent Team View

List/graph of agents:

- CEO
- Engineer
- QA
- Research
- Browser
- Automation
- File Ops
- Gmail Ops
- GitHub Ops
- Workflow Orchestrator
- Executive agents

Click an agent to see:

- Purpose
- File path
- Tools/skills used
- Risk level
- Approval gates

#### 3. Skill Inventory View

Table + graph of skills.

Columns:

- Skill
- Runtime
- Path
- Status
- Risk
- Duplicate count
- Keep/archive recommendation

#### 4. Project Map View

Projects and their linked files/apps:

- Command Center
- DocFlow
- Hermes/OpenClaw gateway
- Business Suite
- Learning Captures
- Skill Registry
- Obsidian AI OS

#### 5. Troubleshooting Memory View

Shows every known problem and fix:

- Bot setup mismatch
- Token safety
- DocFlow recursion
- Command Center build lock
- Windows Git path length

#### 6. Workflow View

Visual workflow examples:

- User request → CEO → subagent → tool → file/app output → verification → memory update
- Learning source → extraction → repo capture → report → adoption decision
- Desktop app fix → source patch → compile → PyInstaller → shortcut verify → lesson saved

#### 7. Risk View

Shows high-risk nodes:

- email senders
- social posting
- file deletion
- desktop automation
- identity eraser
- LinkedIn automation
- system cleanup
- secrets/tokens

---

## 5. Better Version: Living Brain + Observability

After MVP, add live event logging.

### Add Event Log

Each session can write events:

```json
{
  "time": "2026-06-16T12:00:00Z",
  "project": "DocFlow",
  "actor": "engineer",
  "action": "rebuilt_exe",
  "files": ["DOCFLOW/docflow.py"],
  "verification": "passed",
  "lesson": "super.show fixed recursion"
}
```

### Add Timeline View

Like Langfuse/LangSmith traces:

- Request
- Agent decision
- Tool call
- File changed
- Test/build result
- Summary/memory update

### Add Search

Ask:

- “show everything connected to Telegram”
- “which skills are dangerous?”
- “what did we do to DocFlow?”
- “what projects are active?”
- “which duplicate skills need review?”

### Add Graph Query

Later options:

- SQLite first
- KuzuDB later for local graph queries
- Neo4j only if we need a heavier graph platform

---

## 6. Proposed Data Model

### Node fields

```json
{
  "id": "skill:opencode:learning-extractor",
  "label": "learning-extractor",
  "type": "skill",
  "runtime": "opencode",
  "path": "C:/Users/tbank/.config/opencode/skills/learning-extractor",
  "status": "active",
  "risk": "low",
  "description": "Extract lessons from links/videos/repos"
}
```

### Edge fields

```json
{
  "source": "agent:opencode:ceo",
  "target": "skill:opencode:learning-extractor",
  "type": "uses",
  "label": "delegates learning capture"
}
```

---

## 7. Build Phases

### Phase 0 — Current Foundation Already Created

Done/started:

- `AI-OS-GOVERNANCE` folder
- Platform separation plan
- Lessons file
- Agent/skill registry CSV
- Obsidian-style vault skeleton

### Phase 1 — Static Brain Viewer

Build a local web page that loads `graph.json`.

Tasks:

1. Python scanner reads agent/skill/project folders.
2. Python scanner emits `graph.json` and `registry.json`.
3. Static `index.html` visualizes graph with Cytoscape.js.
4. Click node → details side panel.
5. Filters: runtime, type, risk, status.
6. Command Center button opens Brain Viewer.

Deliverable:

`C:\Users\tbank\Desktop\Live Cowork\AI-OS-BRAIN\index.html`

### Phase 2 — Local App Server

Add a lightweight backend.

Tasks:

1. FastAPI app serves graph and registry.
2. Add refresh button to rescan folders.
3. Add search endpoint.
4. Add project pages.
5. Add troubleshooting pages.

Deliverable:

`python brain_app.py`

### Phase 3 — Event Timeline

Add a session/event log.

Tasks:

1. Add `events.jsonl`.
2. Add event ingestion script.
3. Add timeline UI.
4. Add “last session” view.
5. Add verification status tracking.

### Phase 4 — Workflow Builder View

Not full editing yet. First show curated workflow diagrams.

Tasks:

1. Define workflows as YAML/JSON.
2. Render workflow maps.
3. Connect workflow nodes to actual agents/skills/files.

### Phase 5 — Desktop Packaging

Package it like DocFlow/Command Center.

Options:

- PyInstaller for Python server + browser launcher
- Tauri if we want a real desktop app later
- Electron only if needed, but heavier

---

## 8. Recommended UI Layout

### Left Sidebar

- Overview
- Global Map
- Agents
- Skills
- Projects
- Workflows
- Memory
- Troubleshooting
- Risks
- Events
- Settings

### Main Canvas

Interactive graph.

Colors:

- OpenCode = blue
- Claude = purple
- Goose = green
- Workspace = orange
- Memory = gold
- Risk = red
- Projects = white/gray

### Right Inspector Panel

When you click a node:

- Name
- Type
- Runtime
- Path
- Status
- Risk
- Description
- Connected nodes
- Open file/folder button
- Related troubleshooting notes
- Next action

### Top Bar

- Search
- Refresh scan
- Open registry
- Open Obsidian vault
- Export graph
- Health status

---

## 9. What We Should NOT Build First

Avoid these for MVP:

- Full drag-and-drop workflow editor
- Cloud database
- multi-user auth
- real-time background daemon
- auto-deleting duplicate skills
- agent self-modification
- automatic secret scanning with destructive actions
- always-on monitoring

Reason: the immediate need is visibility, not automation.

---

## 10. Recommended First Build Sprint

### Sprint Goal

Create a working local visual map in one focused pass.

### Deliverables

1. `AI-OS-BRAIN\scan_brain.py`
2. `AI-OS-BRAIN\brain-data\graph.json`
3. `AI-OS-BRAIN\index.html`
4. `AI-OS-BRAIN\README.md`
5. Command Center button: “Open AI OS Brain”

### Success Criteria

- Opens in browser locally.
- Shows OpenCode, Claude, Goose, workspace clusters.
- Shows agents and skills as nodes.
- Click node shows file path and details.
- Filters by runtime/type/risk.
- Shows high-risk approval-gated skills.
- Includes project nodes for DocFlow, Command Center, Gateway, Learning Captures.
- Does not move/delete/change existing systems.

---

## 11. Final Recommendation

Yes, this can be designed as a system brain that you can actually see.

The best path is not to start with a huge enterprise tool. Build a local visual brain viewer first:

- Simple scanner
- JSON graph
- Interactive map
- Inspector panel
- Project/risk/memory views
- Command Center launcher

Then grow it into a live observability dashboard with event traces, workflow diagrams, and searchable memory.

This gives Titus a clear command-level view of the AI OS without forcing OpenCode, Goose, and Claude into one messy folder.
