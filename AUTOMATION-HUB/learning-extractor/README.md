# AI Learning Extractor

Turns a URL, pasted text, or local file into an implementation-ready learning report for the Titus AI OS.

The goal is simple: stop losing good ideas from Reels, videos, courses, docs, and screenshots. Convert them into lessons, reusable prompts, bot commands, skills, and next actions.

## Desktop usage

From PowerShell:

```powershell
cd "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor"
.\Start-LearningExtractor.ps1 -Url "https://example.com/article"
```

Text input:

```powershell
.\Start-LearningExtractor.ps1 -Text "Paste the useful lesson here."
```

File input:

```powershell
.\Start-LearningExtractor.ps1 -File "C:\path\to\notes.txt"
```

Reports are saved in:

```text
C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor\outputs
```

## Telegram and WhatsApp usage

Your OpenClaw bots can call this tool through shell execution. Use either exact commands or natural language.

Examples to send to Telegram or WhatsApp:

```text
/learn-source https://anthropic.skilljar.com/
```

```text
Learn this: https://www.facebook.com/reel/3762177677257523
```

```text
/learn-text The main lesson is to use Claude to extract core learnings from courses and turn them into reusable workflows.
```

Agent command mapping:

```powershell
& "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor\Start-LearningExtractor.ps1" -Url "<url>"
```

```powershell
& "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor\Start-LearningExtractor.ps1" -Text "<text>"
```

## Restore on a new device

After cloning the Titus AI OS repo from GitHub, reinstall the bot skill with:

```powershell
openclaw skills install "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor" --as learning-extractor --agent main --force
```

If OpenClaw does not list the skill immediately, copy the skill into the personal skills folder:

```powershell
New-Item -ItemType Directory -Force "C:\Users\tbank\.agents\skills\learning-extractor"
Copy-Item "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor\SKILL.md" "C:\Users\tbank\.agents\skills\learning-extractor\SKILL.md" -Force
```

Then verify:

```powershell
openclaw skills list | Select-String learning-extractor
```

## Screenshots and videos

The lightweight extractor does not install OCR or video transcription. For screenshots and video/Reel content:

1. Send the screenshot to the assistant, or paste visible text from it.
2. Ask the bot: `Learn this screenshot`.
3. The assistant should extract visible text using vision, then run `-Text` with the extracted content.

Future upgrade: add approved local OCR and transcription after user approval.

## Approval gates

The extractor is safe for intake and summaries. It must not auto-send messages, buy tools, connect accounts, post online, or edit secrets without explicit user approval.
