# 项目交接包（2026-04-15）

## 本轮完成

1. 远程仓库与同步自动化已落地  
   - 远程仓库：`https://github.com/junryang/JiGuang-YuanSheng-ZhiNeng-XiTong`
   - 分支：`main` 已与 `origin/main` 对齐
   - 自动化脚本：
     - `scripts/setup_github_repo.ps1`
     - `scripts/git_sync_once.ps1`
     - `scripts/git_auto_sync.ps1`
   - 标准文档：`docs/GIT_AUTOMATION_STANDARD_v1.0.md`

2. 项目主线增强：项目执行风险自动提醒闭环  
   - 文件：`backend/app/api/routes.py`
   - 能力：
     - `GET /api/v1/projects/{project_id}/progress` 返回 `risk_alert_triggered`
     - 当 `risk_summary.risk_level=high` 时，自动写入讨论提醒（`[PROJECT_RISK_ALERT]`）
     - 同时写入审计事件 `project_risk_alert`
     - 最近讨论存在同类提醒时自动去重，避免刷屏

3. 测试补齐  
   - 文件：`backend/tests/test_progress_gantt.py`
   - 新增/增强：
     - 高风险触发提醒
     - 重复访问不重复提醒
     - 审计事件可检索

## 本轮验证结果

- `python -m pytest tests/test_progress_gantt.py -q --tb=short`  
  - 结果：`6 passed`
- `python -m pytest tests/test_api_smoke.py tests/test_project_discussion.py -q --tb=short`  
  - 结果：`32 passed`
- 历史全量回归基线：`165 passed`

## 当前工作区未提交变更

- `backend/app/api/routes.py`
- `backend/tests/test_progress_gantt.py`
- `backend/data/state.json`（运行测试引起的数据文件变化，提交前建议按发布策略决定是否纳入）

## 下一步建议（按项目计划）

1. （已完成）项目详情聚合接口的风险透出（前端减少拼装请求）。
2. （已完成）将 `project_risk_alert` 接入策略门控/阈值配置（YAML 可配置化）。
3. （已完成）对提醒机制增加时间窗口去重（例如 30 分钟内只触发一次）。
4. （已完成）在 CI 中加入针对风险提醒逻辑的最小回归集合（`backend-ci.yml` 独立步骤）。

## 本轮调整记录（持续追加）

1. 新增后端分析报告接口（按项目计划 v1.1 主线）
   - 接口：`GET /api/v1/analytics/reports`
   - 文件：`backend/app/api/routes.py`
   - 能力：
     - `report_type=project_execution`：聚合项目进度、风险分布、高风险项目列表
     - `report_type=ops_risk`：聚合近 N 天 `project_risk_alert` 与 `git_sync_status` 风险信号
     - 非法 `report_type` 返回 `INVALID_REPORT_TYPE`

2. 补充分析报告接口最小回归
   - 文件：`backend/tests/test_api_smoke.py`
   - 新增测试：
     - `test_analytics_reports_project_execution_and_ops_risk`
     - 覆盖 project_execution / ops_risk / 非法参数场景

3. 新增审计日志查询接口（按项目计划 v1.1 主线）
   - 接口：`GET /api/v1/audit/logs`
   - 文件：`backend/app/api/routes.py`
   - 能力：
     - 支持 `event_type_prefix` / `policy_id` / `environment` 过滤
     - 支持 `limit` / `offset` 分页
     - 返回结构：`items/total/limit/offset`

4. 补充审计日志接口最小回归
   - 文件：`backend/tests/test_api_smoke.py`
   - 新增测试：
     - `test_audit_logs_endpoint_with_pagination`

5. 新增 Webhook 创建接口（按项目计划 v1.1 主线）
   - 接口：`POST /api/v1/webhooks`
   - 文件：`backend/app/api/routes.py`、`backend/app/core/store.py`
   - 能力：
     - 支持 webhook 创建（name/url/events/enabled/secret）
     - URL 基础校验（仅允许 `http://` 或 `https://`，非法返回 `INVALID_WEBHOOK_URL`）
     - 持久化保存到 `webhooks` 集合

6. 补充 Webhook 接口最小回归
   - 文件：`backend/tests/test_api_smoke.py`
   - 新增测试：
     - `test_create_webhook_endpoint`

7. 新增智能体自我反思触发接口（按项目计划 v1.1 主线）
   - 接口：`POST /api/v1/agents/{id}/reflect`
   - 文件：`backend/app/api/routes.py`
   - 能力：
     - 受策略门禁（`CEO-POLICY-11`）控制
     - 生成 `[SELF_REFLECTION]` 反思内容并写入工作记忆
     - 记录审计事件 `agent_reflect_triggered`

8. 补充自我反思接口最小回归
   - 文件：`backend/tests/test_api_smoke.py`
   - 新增测试：
     - `test_agent_reflect_endpoint`

9. 新增智能体批量创建接口（按项目计划 v1.1 主线）
   - 接口：`POST /api/v1/agents/batch`
   - 文件：`backend/app/api/routes.py`、`backend/app/core/store.py`
   - 能力：
     - 支持批量创建智能体（name/level/role/status/parent_id/domain）
     - 父节点校验（不存在时返回 `INVALID_PARENT_AGENT`）
     - 返回结构：`items/total`

10. 补充智能体批量创建接口最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_agents_batch_create_endpoint`

11. 落地 v1.1 参数增强（项目/任务/智能体筛选）
    - 文件：`backend/app/api/routes.py`、`backend/app/api/tasks_router.py`、`backend/app/core/store.py`、`backend/app/models/task.py`
    - 能力：
      - `POST /api/v1/projects` 支持 `tags`
      - `GET /api/v1/tasks` / `GET /api/v1/projects/{id}/tasks` 支持 `assignee_id` 过滤
      - `GET /api/v1/agents` 支持 `capability_id` 过滤（匹配 `skill_config.skill_ids`）

12. 补充 v1.1 参数增强最小回归
    - 文件：`backend/tests/test_tasks_api.py`、`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_task_list_filters_by_assignee_id`
      - `test_project_create_accepts_tags`
      - `test_agents_filter` 增强 capability_id 断言

13. 落地 v1.1 响应增强（项目 `last_activity`）
    - 文件：`backend/app/core/store.py`
    - 能力：
      - 创建项目自动写入 `last_activity`
      - 更新项目自动刷新 `last_activity`
      - 任务创建/更新/删除后刷新对应项目 `last_activity`
      - 项目讨论新增后刷新对应项目 `last_activity`

14. 补充 `last_activity` 最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_project_last_activity_updates_after_task_and_discussion`
      - `test_project_create_accepts_tags` 增强 `last_activity` 断言

15. 落地 v1.1 对话流式响应增强（`thinking_steps`）
    - 文件：`backend/app/api/routes.py`
    - 能力：
      - `POST /api/v1/chat/sessions/{id}/messages/stream` 在 `delta` 事件前新增 `thinking_steps` 事件
      - 事件结构：`{ "type": "thinking_steps", "steps": [...] }`

16. 补充 `thinking_steps` 最小回归
    - 文件：`backend/tests/test_auth_and_chat_stream.py`
    - 新增断言：
      - `test_chat_sse_stream` 校验 SSE 输出包含 `thinking_steps`

17. 落地 v1.1 智能体响应增强（`tags` / `runtime_state.cognitive_load`）
    - 文件：`backend/app/api/routes.py`
    - 能力：
      - `GET /api/v1/agents` 返回中补齐 `tags`（默认 `[]`）
      - `GET /api/v1/agents` 返回中补齐 `runtime_state.cognitive_load`（默认 `0.0`）
      - `GET /api/v1/agents/{id}` 与 `POST /api/v1/agents/batch` 返回同样保持该结构

