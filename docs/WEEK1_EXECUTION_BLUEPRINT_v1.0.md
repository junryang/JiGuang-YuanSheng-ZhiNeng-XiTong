# 首周执行蓝图 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\WEEK1_EXECUTION_BLUEPRINT_v1.0.md`

## 一、目的

把 Day1~Day3 的任务串成一条可落地的首周推进链，确保“开发、策略、测试、运维”同步推进。

## 二、周目标（Week 1）

1. 核心 API 骨架可运行（agents/projects/chat）。  
2. 主脑策略链路（CEO-POLICY-09~14）在 dev/staging 具备可观测与可拦截能力。  
3. 全量策略测试用例可执行并形成稳定报告。  
4. 具备 staging→prod 的发布前置清单与回滚入口。

## 三、日程编排

| 日期 | 任务文档 | 重点 |
|---|---|---|
| Day1 | `DAY1_EXECUTION_TASKS_v1.0.md` | 骨架搭建、策略接入、最小门禁 |
| Day2 | `DAY2_EXECUTION_TASKS_v1.0.md` | 双路径推进（顺利/阻塞）与策略深化 |
| Day3 | `DAY3_EXECUTION_TASKS_v1.0.md` | staging 收口、风控闭环、发布清单草案 |
| Day4 | （由主脑根据前三天日报生成） | 缺陷消减 + 关键链路加固 |
| Day5 | （由主脑根据门禁结果生成） | 首周复盘 + 下周迭代计划 |

## 四、统一门禁（首周）

```yaml
week1_gates:
  functional:
    - "核心链路可跑通"
    - "关键接口成功率达标"
  policy:
    - "CEO-POLICY-09~14 可加载并可追溯"
    - "禁止组合拦截有效"
  compliance:
    - "LAW链路按场景触发"
    - "审计事件完整"
  release_ready:
    - "staging 回归通过"
    - "发布与回滚清单完成"
```

## 五、汇报机制

- 日报：团队 -> 主脑（固定模板）  
- 晚间汇总：主脑 -> 老板（风险、进度、次日计划）  
- 周复盘：输出“首周完成度 + 下周优先级调整”

## 六、版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-14 | 首版：整合 Day1~Day3 为首周执行蓝图 |
