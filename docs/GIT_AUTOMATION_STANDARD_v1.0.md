# Git 自动化标准（项目执行版）

## 目标

- 统一后续开发阶段的 Git 同步流程，降低漏提交流程风险。
- 默认遵循：`检查变更 -> 自动提交 -> 推送 main -> 输出结果`。

## 标准规则

1. 默认分支统一为 `main`。
2. 自动提交消息格式：`chore(sync): auto sync <timestamp>`。
3. 无变更时不创建提交（除非显式要求 `--allow-empty`）。
4. 同步失败不中断开发，但必须保留失败日志并重试。
5. 远程仓库创建与联通使用 `scripts/setup_github_repo.ps1`。
6. 自动同步脚本默认写入日志：`scripts/logs/git_auto_sync_yyyyMMdd.log`。
7. 可选将同步状态上报后端审计：`POST /api/v1/ops/git-sync/events`（上报失败不阻断同步）。

## 脚本清单

- `scripts/setup_github_repo.ps1`
  - 作用：创建 GitHub 仓库、绑定 `origin`、推送 `main`。
- `scripts/git_sync_once.ps1`
  - 作用：执行一次标准化同步。
- `scripts/git_auto_sync.ps1`
  - 作用：循环执行自动同步（守护模式）。

## 使用方式

```powershell
# 1) 首次创建并联通 GitHub 仓库（仓库名默认：纪光元生智能系统）
$env:GITHUB_TOKEN = "<token>"
pwsh ./scripts/setup_github_repo.ps1 -Owner <github用户名>

# 2) 单次同步
pwsh ./scripts/git_sync_once.ps1 -Branch main
# 单次同步（带推送重试与日志）
pwsh ./scripts/git_sync_once.ps1 -Branch main -PushRetryCount 3 -PushRetryDelaySeconds 5 -LogFile ./scripts/logs/git_sync_once.log
# 单次同步（失败返回非零退出码，便于外层守护判定）
pwsh ./scripts/git_sync_once.ps1 -Branch main -FailOnError
# 单次同步（可选上报后端审计）
pwsh ./scripts/git_sync_once.ps1 -Branch main -BackendAuditUrl http://127.0.0.1:8000/api/v1/ops/git-sync/events -BackendAuditEnvironment dev

# 3) 持续自动同步（每120秒）
pwsh ./scripts/git_auto_sync.ps1 -Branch main -IntervalSeconds 120
# 持续自动同步（默认保留日志并在推送失败时重试）
pwsh ./scripts/git_auto_sync.ps1 -Branch main -IntervalSeconds 120 -PushRetryCount 3 -PushRetryDelaySeconds 5
# 持续自动同步（可选上报后端审计）
pwsh ./scripts/git_auto_sync.ps1 -Branch main -IntervalSeconds 120 -BackendAuditUrl http://127.0.0.1:8000/api/v1/ops/git-sync/events -BackendAuditEnvironment dev
```

## 输出约定

- `git_sync_once.ps1` 每次执行都会输出一行 `SYNC_RESULT <json>`，字段包含：
  - `branch`
  - `status`（`success|failure|skipped`）
  - `reason`
  - `push_attempts`
  - `commit_sha`
  - `timestamp`
- `git_auto_sync.ps1` 使用 `-FailOnError` 调用单次脚本，通过退出码判断成功/失败并持续循环，不因单次失败退出。

## 建议

- 开发机常驻执行 `git_auto_sync.ps1`。
- 发布前手动执行一次 `git_sync_once.ps1` 做最终收口。
- 观察日志中是否出现 `continuous sync failures`，若出现优先检查网络与凭据有效期。
