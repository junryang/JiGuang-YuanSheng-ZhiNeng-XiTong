# Day3 策略门禁回归报告 v1.1

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\DAY3_POLICY_GATE_REGRESSION_REPORT_v1.0.md`

管理层速览摘要：

`d:\BaiduSyncdisk\JiGuang\docs\DAY3_POLICY_GATE_EXEC_SUMMARY_v1.0.md`

## 一、目标与范围

本报告对应 Day3 任务单中的 D3-07（staging 全量回归：功能 + 策略 + 安全），聚焦策略关键链路门禁可用性与可观测性。

覆盖对象：

- 高风险发布门禁：`/api/v1/contents/publish`
- 策略评估入口：`/api/v1/policy/evaluate`
- 主脑工具编排门禁：`/api/v1/orchestration/plans`
- 审批链关键动作：`submit / approve / reject`
- 审计一致性：`/api/v1/audit/events` 与 `/api/v1/audit/summary`

## 二、回归入口

核心矩阵测试文件：

- `backend/tests/test_policy_gate_matrix.py`

关联回归文件：

- `backend/tests/test_api_smoke.py`
- `backend/tests/test_ui_pages_smoke.py`

## 三、门禁矩阵覆盖摘要

截至本版本，`test_policy_gate_matrix.py` 覆盖 33 条矩阵与一致性用例，包含：

1. 发布门禁矩阵（环境/降级/审批/law）
2. 策略评估矩阵（CEO-POLICY-13 / 14）
3. 编排门禁矩阵（optional tools + strict law bundle）
4. 审批链动作矩阵（提交、重复提交、错级审批、正确审批、驳回）
5. 审计事件与摘要一致性矩阵（过滤组合交叉）

满足 Day3 强制门禁中“24 条策略用例通过率 >= 95%”的覆盖规模要求。

## 四、执行命令与结果

### 1) 策略矩阵专项

命令：

`python -m pytest tests/test_policy_gate_matrix.py -q --tb=short`

或使用统一标记：

`python -m pytest -m day3_gate -q --tb=short`

结果：

- `33 passed`

### 2) 全量回归

命令：

`python -m pytest tests/ -q --tb=short`

结果：

- `191 passed`（用时 `194.42s`，exit_code=0）

### 3) D3-05 安全抽测专项

专项报告：

- `docs/DAY3_SECURITY_APPROVAL_SAMPLING_REPORT_v1.0.md`

结论：

- 高风险动作在 `staging/prod` 未审批均被拒绝（通过率 `100%`）

## 五、关键校验结论

- 策略拒绝码可机读：`error_code` 在核心拒绝场景均可断言
- 审计结构统一：事件包含 `policy_id / environment / reason / reason_code / context`
- 看板字段对齐：审计摘要包含 `trend / top_reasons / total_allowed / total_denied / allowed_rate / denied_rate`
- 过滤一致性：`events` 与 `summary` 在同类过滤维度下统计结果对齐

## 六、剩余风险与建议

剩余风险：

- 目前矩阵主要覆盖 D03 相关关键链路，尚未扩展到更多跨域业务动作（如营销发布全路径、第三方工具链异常分支）

建议：

1. 持续维护 `DAY3_POLICY_GATE_MATRIX_CASES_v1.0.yaml`，新增场景优先改配置而非改测试代码
2. 在 CI 中将 `test_policy_gate_matrix.py` 作为门禁必跑项
3. 下一阶段增加“异常网络/超时/并发冲突”场景，补齐稳定性维度

## 七、本轮发现问题与修复

1. 项目 ID 生成溢出问题

- 现象：项目编号达到 `1000` 后，项目 ID 正则仍按 3 位匹配，导致重复 ID，进而引发审批/进度相关链路异常。
- 修复：将项目 ID 提取正则从 `\d{3}` 扩展为 `\d{3,}`，兼容 4 位及以上序号。
- 影响：消除大规模回归下的 ID 冲突，恢复审批链与进度统计稳定性。

2. 委托列表测试分页稳定性问题

- 现象：当历史委托数据增多时，默认 `limit=100` 可能查不到刚创建记录，导致偶发断言失败。
- 修复：测试查询提升为 `limit=500`，避免受历史数据量影响。
- 影响：委托链路回归稳定性提升，减少非功能性波动。

## 八、版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-15 | 首版：沉淀 Day3 策略门禁回归覆盖与结果 |
| v1.1 | 2026-04-15 | 增补配置化矩阵、稳定性修复记录与最新通过数 |

