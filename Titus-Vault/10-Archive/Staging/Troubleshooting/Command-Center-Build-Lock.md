# Command Center Build Lock

Problem: Windows EXE rebuilds can fail if the target executable is still running.

Rule:

- Before PyInstaller rebuilds, check whether the app process is running.
- Stop the running EXE if needed.
- Rebuild.
- Verify the dist EXE and desktop shortcut target.

Current Command Center source:

- `C:\Users\tbank\Desktop\Live Cowork\BUSINESS-SUITE\analytics-dashboard\command_center.py`

Current Command Center EXE:

- `C:\Users\tbank\Desktop\Live Cowork\BUSINESS-SUITE\analytics-dashboard\dist\Command Center\Command Center.exe`
