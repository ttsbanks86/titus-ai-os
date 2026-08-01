# Titus AI OS Dashboard

Branded web interface for the Titus AI OS operating system.

## Quick Start

### 1. Install API dependencies

```bash
cd api
pip install -r requirements.txt
```

### 2. Start the API server

```bash
cd api
python -m uvicorn main:app --reload --port 8000
```

### 3. Open the dashboard

Open `frontend/index.html` in your browser.

Or serve it with Python:

```bash
cd frontend
python -m http.server 3000
```

Then visit http://localhost:3000

## Architecture

```
Frontend (HTML/CSS/JS)  →  API (FastAPI)  →  Knowledge Engine (M2)
     localhost:3000           localhost:8000         Python modules
```

## Brand Compliance

This dashboard uses the Titus Banks design system:
- Colors: Navy `#0F2742`, Gold `#D4A14A`, Cream `#F5F1E8`
- Typography: Inter
- Components: Cards, buttons, status badges, progress indicators
- Accessibility: WCAG 2.1 AA

## Views

1. **Workspace** - Overview of current project, tests, quick actions
2. **Projects** - All active projects
3. **Milestones** - Current milestone progress
4. **Agents** - Eight-agent team status
5. **Knowledge** - Engine status and context assembly
6. **Verification** - System health and DoD

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/workspace` - Main workspace data
- `GET /api/projects/` - List projects
- `GET /api/milestones/` - List milestones
- `GET /api/agents/` - List agents
- `GET /api/knowledge/` - Knowledge engine status
- `GET /api/knowledge/context?role=ceo` - Assemble context
- `GET /api/verification/` - Verification status
