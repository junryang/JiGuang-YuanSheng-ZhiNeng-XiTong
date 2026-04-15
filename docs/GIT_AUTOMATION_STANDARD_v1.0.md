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

# 3) 持续自动同步（每120秒）
pwsh ./scripts/git_auto_sync.ps1 -Branch main -IntervalSeconds 120
```

## 建议

- 开发机常驻执行 `git_auto_sync.ps1`。
- 发布前手动执行一次 `git_sync_once.ps1` 做最终收口。
