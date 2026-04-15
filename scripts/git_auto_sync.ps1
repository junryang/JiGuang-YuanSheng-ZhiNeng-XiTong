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
        Write-Host "[WARN] 自动同步失败: $($_.Exception.Message)"
    }
}

if ($RunOnce.IsPresent) {
    Invoke-AutoSync
    exit 0
}

Write-Host "自动同步已启动。分支=$Branch，周期=${IntervalSeconds}s"
while ($true) {
    Invoke-AutoSync
    Start-Sleep -Seconds $IntervalSeconds
}