18. 补充智能体响应增强最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_agents_response_includes_tags_and_runtime_state`

19. 增强大模型缓存可观测性（Phase4-T03）
    - 文件：`backend/app/services/model_router.py`
    - 能力：
      - 新增缓存命中统计：`cache_hits` / `cache_misses`
      - 新增缓存命中率：`cache_hit_rate`
      - 通过 `GET /api/v1/llm/status` 对外可观测

20. 补充模型路由可观测性最小回归
    - 文件：`backend/tests/test_llm_router.py`
    - 新增断言：
      - `test_llm_status_endpoint` 校验 `cache_hits` / `cache_misses` / `cache_hit_rate`

21. 增强 Webhook 查询能力（集成能力补齐）
    - 文件：`backend/app/api/routes.py`、`backend/app/core/store.py`
    - 能力：
      - 新增 `GET /api/v1/webhooks`
      - 支持 `enabled` 过滤与 `limit/offset` 分页
      - 返回结构：`items/total/limit/offset`

22. 补充 Webhook 查询最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_list_webhooks_endpoint`

23. 完成 Webhook 基础 CRUD 闭环（集成能力继续完善）
    - 文件：`backend/app/api/routes.py`、`backend/app/core/store.py`
    - 能力：
      - 新增 `PUT /api/v1/webhooks/{id}`（支持 name/url/events/enabled/secret 更新）
      - 新增 `DELETE /api/v1/webhooks/{id}`
      - URL 校验保持一致（非法 URL 返回 `INVALID_WEBHOOK_URL`）

24. 补充 Webhook 更新/删除最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_update_and_delete_webhook_endpoint`

25. 补齐审批待办接口（按计划接口映射）
    - 文件：`backend/app/api/routes.py`
    - 能力：
      - 新增 `GET /api/v1/approvals/pending`
      - 复用项目待审批数据源并支持 `limit/offset` 分页
      - 返回结构：`items/total/limit/offset`

26. 补充审批待办接口最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_approvals_pending_endpoint`

27. 补齐智能体技能关联接口（按 API 计划映射）
    - 文件：`backend/app/api/routes.py`、`backend/app/core/store.py`
    - 能力：
      - 新增 `GET /api/v1/agents/{id}/skills`
      - 新增 `PUT /api/v1/agents/{id}/skills`（整包替换绑定 skill_ids）
      - 自动维护技能记录中的 `linked_agent_ids`

28. 补充智能体技能关联最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_agent_skills_bind_and_query_endpoint`

29. 补齐会话历史聚合查询接口
    - 文件：`backend/app/api/routes.py`
    - 能力：
      - 新增 `GET /api/v1/chat/history`
      - 支持 `limit`（会话数）与 `message_limit`（每会话消息数）
      - 返回结构：`sessions/total_sessions/returned_sessions`

30. 补充会话历史接口最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_chat_history_endpoint`

31. 补齐智能体记忆查询映射接口
    - 文件：`backend/app/api/memory_router.py`
    - 能力：
      - 新增 `GET /api/v1/agents/{id}/memory`
      - 复用 working memory 数据源，返回 `agent_id/working_memory_count/working_memories`
      - 支持 `limit` 参数

32. 补充智能体记忆查询最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_agent_memory_endpoint`

33. 补齐审批动作映射接口（按审批模块计划）
    - 文件：`backend/app/api/routes.py`
    - 能力：
      - 新增 `POST /api/v1/approvals/applications`
      - 新增 `POST /api/v1/approvals/{id}/approve`
      - 新增 `POST /api/v1/approvals/{id}/reject`
      - 驳回场景新增 `reason` 必填校验，缺失返回 `APPROVAL_REJECT_REASON_REQUIRED`

34. 补充审批动作映射接口最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_approval_application_and_actions_endpoints`

35. 补齐 Webhook 单条查询接口
    - 文件：`backend/app/api/routes.py`、`backend/app/core/store.py`
    - 能力：
      - 新增 `GET /api/v1/webhooks/{id}`
      - 不存在时返回 404

36. 补充 Webhook 单条查询最小回归
    - 文件：`backend/tests/test_api_smoke.py`
    - 新增测试：
      - `test_get_webhook_endpoint`

37. 完成 v1.1 变更文档收口
    - 文件：`docs/API_CHANGELOG.md`
    - 变更：
      - 章节标题由 `v1.1.0（计划中）` 更新为 `v1.1.0（已完成）`
      - v1.1 新增 API 状态由 `计划中` 统一更新为 `已完成`

38. 二次收口 API 变更日志与实现对齐
    - 文件：`docs/API_CHANGELOG.md`
    - 变更：
      - 补齐已落地但未登记的 v1.1 端点（Webhook CRUD、审批映射、智能体技能/记忆、会话历史等）
      - 修正 SSE 事件映射端点为 `/api/v1/chat/sessions/{id}/messages/stream`

39. CI 回归集合与新增能力对齐（收口强化）
    - 文件：`.github/workflows/backend-ci.yml`
    - 变更：
      - 新增 `Run chat and llm integration regressions` 步骤（`test_auth_and_chat_stream.py` + `test_llm_router.py`）
      - 后端回归步骤补入 `test_tasks_api.py`，覆盖 v1.1 参数增强与任务筛选场景

40. 运营风险报告补充 Git 同步健康度指标（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增字段：
        - `git_sync_success_count`
        - `git_sync_skipped_count`
        - `git_sync_success_rate`
      - 保持既有 `git_sync_failure_count` 与 `ops_risk_level` 逻辑不变，在不破坏兼容性的前提下增强可观测性
      - 补充测试断言，校验新增字段存在且 `git_sync_success_rate` 类型正确

41. Git 同步链路稳定性与摘要可观测性增强（完成后增强）
    - 文件：`scripts/git_sync_once.ps1`、`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `git_sync_once.ps1` 在 `git add -A` 后新增“二次无变更检测”：
        - 当暂存区无可提交内容且未开启 `AllowEmpty` 时，按 `skipped` 处理并输出 `SYNC_RESULT`，避免将“无有效变更”误判为失败
        - 保留日志与可选审计上报（`stage=post_add`），保持失败不中断策略
      - `GET /api/v1/ops/git-sync/summary` 新增健康度时间字段：
        - `last_success_at` / `last_failure_at`
        - `minutes_since_last_success` / `minutes_since_last_failure`
      - 补充最小回归断言，校验新增字段存在且类型正确（兼容既有返回结构）

42. Git 同步摘要补充 skipped 时序可观测字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `last_skipped_at`
        - `minutes_since_last_skipped`
      - 与既有 `last_success_at/last_failure_at` 保持同口径，便于统一构建健康看板与告警策略
      - 补充最小回归断言，校验新增字段存在且类型正确，保持兼容增强

43. Git 同步摘要补充全量事件总时钟字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `last_event_at`
        - `minutes_since_last_event`
      - 语义为“最近一次 git_sync_status 事件（success/failure/skipped 任意状态）”，用于快速判断链路是否长时间静默
      - 补充最小回归断言，校验字段存在与类型正确，保持接口向后兼容

44. Git 同步摘要补充连续失败/非成功 streak 指标（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `consecutive_failure_streak`
        - `consecutive_non_success_streak`
      - 口径：按过滤条件（environment/branch/source/since/until）取最新事件序列，连续统计直到遇到首个中断状态
      - 用于快速识别“连续推送失败”与“链路持续未成功”风险态
      - 补充最小回归断言，校验字段存在且类型为 `int`

45. 运营风险报告补充 Git 连续失败 streak 指标（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_consecutive_failure_streak`
        - `git_sync_consecutive_non_success_streak`
      - 口径：在报告时间窗口内按事件时间倒序统计，直到遇到首个中断状态
      - 保持既有 `ops_risk_level` 判定逻辑不变，仅追加可观测字段
      - 补充最小回归断言，校验字段存在且类型正确（`int`）

46. Git 同步摘要新增健康等级与风险标记（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `sync_health_level`（`healthy|warning|high_risk`）
        - `sync_health_warning`（布尔值）
      - 判定基于既有连续指标：
        - `high_risk`: `consecutive_failure_streak>=3` 或 `consecutive_non_success_streak>=5`
        - `warning`: `consecutive_failure_streak>=1` 或 `consecutive_non_success_streak>=2`
        - 否则 `healthy`
      - 保持接口兼容，仅追加字段并补最小回归断言

