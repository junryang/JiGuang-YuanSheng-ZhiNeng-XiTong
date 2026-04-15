# 主脑能力映射表 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\CEO_ABILITY_RUNTIME_MAPPING_v1.0.md`

## 一、用途

将 `LAYER_ABILITY_CONFIG_v1.0.md` 中主脑新增能力 `CEO-09`～`CEO-14`，映射到
`AGENT_ABILITY_SPEC_v1.0.md` 里的 `AGENT-RUNTIME-* / WEB-* / LAW-*`，
用于实现设计、验收与审计的一致性。

> 说明：本表是**映射与实现建议**，能力 ID 的权威定义仍以 `AGENT_ABILITY_SPEC_v1.0.md` 为准。

## 二、主脑新增能力对照表（主映射 / 备选映射 / 禁止组合）

| 主脑能力 | 目标 | 主映射（建议默认） | 备选映射（兜底） | 禁止组合（红线） |
|---|---|---|---|---|
| `CEO-09` 工具链编排 | 统一编排 MCP/内部工具/API，支持失败重试与回滚点 | `AGENT-RUNTIME-01` + `AGENT-RUNTIME-04` + `WEB-04` + `LAW-04` + `LAW-05` | `AGENT-RUNTIME-05` + `WEB-09` + `WEB-06` + `LAW-05` | 仅用 `WEB-*` 直接调用而不挂 `LAW-04/LAW-05`；或绕过运行时监控直接批量执行高风险动作 |
| `CEO-10` 上下文与记忆治理 | 多项目并行下维护工作集、摘要与记忆引用 | `AGENT-RUNTIME-06` + `AGENT-RUNTIME-11` + `LAW-02` + `LAW-05` | `AGENT-RUNTIME-02` + `WEB-07` + `LAW-02` | 使用外部存储/共享时缺失 `LAW-02`；将敏感上下文直接外发且无审计 |
| `CEO-11` 任务与注意力调度 | 对请求排队、限时、SLA 与优先级调度 | `AGENT-RUNTIME-04` + `AGENT-RUNTIME-09` + `AGENT-RUNTIME-03` + `LAW-05` | `AGENT-RUNTIME-01` + `WEB-04` + `LAW-05` | 调度决策不可解释（缺 `AGENT-RUNTIME-03`）且无审计；低优任务抢占 P0 任务无熔断 |
| `CEO-12` 委托与子目标封装 | 向 L2/L3 输出可验收目标包与回传契约 | `AGENT-RUNTIME-03` + `AGENT-RUNTIME-01` + `WEB-06` + `LAW-05` | `AGENT-RUNTIME-04` + `WEB-06` | 仅自然语言口头委托、无验收契约；跨层级委托无审计链路 |
| `CEO-13` 安全与合规总闸 | 高风险动作、外发数据、全网发现统一过闸 | `AGENT-RUNTIME-04` + `AGENT-RUNTIME-05` + `LAW-01` + `LAW-02` + `LAW-03` + `LAW-04` + `LAW-05` | `LAW-04` + `LAW-05`（仅限只读探测） | 出网检索/抓取缺 `LAW-04`；内容分发缺 `LAW-01`；素材二次加工缺 `LAW-03` |
| `CEO-14` 自我诊断与运行降级 | 主脑自身或工具链异常时自愈、降级、上报 | `AGENT-RUNTIME-05` + `AGENT-RUNTIME-11` + `AGENT-RUNTIME-04` + `LAW-05` | `WEB-09` + `AGENT-RUNTIME-05` | 故障时继续放行高风险动作；降级或回滚无审计记录 |

## 三、策略引擎规则模板（可直接改造成配置）

```yaml
policy_templates:
  - id: "CEO-POLICY-09"
    ceo_ability: "CEO-09"
    trigger: "主脑发起多工具编排任务"
    required:
      runtime: ["AGENT-RUNTIME-01", "AGENT-RUNTIME-04"]
      web: ["WEB-04"]
      law: ["LAW-04", "LAW-05"]
    optional:
      runtime: ["AGENT-RUNTIME-05"]
      web: ["WEB-06", "WEB-09"]
    deny_if:
      - "missing(LAW-04)"
      - "missing(LAW-05)"
    fallback: "降级为只读检查 + 人工审批"

  - id: "CEO-POLICY-10"
    ceo_ability: "CEO-10"
    trigger: "主脑执行上下文压缩/记忆持久化"
    required:
      runtime: ["AGENT-RUNTIME-06"]
      law: ["LAW-02", "LAW-05"]
    optional:
      runtime: ["AGENT-RUNTIME-11", "AGENT-RUNTIME-02"]
      web: ["WEB-07"]
    deny_if:
      - "sensitive_data && missing(LAW-02)"
    fallback: "仅保留本地短期摘要，不写外部存储"

  - id: "CEO-POLICY-11"
    ceo_ability: "CEO-11"
    trigger: "主脑执行任务优先级调度"
    required:
      runtime: ["AGENT-RUNTIME-04", "AGENT-RUNTIME-03"]
      law: ["LAW-05"]
    optional:
      runtime: ["AGENT-RUNTIME-09"]
      web: ["WEB-04"]
    deny_if:
      - "unexplainable_decision"
    fallback: "切换规则引擎保守调度"

  - id: "CEO-POLICY-12"
    ceo_ability: "CEO-12"
    trigger: "主脑向 L2/L3 进行目标委托"
    required:
      runtime: ["AGENT-RUNTIME-03", "AGENT-RUNTIME-01"]
      law: ["LAW-05"]
    optional:
      web: ["WEB-06"]
    deny_if:
      - "missing_acceptance_contract"
    fallback: "退回主脑补齐子目标包后再下发"

  - id: "CEO-POLICY-13"
    ceo_ability: "CEO-13"
    trigger: "出网搜索/外发内容/素材入库等高风险流程"
    required:
      runtime: ["AGENT-RUNTIME-04"]
      web: ["WEB-02", "WEB-03", "WEB-04"]
      law: ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"]
    optional:
      runtime: ["AGENT-RUNTIME-05"]
    deny_if:
      - "missing_any(LAW-01,LAW-02,LAW-03,LAW-04,LAW-05)"
    fallback: "仅保留外链，不入库，不自动分发"

  - id: "CEO-POLICY-14"
    ceo_ability: "CEO-14"
    trigger: "主脑健康度下降或工具链故障"
    required:
      runtime: ["AGENT-RUNTIME-05", "AGENT-RUNTIME-04"]
      law: ["LAW-05"]
    optional:
      runtime: ["AGENT-RUNTIME-11"]
      web: ["WEB-09"]
    deny_if:
      - "degraded_mode && high_risk_action"
    fallback: "进入降级模式并上报老板/值班负责人"
```

