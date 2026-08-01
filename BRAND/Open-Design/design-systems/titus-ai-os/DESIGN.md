# M3 Open Design Prototype Spec — Titus AI OS

**Date:** 2026-07-31
**Status:** Ready for Review

---

## Overview

This prototype defines the Titus AI OS interface: a branded, understandable operating experience that coordinates project work with less supervision.

## Design Principles

1. **Clarity first** — Every screen answers: What project? What milestone? What's next?
2. **Status at a glance** — Color-coded indicators for complete, running, blocked, pending
3. **Minimal chrome** — Content-first, navigation-secondary
4. **Brand consistent** — Navy, Gold, Cream palette. Inter typography.
5. **Accessible** — WCAG 2.1 AA. Focus visible. Keyboard navigable.

---

## View Specifications

### 1. Main Workspace

**Purpose:** Default landing view. Shows what matters now.

**Layout:**
```
+------------------------------------------+
| NAV: Logo | Projects | Agents | Settings |
+------------------------------------------+
| WELCOME: "Good morning, Titus"           |
| CURRENT PROJECT: [Project Name]          |
| CURRENT MILESTONE: [Milestone Name]      |
+------------------------------------------+
| QUICK ACTIONS                             |
| [Start Milestone] [Run Tests] [Refresh]  |
+------------------------------------------+
| RECENT ACTIVITY                           |
| - [Agent] completed [task]               |
| - Tests passed (131/131)                 |
| - Milestone 67% complete                 |
+------------------------------------------+
```

**Components:**
- Welcome header with time-aware greeting
- Current project/milestone card with progress ring
- Quick action buttons (gold primary)
- Activity feed with status badges

### 2. Project Dashboard

**Purpose:** Overview of all projects and their status.

**Layout:**
```
+------------------------------------------+
| PROJECTS (3 active)                       |
+------------------------------------------+
| +------------------+ +------------------+ |
| | Project A        | | Project B        | |
| | M2 Complete ✓    | | M3 In Progress   | |
| | 131 tests pass   | | 45% complete     | |
| | [View]           | | [View]           | |
| +------------------+ +------------------+ |
| +------------------+                      |
| | Project C        |                      |
| | Planning         |                      |
| | 0% complete      |                      |
| | [View]           |                      |
| +------------------+                      |
+------------------------------------------+
```

**Components:**
- Project cards with status badges
- Progress rings (green=complete, gold=in-progress)
- Test status indicators
- Quick view buttons

### 3. Milestone Workspace

**Purpose:** Deep view of current milestone progress.

**Layout:**
```
+------------------------------------------+
| MILESTONE: M3 Orchestration & Interface  |
| STATUS: In Progress (45%)                |
+------------------------------------------+
| SPRINTS                                   |
| [✓] Phase A: Asset Audit      Complete   |
| [✓] Phase B: Design System    Complete   |
| [●] Phase C: Open Design      Running    |
| [○] Phase D: Interface Arch   Pending    |
| [○] Phase E: Branded UI       Pending    |
+------------------------------------------+
| DEFINITION OF DONE                        |
| [✓] Brand assets audited                 |
| [✓] Design system extended               |
| [ ] Prototype approved                   |
| [ ] Interface implemented                |
+------------------------------------------+
| EVIDENCE                                  |
| - 131 tests passing                      |
| - CI: green                              |
| - Security: clean                        |
+------------------------------------------+
```

**Components:**
- Sprint list with status icons
- Definition of Done checklist
- Evidence panel with test/CI/security status
- Progress bar at top

### 4. Agent Dashboard

**Purpose:** Monitor the eight-agent team.

**Layout:**
```
+------------------------------------------+
| AGENTS (8 registered)                     |
+------------------------------------------+
| +--------+ +--------+ +--------+         |
| | CEO    | | Eng    | | QA     |         |
| | ● Run  | | ○ Idle | | ● Test |         |
| | [View] | | [View] | | [View] |         |
| +--------+ +--------+ +--------+         |
| +--------+ +--------+ +--------+         |
| | Research| | Browser| | Auto   |         |
| | ○ Idle  | | ○ Idle | | ○ Idle |         |
| | [View]  | | [View] | | [View] |         |
| +--------+ +--------+ +--------+         |
+------------------------------------------+
```

**Components:**
- Agent cards with role icon and status
- Status indicators (running, idle, blocked)
- Activity timestamp
- Quick action buttons

