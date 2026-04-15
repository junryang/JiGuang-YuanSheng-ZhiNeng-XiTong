# 项目开发智能体集群开工令 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\DEVELOPMENT_CLUSTER_KICKOFF_v1.0.md`

## 一、开工结论

基于当前文档基线审查结果，项目满足正式开发启动条件，结论为 **GO**。

## 二、开工范围

- 执行基线：`DEVELOPMENT_PLAN_v1.0.md`（v1.2）
- 策略基线：`ceo_policy.engine.yaml`
- 测试门禁：`TEST_PLAN_v1.0.md` + `STRATEGY_TEST_CASES_v1.0.md`
- 范围边界：`PRD_v2.0.md`（In Scope / Out of Scope）

## 三、主脑下发指令（对智能体集群）

```yaml
order:
  issuer: "L1 主脑"
  status: "生效"
  start_mode: "正式开发"
  environment: "dev -> staging -> prod"

  assignments:
    - team: "项目部（L3/L4）"
      tasks:
        - "按阶段拆解WBS并锁定每日目标"
        - "维护风险看板与阻塞清单"
    - team: "后端部"
      tasks:
        - "优先交付 agents/projects/chat 核心API"
        - "接入策略引擎校验中间件"
    - team: "前端部"
      tasks:
        - "老板工作台、项目详情页、关键中心页联调"
    - team: "智能体部"
      tasks:
        - "完成主脑能力CEO-09~14运行接线"
        - "联通记忆治理、调度与降级策略"
    - team: "安全团队"
      tasks:
        - "落实 LAW-01~05 链路拦截与审计"
    - team: "测试团队"
      tasks:
        - "每次策略变更执行12条最小门禁用例"
        - "发版前执行24条全量策略用例"
```

## 四、门禁与升级条件

| 环境 | 必过项 | 升级条件 |
|---|---|---|
| dev | 核心API可用、策略可加载、日志可观测 | 连续3天无P0阻塞且最小策略集通过 |
| staging | 禁止组合拦截、LAW链路完整、降级演练通过 | 全量24条策略用例通过 + 关键链路回归通过 |
| prod | 高风险审批、审计完整、策略版本可追溯 | 老板/主脑联合放行 |

## 五、汇报节奏

- 频率：每日
- 路径：各团队 -> 主脑 -> 老板
- 固定字段：阶段进度、阻塞项、风险等级、策略命中/拦截统计、次日计划

## 六、版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-14 | 首版：正式开发开工结论与主脑下发集群指令 |
