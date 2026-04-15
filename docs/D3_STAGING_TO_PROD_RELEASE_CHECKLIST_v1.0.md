# D3-08 staging→prod 发布清单草案 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\D3_STAGING_TO_PROD_RELEASE_CHECKLIST_v1.0.md`

当班执行版：

`d:\BaiduSyncdisk\JiGuang\docs\D3_RELEASE_DUTY_RUNBOOK_v1.0.md`

## Goal

形成可执行的 staging→prod 发布清单，覆盖版本锁定、门禁、值班、回滚演练入口与发布后观测，满足 `DAY3_EXECUTION_TASKS_v1.0.md` 的 D3-08 验收要求。

## Key Constraints

- 仅允许通过已验证的发布工件进入 prod，禁止“本地临时构建直推”
- 发布前必须完成策略门禁回归与安全抽测（`day3_gate`）
- 变更窗口内必须有值班与升级路径（运维/后端/安全/产品）
- 必须保留可在 10 分钟内触发的回滚入口

## Implementation Plan

1. **版本锁定（Release Freeze）**
   - 锁定分支：`main` 仅允许 Release Manager 合入
   - 锁定版本：记录发布标签（示例：`release-2026-04-15-r1`）
   - 锁定工件：记录 backend 镜像 digest 与前端静态包 checksum
   - 锁定配置：记录 `ceo_policy.engine.yaml`、环境变量快照版本号

2. **发布前门禁检查（Go/No-Go）**
   - 回归：`python -m pytest tests/ -q --tb=short` 必须通过
   - Day3 专项：`python -m pytest -m day3_gate -q --tb=short` 必须通过
   - 文档一致性：风险收口单、抽测报告、回归报告齐全
   - 安全确认：高风险动作未审批在 staging/prod 全拒绝
   - 审计确认：`policy/env/reason_code/context` 字段完整

3. **发布执行（staging→prod）**
   - Step 1: 变更冻结生效（停止非发布变更合并）
   - Step 2: 备份（配置快照 + 数据备份任务触发）
   - Step 3: canary 发布（10% 流量，观察 10~15 分钟）
   - Step 4: 指标达标后提升到 50%，再提升到 100%
   - Step 5: 解除冻结并记录发布纪要

4. **值班与职责**
   - 发布总指挥（运维主管）：节奏控制、Go/No-Go 最终确认
   - 后端值班：API 与策略门禁异常处置
   - 安全值班：审批链路与审计异常处置
   - 产品值班：业务回归口径确认与回退决策参与
   - 升级路径：值班群 -> 发布总指挥 -> 负责人（15 分钟内响应）

5. **回滚预案（必须演练）**
   - 回滚入口：`kubectl rollout undo deployment/<service> -n <namespace>`
   - 回滚触发条件（任一满足即触发）：
     - 5xx 错误率连续 5 分钟超阈值
     - 策略拒绝码异常漂移或高风险动作错误放行
     - 关键业务链路不可用（发布、审批、项目流转）
   - 回滚目标：恢复到上一个已验证版本，10 分钟内完成
   - 回滚后动作：冻结新发布、保存现场、输出事故简报

6. **发布后验证（Post-Release）**
   - 5/15/30 分钟三次巡检：健康检查、关键 API、审计统计
   - 核验项：
     - `/healthz` 正常
     - 高风险发布门禁（staging/prod）行为符合预期
     - 审计 summary 指标连续可读取
   - 24 小时观察：无 P0/P1 告警后关闭发布窗口

## Validation

- 验收勾选清单：
  - [ ] 已完成版本锁定与工件登记
  - [ ] 全量回归通过
  - [ ] `day3_gate` 专项通过
  - [ ] 值班排班与升级路径已确认
  - [ ] 回滚演练入口可用且已记录
  - [ ] 发布后 30 分钟巡检通过

- 建议执行命令：
  - `python -m pytest tests/ -q --tb=short`
  - `python -m pytest -m day3_gate -q --tb=short`

## Risks and Fallbacks

- 风险：发布窗口内出现策略行为与 staging 不一致  
  兜底：立即停止扩流，回滚到稳定版本并启用审计排查
- 风险：同步盘/文件占用导致本地验证抖动  
  兜底：按串行重跑策略复验，并以 CI 结果为准
- 风险：值班响应延迟  
  兜底：升级到发布总指挥，执行预设回滚阈值策略

## 版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-15 | 首版：D3-08 staging→prod 发布清单草案 |
