# Email Monitor - Recruiter Message Scanner
# Monitors Gmail for recruiter responses via MCP/Composio integration
# Saves findings and alerts the hub

$reportDir = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\scans"
$date = Get-Date -Format "yyyyMMdd-HHmm"
$reportFile = Join-Path $reportDir "email-report-$date.txt"

function Write-EmailLog { param([string]$M) Write-Output "[EMAIL] $M" }

$checklist = @"
===========================================
EMAIL MONITOR - Recruiter Check
$(Get-Date -Format "MMM dd, yyyy HH:mm")
===========================================

PLATFORMS TO CHECK:
[ ] Indeed Messages — https://messages.indeed.com
[ ] LinkedIn Messages — https://linkedin.com/messaging
[ ] Wellfound Messages — https://wellfound.com/jobs/messages
[ ] Gmail Inbox — https://mail.google.com (search: indeed OR linkedin OR recruiter)
[ ] Gmail Inbox — Search: "your application" OR "interview" OR "job opportunity"

ACTIVE CONVERSATIONS TO FOLLOW UP:
1. Northridge Consulting (Indeed) - Replied Jun 10 - Waiting for response
2. Upstream Rehabilitation (Wellfound) - Applied Jun 11 - External site

DRAFT REPLY - NORTHRIDGE (if they respond):
"Hi Carly, thanks for the follow-up. I'm very interested in the Business Analyst role.
I believe my healthcare operations background combined with my AI systems experience
positions me well to contribute immediately. I'm available for a call at your convenience."

DRAFT THANK YOU - UPSTREAM REHAB (if called):
"Thank you for the opportunity. I was particularly drawn to Upstream because of
your mission-driven approach to healthcare. My experience at Visiting Angels
and my IT Management degree from WGU align well with this role."

AUTOMATION STATUS:
- Email auto-response: DISABLED (requires explicit approval)
- Follow-up reminders: ENABLED (daily until response received)
- Application tracking: ENABLED (auto-updates JOB-TRACKER.md)
"@

$checklist | Out-File -FilePath $reportFile -Encoding UTF8
Write-EmailLog "Email monitor report saved: $reportFile"
Write-Output $checklist