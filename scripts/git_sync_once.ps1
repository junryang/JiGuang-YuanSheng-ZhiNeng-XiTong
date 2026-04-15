param(
    [string]$Branch = "main",
    [string]$CommitMessage = "",
    [switch]$AllowEmpty,
    [int]$PushRetryCount = 3,
    [int]$PushRetryDelaySeconds = 5,
    [string]$LogFile = "",
    [string]$BackendAuditUrl = "",
    [string]$BackendAuditEnvironment = "dev",
    [switch]$FailOnError
)

$ErrorActionPreference = "Stop"

if ($PushRetryCount -lt 1) {
    $PushRetryCount = 1
}
if ($PushRetryDelaySeconds -lt 1) {
    $PushRetryDelaySeconds = 1
}

function Write-SyncLog {
    param([string]$Message)
    if (-not $LogFile) {
        return
    }
    $dir = Split-Path -Parent $LogFile
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    Add-Content -LiteralPath $LogFile -Value ("[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message)
}

function Send-AuditEvent {
    param(
        [string]$Status,
        [string]$Message,
        [hashtable]$ExtraContext
    )
    if (-not $BackendAuditUrl) {
        return
    }
    try {
        $safeContext = @{}
        if ($null -ne $ExtraContext) {
            $safeContext = $ExtraContext
        }
        $payload = @{
            branch = $Branch
            status = $Status
            message = $Message
            source = "git_sync_once.ps1"
            environment = $BackendAuditEnvironment
            context = $safeContext
        } | ConvertTo-Json -Depth 6
        Invoke-RestMethod -Method Post -Uri $BackendAuditUrl -ContentType "application/json" -Body $payload | Out-Null
        Write-SyncLog "Audit event sent: status=$Status"
    } catch {
        Write-SyncLog "Audit event failed: $($_.Exception.Message)"
    }
}

function Emit-SyncResult {
    param(
        [string]$Status,
        [string]$Reason,
        [int]$Attempts,
        [string]$CommitSha
    )
    $result = @{
        branch = $Branch
        status = $Status
        reason = $Reason
        push_attempts = $Attempts
        commit_sha = $CommitSha
        timestamp = (Get-Date).ToUniversalTime().ToString("o")
    } | ConvertTo-Json -Compress
    Write-Host "SYNC_RESULT $result"
}

$commitSha = ""
$attemptUsed = 0

try {
    git rev-parse --is-inside-work-tree | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Current directory is not a git repository."
    }

    $status = git status --porcelain
    if (-not $status -and -not $AllowEmpty.IsPresent) {
        $msg = "No changes, skip commit and push."
        Write-Host $msg
        Write-SyncLog $msg
        Send-AuditEvent -Status "skipped" -Message $msg -ExtraContext @{ allow_empty = $AllowEmpty.IsPresent }
        Emit-SyncResult -Status "skipped" -Reason $msg -Attempts 0 -CommitSha ""
        exit 0
    }

    if (-not $CommitMessage) {
        $CommitMessage = "chore(sync): auto sync $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    }

    git branch -M $Branch
    if ($LASTEXITCODE -ne 0) {
        throw "git branch switch failed."
    }

    git add -A
    if ($LASTEXITCODE -ne 0) {
        throw "git add failed."
    }
    $stagedStatus = git diff --cached --name-only
    if (-not $stagedStatus -and -not $AllowEmpty.IsPresent) {
        $msg = "No staged changes after git add, skip commit and push."
        Write-Host $msg
        Write-SyncLog $msg
        Send-AuditEvent -Status "skipped" -Message $msg -ExtraContext @{ allow_empty = $AllowEmpty.IsPresent; stage = "post_add" }
        Emit-SyncResult -Status "skipped" -Reason $msg -Attempts 0 -CommitSha ""
        exit 0
    }
    if ($AllowEmpty.IsPresent) {
        git commit --allow-empty -m "$CommitMessage"
    } else {
        git commit -m "$CommitMessage"
    }
    if ($LASTEXITCODE -ne 0) {
        throw "git commit failed."
    }
    $commitSha = (git rev-parse --short HEAD).Trim()
    Write-SyncLog "Commit created on branch $Branch with message: $CommitMessage"

    $pushSucceeded = $false
    $lastPushError = ""
    for ($attempt = 1; $attempt -le $PushRetryCount; $attempt++) {
        $attemptUsed = $attempt
        Write-SyncLog "Push attempt $attempt/$PushRetryCount started."
        try {
            if ($env:GITHUB_TOKEN) {
                $originUrl = (git remote get-url origin).Trim()
                if (-not $originUrl) {
                    throw "origin remote is not configured."
                }
                $authUrl = $originUrl -replace '^https://', "https://x-access-token:$($env:GITHUB_TOKEN)@"
                git push $authUrl $Branch
            } else {
                git push origin $Branch
            }

            if ($LASTEXITCODE -eq 0) {
                $pushSucceeded = $true
                Write-SyncLog "Push attempt $attempt succeeded."
                break
            }
            $lastPushError = "git push exit code $LASTEXITCODE"
            Write-SyncLog "Push attempt $attempt failed: $lastPushError"
        } catch {
            $lastPushError = $_.Exception.Message
            Write-SyncLog "Push attempt $attempt failed: $lastPushError"
        }
        if ($attempt -lt $PushRetryCount) {
            Start-Sleep -Seconds $PushRetryDelaySeconds
        }
    }

    if (-not $pushSucceeded) {
        $reason = "git push failed after retries: $lastPushError"
        Write-SyncLog $reason
        Send-AuditEvent -Status "failure" -Message $reason -ExtraContext @{ push_retry_count = $PushRetryCount; commit_sha = $commitSha }
        Emit-SyncResult -Status "failure" -Reason $reason -Attempts $attemptUsed -CommitSha $commitSha
        if ($FailOnError.IsPresent) {
            exit 1
        }
        exit 0
    }

    $okMsg = "Sync completed: $Branch"
    Write-Host $okMsg
    Write-SyncLog "Sync completed: branch=$Branch commit=$commitSha"
    Send-AuditEvent -Status "success" -Message $okMsg -ExtraContext @{ push_retry_count = $attemptUsed; commit_sha = $commitSha }
    Emit-SyncResult -Status "success" -Reason $okMsg -Attempts $attemptUsed -CommitSha $commitSha
    exit 0
} catch {
    $reason = $_.Exception.Message
    Write-SyncLog "Sync failed before push loop: $reason"
    Send-AuditEvent -Status "failure" -Message $reason -ExtraContext @{ stage = "pre_push"; commit_sha = $commitSha }
    Emit-SyncResult -Status "failure" -Reason $reason -Attempts $attemptUsed -CommitSha $commitSha
    if ($FailOnError.IsPresent) {
        exit 1
    }
    exit 0
}
