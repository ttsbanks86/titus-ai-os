# ═══════════════════════════════════════════════════════════════
# AUTOMATION HUB — TASK REGISTRATION
# Registers all schedules with Windows Task Scheduler
# Run this once to install all automated tasks
# ═══════════════════════════════════════════════════════════════

$HubRoot = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB"
$HubScript = Join-Path $HubRoot "hub.ps1"
$LogDir = Join-Path $HubRoot "logs"
$TaskUser = $env:USERNAME

function Register-HubTask {
    param(
        [string]$Name,
        [string]$Command,
        [string]$Schedule,
        [string]$Description
    )

    $taskPath = "Titus Automation Hub\$Name"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoLogo -NoProfile -ExecutionPolicy Bypass -File `"$HubScript`" -Command $Command"
    $trigger = New-ScheduledTaskTrigger $Schedule

    # Delete existing task if present
    Unregister-ScheduledTask -TaskPath "Titus Automation Hub\" -TaskName $Name -Confirm:$false -ErrorAction SilentlyContinue

    Register-ScheduledTask -TaskName $Name -TaskPath "Titus Automation Hub\" -Action $action -Trigger $trigger -Description $Description -User $TaskUser -RunLevel Limited -Force

    Write-Output "[$Name] Registered — $Description"
}

try {
    Write-Output "═══ REGISTERING AUTOMATION HUB TASKS ═══"
    Write-Output ""

    # Create task directory
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

    # 1. MORNING BRIEFING — Weekdays at 8:00 AM
    Register-HubTask -Name "Morning Briefing" -Command "daily" `
        -Schedule @{Daily="$true"; At="8:00AM"} `
        -Description "Generates daily job search briefing and checks messages"

    # 2. MESSAGE CHECK — Every 4 hours (9AM, 1PM, 5PM)
    Register-HubTask -Name "Message Check" -Command "check-messages" `
        -Schedule @{Daily="$true"; At="9:00AM"; RepetitionInterval=[TimeSpan]::FromHours(4)} `
        -Description "Checks for new recruiter messages across platforms"

    # 3. TRACKER UPDATE — Daily at 6:00 PM
    Register-HubTask -Name "Tracker Update" -Command "tracker" `
        -Schedule @{Daily="$true"; At="6:00PM"} `
        -Description "Updates job tracker with latest application status"

    # 4. HOURLY TOUCH — Check if hub is alive (every hour 7AM-7PM)
    Register-HubTask -Name "Hourly Touch" -Command "status" `
        -Schedule @{Daily="$true"; At="7:00AM"; RepetitionInterval=[TimeSpan]::FromHours(1); RepetitionDuration=[TimeSpan]::FromHours(12)} `
        -Description "Verify automation hub is running correctly"

    Write-Output ""
    Write-Output "═══ ALL TASKS REGISTERED SUCCESSFULLY ═══"
    Write-Output ""
    Write-Output "View them in Task Scheduler under: Titus Automation Hub"
    Write-Output ""

} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
}