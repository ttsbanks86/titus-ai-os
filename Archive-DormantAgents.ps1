<#
.SYNOPSIS
    Archive dormant agent and skill definitions to .agent-archive/ for safe restore.
    Moves files (no deletion). Generates RESTORE_LOG.md with exact paths.

.DESCRIPTION
    Moves identified dormant/duplicate agent and skill files to a dated archive
    folder at C:\Users\tbank\.agent-archive\. Files are MOVED (not copied).
    RESTORE_LOG.md is generated per category with original path, archive path,
    and restore command.

    ALWAYS run with -WhatIf first to preview what will move.

.PARAMETER WhatIf
    Show what would move without moving anything.

.PARAMETER Force
    Skip confirmation prompts.

.EXAMPLE
    .\Archive-DormantAgents.ps1 -WhatIf

.EXAMPLE
    .\Archive-DormantAgents.ps1

.NOTES
    No files are ever deleted. All archived items can be restored.
#>

param(
    [switch]$WhatIf,
    [switch]$Force
)

$UserProfile = $env:USERPROFILE
$LiveCowork = Join-Path $UserProfile "Desktop\Live Cowork"
$ArchiveRoot = Join-Path $UserProfile ".agent-archive"
$DateStamp = "2026-06-21_redesign-v1"
$ArchiveDir  = Join-Path $ArchiveRoot $DateStamp

# ─── Write RESTORE_LOG.md for a category ─────────────────────────────────────
function Write-ArchiveLog {
    param($Category, $ArchiveSubDir, $FileMap, $Description, $RiskNote)

    $logPath = Join-Path $ArchiveSubDir "RESTORE_LOG.md"
    $restoreSrc = $ArchiveSubDir.Replace($ArchiveRoot, ".agent-archive")

    $content = @"
# Restore Log - $Category

Archived: $DateStamp
Description: $Description

## Risk Assessment
Risk: $RiskNote

## Restore Commands

### Restore all files in this category:
  Copy-Item -Path "$restoreSrc\*" -Destination "<ORIGINAL_PATH>" -Recurse

### Restore the entire archive:
  Copy-Item -Path "$ArchiveRoot\*" -Destination "$UserProfile" -Recurse

## File Inventory

"@

    $i = 0
    $invLines = @()
    $invLines += "| # | Original Path | Archive Path |"
    $invLines += "|---|--------------|--------------|"

    foreach ($orig in ($FileMap.Keys | Sort-Object)) {
        $i++
        $name = $FileMap[$orig]
        $relOrig = $orig.Replace($UserProfile, "~")
        $relArch = "$restoreSrc\$name"
        $invLines += "| $i | $relOrig | $relArch |"
    }

    $content += ($invLines -join "`n")

    if (-not $WhatIf) {
        $content | Out-File -FilePath $logPath -Encoding UTF8
        Write-Host "  RESTORE_LOG written: $logPath" -ForegroundColor Green
    } else {
        Write-Host "  [WhatIf] Would write RESTORE_LOG ($($FileMap.Count) items)" -ForegroundColor Cyan
    }
}

# ─── Move files for one category ─────────────────────────────────────────────
function Move-ToArchive {
    param($CategoryName, $SourceDir, $ArchiveSubDirName, $FileNames, $ItemType, $Description, $RiskNote)

    $sourcePath = $SourceDir
    if (-not (Test-Path $sourcePath)) {
        Write-Host "  SKIP: Source not found: $sourcePath" -ForegroundColor Yellow
        return $null
    }

    $archiveSubDir = Join-Path $ArchiveDir $ArchiveSubDirName
    $fileMap = @{}

    foreach ($name in $FileNames) {
        $fullSource = Join-Path $sourcePath $name
        if (-not (Test-Path $fullSource)) {
            Write-Host "  SKIP: Not found: $name" -ForegroundColor Yellow
            continue
        }
        $fileMap[$fullSource] = $name
    }

    if ($fileMap.Count -eq 0) {
        Write-Host "  Nothing to archive in $CategoryName" -ForegroundColor Yellow
        return $null
    }

    Write-Host ""
    Write-Host "-- $CategoryName ($($fileMap.Count) $($ItemType)s) --" -ForegroundColor Magenta
    Write-Host "  From: $sourcePath" -ForegroundColor Gray
    Write-Host "  To:   $archiveSubDir" -ForegroundColor Gray
    Write-Host "  Risk: $RiskNote" -ForegroundColor Gray

    if ($WhatIf) {
        foreach ($orig in ($fileMap.Keys | Sort-Object)) {
            $leaf = Split-Path $orig -Leaf
            Write-Host "  [WhatIf] Move: $leaf -> $archiveSubDir\$leaf" -ForegroundColor Cyan
        }
    } else {
        New-Item -ItemType Directory -Path $archiveSubDir -Force | Out-Null
        Write-Host "  Created directory" -ForegroundColor Gray

        foreach ($orig in ($fileMap.Keys | Sort-Object)) {
            $dest = Join-Path $archiveSubDir $fileMap[$orig]
            Move-Item -Path $orig -Destination $dest -Force
            Write-Host "  Moved: $(Split-Path $orig -Leaf)" -ForegroundColor Green
        }

        Write-Host "  OK: $($fileMap.Count) items archived" -ForegroundColor Green
    }

    Write-ArchiveLog -Category $CategoryName `
                     -ArchiveSubDir $archiveSubDir `
                     -FileMap $fileMap `
                     -Description $Description `
                     -RiskNote $RiskNote

    return $fileMap.Count
}

