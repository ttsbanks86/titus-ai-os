# OpenClaw Bot Instruction Card: AI Learning Extractor

When Titus sends a URL, screenshot, Reel, article, transcript, or text with phrases like:

- `learn this`
- `/learn-source`
- `/learn-text`
- `extract the lessons`
- `turn this into a skill`
- `can we implement this?`

Use the AI Learning Extractor workflow.

## URL command

Run:

```powershell
& "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor\Start-LearningExtractor.ps1" -Url "<URL>"
```

Then reply with:

1. the report path,
2. the top 3 lessons,
3. whether it should become a workflow, skill, memory note, or project task.

## Text command

Run:

```powershell
& "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\learning-extractor\Start-LearningExtractor.ps1" -Text "<TEXT>"
```

## Screenshot/video command

If the message contains an image or video and the bot cannot read it directly:

1. Ask Titus for the visible text or transcript, or ask him to send a screenshot to the assistant session.
2. Once text is available, run the `-Text` command.

## Do not

- Do not log into accounts.
- Do not post, send, buy, or connect accounts.
- Do not edit secrets or bot tokens.
- Do not install OCR/transcription tools without approval.
