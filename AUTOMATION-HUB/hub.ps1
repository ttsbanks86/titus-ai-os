# Titus Banks Automation Hub
# Central orchestrator for all scheduled automation
# Replaces n8n with reliable PowerShell + Task Scheduler

param([string]$Command = "status")

$HubRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptsDir = Join-Path $HubRoot "scripts"
$LogsDir = Join-Path $HubRoot "logs"
$ReportsDir = Join-Path $HubRoot "reports"
$ConfigPath = Join-Path $HubRoot "hub-config.json"
$LogPath = Join-Path $LogsDir ("hub-" + (Get-Date -Format "yyyyMMdd") + ".log")
$env:COMPOSIO_API_KEY = "ak_jxmgwQdWvPVWBxDK3m8W"

function Write-HubLog {
    param([string]$Message)
    $line = "[{0:HH:mm:ss}] {1}" -f (Get-Date), $Message
    Add-Content -LiteralPath $LogPath -Value $line
    Write-Output $line
}

function Get-Composio {
    param([string]$Endpoint, [string]$Method = "GET", [string]$Body = "")
    $headers = @{
        "x-api-key" = $env:COMPOSIO_API_KEY
        "Content-Type" = "application/json"
    }
    $url = "https://backend.composio.dev/api/v1$Endpoint"
    try {
        if ($Method -eq "GET") {
            $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get -TimeoutSec 15
        } else {
            $response = Invoke-RestMethod -Uri $url -Headers $headers -Method Post -Body $Body -TimeoutSec 15
        }
        return $response
    } catch {
        Write-HubLog "Composio API error ($Endpoint): $($_.Exception.Message)"
        return $null
    }
}

function Get-TrackerFile {
    $tracker = "C:\Users\tbank\Desktop\Live Cowork\JOB-TRACKER.md"
    if (Test-Path $tracker) {
        return Get-Content $tracker -Raw
    }
    return "Job tracker not found"
}

function Send-BriefingEmail {
    param([string]$Subject, [string]$Body)
    Write-HubLog "Briefing ready: $Subject"
    Write-HubLog "---"
    Write-HubLog $Body
    Write-HubLog "---"
    # Save to reports folder for review
    $reportPath = Join-Path $ReportsDir ("briefing-" + (Get-Date -Format "yyyyMMdd") + ".txt")
    $Body | Out-File -FilePath $reportPath -Encoding UTF8
    Write-HubLog "Briefing saved to: $reportPath"
}

function Show-Status {
    Write-HubLog "=== AUTOMATION HUB STATUS ==="
    Write-HubLog "Hub root: $HubRoot"
    Write-HubLog "Scripts: $(Get-ChildItem $ScriptsDir -Filter '*.ps1' | Select-Object -ExpandProperty Name)"
    Write-HubLog "Composio API Key: Configured"
    Write-HubLog "================================"
}

# Execute based on command
switch ($Command.ToLowerInvariant()) {
    "status" { Show-Status }
    "briefing" {
        & (Join-Path $ScriptsDir "morning-briefing.ps1")
    }
    "tracker" {
        & (Join-Path $ScriptsDir "update-tracker.ps1")
    }
    "check-messages" {
        & (Join-Path $ScriptsDir "check-messages.ps1")
    }
    "daily" {
        Write-HubLog "=== DAILY AUTOMATION RUN ==="
        & (Join-Path $ScriptsDir "check-messages.ps1")
        & (Join-Path $ScriptsDir "morning-briefing.ps1")
        Write-HubLog "=== DAILY RUN COMPLETE ==="
    }
    "intel" {
        Write-HubLog "=== INTELLIGENCE ENGINE ==="
        & "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\master-intel.ps1"
    }
    "goldmine" {
        Write-HubLog "=== GOLDMINE CRAWL ==="
        & "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\goldmine\goldmine.ps1"
    }
    "full-intel" {
        Write-HubLog "=== FULL INTELLIGENCE RUN ==="
        & "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\master-intel.ps1"
        & "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\goldmine\goldmine.ps1"
        & (Join-Path $ScriptsDir "update-tracker.ps1")
        Write-HubLog "=== FULL RUN COMPLETE ==="
    }
    default {
        Write-HubLog "Unknown command: $Command"
        Write-HubLog "Available: status, briefing, tracker, check-messages, daily, intel, goldmine, full-intel"
    }
}