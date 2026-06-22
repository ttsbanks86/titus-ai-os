<#
.SYNOPSIS
  OpenCode Skill Store — One-Click Skill Installer
.DESCRIPTION
  Installs a skill from a local file or URL into the OpenCode skills directory.
  Includes security scanning before installation.
.PARAMETER Name
  Skill name (lowercase alphanumeric with hyphens).
.PARAMETER Source
  Local path to the SKILL.md file.
.PARAMETER Url
  URL to download the SKILL.md from.
.PARAMETER DryRun
  Preview the installation without making changes.
.PARAMETER Force
  Overwrite existing skill if it already exists.
.EXAMPLE
  .\install-skill.ps1 -Name "my-skill" -Source "C:\path\to\SKILL.md"
.EXAMPLE
  .\install-skill.ps1 -Name "my-skill" -Url "https://example.com/skill.md" -DryRun
#>

param(
    [Parameter(Mandatory = $true)]
    [string]$Name,

    [Parameter(ParameterSetName = "File")]
    [string]$Source,

    [Parameter(ParameterSetName = "Url")]
    [string]$Url,

    [switch]$DryRun,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$skillDir = "$HOME\.config\opencode\skills\$Name"
$skillFile = Join-Path $skillDir "SKILL.md"
$indexFile = "C:\Users\tbank\Desktop\Live Cowork\skill-store\SKILL-INDEX.md"

# ─── Validation ──────────────────────────────────────────────

if ($Name -notmatch '^[a-z0-9-]+$') {
    Write-Error "Skill name must be lowercase alphanumeric with hyphens only."
    exit 1
}

if (Test-Path $skillDir) {
    if (-not $Force) {
        Write-Warning "Skill '$Name' already exists at $skillDir. Use -Force to overwrite."
        exit 1
    }
    Write-Warning "Overwriting existing skill '$Name'..."
}

# ─── Get Skill Content ────────────────────────────────────────

$content = $null

if ($Source) {
    if (-not (Test-Path $Source)) {
        Write-Error "Source file not found: $Source"
        exit 1
    }
    $content = Get-Content -Raw -LiteralPath $Source
    Write-Host "[OK] Reading skill from file: $Source"
}

if ($Url) {
    Write-Host "[...] Downloading skill from: $Url"
    try {
        $content = Invoke-WebRequest -Uri $Url -UseBasicParsing | Select-Object -ExpandProperty Content
        Write-Host "[OK] Downloaded successfully"
    }
    catch {
        Write-Error "Failed to download skill: $_"
        exit 1
    }
}

if (-not $content) {
    Write-Error "No skill content provided. Use -Source (file) or -Url (web)."
    exit 1
}

# ─── Parse Frontmatter ────────────────────────────────────────

Write-Host "`n--- Pre-install check ---"

$nameMatch = [regex]::Match($content, '(?m)^name:\s*(.+)$')
$descMatch = [regex]::Match($content, '(?m)^description:\s*(.+)')

if ($nameMatch.Success) {
    Write-Host "  [OK] Name: $($nameMatch.Groups[1].Value.Trim())"
} else {
    Write-Host "  [WARN] No frontmatter 'name' field found"
}

if ($descMatch.Success) {
    Write-Host "  [OK] Description: $($descMatch.Groups[1].Value.Trim())"
} else {
    Write-Host "  [WARN] No frontmatter 'description' field found"
}

# ─── Security Scan ────────────────────────────────────────────

Write-Host "`n--- Security scan ---"

$alerts = @()
$riskScore = 0

# Check for frontmatter
if (-not ($content -match '^---')) {
    $alerts += "[WARN] No YAML frontmatter found (---)"
    $riskScore += 1
}

# Check for file writes
if ($content -match 'Set-Content|Out-File|Write-Host.*>|\[io\.file\]::WriteAll|fs\.writeFile') {
    $alerts += "[WARN] Contains file write operations"
    $riskScore += 2
}

# Check for network calls
if ($content -match 'Invoke-WebRequest|Invoke-RestMethod|curl\s|wget\s|fetch\(|axios\.') {
    $alerts += "[WARN] Contains network calls"
    $riskScore += 2
}

# Check for credentials/secrets
if ($content -match 'apiKey|api_key|token|password|secret|credentials|auth_token') {
    $alerts += "[HIGH] References credentials or secrets"
    $riskScore += 3
}

# Check for script execution
if ($content -match 'powershell\.exe|cmd\.exe|bash\s|npx\s|node\s') {
    $alerts += "[WARN] Executes external scripts"
    $riskScore += 2
}

# Check for registry access
if ($content -match 'HKLM|HKCU|Get-ItemProperty.*HK|Set-ItemProperty.*HK') {
    $alerts += "[HIGH] Accesses Windows registry"
    $riskScore += 3
}

# Check for environment variables
if ($content -match '\$env\:|process\.env') {
    $alerts += "[WARN] Reads environment variables"
    $riskScore += 1
}

# Check for deletion
if ($content -match 'Remove-Item|del\s|rm\s') {
    $alerts += "[HIGH] Contains file deletion operations"
    $riskScore += 3
}

if ($alerts.Count -eq 0) {
    Write-Host "  [OK] No security issues detected - Safe to install"
} else {
    foreach ($alert in $alerts) {
        Write-Host "  $alert"
    }
    if ($riskScore -ge 5) {
        $riskLabel = "HIGH RISK"
    } elseif ($riskScore -ge 3) {
        $riskLabel = "MEDIUM RISK"
    } else {
        $riskLabel = "LOW RISK"
    }
    Write-Host "`n  Overall: $riskLabel (score: $riskScore)"
}

# ─── Install ──────────────────────────────────────────────────

if ($DryRun) {
    Write-Host "`n--- DRY RUN - No changes made ---"
    Write-Host "  Would create: $skillFile"
    Write-Host "  Content length: $($content.Length) characters"
    Write-Host "  Risk score: $riskScore/10"
    exit 0
}

Write-Host "`n--- Installing skill '$Name' ---"

# Create directory
New-Item -ItemType Directory -Path $skillDir -Force | Out-Null

# Write skill file
$content | Set-Content -LiteralPath $skillFile -Encoding UTF8

Write-Host "  [OK] Skill written to: $skillFile"

# ─── Post-Install Instructions ────────────────────────────────

Write-Host "`n=== Installation complete! ==="
Write-Host ""
Write-Host "  Location: $skillFile"
Write-Host ""
Write-Host "  Next steps:"
Write-Host "  1. Verify: Get-Content '$skillFile' -Head 5"
Write-Host "  2. Update SKILL-INDEX.md with the new entry if needed"
Write-Host "  3. Restart OpenCode to load the new skill"
Write-Host "  4. Test it by describing your task"

if ($riskScore -ge 3) {
    Write-Host ""
    Write-Host "  [WARN] RECOMMENDATION: Test this skill using skill-simulator before regular use."
}
