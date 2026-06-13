# Job Tracker Auto-Update Script
# Keeps JOB-TRACKER.md up to date with application status

$trackerPath = "C:\Users\tbank\Desktop\Live Cowork\JOB-TRACKER.md"
$date = Get-Date -Format "MMMM dd, yyyy"

$trackerContent = @"
# Job Application Tracker

**Last Updated:** $date

| # | Date | Company | Role | Pay | Platform | Status | Notes |
|---|------|---------|------|:---:|:--------:|:------:|-------|
| 1 | Jun 10 | Northridge Consulting, LLC | Business Analyst | \$80-90/hr | Indeed | ✅ Submitted + Replied | Carly Powell reached out. Replied with AeroCardia details. Waiting. |
| 2 | Jun 10 | Terminix | Sr Data Analyst, Marketing | \$94-122K | Indeed | ✅ Submitted | Remote in Memphis, TN. BA-tailored resume submitted. |
| 3 | Jun 10 | InnovaIT Global | Business Analyst | \$40-45/hr | Indeed | ✅ Submitted | Remote. Quick apply via Indeed. |
| 4 | Jun 11 | Upstream Rehabilitation | Sr Business Analyst | \$99-114K | Wellfound | ✅ Applied | Healthcare BA role. Remote. External apply started. |

---

## Active Conversations

### Indeed Messages
- **Northridge Consulting** (Jun 10) — Carly Powell reached out. Replied with detailed background.

### LinkedIn Messages
- (None yet)

---

## Platform Profiles

| Platform | Status | Link |
|----------|--------|------|
| LinkedIn | ✅ Updated | linkedin.com/in/titus-banks-280652227 |
| Indeed | ✅ Updated | profile.indeed.com |
| GitHub | ✅ Live | github.com/ttsbanks86/ba-portfolio |
| Wellfound | ✅ Profile Created | wellfound.com |
| Built In | ✅ Created | builtin.com |
| Bandana | ❌ Skipped | Limited platform |

---

## Interview Prep Notes

### Your 5 Key Talking Points
1. **AeroCardia** — "Competitive micro-internship, 5/5 CEO rating for market entry strategy"
2. **Visiting Angels** — "Requirements gathering for 15+ concurrent clients, cross-functional coordination"
3. **US Bank** — "100% remote, zero quality findings, pipeline management"
4. **WGU Degree** — "BS IT Management, April 2026"
5. **AI Systems** — "Built autonomous AI systems: model router, auto-switcher, content pipeline, PROMPT-MINE"

### Portfolio URL
**https://ttsbanks86.github.io/ba-portfolio**
"@

$trackerContent | Out-File -FilePath $trackerPath -Encoding UTF8
Write-Output "Job tracker updated: $trackerPath"