# ─── Build Categories ────────────────────────────────────────────────────────

$ClaudeAgentDir  = Join-Path $UserProfile ".claude\agents"
$ClaudeSkillDir  = Join-Path $UserProfile ".claude\skills"
$OpenCodeSkillDir = Join-Path $UserProfile ".config\opencode\skills"
$GooseSkillDir   = Join-Path $UserProfile ".agents\skills"
$WorkspaceSkillDir = Join-Path $LiveCowork ".agents\skills"
$LegacyAssetsDir   = Join-Path $LiveCowork "Legacy-Business-Assets"

$categories = @()

# ─── KEPT: 10 Specialist Claude Agents ───
$keptClaudeAgents = @(
    "architect.md",       # System architecture & design
    "code-reviewer.md",   # Code review specialist
    "planner.md",         # Task planning & decomposition
    "performance-optimizer.md",  # Performance analysis
    "security-reviewer.md",      # Security code review
    "docs-lookup.md",     # Documentation lookup
    "tdd-guide.md",       # TDD workflow guidance
    "database-reviewer.md",      # Database design review
    "marketing-agent.md",        # Marketing strategy
    "seo-specialist.md"          # SEO analysis
)

# ─── KEPT: 4 Titus-Specific Business Assets (Goose) ───
$titusBusinessAssets = @(
    "titus-banks-brand",
    "book-launch",
    "review-lead-recovery",
    "identity-credit"
)

# 1. Claude Agents (59 dormant - 10 kept)
$categories += @{
    Name = "Claude Agents (59 dormant, 10 kept)"
    Source = $ClaudeAgentDir
    SubDir = "01-claude-agents"
    Items = @(
        "a11y-architect.md", "build-error-resolver.md", "chief-of-staff.md",
        "code-architect.md", "code-explorer.md", "code-simplifier.md",
        "comment-analyzer.md", "conversation-analyzer.md", "cpp-build-resolver.md",
        "cpp-reviewer.md", "csharp-reviewer.md", "dart-build-resolver.md",
        "django-build-resolver.md", "django-reviewer.md",
        "doc-updater.md", "e2e-runner.md", "fastapi-reviewer.md",
        "flutter-reviewer.md", "fsharp-reviewer.md", "gan-evaluator.md", "gan-generator.md",
        "gan-planner.md", "go-build-resolver.md", "go-reviewer.md",
        "harmonyos-app-resolver.md", "harness-optimizer.md", "healthcare-reviewer.md",
        "homelab-architect.md", "java-build-resolver.md", "java-reviewer.md",
        "kotlin-build-resolver.md", "kotlin-reviewer.md", "loop-operator.md",
        "mle-reviewer.md", "network-architect.md",
        "network-config-reviewer.md", "network-troubleshooter.md", "opensource-forker.md",
        "opensource-packager.md", "opensource-sanitizer.md",
        "php-reviewer.md", "pr-test-analyzer.md", "python-reviewer.md",
        "pytorch-build-resolver.md", "react-build-resolver.md", "react-reviewer.md",
        "refactor-cleaner.md", "rust-build-resolver.md", "rust-reviewer.md",
        "sales-company.md", "sales-competitive.md", "sales-contacts.md",
        "sales-opportunity.md", "sales-strategy.md",
        "silent-failure-hunter.md", "swift-build-resolver.md",
        "swift-reviewer.md", "type-design-analyzer.md",
        "typescript-reviewer.md"
    )
    Type = "File"
    Desc = "59 dormant Claude Code agent .md files. 10 kept (architect, code-reviewer, planner, performance-optimizer, security-reviewer, docs-lookup, tdd-guide, database-reviewer, marketing-agent, seo-specialist)."
    Risk = "LOW - Not loaded by default in Claude Code. Restore by copying back to ~/.claude/agents/"
}

