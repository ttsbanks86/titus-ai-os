' WhatsApp Bot Toggle — Desktop Launcher
' Toggles WhatsApp channel on/off via OpenClaw CLI

Dim shell, fso, openclawExe, output, currentStatus
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Find openclaw executable
pythonExe = "C:\Python313\python.exe"
If Not fso.FileExists(pythonExe) Then pythonExe = "python"
openclawExe = fso.GetParentFolderName(fso.GetParentFolderName(pythonExe)) & "\Scripts\openclaw.exe"
If Not fso.FileExists(openclawExe) Then openclawExe = "openclaw"

' Get current WhatsApp status
Set exec = shell.Exec(openclawExe & " channels status")
output = exec.StdOut.ReadAll()

' Parse WhatsApp status
currentStatus = "unknown"
If InStr(output, "WhatsApp default") > 0 Then
    If InStr(output, "health:healthy") > 0 Or InStr(output, "running, connected") > 0 Then
        currentStatus = "on"
    ElseIf InStr(output, "health:stopped") > 0 Or InStr(output, "disabled") > 0 Or InStr(output, "stopped") > 0 Then
        currentStatus = "off"
    End If
End If

' Toggle based on current status
If currentStatus = "on" Then
    ' Turn OFF
    shell.Run "cmd /c echo Yes | " & openclawExe & " channels remove --channel whatsapp --account default", 0, True
    result = "WhatsApp Bot: OFF"
Else
    ' Turn ON
    shell.Run openclawExe & " channels add --channel whatsapp --account default", 0, True
    result = "WhatsApp Bot: ON"
End If

' Show notification
shell.Popup result, 3, "WhatsApp Bot Toggle", 64

Set shell = Nothing
Set fso = Nothing