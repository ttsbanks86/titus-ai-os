# Bot Setup Mismatch

Problem: Bot setup became confusing because Telegram/BotFather text, pasted token checks, Hermes/OpenClaw gateway logs, and OpenCode-Go config could refer to different bots.

Known facts from latest session:

- Working gateway logs referenced `@Bankshez_bot`.
- A pasted token was verified as a different bot: `@titus_ai_ops_bot`.
- Fresh bot project `openclaw-telegram-bot` was created, then deleted after confirming old bot worked.

Rule:

- Verify bot identity with gateway logs or Telegram `getMe` before changing config.
- Rotate pasted tokens before production.
- Do not create new bot projects until existing runtime is inspected.
