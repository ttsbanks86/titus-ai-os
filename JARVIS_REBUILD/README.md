# Jarvis Rebuild

This is a clean rebuild of Jarvis. The old voice, routing, intent, and OpenClaw code is isolated in `JARVIS_OLD_BROKEN` and is not imported here.

## Architecture

- `app/main.py` provides command-line, text-loop, and push-to-talk entry points.
- `app/intents.py` cleans transcripts and classifies simple intents.
- `app/router.py` applies the routing order and writes command audit logs.
- `app/voice/` contains isolated capture, transcription, speech, and turn management modules.
- `app/tools/` contains local capabilities, browser, calendar, email, weather, files, system, and optional OpenClaw adapters.
- `app/memory/short_term.py` tracks recent assistant speech for self-speech rejection.
- `app/memory/profile.py` reads approved Titus profile notes from the configured Obsidian vault.
- `tests/` verifies intent classification, route selection, command audit logs, self-speech rejection, and OpenClaw restrictions.

## Routing Order

1. Noise rejection
2. System commands
3. Built-in capabilities
4. Weather
5. Memory
6. Files
7. Calendar
8. Email
9. OpenClaw
10. LLM-backed basic chat and system questions
11. Fallback setup response

Implemented routes stay local before OpenClaw. Browser open/search/close, Obsidian search, read-only Gmail, file creation, weather, and calendar setup detection are active.

## Setup

```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD"
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` if you want to track local settings. The current code reads environment variables directly.

## Weather Setup

Jarvis supports a no-key `wttr` provider, OpenWeatherMap, or WeatherAPI for current weather.

No-key default:

```powershell
$env:JARVIS_WEATHER_PROVIDER="wttr"
python app/main.py --command "Jarvis, what's the weather today?"
```

PowerShell example:

```powershell
$env:JARVIS_WEATHER_PROVIDER="openweathermap"
$env:JARVIS_WEATHER_API_KEY="your_api_key_here"
$env:JARVIS_DEFAULT_LOCATION="New Orleans, LA"
python app/main.py --command "Jarvis, what's the weather today?"
```

WeatherAPI example:

```powershell
$env:JARVIS_WEATHER_PROVIDER="weatherapi"
$env:JARVIS_WEATHER_API_KEY="your_api_key_here"
$env:JARVIS_DEFAULT_LOCATION="New Orleans, LA"
python app/main.py --command "Jarvis, what's the weather today?"
```

Required variables:

- `JARVIS_WEATHER_PROVIDER`: `openweathermap` or `weatherapi`
- `JARVIS_WEATHER_API_KEY`: your provider API key
- `JARVIS_DEFAULT_LOCATION`: city, state, ZIP, or other provider-supported location

If these are missing, Jarvis gives a setup response instead of routing weather to OpenClaw.

## Obsidian Vault

Jarvis has read-only vault access. It reads configured index files first, follows Obsidian wikilinks, then falls back to broad Markdown search inside the allowed vault path.

```powershell
$env:JARVIS_OBSIDIAN_VAULT_PATH="C:\Users\tbank\Desktop\Live Cowork\Titus-Vault"
$env:JARVIS_OBSIDIAN_INBOX_PATH="C:\Users\tbank\Desktop\Live Cowork\Titus-Vault\02-Daily-Notes"
$env:JARVIS_OBSIDIAN_INDEX_FILES="VAULT-INDEX.md;09-Knowledge/Knowledge-Index.md;08-Agents/Agents-Index.md"
$env:JARVIS_ALLOWED_FILE_ROOTS="C:\Users\tbank\Desktop\Live Cowork\Titus-Vault"
```

Supported examples:

```powershell
python app/main.py --command "Jarvis, search Obsidian for Jarvis system"
python app/main.py --command "Jarvis, what do I have in my vault about AI agents?"
python app/main.py --command "Jarvis, find my note about marketing"
```

Vault search is read-only and returns a short answer, note title, full path, and short preview. Jarvis does not read long Markdown sections aloud unless asked.

## Workspace Files

Jarvis can create new Markdown files inside the approved workspace path, and new Obsidian notes inside the configured Obsidian inbox path:

