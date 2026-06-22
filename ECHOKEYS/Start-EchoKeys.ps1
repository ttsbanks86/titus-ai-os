# EchoKeys Launcher
# Launches the EchoKeys floating desktop transcription app

$EchoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $EchoDir "echokeys.py"
$LogFile = Join-Path $EchoDir "echokeys.log"

# Check if already running
$existing = Get-Process -Name "python*" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "echokeys" }
if ($existing) {
    Write-Output "EchoKeys is already running (PID: $($existing.Id))"
    exit
}

# Launch
try {
    $proc = Start-Process -FilePath "python" -ArgumentList $PythonScript -WindowStyle Normal -PassThru
    Start-Sleep -Seconds 2
    if (!$proc.HasExited) {
        Write-Output "EchoKeys launched (PID: $($proc.Id))"
        "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - Started PID $($proc.Id)" | Out-File $LogFile -Append
    }
} catch {
    Write-Output "Failed to start EchoKeys: $($_.Exception.Message)"
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - FAILED: $($_)" | Out-File $LogFile -Append
}