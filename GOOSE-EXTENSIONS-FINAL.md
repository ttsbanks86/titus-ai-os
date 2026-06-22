# Goose Extensions — Final Configuration

**Date:** 2026-06-07
**Total Extensions:** 34 (13 built-in + 21 MCP)

---

## ALL INSTALLED EXTENSIONS

### Built-in (13)
| Extension | Status |
|-----------|--------|
| Todo | ✅ Active |
| Summon | ✅ Active |
| Analyze | ✅ Active |
| Developer | ✅ Active |
| Extension Manager | ✅ Active |
| Summarize | ✅ Active |
| Orchestrator | ✅ Active |
| Top of Mind | ✅ Active |
| Skills | ✅ Active |
| Chat Recall | ✅ Active |
| Code Mode | ✅ Active |
| Apps | ✅ Active |
| Computer Controller | ✅ Active |
| Auto Visualiser | ✅ Active |
| Memory | ✅ Active |
| Tutorial | ✅ Active |

### MCP Extensions (21)
| Extension | API Key Needed | Status |
|-----------|----------------|--------|
| Fetch | None | ✅ Tested |
| Playwright | None | ✅ Tested |
| Context7 | None | ✅ Tested |
| Knowledge Graph Memory | None | ⏳ Added |
| PDF Reader | None | ⏳ Added |
| Container Use | None | ⏳ Added |
| Repomix | None | ⏳ Added |
| YouTube Transcript | None | ⏳ Added |
| Chrome DevTools | None | ⏳ Added |
| GitMCP | None | ⏳ Added |
| Beads | None | ⏳ Added |
| Selenium | None | ⏳ Added |
| **ElevenLabs** | ELEVENLABS_API_KEY | ⏳ Needs key |
| **Reddit** | REDDIT_CLIENT_ID + SECRET | ⏳ Needs key |
| **GitHub** | GITHUB_PERSONAL_ACCESS_TOKEN | ⏳ Needs key |
| **Exa Search** | EXA_API_KEY | ⏳ Needs key |
| **Nano Banana** | GEMINI_API_KEY | ⏳ Needs key |
| **Apify** | APIFY_TOKEN | ⏳ Needs key |

---

## API KEYS NEEDED

### You Already Have
| Service | Key Location |
|---------|--------------|
| Apify | `C:\Users\tbank\.config\opencode\auth.json` (APIFY_TOKEN) |

### Need to Create
| Service | How to Get | Free Tier |
|---------|------------|-----------|
| GitHub PAT | https://github.com/settings/personal-access-tokens | ✅ Yes |
| ElevenLabs | https://elevenlabs.io | ✅ Yes (limited) |
| Reddit | https://www.reddit.com/prefs/apps | ✅ Yes |
| Exa Search | https://exa.ai | ✅ Yes |
| Nano Banana (Gemini) | https://aistudio.google.com/apikey | ✅ Yes |

---

## HOW TO ADD API KEYS

### Option 1: Edit Config File
Add keys to `C:\Users\tbank\AppData\Roaming\Block\goose\config\config.yaml`:

```yaml
  elevenlabs:
    enabled: true
    type: mcp
    name: elevenlabs
    command: uvx
    args:
    - elevenlabs-mcp
    description: Text-to-speech and voice synthesis
    display_name: ElevenLabs
    timeout: 300
    env:
      ELEVENLABS_API_KEY: your_key_here
    available_tools: []
```

### Option 2: Use goose configure
```powershell
goose configure
# Select: Add Extension
# Enter command and environment variables
```

### Option 3: Use Install URLs (Desktop)
Click these in Goose Desktop to install with pre-filled config:

**GitHub:**
```
goose://extension?type=streamable_http&url=https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F&id=github-mcp&name=GitHub&header=Authorization%3DBearer%20YOUR_TOKEN_HERE
```

**Exa Search:**
```
goose://extension?cmd=npx&arg=-y&arg=exa-mcp-server&id=exa&name=Exa%20Search&env=EXA_API_KEY%3Dyour_key_here
```

**Reddit:**
```
goose://extension?cmd=npx&arg=-y&arg=reddit-mcp&id=reddit-mcp&name=Reddit&env=REDDIT_CLIENT_ID%3Dyour_id&env=REDDIT_CLIENT_SECRET%3Dyour_secret
```

---

## RECOMMENDED NEXT STEPS

### Priority 1: Add GitHub PAT (most useful)
1. Go to https://github.com/settings/personal-access-tokens
2. Create token with `repo` scope
3. Copy token
4. Edit config.yaml and add to `github` extension env

### Priority 2: Add Apify Token (you already have it)
1. Get APIFY_TOKEN from auth.json
2. Add to `apify-goose` extension env

### Priority 3: Add Exa Search (free, powerful)
1. Go to https://exa.ai
2. Get free API key
3. Add to `exa` extension env

---

## SKILLS INSTALLED (18)

See `GOOSE-SKILLS-SETUP.md` for complete list.

---

## QUICK REFERENCE

| Task | Extension to Use |
|------|------------------|
| Web research | Fetch, Exa Search |
| Browser automation | Playwright, Selenium, Chrome DevTools |
| GitHub repos | GitHub, GitMCP, Repomix |
| PDF reading | PDF Reader |
| Video transcripts | YouTube Transcript |
| Image generation | Nano Banana |
| Voice synthesis | ElevenLabs |
| Reddit posts | Reddit |
| Web scraping | Apify, Fetch |
| Docker containers | Container Use |
| Library docs | Context7 |
| Knowledge storage | Knowledge Graph Memory, Memory |
| Task tracking | Todo, Beads |
| Code analysis | Analyze, Developer |

---

**Total: 34 extensions + 18 skills = 52 tools available**
