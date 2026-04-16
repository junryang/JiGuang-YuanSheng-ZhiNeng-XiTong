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
