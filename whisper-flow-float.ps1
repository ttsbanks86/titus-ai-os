<#
.SYNOPSIS
  Launch EchoKey.
.DESCRIPTION
  Starts the always-on-top EchoKey local dictation control panel.
#>

$scriptPath = "C:\Users\tbank\Desktop\Live Cowork\whisper-flow-float.py"
$workDir = "C:\Users\tbank\Desktop\Live Cowork"

Write-Host "Starting EchoKey..."
Start-Process -FilePath "python" `
  -ArgumentList "`"$scriptPath`"" `
  -WorkingDirectory $workDir `
  -WindowStyle Hidden
Write-Host "EchoKey launched. Look for the floating panel."
