# D3 发布当班执行 Runbook v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\D3_RELEASE_DUTY_RUNBOOK_v1.0.md`

彩排记录模板：

`d:\BaiduSyncdisk\JiGuang\docs\D3_RELEASE_REHEARSAL_RECORD_TEMPLATE_v1.0.md`

彩排记录样例：

`d:\BaiduSyncdisk\JiGuang\docs\D4_RELEASE_REHEARSAL_RECORD_SAMPLE_v1.0.md`

## 1. 使用说明

- 本文档用于 D3-08 发布窗口值班执行，按顺序打勾。
- 执行基线：`D3_STAGING_TO_PROD_RELEASE_CHECKLIST_v1.0.md`
- 任一步骤触发阻断条件，立即进入回滚流程并升级通知。

## 2. 值班编组（发布前填写）

| 角色 | 姓名 | 联系方式 | 备份人 | 状态 |
|---|---|---|---|---|
| 发布总指挥（运维） | [待填] | [待填] | [待填] | [ ] |
| 后端值班 | [待填] | [待填] | [待填] | [ ] |
| 安全值班 | [待填] | [待填] | [待填] | [ ] |
| 产品值班 | [待填] | [待填] | [待填] | [ ] |

## 3. 发布窗口信息（发布前填写）

| 字段 | 值 |
|---|---|
| 发布日期 | [YYYY-MM-DD] |
| 窗口时间 | [HH:MM-HH:MM] |
| 发布标签 | [release-xxxx] |
| backend 镜像 digest | [sha256:...] |
| frontend 包 checksum | [sha256:...] |
| 配置快照版本 | [config-xxxx] |

## 4. 执行清单（可打勾）

### A. 窗口前 60 分钟

- [ ] 值班到位，升级群已拉通
- [ ] 变更冻结已生效（非发布变更禁止合入）
- [ ] 备份任务已触发并记录任务 ID
- [ ] 基线回归通过：`python -m pytest tests/ -q --tb=short`
- [ ] Day3 门禁通过：`python -m pytest -m day3_gate -q --tb=short`

### B. 窗口前 30 分钟

- [ ] `healthz` 正常
- [ ] 关键 API 探活正常（发布/审批/项目）
- [ ] 审计摘要接口可读：`/api/v1/audit/summary`
- [ ] 观测看板阈值已确认（错误率、延迟、拒绝码）

### C. Canary 执行（10%）

- [ ] 下发 canary 版本（记录命令与版本）
- [ ] 10% 流量开启（记录开始时间）
- [ ] 观察 10-15 分钟，错误率/延迟/拒绝码无异常
- [ ] 安全确认：高风险未审批动作仍拒绝

### D. 扩流与全量

- [ ] 扩流至 50% 并观察 10 分钟
- [ ] 扩流至 100% 并观察 15 分钟
- [ ] 发布后巡检 5/15/30 分钟全部通过
- [ ] 解除冻结并发送发布完成通知

## 5. 阻断条件（命中即停止扩流）

- 5xx 错误率连续 5 分钟超阈值
- 关键链路不可用（发布、审批、项目流转）
- 策略拒绝码异常漂移（尤其审批相关拒绝码）
- 审计字段缺失或 summary 明显异常

## 6. 回滚流程（10 分钟内完成）

### 6.1 回滚命令模板

```bash
# 查看历史版本
kubectl rollout history deployment/<service> -n <namespace>

# 回滚到上一版
kubectl rollout undo deployment/<service> -n <namespace>

# 或回滚到指定 revision
kubectl rollout undo deployment/<service> -n <namespace> --to-revision=<rev>

# 等待回滚完成
kubectl rollout status deployment/<service> -n <namespace> --timeout=10m
```

### 6.2 回滚后动作

- [ ] 停止后续扩流
- [ ] 发布群广播“已回滚 + 当前状态”
- [ ] 保存现场（日志、指标截图、审计样本）
- [ ] 输出事故简报（30 分钟内）

## 7. 升级链路与 SLA

| 级别 | 触发条件 | 响应时限 | 通知对象 |
|---|---|---|---|
| L1 | 单点异常可绕过 | 15 分钟 | 值班工程师 |
| L2 | 关键链路异常 | 10 分钟 | 发布总指挥 + 后端/安全 |
| L3 | 影响发布成败 | 5 分钟 | 项目负责人 + 管理层 |

## 8. 发布纪要（窗口结束后填写）

| 项 | 内容 |
|---|---|
| 发布结果 | [成功/回滚/延期] |
| 开始时间 | [HH:MM] |
| 结束时间 | [HH:MM] |
| 关键事件 | [简述] |
| 遗留问题 | [简述] |
| 责任人 | [签名] |

## 9. 版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-15 | 首版：D3 发布当班执行 Runbook（可打勾） |
