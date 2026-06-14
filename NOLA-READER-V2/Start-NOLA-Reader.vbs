' NOLA Reader v2 — Silent Launcher (no console window)
' Uses Python directly (pre-built EXE not required)

Dim shell, pythonExe, scriptPath
Set shell = CreateObject("WScript.Shell")

' Find Python
pythonExe = "C:\Python313\python.exe"
If Not shell.FileExists(pythonExe) Then
    pythonExe = "python"
End If

scriptPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\nola_reader_v2.py"

' Launch without console window
shell.Run """" & pythonExe & """ """ & scriptPath & """", 0, False
Set shell = Nothing
