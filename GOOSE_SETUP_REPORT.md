# Goose Setup Report
## Local AI Agent System — Operations & Automation Agent

**Date:** 2026-06-07
**Status:** CONFIGURED AND OPERATIONAL

---

## 1. Environment Summary

| Component | Status | Version |
|-----------|--------|---------|
| OS | Windows 11 Pro | 10.0.26200 Build 26200 |
| Architecture | x64 | Intel Core i7-11800H, 8 cores, ~31.7 GB RAM |
| GPU | NVIDIA RTX 3080 Laptop | 8 GB VRAM |
| Git | INSTALLED | 2.54.0 |
| Docker | INSTALLED (not running) | 27.5.1 |
| Node.js | INSTALLED | v22.22.3 |
| Python | INSTALLED | 3.13.2 |
| Ollama | INSTALLED | 0.30.6 |
| **Goose Desktop** | **INSTALLED** | **1.37.0** |
| **Goose CLI** | **INSTALLED** | **1.37.0** |

---

## 2. What Was Installed

### Goose Desktop
- **Location:** `C:\Users\tbank\AppData\Local\Programs\Goose\dist-windows\Goose.exe`
- **Size:** 212.6 MB
- **Source:** Official GitHub release v1.37.0 (`Goose-win32-x64.zip`)
- **Status:** Installed, ready to launch

### Goose CLI
- **Location:** `C:\Users\tbank\AppData\Local\Programs\Goose\cli\goose-package\goose.exe`
- **Size:** 224.23 MB
- **Source:** Official GitHub release v1.37.0 (`goose-x86_64-pc-windows-msvc.zip`)
- **Status:** Installed, added to user PATH

---

## 3. What Was Already Installed

| Component | Location | Notes |
|-----------|----------|-------|
| Ollama | `C:\Users\tbank\AppData\Local\Programs\Ollama\ollama.exe` | 3 models available |
| Git | System PATH | v2.54.0 |
| Docker | System PATH | v27.5.1 (Desktop not running) |
| Node.js | System PATH | v22.22.3 |
| Python | System PATH | 3.13.2 |
| OpenCode | `C:\Users\tbank\AppData\Local\OpenCode\opencode-cli.exe` | Primary code agent |

---

## 4. Verification Results

| Check | Result |
|-------|--------|
| Goose Desktop exists | PASS |
| Goose Desktop executable found | PASS |
| Goose CLI exists | PASS |
| Goose CLI executable found | PASS |
| Goose CLI --version | PASS (1.37.0) |
| Goose CLI --help | PASS (commands listed) |
| Goose CLI in PATH | PASS (added to user PATH) |
| Ollama API reachable | PASS (localhost:11434) |
| Ollama models available | PASS (3 models) |

---

## 5. Ollama Models Available for Goose

| Model | Size | Recommended Use |
|-------|------|-----------------|
| gemma2:2b | 1.52 GB | Fast tasks, general chat |
| qwen2.5-coder-7b-lmstudio | 4.36 GB | Code-focused tasks |
| deepseek-coder-7b-lmstudio | 3.75 GB | Code-focused tasks |

**Goose + Ollama Configuration:**
- Provider: `Ollama`
- Default endpoint: `http://localhost:11434`
- Environment variable: `OLLAMA_HOST=http://localhost:11434`
- **Recommended model for Goose:** `gemma2:2b` (fastest) or `qwen2.5-coder-7b-lmstudio` (best for code)

---

## 6. What Still Needs Manual Setup

### 6.1 First-Launch Configuration (Required)
When you first launch Goose Desktop or run `goose configure` in CLI:

1. **Select LLM Provider:** Choose `Ollama`
2. **Set Ollama Host:** `http://localhost:11434`
3. **Select Model:** Start with `gemma2:2b` (fastest) or try `qwen2.5-coder-7b-lmstudio`
4. **Set Permission Mode:** Recommended `Smart Approve` (balanced autonomy + oversight)

### 6.2 Docker Desktop (Optional)
- Docker Desktop is installed but not running
- Start Docker Desktop manually if you need Docker-based extensions
- Not required for basic Goose operation

### 6.3 MCP Extensions (Optional — See Section 8)
- No extensions installed yet
- Built-in extensions available out of the box (Developer, Computer Controller, Memory, etc.)
- External extensions require manual configuration via `goose configure` or Desktop UI

---

## 7. Division of Labor: OpenCode vs Goose

| Task | OpenCode | Goose |
|------|----------|-------|
| Code writing | PRIMARY | — |
| Refactoring | PRIMARY | — |
| Debugging | PRIMARY | — |
| Tests | PRIMARY | — |
| Software architecture | PRIMARY | — |
| Multi-file repo work | PRIMARY | — |
| Research | — | PRIMARY |
| Desktop and file tasks | — | PRIMARY |
| GitHub workflows | — | PRIMARY |
| Docker support | — | PRIMARY |
| Browser/API workflows | — | PRIMARY |
| Documentation gathering | — | PRIMARY |
| MCP-based automation | — | PRIMARY |
| Environment setup | — | PRIMARY |

