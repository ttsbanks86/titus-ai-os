# Goose MCP Extensions — Full Setup Guide

**Date:** 2026-06-07
**Goose Version:** 1.37.0
**Source:** https://goose-docs.ai/extensions/

---

## Your Current Status

| Extension | Status |
|-----------|--------|
| Developer | ACTIVE (built-in) |
| Memory | ACTIVE (built-in) |
| Summon | ACTIVE (built-in) |
| Top of Mind | ACTIVE (built-in) |
| Tutorial | ACTIVE (built-in) |
| Auto Visualiser | ACTIVE (built-in) |
| Code Mode | ACTIVE (built-in) |
| Computer Controller | ACTIVE (built-in) |
| **All others** | NOT INSTALLED |

---

## Extensions by Category

### CATEGORY 1: No API Key Needed (Install Now)

| Extension | Command | Purpose |
|-----------|---------|---------|
| **Fetch** | `uvx mcp-server-fetch` | Web content fetching |
| **Playwright** | `npx @playwright/mcp@latest` | Browser automation |
| **Context7** | `npx @upstash/context7-mcp` | Library documentation |
| **Knowledge Graph Memory** | `npx @modelcontextprotocol/server-memory` | Graph-based memory |
| **PDF Reader** | `uvx mcp-read-pdf` | Read PDF documents |
| **Container Use** | `npx mcp-remote https://container-use.com/mcp` | Docker containers |
| **Chrome DevTools** | `npx chrome-devtools-mcp@latest` | Chrome browser control |
| **Selenium** | `npx selenium-mcp` | Browser testing |
| **Repomix** | `npx repomix-mcp` | Repository analysis |
| **YouTube Transcript** | `uvx --from git+https://github.com/jkawamoto/mcp-youtube-transcript mcp-youtube-transcript` | Video transcripts |

### CATEGORY 2: Needs API Key (Setup Later)

| Extension | Key Needed | How to Get |
|-----------|------------|------------|
| **GitHub** | GitHub PAT | https://github.com/settings/personal-access-tokens |
| **Apify** | APIFY_TOKEN | https://apify.com/account/integrations |
| **Exa Search** | EXA_API_KEY | https://exa.ai |
| **Tavily** | TAVILY_API_KEY | https://tavily.com |
| **ElevenLabs** | ELEVENLABS_API_KEY | https://elevenlabs.io |
| **Browserbase** | BROWSERBASE_API_KEY | https://browserbase.com |

### CATEGORY 3: Needs Local Server

| Extension | Requirement |
|-----------|-------------|
| **Figma** | Figma MCP server running on localhost:3845 |
| **Dev.to** | Local server on localhost:3000 |
| **MBot** | MakeBlock mbot2 rover |
| **Blender** | Blender with MCP plugin |

---

## Quick Install Commands

Copy and paste these into Goose Desktop chat or CLI:

### Phase 1: Essential (No Keys Needed)

```bash
# 1. Fetch — web content
uvx mcp-server-fetch

# 2. Playwright — browser automation
npx @playwright/mcp@latest

# 3. Context7 — library docs
npx @upstash/context7-mcp

# 4. Knowledge Graph Memory — graph memory
npx @modelcontextprotocol/server-memory

# 5. PDF Reader — read PDFs
uvx mcp-read-pdf

# 6. Container Use — Docker isolation
npx mcp-remote https://container-use.com/mcp
```

### Phase 2: Power Tools

```bash
# 7. Chrome DevTools — Chrome control
npx chrome-devtools-mcp@latest

# 8. Selenium — browser testing
npx selenium-mcp

# 9. Repomix — repo analysis
npx repomix-mcp

# 10. YouTube Transcript — video transcripts
uvx --from git+https://github.com/jkawamoto/mcp-youtube-transcript mcp-youtube-transcript
```

---

## Step-by-Step: Adding Extensions via CLI

For each extension, run:

```powershell
goose configure
```

Then follow the prompts:

