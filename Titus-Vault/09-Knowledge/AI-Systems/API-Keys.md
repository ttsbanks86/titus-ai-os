# API Keys

## Overview
API key inventory for the Titus AI OS. This file tracks which keys are configured, which are placeholders, and where each key is stored. No actual key values are stored here.

## Key Inventory

| Service | Status | Storage Location | Notes |
|---|---|---|---|
| ANTHROPIC_API_KEY | Placeholder | `~/.config/opencode/.env` | Must fill in personal key |
| OPENAI_API_KEY | Placeholder | `~/.config/opencode/.env` | Must fill in personal key |
| OPENCODE_API_KEY | Placeholder | `~/.config/opencode/.env` | Must fill in personal key |
| KIE_API_KEY | ✅ Loaded | `~/.config/opencode/.env` | Real, tested, working |
| FIRECRAWL_API_KEY | Not configured | N/A | Not yet set up |
| APIFY_API_KEY | Not configured | N/A | Not yet set up |

## Key Loading
Keys are loaded using `Set-CloudApiKeys.ps1` from `~/.config/opencode/.env` as user-level environment variables.

## Security Rules
- API keys are never stored in config files
- Keys never appear in shared prompts or delegated tasks
- Set-CloudApiKeys.ps1 is the single entry point for loading all keys

## Linked Notes
- [[OpenCode-Config]]
- [[Model-Routing]]
- [[Provider-Architecture]]
- [[09-Knowledge/Knowledge-Index]]

## Active Tasks
- [ ] Load real API keys after user fills `.env`
- [ ] Verify key loading script works end-to-end

## References
- `C:\Users\tbank\.config\opencode\.env`
- `C:\Users\tbank\Desktop\Live Cowork\Set-CloudApiKeys.ps1`
- `C:\Users\tbank\.config\opencode\api-keys-template.txt`