47. 运营风险报告补充 Git 同步健康等级字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_health_level`（`healthy|warning|high_risk`）
        - `git_sync_health_warning`（布尔值）
      - 判定口径与 `git_sync` 摘要保持一致（基于连续失败/连续非成功 streak）
      - 保持 `ops_risk_level` 既有逻辑不变，仅追加健康透出字段
      - 补充最小回归断言，校验字段存在、枚举值合法与类型正确

48. 运营风险报告补充最近 Git 同步事件时钟（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `last_git_sync_event_at`
        - `minutes_since_last_git_sync_event`
      - 用于快速识别“Git 同步链路是否长时间无事件”的静默风险
      - 保持既有风险分级逻辑不变，仅追加可观测字段
      - 补充最小回归断言，校验字段存在且类型正确（`str`/`float`）

49. 运营风险报告补充最近失败事件时钟（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `last_git_sync_failure_at`
        - `minutes_since_last_git_sync_failure`
      - 用于识别“最近失败距今多久”，支持失败恢复时效观测
      - 保持既有 `ops_risk_level` 与健康等级逻辑不变，仅追加可观测字段
      - 补充最小回归断言，校验字段存在且类型正确（`str`/`float`）

50. 运营风险报告补充最近成功事件时钟（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `last_git_sync_success_at`
        - `minutes_since_last_git_sync_success`
      - 用于评估“成功同步最近发生时间”与链路恢复有效性
      - 保持既有风险与健康逻辑不变，仅追加可观测字段
      - 补充最小回归断言，校验字段存在且类型正确（`str`/`float`）

51. 运营风险报告补充失败率/跳过率指标（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_failure_rate`
        - `git_sync_skipped_rate`
      - 与既有 `git_sync_success_rate` 保持同口径（基于报告窗口内 `git_sync_event_count` 百分比计算）
      - 保持既有 `ops_risk_level` 与健康等级逻辑不变，仅追加可观测字段
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

52. 运营风险报告补充 Git 同步失败主因字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_top_failure_reason_code`
        - `git_sync_top_failure_reason_count`
      - 口径：在报告窗口内统计失败事件 `reason_code` 分布，返回出现次数最多的失败原因
      - 保持既有风险分级与健康判定逻辑不变，仅追加可观测字段
      - 补充最小回归断言，校验字段存在且类型正确（`str`/`int`）

53. 运营风险报告补充失败主因占比字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_top_failure_reason_rate`
      - 口径：`git_sync_top_failure_reason_count / git_sync_failure_count * 100`，保留 1 位小数
      - 当无失败事件时返回 `0.0`，保持返回结构稳定
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

54. 运营风险报告补充日均失败事件密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_failure_density_per_day`
      - 口径：`git_sync_failure_count / days`，保留 2 位小数（`days` 最小按 1 计算）
      - 用于衡量时间窗口内失败事件强度，便于横向对比不同窗口风险
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

55. 运营风险报告补充日均跳过事件密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_skipped_density_per_day`
      - 口径：`git_sync_skipped_count / days`，保留 2 位小数（`days` 最小按 1 计算）
      - 用于观测同步链路“跳过事件”强度变化，辅助判断是否存在长期无变更或触发条件偏差
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

56. 运营风险报告补充日均成功事件密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_success_density_per_day`
      - 口径：`git_sync_success_count / days`，保留 2 位小数（`days` 最小按 1 计算）
      - 用于衡量同步链路正向产出强度，与失败/跳过密度形成对照
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

57. 运营风险报告补充日均总事件密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_event_density_per_day`
      - 口径：`git_sync_event_count / days`，保留 2 位小数（`days` 最小按 1 计算）
      - 用于衡量同步链路总体活跃度，与成功/失败/跳过密度联合判断健康状态
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

58. 运营风险报告补充成功-失败净值密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_net_success_density_per_day`
      - 口径：`(git_sync_success_count - git_sync_failure_count) / days`，保留 2 位小数（`days` 最小按 1 计算）
      - 用于快速判断窗口期内同步净健康趋势（正值偏健康，负值偏风险）
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

59. 运营风险报告补充成功-失败净值占比（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_net_success_rate`
      - 口径：`(git_sync_success_count - git_sync_failure_count) / git_sync_event_count * 100`，保留 1 位小数
      - 当无事件时返回 `0.0`，保持返回结构稳定
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

60. 运营风险报告补充 Git 同步失败压力指数（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_failure_pressure_index`
      - 口径：`git_sync_failure_rate * (1 + git_sync_consecutive_failure_streak)`，保留 1 位小数
      - 用于同时反映失败占比与连续失败叠加压力，便于快速识别高压风险窗口
      - 补充最小回归断言，校验字段存在且类型正确（`float`）

61. Git 同步链路兼容修复与推送重试可观测增强（完成后增强）
    - 文件：`scripts/git_sync_once.ps1`、`scripts/logs/git_auto_sync_20260416.log`、`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - 修复 `git_sync_once.ps1` 在旧版 PowerShell 下的解析阻塞（`??` 语法兼容问题），改为显式空值处理，恢复同步脚本可执行性。
      - 实测一次 Git 同步链路：首次 push 失败后重试成功，`SYNC_RESULT` 为 `success`，日志记录失败原因（连接重置）与重试成功轨迹；审计上报失败不阻断主流程。
      - `GET /api/v1/ops/git-sync/summary` 新增推送重试观测字段：
        - `avg_push_attempts`
        - `max_push_attempts`
        - `push_attempt_sample_count`
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增推送重试观测字段：
        - `git_sync_avg_push_attempts`
        - `git_sync_max_push_attempts`
        - `git_sync_push_attempt_sample_count`
      - 增强时区稳定性：当运行环境缺少 IANA tzdata 时，为 `UTC/GMT/Asia/Shanghai` 提供兜底映射，避免 `git-sync/summary` 因时区解析失败返回 400。
      - 补充最小回归断言并修正审批分页断言（扩大 `limit` 以避免数据累积导致的偶发漏检），保持兼容增强。

62. 运营风险报告补充 Git 同步审计投递可观测指标（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_failed_count`
        - `git_sync_audit_delivery_success_count`
        - `git_sync_audit_delivery_failure_rate`
        - `git_sync_audit_delivery_success_rate`
      - 口径：读取 `git_sync_status` 事件 `context.audit_delivery`（`failed|success`）聚合计数与占比，分母为报告窗口内 `git_sync_event_count`。
      - 目标：在“同步成功/失败”之外，补齐“审计上报通道本身是否稳定”的观测维度，便于排查“主链路成功但审计旁路不稳定”场景。
      - 补充最小回归断言，校验新增字段存在且类型正确（`int`/`float`），保持返回结构兼容增强。

63. Git 同步摘要补充审计投递健康字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_success_count`
        - `audit_delivery_failed_count`
        - `audit_delivery_success_rate`
        - `audit_delivery_failure_rate`
      - 口径：在现有时间窗口与过滤条件下，聚合 `git_sync_status` 事件中 `context.audit_delivery`（`success|failed`）并计算占比（分母为 `totals.total`）。
      - 目标：让 Git 摘要接口直接具备“同步主链路 + 审计旁路”双维健康观测能力，减少仅靠 `ops_risk` 报告排障的时延。
      - 补充最小回归断言，校验新增字段存在且类型正确（`int`/`float`），保持接口向后兼容。

64. Git 同步摘要补充审计投递时钟字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `last_audit_delivery_success_at`
        - `last_audit_delivery_failed_at`
        - `minutes_since_last_audit_delivery_success`
        - `minutes_since_last_audit_delivery_failed`
      - 口径：在现有过滤条件窗口内，基于 `context.audit_delivery=success|failed` 统计最近事件时间与距今分钟数。
      - 目标：支撑“审计旁路是否长时间失败/沉默”的时效观测，缩短故障定位路径。
      - 补充最小回归断言，校验字段存在且类型正确（`str`/`float`），保持接口兼容增强。

