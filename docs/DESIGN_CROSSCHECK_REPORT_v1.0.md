# 设计文档交叉审查报告 v1.0

## 文件路径

`d:\BaiduSyncdisk\JiGuang\docs\DESIGN_CROSSCHECK_REPORT_v1.0.md`

## 一、审查范围与方法

- **范围**：`docs/` 下与产品、模块、UI、API、性能、组织相关的设计基线；**重点**：营销中心（`MARKETING_MODULE_v1.0.md`、`UI_MARKETING_CENTER_v1.0.md`）与项目中心（`PROJECT_MANAGEMENT_MODULE_v1.0.md`、`UI_PM_CENTER_v1.0.md`、`PROJECT_PLAN_TEMPLATE_v1.0.md`）。
- **方法**：对照 `DOCUMENTATION_BASELINE_v1.0.md`、`ORGANIZATION_ARCHITECTURE_v1.0.md`、`API_REFERENCE_v1.0.md`、`ENDPOINT_MAPPING_v1.0.md`、`ACCEPTANCE_CHECKLIST_v1.0.md` 做标识符与口径一致性检查。第二轮对 `docs/*.md` 全量检索关键词（项目编号、占位符、能力分母等）并交叉核对 `DOCS_MODULE_INDEX_v1.0.md`。

## 二、已修复的缺陷（累计落盘）

| 编号 | 问题 | 处理 |
|------|------|------|
| D1 | `PROJECT_MANAGEMENT_MODULE_v1.0.md` 中项目 ID 写为 `PRJ-YYYY-XXX`，与 `PROJECT_PLAN_TEMPLATE_v1.0.md` 及 UI 示例中的 `JYIS-YYYY-XXX` 冲突 | 模块内统一为 **JYIS-YYYY-XXX** |
| D2 | 营销中心模块 `owner: L4 营销主管` 与界面中「营销总经理」审批线易混淆 | 在 `MARKETING_MODULE_v1.0.md` 增加 `owner_note`，明确重大审批以 **L2 营销总经理** 为准 |
| D3 | `UI_MARKETING_CENTER` 未说明 MK-01 与 PERF-01、外部账号专档的关系 | 在基线约束中补充 PERF-01 对应关系及 `UI_EXTERNAL_ACCOUNTS_CENTER` 跳转说明 |
| D4 | `UI_PM_CENTER` 领域筛选仅展示 D01–D05，易被理解为仅有四域 | 基线约束中说明 **D01–D08** 全量及快捷筛选仅为示例 |
| D5 | `PROJECT_OVERVIEW_v1.0.md`、`CHAT_SYSTEM_MODULE_v1.0.md` 仍使用 `PRJ-*` 作为项目编号示例 | 已改为 **JYIS-2026-001**；`DOCUMENTATION_BASELINE_v1.0.md` 增加项目编号统一规则 |

## 三、营销中心专项结论

**合理之处**

- 功能 ID（MK-01、MK-14～17 等）与 `ACCEPTANCE_CHECKLIST_v1.0.md`、`API_REFERENCE_v1.0.md`、`ENDPOINT_MAPPING_v1.0.md` 可对应。
- 「智能洞察」标注 CG-01 与 `AGENT_ABILITY_SPEC_v1.0.md` 中认知能力一致。

**仍须实施时注意的点（非文档错误）**

- **数据依赖**：粉丝、互动、用户画像等依赖各平台数据接入；`MARKETING_MODULE` 中多平台 `status: planned` 与 UI 中「已连接」展示并存时，应以**实际接入里程碑**区分原型与上线状态。
- **与财务口径**：**已处理**——见 `DATA_ANALYTICS_INSIGHT_v1.0.md` 第 1.1 节及两中心 UI 基线引用。

## 四、项目中心专项结论

**合理之处**

- 项目状态机（草稿、待审批、进行中等）与 PM-01 等流程在 `PROJECT_MANAGEMENT_MODULE_v1.0.md` 中定义完整。
- 详情页中里程碑、风险、资源与 `PROJECT_LIFECYCLE_SPEC_v1.0.md` 方向一致。

