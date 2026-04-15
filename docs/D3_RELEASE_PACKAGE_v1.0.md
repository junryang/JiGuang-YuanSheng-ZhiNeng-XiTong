# D3 本地稳定性执行包 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\D3_RELEASE_PACKAGE_v1.0.md`

## 1. 目标

提供本地开发“一页总入口”，让个人开发按固定顺序完成 D3-08 稳定性执行、留痕与收口，减少跨文档跳转成本。

最小入口：

- `docs/SOLO_DEV_MINIMAL_PACK_v1.0.md`

## 2. 文档清单（按使用顺序）

1. 稳定性清单草案（策略层）  
   `docs/D3_STAGING_TO_PROD_RELEASE_CHECKLIST_v1.0.md`
2. 本地执行 Runbook（执行层）  
   `docs/D3_RELEASE_DUTY_RUNBOOK_v1.0.md`
3. 彩排记录模板（留痕层）  
   `docs/D3_RELEASE_REHEARSAL_RECORD_TEMPLATE_v1.0.md`
4. 彩排记录样例（参考层）  
   `docs/D4_RELEASE_REHEARSAL_RECORD_SAMPLE_v1.0.md`
5. 正式发布纪要模板（关窗输出）  
   `docs/D3_RELEASE_MEMO_TEMPLATE_v1.0.md`
6. 正式发布纪要样例（10分钟出稿参考）  
   `docs/D5_RELEASE_MEMO_SAMPLE_v1.0.md`
7. Go/No-Go 评审纪要模板（发布前决策）  
   `docs/D5_GO_NO_GO_REVIEW_MEMO_TEMPLATE_v1.0.md`
8. Go/No-Go 评审纪要样例（5分钟出稿参考）  
   `docs/D5_GO_NO_GO_REVIEW_MEMO_SAMPLE_v1.0.md`
9. 发布窗口值班排班表模板（主备与交接）  
   `docs/D5_RELEASE_DUTY_SCHEDULE_TEMPLATE_v1.0.md`
10. 发布窗口值班排班表样例（复制即用）  
   `docs/D5_RELEASE_DUTY_SCHEDULE_SAMPLE_v1.0.md`
11. 风险收口单（决策层）  
   `docs/DAY3_RISK_CLOSURE_LIST_v1.0.md`
12. 安全抽测报告（门禁证明）  
   `docs/DAY3_SECURITY_APPROVAL_SAMPLING_REPORT_v1.0.md`
13. 策略门禁回归报告（测试证明）  
   `docs/DAY3_POLICY_GATE_REGRESSION_REPORT_v1.0.md`

## 3. 执行顺序（本地版）

### Step A：开始开发前

- 确认本地环境可用（依赖、数据文件、最近改动）
- 记录本轮目标（可选使用 Go/No-Go 模板做决策留痕）
- 执行门禁回归：
  - `python -m pytest tests/ -q --tb=short`
  - `python -m pytest -m day3_gate -q --tb=short`
- 记录 Go/No-Go 决议

### Step B：改动完成后

- 完成数据备份与版本快照登记
- 完成健康检查与关键接口探活
- 在 Runbook 中勾选本轮执行检查项

### Step C：本地验证

- 先跑受影响测试，再跑冒烟，再按需全量
- 观察错误率、延迟、拒绝码、审计一致性
- 发现阻断条件立即进入回滚/恢复流程

### Step D：收尾与归档

- 完成一次收尾巡检
- 填写演练/开发记录，明确遗留行动项与责任人
- 产出本轮开发纪要（可复用发布纪要模板）

## 4. 角色责任矩阵（单人自用版）

| 任务 | 开发者（你） |
|---|---|
| 本轮目标确认 | A/R |
| 门禁回归确认 | A/R |
| 异常处置 | A/R |
| 回滚决策与触发 | A/R |
| 本轮结论归档 | A/R |

## 5. 门禁与阻断（摘要）

- 门禁必须满足：
  - 全量回归通过
  - `day3_gate` 通过
  - 安全抽测结论有效（高风险动作未审批应被拒绝）
- 阻断触发即停止扩流：
  - 5xx 错误率超阈值
  - 关键链路不可用（发布/审批/项目）
  - 拒绝码异常漂移
  - 审计统计不一致

## 6. 回滚入口（摘要）

```bash
kubectl rollout history deployment/<service> -n <namespace>
kubectl rollout undo deployment/<service> -n <namespace>
kubectl rollout status deployment/<service> -n <namespace> --timeout=10m
```

## 7. 本轮输出物（收尾前建议齐）

- [ ] Runbook 勾选完成
- [ ] 演练/发布记录已归档
- [ ] 本轮纪要（结果、时间、异常、行动项）已记录
- [ ] 风险收口单状态已更新

## 8. 版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-15 | 首版：D3 发布窗口最终包总入口 |
| v1.1 | 2026-04-15 | 调整为单人自用本地稳定性执行包 |
