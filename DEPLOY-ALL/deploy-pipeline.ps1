<#
.SYNOPSIS
    Titus Banks Wired-Open Deployment Pipeline
.DESCRIPTION
    Packages the 4 landing pages (opendoor, ba-services, fjq, gap-audit) into a single
    Netlify-Drop-ready folder with a verification report. Run this from a PowerShell prompt.

    What it does:
    1. Verifies all 4 source folders exist with their index.html
    2. Builds a fresh NETLIFY-DROP/ folder with all sites
    3. Validates each HTML for brand compliance (em-dashes, banned words)
    4. Prints a deploy report with the drag-and-drop steps

    Total runtime: 30 seconds.

    After this runs, you have a single folder to drag into Netlify Drop.
    Netlify gives you 4 URLs in return.
#>

# Configuration
$ErrorActionPreference = "Stop"
$Root = "C:\Users\tbank\Desktop\Live Cowork"
$Source = Join-Path $Root "DEPLOY-ALL"
$OutDir = Join-Path $Root "NETLIFY-DROP"
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm"

# Brand rules
$emDashPattern = [char]0x2014
$BannedWords = @("elevate", "seamless", "unleash", "next-gen", "nextgen")

# 4 sites to deploy (source file/folder, output folder name, site title, final URL slug)
$Sites = @(
    @{ Source = "01-opendoor-ai-landing.html";        OutFolder = "opendoor";  Title = "Open Door AI Systems";              Slug = "opendoor" },
    @{ Source = "02-ba-services-landing.html";        OutFolder = "ba";        Title = "Business Analysis and Operations";  Slug = "ba" },
    @{ Source = "03-faithful-journey-quest-cover.html"; OutFolder = "fjq";     Title = "Faithful Journey Quest";            Slug = "fjq" },
    @{ Source = "gap-audit/index.html";               OutFolder = "audit";    Title = "Faith and Operations Gap Audit";    Slug = "audit" }
)

# 1. Wipe and recreate output folder
Write-Host ""
Write-Host "====== TITUS BANKS WIRED-OPEN DEPLOY PIPELINE ======" -ForegroundColor Cyan
Write-Host "Build timestamp: $Timestamp"
Write-Host ""

if (Test-Path -LiteralPath $OutDir) {
    Remove-Item -LiteralPath $OutDir -Recurse -Force
}
New-Item -ItemType Directory -Path $OutDir | Out-Null
Write-Host "[1/5] Created fresh NETLIFY-DROP/ folder" -ForegroundColor Green

# 2. Verify source sites exist
Write-Host ""
Write-Host "[2/5] Verifying source sites..." -ForegroundColor Green
$allFound = $true
foreach ($site in $Sites) {
    $srcPath = Join-Path $Source $site.Source
    if (Test-Path -LiteralPath $srcPath) {
        $size = (Get-Item $srcPath).Length
        Write-Host "  [OK] $($site.Source)  ($([math]::Round($size/1KB,1)) KB)"
    } else {
        Write-Host "  [MISSING] $($site.Source)" -ForegroundColor Red
        $allFound = $false
    }
}
if (-not $allFound) {
    Write-Host ""
    Write-Host "ABORT: One or more source sites are missing." -ForegroundColor Red
    Write-Host "Expected at: $Source"
    exit 1
}

# 3. Copy sites to output (each gets its own subfolder, with the source renamed to index.html)
Write-Host ""
Write-Host "[3/5] Copying sites to NETLIFY-DROP/..." -ForegroundColor Green
foreach ($site in $Sites) {
    $srcPath = Join-Path $Source $site.Source
    $destFolder = Join-Path $OutDir $site.OutFolder
    New-Item -ItemType Directory -Path $destFolder -Force | Out-Null

    # If the source is a file, copy it as index.html
    # If the source is a directory, copy all its contents
    if ((Get-Item $srcPath) -is [System.IO.FileInfo]) {
        $destFile = Join-Path $destFolder "index.html"
        Copy-Item -LiteralPath $srcPath -Destination $destFile -Force
    } else {
        Copy-Item -Path "$srcPath\*" -Destination $destFolder -Recurse -Force
    }

    $fileCount = (Get-ChildItem $destFolder -Recurse -File).Count
    Write-Host "  [COPIED] $($site.OutFolder)/  ($fileCount files)"
}

