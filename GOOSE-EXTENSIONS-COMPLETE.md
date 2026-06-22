# Goose Extensions — Complete Reference

**Date:** 2026-06-07
**Source:** https://goose-docs.ai/extensions/

---

## INSTALLED (13 Extensions)

### Built-in (No Setup Needed)
| Extension | Status | Purpose |
|-----------|--------|---------|
| Auto Visualiser | ✅ Active | Data visualization via MCP-UI |
| Code Mode | ✅ Active | Execute JavaScript code |
| Computer Controller | ✅ Active | Webscraping, file caching, automations |
| Developer | ✅ Active | File editing and shell commands |
| Memory | ✅ Active | Persistent context storage |
| Summon | ✅ Active | Load skills, delegate to subagents |
| Top of Mind | ✅ Active | Inject persistent instructions |
| Tutorial | ✅ Active | Interactive tutorials |
| Todo | ✅ Active | Task tracking |
| Summarize | ✅ Active | File/directory summarization |
| Analyze | ✅ Active | Code structure analysis (tree-sitter) |
| Skills | ✅ Active | Discover skill instructions |
| Chat Recall | ✅ Active | Search past conversations |

### MCP Extensions (Added)
| Extension | Command | Status |
|-----------|---------|--------|
| Fetch | `uvx mcp-server-fetch` | ✅ Tested |
| Playwright | `npx @playwright/mcp@latest` | ✅ Tested |
| Context7 | `npx @upstash/context7-mcp` | ✅ Tested |
| Knowledge Graph Memory | `npx @modelcontextprotocol/server-memory` | ⏳ Added |
| PDF Reader | `uvx mcp-read-pdf` | ⏳ Added |
| Container Use | `npx mcp-remote https://container-use.com/mcp` | ⏳ Added |
| Repomix | `npx repomix-mcp` | ⏳ Added |
| YouTube Transcript | `uvx --from git+... mcp-youtube-transcript` | ⏳ Added |
| Chrome DevTools | `npx chrome-devtools-mcp@latest` | ⏳ Added |
| GitMCP | `npx mcp-remote https://gitmcp.io/docs` | ⏳ Added |
| Beads | `uvx beads-mcp` | ⏳ Added |
| Selenium | `npx selenium-mcp` | ⏳ Added |

---

## AVAILABLE BUT NOT INSTALLED

### No API Key Needed
| Extension | Install Command | Purpose |
|-----------|-----------------|---------|
| Blender | `uvx blender-mcp` | 3D modeling (requires Blender running) |
| prompts.chat | `npx @fkadev/prompts.chat-mcp@latest` | AI prompt library |
| Council of Mine | `uvx --from git+... mcp_council_of_mine` | 9-persona LLM debate |
| I Ching | `i-ching-mcp-server` | Divination readings |
| Scholar Sidekick | `npx scholar-sidekick-mcp@latest` | Academic citations |

### Needs API Key
| Extension | Key Needed | How to Get |
|-----------|------------|------------|
| GitHub | GitHub PAT | https://github.com/settings/personal-access-tokens |
| Apify | APIFY_TOKEN | https://apify.com/account/integrations |
| Exa Search | EXA_API_KEY | https://exa.ai |
| Tavily | TAVILY_API_KEY | https://tavily.com |
| ElevenLabs | ELEVENLABS_API_KEY | https://elevenlabs.io |
| Browserbase | BROWSERBASE_API_KEY | https://browserbase.com |
| AgentQL | AGENTQL_API_KEY | https://agentql.com |
| Nano Banana | GEMINI_API_KEY | https://aistudio.google.com/apikey |
| Netlify | NETLIFY_ACCESS_TOKEN | https://app.netlify.com/user/applications#personal-access-tokens |
| Reddit | REDDIT_CLIENT_ID + SECRET | https://www.reddit.com/prefs/apps |
| Rendex | RENDEX_API_KEY | https://mcp.rendex.dev |

### Needs Local Server
| Extension | Requirement |
|-----------|-------------|
| Figma | Figma MCP server on localhost:3845 |
| Dev.to | Local server on localhost:3000 |
| MBot | MakeBlock mbot2 rover |
| Blender | Blender with MCP plugin |

---

## INSTALL URLS (Click to Install in Goose Desktop)

These are `goose://extension?` URLs that trigger installation when clicked in Goose:

### GitHub (Needs PAT)
```
goose://extension?type=streamable_http&url=https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F&id=github-mcp&name=GitHub&description=GitHub%20repository%20management%20and%20operations&header=Authorization%3DBearer%20%3CYOUR_GITHUB_PERSONAL_ACCESS_TOKEN%3E
```

### Exa Search (Needs API Key)
```
goose://extension?cmd=npx&arg=-y&arg=exa-mcp-server&id=exa&name=Exa%20Search&description=AI-powered%20web%20search%20with%20neural%20and%20keyword%20capabilities&env=EXA_API_KEY%3DAPI%20key%20for%20Exa%20web%20search%20service
```

### Tavily (Needs API Key)
```
goose://extension?cmd=npx&arg=-y&arg=tavily-mcp&id=tavily&name=Tavily%20Web%20Search&description=Web%20search%20capabilities%20powered%20by%20Tavily&env=TAVILY_API_KEY%3DAPI%20key%20for%20Tavily%20web%20search%20service
```

### Nano Banana (Needs Gemini API Key)
```
goose://extension?cmd=npx&arg=nano-banana-mcp&id=nano-banana-mcp&name=Nano%20Banana&description=AI-powered%20image%20generation%20and%20editing&env=GEMINI_API_KEY%3DAPI%20key%20from%20Google%20AI%20Studio
```

### Apify (Needs APIFY_TOKEN)
```
goose://extension?cmd=npx&arg=-y&arg=%40apify%2Factors-mcp-server&id=apify&name=Apify&description=Extract%20data%20from%20any%20website%20with%20thousands%20of%20scrapers%2C%20crawlers%2C%20and%20automations%20on%20Apify%20Store%20%E2%9A%A1&env=APIFY_TOKEN%3DRequired%20environment%20variable
```

---

## RECOMMENDED NEXT INSTALLS

### Priority 1: No API Key Needed
1. **Beads** — Git-backed task management (already added)
2. **Chrome DevTools** — Advanced browser control (already added)
3. **GitMCP** — GitHub project docs (already added)

### Priority 2: Free API Keys Available
1. **GitHub** — Create PAT at https://github.com/settings/personal-access-tokens
2. **Exa Search** — Free tier at https://exa.ai
3. **Nano Banana** — Free Gemini API key at https://aistudio.google.com/apikey

### Priority 3: Already Have API Keys
1. **Apify** — You already have APIFY_TOKEN in opencode.json

---

## QUICK INSTALL COMMANDS

For CLI installation, run these in PowerShell:

```powershell
# GitHub (after creating PAT)
goose configure
# Select: Add Extension > Command-line Extension
# Name: github
# Command: npx -y @github/github-mcp-server
# Add environment variable: GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here

# Exa Search (after getting API key)
goose configure
# Select: Add Extension > Command-line Extension
# Name: exa
# Command: npx -y exa-mcp-server
# Add environment variable: EXA_API_KEY=your_key_here
```

---

**Total Extensions Available:** 70+
**Currently Installed:** 13 built-in + 12 MCP = 25
**Recommended Next:** GitHub, Exa Search, Nano Banana
