param(
    [string]$Branch = "main",
    [int]$IntervalSeconds = 120,
    [switch]$RunOnce
)

$ErrorActionPreference = "Stop"

function Invoke-AutoSync {
    try {
        & "$PSScriptRoot\git_sync_once.ps1" -Branch $Branch
    } catch {
        Write-Host "[WARN] Auto sync failed: $($_.Exception.Message)"
    }
}

if ($RunOnce.IsPresent) {
    Invoke-AutoSync
    exit 0
}

Write-Host "Auto sync started. branch=$Branch interval=${IntervalSeconds}s"
while ($true) {
    Invoke-AutoSync
    Start-Sleep -Seconds $IntervalSeconds
}
