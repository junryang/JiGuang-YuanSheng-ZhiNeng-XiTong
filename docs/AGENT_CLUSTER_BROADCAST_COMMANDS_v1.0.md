# 智能体集群广播指令 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\AGENT_CLUSTER_BROADCAST_COMMANDS_v1.0.md`

## 一、用途

本文件提供可直接发送给主脑的“正式开发阶段”广播指令，目标是让你之前创建的技能智能体集群按全量设计文件开工。

## 二、一键广播总指令（发给主脑）

```text
@docs/PROJECT_OVERVIEW_v1.0.md
@docs/PRD_v2.0.md
@docs/DOCS_MODULE_INDEX_v1.0.md
@docs/DEVELOPMENT_PLAN_v1.0.md
@docs/DEVELOPMENT_CLUSTER_KICKOFF_v1.0.md
@docs/DAY1_EXECUTION_TASKS_v1.0.md
@docs/DAY2_EXECUTION_TASKS_v1.0.md
@docs/DAY3_EXECUTION_TASKS_v1.0.md
@docs/WEEK1_EXECUTION_BLUEPRINT_v1.0.md
@docs/ceo_policy.engine.yaml
@docs/STRATEGY_TEST_CASES_v1.0.md

以这些文档为唯一基线，立即进入正式开发阶段：
1) 生成“全智能体集群任务分配表（按技能智能体）”；
2) 按 Day1 任务单立即开工并回报首批结果；
3) 启用策略门禁（CEO-POLICY-09~14），每次策略变更执行12条最小门禁用例；
4) 每日20:00输出汇总：进度、阻塞、风险、策略命中/拒绝统计、次日计划。
```

## 三、按技能智能体的分组开工指令

> 以下为“主脑 -> 技能智能体”分发模板。每条均可单独下发。

### A. 架构与主干实现

```text
指令对象：project-architecture-planner, backend-api-implementer, frontend-experience-builder, database-schema-governor
任务：按 PRD v2.0 与 DEVELOPMENT_PLAN v1.2 完成核心API、数据模型、前端骨架、主干架构联调。
交付：核心链路（agents/projects/chat）可运行，接口契约与数据模型一致，提交联调报告。
截止：Day1 结束前。
```

### B. 主脑策略与治理

```text
指令对象：agent-governance-manager, llm-orchestration-engineer, integration-connector-specialist, security-compliance-guardian
任务：落地 ceo_policy.engine.yaml，接入 CEO-POLICY-09~14，打通 LAW-01~05 合规链路与审批门禁。
交付：策略加载成功、拒绝路径可观测、审计字段完整（policy_id/version/reason/env）。
截止：Day2 结束前。
```

### C. 测试与质量门禁

```text
指令对象：test-strategy-designer, quality-standards-auditor, monitoring-observability-analyst
任务：执行 STRATEGY_TEST_CASES（最小12条 -> 全量24条），建立策略与核心链路回归门禁。
交付：测试报告、失败复现步骤、修复建议、门禁通过结论。
截止：Day2~Day3 持续。
```

### D. 发布与运行保障

```text
指令对象：deployment-release-manager, performance-optimization-engineer, automation-workflow-designer
任务：完善 dev/staging/prod 发布清单、回滚预案、性能与告警阈值、自动化流水线门禁。
交付：发布前检查清单、回滚演练结果、性能与稳定性基线报告。
截止：Day3 结束前。
```

### E. 项目调度与文档同步

```text
指令对象：project-plan-executor, project-roadmap-owner, department-capability-coordinator, documentation-maintainer
任务：跟踪日任务完成度、跨团队依赖、文档与实现一致性；每日更新里程碑状态。
交付：日报与里程碑看板，文档差异清单（如有）及修订建议。
截止：每日20:00前。
```

### F. 业务域并行推进（营销/内容/分发/数据）

```text
指令对象：marketing-campaign-engineer, content-creation-orchestrator, multi-platform-distribution-lead, data-insight-analyst, customer-service-assistant-engineer, domain-routing-specialist
任务：按营销、客服、分发与数据模块设计文档并行开发接口与流程，保证与主干策略门禁兼容。
交付：模块联调结果、场景验收记录、与主脑策略冲突清单（如有）。
截止：Day3~Week1 持续。
```

## 四、回执格式（强制）

```yaml
cluster_feedback:
  date: "YYYY-MM-DD"
  team_or_skill_agent: ""
  completed:
    - ""
  blocked:
    - ""
  risk_level: "low|medium|high"
  policy_stats:
    hits: 0
    denies: 0
    top_reasons: []
  next_day_plan:
    - ""
```

## 五、版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-14 | 首版：可直接发送给主脑的集群广播开工指令 |