65. 运营风险报告补充审计投递最近时钟字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `last_git_sync_audit_delivery_success_at`
        - `minutes_since_last_git_sync_audit_delivery_success`
        - `last_git_sync_audit_delivery_failed_at`
        - `minutes_since_last_git_sync_audit_delivery_failed`
      - 口径：在报告窗口内基于 `git_sync_status.context.audit_delivery=success|failed` 统计最近一次事件时钟。
      - 目标：让 `ops_risk` 报告直接观测“审计投递成功/失败最近发生时间”，提升旁路异常定位效率。
      - 补充最小回归断言，校验新增字段存在且类型正确（`str`/`float`），保持兼容增强。

66. Git 摘要与运营风险报告补充审计投递健康等级（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_health_level`（`healthy|warning|high_risk`）
        - `audit_delivery_health_warning`（布尔值）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_health_level`（`healthy|warning|high_risk`）
        - `git_sync_audit_delivery_health_warning`（布尔值）
      - 判定口径：优先基于审计投递失败计数与“仅失败无成功”场景进行风险分级，保持现有字段兼容并增强可观测判读效率。
      - 补充最小回归断言，校验字段存在、枚举合法和类型正确。

67. Git 摘要与运营风险报告补充审计投递失败压力指数（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_failure_pressure_index`
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_failure_pressure_index`
      - 口径：
        - `audit_delivery_failure_rate * (1 + audit_delivery_failed_count)`，保留 1 位小数
      - 目标：同时反映审计投递失败占比与失败规模叠加压力，快速识别审计旁路高压窗口。
      - 补充最小回归断言，校验字段存在且类型正确（`float`），保持兼容增强。

68. Git 摘要与运营风险报告补充审计投递净健康分（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_net_health_score`
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_net_health_score`
      - 口径：
        - `audit_delivery_success_rate - audit_delivery_failure_rate`，保留 1 位小数
      - 目标：在失败压力指标之外，提供“成功-失败净值”视角，快速判定审计投递通道净健康趋势（正值偏健康，负值偏风险）。
      - 补充最小回归断言，校验字段存在且类型正确（`float`），保持接口兼容增强。

69. Git 摘要与运营风险报告补充审计投递净健康等级（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_net_health_level`（`healthy|warning|high_risk`）
        - `audit_delivery_net_health_warning`（布尔值）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_net_health_level`（`healthy|warning|high_risk`）
        - `git_sync_audit_delivery_net_health_warning`（布尔值）
      - 判定口径：基于净健康分（`success_rate - failure_rate`）分级，`<= -20` 判 `high_risk`，`<0` 判 `warning`，其余为 `healthy`。
      - 目标：让净值指标可直接用于看板分层和告警触发，减少人工解读成本。
      - 补充最小回归断言，校验字段存在、枚举合法和类型正确。

70. Git 摘要与运营风险报告补充审计投递日均密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_success_density_per_day`
        - `audit_delivery_failed_density_per_day`
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_success_density_per_day`
        - `git_sync_audit_delivery_failed_density_per_day`
      - 口径：成功/失败审计投递计数分别除以摘要窗口 `days` 或报告参数 `days`（最小按 1），保留 2 位小数，与既有 Git 事件密度字段口径一致。
      - 目标：横向对比不同时间窗口内审计旁路活跃度，辅助判断“偶发失败”与“持续高压”。
      - 补充最小回归断言，校验字段存在且类型为 `float`，保持兼容增强。

71. Git 摘要与运营风险报告补充审计投递净日均密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_net_density_per_day`
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_net_density_per_day`
      - 口径：`(成功审计投递计数 - 失败审计投递计数) / days`（摘要与报告窗口 `days` 最小按 1），保留 2 位小数，与 `git_sync_net_success_density_per_day` 语义对齐。
      - 目标：在成功/失败分密度之外，一眼判断审计旁路净产出趋势（正值偏健康，负值偏风险）。
      - 补充最小回归断言，校验字段存在且类型为 `float`，保持兼容增强。

72. Git 摘要与运营风险报告补充审计投递覆盖率（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_tagged_count`（`context.audit_delivery` 为 `success|failed` 的事件条数）
        - `audit_delivery_coverage_rate`（`tagged_count / totals.total * 100`，保留 1 位小数；无事件时为 `0.0`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_tagged_count`
        - `git_sync_audit_delivery_coverage_rate`
      - 目标：衡量同步事件中有多少比例回传了审计投递状态，便于发现“主链路有事件但旁路未打点”的静默缺口。
      - 补充最小回归断言，校验字段存在且类型正确（`int`/`float`），保持兼容增强。

73. Git 摘要与运营风险报告补充审计投递未标记占比（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_untagged_count`（`totals.total - audit_delivery_tagged_count`，下限 0）
        - `audit_delivery_untagged_rate`（`untagged_count / totals.total * 100`，保留 1 位小数；无事件时为 `0.0`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_untagged_count`
        - `git_sync_audit_delivery_untagged_rate`
      - 目标：与覆盖率字段互补，直接量化未携带 `success|failed` 审计投递标记的同步事件规模，便于推动脚本侧全量打点。
      - 补充最小回归断言，校验字段存在且类型正确（`int`/`float`），保持兼容增强。

74. Git 自动同步远端推送失败记录（网络/TLS，非代码回退）
    - 时间：2026-04-16（与条目 73 同轮）
    - 本地提交：`2f55dfd`（`chore(sync): auto sync 2026-04-16 09:10:38`），已包含条目 73 代码与交接更新。
    - 远端：`git push origin main` 经脚本重试 3 次及手工重试仍失败，典型错误为 `Recv failure: Connection was reset` / `schannel: server closed abruptly`。
    - 处置：网络恢复后执行 `scripts/git_sync_once.ps1` 或 `git push origin main` 补推即可；失败不阻断本地开发与审计日志落盘。

75. Git 摘要与运营风险报告补充审计投递非法取值统计（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_invalid_count`：`context.audit_delivery` 非空且不为 `success|failed` 的条数（与「未标记」区分，用于发现脚本枚举/拼写错误）
        - `audit_delivery_invalid_rate`（相对 `totals.total`，保留 1 位小数）
        - `last_audit_delivery_invalid_at`、`minutes_since_last_audit_delivery_invalid`
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_invalid_count`、`git_sync_audit_delivery_invalid_rate`
        - `last_git_sync_audit_delivery_invalid_at`、`minutes_since_last_git_sync_audit_delivery_invalid`
      - 运营报告侧非法计数仅统计 `context.status` 为 `success|failure|skipped` 的事件，与摘要主循环口径一致。
      - 最小回归：`test_git_sync_summary_endpoint`、`test_analytics_reports_project_execution_and_ops_risk` 注入非法 `audit_delivery` 样例并断言新字段。

76. 条目 75 同步远端记录（运维追溯）
    - 本地提交：`d575df1`（`feat(ops): audit_delivery invalid metrics for git summary and ops_risk`），已成功推送至 `origin/main`（首轮 `git push` 曾遇 `Recv failure: Connection was reset`，重试后成功）。

77. Git 摘要与运营风险报告补充审计投递「空标记」分解（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：
        - `audit_delivery_empty_count`：`context.audit_delivery` 缺省或去空格后为空（未打点）的条数
        - `audit_delivery_empty_rate`（相对 `totals.total`，保留 1 位小数）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：
        - `git_sync_audit_delivery_empty_count`、`git_sync_audit_delivery_empty_rate`
      - 摘要主循环内每条合法同步事件在审计投递维度上互斥归入：`success|failed`（计入 tagged）、非法非空取值、空标记；因此恒有 `tagged + invalid + empty == totals.total`，且 `untagged == invalid + empty`。
      - 运营报告侧：`empty`/`invalid` 仅对 `context.status` 为 `success|failure|skipped` 的事件计数；`git_sync_audit_delivery_success/failed` 仍来自全窗口内全部 `git_sync_status` 事件。若存在非规范 `context.status` 的存量数据，可能出现 `git_sync_audit_delivery_untagged_count` 大于 `invalid + empty` 的情况（分母仍为 `git_sync_event_count`）。
      - 最小回归：向 `test_git_sync_summary_endpoint` / `test_analytics_reports_project_execution_and_ops_risk` 追加无 `audit_delivery` 的成功样例，并校验摘要侧分拆恒等式。

