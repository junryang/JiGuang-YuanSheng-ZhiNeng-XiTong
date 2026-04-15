# 设计覆盖与扩展 v1.0

## 文件存放路径

```
d:\BaiduSyncdisk\JiGuang\docs\DESIGN_COVERAGE_AND_EXTENSIONS_v1.0.md
```

## 一、结论摘要

1. **工具库（技能库结构）**  
   - `SKILL_LIBRARY_STRUCTURE_v1.0.md` 对**按部门划分的编码类技能**（common、backend、agent、testing、data、devops、security 等）覆盖较完整。  
   - 与「智能体运行时可调用工具」**未形成一等结构**：MCP/统一适配器、浏览器沙箱、代码工作区、可观测性与特性开关、审批与配额等，原先散落在各部门或隐含在实现中。  
   - **已在同一文档中补充** `runtime_integrations/` 目录约定，与执行期工具链对齐。
   - **层级与主脑**：自上而下传导与 **L1 主脑工具智能化**（编排、记忆、调度、合规总闸）以 `LAYER_ABILITY_CONFIG_v1.0.md`「一点五」及 CEO-09～CEO-14 为设计约束，与运行时集成层相互印证。

2. **界面设计**  
   - 指挥舱、对话、九大中心（项目、财务、营销、调研、能力/工具、外部工具与权限、外部账号、安全、智能体管理）已形成**主干信息架构**，与老板/高管「态势感知 + 专项纵深」分工匹配。  
   - **缺口**集中在生产治理与闭环：**评测与回归看板、事故/降级与 SRE 态势、模型与工具成本配额、特性开关与灰度、数据血缘与高风险操作留痕**。建议以「嵌入现有中心 + 少量新模块片段」方式补齐，避免界面碎片化。

3. **与能力体系合并优化**  
   - 下列 **P0/P1/P2** 与工具库/UI 缺口一一映射；正式 **能力 ID** 须在 `AGENT_ABILITY_SPEC_v1.0.md` 中单条立项并补全 YAML 后，方可作为基线引用。  
   - `AGENT_ABILITY_SPEC_v1.0.md` **第二十八节**提供索引表；本文件为展开说明与实施顺序。

---

## 二、工具库完整性分析

### 2.1 双层模型（必须区分）

| 层级 | 含义 | 主要文档 |
|------|------|----------|
| **部门技能库** | 智能体「会什么」——研发、测试、营销等可编排的编码/流程技能模块 | `SKILL_LIBRARY_STRUCTURE_v1.0.md` 中 `common/`～`hardware/` |
| **运行时工具与集成** | 智能体「调什么」——MCP、浏览器、Git、监控、审批闸等执行期适配与安全边界 | 同文档中 `runtime_integrations/`（v1.0 起） |

二者关系：部门技能实现业务；运行时工具提供**受控的执行面**。设计框架要同时覆盖两层，否则会出现「规范里只有技能、运行时工具无处登记」的断层。

### 2.2 原结构缺口与补全

| 缺口 | 说明 | 补全方式 |
|------|------|----------|
| MCP / OpenAPI 适配器 | 与 `THIRD_PARTY_INTEGRATION`、`UI_EXTERNAL_TOOLS` 呼应 | `runtime_integrations/mcp/` |
| 浏览器自动化 | 与 `WEB-01` 等能力呼应，需沙箱与会话策略 | `runtime_integrations/browser/` |
| 代码与变更 | 与自主开发、工作区隔离相关 | `runtime_integrations/scm/` |
| 可观测与特性开关 | 与 `PRODUCTION_RUNTIME_ASSUMPTIONS`、降级策略呼应 | `runtime_integrations/observability/` |
| 审批、配额、血缘登记 | 与高风险工具调用、合规留痕呼应 | `runtime_integrations/governance/` |

### 2.3 与 `SKILL_DEFINITION_SPEC` 的关系

- 技能元数据中的 `execution.requires_approval`、`allowed_agents`、`timeout_seconds` 等字段，应与 **governance** 工具策略一致。  
- 新增运行时工具时，建议在技能定义中增加 **tool_binding**（或等价字段）的约定，见该规范后续迭代；当前以本文件与技能库目录为**设计层**对齐即可。

---

## 三、界面设计合理性分析

### 3.1 已合理覆盖的部分

