<#
.SYNOPSIS
    Start the full Titus AI OS: dashboard (API + frontend) and OpenCode with
    Titus integration (theme, plugins, resume). One command, idempotent.

.DESCRIPTION
    Stage 0: Pre-flight checks (python, opencode, vault paths)
    Stage 1: Knowledge engine presence check
    Stage 2: Dashboard start (idempotent - skips if ports already listening)
    Stage 3: Resume context preparation (reads vault records)
    Stage 4: Launch OpenCode in the Live Cowork workspace
    Stage 5: Post-launch verification hints

.EXAMPLE
    .\bin\Start-TitusAIOS.ps1
    .\bin\Start-TitusAIOS.ps1 -NoOpenCode   # dashboard only
    .\bin\Start-TitusAIOS.ps1 -NoDashboard  # opencode only

.NOTES
    Part of M4 (Hybrid OpenCode Integration and Unified Startup).
    Fails soft: dashboard problems never block OpenCode and vice versa.
#>

[CmdletBinding()]
param(
    [switch]$NoOpenCode,
    [switch]$NoDashboard
)

$ErrorActionPreference = "Continue"

# ---------------------------------------------------------------- paths
$Root          = Split-Path -Parent $PSScriptRoot          # Live Cowork
$VaultRoot     = Join-Path $Root "Titus-Vault"
$DashboardDir  = Join-Path $VaultRoot "titus-ai-os-dashboard"
$ApiDir        = Join-Path $DashboardDir "api"
$FrontendDir   = Join-Path $DashboardDir "frontend"
$ProjectDir    = Join-Path $VaultRoot "06-Projects\Titus-AI-OS-Upgrade"
$LogDir        = Join-Path $DashboardDir "logs"
$OpencodeCwd   = $Root

function Write-Step([string]$msg) {
    Write-Host ""
    Write-Host "== $msg" -ForegroundColor Cyan
}

function Test-PortListening([int]$port) {
    try {
        $conn = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction Stop
        return $null -ne $conn
    } catch {
        return $false
    }
}

function Wait-Health([string]$url, [int]$maxSeconds = 15) {
    for ($i = 0; $i -lt $maxSeconds; $i++) {
        try {
            $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
            if ($r.StatusCode -eq 200) { return $true }
        } catch { Start-Sleep -Seconds 1 }
    }
    return $false
}

# ---------------------------------------------------------------- stage 0
Write-Host "TITUS AI OS - unified startup" -ForegroundColor White
Write-Host "Vault: $VaultRoot" -ForegroundColor DarkGray
Write-Host "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor DarkGray

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { Write-Host "WARN: python not found - dashboard will be skipped." -ForegroundColor Yellow }
$opencode = Get-Command opencode -ErrorAction SilentlyContinue
if (-not $opencode) { Write-Host "WARN: opencode not found on PATH." -ForegroundColor Yellow }
if (-not (Test-Path $VaultRoot)) { Write-Host "ERROR: vault not found at $VaultRoot - aborting." -ForegroundColor Red; exit 1 }

# ---------------------------------------------------------------- stage 1
if (-not $NoDashboard) {
    Write-Step "Stage 1 - Knowledge engine check"
    if (Test-Path (Join-Path $VaultRoot "knowledge_engine")) {
        Write-Host "OK: knowledge_engine present (index builds on demand)." -ForegroundColor Green
    } else {
        Write-Host "WARN: knowledge_engine missing." -ForegroundColor Yellow
    }
}

# ---------------------------------------------------------------- stage 2
if (-not $NoDashboard) {
    Write-Step "Stage 2 - Dashboard (idempotent)"

    if ($python) {
        $apiUp = Test-PortListening 8000
        if (-not $apiUp) {
            Write-Host "Starting API on :8000 ..."
            New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
            Start-Process python -ArgumentList "-m", "uvicorn", "api.main:app", "--host", "127.0.0.1", "--port", "8000" `
                -WorkingDirectory $DashboardDir -WindowStyle Minimized -RedirectStandardOutput (Join-Path $LogDir "api.out.log") `
                -RedirectStandardError (Join-Path $LogDir "api.err.log")
        } else {
            Write-Host "API already listening on :8000 - skip." -ForegroundColor Green
        }

        $webUp = Test-PortListening 3000
        if (-not $webUp) {
            Write-Host "Starting frontend on :3000 ..."
            Start-Process python -ArgumentList "-m", "http.server", "3000" `
                -WorkingDirectory $FrontendDir -WindowStyle Minimized -RedirectStandardOutput (Join-Path $LogDir "web.out.log") `
                -RedirectStandardError (Join-Path $LogDir "web.err.log")
        } else {
            Write-Host "Frontend already listening on :3000 - skip." -ForegroundColor Green
        }

        if (-not $apiUp) {
            $ok = Wait-Health "http://127.0.0.1:8000/api/health" 20
            if ($ok) { Write-Host "API health: OK" -ForegroundColor Green }
            else { Write-Host "WARN: API not healthy within 20s - see logs\api.err.log" -ForegroundColor Yellow }
        }
    } else {
        Write-Host "Skipping dashboard (python missing)." -ForegroundColor Yellow
    }
}

# ---------------------------------------------------------------- stage 3
Write-Step "Stage 3 - Resume context"
$statusFile = Join-Path $ProjectDir "PROJECT_STATUS.md"
$milestoneFile = Join-Path $ProjectDir "CURRENT_MILESTONE.md"
if (Test-Path $milestoneFile) {
    $milestoneLine = Get-Content $milestoneFile -TotalCount 5 -Encoding UTF8 | Where-Object { $_ -match "^# CURRENT" } | Select-Object -First 1
    $milestone = $milestoneLine -replace "^#\s*CURRENT_MILESTONE", ""
    $milestone = ($milestone.Trim() -replace "^[\s\-:\u2013\u2014]+", "").Trim()
    Write-Host "Active milestone: $milestone" -ForegroundColor Green
} elseif (Test-Path $statusFile) {
    Write-Host "Active milestone: (PROJECT_STATUS.md)" -ForegroundColor Green
} else {
    Write-Host "WARN: no milestone records - resume will be generic." -ForegroundColor Yellow
}

# ---------------------------------------------------------------- stage 4
if (-not $NoOpenCode) {
    Write-Step "Stage 4 - Launch OpenCode (Titus workspace)"
    if ($opencode) {
        Write-Host "Working dir: $OpencodeCwd" -ForegroundColor DarkGray
        Write-Host "OpenCode will load: Titus theme (tui.json), titus plugins (status/resume/health), vault MCP."
        Push-Location $OpencodeCwd
        try {
            & opencode
        } finally {
            Pop-Location
        }
    } else {
        Write-Host "WARN: opencode not found - skipped launch." -ForegroundColor Yellow
    }
}

# ---------------------------------------------------------------- stage 5
Write-Step "Stage 5 - Summary"
Write-Host "Dashboard:  http://localhost:3000" -ForegroundColor White
Write-Host "API docs:   http://localhost:8000/docs" -ForegroundColor White
if (-not $NoOpenCode) {
    Write-Host "In OpenCode: /titus-status command | titus_status / titus_resume / titus_health tools"
}
Write-Host "Done: $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor DarkGray
