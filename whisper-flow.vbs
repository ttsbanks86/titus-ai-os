' Whisper Flow v2.0 — Desktop Toggle
' Double-click to start engine. Double-click again to stop.
' Right-click -> Open with Notepad to edit the hotkey in config.

Dim shell, fso, pidFile, running, cmd, configFile

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
pidFile = shell.ExpandEnvironmentStrings("%USERPROFILE%") & "\.whisper-flow\whisper-flow.pid"
configFile = shell.ExpandEnvironmentStrings("%USERPROFILE%") & "\.whisper-flow\config.json"

' Read hotkey from config for display
hotkey = "Ctrl+Shift+Space"
If fso.FileExists(configFile) Then
    On Error Resume Next
    configText = fso.OpenTextFile(configFile).ReadAll()
    hotkeyMatch = InStr(configText, """hotkey""")
    If hotkeyMatch > 0 Then
        quote1 = InStr(hotkeyMatch + 10, configText, """")
        If quote1 > 0 Then
            quote2 = InStr(quote1 + 1, configText, """")
            If quote2 > 0 Then
                hotkey = Mid(configText, quote1 + 1, quote2 - quote1 - 1)
            End If
        End If
    End If
    On Error GoTo 0
End If

' Check if already running
running = False
If fso.FileExists(pidFile) Then
    Dim pidText, pid
    pidText = Trim(fso.OpenTextFile(pidFile).ReadAll())
    If IsNumeric(pidText) Then
        pid = CInt(pidText)
        Dim processes
        Set processes = GetObject("winmgmts:\\.\root\cimv2").ExecQuery( _
            "SELECT * FROM Win32_Process WHERE ProcessId=" & pid)
        If processes.Count > 0 Then running = True
    End If
End If

If running Then
    ' Stop
    cmd = "powershell -NoProfile -ExecutionPolicy Bypass -File """ & _
          "C:\Users\tbank\Desktop\Live Cowork\whisper-flow.ps1"" stop"
    shell.Run cmd, 0, True
    shell.Popup "Whisper Flow stopped.", 2, "Whisper Flow", 64
Else
    ' Start
    cmd = "powershell -NoProfile -ExecutionPolicy Bypass -File """ & _
          "C:\Users\tbank\Desktop\Live Cowork\whisper-flow.ps1"" start"
    shell.Run cmd, 0, True
    shell.Popup "Whisper Flow started." & vbCrLf & _
                "Press " & hotkey & " to record." & vbCrLf & _
                "Press again to transcribe and paste.", 3, "Whisper Flow", 64
End If
