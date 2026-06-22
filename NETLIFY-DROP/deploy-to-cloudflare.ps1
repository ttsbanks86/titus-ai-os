# Titus Banks Cloudflare Pages Deploy Script
# Deploys all 4 brand sites to Cloudflare Pages
# Usage: Right-click > Run with PowerShell, or run from PowerShell

$ErrorActionPreference = "Stop"
$rootPath = "C:\Users\tbank\Desktop\Live Cowork\NETLIFY-DROP"

# Check Wrangler
Write-Host "Checking Wrangler..." -ForegroundColor Cyan
$wranglerVersion = wrangler --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Wrangler not found. Installing..." -ForegroundColor Yellow
    npm install -g wrangler
}

# Check auth
Write-Host "Checking Cloudflare auth..." -ForegroundColor Cyan
$whoami = wrangler whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Not logged in. Opening browser..." -ForegroundColor Yellow
    wrangler login
    Write-Host "Press Enter after browser auth completes..." -ForegroundColor Yellow
    Read-Host
}

# Confirm
Write-Host ""
Write-Host "Ready to deploy 4 sites from: $rootPath" -ForegroundColor Green
Write-Host ""
Write-Host "  1. opendoor  -> Open Door AI Systems"
Write-Host "  2. ba        -> Business Analysis and Operations"
Write-Host "  3. fjq       -> Faithful Journey Quest"
Write-Host "  4. audit     -> Faith and Operations Gap Audit"
Write-Host ""
$confirm = Read-Host "Deploy all 4? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Red
    exit
}

# Deploy each
Set-Location $rootPath

$sites = @(
    @{folder="opendoor"; project="titus-opendoor"},
    @{folder="ba"; project="titus-ba"},
    @{folder="fjq"; project="titus-fjq"},
    @{folder="audit"; project="titus-audit"}
)

foreach ($site in $sites) {
    Write-Host ""
    Write-Host "Deploying $($site.folder) -> $($site.project)..." -ForegroundColor Cyan
    try {
        wrangler pages deploy $site.folder --project-name=$site.project --commit-dirty=true
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] $($site.folder) deployed" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] $($site.folder) failed" -ForegroundColor Red
        }
    } catch {
        Write-Host "[ERROR] $($site.folder): $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "All deployments complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Go to https://dash.cloudflare.com > Workers & Pages"
Write-Host "  2. Each site has a *.pages.dev URL"
Write-Host "  3. Add custom domain if desired"
Write-Host "  4. Update Linkpod master page with new URLs"
Write-Host ""
Read-Host "Press Enter to exit"
