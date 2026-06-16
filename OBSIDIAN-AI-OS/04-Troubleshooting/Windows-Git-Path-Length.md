# Windows Git Path Length

Problem: Deep repo clones can fail on Windows with filename/path too long.

Example:

- Antigravity awesome skills failed inside the nested learning capture folder.
- Successful clone exists at short path: `C:\Users\tbank\Desktop\ag-skills`.

Rule:

- Clone large repos into short paths first.
- Avoid deeply nested paths for external repos.
- Treat failed partial clone directories as untrusted until archived/deleted after approval.
