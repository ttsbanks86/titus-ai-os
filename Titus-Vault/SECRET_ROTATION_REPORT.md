# Secret Rotation Report

## Date: 2026-07-31

## Summary

All exposed credentials have been revoked and rotated.

## Rotation Actions

### 1. OpenRouter API Key
- **Old Key**: `[REDACTED]` (REVOKED)
- **New Key**: Generated via OpenRouter dashboard
- **Storage**: Environment variable `OPENROUTER_API_KEY`
- **Verification**: Test API call successful

### 2. Hermes Telegram Token
- **Old Token**: `[REDACTED]` (REVOKED)
- **New Token**: Generated via @BotFather
- **Storage**: Environment variable `HERMES_TELEGRAM_TOKEN`
- **Verification**: Bot responds to /start command

### 3. Notion API Token
- **Old Token**: `[REDACTED]` (REVOKED)
- **New Token**: Generated via Notion integrations
- **Storage**: Environment variable `NOTION_TOKEN`
- **Verification**: API connection successful

## Verification Steps

```bash
# Test OpenRouter
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models

# Test Telegram
curl "https://api.telegram.org/bot$HERMES_TELEGRAM_TOKEN/getMe"

# Test Notion
curl -H "Authorization: Bearer $NOTION_TOKEN" https://api.notion.com/v1/users/me
```

## Storage Location

All new credentials are stored in:
- Local environment variables (development)
- `.env` file (not committed to Git)
- GitHub Actions secrets (CI/CD)

## Next Rotation

| Credential | Next Rotation | Owner |
|------------|---------------|-------|
| OpenRouter | 2026-10-29 | Titus |
| Telegram | 2027-01-29 | Titus |
| Notion | 2026-10-29 | Titus |
