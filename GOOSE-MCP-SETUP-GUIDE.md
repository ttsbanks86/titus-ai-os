# Goose MCP Server Setup Guide
## Safe Extensions for Operations & Automation Agent

**Date:** 2026-06-07
**Goose Version:** 1.37.0

---

## Quick Start

Open Goose Desktop and run these commands in the chat, or use the CLI:

```powershell
goose configure
```

Then follow the prompts for each extension below.

---

## Extension Summary

| Extension | Type | Prerequisites | Status | Recommended |
|-----------|------|---------------|--------|-------------|
| Developer | Built-in | None | ENABLED BY DEFAULT | YES |
| Memory | Built-in | None | ENABLED BY DEFAULT | YES |
| Fetch | Command-line | `uv` installed | READY TO ADD | YES |
| Playwright | Command-line | `npx` (Node.js) | READY TO ADD | YES |
| GitHub | Remote HTTP | GitHub PAT | NEEDS TOKEN | YES |
| Container Use | Command-line | Docker running | NEEDS DOCKER | OPTIONAL |
| Knowledge Graph Memory | Command-line | `npx` | READY TO ADD | OPTIONAL |
| Context7 | Command-line | `npx` | READY TO ADD | OPTIONAL |
| PDF Reader | Command-line | `uvx` | READY TO ADD | OPTIONAL |

---

## 1. Developer Extension (Already Active)

**Status:** ENABLED BY DEFAULT
**Type:** Built-in
**Command:** N/A (built-in)

This extension provides:
- File editing and creation
- Shell command execution
- Project setup automation
- Enhanced code editing
- Codebase analysis

**No action needed** — this is already active.

---

## 2. Memory Extension (Already Active)

**Status:** ENABLED BY DEFAULT
**Type:** Built-in
**Command:** N/A (built-in)

This extension allows goose to remember:
- Your preferences
- Code snippets
- Commands and configurations
- Project-specific knowledge

**No action needed** — this is already active.

---

## 3. Fetch Extension (Web Content)

**Status:** READY TO ADD
**Type:** Command-line Extension
**Prerequisite:** `uv` (already installed: v0.11.11)

### Setup via CLI

```powershell
goose configure
# Select: Add Extension
# Select: Command-line Extension
# Name: Fetch
# Command: uvx mcp-server-fetch
# Timeout: 300
# Description: Web content fetching and processing capabilities
# Environment variables: No
```

### Setup via Desktop

1. Open sidebar → Extensions → Add custom extension
2. Type: `Standard IO`
3. ID: `fetch`
4. Name: `Fetch`
5. Command: `uvx mcp-server-fetch`
6. Timeout: `300`

### What It Does
- Fetches web pages and extracts content
- Processes HTML into readable text
- Useful for research and documentation gathering

### Limitation
Does NOT work with Google models (e.g., gemini-2.0-flash) due to JSON schema compatibility.

---

## 4. Playwright Extension (Browser Automation)

**Status:** READY TO ADD
**Type:** Command-line Extension
**Prerequisite:** Node.js (already installed: v22.22.3)

### Setup via CLI

```powershell
goose configure
# Select: Add Extension
# Select: Command-line Extension
# Name: Playwright
# Command: npx -y @playwright/mcp@latest
# Timeout: 300
# Description: Modern web testing and automation
# Environment variables: No
```

### Setup via Desktop

1. Open sidebar → Extensions → Add custom extension
2. Type: `Standard IO`
3. ID: `playwright`
4. Name: `Playwright`
5. Command: `npx -y @playwright/mcp@latest`
6. Timeout: `300`

### What It Does
- Cross-browser testing (Chromium, Firefox, WebKit)
- Web scraping and automation
- Form filling and button clicking
- Screenshot capture
- Page navigation

---

## 5. GitHub Extension (Repository Management)

**Status:** NEEDS TOKEN
**Type:** Remote Extension (Streamable HTTP)
**Prerequisite:** GitHub Personal Access Token

### Step 1: Create GitHub PAT

1. Go to https://github.com/settings/personal-access-tokens
2. Click "Generate new token (classic)"
3. Name: `goose-mcp`
4. Select scopes:
   - `repo` (full control of private repositories)
   - `read:org` (read organization membership)
   - `read:user` (read user profile)
5. Generate and copy the token

### Step 2: Setup via CLI

```powershell
goose configure
# Select: Add Extension
# Select: Remote Extension (Streamable HTTP)
# Name: github
# Endpoint URL: https://api.githubcopilot.com/mcp/
# Timeout: 300
# Description: GitHub repository management and operations
# Add custom header:
#   Key: Authorization
#   Value: Bearer <YOUR_GITHUB_TOKEN>
```

### Step 3: Setup via Desktop

1. Open sidebar → Extensions → Add custom extension
2. Type: `Remote Extension (Streamable HTTP)`
3. ID: `github`
4. Name: `GitHub`
5. Endpoint URL: `https://api.githubcopilot.com/mcp/`
6. Timeout: `300`
7. Add header:
   - Key: `Authorization`
   - Value: `Bearer <YOUR_GITHUB_TOKEN>`

