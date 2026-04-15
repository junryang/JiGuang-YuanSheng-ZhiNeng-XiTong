param(
    [string]$Label = "daily",
    [int]$MaxBackupAgeHours = 24,
    [int]$KeepLast = 30,
    [int]$KeepDays = 14,
    [switch]$PruneDryRun
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "daily_maintenance.py"

if (-not (Test-Path $PythonScript)) {
    throw "找不到脚本: $PythonScript"
}

$argsList = @(
    $PythonScript,
    "--label", $Label,
    "--max-backup-age-hours", "$MaxBackupAgeHours",
    "--keep-last", "$KeepLast",
    "--keep-days", "$KeepDays"
)

if ($PruneDryRun) {
    $argsList += "--prune-dry-run"
}

Write-Host "Running: python $($argsList -join ' ')"
python @argsList
$exitCode = $LASTEXITCODE
if ($exitCode -ne 0) {
    throw "daily_maintenance.py 执行失败，退出码: $exitCode"
}

Write-Host "daily maintenance done."
