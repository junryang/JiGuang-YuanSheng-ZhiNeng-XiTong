# 自用开发工作流 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\SELF_HOSTED_DEV_WORKFLOW_v1.0.md`

## 1. 目标

适用于“超级个体自用、无需上线”的开发模式，核心目标是：

- 本地功能持续可用
- 改动可回滚
- 数据不丢失
- 调试成本低

最小入口：

- `docs/SOLO_DEV_MINIMAL_PACK_v1.0.md`

## 2. 工作模式

- 单环境：`dev/local`
- 单人决策：无需 Go/No-Go 审批流
- 轻量门禁：保留测试回归与数据备份，不做发布值班流程

## 3. 每日开发最小闭环（建议 5-15 分钟）

1. **启动前检查**
   - 确认工作目录与依赖正常
   - 快速查看最近改动文件

2. **编码后快速回归**
   - 运行目标测试（受影响模块）
   - 至少执行一次核心冒烟回归：
     - `python -m pytest tests/test_api_smoke.py -q --tb=short`

3. **里程碑快照**
   - 记录本次变更目标、结果、遗留事项
   - 重要改动前后备份 `backend/data/state.json`

## 4. 推荐命令集（本地）

```bash
# 每日一键维护（健康检查 + 备份 + 清理）
python backend/scripts/daily_maintenance.py --label daily --prune-dry-run

# 1) 快速冒烟
python -m pytest tests/test_api_smoke.py -q --tb=short

# 2) Day3策略门禁（如改到策略逻辑）
python -m pytest -m day3_gate -q --tb=short

# 3) 全量回归（阶段性执行）
python -m pytest tests/ -q --tb=short
```

## 5. 数据安全与恢复

- 关键数据文件：`backend/data/state.json`
- 建议策略：
  - 每次大改前备份一次
  - 每日结束备份一次
- 恢复原则：
  - 先保留故障现场副本
  - 再回滚到最近可用备份

可执行脚本（已提供）：

```bash
# 本地 state 健康检查（建议每日一次）
python backend/scripts/check_state_health.py --max-backup-age-hours 24

# 备份 state.json（输出备份文件路径）
python backend/scripts/backup_state.py --label before-big-change

# 查看最近备份（默认展示最新20条）
python backend/scripts/list_backups.py --limit 20

# 恢复到最新备份，并保留当前现场
python backend/scripts/restore_state.py --preserve-current

# 恢复到指定备份文件
python backend/scripts/restore_state.py --backup "backend/data/backups/state-20260415-200000.json" --preserve-current

# 清理旧备份（先预演，再执行）
python backend/scripts/prune_backups.py --keep-last 30 --keep-days 14 --dry-run
python backend/scripts/prune_backups.py --keep-last 30 --keep-days 14

# 一键日常维护（可替代上面多条命令）
python backend/scripts/daily_maintenance.py --label daily --max-backup-age-hours 24 --keep-last 30 --keep-days 14
```

Windows PowerShell 可用：

```powershell
.\backend\scripts\daily_maintenance.ps1 -Label daily -PruneDryRun
```

## 6. 故障自救顺序

1. 定位范围（最近改动 -> 受影响接口 -> 对应测试）
2. 跑最小失败用例复现
3. 修复后先跑受影响测试，再跑冒烟
4. 必要时回滚数据文件到上一个备份点

## 7. 文档与计划策略

- 发布相关文档保留为归档参考，不作为必做项
- 后续新增文档优先聚焦：
  - 本地调试效率
  - 失败恢复效率
  - 功能自测清单

## 8. 版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-15 | 首版：自用开发工作流（无需上线） |
