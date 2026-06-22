# Odysseus Guided Setup

## Step 1 — Open Odysseus
Open:
```text
http://127.0.0.1:7000
```

Or use the Desktop shortcut:
```text
Odysseus.lnk
```

## Step 2 — Login
Username:
```text
admin
```

Temporary password is available from Docker logs or the temporary password file if you moved it there.

After login, change the password immediately.

## Step 3 — Model Providers
Go to Odysseus Settings and look for model/provider settings.

Use these local endpoints:

### LM Studio
```text
http://host.docker.internal:1234
```

If Odysseus asks for OpenAI-compatible base URL, try:
```text
http://host.docker.internal:1234/v1
```

### Ollama
```text
http://host.docker.internal:11434
```

If Odysseus asks for OpenAI-compatible base URL, try:
```text
http://host.docker.internal:11434/v1
```

## Step 4 — Test Chat
Pick a local model and send:

```text
Hello. Confirm you are responding from a local model.
```

## Step 5 — Search
SearXNG is bundled and reachable inside Docker as:
```text
http://searxng:8080
```

Host URL:
```text
http://127.0.0.1:8080
```

## Step 6 — Memory / RAG
ChromaDB is bundled and reachable inside Docker as:
```text
http://chromadb:8000
```

Host URL:
```text
http://127.0.0.1:8100
```

## Step 7 — Email
Odysseus email is not configured yet.

You will need:
- Email address
- IMAP server
- IMAP port
- SMTP server
- SMTP port
- App password or provider-specific password

For Gmail, use a Google App Password, not your normal password.

## Step 8 — Calendar
You will need CalDAV info if you want calendar sync.

Examples:
- Apple iCloud Calendar uses app-specific password.
- Fastmail supports CalDAV.
- Nextcloud supports CalDAV.

## Step 9 — Notifications
ntfy is running locally:
```text
http://127.0.0.1:8091
```

## Step 10 — Phone Access
For phone access, keep it local/private.
Options:
- VS Code tunnel / forwarded port
- Tailscale
- Local LAN only if secured

Do not expose Odysseus publicly without strong authentication and HTTPS.
