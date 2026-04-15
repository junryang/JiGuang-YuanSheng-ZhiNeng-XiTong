param(
    [string]$Branch = "main",
    [string]$CommitMessage = "",
    [switch]$AllowEmpty
)

$ErrorActionPreference = "Stop"

git rev-parse --is-inside-work-tree | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "当前目录不是 git 仓库。"
}

$status = git status --porcelain
if (-not $status -and -not $AllowEmpty.IsPresent) {
    Write-Host "无变更，跳过提交与推送。"
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
git push origin $Branch

Write-Host "同步完成：$Branch"