78. 条目 77 同步远端记录（运维追溯）
    - 本地提交：`570c8da`（`feat(ops): audit_delivery empty breakdown for git summary and ops_risk`），已推送至 `origin/main`。

79. Git 摘要与运营风险报告补充审计投递「空标记」最近时钟（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：`last_audit_delivery_empty_at`、`minutes_since_last_audit_delivery_empty`（在窗口与过滤条件下，取最近一次 `audit_delivery` 为空的同步事件时间戳，与条目 64/75 的 success/failed/invalid 时钟字段对称）。
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`last_git_sync_audit_delivery_empty_at`、`minutes_since_last_git_sync_audit_delivery_empty`（仅对 `context.status` 合法且 `audit_delivery` 为空的事件取最近时间）。
      - 最小回归：在既有「空标记」样例上断言新字段类型（`str`/`float`）。

80. 条目 79 同步远端记录（运维追溯）
    - 本地提交：`cd3a4d2`（`feat(ops): audit_delivery empty last-seen timestamps for summary and ops_risk`），已推送至 `origin/main`。

81. Git 摘要与运营风险报告补充审计投递非法/空标记日均密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：`audit_delivery_invalid_density_per_day`、`audit_delivery_empty_density_per_day`（分别 `invalid_count / days`、`empty_count / days`，`days` 为摘要参数 `days`，保留 2 位小数，与 `audit_delivery_success_density_per_day` 等口径一致）。
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_audit_delivery_invalid_density_per_day`、`git_sync_audit_delivery_empty_density_per_day`（分母 `max(1, days)`，与报告参数 `days` 对齐）。
      - 最小回归：`test_git_sync_summary_endpoint`、`test_analytics_reports_project_execution_and_ops_risk` 增加字段存在性与 `float` 类型断言。

82. 条目 81 同步远端记录（运维追溯）
    - 本地提交：`92204cf`（`feat(ops): audit_delivery invalid/empty density per day`），已推送至 `origin/main`。

83. Git 摘要与运营风险报告补充审计投递未标记日均密度（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：`audit_delivery_untagged_density_per_day`（`audit_delivery_untagged_count / days`，保留 2 位小数；摘要侧恒等于 `invalid_density + empty_density`，测试中断言该恒等式）。
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_audit_delivery_untagged_density_per_day`（`git_sync_audit_delivery_untagged_count / max(1, days)`），便于与 `git_sync_event_density_per_day` 等并列观察「未携带 success|failed 审计标记」的日均强度。
      - 最小回归：字段存在性、`float` 类型及摘要侧分拆恒等校验。

84. 条目 83 同步远端记录（运维追溯）
    - 本地提交：`76dbd55`（`feat(ops): audit_delivery untagged density per day`），已推送至 `origin/main`（首轮 `git push` 曾遇 `schannel: server closed abruptly` / `Recv failure: Connection was reset`，重试后成功）。

85. Git 摘要与运营风险报告补充审计投递未标记最近时钟（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 变更：
      - `GET /api/v1/ops/git-sync/summary` 新增：`last_audit_delivery_untagged_at`、`minutes_since_last_audit_delivery_untagged`。
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`last_git_sync_audit_delivery_untagged_at`、`minutes_since_last_git_sync_audit_delivery_untagged`。
      - 口径：基于非法标记与空标记最近时钟取并集最近值（`max(last_invalid_at, last_empty_at)`）；若其中一类不存在，则回退到另一类；两类均不存在则为 `null`。
      - 最小回归：补充字段存在性与 `str`/`float` 类型断言。

86. 条目 85 同步远端记录（运维追溯）
    - 本地提交：`e0ddc37`（`feat(ops): audit_delivery untagged last-seen timestamps`），已推送至 `origin/main`。

87. Git 同步摘要与运营风险报告补充链路静默告警字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_warning`（`bool`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_warning`（`bool`）
    - 统计口径：
      - 统一基于“最近 Git 同步事件距今分钟数”判定；
      - 当最近事件缺失（`minutes_since_*` 为 `null`）或超过查询窗口分钟数（`days*24*60`）时置为 `true`，否则为 `false`。
    - 测试覆盖：
      - 最小回归 `python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 新增断言校验上述两个字段存在且类型为 `bool`。
    - 推送结果：
      - 本轮已执行提交流程与 `git push origin main`，但当前自动化终端未返回可读的提交回执；需在本地终端复核最终远端状态。

88. 条目 87 同步状态复核占位（运维追溯）
    - 目标提交信息：
      - `feat(ops): add git sync silence warning observability`
      - `docs(handoff): append item 87 for silence warning metrics`
    - 当前状态：
      - 已完成代码与文档变更、并通过最小回归；
      - 自动化会话未能读取到新增提交 SHA 与远端确认信息，建议在本地命令行执行 `git log -2 --oneline` 与 `git push origin main` 复核并回填本条。

89. Git 同步摘要与运营风险报告补充静默阈值分钟数字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_threshold_minutes`（`int`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_threshold_minutes`（`int`）
    - 统计口径：
      - 与既有静默告警保持同口径，阈值固定为查询窗口分钟数（`days*24*60`），用于解释告警判定边界。
      - 关系：`*_silence_warning = (minutes_since_last_event is null) or (minutes_since_last_event > *_silence_threshold_minutes)`。
    - 测试覆盖：
      - 目标最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 增量断言：新增阈值字段存在性与 `int` 类型校验。
      - 实际执行：一次定向回归报错（`NameError`，已修复），后续全量最小回归在当前环境出现长时间阻塞；中断后待下一轮复跑确认。
    - 推送结果：
      - 本条将在提交与推送完成后补充 SHA 与重试状态。

90. 条目 89 同步远端记录（运维追溯）
    - 本地提交：
      - `192d1bf`（`feat(ops): expose git sync silence threshold minutes`）
      - `2452cad`（`docs(handoff): append item 89 for silence threshold minutes`）
    - 推送结果：
      - `git push origin main` 一次成功，远端快进：`9abba91..2452cad`，未触发 TLS/网络重试。
    - 最小回归补充说明：
      - 本轮执行 `python -m pytest tests/test_api_smoke.py -q --tb=short` 时在当前环境出现阻塞，已中断并记录；
      - 已通过定向回归定位并修复新增代码缺陷（`NameError`），下一轮将优先复跑最小回归并回填最终通过结果。

91. Git 同步摘要与运营风险报告补充静默超阈值分钟数字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_overdue_minutes`（`float|null`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_overdue_minutes`（`float|null`）
    - 统计口径：
      - 统一为 `max(0, minutes_since_last_event - silence_threshold_minutes)`，保留 1 位小数；
      - 当最近事件不存在（`minutes_since_last_event=null`）时，该字段返回 `null`，保持语义清晰。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 133.69s`
      - 新增断言：字段存在且在当前样例下类型为 `float`。
    - 推送结果：
      - 本条将在提交并推送完成后补充 SHA 与重试状态。

92. 条目 91 同步远端记录（运维追溯）
    - 本地提交：
      - `1c86c93`（`feat(ops): add git sync silence overdue minute metrics`）
      - `1c53764`（`docs(handoff): append item 91 for silence overdue metrics`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Recv failure: Connection was reset`
      - 第 2 次重试失败：`Recv failure: Connection was reset`
      - 第 3 次重试成功：`a12db90..1c53764  main -> main`
    - 处置结论：
      - 属于瞬时网络/TLS波动，代码与文档已成功推送到远端 `main`，无需回滚。

93. Git 同步摘要与运营风险报告补充静默超阈值比例字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_overdue_rate`（`float|null`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_overdue_rate`（`float|null`）
    - 统计口径：
      - 统一为 `sync_silence_overdue_minutes / silence_threshold_minutes * 100`，保留 1 位小数；
      - 当最近事件不存在（`minutes_since_last_event=null`）时，该字段返回 `null`。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 134.87s`
      - 新增断言：字段存在且在当前样例下类型为 `float`。
    - 推送结果：
      - 本条将在提交并推送完成后补充 SHA 与重试状态。