```powershell
$env:JARVIS_WORKSPACE_PATH="C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD\workspace"
$env:JARVIS_OBSIDIAN_INBOX_PATH="C:\Users\tbank\Desktop\Live Cowork\Titus-Vault\02-Daily-Notes"
$env:JARVIS_FILE_EDITING_ENABLED="true"
python app/main.py --command "Jarvis, create a file called project-notes.md"
python app/main.py --command "Jarvis, create an Obsidian note about my Jarvis setup"
```

Appending to existing files requires approval. Overwriting files requires approval. Files outside allowed roots are blocked.

## Browser

Browser open, close, website, and web search commands execute locally and do not route to OpenClaw.

```powershell
$env:JARVIS_DEFAULT_BROWSER="chrome"
$env:JARVIS_BROWSER_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
python app/main.py --command "Jarvis, open Chrome"
python app/main.py --command "Jarvis, open browser"
python app/main.py --command "Jarvis, close browser"
python app/main.py --command "Jarvis, search the web for AI agents"
```

`JARVIS_BROWSER_PATH` is optional if `chrome`, `msedge`, or `firefox` is already available on PATH.

## Google Calendar

Calendar starts read-only. If it is not connected, Jarvis says:

```text
Calendar access is not connected yet. I can add Google Calendar next.
```

Setup variables:

```powershell
$env:JARVIS_GOOGLE_CALENDAR_ENABLED="true"
$env:JARVIS_GOOGLE_CALENDAR_CREDENTIALS_PATH="C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD\secrets\google-calendar-client-secret.json"
$env:JARVIS_GOOGLE_CALENDAR_TOKEN_PATH="C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD\secrets\google-calendar-token.json"
```

Supported schedule intent examples:

```powershell
python app/main.py --command "Jarvis, what am I working on today?"
python app/main.py --command "Jarvis, what is on my schedule today?"
python app/main.py --command "Jarvis, what do I have today?"
python app/main.py --command "Jarvis, what are my tasks today?"
```

The first connected run opens a local OAuth browser flow if the token file does not exist, then stores the read-only token at `JARVIS_GOOGLE_CALENDAR_TOKEN_PATH`.

Calendar scope is read-only: `https://www.googleapis.com/auth/calendar.readonly`. Calendar updates remain blocked behind approval.

## Composio Connector

Composio is the optional external app connector for Gmail, Google Calendar, Google Drive, and Notion. Secrets stay in environment variables; Jarvis never hardcodes API keys.

```powershell
$env:JARVIS_COMPOSIO_ENABLED="true"
$env:JARVIS_COMPOSIO_API_KEY="your_composio_project_api_key"
$env:JARVIS_COMPOSIO_USER_ID="titus-local"
$env:JARVIS_COMPOSIO_ALLOWED_TOOLS="gmail;googlecalendar;googledrive;notion"
$env:JARVIS_CONNECTOR_MODE="composio"
```

Read-only app requests can use Composio when `JARVIS_CONNECTOR_MODE=composio`. Write actions still require Jarvis approval first:

- send email
- create or update calendar event
- create Notion page
- edit Drive file
- delete anything

If Composio is not configured, Jarvis gives a clean setup response instead of attempting tool execution.

If Composio has an auth config but no active connected account visible, Jarvis can still use direct read-only Gmail when `JARVIS_GMAIL_CREDENTIALS_PATH` and `JARVIS_GMAIL_TOKEN_PATH` are configured.

## LLM and Titus Context

Jarvis can answer basic questions and system questions through a connected LLM after local routes have had the first chance to handle the command. This is for natural conversation, explanations, planning, and questions such as:

```powershell
python app/main.py --no-speech --command "Jarvis, what do you know about me?"
python app/main.py --no-speech --command "Why is the sky blue?"
python app/main.py --no-speech --command "Jarvis, what tools are connected?"
```

OpenAI setup:

```powershell
$env:JARVIS_LLM_ENABLED="true"
$env:JARVIS_LLM_PROVIDER="openai"
$env:JARVIS_LLM_API_KEY="your_key_here"
$env:JARVIS_LLM_MODEL="gpt-4.1-mini"
```

If `JARVIS_LLM_API_KEY` is blank, Jarvis also checks `OPENAI_API_KEY`. Secrets should stay in `.env` or local environment variables.

Local Ollama setup:

```powershell
ollama serve
ollama pull llama3.2
$env:JARVIS_LLM_ENABLED="true"
$env:JARVIS_LLM_PROVIDER="ollama"
$env:JARVIS_LLM_MODEL="llama3.2"
```