# 4. Brand compliance audit on the package
Write-Host ""
Write-Host "[4/5] Brand compliance audit..." -ForegroundColor Green
$emCount = 0
$bannedCount = 0
$emFiles = @()
$bannedFiles = @()
Get-ChildItem $OutDir -Recurse -File -Include "*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $emInFile = ([regex]::Matches($content, [regex]::Escape($emDashPattern))).Count
    if ($emInFile -gt 0) {
        $emCount += $emInFile
        $emFiles += "$($_.Name) ($emInFile)"
    }
    foreach ($b in $BannedWords) {
        $inFile = ([regex]::Matches($content, [regex]::Escape($b))).Count
        if ($inFile -gt 0) {
            $bannedCount += $inFile
            $bannedFiles += "$($_.Name) [$b] ($inFile)"
        }
    }
}

if ($emCount -eq 0) {
    Write-Host "  [OK] 0 em-dashes across $($Sites.Count) sites"
} else {
    Write-Host "  [WARN] $emCount em-dashes found:" -ForegroundColor Yellow
    foreach ($f in $emFiles) { Write-Host "         $f" -ForegroundColor Yellow }
}
if ($bannedCount -eq 0) {
    Write-Host "  [OK] 0 banned words across $($Sites.Count) sites"
} else {
    Write-Host "  [WARN] $bannedCount banned words found:" -ForegroundColor Yellow
    foreach ($f in $bannedFiles) { Write-Host "         $f" -ForegroundColor Yellow }
}

# 5. Generate deploy report
Write-Host ""
Write-Host "[5/5] Generating deploy report..." -ForegroundColor Green
$reportPath = Join-Path $OutDir "DEPLOY-REPORT.md"
$report = @"
# Titus Banks Deploy Report
**Build:** $Timestamp
**Sites:** $($Sites.Count)
**Status:** READY TO DEPLOY

## The 4 Sites

| Folder | Site | Index Size |
|---|---|---|
"@
foreach ($site in $Sites) {
    $indexPath = Join-Path $OutDir "$($site.OutFolder)\index.html"
    $size = [math]::Round((Get-Item $indexPath).Length / 1KB, 1)
    $report += "| ``$($site.OutFolder)/`` | $($site.Title) | ${size} KB |`n"
}

$report += @"

## Brand Compliance
- Em-dashes found: $emCount
- Banned words found: $bannedCount

## How to deploy (60 seconds)

1. Open https://app.netlify.com/drop in a new browser tab
2. Drag the entire ``NETLIFY-DROP/`` folder onto the drop zone
3. Netlify deploys all 4 subfolders as 4 separate sites in one drop
4. You get 4 URLs back. Example:
   - ``https://random-name-123.netlify.app/opendoor/``
   - ``https://random-name-123.netlify.app/ba/``
   - ``https://random-name-123.netlify.app/fjq/``
   - ``https://random-name-123.netlify.app/audit/``
5. In Netlify, rename each site to a memorable name (e.g. ``titus-opendoor``)
6. Copy the final URLs into the Linkpod master page

## What you do NOT need to do

- You do NOT need a Netlify account for the first drop
- You do NOT need to install Netlify CLI
- You do NOT need a custom domain (you can add one later in Netlify settings)
- You do NOT need to touch the HTML files

## Re-running this script

If you edit any of the 4 landing pages, re-run this script and re-drag the folder.
It takes 30 seconds. The drag-drop always overwrites the previous deploy.
"@

Set-Content -LiteralPath $reportPath -Value $report -Encoding UTF8
Write-Host "  [WROTE] DEPLOY-REPORT.md"

# 6. Final summary
Write-Host ""
Write-Host "====== BUILD COMPLETE ======" -ForegroundColor Cyan
Write-Host ""
Write-Host "Output folder: $OutDir"
Write-Host ""
Write-Host "NEXT STEP: Open https://app.netlify.com/drop and drag this folder:"
Write-Host "  $OutDir" -ForegroundColor Yellow
Write-Host ""
Write-Host "After Netlify gives you 4 URLs, paste them into the Linkpod master page."
Write-Host ""

# Open the folder in Explorer
Write-Host "Opening NETLIFY-DROP/ in Explorer..." -ForegroundColor Green
Start-Process explorer.exe -ArgumentList $OutDir