## 四、最小落地要求（建议）

1. 每个 `CEO-09`～`CEO-14` 能力在实现时至少绑定 1 个 `AGENT-RUNTIME-*` 主能力。  
2. 涉及联网与外部调用时，默认附带 `LAW-04` 检查，关键动作落 `LAW-05` 审计。  
3. 涉及内容/数据时，根据场景附加 `LAW-01`（内容）与 `LAW-02`（隐私）/`LAW-03`（版权）。  
4. 主脑降级与恢复流程必须在监控面可见，并可回放关键决策链路。

## 五、分环境策略细化（dev / staging / prod）

### 5.1 环境总原则

| 环境 | 目标 | 默认策略 |
|---|---|---|
| `dev` | 快速验证与研发效率 | 允许更多备选映射；高风险动作可模拟执行，但必须保留审计日志 |
| `staging` | 上线前验证 | 主映射优先；禁止组合全部拦截；故障演练与回滚路径必须可复现 |
| `prod` | 稳定与合规优先 | 仅允许主映射 + 受控备选；高风险默认需审批；严格执行 LAW 全链路 |

### 5.2 环境参数模板（可直接用于策略中心）

```yaml
environment_policy:
  dev:
    allow_optional_mapping: true
    high_risk_requires_approval: false
    allow_simulation_only_on_violation: true
    strict_law_bundle: false
    deny_on_missing_audit: true
    max_retry: 3

  staging:
    allow_optional_mapping: true
    high_risk_requires_approval: true
    allow_simulation_only_on_violation: false
    strict_law_bundle: true
    deny_on_missing_audit: true
    max_retry: 2

  prod:
    allow_optional_mapping: false
    high_risk_requires_approval: true
    allow_simulation_only_on_violation: false
    strict_law_bundle: true
    deny_on_missing_audit: true
    max_retry: 1
```

> 可执行配置草案已落盘：`docs/ceo_policy.engine.yaml`（策略中心可直接读取并按环境覆盖）。

### 5.3 六条 CEO 策略的环境化约束

| 策略 | dev | staging | prod |
|---|---|---|---|
| `CEO-POLICY-09` 工具链编排 | 允许 `WEB-06/09` 备选并行验证 | 主映射为主，备选需记录原因 | 主映射固定；备选仅在主链失败且审批通过 |
| `CEO-POLICY-10` 记忆治理 | 可写测试存储，需脱敏 | 脱敏 + 审计强制 | 敏感数据仅最小必要写入，缺 `LAW-02` 直接拒绝 |
| `CEO-POLICY-11` 调度 | 允许实验性调度算法 | 需可解释并与基线策略对比 | 仅允许可解释策略，禁止黑箱调度上线 |
| `CEO-POLICY-12` 委托封装 | 契约字段可半自动补全 | 契约字段完整性检查必过 | 契约不完整直接阻断下发 |
| `CEO-POLICY-13` 合规总闸 | 可做只读探测与模拟拦截 | LAW 全链路真实执行 | LAW 全链路 + 审批 + 审计三重强制 |
| `CEO-POLICY-14` 诊断降级 | 可自动切换到调试降级模式 | 必须验证恢复流程 | 高风险动作在降级态一律禁止，需人工确认恢复 |

### 5.4 推荐阈值（首版）

```yaml
thresholds:
  dev:
    ceo_error_rate: ">=5%"
    tool_fail_rate: ">=10%"
    p95_latency: ">=4s"
  staging:
    ceo_error_rate: ">=2%"
    tool_fail_rate: ">=5%"
    p95_latency: ">=3s"
  prod:
    ceo_error_rate: ">=1%"
    tool_fail_rate: ">=2%"
    p95_latency: ">=2s"
```

> 阈值作为起始配置，最终以运行数据和 `PRODUCTION_RUNTIME_ASSUMPTIONS_v1.0.md` 演练结果迭代。

## 六、版本记录

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.3 | 2026-04-14 | 新增 `docs/ceo_policy.engine.yaml` 可执行策略配置草案引用 |
| v1.2 | 2026-04-14 | 新增分环境策略（dev/staging/prod）、参数模板、阈值建议 |
| v1.1 | 2026-04-14 | 升级为主映射/备选映射/禁止组合，并增加策略引擎规则模板 |
| v1.0 | 2026-04-14 | 首版：CEO-09～CEO-14 到 AGENT-RUNTIME/WEB/LAW 映射 |