# 2. Claude Sales Skills (14 directories)
$categories += @{
    Name = "Claude Sales Skills (14 duplicates)"
    Source = $ClaudeSkillDir
    SubDir = "02-claude-sales-skills"
    Items = @(
        "sales", "sales-competitors", "sales-contacts", "sales-followup",
        "sales-icp", "sales-objections", "sales-outreach", "sales-prep",
        "sales-proposal", "sales-prospect", "sales-qualify", "sales-report",
        "sales-report-pdf", "sales-research"
    )
    Type = "Directory"
    Desc = "14 sales skill directories. Duplicates of OpenCode sales skills."
    Risk = "LOW - Sales is not current work. OpenCode has the canonical set."
}

# 3. Claude GSAP Skills (8 directories)
$categories += @{
    Name = "Claude GSAP Skills (8 duplicates)"
    Source = $ClaudeSkillDir
    SubDir = "03-claude-gsap-skills"
    Items = @(
        "gsap-core", "gsap-frameworks", "gsap-performance", "gsap-plugins",
        "gsap-react", "gsap-scrolltrigger", "gsap-timeline", "gsap-utils"
    )
    Type = "Directory"
    Desc = "8 GSAP skill directories. OpenCode has the canonical gsap-core."
    Risk = "LOW - OpenCode canonical. Restore if Claude-specific GSAP work needs isolation."
}

# 4. OpenCode Cybersecurity Skills (20 directories)
$categories += @{
    Name = "OpenCode Cybersecurity Skills (20)"
    Source = $OpenCodeSkillDir
    SubDir = "04-opencode-cybersecurity"
    Items = @(
        "analyzing-azure-activity-logs-for-threats",
        "analyzing-memory-dumps-with-volatility",
        "analyzing-network-traffic-with-wireshark",
        "auditing-kubernetes-cluster-rbac",
        "auditing-terraform-infrastructure-for-security",
        "building-detection-rules-with-sigma",
        "building-ioc-enrichment-pipeline-with-opencti",
        "building-threat-hunt-hypothesis-framework",
        "building-vulnerability-dashboard-with-defectdojo",
        "conducting-api-security-testing",
        "conducting-cloud-incident-response",
        "conducting-malware-incident-response",
        "deploying-active-directory-honeytokens",
        "detecting-ai-model-prompt-injection-attacks",
        "detecting-aws-cloudtrail-anomalies",
        "detecting-business-email-compromise",
        "performing-deception-technology-deployment",
        "performing-memory-forensics-with-volatility3",
        "performing-threat-intelligence-sharing-with-misp",
        "performing-threat-modeling-with-owasp-threat-dragon"
    )
    Type = "Directory"
    Desc = "20 SOC/IR skill directories. Zero relevance to BA job search or AI systems work."
    Risk = "LOW - None relate to current work. Restore if cybersecurity work resumes."
}

# 5. OpenCode Retired Tools (6 directories)
$categories += @{
    Name = "OpenCode Retired Tools (6)"
    Source = $OpenCodeSkillDir
    SubDir = "05-opencode-retired"
    Items = @(
        "ai-inspiration",
        "composio-mcp-hermes",
        "local-tts",
        "open-animation",
        "skill-store",
        "speech-context-corrector"
    )
    Type = "Directory"
    Desc = "6 retired skill directories: local TTS (replaced by cloud), local animation (stopped), Hermes API (credits exhausted), AI inspiration (never used), skill store (deprecated), speech context corrector (merged)."
    Risk = "LOW - All replaced by cloud alternatives or deprecated."
}

# 6. Goose Duplicates (16 directories - 4 Titus assets excluded)
$categories += @{
    Name = "Goose Agent Duplicates (16)"
    Source = $GooseSkillDir
    SubDir = "06-goose-duplicates"
    Items = @(
        "book-access-workflow", "brand-guidelines",
        "browser-automation", "career-ops", "doc-coauthoring",
        "file-organization", "gmail-automation",
        "identity-eraser", "internal-comms", "learning-extractor",
        "local-ai", "mcp-builder", "project-radar",
        "system-cleanup",
        "windows-automation", "workflow-orchestration"
    )
    Type = "Directory"
    Desc = "16 Goose skill directories with OpenCode equivalents. 4 Titus-specific assets moved to Legacy-Business-Assets."
    Risk = "LOW - OpenCode is canonical runtime. Goose skills are redundant."
}