**仍须实施时注意的点**

- **「21人」表述**：原型中为岗位/智能体编制数；若含人类员工，需在权限与组织模块中区分 **人类账号 vs 智能体岗位**，避免审计歧义（建议在实现 `UI_PM_CENTER` 时增加图例或术语表）。
- **项目与营销联动**：「内容营销自动化」等项目出现在 PM 列表时，与 `UI_MARKETING_CENTER` 的战役/内容对象应通过**项目 ID 或标签**关联，设计层可在后续 `ENDPOINT_MAPPING` 增量中补充关联字段。

## 五、全局性观察（迭代状态）

| 观察 | 说明 | 状态 |
|------|------|------|
| 顶栏导航不一致 | 指挥舱与各业务中心线框顶栏项不完全相同 | **已处理**：`UI_UX_DESIGN_v1.0.md` 增加「全局壳导航规范（顶栏）」全量业务壳与指挥舱摘要壳说明 |
| 营销 vs 财务收入口径 | 两中心均可能出现「收入」类指标 | **已处理**：`DATA_ANALYTICS_INSIGHT_v1.0.md` 第 1.1 节定义运营视图与财务账口径及对账关系；`UI_MARKETING_CENTER`、`UI_FINANCE_CENTER` 基线已引用 |
| 能力数量展示 | `UI_CAPABILITY_CENTER` 等处固定数字（如 142）易与 `AGENT_ABILITY_SPEC` 演进漂移 | 待实现阶段改为「基线版本 + 数量」或配置驱动 |
| 设计覆盖扩展 | 评测看板、事故降级等 | 见 `DESIGN_COVERAGE_AND_EXTENSIONS_v1.0.md`，分阶段纳入 |
| 文档索引覆盖 | 大量技能/集成类文档未出现在主索引 | **已处理**：`DOCS_MODULE_INDEX_v1.0.md` 新增第八节扩展索引 |

## 六、全量扫描：残余风险与可优化项（设计层）

以下不阻塞当前基线，建议在后续迭代处理。

| 类型 | 说明 | 建议 |
|------|------|------|
| 超大单文件 | `AGENT_ABILITY_SPEC_v1.0.md` 体量极大 | 已符合「拆分计划登记」原则；新增能力优先走附录/扩展文档再合并 |
| 归档与主文档 | `UI_UX_DESIGN_v1.0.archive_before_slim.md` 中仍含历史不一致片段（如 `142/210`） | 归档只读、不强制改；**以当前 `UI_*_CENTER` 与能力基线为准** |
| 能力分母 142 | 多处 UI/测试计划写死「142」 | 展示与自动化改为「基线版本号 + 动态计数」或配置项 |
| 智能体管理 UI | `UI_AGENT_MANAGEMENT_CENTER` 中「58/142」与主脑「142/142」并存 | **已处理**：`UI_AGENT_MANAGEMENT_CENTER_v1.0.md` 基线约束说明为子集激活，非错误 |
| API/架构版本脚注 | `API_REFERENCE`、`ARCHITECTURE` 等含「238 端点、142 能力」等汇总 | 随实现变更时同步修订表头版本记录，避免与真实代码漂移 |
| 工程 tasks | `tasks.md` 为执行清单，非规范 | 与 `DOCS_MODULE_INDEX` 第八节说明一致，勿当作验收基线 |

## 七、版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.2 | 2026-04-14 | 全量扫描：D5 项目编号、`DOCS_MODULE_INDEX` 扩展索引、第六节残余与优化项 |
| v1.1 | 2026-04-14 | 登记顶栏规范与营销-财务口径已落盘至 `UI_UX_DESIGN`、`DATA_ANALYTICS_INSIGHT` |
| v1.0 | 2026-04-14 | 首版：营销与项目中心重点审查 + 全局观察 + 已修复项登记 |
