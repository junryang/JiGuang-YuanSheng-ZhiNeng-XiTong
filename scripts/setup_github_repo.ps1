param(
    [Parameter(Mandatory = $true)]
    [string]$Owner,

    [string]$Repo = "纪光元生智能系统",

    [string]$DefaultBranch = "main",
    [switch]$Private,
    [switch]$SkipPush
)

$ErrorActionPreference = "Stop"

if (-not $env:GITHUB_TOKEN) {
    throw "请先设置环境变量 GITHUB_TOKEN（需具备 repo 权限）。"
}

$headers = @{
    Authorization = "Bearer $($env:GITHUB_TOKEN)"
    Accept        = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$visibility = if ($Private.IsPresent) { $true } else { $false }
$repoBody = @{
    name    = $Repo
    private = $visibility
    auto_init = $false
} | ConvertTo-Json

Write-Host ">> 检查仓库是否存在: $Owner/$Repo"
$repoExists = $false
try {
    Invoke-RestMethod -Method Get -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $headers | Out-Null
    $repoExists = $true
} catch {
    $repoExists = $false
}

if (-not $repoExists) {
    Write-Host ">> 创建仓库: $Owner/$Repo"
    Invoke-RestMethod -Method Post -Uri "https://api.github.com/user/repos" -Headers $headers -Body $repoBody -ContentType "application/json" | Out-Null
}

$remoteUrl = "https://github.com/$Owner/$Repo.git"
Write-Host ">> 配置本地 git remote"
git rev-parse --is-inside-work-tree | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "当前目录不是 git 仓库，请先执行 git init。"
}

$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0 -and $existingRemote) {
    git remote set-url origin $remoteUrl
} else {
    git remote add origin $remoteUrl
}

Write-Host ">> 推送到远程并设置默认分支"
git branch -M $DefaultBranch
if (-not $SkipPush.IsPresent) {
    $hasCommit = $true
    try {
        git rev-parse --verify HEAD | Out-Null
    } catch {
        $hasCommit = $false
    }
    if (-not $hasCommit) {
        Write-Host ">> 检测到暂无提交，自动创建初始提交"
        git add -A
        git commit -m "chore: initialize repository for GitHub sync"
    }
    git push -u origin $DefaultBranch
}

Write-Host ">> 设置仓库默认分支: $DefaultBranch"
$patchBody = @{ default_branch = $DefaultBranch } | ConvertTo-Json
Invoke-RestMethod -Method Patch -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $headers -Body $patchBody -ContentType "application/json" | Out-Null

Write-Host "完成: https://github.com/$Owner/$Repo"