# 7. Workspace Duplicates (17 directories)
$categories += @{
    Name = "Workspace Agent Duplicates (17)"
    Source = $WorkspaceSkillDir
    SubDir = "07-workspace-duplicates"
    Items = @(
        "animejs", "book-access-workflow", "contribute-catalog",
        "css-animations", "gsap", "hyperframes", "hyperframes-cli",
        "hyperframes-media", "hyperframes-registry", "lottie",
        "remotion-to-hyperframes", "speech-context-corrector", "tailwind",
        "three", "typegpu", "waapi", "website-to-hyperframes"
    )
    Type = "Directory"
    Desc = "17 workspace skill directories. All have OpenCode equivalents. HyperFrames skills consolidated into OpenCode."
    Risk = "LOW - OpenCode is canonical runtime. Workspace skills are redundant."
}

# ─── Pre-flight ──────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Dormant Agent & Skill Archive - Pre-Flight" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$totalItems = 0
foreach ($cat in $categories) { $totalItems += $cat.Items.Count }

Write-Host "Archive Root:       $ArchiveDir" -ForegroundColor White
Write-Host "Categories:         $($categories.Count)" -ForegroundColor White
Write-Host "Items to archive:   $totalItems" -ForegroundColor White
Write-Host "Legacy assets:      $($titusBusinessAssets.Count) (to Legacy-Business-Assets)" -ForegroundColor White
Write-Host "Claude agents kept: $($keptClaudeAgents.Count) (architect, code-reviewer, planner, etc.)" -ForegroundColor White
Write-Host "Rollback:           $env:USERPROFILE\.agent-archive\PRE-REDESIGN_CHECKPOINT_2026-06-21_092629" -ForegroundColor White
Write-Host "Operation:          MOVE (files leave original location)" -ForegroundColor Yellow
Write-Host ""

Write-Host "--- 3 Adjustments Applied ---" -ForegroundColor Green
Write-Host "Adj 1: 10 specialist Claude agents PRESERVED in place" -ForegroundColor Green
Write-Host "Adj 2: 4 Titus business assets -> Legacy-Business-Assets/" -ForegroundColor Green
Write-Host "Adj 3: ZIP snapshots created for full rollback" -ForegroundColor Green
Write-Host ""
Write-Host "--- What Stays ---" -ForegroundColor Cyan
Write-Host "$($keptClaudeAgents.Count) Claude agents: $($keptClaudeAgents -join ', ')" -ForegroundColor Cyan
Write-Host "$($titusBusinessAssets.Count) Titus assets: $($titusBusinessAssets -join ', ')" -ForegroundColor Cyan
Write-Host ""
Write-Host "--- What Goes (to .agent-archive) ---" -ForegroundColor Yellow
Write-Host "59 Claude agents (language-specific, build, GAN, sales)" -ForegroundColor Yellow
Write-Host "14 Claude sales skills" -ForegroundColor Yellow
Write-Host "8 Claude GSAP skills" -ForegroundColor Yellow
Write-Host "20 cybersecurity skills" -ForegroundColor Yellow
Write-Host "6 retired tools" -ForegroundColor Yellow
Write-Host "16 Goose duplicates" -ForegroundColor Yellow
Write-Host "17 workspace duplicates" -ForegroundColor Yellow
Write-Host "Total: $totalItems items to move, $($titusBusinessAssets.Count) to legacy folder" -ForegroundColor Yellow

if ($WhatIf) {
    Write-Host "  WHATIF MODE - No files will be moved" -ForegroundColor Yellow
    Write-Host ""
}

