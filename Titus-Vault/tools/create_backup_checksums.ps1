param(
    [Parameter(Mandatory = $true)][string]$BackupPath,
    [Parameter(Mandatory = $true)][string]$ManifestPath,
    [Parameter(Mandatory = $true)][string]$DonePath
)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath $BackupPath).Path
Get-ChildItem -LiteralPath $root -Recurse -File |
    Where-Object { $_.Name -ne 'TKOS-Baseline-Checksums.csv' } |
    ForEach-Object {
        $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $_.FullName
        [pscustomobject]@{
            Path = $_.FullName.Substring($root.Length + 1)
            SHA256 = $hash.Hash
            Bytes = $_.Length
        }
    } | Export-Csv -NoTypeInformation -Encoding UTF8 -LiteralPath $ManifestPath

$count = (Import-Csv -LiteralPath $ManifestPath).Count
Set-Content -LiteralPath $DonePath -Value "CHECKSUMS=$count" -Encoding UTF8
