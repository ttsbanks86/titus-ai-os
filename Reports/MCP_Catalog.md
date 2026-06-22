# MCP Server Catalog
## Generated: 2026-06-08

---

## Communications

### 1. Nexus (Gmail + Slack + Discord + Telegram + WhatsApp)
- **GitHub**: https://github.com/santoshakil/nexus
- **Install**: `cargo install nexus` or download binary
- **Dependencies**: Rust runtime, platform API credentials
- **Tools**: 48 tools across 5 platforms
- **Security**: Local binary, no cloud dependency
- **Use Cases**: Unified messaging, email management, team communication
- **Priority**: 10/10
- **Status**: RECOMMENDED - Single binary, covers all comms

### 2. Gmail MCP (Official Google)
- **GitHub**: https://github.com/nicholasgriffinintc/gmail-mcp-server
- **Install**: `npx -y gmail-mcp-server`
- **Dependencies**: Gmail API credentials, OAuth
- **Tools**: Read, send, search, label, archive emails
- **Security**: OAuth 2.0, Google API scopes
- **Use Cases**: Email triage, automated responses, newsletter management
- **Priority**: 9/10

### 3. Slack MCP
- **GitHub**: https://github.com/nicholasgriffinintc/slack-mcp-server
- **Install**: `npx -y slack-mcp-server`
- **Dependencies**: Slack Bot Token (xoxb-...)
- **Tools**: Read/send messages, manage channels, reactions
- **Security**: Bot token with granular scopes
- **Use Cases**: Team updates, channel monitoring, automated alerts
- **Priority**: 8/10

### 4. Discord MCP
- **GitHub**: https://github.com/nicholasgriffinintc/discord-mcp-server
- **Install**: `npx -y discord-mcp-server`
- **Dependencies**: Discord Bot Token
- **Tools**: Read/send messages, manage channels, threads
- **Security**: Bot token with intent configuration
- **Use Cases**: Community management, support channels
- **Priority**: 7/10

### 5. Outlook MCP
- **GitHub**: https://github.com/microsoftgraph/mcp-server-outlook
- **Install**: `npx -y @microsoftgraph/mcp-server-outlook`
- **Dependencies**: Microsoft Graph API, Azure AD app
- **Tools**: Email, calendar, contacts management
- **Security**: Azure AD OAuth 2.0
- **Use Cases**: Enterprise email, calendar integration
- **Priority**: 7/10

---

## Productivity

### 6. Notion MCP (Official)
- **GitHub**: https://github.com/makenotion/notion-mcp-server
- **Install**: `npx -y @notionhq/notion-mcp-server`
- **Dependencies**: Notion API token
- **Tools**: CRUD pages, databases, blocks
- **Security**: API token with workspace access
- **Use Cases**: Knowledge base, project tracking, documentation
- **Priority**: 9/10
- **Status**: ALREADY CONFIGURED in OpenCode

### 7. Obsidian MCP
- **GitHub**: https://github.com/yanxue06/obsidian-mcp
- **Install**: `npx -y @yanxue06/obsidian-mcp`
- **Dependencies**: Obsidian Local REST API plugin
- **Tools**: 25 tools - graph traversal, Dataview queries, note CRUD
- **Security**: Local REST API, API key required
- **Use Cases**: Knowledge graph, note management, research
- **Priority**: 8/10

### 8. Google Drive MCP
- **GitHub**: https://github.com/nicholasgriffinintc/google-drive-mcp-server
- **Install**: `npx -y google-drive-mcp-server`
- **Dependencies**: Google API credentials, OAuth
- **Tools**: File search, read, upload, organize
- **Security**: OAuth 2.0, Drive API scopes
- **Use Cases**: Document management, file sharing, backups
- **Priority**: 8/10

### 9. OneDrive MCP
- **GitHub**: https://github.com/nicholasgriffinintc/onedrive-mcp-server
- **Install**: `npx -y onedrive-mcp-server`
- **Dependencies**: Microsoft Graph API, Azure AD
- **Tools**: File operations, sharing, sync
- **Security**: Azure AD OAuth
- **Use Cases**: Enterprise file storage, Office integration
- **Priority**: 7/10

---

## CRM

### 10. HubSpot MCP (Official Remote)
- **URL**: https://mcp.hubspot.com
- **Install**: Remote MCP endpoint (no local install)
- **Dependencies**: HubSpot OAuth app with PKCE
- **Tools**: CRM search, CRUD contacts/deals/companies, property lookup
- **Security**: OAuth 2.1 with PKCE, granular scopes
- **Use Cases**: Sales pipeline, contact management, deal tracking
- **Priority**: 9/10

### 11. Salesforce MCP
- **GitHub**: https://github.com/salesforce/mcp-server
- **Install**: `pip install salesforce-mcp-server`
- **Dependencies**: Salesforce Connected App, OAuth
- **Tools**: SOQL queries, CRUD operations, metadata access
- **Security**: OAuth 2.0, IP restrictions
- **Use Cases**: Enterprise CRM, sales automation, reporting
- **Priority**: 8/10

