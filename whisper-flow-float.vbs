' EchoKey — Silent Launcher
' Double-click to open the floating local dictation control panel.

Dim shell, cmd
Set shell = CreateObject("WScript.Shell")
cmd = "powershell -NoProfile -ExecutionPolicy Bypass -File ""C:\Users\tbank\Desktop\Live Cowork\whisper-flow-float.ps1"""
shell.Run cmd, 0, False
