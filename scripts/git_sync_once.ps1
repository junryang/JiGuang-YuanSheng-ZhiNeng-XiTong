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
if ($AllowEmpty.IsPresent) {
    git commit --allow-empty -m "$CommitMessage"
} else {
    git commit -m "$CommitMessage"
}

git branch -M $Branch
if ($env:GITHUB_TOKEN) {
    git -c "http.https://github.com/.extraheader=AUTHORIZATION: bearer $($env:GITHUB_TOKEN)" push origin $Branch
} else {
    git push origin $Branch
}

Write-Host "Sync completed: $Branch"