```
Select: Add Extension
Select: Command-line Extension
Name: [extension name]
Command: [command from table]
Timeout: 300
Description: [description]
Environment variables: No
```

---

## Step-by-Step: Adding Extensions via Desktop

1. Open Goose Desktop
2. Click sidebar (top-left button)
3. Click "Extensions"
4. Click "Add custom extension"
5. Type: `Standard IO`
6. Enter ID, Name, Command, Timeout
7. Click "Add"

---

## Recommended Setup Order

### RIGHT NOW (5 minutes)
1. Fetch — web research
2. Playwright — browser automation
3. Context7 — library documentation

### THIS WEEK
4. Knowledge Graph Memory — persistent knowledge
5. PDF Reader — document analysis
6. Container Use — Docker workflows

### WHEN READY
7. GitHub — needs Personal Access Token
8. Chrome DevTools — advanced browser control
9. Repomix — repository analysis

### OPTIONAL
10. YouTube Transcript — video content
11. Selenium — alternative browser testing

---

## Verification

After adding extensions, test them:

```bash
# Start a session
goose session

# Test Fetch
"Fetch the content from https://example.com"

# Test Playwright
"Navigate to https://example.com and take a screenshot"

# Test Context7
"What is the latest React documentation for hooks?"

# Test PDF Reader
"Read the PDF at C:\path\to\document.pdf"

# Test Container Use
"Run 'echo hello' in a Docker container"
```

---

## Extension Details

### Fetch
- **GitHub:** 86.9k stars
- **Purpose:** Retrieve and process web content
- **Prerequisite:** `uv` (installed: v0.11.11)
- **Limitation:** Does NOT work with Google models

### Playwright
- **GitHub:** 33.6k stars
- **Purpose:** Cross-browser testing and automation
- **Prerequisite:** Node.js (installed: v22.22.3)
- **Supports:** Chromium, Firefox, WebKit

### Context7
- **GitHub:** 56.9k stars
- **Purpose:** Up-to-date library documentation
- **Prerequisite:** Node.js
- **Use case:** Learning new frameworks, API reference

### Knowledge Graph Memory
- **GitHub:** 86.9k stars
- **Purpose:** Graph-based knowledge storage
- **Prerequisite:** Node.js
- **Use case:** Mapping relationships, complex knowledge

### PDF Reader
- **GitHub:** 9 stars
- **Purpose:** Read and extract text from PDFs
- **Prerequisite:** `uv` (installed)
- **Use case:** Document analysis, research

### Container Use
- **Purpose:** Run tasks in isolated Docker containers
- **Prerequisite:** Docker Desktop running
- **Use case:** Safe experimentation, environment isolation

### Chrome DevTools
- **GitHub:** 43.0k stars
- **Purpose:** Control and inspect Chrome browser
- **Prerequisite:** Node.js
- **Use case:** Advanced browser debugging

### Selenium
- **GitHub:** 420 stars
- **Purpose:** Browser automation and testing
- **Prerequisite:** Node.js
- **Use case:** Web testing, automation

### Repomix
- **GitHub:** 26.1k stars
- **Purpose:** Repository analysis and code organization
- **Prerequisite:** Node.js
- **Use case:** Codebase understanding, refactoring

### YouTube Transcript
- **GitHub:** 403 stars
- **Purpose:** Extract video transcripts
- **Prerequisite:** `uv` (installed)
- **Use case:** Video research, content analysis

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | Ensure Node.js or uv is installed |
| Timeout | Increase timeout to 600 seconds |
| Extension not loading | Restart Goose session |
| Docker not running | Start Docker Desktop |
| Permission denied | Run as administrator |

---

## Reference

- Extensions directory: https://goose-docs.ai/extensions/
- MCP Server docs: https://goose-docs.ai/docs/category/mcp-servers
- GitHub: https://github.com/aaif-goose/goose
- Discord: https://discord.gg/goose-oss

---

**Guide created by:** Local AI Setup Engineer
**Goose version:** 1.37.0
