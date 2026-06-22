$ws = New-Object -ComObject WScript.Shell
$desktop = [System.Environment]::GetFolderPath('Desktop')
$shortcut = $ws.CreateShortcut("$desktop\TTS Studio.lnk")
$shortcut.TargetPath = "cmd.exe"
$shortcut.Arguments = '/c "cd /d ""C:\Users\tbank\Desktop\Live Cowork\video-automation\tts-studio"" && npx electron . && exit"'
$shortcut.WorkingDirectory = "C:\Users\tbank\Desktop\Live Cowork\video-automation\tts-studio"
$shortcut.IconLocation = "C:\Users\tbank\Desktop\Live Cowork\video-automation\tts-studio\icon.png"
$shortcut.WindowStyle = 7
$shortcut.Description = "TTS Studio - Local Neural Voice Synthesis"
$shortcut.Save()
Write-Host "Shortcut updated with new icon"