### 12. Pipedrive MCP
- **GitHub**: https://github.com/nicholasgriffinintc/pipedrive-mcp-server
- **Install**: `npx -y pipedrive-mcp-server`
- **Dependencies**: Pipedrive API token
- **Tools**: Deals, contacts, organizations, activities
- **Security**: API token
- **Use Cases**: Sales pipeline for SMBs
- **Priority**: 7/10

---

## Lead Generation

### 13. Apollo MCP (Official)
- **URL**: https://www.apollo.io/product/mcp
- **Install**: OAuth via Claude/Apollo connector
- **Dependencies**: Apollo account
- **Tools**: Search leads, enrich contacts, add to sequences
- **Security**: OAuth 2.0
- **Use Cases**: B2B prospecting, contact enrichment, outreach
- **Priority**: 9/10

### 14. Clay MCP
- **GitHub**: https://github.com/shanefirek/clay-mcp-public
- **Install**: `uvx clay-mcp-server`
- **Dependencies**: Clay account API key
- **Tools**: 73 tools - enrichments, waterfalls, CRM sync
- **Security**: API key authentication
- **Use Cases**: Data enrichment, waterfall sequences, GTM workflows
- **Priority**: 8/10

### 15. GTM MCP (Apollo + SmartLead)
- **GitHub**: https://github.com/impecablemee/gtm-mcp
- **Install**: `uv run gtm-mcp` (auto-discovers .mcp.json)
- **Dependencies**: Apollo API key, SmartLead API key
- **Tools**: 6 Apollo + 13 SmartLead + pipeline tools
- **Security**: API keys, local execution
- **Use Cases**: B2B cold outreach pipeline, campaign management
- **Priority**: 9/10
- **Status**: RECOMMENDED for lead generation

### 16. Instantly MCP
- **GitHub**: https://github.com/nicholasgriffinintc/instantly-mcp-server
- **Install**: `npx -y instantly-mcp-server`
- **Dependencies**: Instantly API key
- **Tools**: Campaign management, lead management, analytics
- **Security**: API key
- **Use Cases**: Cold email at scale
- **Priority**: 7/10

### 17. SmartLead MCP
- **GitHub**: https://github.com/nicholasgriffinintc/smartlead-mcp-server
- **Install**: `npx -y smartlead-mcp-server`
- **Dependencies**: SmartLead API key
- **Tools**: Campaign CRUD, lead management, sequence building
- **Security**: API key
- **Use Cases**: Multi-channel outreach, email warmup
- **Priority**: 8/10

---

## Research

### 18. Firecrawl MCP (Official)
- **GitHub**: https://github.com/firecrawl/firecrawl-mcp-server
- **Install**: `npx -y firecrawl-mcp-server`
- **Dependencies**: Firecrawl API key
- **Tools**: Scrape, crawl, extract, search
- **Security**: API key, rate limiting
- **Use Cases**: Web scraping, content extraction, site mapping
- **Priority**: 9/10
- **Status**: ALREADY CONFIGURED in OpenCode

### 19. Tavily MCP (Official)
- **GitHub**: https://github.com/tavily-ai/tavily-mcp
- **Install**: `npx -y tavily-mcp` or remote URL
- **Dependencies**: Tavily API key
- **Tools**: search, extract, map, crawl
- **Security**: API key
- **Use Cases**: Real-time web search, content extraction
- **Priority**: 9/10

### 20. Perplexity MCP
- **GitHub**: https://github.com/nicholasgriffinintc/perplexity-mcp-server
- **Install**: `npx -y perplexity-mcp-server`
- **Dependencies**: Perplexity API key
- **Tools**: AI-powered web search, Q&A
- **Security**: API key
- **Use Cases**: Research, fact-checking, summarization
- **Priority**: 8/10
- **Status**: ALREADY CONFIGURED in OpenCode

### 21. Browserbase MCP
- **GitHub**: https://github.com/nicholasgriffinintc/browserbase-mcp-server
- **Install**: `npx -y browserbase-mcp-server`
- **Dependencies**: Browserbase API key
- **Tools**: Browser automation, screenshots, data extraction
- **Security**: API key, sandboxed browsers
- **Use Cases**: Complex web automation, login-required sites
- **Priority**: 7/10

### 22. Exa MCP (Official)
- **GitHub**: https://github.com/exa-labs/exa-mcp-server
- **Install**: `npx -y exa-mcp-server`
- **Dependencies**: Exa API key
- **Tools**: Semantic search, content extraction, site crawling
- **Security**: API key
- **Use Cases**: Semantic web search, research
- **Priority**: 8/10

---

## Databases

