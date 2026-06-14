# Build Whisper My Idea Pro v2 — Single EXE
param([switch]$SkipPyInstaller)

$Python = 'C:\Python313\python.exe'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath = Join-Path $ScriptDir 'main.py'
$SpecPath = Join-Path $ScriptDir 'whisper_pro_v2.spec'
$OutputDir = Join-Path $ScriptDir 'dist'

Write-Host '═' x60
Write-Host 'Whisper My Idea Pro v2 — Build'
Write-Host '═' x60

# 1. Syntax check
Write-Host "`n[1/5] Syntax check..."
& $Python -m py_compile "$ScriptDir\main.py"
& $Python -m py_compile "$ScriptDir\main_window.py"
& $Python -m py_compile "$ScriptDir\hud_window.py"
& $Python -m py_compile "$ScriptDir\model_manager.py"
& $Python -m py_compile "$ScriptDir\audio_recorder.py"
& $Python -m py_compile "$ScriptDir\transcriber.py"
& $Python -m py_compile "$ScriptDir\hotkey_manager.py"
& $Python -m py_compile "$ScriptDir\model_manager.py"
& $Python -m py_compile "$ScriptDir\audio_recorder.py"
& $Python -m py_compile "$ScriptDir\vocab.py"
& $Python -m py_compile "$ScriptDir\history.py"
& $Python -m py_compile "$ScriptDir\stats.py"
& $Python -m py_compile "$ScriptDir\settings.py"
& $Python -m py_compile "$ScriptDir\constants.py"
if ($LASTEXITCODE -ne 0) { throw 'Syntax error' }
Write-Host '  OK' -ForegroundColor Green

# 2. Clean old build
Write-Host "`n[2/5] Cleaning previous build..."
$distDir = Join-Path $ScriptDir 'dist'
$buildDir = Join-Path $ScriptDir 'build'
if (Test-Path -LiteralPath $distDir) { Remove-Item -LiteralPath $distDir -Recurse -Force }
Remove-Item -LiteralPath $buildDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host '  OK' -ForegroundColor Green

# 3. Install dependencies
Write-Host "`n[3/5] Checking dependencies..."
& $Python -m pip install -q PySide6 faster-whisper sounddevice numpy keyboard pyperclip pyinstaller 2>&1 | Out-Null
Write-Host '  OK' -ForegroundColor Green

# 4. Build
Write-Host "`n[4/5] Building single EXE (this takes 1-2 minutes)..."
if (-not $SkipPyInstaller) {
    & $Python -m PyInstaller "$ScriptDir\whisper_pro_v2.spec" --clean --noconfirm 2>&1 | ForEach-Object { Write-Progress -Activity 'Building EXE...' -Status $_ }
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller failed' }
}
Write-Host '  OK' -ForegroundColor Green

# 5. Verify
$ExePath = Join-Path $ScriptDir 'dist\WhisperMyIdeaPro.exe'
Write-Host "`n[5/5] Verifying output..."
if (Test-Path -LiteralPath $ExePath) {
    $info = Get-Item -LiteralPath $ExePath
    Write-Host "  EXE: $($info.FullName)" -ForegroundColor Green
    Write-Host "  Size: $([math]::Round($info.Length / 1MB, 1)) MB" -ForegroundColor Cyan
    Write-Host "`nBuild complete! Run: $ExePath"
} else {
    Write-Host '  ERROR: EXE not found at expected path' -ForegroundColor Red
    throw 'Build failed'
}