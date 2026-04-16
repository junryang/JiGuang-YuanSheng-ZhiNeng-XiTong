# Day3 D3-05 安全抽测报告 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\DAY3_SECURITY_APPROVAL_SAMPLING_REPORT_v1.0.md`

## 1. 目标

对应 `DAY3_EXECUTION_TASKS_v1.0.md` 的 D3-05：对高风险动作审批链路进行抽测，验证“未审批动作在 staging/prod 全部拒绝”。

## 2. 抽测范围

- 高风险发布：`POST /api/v1/contents/publish`
- 营销高风险发布：`POST /api/v1/marketing/contents/{content_id}/publish`
- 主脑可选工具编排：`POST /api/v1/orchestration/plans`（`use_optional_tools=true`）
- 环境范围：`staging`、`prod`

## 3. 抽测用例与结果

用例数据源：

- `docs/DAY3_POLICY_GATE_MATRIX_CASES_v1.0.yaml` -> `security_sampling_cases`

自动化执行：

- `backend/tests/test_policy_gate_matrix.py::test_security_high_risk_approval_sampling_matrix`

结果：

- 用例数：4
- 通过：4
- 失败：0
- 通过率：100%

关键断言：

- staging 未审批发布 -> `403` + `STAGING_APPROVAL_REQUIRED`
- prod 未审批发布 -> `403` + `PROD_APPROVAL_REQUIRED`
- staging/prod 可选工具链未审批 -> `403` + `OPTIONAL_TOOLS_APPROVAL_REQUIRED`

## 4. 本轮修复

为满足 D3-05 验收口径，补齐了 staging 高风险发布审批门禁：

- `backend/app/api/routes.py`：`/contents/publish` 从“仅 prod 审批”升级为“staging/prod 审批”
- `backend/app/api/marketing_router.py`：营销发布门禁同步升级
- `backend/tests/test_api_smoke.py`：新增 `test_staging_publish_requires_approval`
- `backend/tests/test_marketing_api.py`：新增 `test_marketing_publish_staging_requires_approval`

## 5. 验证记录

执行命令：

- `python -m pytest tests/test_policy_gate_matrix.py tests/test_api_smoke.py tests/test_marketing_api.py -q --tb=short`
- `python -m pytest tests/ -q --tb=short`

执行结果：

- 影响范围回归：`89 passed in 164.67s`
- 全量回归：`191 passed in 194.42s`

## 6. 结论

D3-05 抽测要求已满足：高风险动作在 staging/prod 环境下未审批均被拒绝，且拒绝码可机读、可统计，可继续进入 D3-07 / D3-08 收口阶段。