94. 条目 93 同步远端记录（运维追溯）
    - 本地提交：
      - `7b0d9c9`（`feat(ops): add git sync silence overdue rate metrics`）
      - `2096d26`（`docs(handoff): append item 93 for silence overdue rates`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Could not resolve host: github.com`
      - 第 2 次重试失败：`Could not resolve host: github.com`
      - 第 3 次重试成功：`06515ab..2096d26  main -> main`
    - 处置结论：
      - 属于瞬时 DNS/网络波动，代码与文档已成功推送到远端 `main`。

95. Git 同步摘要与运营风险报告补充静默余量分钟数字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_headroom_minutes`（`float|null`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_headroom_minutes`（`float|null`）
    - 统计口径：
      - 与 `*_silence_overdue_minutes` 对称：`max(0, silence_threshold_minutes - minutes_since_last_event)`，保留 1 位小数；
      - 当最近事件不存在（`minutes_since_last_event=null`）时返回 `null`；
      - 与超阈值侧关系：在「有最近事件时间戳」前提下，恒有 `overdue_minutes` 与 `headroom_minutes` 其一为 0（另一为非负），二者不同时为正。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 140.94s`
      - 新增断言：两接口字段存在且类型为 `float`。
    - 推送结果：
      - 见条目 96。

96. 条目 95 同步远端记录（运维追溯）
    - 本地提交：
      - `1cbca9b`（`feat(ops): add git sync silence headroom minute metrics`）
      - `370ef7b`（`docs(handoff): append items 95-96 for silence headroom metrics`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Could not resolve host: github.com`
      - 第 2 次重试成功：`3175581..370ef7b  main -> main`
    - 处置结论：
      - 属于瞬时 DNS/网络波动，代码与文档已成功推送到远端 `main`。

97. Git 同步摘要与运营风险报告补充静默状态枚举字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_state`（`missing|within|overdue`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_state`（`missing|within|overdue`）
    - 统计口径：
      - `missing`: `minutes_since_last_*` 为 `null`（窗口内没有任何 git_sync 事件，或无法计算分钟数）
      - `overdue`: `*_silence_warning=true`（超出 `*_silence_threshold_minutes`）
      - `within`: 其余情况（窗口内有事件且未超阈值）
      - 目的：为看板/告警提供可直接分组的离散状态，避免前端重复推导。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 137.55s`
      - 新增断言：字段存在且枚举值合法。
    - 推送结果：
      - 见条目 98。

98. 条目 97 同步远端记录（运维追溯）
    - 本地提交：
      - `907f2a1`（`feat(ops): add git sync silence state enum`）
      - `e5b7206`（`docs(handoff): append items 97-98 for silence state enums`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Could not resolve host: github.com`
      - 第 2 次重试成功：`d8f8dd9..e5b7206  main -> main`
    - 处置结论：
      - 属于瞬时 DNS/网络波动，代码与文档已成功推送到远端 `main`。

99. Git 同步摘要与运营风险报告补充静默状态排序字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_state_rank`（`int`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_state_rank`（`int`）
    - 统计口径：
      - 与 `*_silence_state` 一一对应：
        - `within` → `0`
        - `overdue` → `1`
        - `missing` → `2`
      - 目的：便于看板/告警按严重程度排序与阈值比较（无需前端/BI 再映射）。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 138.48s`
      - 新增断言：字段存在、类型为 `int` 且取值集合为 `{0,1,2}`。
    - 推送结果：
      - 见条目 100。

100. 条目 99 同步远端记录（运维追溯）
    - 本地提交：
      - `552c9e6`（`feat(ops): add git sync silence state rank metrics`）
      - `f6f7f79`（`docs(handoff): append items 99-100 for silence state ranks`）
    - 推送结果：
      - `git push origin main` 一次成功：`0e32de2..f6f7f79  main -> main`

101. Git 同步摘要与运营风险报告补充静默事件存在布尔字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_event_present`（`bool`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_event_present`（`bool`）
    - 统计口径：
      - 当 `minutes_since_last_*` 可计算时返回 `true`
      - 当窗口内无事件或无法计算分钟数时返回 `false`
      - 目标：与既有 `*_silence_state` / `*_silence_state_rank` 形成布尔-枚举-排序三层观测，方便不同消费端按最简模型取值
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 138.79s`
      - 新增断言：字段存在且类型为 `bool`
    - 推送结果：
      - 见条目 102。

102. 条目 101 同步远端记录（运维追溯）
    - 本地提交：
      - `108390a`（`feat(ops): add git sync silence event-present flags`）
      - `65559ee`（`docs(handoff): append items 101-102 for silence event flags`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Could not resolve host: github.com`
      - 第 2 次重试失败：`schannel: failed to receive handshake, SSL/TLS connection failed`
      - 第 3 次重试失败：`Recv failure: Connection was reset`
      - 第 4 次重试成功：`53c0470..65559ee  main -> main`

103. Git 同步摘要与运营风险报告补充静默状态标签字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_state_label`（`无事件|阈值内|已超阈值`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_state_label`（`无事件|阈值内|已超阈值`）
    - 统计口径：
      - 与既有 `*_silence_state` 一一对应：
        - `missing` → `无事件`
        - `within` → `阈值内`
        - `overdue` → `已超阈值`
      - 目标：为控制台、报表导出与交接视图提供开箱即用的人类可读标签，减少调用端翻译成本。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 141.35s`
      - 新增断言：字段存在且标签枚举值合法。
    - 推送结果：
      - 见条目 104。

104. 条目 103 同步远端记录（运维追溯）
    - 本地提交：
      - `68b9056`（`feat(ops): add git sync silence state labels`）
      - `357afcf`（`docs(handoff): append items 103-104 for silence state labels`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Could not resolve host: github.com`
      - 第 2 次重试失败：`Recv failure: Connection was reset`
      - 第 3 次重试成功：`2c20841..357afcf  main -> main`

105. Git 同步摘要与运营风险报告补充静默状态短码字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_state_code`（`MISSING|WITHIN|OVERDUE`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_state_code`（`MISSING|WITHIN|OVERDUE`）
    - 统计口径：
      - 与既有 `*_silence_state` / `*_silence_state_label` 一一对应：
        - `missing` → `MISSING`
        - `within` → `WITHIN`
        - `overdue` → `OVERDUE`
      - 目标：为日志、导出、规则表达式与外部系统集成提供稳定短码，避免消费端依赖中文标签或低层枚举再映射。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 139.67s`
      - 新增断言：字段存在且短码枚举值合法。
    - 推送结果：
      - 见条目 106。

106. 条目 105 同步远端记录（运维追溯）
    - 本地提交：
      - `6723f62`（`feat(ops): add git sync silence state codes`）
      - `6d82bb8`（`docs(handoff): append items 105-106 for silence state codes`）
    - 推送结果：
      - `git push origin main` 一次成功：`0b38756..6d82bb8  main -> main`

107. Git 同步摘要与运营风险报告补充静默严重度分数字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_severity_score`（`float|null`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_severity_score`（`float|null`）
    - 统计口径：
      - 当前实现复用既有 `*_silence_overdue_rate`：
        - 有事件时：与 `*_silence_overdue_rate` 数值一致（within 为 0.0，overdue 为正值）
        - 无事件时：为 `null`
      - 目标：为看板提供单字段排序/阈值判断入口，减少多字段推导。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 141.13s`
      - 新增断言：字段存在且类型正确（当前样例为 `float`）。
    - 推送结果：
      - 见条目 108。

108. 条目 107 同步远端记录（运维追溯）
    - 本地提交：
      - `d18cd2d`（`feat(ops): add git sync silence severity scores`）
      - `6931ef2`（`docs(handoff): append items 107-108 for silence severity scores`）
    - 推送结果：
      - `git push origin main` 一次成功：`d3ef134..6931ef2  main -> main`

