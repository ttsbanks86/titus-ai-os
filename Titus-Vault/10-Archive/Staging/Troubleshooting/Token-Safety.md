# Token Safety

Rules:

- Do not print secrets in final reports.
- If a secret/token was pasted in chat, mark it exposed.
- Use pasted secrets only for temporary diagnosis if necessary.
- Rotate before production use.
- Never commit secrets to repo.
- Prefer `.env` files, Windows Credential Manager, or provider dashboards for secret storage.

Approval required before deploying any service with a token.
