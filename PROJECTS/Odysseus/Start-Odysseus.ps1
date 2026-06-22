<#
.SYNOPSIS
  Start Odysseus local AI workspace.
#>
$repo = "C:\Users\tbank\Desktop\Live Cowork\PROJECTS\Odysseus\odysseus"
Set-Location -LiteralPath $repo
docker compose up -d
Start-Sleep -Seconds 3
Start-Process "http://127.0.0.1:7000"
Write-Host "Odysseus opened at http://127.0.0.1:7000"
Write-Host "To retrieve the temporary admin password, run:"
Write-Host "docker compose logs odysseus --tail 80"