109. Git 同步摘要与运营风险报告补充静默严重度等级字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_severity_level`（`low|medium|high|missing`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_severity_level`（`low|medium|high|missing`）
    - 统计口径：
      - 基于既有 `*_silence_severity_score` 分层：
        - `missing`: 分数为 `null`
        - `high`: 分数 `>= 100.0`
        - `medium`: 分数 `> 0.0 且 < 100.0`
        - `low`: 分数 `= 0.0`
      - 目标：为看板着色、筛选器和规则引擎提供稳定离散等级。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 142.90s`
      - 新增断言：字段存在且枚举值合法。
    - 推送结果：
      - 见条目 110。

110. 条目 109 同步远端记录（运维追溯）
    - 本地提交：
      - `67ceeb3`（`feat(ops): add git sync silence severity levels`）
      - `08eddb5`（`docs(handoff): append items 109-110 for silence severity levels`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Recv failure: Connection was reset`
      - 第 2 次重试成功：`b02b91f..08eddb5  main -> main`

111. Git 同步摘要与运营风险报告补充静默严重度等级排序字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_severity_level_rank`（`int`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_severity_level_rank`（`int`）
    - 统计口径：
      - 与既有 `*_silence_severity_level` 一一对应：
        - `low` → `0`
        - `medium` → `1`
        - `high` → `2`
        - `missing` → `3`
      - 目标：便于排序、阈值比较与外部规则引擎直接消费，不必自行映射等级。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 143.25s`
      - 新增断言：字段存在、类型为 `int` 且取值集合为 `{0,1,2,3}`。
    - 推送结果：
      - 见条目 112。

112. 条目 111 同步远端记录（运维追溯）
    - 本地提交：
      - `7089a37`（`feat(ops): add git sync silence severity level ranks`）
      - `e2eb92d`（`docs(handoff): append items 111-112 for silence severity level ranks`）
    - 推送结果：
      - `git push origin main` 一次成功：`5535363..e2eb92d  main -> main`
      - 后续追溯提交 `929edce`（`docs(handoff): finalize item 112 push trace`）推送时：
        - 首次失败：`Recv failure: Connection was reset`
        - 第 2 次重试失败：`schannel: failed to receive handshake, SSL/TLS connection failed`
        - 第 3 次重试失败：`schannel: failed to receive handshake, SSL/TLS connection failed`
        - 第 4 次重试失败：`Recv failure: Connection was reset`
        - 第 5 次重试成功：`e2eb92d..929edce  main -> main`

113. Git 同步摘要与运营风险报告补充静默严重度等级标签字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_severity_level_label`（`低|中|高|缺失`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_severity_level_label`（`低|中|高|缺失`）
    - 统计口径：
      - 与既有 `*_silence_severity_level` 一一对应：
        - `low` → `低`
        - `medium` → `中`
        - `high` → `高`
        - `missing` → `缺失`
      - 目标：为前端展示、报表导出与交接视图提供直接可读的中文等级标签。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 143.85s`
      - 新增断言：字段存在且中文标签枚举值合法。
    - 推送结果：
      - 见条目 114。

114. 条目 113 同步远端记录（运维追溯）
    - 本地提交：
      - `74041cb`（`feat(ops): add git sync silence severity level labels`）
      - `dd36f30`（`docs(handoff): append items 113-114 for severity level labels`）
    - 推送结果：
      - 首次 `git push origin main` 长时间无输出并卡住，已人工终止后重试
      - 第 2 次推送成功：`48dea22..dd36f30  main -> main`

115. Git 同步摘要与运营风险报告补充静默严重度等级颜色字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_severity_level_color`（`string`，hex）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_severity_level_color`（`string`，hex）
    - 统计口径（映射逻辑，非计算）：
      - `missing` → `#9CA3AF`
      - `low` → `#22C55E`
      - `medium` → `#FBBF24`
      - `high` → `#EF4444`
      - 颜色字段直接由 `*_silence_severity_level` 映射得到，保持与既有等级字段一致性。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed`
      - 新增断言：字段存在且颜色值属于固定 hex 集合。
    - 推送结果：
      - 见条目 116。

116. 条目 115 同步远端记录（运维追溯）
    - 本地提交：（待回填）
    - 推送结果：（待 push/重试后回填）

117. 条目 115-116 同步远端记录补全（运维追溯）
    - 本地提交：
      - `b0c1e32`（`feat(ops): add git sync silence severity level color fields`）
      - `f2d2e05`（`docs(handoff): append items 115-116 for silence severity level colors`）
    - 推送结果：
      - `git push origin main` 一次成功：`ef285ca..f2d2e05  main -> main`

118. 条目 116 待回填说明清理（运维追溯）
    - 本次功能推送（静默严重度等级颜色字段）对应的 `git push origin main` 结果已在条目 `117` 中明确记录。

119. Git 同步摘要与运营风险报告补充静默状态颜色字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_state_color`（`string`，hex）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_state_color`（`string`，hex）
    - 统计口径：
      - 显式“状态颜色”字段，语义上与 `*_silence_severity_level_color` 保持一致：
        - `missing` → `#9CA3AF`
        - `low` → `#22C55E`
        - `medium` → `#FBBF24`
        - `high` → `#EF4444`
      - 实现为直接复用 `*_silence_severity_level_color`，保证一致性、避免重复映射。
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed`
      - 新增断言：字段存在且颜色值属于固定 hex 集合。
    - 推送结果：
      - 见条目 120。

120. 条目 119 同步远端记录（运维追溯）
    - 本地提交：
      - `01efb77`（`feat(ops): add git sync silence state color fields`）
      - `f8b55ce`（`docs(handoff): append items 119-120 for silence state colors`）
    - 推送结果：
      - 首次 `git push origin main` 失败：`Recv failure: Connection was reset`
      - 第 2 次重试成功：`5d3f69b..f8b55ce  main -> main`

121. 条目 120 追溯提交（运维追溯）
    - 本地提交：
      - `2d3a31c`（`docs(handoff): finalize item 120 push trace for state colors`）
    - 推送结果：
      - 首次推送失败：`Recv failure: Connection was reset`
      - 重试成功：`f8b55ce..2d3a31c  main -> main`

122. 条目 121 文档提交（dd6207c）推送重试补记（运维追溯）
    - 本地提交：
      - `dd6207c`（`docs(handoff): append item 121 retry trace`）
    - 推送结果：
      - 第 1 次失败：`Could not resolve host: github.com`
      - 第 2 次失败：`Recv failure: Connection was reset`
      - 第 3 次成功：`2d3a31c..dd6207c  main -> main`

123. Git 同步摘要与运营风险报告补充静默严重度等级短码字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_severity_level_code`（`MISSING|LOW|MEDIUM|HIGH`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_severity_level_code`（`MISSING|LOW|MEDIUM|HIGH`）
    - 统计口径：
      - 基于 `*_silence_severity_level` 的映射：
        - `missing` → `MISSING`
        - `low` → `LOW`
        - `medium` → `MEDIUM`
        - `high` → `HIGH`
    - 测试覆盖：
      - 最小回归：`python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed`
      - 新增断言：字段存在且短码枚举值合法。
    - 推送结果：
      - 见条目 124。

124. 条目 123 同步远端记录（运维追溯）
    - 本地提交：
      - `ec0a89d`（`feat(ops): add git sync silence severity level codes`）
      - `01fe9cf`（`docs(handoff): append items 123-124 for silence severity codes`）
    - 推送结果：
      - 第 1 次推送失败：`Could not resolve host: github.com`
      - 第 2 次推送失败：`Recv failure: Connection was reset`
      - 第 3 次推送失败：`schannel: failed to receive handshake, SSL/TLS connection failed`
      - 第 4 次推送成功：`dbc81e8..01fe9cf  main -> main`

125. Git 同步摘要与运营风险报告补充静默严重度等级颜色 RGB 字段（完成后增强）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加，不破坏既有字段）：
      - `GET /api/v1/ops/git-sync/summary` 新增：`sync_silence_severity_level_color_rgb`（`string`，`r,g,b`）
      - `GET /api/v1/analytics/reports?report_type=ops_risk` 新增：`git_sync_event_silence_severity_level_color_rgb`（`string`，`r,g,b`）
    - 统计口径（hex -> rgb 字符串解析，非计算）：
      - 由 `*_silence_severity_level_color`（`#RRGGBB`）解析得到：
        - `R` -> 十进制整数
        - `G` -> 十进制整数
        - `B` -> 十进制整数
      - 输出格式：`{r},{g},{b}`（三个十进制整数，逗号分隔）
    - 测试覆盖：
      - 最小回归：`cd backend && python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 149.31s`
      - 新增断言：`*_color_rgb` 字段存在；`split(',')` 后长度为 3 且每段均为数字。
    - 推送结果：
      - 见条目 126。

