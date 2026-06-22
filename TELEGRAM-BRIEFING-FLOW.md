# Telegram Briefing Flow

## Purpose
Send a project-manager style execution briefing to your phone through Telegram without depending on Gmail.

## Inputs
- Morning briefing from `DAILY-BRIEFING-PROMPT.md`
- Daily scorecard
- Downloads organizer log
- School / personal / home backlog

## Required Credentials
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

## Script
- `C:\Users\tbank\Desktop\4_Automation\Scripts\Send-Telegram-Briefing.ps1`

## Message Format
Use short sections:
- Time-aware greeting
- What matters now
- Today's command list
- Project radar
- Already started
- Lagging / needs attention
- Calendar / reminders
- Career / income
- Education
- Agency / content systems
- Home / admin
- Behind or lagging
- Not clear yet
- Market radar
- Logistics
- One assignment

## Rules
- If Gmail fails, still send the briefing.
- If a task repeats, move it into the overdue list.
- If a file bucket keeps growing, mention it in the briefing.
- If the phone message gets too long, send the top priorities first and move the rest to a second message.
- Do not surface tool failures as the main briefing unless they require action.
- Use the actual time of day for the greeting and action plan, even if the scheduled task passes the wrong mode.
- Convert vague goals into the next visible action.
- Track ideas like the book project, analyst 30-day plan, portfolio, NOLO scheduling, Content Absorption, and education progress.

## Suggested Schedule
- 8:00 AM: Morning briefing
- 12:00 PM: Midday reset
- 8:00 PM: Evening closeout

## Next Step
Fill in the Telegram bot token and chat id, then I can wire the scheduled send.
