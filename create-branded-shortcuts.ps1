$desktop = [Environment]::GetFolderPath('Desktop')
$base = "C:\Users\tbank\Desktop\Live Cowork"
$icons = Join-Path $base "app-icons"
$dock = Join-Path $desktop "AI App Dock"
New-Item -ItemType Directory -Path $dock -Force | Out-Null

$apps = @(
  @{ Name="EchoKey"; Target=(Join-Path $base "whisper-flow-float.vbs"); Icon=(Join-Path $icons "EchoKey.ico"); Desc="Local voice dictation" },
  @{ Name="SkillVault"; Target=(Join-Path $base "skill-store\index.html"); Icon=(Join-Path $icons "SkillVault.ico"); Desc="OpenCode skill store" },
  @{ Name="NoloCast Voice"; Target=(Join-Path $desktop "NOLO Voice App.vbs"); Icon=(Join-Path $icons "NoloCast-Voice.ico"); Desc="NOLO voice launcher" },
  @{ Name="RelayBoard"; Target=(Join-Path $desktop "Telegram Board.vbs"); Icon=(Join-Path $icons "RelayBoard.ico"); Desc="Telegram board" },
  @{ Name="FlowNode Local"; Target=(Join-Path $desktop "Start Local n8n.vbs"); Icon=(Join-Path $icons "FlowNode-Local.ico"); Desc="Local n8n launcher" },
  @{ Name="CommandDeck"; Target=(Join-Path $desktop "Titus Command Center.lnk"); Icon=(Join-Path $icons "CommandDeck.ico"); Desc="Titus command center" }
)

$shell = New-Object -ComObject WScript.Shell
foreach ($app in $apps) {
  foreach ($folder in @($desktop, $dock)) {
    $shortcutPath = Join-Path $folder ($app.Name + ".lnk")
    $lnk = $shell.CreateShortcut($shortcutPath)
    $lnk.TargetPath = $app.Target
    if (Test-Path -LiteralPath $app.Target) {
      $lnk.WorkingDirectory = Split-Path -Parent $app.Target
    } else {
      $lnk.WorkingDirectory = $desktop
    }
    $lnk.Description = $app.Desc
    if (Test-Path -LiteralPath $app.Icon) { $lnk.IconLocation = $app.Icon }
    $lnk.Save()
  }
  "Created: $($app.Name)"
}
"Dock: $dock"
