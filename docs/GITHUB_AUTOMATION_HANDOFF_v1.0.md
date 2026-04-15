# GitHub 仓库与自动化落地说明

## 目标

- 在无 `gh` CLI 的 Windows 环境下，仍可自动创建并联通 GitHub 远程仓库。
- 确保后端 CI 在 `main` 推送、PR 与手动触发时稳定执行。

## 本次已落地项

- 新增仓库级忽略文件：`.gitignore`
- 增强 CI：`.github/workflows/backend-ci.yml`
  - 仅对 `main` 分支 push 触发
  - 保留 PR 触发
  - 新增 `workflow_dispatch`
  - 新增 `concurrency` 防并发重复跑
- 新增自动化脚本：`scripts/setup_github_repo.ps1`
  - 基于 `GITHUB_TOKEN` + GitHub REST API 自动创建仓库
  - 自动配置 `origin`
  - 自动推送并设置默认分支

## 执行前提

1. 本机已安装 `git`
2. 已设置环境变量 `GITHUB_TOKEN`（至少 `repo` 权限）
3. 当前目录为 git 仓库，且已至少有一次提交

## 一键联通命令

```powershell
$env:GITHUB_TOKEN="你的token"
pwsh ./scripts/setup_github_repo.ps1 -Owner <github用户名> -Repo <仓库名> -DefaultBranch main
```

如需私有仓库：

```powershell
pwsh ./scripts/setup_github_repo.ps1 -Owner <github用户名> -Repo <仓库名> -DefaultBranch main -Private
```

## 验证项

- `git remote -v` 显示 `origin` 指向目标仓库
- 访问 GitHub 仓库页面可见推送代码
- GitHub Actions 页面可见 `Backend CI` 工作流，并可手动触发一次成功运行