# ─── Confirmation ────────────────────────────────────────────────────────────
if ((-not $WhatIf) -and (-not $Force)) {
    Write-Host "WARNING: This will MOVE $totalItems items from their current locations" -ForegroundColor Red
    Write-Host "         to the archive folder. Nothing is deleted." -ForegroundColor Red
    Write-Host ""
    Write-Host "Preview first with: .\Archive-DormantAgents.ps1 -WhatIf" -ForegroundColor Cyan
    Write-Host ""
    $confirm = Read-Host "Type 'ARCHIVE' to proceed, or press Enter to cancel"
    if ($confirm -ne "ARCHIVE") {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
}

# ─── Move Titus Assets to Legacy-Business-Assets ───────────────────────────
function Move-LegacyBusinessAssets {
    param($SourceDir, $AssetNames)

    $destDir = $LegacyAssetsDir
    $fileMap = @{}

    foreach ($name in $AssetNames) {
        $fullSource = Join-Path $SourceDir $name
        if (-not (Test-Path $fullSource)) {
            Write-Host "  SKIP: Not found: $name" -ForegroundColor Yellow
            continue
        }
        $fileMap[$fullSource] = $name
    }

    if ($fileMap.Count -eq 0) {
        Write-Host "  Nothing to move for Legacy Business Assets" -ForegroundColor Yellow
        return $null
    }

    Write-Host ""
    Write-Host "-- Legacy Business Assets ($($fileMap.Count) items) --" -ForegroundColor Magenta
    Write-Host "  From: $SourceDir" -ForegroundColor Gray
    Write-Host "  To:   $destDir" -ForegroundColor Gray
    Write-Host "  (Not archived - kept locally for reference)" -ForegroundColor Gray

    if ($WhatIf) {
        foreach ($orig in ($fileMap.Keys | Sort-Object)) {
            $leaf = Split-Path $orig -Leaf
            Write-Host "  [WhatIf] Move: $leaf -> $destDir\$leaf" -ForegroundColor Cyan
        }
    } else {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        Write-Host "  Created directory: $destDir" -ForegroundColor Gray

        foreach ($orig in ($fileMap.Keys | Sort-Object)) {
            $dest = Join-Path $destDir $fileMap[$orig]
            Move-Item -Path $orig -Destination $dest -Force
            Write-Host "  Moved: $(Split-Path $orig -Leaf)" -ForegroundColor Green
        }

        Write-Host "  OK: $($fileMap.Count) items relocated to Legacy-Business-Assets" -ForegroundColor Green
    }

    return $fileMap.Count
}

# ─── Execute ─────────────────────────────────────────────────────────────────
$totalArchived = 0
$totalLegacy = 0
$failedCats = @()

foreach ($cat in $categories) {
    $result = Move-ToArchive -CategoryName $cat.Name `
        -SourceDir $cat.Source `
        -ArchiveSubDirName $cat.SubDir `
        -FileNames $cat.Items `
        -ItemType $cat.Type `
        -Description $cat.Desc `
        -RiskNote $cat.Risk

    if ($result -ne $null) {
        $totalArchived += $result
    } else {
        $failedCats += $cat.Name
    }
}

# ─── Execute Legacy Assets Move ──────────────────────────────────────────────
$legacyResult = Move-LegacyBusinessAssets -SourceDir $GooseSkillDir -AssetNames $titusBusinessAssets
if ($legacyResult -ne $null) {
    $totalLegacy = $legacyResult
}

# ─── Summary ─────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Archive Summary" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if ($WhatIf) {
    Write-Host "WhatIf complete." -ForegroundColor Cyan
    Write-Host "  Items to archive:      $totalArchived" -ForegroundColor Cyan
    Write-Host "  Legacy assets to move: $totalLegacy" -ForegroundColor Cyan
    Write-Host "  Rollback checkpoint:   C:\Users\tbank\.agent-archive\PRE-REDESIGN_CHECKPOINT_2026-06-21_092629" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Run without -WhatIf to execute." -ForegroundColor Cyan
} else {
    Write-Host "Archive complete." -ForegroundColor Green
    Write-Host "  Items archived:         $totalArchived" -ForegroundColor Green
    Write-Host "  Legacy assets moved:    $totalLegacy" -ForegroundColor Green
    Write-Host "  Archive location:       $ArchiveDir" -ForegroundColor Green
    Write-Host "  Legacy assets location: $LegacyAssetsDir" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Rollback: unzip C:\Users\tbank\.agent-archive\PRE-REDESIGN_CHECKPOINT_2026-06-21_092629" -ForegroundColor Cyan
    Write-Host "  To restore everything from archive:" -ForegroundColor White
    Write-Host "    Copy-Item -Path `"$ArchiveDir\*`" -Destination `"C:\Users\tbank\`" -Recurse" -ForegroundColor Gray
}

if ($failedCats.Count -gt 0) {
    Write-Host ""
    Write-Host "Categories with errors:" -ForegroundColor Yellow
    foreach ($f in $failedCats) { Write-Host "  - $f" -ForegroundColor Yellow }
}

Write-Host ""
Write-Host "Zero files were deleted. All archived items can be restored." -ForegroundColor Green
