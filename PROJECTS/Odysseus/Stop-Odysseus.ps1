<#
.SYNOPSIS
  Stop Odysseus local AI workspace.
#>
$repo = "C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\odysseus"
Set-Location -LiteralPath $repo
docker compose stop
Write-Host "Odysseus stopped."