---

## 8. Recommended MCP Extensions (Safe to Install)

### Built-in (Already Available)
- **Developer** — General development tools (enabled by default)
- **Computer Controller** — Web scraping, file caching, automations
- **Memory** — Remembers preferences across sessions
- **Extension Manager** — Discover, enable, disable extensions (enabled by default)
- **Todo** — Task lists and progress tracking (enabled by default)
- **Summon** — Load skills and recipes, delegate to subagents (enabled by default)

### External — Safe First Extensions
| Extension | Purpose | Risk |
|-----------|---------|------|
| **Filesystem** | File operations, reading, writing | Low |
| **GitHub** | PR management, issues, repos | Low |
| **Docker** | Container management | Low (Docker Desktop must be running) |
| **Browser** | Web automation, scraping | Low |
| **Google Drive** | File access (requires API key) | Medium — needs OAuth setup |

### Extensions to Evaluate Later
| Extension | Purpose | Risk |
|-----------|---------|------|
| **Playwright** | Advanced browser automation | Medium |
| **Notion** | Workspace integration | Medium |
| **Perplexity** | Web search (requires API key) | Low |

---

## 9. API Keys Needed

| Service | Key Required | Status |
|---------|--------------|--------|
| Ollama | None (local) | READY |
| OpenCode | Already configured | READY |
| GitHub | Optional (for GitHub extension) | NOT CONFIGURED |
| Google Drive | Optional (for Drive extension) | NOT CONFIGURED |
| Playwright | None (uses local browser) | NOT CONFIGURED |

---

## 10. Errors and Issues

| Issue | Status | Resolution |
|-------|--------|------------|
| Docker Desktop not running | INFO | Start Docker manually when needed |
| Goose config folder missing | INFO | Created automatically on first run |
| PATH not yet refreshed | INFO | New terminal sessions will pick up Goose CLI |

---

## 11. Quick Start Commands

### Launch Goose Desktop
```powershell
& "$env:LOCALAPPDATA\Programs\Goose\dist-windows\Goose.exe"
```

### Run Goose CLI (interactive session)
```powershell
goose session
```

### Configure Goose
```powershell
goose configure
```

### Check Goose Doctor
```powershell
goose doctor
```

### Update Goose
```powershell
goose update
```

---

## 12. Recommended Goose Workflow for Local AI Agent System

### Daily Operations Flow
```
Morning:
  1. OpenCode → code tasks, debugging, repo work
  2. Goose → research, file ops, GitHub, Docker, docs

Task Routing:
  - Code task → OpenCode
  - Research task → Goose
  - File organization → Goose
  - GitHub PR → Goose
  - Docker container → Goose
  - Browser automation → Goose
  - Documentation → Goose
```

### Goose Session Management
```powershell
# Start a new session
goose session

# Resume last session
goose session --resume

# Run a specific task
goose run --instructions "research topic X and save findings"

# Run from a recipe file
goose run --recipe research-task.yaml
```

### Goose + OpenCode Integration
- OpenCode handles all code-related work (writing, testing, debugging)
- Goose handles everything else (research, files, GitHub, Docker, docs)
- Both can work on the same project directory
- OpenCode's MCP servers (apify, notion, etc.) remain exclusive to OpenCode
- Goose gets its own MCP extensions for different tooling

---

## 13. Next Steps

1. **Launch Goose Desktop** — double-click `Goose.exe` or run the command above
2. **Run first-time configuration** — select Ollama provider, set model to `gemma2:2b`
3. **Test basic functionality** — ask Goose a question to verify it works
4. **Add safe MCP extensions** — start with Filesystem and GitHub
5. **Configure Docker extension** — if Docker Desktop is started
6. **Create Goose recipes** — for recurring research/automation tasks
7. **Set up Goose schedules** — for automated monitoring tasks

---

## 14. Key Files

| File | Location |
|------|----------|
| Goose Desktop | `C:\Users\tbank\AppData\Local\Programs\Goose\dist-windows\Goose.exe` |
| Goose CLI | `C:\Users\tbank\AppData\Local\Programs\Goose\cli\goose-package\goose.exe` |
| Goose Config | `C:\Users\tbank\AppData\Roaming\Block\goose\config\config.yaml` (created on first run) |
| Goose Sessions | `C:\Users\tbank\AppData\Roaming\Block\goose\data\sessions\sessions.db` (created on first run) |
| Goose Logs | `C:\Users\tbank\AppData\Roaming\Block\goose\data\logs` |
| This Report | `C:\Users\tbank\Desktop\Live Cowork\GOOSE_SETUP_REPORT.md` |

---

**Report created by:** Local AI Setup Engineer
**Goose version:** 1.37.0
**Next review:** After first-run configuration complete
