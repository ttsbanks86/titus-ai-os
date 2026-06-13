# Morning Briefing Script
# Generates a daily briefing with job search status and priorities

$date = Get-Date -Format "dddd, MMMM dd, yyyy"
$reportPath = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\reports\briefing-$((Get-Date).ToString('yyyyMMdd')).txt"

$briefing = @"
===========================================
  JOB SEARCH BRIEFING - $date
===========================================

RECRUITER MESSAGES: Check Indeed & LinkedIn
   - Northridge Consulting - BA (\$80-90/hr) - Waiting
   - Upstream Rehabilitation - Sr BA (\$99-114K) - Applied
   - Terminix - Sr Data Analyst (\$94-122K) - Applied
   - InnovaIT Global - BA (\$40-45/hr) - Applied

TODAY'S PRIORITIES:
  [ ] Check Indeed messages for replies
  [ ] Check LinkedIn messages/notifications
  [ ] Study 15 min from 30-day roadmap
  [ ] Check Wellfound for new BA listings
  [ ] Apply to 1-2 new BA roles

PORTFOLIO: titusbanks86.github.io/ba-portfolio
LINKEDIN: linkedin.com/in/titus-banks-280652227

Active Applications: 4
Platforms: LinkedIn [OK] | Indeed [OK] | Wellfound [OK] | Built In [OK]

Have a productive day.
"@

$briefing | Out-File -FilePath $reportPath -Encoding UTF8
Write-Output $briefing
Write-Output "Briefing saved to: $reportPath"