### 5. Knowledge View

**Purpose:** See what the system knows and how context is assembled.

**Layout:**
```
+------------------------------------------+
| KNOWLEDGE ENGINE                          |
| Index: 6,583 documents | Cache: 94% hit  |
+------------------------------------------+
| CURRENT CONTEXT                           |
| Role: CEO | Budget: 4,000 tokens          |
| [Refresh Context]                         |
+------------------------------------------+
| LOADED DOCUMENTS (29)                     |
| 1. TITUS_AI_OS_ARCHITECTURE.md  SOT      |
| 2. M2_COMPLETION_REPORT.md      CURRENT   |
| 3. CURRENT_STATE_AUDIT.md       GOVERNING |
+------------------------------------------+
| SEARCH                                    |
| [Search knowledge...]                     |
+------------------------------------------+
```

**Components:**
- Engine stats bar (index size, cache hit rate)
- Context assembly panel with role selector
- Document list with authority badges
- Search input with results

### 6. Verification View

**Purpose:** System health and quality status.

**Layout:**
```
+------------------------------------------+
| VERIFICATION                              |
+------------------------------------------+
| TESTS: 131/131 passing ✓                 |
| CI: Last run passed ✓                    |
| SECURITY: No issues found ✓              |
| GIT: Clean working tree ✓                |
+------------------------------------------+
| DEFINITION OF DONE                        |
| [✓] All tests pass                       |
| [✓] CI passes                           |
| [✓] Security clean                       |
| [ ] Documentation complete               |
+------------------------------------------+
| EVIDENCE LOG                              |
| - 2026-07-31: M2 verified complete       |
| - Tag: titus-ai-os-m2-complete           |
+------------------------------------------+
```

**Components:**
- Status cards with green/gold/red indicators
- DoD checklist
- Evidence timeline

### 7. Workflow Queue

**Purpose:** See what's waiting, running, or blocked.

**Layout:**
```
+------------------------------------------+
| WORKFLOW QUEUE                            |
+------------------------------------------+
| RUNNING (2)                               |
| - [Eng] Implement Phase C                |
| - [QA] Run integration tests             |
+------------------------------------------+
| WAITING (3)                               |
| - [CEO] Approve prototype                |
| - [Research] Semantic search design      |
| - [Auto] Index watcher setup             |
+------------------------------------------+
| BLOCKED (0)                               |
| (nothing blocked)                         |
+------------------------------------------+
```

**Components:**
- Queue sections with count badges
- Task cards with agent assignment
- Status indicators
- Priority ordering

### 8. Quick Actions

**Purpose:** One-click safe operations.

**Actions:**
| Action | Permission | Confirmation |
|--------|------------|--------------|
| Start approved milestone | CEO | Yes |
| Run tests | Engineer, QA | No |
| Run health check | Any | No |
| Refresh knowledge index | Any | No |
| Assemble project context | Any | No |
| Generate evidence | QA | No |
| Verify milestone | QA | Yes |
| Open Source of Truth | Any | No |

**Rules:**
- Destructive actions require confirmation
- Actions respect role permissions
- Audit log for all actions
- No bypass of approval gates

### 9. Settings

**Purpose:** System configuration and preferences.

**Sections:**
- Theme: Light / Dark / System
- Notifications: Enable/Disable
- Agent defaults: Model preferences
- Knowledge: Index refresh interval
- Security: Scan schedule
- About: Version, license, credits

---

## Component Inventory

### New Components (M3)
- StatusBadge — pill with color and icon
- ProgressRing — circular progress indicator
- ProgressBar — linear progress indicator
- Alert — bordered notification
- AgentCard — agent status display
- TaskCard — workflow task display
- DocumentCard — knowledge document display
- Checklist — DoD-style checkbox list
- ActivityFeed — recent events timeline
- QuickAction — permission-gated button

### Existing Components (REUSE from DESIGN.md)
- Button (primary, secondary)
- Card
- Form inputs
- Navigation
- Table

---

## Accessibility Requirements

- All interactive elements have visible focus
- Color is never the only signal (pair with icon/text)
- Touch targets 44x44px minimum
- Keyboard navigation for all views
- Screen reader labels for all icons
- Reduced motion support
- High contrast mode support

---

## Responsive Behavior

- Mobile: Single column, hamburger nav, card layout
- Tablet: 2 column, condensed nav
- Desktop: 3 column, full nav
- All views work at 375px+ width
