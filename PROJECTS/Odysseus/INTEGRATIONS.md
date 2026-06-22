# Odysseus Integration Status

## Local URL
`http://127.0.0.1:7000`

## Install Folder
`C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\odysseus`

## Core Docker Services

| Service | Purpose | Status | URL / Endpoint |
|---|---|---|---|
| Odysseus | Main app | ✅ Running | `http://127.0.0.1:7000` |
| ChromaDB | Vector store / memory | ✅ Running | `http://127.0.0.1:8100` |
| SearXNG | Self-hosted web search | ✅ Running | `http://127.0.0.1:8080` |
| ntfy | Notifications | ✅ Running | `http://127.0.0.1:8091` |

## Local Model Integrations

| Integration | Host Endpoint | Docker Endpoint | Status |
|---|---|---|---|
| LM Studio | `http://127.0.0.1:1234/v1/models` | `http://host.docker.internal:1234/v1/models` | ✅ Added in Odysseus; 4 models found |
| Ollama | `http://127.0.0.1:11434/api/tags` | `http://host.docker.internal:11434/v1` | ✅ Added in Odysseus; `gemma2:2b` found |

## Odysseus UI Model Defaults

| Setting | Value | Status |
|---|---|---|
| Default chat endpoint | `host.docker.internal:1234` | ✅ Set |
| Default chat model | `qwen2.5-coder-7b-instruct` | ✅ Set and tested |
| Utility endpoint | `host.docker.internal:11434` | ✅ Set |
| Utility model | `gemma2:2b` | ✅ Set |
| Chat smoke test | Prompt returned: "Odysseus local model is working." | ✅ Passed |

## `.env` Local Setup
Current local `.env` is configured for:

```text
APP_BIND=127.0.0.1
APP_PORT=7000
AUTH_ENABLED=true
LM_STUDIO_URL=http://host.docker.internal:1234
OLLAMA_BASE_URL=http://host.docker.internal:11434/v1
LLM_HOST=host.docker.internal
SEARXNG_INSTANCE=http://searxng:8080
```

## Needs User Credentials / Optional Setup
These cannot be fully completed without user-provided credentials, permission, or optional API keys:

| Integration | Needed From User | Notes |
|---|---|---|
| Email IMAP/SMTP | Email address, app password, IMAP/SMTP servers | Odysseus logs show email is not configured yet. |
| Calendar CalDAV | Provider URL, username, app password | Apple/Fastmail/Nextcloud/etc. |
| OpenAI / OpenRouter | API key if wanted | Optional; local LM Studio/Ollama already work. |
| Notifications | Browser permission or ntfy topic setup | ntfy service is running locally. |

## Login Help
Username:
```text
admin
```

Retrieve temporary password:
```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\odysseus"
docker compose logs odysseus --tail 80
```

Look for:
```text
Temporary password:
```

Do not save long-term passwords in plain text.

## Completed Setup Order
1. ✅ Login to Odysseus.
2. ✅ Go to Settings → Add Models.
3. ✅ Add/test LM Studio endpoint.
4. ✅ Add/test Ollama endpoint.
5. ✅ Select default chat model.
6. ✅ Select utility model.
7. ✅ Test Chat with local model.

## Remaining Optional Setup
1. Change admin password if not already changed.
2. Configure Email if desired.
3. Configure Calendar if desired.
4. Configure Notifications.
5. Add documents/files for RAG if desired.