### 23. Database MCP (Multi-DB)
- **GitHub**: https://github.com/haymon-ai/database-mcp
- **Install**: Download binary (~7MB)
- **Dependencies**: None (single binary)
- **Tools**: listDatabases, listTables, readQuery, writeQuery, explainQuery
- **Security**: Read-only mode, PII redaction (46 entity types)
- **Use Cases**: MySQL, PostgreSQL, SQLite access
- **Priority**: 9/10
- **Status**: RECOMMENDED - covers all database needs

### 24. PostgreSQL MCP
- **GitHub**: https://github.com/nicholasgriffinintc/postgres-mcp-server
- **Install**: `npx -y postgres-mcp-server`
- **Dependencies**: PostgreSQL connection string
- **Tools**: Query execution, schema exploration
- **Security**: Connection pooling, SSL support
- **Use Cases**: PostgreSQL database access
- **Priority**: 8/10

### 25. MySQL MCP
- **GitHub**: https://github.com/nicholasgriffinintc/mysql-mcp-server
- **Install**: `npx -y mysql-mcp-server`
- **Dependencies**: MySQL connection string
- **Tools**: Query execution, schema discovery
- **Security**: SSL support, credential management
- **Use Cases**: MySQL database access
- **Priority**: 7/10

---

## Development

### 26. GitHub MCP (Official)
- **GitHub**: https://github.com/nicholasgriffinintc/github-mcp-server
- **Install**: `npx -y @modelcontextprotocol/server-github`
- **Dependencies**: GitHub Personal Access Token
- **Tools**: Repos, issues, PRs, code search, actions
- **Security**: PAT with granular scopes
- **Use Cases**: Code management, CI/CD, code review
- **Priority**: 9/10
- **Status**: ALREADY CONFIGURED (disabled, needs PAT)

### 27. GitLab MCP
- **GitHub**: https://github.com/nicholasgriffinintc/gitlab-mcp-server
- **Install**: `npx -y gitlab-mcp-server`
- **Dependencies**: GitLab API token
- **Tools**: Repos, issues, MRs, pipelines
- **Security**: API token with scopes
- **Use Cases**: GitLab code management
- **Priority**: 7/10

---

## Already Installed/Configured

| MCP Server | Status | Notes |
|------------|--------|-------|
| Playwright | ACTIVE | Browser automation |
| Filesystem | ACTIVE | File system access |
| Perplexity | ACTIVE | AI search |
| Firecrawl | ACTIVE | Web scraping |
| Memory | ACTIVE | Persistent memory |
| Sequential Thinking | ACTIVE | Chain-of-thought |
| Context7 | ACTIVE | Documentation lookup |
| YouTube | ACTIVE | YouTube data |
| Yahoo Finance | ACTIVE | Financial data |
| NewsAPI | ACTIVE | News aggregation |
| LinkedIn | ACTIVE | LinkedIn scraping |
| Captions | ACTIVE | Video captions |
| Claude-Mem | ACTIVE | Claude memory |
| Apify | ACTIVE | Web scraping actors |
| Notion | ACTIVE | Notion API |
| GitHub | DISABLED | Needs PAT |
| Google Calendar | DISABLED | Needs OAuth |
| Discord | DISABLED | Needs bot token |
| Reddit | DISABLED | Needs API credentials |

---

## Priority Installation Order

### Phase 1: Critical (Install Now)
1. **Nexus** - Unified communications (Gmail + Slack + Discord)
2. **Database MCP** - Multi-database access
3. **GitHub MCP** - Enable with PAT
4. **Tavily MCP** - Enhanced web research

### Phase 2: High Priority
5. **Apollo MCP** - Lead generation
6. **HubSpot MCP** - CRM integration
7. **Obsidian MCP** - Knowledge management
8. **Google Drive MCP** - Document management

### Phase 3: Medium Priority
9. **Clay MCP** - Advanced enrichment
10. **SmartLead MCP** - Email campaigns
11. **Browserbase MCP** - Advanced browser automation
12. **OneDrive MCP** - Enterprise file storage

### Phase 4: Optional
13. **Salesforce MCP** - Enterprise CRM
14. **GitLab MCP** - GitLab integration
15. **Instantly MCP** - Cold email at scale

---

## Summary

| Category | Total Available | Installed | Recommended |
|----------|----------------|-----------|-------------|
| Communications | 5 | 0 | Nexus (unified) |
| Productivity | 4 | 1 (Notion) | Obsidian, Google Drive |
| CRM | 3 | 0 | HubSpot |
| Lead Gen | 5 | 0 | Apollo, GTM MCP |
| Research | 5 | 3 (Firecrawl, Perplexity, Apify) | Tavily |
| Databases | 3 | 0 | Database MCP (multi-DB) |
| Development | 2 | 1 (GitHub, disabled) | Enable GitHub |

**Total MCPs to install: 12** (across all phases)