Ollama uses `http://127.0.0.1:11434/api/generate` by default unless `JARVIS_LLM_BASE_URL` is set.

Profile context is read only from approved vault files:

```powershell
$env:JARVIS_USER_PROFILE_ENABLED="true"
$env:JARVIS_USER_PROFILE_FILES="MEMORY.md;01-Dashboard/Personal-Context.md;01-Dashboard/My-Goals.md;01-Dashboard/My-Rules.md;01-Dashboard/My-Voice.md"
```

The LLM is still behind safety rules. It cannot bypass approval for sending email, deleting or moving files, running terminal commands, spending money, updating calendar events, or allowing OpenClaw to execute changes.

## Mission Control API

Jarvis can expose a local API for Mission Control:

```powershell
python app/main.py --api
python app/main.py --doctor
```

Default endpoint:

```text
http://127.0.0.1:8765
```

Endpoints:

- `GET /health`
- `GET /status`
- `GET /audit/latest`
- `POST /command` with `{ "command": "Jarvis, what are your capabilities?" }`
- `POST /approval` with `{ "decision": "approve" }` or `{ "decision": "cancel" }`

Mission Control cannot bypass Jarvis approvals. Risky requests still become pending approvals inside Jarvis.

## Email

Email starts read-only. If Gmail is not connected, Jarvis returns a clean placeholder:

```powershell
python app/main.py --command "Jarvis, check my email"
```

Read-only Gmail setup uses local OAuth files. Do not hardcode secrets.

```powershell
$env:JARVIS_GMAIL_CREDENTIALS_PATH="C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD\secrets\gmail-client-secret.json"
$env:JARVIS_GMAIL_TOKEN_PATH="C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD\secrets\gmail-token.json"
$env:JARVIS_GMAIL_MAX_RESULTS="5"
python app/main.py --command "Jarvis, check my email"
```

The first connected run opens a local OAuth browser flow if the token file does not exist, then stores the read-only token at `JARVIS_GMAIL_TOKEN_PATH`.

Supported Gmail commands:

```powershell
python app/main.py --command "Jarvis, check my email"
python app/main.py --command "Jarvis, do I have new emails?"
python app/main.py --command "Jarvis, summarize my latest emails"
python app/main.py --command "Jarvis, search my email for invoices"
```

Gmail scope is read-only: `https://www.googleapis.com/auth/gmail.readonly`. Jarvis does not send, delete, archive, or label emails yet. Sending email remains blocked behind approval and postponed.

## Windows Audio Setup

Use PowerShell:

```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python app/main.py --list-mics
```

If Windows blocks microphone access, open Settings, then Privacy & security, then Microphone, and allow microphone access for desktop apps.

If multiple microphones are listed, pass the device index:

```powershell
python app/main.py --test-mic --mode enter --input-device 2
python app/main.py --push-to-talk --input-device 2
```

## Test

```powershell
python -m pytest
python -m py_compile app/main.py app/router.py app/intents.py
```

## Acceptance Commands

```powershell
python app/main.py --no-speech --command "Jarvis, what are your capabilities?"
python app/main.py --no-speech --command "Jarvis, what's the weather today?"
python app/main.py --no-speech --command "Hello Jarvis"
python app/main.py --no-speech --command "I'll see you in the next one."
python app/main.py --no-speech --command "Help me debug this Python script"
python app/main.py --no-speech --command "Jarvis, open Chrome"
python app/main.py --no-speech --command "Jarvis, what am I working on today?"
python app/main.py --no-speech --command "Jarvis, search Obsidian for AI agents"
python app/main.py --no-speech --command "Jarvis, check my email"
python app/main.py --no-speech --command "Jarvis, what do you know about me?"
python app/main.py --no-speech --command "Why is the sky blue?"
python app/main.py --api
```

The background-noise command intentionally prints nothing and writes a rejected audit record.

## Approval Layer

Jarvis requires explicit approval before risky actions:

- send email
- delete files
- move files
- run terminal commands
- spend money
- update calendar
- connect OpenClaw to execute changes

Jarvis summarizes the pending action first. To approve, say exactly:

```text
yes, approve
```

To discard the pending action, say:

```text
cancel
```

Execution is not connected yet; approved actions are recorded as approved but not run.

## OpenClaw

OpenClaw is an optional tool for coding, debugging, app build tasks, and system planning.

