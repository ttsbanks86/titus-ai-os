# Titus AI OS Brain

A local visual system brain for the Titus AI OS.

It maps:

- OpenCode agents and skills
- Claude agents and skills
- Goose `.agents` skills
- Workspace/project skills
- Governance files
- Obsidian-style memory notes
- Projects
- Workflows
- Portfolio items
- Approval-gated risk areas

## Run

```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\AI-OS-BRAIN"
python scan_brain.py
python -m http.server 8765
```

Then open:

```text
http://localhost:8765
```

You can also open `index.html` directly, but a local server is more reliable because browsers often block local JSON fetches from `file://` pages.

## Files

- `scan_brain.py` — scans local runtime folders and writes graph data
- `brain-data/graph.json` — generated graph consumed by the viewer
- `index.html` — interactive graph viewer

## Design

The app is intentionally read-only in the first version. It helps you see how the system is connected before adding more automation.

## Next improvements

- Add a FastAPI backend with refresh/search endpoints
- Add live event timeline from sessions/tool calls
- Add Command Center launcher button
- Add workflow YAML definitions
- Add graph query: “How is X connected to Y?”
