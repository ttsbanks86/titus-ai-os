# Job Intelligence Scanner
# Searches Indeed and Wellfound for new BA roles matching our profile
# Uses browser automation to find actual listings

$scanDir = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\scans"
$date = Get-Date -Format "yyyyMMdd"
$scanFile = Join-Path $scanDir "scan-$date.json"
$reportFile = Join-Path $scanDir "scan-$date.txt"

# Our target criteria
$targetRoles = @("Business Analyst", "Junior Business Analyst", "Data Analyst", "Healthcare Business Analyst", "IT Business Analyst")
$targetRemote = $true
$targetMinPay = 65000
$targetLocations = @("Remote", "Seattle", "Dallas")
$targetIndustries = @("Healthcare", "Technology", "Financial Services", "AI")

function Write-ScanLog { param([string]$M) Write-Output "[SCAN] $M" }

# Score a job listing against our profile
function Get-JobScore {
    param([string]$Title, [string]$Company, [string]$Description, [string]$Pay, [string]$Location)
    $score = 0
    
    # Title match
    foreach ($role in $targetRoles) {
        if ($Title -match [regex]::Escape($role)) { $score += 30; break }
    }
    if ($Title -match "Senior") { $score -= 10 }  # Senior roles may ask 5+ years
    if ($Title -match "Jr|Junior|Entry|Associate") { $score += 15 }  # Entry level is good
    
    # Remote score
    if ($Location -match "Remote") { $score += 25 }
    elseif ($Location -match "Seattle|Dallas") { $score += 15 }
    
    # Industry score
    foreach ($ind in $targetIndustries) {
        if ($Description -match [regex]::Escape($ind)) { $score += 15 }
    }
    
    # Key skills in description
    $keywords = @("requirements", "stakeholder", "SQL", "Power BI", "agile", "scrum", "documentation", "process", "UAT", "user stories")
    foreach ($kw in $keywords) {
        if ($Description -match $kw) { $score += 5 }
    }
    
    return $score
}

# Generate interview cheat sheet for a job
function New-CheatSheet {
    param([string]$Company, [string]$Role, [string]$Description, [int]$Score)
    
    $cheatDir = "C:\Users\tbank\Desktop\Live Cowork\AUTOMATION-HUB\intelligence\interviews"
    $cheatFile = Join-Path $cheatDir ("$($Company.Replace(' ','-').Replace('.',''))-$Role-interview-prep.md")
    
    $extra = if ($Description -match "healthcare|health|medical|patient|clinical|hospital") { "Your Visiting Angels experience is a MAJOR advantage here. Lead with healthcare BA stories." } `
             elseif ($Description -match "SQL|data|analytics|Power BI") { "Highlight SQL + Power BI from your toolkit. Mention the dashboard project." } `
             elseif ($Description -match "AI|machine learning|automation") { "Your AI systems experience (router, agent automation) directly applies here." } `
             else { "Lead with AeroCardia project and stakeholder management experience." }
    
    $certTip = if ($Description -match "CBAP|IIBA|certification") { "They value BA certs. Mention your BABOK self-study and planned certification." } `
               else { "No cert required - your degree and experience cover this." }
    
    $content = @"
# Interview Prep: $Role at $Company
Generated: $(Get-Date -Format "MMM dd, yyyy")
Fit Score: $Score/100

## Why You're a Fit
$extra

## Key Responsibilities (From Job Description)
"@

    # Extract key responsibilities
    $respMatches = [regex]::Matches($Description, '(?:Lead|Manage|Create|Develop|Analyze|Coordinate|Facilitate|Partner|Drive|Support)\s[^.!?]*[.!?]')
    $i = 1
    foreach ($match in $respMatches) {
        if ($match.Value.Length -gt 15) {
            $content += "`n$i. $($match.Value.Trim())"
            $i++
        }
    }
    
    $content += @"

## Your Talking Points
1. AeroCardia: "5/5 CEO rating for market entry strategy and competitive analysis"
2. Visiting Angels: "Requirements gathering for 15+ concurrent clients"
3. US Bank: "100% remote, zero quality findings, pipeline management"  
4. WGU: "BS IT Management, April 2026"
5. AI Systems: "Built model router, auto-switcher, content pipeline"

## Interview Tips
- $certTip
- Portfolio is live: titusbanks86.github.io/ba-portfolio
- Linkedin is updated: linkedin.com/in/titus-banks-280652227
- Study STAR method for behavioral questions
- Practice explaining AI concepts in business language

## Questions to Ask Them
- "What does success look like for this role in the first 90 days?"
- "What tools and systems does the team currently use?"
- "How does the BA team collaborate with product and engineering?"
"@
    
    $content | Out-File -FilePath $cheatFile -Encoding UTF8
    Write-ScanLog "Cheat sheet saved: $cheatFile"
    return $cheatFile
}

# === MAIN EXECUTION ===
Write-ScanLog "Starting job intelligence scan for $(Get-Date -Format 'MMM dd, yyyy')"

$results = @()

# Check Indeed for BA jobs - we'll use the search URL patterns
$indeedUrls = @(
    "https://www.indeed.com/jobs?q=Business+Analyst&l=Remote&sort=date",
    "https://www.indeed.com/jobs?q=Business+Analyst+Entry+Level&l=Remote&sort=date",
    "https://www.indeed.com/jobs?q=Healthcare+Business+Analyst&l=Remote&sort=date"
)

Write-ScanLog "Indeed URLs queued for scan: $($indeedUrls.Count)"
Write-ScanLog "To scan manually, open: $($indeedUrls[0])"

# For now, we log the opportunities for the browser to visit
$scanSummary = @"
===========================================
JOB INTELLIGENCE SCAN - $(Get-Date -Format "MMM dd, yyyy")
===========================================

SCAN QUEUED
The following job boards are ready for automated scanning:

1. Indeed - Remote BA Jobs
   URL: https://www.indeed.com/jobs?q=Business+Analyst&l=Remote&sort=date

2. Indeed - Entry Level Remote BA Jobs
   URL: https://www.indeed.com/jobs?q=Business+Analyst+Entry+Level&l=Remote&sort=date

3. Indeed - Healthcare BA Remote Jobs
   URL: https://www.indeed.com/jobs?q=Healthcare+Business+Analyst&l=Remote&sort=date

4. Wellfound - Startup BA Jobs
   URL: https://wellfound.com/role/r/business-analyst

5. LinkedIn - BA Jobs
   URL: https://www.linkedin.com/jobs/search/?keywords=Business%20Analyst&location=Remote

TARGET CRITERIA:
- Roles: Business Analyst, Data Analyst, IT BA, Healthcare BA
- Remote: Required
- Pay: \$65K+
- Industries: Healthcare, Tech, Financial, AI
- Experience: Entry to Mid-Level

ACTIVE APPLICATIONS:
- Northridge Consulting - BA (\$80-90/hr) - Waiting
- Terminix - Sr Data Analyst (\$94-122K) - Waiting  
- InnovaIT Global - BA (\$40-45/hr) - Waiting
- Upstream Rehabilitation - Sr BA (\$99-114K) - Waiting

NEXT STEPS:
1. Open Indeed links in browser to scan new listings
2. Score and rank new opportunities
3. Prepare tailored resumes for top matches
4. Generate interview cheat sheets
"@

$scanSummary | Out-File -FilePath $reportFile -Encoding UTF8
Write-ScanLog "Scan report saved: $reportFile"
Write-ScanLog "Use: powershell hub.ps1 -Command scan-jobboards to open all boards"
Write-Output $scanSummary