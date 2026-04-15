param(
    [string]$Branch = "main",
    [string]$CommitMessage = "",
    [switch]$AllowEmpty
)

$ErrorActionPreference = "Stop"

git rev-parse --is-inside-work-tree | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Current directory is not a git repository."
}

$status = git status --porcelain
if (-not $status -and -not $AllowEmpty.IsPresent) {
    Write-Host "No changes, skip commit and push."
    exit 0
}

if (-not $CommitMessage) {
    $CommitMessage = "chore(sync): auto sync $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

git add -A
if ($LASTEXITCODE -ne 0) {
    throw "git add failed."
}
if ($AllowEmpty.IsPresent) {
    git commit --allow-empty -m "$CommitMessage"
} else {
    git commit -m "$CommitMessage"
}
if ($LASTEXITCODE -ne 0) {
    throw "git commit failed."
}

git branch -M $Branch
if ($LASTEXITCODE -ne 0) {
    throw "git branch switch failed."
}
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
if ($LASTEXITCODE -ne 0) {
    throw "git push failed."
}

Write-Host "Sync completed: $Branch"
