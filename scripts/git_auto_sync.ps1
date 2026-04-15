param(
    [string]$Branch = "main",
    [int]$IntervalSeconds = 120,
    [switch]$RunOnce,
    [int]$PushRetryCount = 3,
    [int]$PushRetryDelaySeconds = 5,
    [string]$LogFile = "",
    [string]$BackendAuditUrl = "",
    [string]$BackendAuditEnvironment = "dev"
)

$ErrorActionPreference = "Stop"

if ($IntervalSeconds -lt 5) {
    $IntervalSeconds = 5
}

if (-not $LogFile) {
    $LogFile = Join-Path $PSScriptRoot ("logs\git_auto_sync_{0}.log" -f (Get-Date -Format "yyyyMMdd"))
}

function Write-AutoSyncLog {
    param([string]$Message)
    $dir = Split-Path -Parent $LogFile
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Add-Content -LiteralPath $LogFile -Value ("[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message)
}

function Invoke-AutoSync {
    & "$PSScriptRoot\git_sync_once.ps1" `
        -Branch $Branch `
        -PushRetryCount $PushRetryCount `
        -PushRetryDelaySeconds $PushRetryDelaySeconds `
        -LogFile $LogFile `
        -BackendAuditUrl $BackendAuditUrl `
        -BackendAuditEnvironment $BackendAuditEnvironment `
        -FailOnError
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
        Write-AutoSyncLog "Loop sync finished with exit_code=0"
        return $true
    }
    Write-AutoSyncLog "Loop sync finished with exit_code=$exitCode"
    return $false
}

if ($RunOnce.IsPresent) {
    $ok = Invoke-AutoSync
    if (-not $ok) {
        exit 1
    }
    exit 0
}

Write-Host "Auto sync started. branch=$Branch interval=${IntervalSeconds}s"
Write-AutoSyncLog "Auto sync started. branch=$Branch interval=${IntervalSeconds}s"
$failureStreak = 0
while ($true) {
    $ok = Invoke-AutoSync
    if ($ok) {
        $failureStreak = 0
    } else {
        $failureStreak += 1
        Write-Host "[WARN] Auto sync failed. streak=$failureStreak"
        Write-AutoSyncLog "Auto sync failed. streak=$failureStreak"
        if ($failureStreak -ge 3) {
            Write-AutoSyncLog "Detected continuous sync failures: count=$failureStreak"
        }
    }
    Start-Sleep -Seconds $IntervalSeconds
}
