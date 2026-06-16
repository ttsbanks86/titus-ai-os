# Keeps this Windows session awake during an unattended AI OS build.
# Non-permanent: close this PowerShell process to stop.
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class SleepUtil {
  [DllImport("kernel32.dll", CharSet = CharSet.Auto, SetLastError = true)]
  public static extern uint SetThreadExecutionState(uint esFlags);
}
"@
$ES_CONTINUOUS = [uint32]0x80000000
$ES_SYSTEM_REQUIRED = [uint32]0x00000001
$ES_AWAYMODE_REQUIRED = [uint32]0x00000040
while ($true) {
  [SleepUtil]::SetThreadExecutionState($ES_CONTINUOUS -bor $ES_SYSTEM_REQUIRED -bor $ES_AWAYMODE_REQUIRED) | Out-Null
  Start-Sleep -Seconds 55
}
