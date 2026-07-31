# M3 Interface Architecture

**Date:** 2026-07-31
**Status:** Designed

---

## OpenCode Analysis

OpenCode is a terminal-based AI coding assistant (TUI). It does not have a web UI that can be themed or extended.

**Key findings:**
- Framework: Terminal UI (TUI)
- Component system: Ink (React for CLI)
- Styling: Terminal colors, not CSS
- Plugin system: Skills (markdown-based)
- No web interface to customize

## M3 Interface Strategy

Since OpenCode is TUI-based, the Titus AI OS branded interface will be a **standalone web dashboard** that:

1. Reads from the Knowledge Engine (M2 Python modules)
2. Displays project/milestone/agent status
3. Provides quick actions via API calls
4. Uses the Titus brand design system
5. Runs locally on `localhost:3000`

### Architecture

```
┌─────────────────────────────────────────┐
│           Titus AI OS Dashboard         │
│         (Standalone Web App)            │
├─────────────────────────────────────────┤
│  React + Vite + Tailwind CSS            │
│  Brand tokens from tokens.css           │
│  Components from DESIGN.md              │
├─────────────────────────────────────────┤
│           API Layer (Python)            │
│  FastAPI server on localhost:8000       │
│  Endpoints for projects, milestones,    │
│  agents, knowledge, verification        │
├─────────────────────────────────────────┤
│         Knowledge Engine (M2)           │
│  inventory, index, search, cache,       │
│  assembler, access, agents              │
├─────────────────────────────────────────┤
│           File System                   │
│  Titus-Vault markdown files             │
│  Git repository                         │
└─────────────────────────────────────────┘
```

### Technology Choices

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | React + Vite | Fast dev, component-based, Tailwind CSS |
| Styling | Tailwind CSS + tokens.css | Brand tokens as CSS variables |
| Backend | Python FastAPI | Reuses M2 modules directly |
| Data | File system + JSON | No database needed for MVP |
| State | React useState/useContext | Simple state management |

### What is Configurable Without Fork

- Brand colors via CSS variables (tokens.css)
- Typography via CSS variables
- Component styles via Tailwind config
- Layout via React components

### What Requires Source Changes

- New views (dashboard, milestone, agent)
- New API endpoints
- New data models

### Upgrade Maintenance Risk

- Low: Standalone app, not forked from OpenCode
- React/Vite are stable, well-maintained
- No dependency on OpenCode internals

### License Constraints

- OpenCode: MIT license
- React: MIT license
- Tailwind CSS: MIT license
- No conflicts expected

---

## Implementation Plan

### Phase 1: API Layer
- FastAPI server with endpoints
- Reuse M2 modules for data access
- JSON responses for all views

### Phase 2: Frontend Foundation
- React + Vite setup
- Tailwind CSS with brand tokens
- Routing and layout

### Phase 3: Views
- Main workspace
- Project dashboard
- Milestone workspace
- Agent dashboard
- Knowledge view
- Verification view
- Workflow queue

### Phase 4: Integration
- Connect frontend to API
- Real-time updates via polling
- Quick actions with confirmation

---

## File Structure

```
Titus-Vault/titus-ai-os-dashboard/
├── api/
│   ├── main.py              # FastAPI server
│   ├── routes/
│   │   ├── projects.py
│   │   ├── milestones.py
│   │   ├── agents.py
│   │   ├── knowledge.py
│   │   └── verification.py
│   └── deps.py              # M2 module dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── StatusBadge.jsx
│   │   │   ├── ProgressRing.jsx
│   │   │   ├── AgentCard.jsx
│   │   │   └── ...
│   │   ├── views/
│   │   │   ├── Workspace.jsx
│   │   │   ├── Projects.jsx
│   │   │   ├── Milestones.jsx
│   │   │   ├── Agents.jsx
│   │   │   ├── Knowledge.jsx
│   │   │   ├── Verification.jsx
│   │   │   └── Queue.jsx
│   │   └── styles/
│   │       └── tokens.css
│   ├── package.json
│   └── vite.config.js
└── README.md
```
