param(
    [string]$Url,
    [string]$Text,
    [string]$File,
    [string]$Out
)

$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = 'C:\Python313\python.exe'
if (-not (Test-Path -LiteralPath $Python)) {
    $Python = 'python'
}

$ArgsList = @((Join-Path $ScriptDir 'extractor.py'))

if ($Url) {
    $ArgsList += @('--url', $Url)
} elseif ($Text) {
    $ArgsList += @('--text', $Text)
} elseif ($File) {
    $ArgsList += @('--file', $File)
} else {
    throw 'Provide one of -Url, -Text, or -File.'
}

if ($Out) {
    $ArgsList += @('--out', $Out)
}

& $Python @ArgsList
