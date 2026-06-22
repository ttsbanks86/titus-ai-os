<#
.SYNOPSIS
  Whisper Flow v2.0 — Start/Stop/Configure local voice-to-text
.DESCRIPTION
  Launches Whisper Flow engine or settings panel.
  Now with device selection and hard-key support.
.EXAMPLE
  .\whisper-flow.ps1 start           # Start engine (Ctrl+Shift+Space)
  .\whisper-flow.ps1 settings        # Open settings panel in browser
  .\whisper-flow.ps1 devices         # List all microphones/speakers
  .\whisper-flow.ps1 stop            # Stop engine
  .\whisper-flow.ps1 status          # Check if running
#>

param(
    [ValidateSet("start", "stop", "toggle", "status", "settings", "devices", "restart")]
    [string]$Command = "start"
)

$scriptPath = "C:\Users\tbank\Desktop\Live Cowork\whisper-flow.py"
$workDir = "C:\Users\tbank\Desktop\Live Cowork"
$pidFile = "$HOME\.whisper-flow\whisper-flow.pid"
$null = New-Item -ItemType Directory -Path "$HOME\.whisper-flow" -Force

function Test-WhisperFlowRunning {
    if (-not (Test-Path $pidFile)) { return $false }
    $wfPid = Get-Content $pidFile -ErrorAction SilentlyContinue
    if (-not $wfPid) { return $false }
    try {
        $proc = Get-Process -Id $wfPid -ErrorAction Stop
        return (-not $proc.HasExited)
    } catch {
        Remove-Item $pidFile -ErrorAction SilentlyContinue
        return $false
    }
}

function Start-WhisperFlow {
    if (Test-WhisperFlowRunning) {
        Write-Host "  [WHISPER] Already running. Use 'restart' or 'stop' first."
        return
    }

    Write-Host "  [WHISPER] Starting Whisper Flow engine..."

    $process = Start-Process -FilePath "python" `
        -ArgumentList "-u", "`"$scriptPath`"" `
        -WorkingDirectory $workDir `
        -WindowStyle Hidden -PassThru

    if ($process -and (-not $process.HasExited)) {
        $process.Id | Out-File -FilePath $pidFile -Encoding ascii
        Write-Host "  [WHISPER] Running (PID: $($process.Id))"
        Write-Host "  [WHISPER] Hotkey: $(Get-HotkeyFromConfig)"
        Write-Host "  [WHISPER] Press hotkey to record, again to transcribe"
        Write-Host "  [WHISPER] Use '.\whisper-flow.ps1 stop' to quit"
        Write-Host "  [WHISPER] Use '.\whisper-flow.ps1 settings' to configure"
    } else {
        Write-Host "  [WHISPER] FAILED to start"
    }
}

function Stop-WhisperFlow {
    if (-not (Test-Path $pidFile)) {
        Write-Host "  [WHISPER] Not running"
        return
    }
    $wfPid = Get-Content $pidFile -ErrorAction SilentlyContinue
    if ($wfPid) {
        try {
            $proc = Get-Process -Id $wfPid -ErrorAction Stop
            $proc.Kill()
            Wait-Process -Id $wfPid -Timeout 3 -ErrorAction SilentlyContinue
            Write-Host "  [WHISPER] Stopped (PID: $wfPid)"
        } catch {
            Write-Host "  [WHISPER] Already stopped"
        }
    }
    Remove-Item $pidFile -ErrorAction SilentlyContinue
}

function Start-Settings {
    Write-Host "  [WHISPER] Opening settings panel..."
    $process = Start-Process -FilePath "python" `
        -ArgumentList "-u", "`"$scriptPath`"", "--settings" `
        -WorkingDirectory $workDir `
        -WindowStyle Normal -PassThru
    Write-Host "  [WHISPER] Settings panel should open in your browser."
    Write-Host "  [WHISPER] Close the browser tab when done."
}

function Get-HotkeyFromConfig {
    $cfgPath = "$HOME\.whisper-flow\config.json"
    if (Test-Path $cfgPath) {
        $cfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
        return $cfg.hotkey
    }
    return "ctrl+shift+space"
}

function Get-WhisperFlowStatus {
    if (Test-WhisperFlowRunning) {
        $wfPid = Get-Content $pidFile
        Write-Host "  [WHISPER] Status: RUNNING (PID: $wfPid)"
        Write-Host "  [WHISPER] Hotkey: $(Get-HotkeyFromConfig)"
    } else {
        Write-Host "  [WHISPER] Status: STOPPED"
    }
}

switch ($Command) {
    "start" { Start-WhisperFlow }
    "stop" { Stop-WhisperFlow }
    "toggle" {
        if (Test-WhisperFlowRunning) { Stop-WhisperFlow }
        else { Start-WhisperFlow }
    }
    "status" { Get-WhisperFlowStatus }
    "settings" { Start-Settings }
    "devices" {
        & python "$scriptPath" --list-devices
    }
    "restart" {
        Stop-WhisperFlow
        Start-Sleep -Seconds 2
        Start-WhisperFlow
    }
}
