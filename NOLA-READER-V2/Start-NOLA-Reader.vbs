' NOLA Reader v2 — Silent Launcher (no console window)
' Uses Python directly (pre-built EXE not required)

Dim shell, fso, pythonExe, scriptPath
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Find Python (windowed version — no console)
pythonExe = "C:\Python313\pythonw.exe"
If Not fso.FileExists(pythonExe) Then
    pythonExe = "C:\Python313\python.exe"
End If
If Not fso.FileExists(pythonExe) Then
    pythonExe = "pythonw"
End If

scriptPath = fso.GetParentFolderName(WScript.ScriptFullName) & "\nola_reader_v2.py"

' Launch without console window
shell.Run """" & pythonExe & """ """ & scriptPath & """", 0, False
Set shell = Nothing
Set fso = Nothing