126. 条目 125 同步远端记录（运维追溯）
    - 本地提交：
      - `527a433`（`feat(ops): add git sync silence severity color rgb fields`）
      - `d39b533`（`docs(handoff): append items 125-126 for silence severity color rgb`）
    - 推送结果：
      - 代码提交：`512dce7..527a433  main -> main`
      - 文档推送：第 1 次失败：`Could not resolve host: github.com`；第 2 次成功：`527a433..d39b533  main -> main`

127. Git 同步摘要与运营风险报告字段契约回归确认（最小回归）
    - 文件：`backend/app/api/routes.py`、`backend/tests/test_api_smoke.py`
    - 接口字段（兼容追加且全量返回；字段名/类型与测试一致）：
      - `GET /api/v1/ops/git-sync/summary`：
        - 健康/静默：`sync_silence_warning`(bool)、`sync_silence_overdue_minutes`(float|null)、`sync_silence_overdue_rate`(float|null)、`sync_silence_headroom_minutes`(float|null)
        - 状态/等级枚举与分层：`sync_silence_state`/`sync_silence_state_rank`/`sync_silence_state_label`/`sync_silence_state_code`、`sync_silence_severity_level`/`sync_silence_severity_level_rank`/`sync_silence_severity_level_label`/`sync_silence_severity_level_code`
        - 颜色字段：`sync_silence_severity_level_color`(hex)、`sync_silence_severity_level_color_rgb`(`r,g,b`)、以及 `sync_silence_state_color`（复用颜色）
        - 连续风险与健康：`consecutive_failure_streak`(int)、`consecutive_non_success_streak`(int)、`sync_health_level`/`sync_health_warning`
        - 审计投递维度：`audit_delivery_*_count`(int)、`audit_delivery_*_rate`(float)、`audit_delivery_health_level`/`audit_delivery_*_pressure_index`/`audit_delivery_net_health_score`、以及 invalid/empty 对应 last/分钟字段
      - `GET /api/v1/analytics/reports?report_type=ops_risk`：
        - 主链路计数与比例：`git_sync_success_count`/`git_sync_failure_count`/`git_sync_skipped_count` 与 `git_sync_*_rate`(float)
        - 审计投递健康与密度：`git_sync_audit_delivery_failed_count`/`success_count`、`git_sync_audit_delivery_failure_rate`/`success_rate`、`git_sync_audit_delivery_health_level`/`warning`、以及各类 `git_sync_audit_delivery_*_density_per_day`
        - 失败主因：`git_sync_top_failure_reason_code`/`count`/`rate`
        - 事件静默与分层：`git_sync_event_silence_threshold_minutes`、`git_sync_event_silence_warning`、`git_sync_event_silence_overdue_minutes`/`overdue_rate`/`headroom_minutes`、`git_sync_event_silence_state*`、`git_sync_event_silence_severity_*`（含颜色字段 rgb）
        - 连续失败与健康：`git_sync_consecutive_failure_streak`/`git_sync_consecutive_non_success_streak`、`git_sync_health_level`/`warning`、`ops_risk_level`
    - 统计口径/映射规则（与当前实现保持一致）：
      - `git-sync/summary` 静默阈值：`sync_silence_threshold_minutes = days*24*60`；`sync_silence_warning` 在 `minutes_since_last_event` 为 `null` 或 `> threshold` 时为 true；`overdue_minutes = max(0, minutes_since_last_event - threshold)`（返回 float 或 null）。
      - `sync_silence_state`：`missing`（无事件，rank=2）/`within`（rank=0）/`overdue`（rank=1），并派生 label/code；severity 以 `sync_silence_overdue_rate` 分层（missing/low/medium/high），hex->rgb 提供 `r,g,b` 字符串。
      - 健康等级：基于连续指标（`failure_streak>=3` 或 `non_success_streak>=5` => high_risk；`>=1/>=2` => warning；否则 healthy）。
      - 审计投递分解：`context.audit_delivery=success|failed` 计入 success/failed；非空但非枚举计入 invalid；缺失/空计入 empty；`last_audit_delivery_untagged_at` 取 invalid/empty 最新值。
      - ops_risk 报告窗口：按 audit 事件时间回溯 `days`，将上述指标以 `git_sync_*` 命名完整映射并保持类型一致。
    - 本轮最小回归：
      - 执行：`cd backend && python -m pytest tests/test_api_smoke.py -q --tb=short`
      - 结果：`48 passed in 151.43s`（exit_code=0）
    - 推送结果：
      - 第 1 次推送失败：`Recv failure: Connection was reset`
      - 第 2 次推送成功：`331c11a..30b38eb  main -> main`

128. Day3 门禁回归与发布前收口快照更新（Day4 收口）
    - 文件：`docs/DAY3_POLICY_GATE_REGRESSION_REPORT_v1.0.md`、`docs/DAY3_POLICY_GATE_EXEC_SUMMARY_v1.0.md`
    - 更新内容：
      - 将全量回归通过数从 `138 passed` 更新为本轮实测的 `191 passed`
      - 同步更新一页摘要中“矩阵专项/全量”通过数口径，保持统计一致
    - 本轮回归执行：
      - Day3 门禁矩阵（marker）：`cd backend && python -m pytest -m day3_gate -q --tb=short`
      - 结果：`33 passed, 158 deselected`
      - 全量回归：`cd backend && python -m pytest tests/ -q --tb=short`
      - 结果：`191 passed in 194.42s (exit_code=0)`
    - 统计口径：
      - `day3_gate` 仅执行 Day3 策略门禁矩阵/一致性相关用例
      - 全量回归统计 `tests/` 下所有用例的通过数，用于发布前 Go/No-Go 的“稳定性证明”
    - 推送结果：
      - 第 1 次推送成功：`ba4fb4d..59761da  main -> main`

129. Day4/Day5 发布前收口产物与 Go/No-Go 决策落地（文档交付）
    - 文件：
      - `docs/D3_RELEASE_REHEARSAL_RECORD_20260416_r1.md`
      - `docs/D5_GO_NO_GO_REVIEW_MEMO_20260416_r1.md`
      - `docs/D5_RELEASE_DUTY_SCHEDULE_20260416_r1.md`
      - `docs/DAY3_SECURITY_APPROVAL_SAMPLING_REPORT_v1.0.md`（更新统计口径）
      - `docs/DAY3_POLICY_GATE_REGRESSION_REPORT_v1.0.md`、`docs/DAY3_POLICY_GATE_EXEC_SUMMARY_v1.0.md`（更新门禁回归统计口径）
    - 接口字段：本轮为发布门禁/演练/决策文档，无新增运行时 API 字段（接口契约以既有回归验证为准）。
    - 统计口径/映射规则（仅文档引用）：
      - `day3_gate`：只跑标记为 `day3_gate` 的 Day3 策略门禁矩阵/一致性用例
      - 全量回归：跑 `tests/` 下所有用例，用于发布前稳定性证明
      - 安全抽测：引用 `test_security_high_risk_approval_sampling_matrix` 的抽测用例集合与拒绝码机读断言
    - 测试结果（证据汇总）：
      - `cd backend && python -m pytest -m day3_gate -q --tb=short`：`33 passed, 158 deselected`
      - `cd backend && python -m pytest tests/ -q --tb=short`：`191 passed in 194.42s (exit_code=0)`
      - `cd backend && python -m pytest tests/test_policy_gate_matrix.py tests/test_api_smoke.py tests/test_marketing_api.py -q --tb=short`：`89 passed in 164.67s (exit_code=0)`
    - 推送结果：
      - 第 1 次推送失败：`Recv failure: Connection was reset`
      - 第 2 次推送成功：`898491c..cb69f57  main -> main`