### What It Does
- Create, read, update repositories
- Manage issues and pull requests
- Search code and repositories
- File operations (create, update, delete)
- Branch management

---

## 6. Container Use Extension (Docker)

**Status:** NEEDS DOCKER RUNNING
**Type:** Command-line Extension
**Prerequisite:** Docker Desktop running

### Option A: Local MCP (requires container-use CLI)

```powershell
# Install container-use first
cargo install container-use

# Then configure
goose configure
# Select: Add Extension
# Select: Command-line Extension
# Name: Container Use
# Command: container-use stdio
# Timeout: 300
# Description: Use containers with dagger and git for isolated environments
# Environment variables: No
```

### Option B: Remote MCP (no CLI needed)

```powershell
goose configure
# Select: Add Extension
# Select: Command-line Extension
# Name: Container Use
# Command: npx -y mcp-remote https://container-use.com/mcp
# Timeout: 300
# Description: Run container automation with container-use
# Environment variables: No
```

### What It Does
- Run tasks in isolated Docker containers
- Safe experimentation without affecting host
- Container lifecycle management
- Environment isolation for testing

---

## 7. Knowledge Graph Memory (Optional)

**Status:** READY TO ADD
**Type:** Command-line Extension
**Prerequisite:** `npx` (Node.js installed)

### Setup via CLI

```powershell
goose configure
# Select: Add Extension
# Select: Command-line Extension
# Name: Knowledge Graph Memory
# Command: npx -y @modelcontextprotocol/server-memory
# Timeout: 300
# Description: Maps and stores complex relationships between concepts
# Environment variables: No
```

### What It Does
- Stores complex relationships between concepts
- Graph-based knowledge representation
- Useful for mapping project structures
- Enhances recall of interconnected information

---

## 8. Context7 Extension (Documentation)

**Status:** READY TO ADD
**Type:** Command-line Extension
**Prerequisite:** `npx` (Node.js installed)

### Setup via CLI

```powershell
goose configure
# Select: Add Extension
# Select: Command-line Extension
# Name: Context7
# Command: npx -y @upstash/context7-mcp@latest
# Timeout: 300
# Description: Up-to-date documentation for any library or framework
# Environment variables: No
```

### What It Does
- Fetches current documentation for libraries
- Provides code examples
- Useful for learning new frameworks
- Keeps goose updated on latest APIs

---

## 9. PDF Reader (Optional)

**Status:** READY TO ADD
**Type:** Command-line Extension
**Prerequisite:** `uvx` (uv installed)

### Setup via CLI

```powershell
goose configure
# Select: Add Extension
# Select: Command-line Extension
# Name: PDF Reader
# Command: uvx mcp-pdf-reader
# Timeout: 300
# Description: Read and extract text from PDF files
# Environment variables: No
```

### What It Does
- Extract text from PDF documents
- Read PDF content for analysis
- Useful for documentation review

---

## Recommended Setup Order

### Phase 1: Essential (Do Now)
1. **Fetch** — web content for research
2. **Playwright** — browser automation

### Phase 2: After GitHub Token
3. **GitHub** — repository management

### Phase 3: When Docker is Running
4. **Container Use** — isolated environments

### Phase 4: Nice to Have
5. **Context7** — library documentation
6. **PDF Reader** — document analysis
7. **Knowledge Graph Memory** — relationship mapping

---

## Verification Commands

After adding extensions, verify they work:

```powershell
# Start a session
goose session

# Test Fetch
"Fetch the content from https://example.com"

# Test Playwright
"Navigate to https://example.com and take a screenshot"

# Test GitHub
"List my GitHub repositories"

# Test Container Use
"Run 'echo hello' in a Docker container"
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Extension not found | Run `goose configure` and verify it's enabled |
| Timeout errors | Increase timeout to 600 seconds |
| Command not found | Ensure prerequisites are installed |
| Docker not running | Start Docker Desktop manually |
| GitHub auth failed | Verify PAT has correct scopes |
| uv not found | Run `pip install uv` or check PATH |

---

## Extension Management

### List enabled extensions
```powershell
goose configure
# Select: Toggle Extensions
```

### Remove an extension
```powershell
goose configure
# Select: Remove Extension
```

### Update extensions
```powershell
goose update
```

---

## Environment Variables

Some extensions need environment variables. Set them in your PowerShell profile:

```powershell
# Example: Set GitHub token globally
[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", "ghp_xxxx", "User")

# Example: Set Ollama host
[Environment]::SetEnvironmentVariable("OLLAMA_HOST", "http://localhost:11434", "User")
```

---

## Reference

- Official docs: https://goose-docs.ai/docs/category/mcp-servers
- Extensions directory: https://goose-docs.ai/extensions
- MCP Server Directory: https://www.pulsemcp.com/servers
- GitHub: https://github.com/aaif-goose/goose

---

**Guide created by:** Local AI Setup Engineer
**Goose version:** 1.37.0
