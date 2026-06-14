# Build NOLA Reader v2 — Single EXE
param([switch]$SkipPyInstaller)

$Python = 'C:\Python313\python.exe'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $ScriptDir 'nola_reader_v2.py'
$SpecPath = Join-Path $ScriptDir 'nola_reader_v2.spec'
$OutputDir = Join-Path $ScriptDir 'dist'

Write-Host '═' x60
Write-Host 'NOLA Reader v2 — Build'
Write-Host '═' x60

# 1. Syntax check
Write-Host '`n[1/4] Syntax check...'
& $Python -m py_compile $ScriptPath
if ($LASTEXITCODE -ne 0) { throw 'Syntax error' }
Write-Host '  OK' -ForegroundColor Green

# 2. Clean old build
Write-Host '`n[2/4] Cleaning previous build...'
if (Test-Path -LiteralPath $OutputDir) {
    Remove-Item -LiteralPath $OutputDir -Recurse -Force
}
Remove-Item -LiteralPath (Join-Path $ScriptDir 'build') -Recurse -Force -ErrorAction SilentlyContinue
Write-Host '  OK' -ForegroundColor Green

# 3. Build
Write-Host '`n[3/4] Building single EXE (this takes a minute)...'
if (-not $SkipPyInstaller) {
    & $Python -m PyInstaller $SpecPath --clean --noconfirm 2>&1 | ForEach-Object { Write-Progress -Activity 'Building EXE...' -Status $_ }
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed' }
}
Write-Host '  OK' -ForegroundColor Green

# 4. Verify
$ExePath = Join-Path $OutputDir 'NOLA_Reader.exe'
Write-Host '`n[4/4] Verifying output...'
if (Test-Path -LiteralPath $ExePath) {
    $info = Get-Item -LiteralPath $ExePath
    Write-Host "  EXE: $($info.FullName)" -ForegroundColor Green
    Write-Host "  Size: $([math]::Round($info.Length / 1MB, 1)) MB" -ForegroundColor Cyan
    Write-Host "`nBuild complete! Run: $ExePath"
} else {
    Write-Host '  ERROR: EXE not found at expected path' -ForegroundColor Red
    throw 'Build failed'
}
