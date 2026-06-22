# =============================================================================
# Set-CloudApiKeys.ps1
# =============================================================================
# Sets API keys as persistent user-level environment variables so OpenCode
# and Claude Code can use them.
#
# Usage:
#   1. Edit C:\Users\tbank\.config\opencode\.env with your real keys
#   2. Run this script as administrator
#   3. Restart your terminal / Claude Code
# =============================================================================

$envFile = "$env:USERPROFILE\.config\opencode\.env"

if (-not (Test-Path $envFile)) {
    Write-Host "ERROR: $envFile not found." -ForegroundColor Red
    Write-Host "Copy .env.template to .env and fill in your keys first." -ForegroundColor Yellow
    exit 1
}

$envVars = @{}
Get-Content $envFile | ForEach-Object {
    if ($_ -match '^\s*([A-Z_]+)=(.*)$' -and -not $_.StartsWith('#')) {
        $key = $matches[1]
        $value = $matches[2]
        $envVars[$key] = $value
    }
}

$updated = $false

if ($envVars['ANTHROPIC_API_KEY'] -and $envVars['ANTHROPIC_API_KEY'] -ne 'sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') {
    [Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', $envVars['ANTHROPIC_API_KEY'], 'User')
    Write-Host "  ANTHROPIC_API_KEY set." -ForegroundColor Green
    $updated = $true
} else {
    Write-Host "  ANTHROPIC_API_KEY: not set (placeholder or missing)." -ForegroundColor Yellow
}

if ($envVars['OPENAI_API_KEY'] -and $envVars['OPENAI_API_KEY'] -ne 'sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') {
    [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $envVars['OPENAI_API_KEY'], 'User')
    Write-Host "  OPENAI_API_KEY set." -ForegroundColor Green
    $updated = $true
} else {
    Write-Host "  OPENAI_API_KEY: not set (placeholder or missing)." -ForegroundColor Yellow
}

if ($envVars['KIE_API_KEY'] -and $envVars['KIE_API_KEY'] -ne 'sk-kie-xxxx') {
    [Environment]::SetEnvironmentVariable('KIE_API_KEY', $envVars['KIE_API_KEY'], 'User')
    Write-Host "  KIE_API_KEY set." -ForegroundColor Green
    $updated = $true
} else {
    Write-Host "  KIE_API_KEY: not set (placeholder or missing)." -ForegroundColor Yellow
}

if ($envVars['OPENCODE_API_KEY'] -and $envVars['OPENCODE_API_KEY'] -ne 'sk-opencode-xxxx') {
    [Environment]::SetEnvironmentVariable('OPENCODE_API_KEY', $envVars['OPENCODE_API_KEY'], 'User')
    Write-Host "  OPENCODE_API_KEY set (OpenCodeGo)." -ForegroundColor Green
    $updated = $true
} else {
    Write-Host "  OPENCODE_API_KEY: not set (placeholder or missing)." -ForegroundColor Yellow
}

# Remove proxy base URL if a real Anthropic key was set
if ($updated -and $envVars['ANTHROPIC_API_KEY'] -and $envVars['ANTHROPIC_API_KEY'] -ne 'sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx') {
    [Environment]::SetEnvironmentVariable('ANTHROPIC_BASE_URL', $null, 'User')
    Write-Host "  ANTHROPIC_BASE_URL removed (no longer proxying through Ollama)." -ForegroundColor Green
}

Write-Host ""
if ($updated) {
    Write-Host "Done. Restart your terminal and Claude Code for changes to take effect." -ForegroundColor Green
} else {
    Write-Host "No keys were set. Edit $envFile with your real API keys and re-run." -ForegroundColor Yellow
}
