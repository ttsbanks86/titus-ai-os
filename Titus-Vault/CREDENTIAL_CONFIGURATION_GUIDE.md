# Credential Configuration Guide

## Overview

This guide explains how to securely configure credentials for the Titus AI OS.

## Security Principles

1. **Never commit credentials** to version control
2. **Use environment variables** for all secrets
3. **Rotate credentials** regularly
4. **Use minimal permissions** for each credential

## Setup Instructions

### 1. Create Environment File

```bash
cp .env.example .env
```

### 2. Configure Credentials

Edit `.env` and fill in your credentials:

```bash
# OpenRouter API Key
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Telegram Bot Token
HERMES_TELEGRAM_TOKEN=your-bot-token-here

# Notion API Token
NOTION_TOKEN=ntn-your-token-here

# GitHub Personal Access Token
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_your-token-here

# Tavily API Key
TAVILY_API_KEY=tvly-your-key-here
```

### 3. Verify .gitignore

Ensure `.env` is in `.gitignore`:

```bash
grep -q "^\.env$" .gitignore && echo "Protected" || echo ".env not in .gitignore!"
```

## Credential Sources

### OpenRouter API Key
- **Service**: OpenRouter (openrouter.ai)
- **Purpose**: AI model access
- **Setup**: https://openrouter.ai/keys

### Telegram Bot Token
- **Service**: Telegram Bot API
- **Purpose**: Hermes bot integration
- **Setup**: https://t.me/BotFather

### Notion API Token
- **Service**: Notion API
- **Purpose**: Knowledge base integration
- **Setup**: https://www.notion.so/my-integrations

### GitHub Personal Access Token
- **Service**: GitHub API
- **Purpose**: Repository access
- **Setup**: https://github.com/settings/tokens

### Tavily API Key
- **Service**: Tavily Search API
- **Purpose**: Web search
- **Setup**: https://tavily.com

## Rotation Schedule

| Credential | Rotation Period | Notes |
|------------|----------------|-------|
| OpenRouter | Every 90 days | Or if compromised |
| Telegram | Every 180 days | Or if bot is compromised |
| Notion | Every 90 days | Or if workspace is compromised |
| GitHub PAT | Every 90 days | Or if access is compromised |
| Tavily | Every 180 days | Or if compromised |

## Emergency Response

If a credential is exposed:

1. **Revoke immediately** through the service dashboard
2. **Generate new credential**
3. **Update .env** with new value
4. **Check audit logs** for unauthorized access
5. **Document the incident**

## CI/CD Configuration

For GitHub Actions, use repository secrets:

1. Go to repository Settings → Secrets and variables → Actions
2. Add each credential as a repository secret
3. Reference in workflows as `${{ secrets.CREDENTIAL_NAME }}`

## Validation

Test your configuration:

```bash
# Check if environment variables are set
python -c "import os; print('OPENROUTER_API_KEY' in os.environ)"

# Run tests (should pass without real credentials)
pytest tests/ -v
```
