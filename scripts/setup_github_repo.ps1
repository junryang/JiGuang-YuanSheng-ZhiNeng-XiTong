param(
    [Parameter(Mandatory = $true)]
    [string]$Owner,

    [string]$Repo = "JiGuang-YuanSheng-ZhiNeng-XiTong",

    [string]$DefaultBranch = "main",
    [switch]$Private,
    [switch]$SkipPush
)

$ErrorActionPreference = "Stop"

if (-not $env:GITHUB_TOKEN) {
    throw "Please set GITHUB_TOKEN first (repo scope required)."
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

Write-Host ">> Check repository: $Owner/$Repo"
$repoExists = $false
try {
    Invoke-RestMethod -Method Get -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $headers | Out-Null
    $repoExists = $true
} catch {
    $repoExists = $false
}

if (-not $repoExists) {
    Write-Host ">> Create repository: $Owner/$Repo"
    Invoke-RestMethod -Method Post -Uri "https://api.github.com/user/repos" -Headers $headers -Body $repoBody -ContentType "application/json" | Out-Null
}

$remoteUrl = "https://github.com/$Owner/$Repo.git"
Write-Host ">> Configure local git remote"
git rev-parse --is-inside-work-tree | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Current directory is not a git repository. Run git init first."
}

$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0 -and $existingRemote) {
    git remote set-url origin $remoteUrl
} else {
    git remote add origin $remoteUrl
}

Write-Host ">> Push to remote and set default branch"
git branch -M $DefaultBranch
if (-not $SkipPush.IsPresent) {
    $hasCommit = $true
    try {
        git rev-parse --verify HEAD | Out-Null
    } catch {
        $hasCommit = $false
    }
    if (-not $hasCommit) {
        Write-Host ">> No commit found, create initial commit"
        git add -A
        git commit -m "chore: initialize repository for GitHub sync"
    }
    git push -u origin $DefaultBranch
}

Write-Host ">> Set default branch: $DefaultBranch"
$patchBody = @{ default_branch = $DefaultBranch } | ConvertTo-Json
Invoke-RestMethod -Method Patch -Uri "https://api.github.com/repos/$Owner/$Repo" -Headers $headers -Body $patchBody -ContentType "application/json" | Out-Null

Write-Host "Done: https://github.com/$Owner/$Repo"
