$ErrorActionPreference = 'Stop'

$vault = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$items = @(
    @{s='03-Businesses/Businesses.md';d='Archive/Superseded/Businesses.md';o='Titus';dm='Archive';st='Archived';p='Low';pr='';a='Business';h='[[Business Dashboard]]';t='archive,business'},
    @{s='03-Businesses/Business-Ideas.md';d='Business/Research/Business-Ideas.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='AI Small Business Initiative';a='Business Research';h='[[AI Small Business Solutions]]';t='business,research'},
    @{s='03-Businesses/CareNotes-Pro.md';d='Business/Inactive/CareNotes-Pro.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='CareNotes Pro';a='Product Research';h='[[AI Small Business Solutions]]';t='business,inactive'},
    @{s='03-Businesses/Legacy-Businesses.md';d='Archive/Business/Legacy-Businesses.md';o='Titus';dm='Archive';st='Archived';p='Low';pr='';a='Business History';h='[[Archive Index]]';t='archive,business'},
    @{s='04-Products/Content-Income-System.md';d='Business/Inactive/Content-Income-System.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='Content Income System';a='Product Research';h='[[AI Small Business Solutions]]';t='business,inactive'},
    @{s='04-Products/DocFlow.md';d='Business/Inactive/DocFlow.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='DocFlow';a='Product Research';h='[[AI Small Business Solutions]]';t='business,inactive'},
    @{s='04-Products/EchoKeys.md';d='Business/Inactive/EchoKeys.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='EchoKeys';a='Product Research';h='[[AI Small Business Solutions]]';t='business,inactive'},
    @{s='04-Products/Floating-AI-Tutor.md';d='Business/Inactive/Floating-AI-Tutor.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='Floating AI Tutor';a='Product Research';h='[[AI Small Business Solutions]]';t='business,inactive'},
    @{s='04-Products/Hermes-Gateway.md';d='JARVIS/Infrastructure/Hermes-Gateway.md';o='Titus';dm='JARVIS';st='Active';p='Medium';pr='JARVIS';a='AI Infrastructure';h='[[JARVIS Hub]]';t='jarvis,infrastructure'},
    @{s='04-Products/NOLA-Voice.md';d='Business/Inactive/NOLA-Voice.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='NOLA Voice';a='Product Research';h='[[AI Small Business Solutions]]';t='business,inactive'},
    @{s='04-Products/Personal-AI-Operator.md';d='JARVIS/Architecture/Personal-AI-Operator.md';o='Titus';dm='JARVIS';st='Active';p='Medium';pr='JARVIS';a='Architecture';h='[[JARVIS Hub]]';t='jarvis,architecture'},
    @{s='04-Products/Products.md';d='Review/Migration Review/Products.md';o='Titus';dm='Review';st='Review Required';p='Medium';pr='TKOS';a='Migration Review';h='[[Review Queue]]';t='review,migration'},
    @{s='04-Products/Whisper-Pro.md';d='Business/Inactive/Whisper-Pro.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='Whisper Pro';a='Product Research';h='[[AI Small Business Solutions]]';t='business,inactive'},
    @{s='05-Career/Business-Analyst-Path.md';d='Titus/Career/Business-Analyst-Path.md';o='Titus';dm='Titus';st='Prioritizing';p='High';pr='Business Analyst Career';a='Career';h='[[Career Command Center]]';t='career,business-analysis'},
    @{s='05-Career/Career.md';d='Titus/Career/Career.md';o='Titus';dm='Titus';st='Active';p='High';pr='Career Development';a='Career';h='[[Career Command Center]]';t='career'},
    @{s='05-Career/Certifications.md';d='Titus/Education/Certifications.md';o='Titus';dm='Titus';st='Prioritizing';p='High';pr='ISC2';a='Certifications';h='[[Education Dashboard]]';t='education,certifications'},
    @{s='05-Career/Education.md';d='Titus/Education/Education.md';o='Titus';dm='Titus';st='Active';p='High';pr='Master of Divinity';a='Education';h='[[Education Dashboard]]';t='education'},
    @{s='05-Career/Job-Search.md';d='Titus/Career/Job-Search.md';o='Titus';dm='Titus';st='Prioritizing';p='High';pr='Job Search';a='Career';h='[[Job Search Dashboard]]';t='career,job-search'},
    @{s='05-Career/LinkedIn-Strategy.md';d='Titus/Career/LinkedIn-Strategy.md';o='Titus';dm='Titus';st='Active';p='High';pr='Job Search';a='Career';h='[[Job Search Dashboard]]';t='career,linkedin'},
    @{s='05-Career/Portfolio.md';d='Titus/Career/Portfolio.md';o='Titus';dm='Titus';st='Active';p='High';pr='Professional Portfolio';a='Career';h='[[Career Command Center]]';t='career,portfolio'},
    @{s='05-Career/Resume.md';d='Titus/Career/Resume.md';o='Titus';dm='Titus';st='Active';p='High';pr='Resume';a='Career';h='[[Job Search Dashboard]]';t='career,resume'},
    @{s='06-Projects/AeroCardia.md';d='Titus/Career/Portfolio/AeroCardia.md';o='Titus';dm='Titus';st='Active';p='Medium';pr='Professional Portfolio';a='Career Portfolio';h='[[Career Command Center]]';t='career,portfolio'},
    @{s='06-Projects/Bonolo-Book-Marketing.md';d='Bonolo/Projects/Bonolo-Book-Marketing.md';o='Bonolo';dm='Bonolo';st='Active';p='Medium';pr='Bonolo Book Marketing';a='Book Marketing';h='[[Bonolo Living Profile]]';t='bonolo,books'},
    @{s='06-Projects/Local-Business-AI-Services.md';d='Business/Research/Local-Business-AI-Services.md';o='Titus';dm='Business';st='Inactive';p='Low';pr='AI Small Business Initiative';a='Business Research';h='[[AI Small Business Solutions]]';t='business,research'},
    @{s='06-Projects/Ministry-Return.md';d='Titus/Projects/Ministry-Return.md';o='Titus';dm='Titus';st='Planned';p='Low';pr='Ministry Return';a='Ministry';h='[[Project Registry]]';t='titus,ministry'},
    @{s='06-Projects/PM-Portfolio.md';d='Titus/Career/Portfolio/PM-Portfolio.md';o='Titus';dm='Titus';st='Active';p='High';pr='Professional Portfolio';a='Career Portfolio';h='[[Career Command Center]]';t='career,portfolio'},
    @{s='06-Projects/Projects.md';d='Review/Migration Review/Projects.md';o='Titus';dm='Review';st='Review Required';p='Medium';pr='TKOS';a='Migration Review';h='[[Review Queue]]';t='review,migration'},
    @{s='08-Agents/Agents-Index.md';d='JARVIS/Agents/Agents-Index.md';o='Titus';dm='JARVIS';st='Active';p='Medium';pr='JARVIS';a='Agents';h='[[JARVIS Hub]]';t='jarvis,agents'},
    @{s='08-Agents/Hermes-Agent.md';d='JARVIS/Agents/Hermes-Agent.md';o='Titus';dm='JARVIS';st='Active';p='Medium';pr='JARVIS';a='Agents';h='[[JARVIS Hub]]';t='jarvis,agents'}
)

$replacements = @()
foreach ($item in $items) {
    $source = Join-Path $vault $item.s
    $dest = Join-Path $vault $item.d
    if (Test-Path -LiteralPath $source) {
        New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
        Move-Item -LiteralPath $source -Destination $dest
        $oldTarget = [IO.Path]::ChangeExtension($item.s, $null).Replace('\\','/')
        $newTarget = [IO.Path]::ChangeExtension($item.d, $null).Replace('\\','/')
        $replacements += [pscustomobject]@{Old=$oldTarget;New=$newTarget}
    }
    if (-not (Test-Path -LiteralPath $dest)) { throw "Destination missing: $($item.d)" }
    $body = [IO.File]::ReadAllText($dest)
    if (-not $body.StartsWith('---')) {
        $tagLines = ($item.t -split ',' | ForEach-Object { "  - $_" }) -join "`n"
        $yaml = @"
---
owner: $($item.o)
domain: $($item.dm)
status: $($item.st)
priority: $($item.p)
project: $($item.pr)
area: $($item.a)
created:
updated: 2026-07-12
reviewed: 2026-07-12
related:
  - "$($item.h)"
tags:
$tagLines
---

"@
        $body = $yaml + $body
    }
    if ($body -notmatch '(?m)^## TKOS Connections$') {
        $body = $body.TrimEnd() + "`n`n## TKOS Connections`n`n- $($item.h)`n"
    }
    [IO.File]::WriteAllText($dest, $body, [Text.UTF8Encoding]::new($false))
}

if ($replacements.Count -gt 0) {
    Get-ChildItem -LiteralPath $vault -Recurse -File -Filter '*.md' | ForEach-Object {
        $linkText = [IO.File]::ReadAllText($_.FullName)
        $updated = $linkText
        foreach ($replacement in $replacements) { $updated = $updated.Replace($replacement.Old, $replacement.New) }
        if ($updated -ne $linkText) { [IO.File]::WriteAllText($_.FullName, $updated, [Text.UTF8Encoding]::new($false)) }
    }
}

[pscustomobject]@{Batch='002';Processed=$items.Count;Completed=(Get-Date -Format o)} |
    ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $vault 'Governance/batch-002-result.json')
