# Jarvis Daily Briefing Automation
# Run with: powershell -ExecutionPolicy Bypass -File Run-DailyBriefing.ps1 -Type [morning|midday|evening]
param(
    [ValidateSet("morning","midday","evening")]
    [string]$Type = "morning"
)

$jarvisRoot = "C:\Users\tbank\Desktop\Live Cowork\JARVIS_REBUILD"
$logFile = "$jarvisRoot\app\logs\briefing_$(Get-Date -Format 'yyyy-MM-dd').log"

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logFile -Value "[$timestamp] Starting $Type briefing"

try {
    cd $jarvisRoot
    $output = python -c @"
from app.config import load_config
from app.tools.briefing_exec import generate_morning_briefing, generate_midday_check, generate_evening_review, spoken_briefing_summary, write_briefing_to_obsidian

config = load_config()
btype = '$Type'

if btype == 'morning':
    content = generate_morning_briefing(config)
elif btype == 'midday':
    content = generate_midday_check(config)
else:
    content = generate_evening_review(config)

result = write_briefing_to_obsidian(config, btype, content)
print(result)
"@
    Add-Content -Path $logFile -Value "[$timestamp] Output: $output"
    Add-Content -Path $logFile -Value "[$timestamp] $Type briefing completed successfully"
} catch {
    Add-Content -Path $logFile -Value "[$timestamp] ERROR: $_"
}

exit 0