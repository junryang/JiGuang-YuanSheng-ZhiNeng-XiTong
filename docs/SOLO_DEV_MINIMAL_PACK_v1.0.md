# 单人开发最小必读包 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\SOLO_DEV_MINIMAL_PACK_v1.0.md`

## 1. 适用场景

适用于“超级个体自用、无需上线”的日常开发。  
目标：以最小文档成本维持本地可用性、可回滚性与可持续迭代。

## 2. 必读 3 份（仅保留）

1. **工作流主文档**  
   `docs/SELF_HOSTED_DEV_WORKFLOW_v1.0.md`
2. **本地稳定性执行包（总入口）**  
   `docs/D3_RELEASE_PACKAGE_v1.0.md`
3. **Day3 执行任务单（当前阶段目标）**  
   `docs/DAY3_EXECUTION_TASKS_v1.0.md`

> 日常只看这三份即可，其他文档按需查阅。

## 3. 建议执行节奏（轻量）

- 开始开发前：看 `SELF_HOSTED_DEV_WORKFLOW_v1.0.md`
- 改动完成后：按 `D3_RELEASE_PACKAGE_v1.0.md` 做最小回归与归档
- 阶段回顾时：对照 `DAY3_EXECUTION_TASKS_v1.0.md` 更新进度

## 4. 最小命令集

```bash
# 1) 快速冒烟
python -m pytest tests/test_api_smoke.py -q --tb=short

# 2) 策略相关改动
python -m pytest -m day3_gate -q --tb=short

# 3) 阶段性全量
python -m pytest tests/ -q --tb=short
```

## 5. 可选参考（非必读）

- Runbook/排班/评审/纪要模板与样例均可保留归档，不作为日常必做
- 只有在你需要“演练式”管理时再启用

## 6. 版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0 | 2026-04-15 | 首版：单人开发最小必读包（三份） |