- **全局指挥舱**：战略进度、核心指标、项目健康度、智能体团队、财务趋势、活动流——满足「一眼掌控」。  
- **能力库与工具库中心**：能力统计、缺口告警、工具/模型库入口——与能力基线文档衔接明确。  
- **外部工具与权限、安全中心、智能体管理**：权限、审计、账号、安全态势与智能体生命周期——与生产假设文档方向一致。

### 3.2 建议补充的界面能力（不强制拆成独立「第十个中心」）

| 补充项 | 建议落点 | 说明 |
|--------|----------|------|
| **评测与回归看板** | `UI_AGENT_MANAGEMENT_CENTER_v1.0.md` 或 `UI_CAPABILITY_CENTER_v1.0.md` 增一节 | 对齐 `AGENT_MATURITY_MODEL`、`validation_benchmarks`；展示通过率、回归任务、基线对比 |
| **事故 / 降级 / SRE 态势** | `UI_SECURITY_CENTER_v1.0.md` 或指挥舱「需要关注」旁路模块 | 对齐 `PRODUCTION_RUNTIME_ASSUMPTIONS_v1.0.md`：当前降级级别、人工接管、RTO 相关提示 |
| **成本与配额（模型 + 工具）** | `UI_FINANCE_CENTER_v1.0.md` 已有模型费用；**补充工具调用配额/成本** | 与预算告警、L2 负载联动 |
| **特性开关与灰度** | `UI_AGENT_MANAGEMENT_CENTER_v1.0.md` 或系统设置片段 | 与发布、回滚、成熟度分级一致 |
| **数据血缘与高风险留痕** | `UI_SECURITY_CENTER_v1.0.md` + 审批流 | 支撑合规审计与事后追溯 |

### 3.3 导航与一致性

- 九大中心 + 指挥舱已较多，新增能力宜采用 **标签页或二级面板** 嵌入现有中心，并在 `UI_UX_DESIGN_v1.0.md` 入口摘要中增加一句「生产治理类视图见各中心扩展节」。  
- `UI_CAPABILITY_CENTER` 中统计数字（如 142）须与 `AGENT_ABILITY_SPEC` **同步修订**，避免展示层与基线漂移。

---

## 四、与能力建议合并的映射表（P0 / P1 / P2）

以下合并**此前缺口分析中的能力建议**与本文件的**工具/UI 缺口**，便于统一排期。正式 ID 以能力规范立项为准。

| 优先级 | 域 | 能力/机制方向（候选描述） | 工具库落点 | 界面落点 |
|--------|----|---------------------------|------------|----------|
| **P0** | 安全与运行时 | 工具/MCP 沙箱、提示注入纵深防御、高风险调用审批 | `runtime_integrations/mcp`、`governance` | 安全中心 + 外部工具权限 |
| **P0** | 可观测与事故 | 结构化事故响应、运行降级与健康度 | `runtime_integrations/observability`、devops/monitor | SRE 态势片段 + 指挥舱告警 |
| **P0** | 评测与质量 | 智能体/流水线评测、回归与门禁 | testing + agent 编排 | 评测看板 |
| **P1** | 数据治理 | 数据血缘、敏感分级、留痕 | `data/`、`runtime_integrations/governance` | 安全中心 + 审批 |
| **P1** | 多租户与配额 | 租户隔离、模型与工具配额 | `governance`、backend | 财务 + 系统设置 |
| **P1** | 供应链与适配器 | 第三方/MCP 版本与健康探活 | `runtime_integrations/mcp` | 外部工具中心 |
| **P2** | 成本优化 | 路由与缓存、批处理策略 | `ai_model/inference`、observability | 财务中心 |
| **P2** | 组织与流程 | 跨部门能力协调的显式工作流 | product、department 技能 | 项目管理 / 报告 |

---

## 五、维护规则

1. 本文件与 `SKILL_LIBRARY_STRUCTURE_v1.0.md`、`UI_*_CENTER_v1.0.md`、`AGENT_ABILITY_SPEC_v1.0.md` 变更时**交叉检查**一节内映射是否仍成立。  
2. 新增「候选能力」时，先更新本文件第四节与 `AGENT_ABILITY_SPEC` 第二十八节索引，再单独立项写入完整能力条目。  
3. 本文件**不**作为能力 ID 的授权来源；唯一基线仍为 `AGENT_ABILITY_SPEC_v1.0.md`。

---

## 六、版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-04-14 | 首版：工具库双层模型、UI 缺口、与 P0–P2 能力映射 |
