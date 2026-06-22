<#
.SYNOPSIS
  Start Command Portal.
.DESCRIPTION
  Launches a chatbot-style local webpage for typing plain-English commands.
#>

$script = "C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Command Portal\command-portal.py"
$workdir = "C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Command Portal"
Start-Process -FilePath "python" -ArgumentList "`"$script`"" -WorkingDirectory $workdir -WindowStyle Hidden
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:8787"
