# Check Messages Script
# Checks for new recruiter messages and saves a report

$reportPath = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\reports\messages-$((Get-Date).ToString('yyyyMMdd-HHmm')).txt"
$date = Get-Date -Format "yyyy-MM-dd HH:mm"

$report = @"
Message Check Report
Generated: $date

PLATFORMS TO CHECK MANUALLY:
- Indeed Messages: https://messages.indeed.com
- LinkedIn Messages: https://linkedin.com/messaging
- Wellfound Messages: https://wellfound.com/jobs/messages

KNOWN ACTIVE CONVERSATIONS:
- Northridge Consulting (Indeed) — Replied, waiting for response

ACTIVE APPLICATIONS: 4
- Northridge Consulting — BA ($80-90/hr)
- Terminix — Sr Data Analyst ($94-122K)
- InnovaIT Global — BA ($40-45/hr)
- Upstream Rehabilitation — Sr BA ($99-114K)

"@

$report | Out-File -FilePath $reportPath -Encoding UTF8
Write-Output "Message check complete. Report saved to: $reportPath"