It does not handle:

- greetings
- weather
- capabilities
- noise
- basic chat
- unclear commands

Configure it with:

```powershell
$env:JARVIS_OPENCLAW_ENABLED="true"
$env:JARVIS_OPENCLAW_COMMAND="C:\Users\tbank\AppData\Roaming\npm\openclaw.cmd agent --local --agent main --message"
$env:JARVIS_OPENCLAW_TIMEOUT_SECONDS="180"
```

This rebuild configures OpenClaw to use a local Ollama model (`ollama/llama3.2:3b`) instead of the invalid OpenAI provider key. OpenClaw output is filtered before Jarvis speaks it so provider diagnostics are not read aloud.

OpenClaw selection is logged in the command audit with the reason it was selected. Requests that would make OpenClaw change files, run commands, delete files, move files, or execute tasks require the approval phrase first:

```text
yes, approve
```

## Push-To-Talk

```powershell
python app/main.py --push-to-talk
python app/main.py --push-to-talk --mode hold
python app/main.py --push-to-talk --mode enter
```

Default push-to-talk mode is hold-to-talk with Right Ctrl:

1. Run `python app/main.py --push-to-talk`.
2. Hold Right Ctrl.
3. Speak.
4. Release Right Ctrl to stop recording.

Console status:

```text
Hold Right Ctrl to talk
Recording...
Processing...
Jarvis: ...
```

Enter fallback mode records a fixed window after Enter:

```powershell
python app/main.py --push-to-talk --mode enter --record-seconds 5
```

Recordings are transcribed, routed, spoken, and logged to `app/logs/command_audit.jsonl`.

Debug WAV files are saved only when debug audio is enabled:

```powershell
python app/main.py --push-to-talk --debug-audio
```

Debug files are written to `app/logs/audio_debug/`. Without debug audio, temporary WAV files are deleted after transcription.

Run a one-turn microphone test:

```powershell
python app/main.py --test-mic --mode enter --record-seconds 5
```

Hold-to-talk depends on `pynput`, `sounddevice`, `numpy`, `scipy`, and `SpeechRecognition`. Speech output uses `pyttsx3` when enabled.

Recovered safe voice settings from the old Jarvis config:

```powershell
$env:JARVIS_TTS_ENGINE="edge-tts"
$env:JARVIS_TTS_VOICE="en-GB-RyanNeural"
$env:JARVIS_TTS_RATE="+10%"
$env:JARVIS_TTS_VOLUME="1.0"
$env:JARVIS_TTS_PITCH="-20Hz"
```

These are configuration values only. No old routing, intent, OpenClaw, or voice pipeline code was copied.

## Speech Recognition

Recording defaults:

- `JARVIS_SAMPLE_RATE=16000`
- `JARVIS_RECORD_END_PADDING_MS=500`
- `JARVIS_MIN_RECORD_SECONDS=0.35`
- hold mode also keeps about 250ms of pre-roll before the push key is pressed

Transcription defaults to SpeechRecognition:

```powershell
$env:JARVIS_TRANSCRIBE_PROVIDER="speechrecognition"
```

Optional local Whisper mode:

```powershell
$env:JARVIS_TRANSCRIBE_PROVIDER="whisper"
python -m pip install openai-whisper
```

If Whisper is requested but not installed, Jarvis falls back to SpeechRecognition and shows the fallback in debug output.

## Rebuilt, Removed, Postponed

Rebuilt:
- Clean command-line core
- Intent classification
- Local-first router
- Capability and weather handlers
- Browser control
- Read-only Gmail setup and summary path
- Calendar read-only setup boundary
- Composio connector boundary
- Mission Control local API
- LLM fallback for basic chat and system questions
- Titus profile context from approved vault notes
- Safe Obsidian search response formatting
- JSONL command audit logging
- Push-to-talk capture/transcription modules
- Self-speech rejection
- Optional OpenClaw adapter boundary

Removed or isolated:
- Old Jarvis folder moved to `JARVIS_OLD_BROKEN`
- Old OpenClaw bridge isolated with the old system
- Old voice capture, wake, and realtime listener code isolated
- Old intent and routing logic isolated

Postponed:
- Wake word
- Always-listening mode
- Barge-in
- Calendar write/update actions
- Composio write actions
- Full OpenClaw reconnection with a configured command
