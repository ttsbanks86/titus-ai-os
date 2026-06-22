# DocFlow Recursion

Problem: DocFlow crashed with `maximum recursion depth exceeded`.

Cause: UI class overrode `show()` and called `self.show()` from inside itself.

Fix:

- Replace recursive call with `super().show()`.
- Rebuild EXE.
- Update/verify desktop shortcut.

Relevant files:

- `C:\Users\tbank\Desktop\Live Cowork\DOCFLOW\docflow.py`
- `C:\Users\tbank\Desktop\Live Cowork\DOCFLOW\dist\DocFlow\DocFlow.exe`
- `C:\Users\tbank\Desktop\DocFlow.lnk`
