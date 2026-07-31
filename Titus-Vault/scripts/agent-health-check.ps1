# Agent Health Check Script
# Titus AI OS - Phase 1

param(
    [switch]$Verbose
)

# Agent list
$agents = @(
    @{ Name = "CEO Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") },
    @{ Name = "Developer Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") },
    @{ Name = "QA Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") },
    @{ Name = "Security Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") },
    @{ Name = "Research Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") },
    @{ Name = "Documentation Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") },
    @{ Name = "DevOps Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") },
    @{ Name = "Knowledge Agent"; Status = "Active"; LastCheck = (Get-Date).ToString("yyyy-MM-dd HH:mm") }
)

# Display header
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Agent Health Status" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check each agent
$healthyCount = 0
$totalCount = $agents.Count

foreach ($agent in $agents) {
    # Simulate health check (in real implementation, this would check actual agent status)
    $isHealthy = $agent.Status -eq "Active"
    
    if ($isHealthy) {
        Write-Host "  [OK] " -ForegroundColor Green -NoNewline
        $healthyCount++
    } else {
        Write-Host "  [!!] " -ForegroundColor Red -NoNewline
    }
    
    Write-Host "$($agent.Name): " -NoNewline
    Write-Host "$($agent.Status)" -ForegroundColor $(if ($isHealthy) { "Green" } else { "Red" })
    
    if ($Verbose) {
        Write-Host "        Last Check: $($agent.LastCheck)" -ForegroundColor Gray
    }
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Total Agents: $totalCount" -ForegroundColor White
Write-Host "  Healthy: $healthyCount" -ForegroundColor Green
Write-Host "  Unhealthy: $($totalCount - $healthyCount)" -ForegroundColor $(if ($healthyCount -eq $totalCount) { "Green" } else { "Red" })
Write-Host "  Check Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray

# Overall status
if ($healthyCount -eq $totalCount) {
    Write-Host "`n  All agents healthy`n" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n  Some agents unhealthy`n" -ForegroundColor Red
    exit 1
}
