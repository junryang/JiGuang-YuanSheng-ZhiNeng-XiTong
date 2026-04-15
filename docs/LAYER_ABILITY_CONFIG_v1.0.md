# 按层级的能力配置 v1.0 - 完整版

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\LAYER_ABILITY_CONFIG_v1.0.md
```


# 按层级的能力配置 v1.0

## 一、层级能力总览

```yaml
# 七层组织架构能力配置

layers:
  L0:
    name: "老板"
    type: "human"
    description: "战略决策者，不直接执行智能体能力"
    
  L1:
    name: "CEO"
    codename: "主脑"
    type: "agent"
    description: "战略级智能体，负责全局规划与协调"
    
  L2:
    name: "总经理"
    type: "agent"
    description: "领域级智能体，负责特定领域管理"
    
  L3:
    name: "经理"
    type: "agent"
    description: "项目级智能体，负责具体项目执行"
    
  L4:
    name: "主管"
    type: "agent"
    description: "部门级智能体，负责技术质量把控"
    
  L5:
    name: "员工"
    type: "agent"
    description: "执行级智能体，负责具体任务执行"
    
  L6:
    name: "实习"
    type: "agent"
    description: "辅助级智能体，负责辅助支持"
```

## 一点五、自上而下能力传导与主脑工具智能化（设计约束）

本节约束**全层级**的能力建设方向：上层输出的是**可验证的目标、边界与优先级**；下层在边界内强化**执行与专业工具**。**主脑（L1）**处于负荷与决策最密集的一层，必须在工程上优先保证其**工具链智能化、编排能力与可观测性**，否则自上而下传导会失真。

### 1. 传导链（L0→L6）

| 层级 | 对上承接 | 对下输出 | 工具强度期望 |
|------|-----------|-----------|----------------|
| **L0 老板** | 外部环境 | 战略意图、预算与风险承受度 | 人脑 + 指挥舱（态势） |
| **L1 主脑** | L0 | 可量化目标、策略包、资源与优先级、跨域协调结论 | **最高**：编排、记忆、MCP/工具总线、队列与降级 |
| **L2 总经理** | L1 | 领域路线图、项目组合与领域资源方案 | 高：领域工具栈、模板库 |
| **L3 经理** | L2 | WBS、里程碑、项目风险与变更 | 中高：项目管理与协作工具 |
| **L4 主管** | L3 | 技术方案与质量门禁、团队分工 | 中：评审/CI/静态分析集成 |
| **L5 员工** | L4 | 交付物（代码/文档/测试等） | 中高：IDE、专项自动化 |
| **L6 实习** | L5 | 辅助产出与整理 | 中：在监护下使用受限工具 |

### 2. 主脑（L1）为何必须「能力 + 工具」双强化

- **工作量大**：并行处理多领域立项、异常、汇报与跨域依赖，纯对话式推理不足以保证时延与一致性。  
- **责任集中**：L1 的失误会放大为全系统偏差，需**可回放、可审计、可降级**的工具路径。  
- **实现要点**（与 `SKILL_LIBRARY_STRUCTURE_v1.0.md` 中 `runtime_integrations/`、`DESIGN_COVERAGE_AND_EXTENSIONS_v1.0.md` 一致）：工具/MCP 统一编排、审批与配额、记忆与上下文治理、观测与熔断。

### 3. 与基线文档关系

- 通用能力 ID 仍以 `AGENT_ABILITY_SPEC_v1.0.md` 为准；本节 **CEO-xx** 为**层级职责与工具期望**，实现时映射到运行时能力与工具策略。  
- 角色指令补充见 `AGENT_ORG_SPEC_v1.0.md` 主脑章节。  
- 具体映射表见 `CEO_ABILITY_RUNTIME_MAPPING_v1.0.md`（CEO-09～CEO-14 对照 AGENT-RUNTIME/WEB/LAW）。


## 二、能力定义格式

```yaml
ability_format:
  id: "唯一标识"
  name: "能力名称"
  layer: "适用层级"
  description: "能力描述"
  input: "输入说明"
  output: "输出说明"
  implementation: "实现方式"
  priority: "P0|P1|P2"
```


## 三、L1 CEO（主脑）- 战略级能力

```yaml
layer: "L1"
name: "CEO"
codename: "主脑"
description: "战略级智能体，理解老板意图，拆解目标，分配资源，协调多领域"

abilities:
  - id: "CEO-01"
    name: "战略规划"
    description: "理解老板的战略意图，制定长期发展规划"
    input: "老板的宏观指令"
    output: "战略规划文档、里程碑计划"
    implementation: "大模型 + 战略知识库"
    priority: "P0"
    
  - id: "CEO-02"
    name: "意图拆解"
    description: "将模糊的老板意图拆解为清晰可执行的目标"
    input: "自然语言指令"
    output: "结构化目标列表"
    implementation: "意图识别 + 任务分解"
    priority: "P0"
    
  - id: "CEO-03"
    name: "资源分配"
    description: "根据优先级分配计算资源、API配额、人力"
    input: "资源需求和优先级"
    output: "资源分配方案"
    implementation: "资源调度算法"
    priority: "P0"
    
  - id: "CEO-04"
    name: "多领域协调"
    description: "协调不同领域间的资源、信息和任务"
    input: "跨领域冲突或依赖"
    output: "协调方案"
    implementation: "冲突解决 + 协商机制"
    priority: "P0"
    
  - id: "CEO-05"
    name: "立项审批"
    description: "审批总经理提交的项目立项申请"
    input: "项目计划书"
    output: "审批结论（批准/驳回/修改）"
    implementation: "规则引擎 + 风险评估"
    priority: "P0"
    
  - id: "CEO-06"
    name: "结果汇报"
    description: "向老板汇报整体进展和重要成果"
    input: "各领域汇总数据"
    output: "汇报报告"
    implementation: "摘要生成 + 可视化"
    priority: "P0"
    
  - id: "CEO-07"
    name: "全局监控"
    description: "监控整个系统的运行状态"
    input: "系统指标"
    output: "监控报告"
    implementation: "监控聚合 + 异常检测"
    priority: "P1"
    
  - id: "CEO-08"
    name: "危机处理"
    description: "处理系统级别的紧急问题"
    input: "危机事件"
    output: "处理方案"
    implementation: "应急响应流程"
    priority: "P1"

  - id: "CEO-09"
    name: "工具链编排"
    description: "对 MCP/内部工具/API 进行统一编排、路由与失败重试；避免主脑在无工具辅助下手工拼接长链路"
    input: "目标与子任务、工具目录、约束"
    output: "可执行工具计划、调用图、回滚点"
    implementation: "运行时集成层 + 工具注册表 + 策略引擎"
    priority: "P0"

  - id: "CEO-10"
    name: "上下文与记忆治理"
    description: "在多项目并行下维护工作集、摘要与长期记忆引用，控制上下文窗口与遗忘策略"
    input: "会话流、项目事件、记忆检索需求"
    output: "压缩摘要、记忆指针、召回计划"
    implementation: "MEMORY_SYSTEM_SPEC + 分层摘要"
    priority: "P0"

  - id: "CEO-11"
    name: "任务与注意力调度"
    description: "对跨领域请求做优先级排队、期限与 SLA 提示，防止低优任务挤占战略任务"
    input: "任务流、截止日期、依赖"
    output: "排序队列、资源预留建议"
    implementation: "优先级队列 + 多臂老虎机/简单调度规则可插拔"
    priority: "P0"

  - id: "CEO-12"
    name: "委托与子目标封装"
    description: "向 L2/L3 输出边界清晰、可验收的子目标包（含输入输出契约），减少往返澄清"
    input: "战略拆解结果"
    output: "子目标包、验收标准、回传格式"
    implementation: "结构化模板 + 契约校验"
    priority: "P0"

  - id: "CEO-13"
    name: "安全与合规总闸"
    description: "对高风险工具调用、外发数据与全网发现类任务执行强制合规检查与审批路由"
    input: "拟执行动作、数据分级"
    output: "放行/拦截/升级老板"
    implementation: "LAW-* 能力组合 + 审批流"
    priority: "P0"

  - id: "CEO-14"
    name: "自我诊断与运行降级"
    description: "主脑自身负载、错误率与工具失败率超阈时触发自愈、降级或请求人类/主备切换"
    input: "健康指标、工具错误统计"
    output: "降级策略、告警"
    implementation: "AGENT-RUNTIME-05 + PRODUCTION_RUNTIME_ASSUMPTIONS"
    priority: "P0"
```


## 四、L2 总经理 - 领域级能力

```yaml
layer: "L2"
name: "总经理"
description: "领域级智能体，负责特定开发领域的整体规划和管理"

abilities:
  - id: "GM-01"
    name: "领域规划"
    description: "制定特定领域的发展规划和策略"
    input: "CEO的战略目标"
    output: "领域规划文档"
    implementation: "大模型 + 领域知识库"
    priority: "P0"
    
  - id: "GM-02"
    name: "项目立项审批"
    description: "审批经理提交的项目立项申请"
    input: "项目计划书"
    output: "审批结论"
    implementation: "规则引擎 + 领域评估"
    priority: "P0"
    
  - id: "GM-03"
    name: "跨项目资源调配"
    description: "在领域内多个项目间调配资源"
    input: "各项目资源需求"
    output: "资源调配方案"
    implementation: "资源调度 + 优先级排序"
    priority: "P0"
    
  - id: "GM-04"
    name: "领域风险管理"
    description: "识别和管理领域级的风险"
    input: "各项目风险报告"
    output: "风险应对方案"
    implementation: "风险分析模型"
    priority: "P1"
    
  - id: "GM-05"
    name: "领域汇报"
    description: "向CEO汇报领域整体进展"
    input: "各项目汇总数据"
    output: "领域汇报报告"
    implementation: "数据聚合 + 摘要生成"
    priority: "P0"
    
  - id: "GM-06"
    name: "领域标准制定"
    description: "制定领域内的技术标准和规范"
    input: "行业标准、团队经验"
    output: "领域规范文档"
    implementation: "规范模板 + 审核流程"
    priority: "P1"
    
  - id: "GM-07"
    name: "领域人才培养"
    description: "规划领域内的人才培养"
    input: "技能缺口分析"
    output: "培训计划"
    implementation: "学习路径规划"
    priority: "P2"
```


## 五、L3 经理 - 项目级能力

```yaml
layer: "L3"
name: "经理"
description: "项目级智能体，负责具体项目的执行管理"

abilities:
  - id: "PM-01"
    name: "项目计划"
    description: "制定详细的项目执行计划"
    input: "立项决议"
    output: "项目计划书（含时间、资源、预算）"
    implementation: "项目计划模板 + 大模型"
    priority: "P0"
    
  - id: "PM-02"
    name: "任务分解"
    description: "将项目目标分解为可执行的任务"
    input: "项目目标"
    output: "任务清单（WBS）"
    implementation: "WBS分解算法"
    priority: "P0"
    
  - id: "PM-03"
    name: "进度跟踪"
    description: "跟踪项目进度，识别偏差"
    input: "各任务进度数据"
    output: "进度报告、偏差预警"
    implementation: "甘特图 + 偏差检测"
    priority: "P0"
    
  - id: "PM-04"
    name: "风险识别"
    description: "识别项目执行中的风险"
    input: "项目状态、外部因素"
    output: "风险清单"
    implementation: "风险检测模型"
    priority: "P0"
    
  - id: "PM-05"
    name: "任务分配"
    description: "将任务分配给合适的主管或员工"
    input: "任务清单、团队能力"
    output: "任务分配方案"
    implementation: "能力匹配 + 负载均衡"
    priority: "P0"
    
  - id: "PM-06"
    name: "项目复盘"
    description: "项目完成后进行复盘总结"
    input: "项目执行数据"
    output: "复盘报告"
    implementation: "复盘模板 + 数据分析"
    priority: "P1"
    
  - id: "PM-07"
    name: "沟通协调"
    description: "协调项目内各部门的沟通"
    input: "跨部门问题"
    output: "协调方案"
    implementation: "会议管理 + 决策记录"
    priority: "P1"
    
  - id: "PM-08"
    name: "变更管理"
    description: "管理项目范围的变更"
    input: "变更请求"
    output: "变更评估、审批结果"
    implementation: "变更控制流程"
    priority: "P1"
```


## 六、L4 主管 - 部门级能力

```yaml
layer: "L4"
name: "主管"
description: "部门级智能体，负责技术方案评审、质量把控、团队技能管理"

abilities:
  - id: "LEAD-01"
    name: "技术方案评审"
    description: "评审技术方案的可行性和合理性"
    input: "技术方案文档"
    output: "评审意见（通过/修改/驳回）"
    implementation: "技术评审规则 + 大模型"
    priority: "P0"
    
  - id: "LEAD-02"
    name: "代码质量把控"
    description: "把控部门代码质量，审查关键代码"
    input: "代码变更"
    output: "代码审查意见"
    implementation: "代码审查规则 + 静态分析"
    priority: "P0"
    
  - id: "LEAD-03"
    name: "团队技能管理"
    description: "管理团队技能矩阵，识别技能缺口"
    input: "团队成员技能数据"
    output: "技能矩阵、培训计划"
    implementation: "技能图谱 + 差距分析"
    priority: "P1"
    
  - id: "LEAD-04"
    name: "技术难点攻关"
    description: "带领团队解决技术难点"
    input: "技术难题描述"
    output: "解决方案"
    implementation: "技术调研 + 方案设计"
    priority: "P0"
    
  - id: "LEAD-05"
    name: "部门工作分配"
    description: "将任务分配给部门内员工"
    input: "任务清单、员工能力"
    output: "工作分配方案"
    implementation: "能力匹配 + 负载均衡"
    priority: "P0"
    
  - id: "LEAD-06"
    name: "部门汇报"
    description: "向经理汇报部门工作进展"
    input: "各员工工作数据"
    output: "部门汇报报告"
    implementation: "数据聚合 + 摘要生成"
    priority: "P0"
    
  - id: "LEAD-07"
    name: "技术预研"
    description: "组织新技术预研和评估"
    input: "新技术方向"
    output: "技术评估报告"
    implementation: "技术调研 + 原型验证"
    priority: "P1"
    
  - id: "LEAD-08"
    name: "故障处理"
    description: "处理部门内的技术故障"
    input: "故障报告"
    output: "故障分析、解决方案"
    implementation: "故障排查流程"
    priority: "P1"
```


## 七、L5 员工 - 执行级能力

```yaml
layer: "L5"
name: "员工"
description: "执行级智能体，负责具体任务的执行"

abilities:
  - id: "EMP-01"
    name: "代码编写"
    description: "根据需求编写高质量代码"
    input: "技术方案、任务描述"
    output: "代码文件"
    implementation: "代码生成模型"
    priority: "P0"
    
  - id: "EMP-02"
    name: "代码修改"
    description: "修改现有代码，修复Bug或添加功能"
    input: "代码变更需求"
    output: "修改后的代码"
    implementation: "代码编辑 + 验证"
    priority: "P0"
    
  - id: "EMP-03"
    name: "单元测试执行"
    description: "编写和执行单元测试"
    input: "代码文件"
    output: "测试用例、测试报告"
    implementation: "测试生成 + 执行"
    priority: "P0"
    
  - id: "EMP-04"
    name: "文档撰写"
    description: "撰写技术文档、API文档、用户手册"
    input: "代码、设计文档"
    output: "文档文件"
    implementation: "文档生成模板 + 大模型"
    priority: "P0"
    
  - id: "EMP-05"
    name: "技术调研"
    description: "调研新技术、新工具"
    input: "调研主题"
    output: "调研报告"
    implementation: "搜索 + 信息整合"
    priority: "P1"
    
  - id: "EMP-06"
    name: "代码审查"
    description: "审查其他员工的代码"
    input: "代码变更"
    output: "审查意见"
    implementation: "代码审查规则"
    priority: "P0"
    
  - id: "EMP-07"
    name: "任务汇报"
    description: "向主管汇报任务执行情况"
    input: "任务执行数据"
    output: "任务汇报"
    implementation: "状态报告生成"
    priority: "P0"
    
  - id: "EMP-08"
    name: "问题排查"
    description: "排查和定位技术问题"
    input: "问题描述、日志"
    output: "问题分析报告"
    implementation: "日志分析 + 推理"
    priority: "P1"
    
  - id: "EMP-09"
    name: "数据查询"
    description: "执行数据库查询和数据提取"
    input: "查询需求"
    output: "查询结果"
    implementation: "SQL生成 + 执行"
    priority: "P1"
    
  - id: "EMP-10"
    name: "API调用"
    description: "调用内部和外部API"
    input: "API名称、参数"
    output: "API响应"
    implementation: "API客户端"
    priority: "P0"
```


## 八、L6 实习 - 辅助级能力

```yaml
layer: "L6"
name: "实习"
description: "辅助级智能体，负责辅助支持工作"

abilities:
  - id: "INT-01"
    name: "代码审查辅助"
    description: "辅助进行代码审查，发现常见问题"
    input: "代码文件"
    output: "代码问题列表"
    implementation: "静态分析 + 规则匹配"
    priority: "P0"
    
  - id: "INT-02"
    name: "日志分析"
    description: "分析系统日志，发现异常模式"
    input: "日志文件"
    output: "日志分析报告"
    implementation: "日志解析 + 模式识别"
    priority: "P0"
    
  - id: "INT-03"
    name: "文档整理"
    description: "整理和格式化文档"
    input: "原始文档"
    output: "格式化文档"
    implementation: "文档格式化工具"
    priority: "P0"
    
  - id: "INT-04"
    name: "知识检索"
    description: "从知识库中检索相关信息"
    input: "查询关键词"
    output: "相关知识片段"
    implementation: "向量检索 + RAG"
    priority: "P0"
    
  - id: "INT-05"
    name: "数据标注"
    description: "辅助标注训练数据"
    input: "待标注数据"
    output: "标注结果"
    implementation: "主动学习 + 人工审核"
    priority: "P1"
    
  - id: "INT-06"
    name: "问题分类"
    description: "对用户问题进行初步分类"
    input: "用户问题"
    output: "问题分类标签"
    implementation: "分类模型"
    priority: "P0"
    
  - id: "INT-07"
    name: "模板生成"
    description: "根据模板生成标准化文档"
    input: "模板名称、参数"
    output: "标准化文档"
    implementation: "模板引擎"
    priority: "P0"
    
  - id: "INT-08"
    name: "学习记录"
    description: "记录学习过程和成果"
    input: "学习内容"
    output: "学习记录"
    implementation: "笔记系统"
    priority: "P1"
    
  - id: "INT-09"
    name: "提醒管理"
    description: "管理提醒和待办事项"
    input: "待办事项"
    output: "提醒通知"
    implementation: "定时器 + 通知"
    priority: "P1"
    
  - id: "INT-10"
    name: "信息汇总"
    description: "汇总和整理信息"
    input: "多条信息"
    output: "汇总报告"
    implementation: "信息聚合"
    priority: "P1"
```


## 九、能力对比矩阵

```yaml
# 各层级能力对比

comparison_matrix:
  - ability_category: "战略规划"
    L1_CEO: "⭐⭐⭐ 全局战略"
    L2_GM: "⭐⭐ 领域战略"
    L3_PM: "⭐ 项目计划"
    L4_LEAD: "-"
    L5_EMP: "-"
    L6_INT: "-"
    
  - ability_category: "意图拆解"
    L1_CEO: "⭐⭐⭐ 老板意图"
    L2_GM: "⭐⭐ 领域需求"
    L3_PM: "⭐ 项目需求"
    L4_LEAD: "-"
    L5_EMP: "-"
    L6_INT: "-"
    
  - ability_category: "资源分配"
    L1_CEO: "⭐⭐⭐ 全局资源"
    L2_GM: "⭐⭐ 领域资源"
    L3_PM: "⭐ 项目资源"
    L4_LEAD: "-"
    L5_EMP: "-"
    L6_INT: "-"
    
  - ability_category: "任务分解"
    L1_CEO: "-"
    L2_GM: "-"
    L3_PM: "⭐⭐⭐ 项目分解"
    L4_LEAD: "⭐ 部门任务"
    L5_EMP: "-"
    L6_INT: "-"
    
  - ability_category: "进度跟踪"
    L1_CEO: "⭐ 整体进度"
    L2_GM: "⭐⭐ 领域进度"
    L3_PM: "⭐⭐⭐ 项目进度"
    L4_LEAD: "⭐ 部门进度"
    L5_EMP: "-"
    L6_INT: "-"
    
  - ability_category: "技术评审"
    L1_CEO: "-"
    L2_GM: "-"
    L3_PM: "-"
    L4_LEAD: "⭐⭐⭐ 方案评审"
    L5_EMP: "-"
    L6_INT: "-"
    
  - ability_category: "代码编写"
    L1_CEO: "-"
    L2_GM: "-"
    L3_PM: "-"
    L4_LEAD: "⭐ 关键代码"
    L5_EMP: "⭐⭐⭐ 日常开发"
    L6_INT: "-"
    
  - ability_category: "代码审查"
    L1_CEO: "-"
    L2_GM: "-"
    L3_PM: "-"
    L4_LEAD: "⭐⭐⭐ 审查"
    L5_EMP: "⭐⭐ 互审"
    L6_INT: "⭐ 辅助审查"
    
  - ability_category: "文档撰写"
    L1_CEO: "⭐ 战略文档"
    L2_GM: "⭐ 领域文档"
    L3_PM: "⭐⭐ 项目文档"
    L4_LEAD: "⭐ 技术文档"
    L5_EMP: "⭐⭐⭐ 代码文档"
    L6_INT: "⭐⭐ 文档整理"
    
  - ability_category: "知识检索"
    L1_CEO: "⭐⭐ 战略级检索"
    L2_GM: "⭐"
    L3_PM: "⭐"
    L4_LEAD: "⭐"
    L5_EMP: "⭐⭐"
    L6_INT: "⭐⭐⭐ 主要执行"

  - ability_category: "工具与集成编排"
    L1_CEO: "⭐⭐⭐ 总编排（MCP/运行时）"
    L2_GM: "⭐⭐ 领域工具栈"
    L3_PM: "⭐ 项目内自动化"
    L4_LEAD: "⭐ CI/评审工具"
    L5_EMP: "⭐⭐ 执行侧工具"
    L6_INT: "⭐ 受限工具"
    
  - ability_category: "问题排查"
    L1_CEO: "-"
    L2_GM: "-"
    L3_PM: "-"
    L4_LEAD: "⭐⭐ 指导"
    L5_EMP: "⭐⭐⭐ 执行"
    L6_INT: "⭐ 辅助"
```


## 十、能力统计汇总

```yaml
# 各层级能力数量统计

statistics:
  L1_CEO:
    total: 14
    P0: 12
    P1: 2
    P2: 0
    
  L2_GM:
    total: 7
    P0: 4
    P1: 2
    P2: 1
    
  L3_PM:
    total: 8
    P0: 5
    P1: 3
    P2: 0
    
  L4_LEAD:
    total: 8
    P0: 5
    P1: 3
    P2: 0
    
  L5_EMP:
    total: 10
    P0: 7
    P1: 3
    P2: 0
    
  L6_INT:
    total: 10
    P0: 6
    P1: 4
    P2: 0
    
  summary:
    total_abilities: 57
    total_P0: 39
    total_P1: 17
    total_P2: 1
```


## 十一、能力分配原则

```yaml
# 能力分配原则

principles:
  - name: "职责匹配"
    description: "能力与层级职责严格对应"
    
  - name: "权限最小化"
    description: "只赋予完成职责所需的最小能力"
    
  - name: "向上汇报"
    description: "低层级向高层级汇报，不可越级"
    
  - name: "向下授权"
    description: "高层级可向下授权部分能力"
    
  - name: "能力递进"
    description: "相同能力在不同层级强度不同"

  - name: "自上而下传导"
    description: "L1 主脑输出须可验收、可度量；L2–L6 在边界内强化专业与执行工具，避免反向架空战略"

  - name: "主脑工具智能化优先"
    description: "L1 必须优先建设工具编排、记忆治理、调度与合规总闸；禁止将主脑降级为纯聊天代理"
```


## 十二、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 查看所有层级能力
@docs/LAYER_ABILITY_CONFIG_v1.0.md 列出所有层级的能力配置

# 查看特定层级能力
@docs/LAYER_ABILITY_CONFIG_v1.0.md 查看L3经理的所有能力

# 实现特定能力
@docs/LAYER_ABILITY_CONFIG_v1.0.md 实现CEO-01战略规划能力

# 创建带能力的智能体
@docs/LAYER_ABILITY_CONFIG_v1.0.md 根据L5员工的能力配置，创建资深后端工程师智能体

# 生成能力对比报告
@docs/LAYER_ABILITY_CONFIG_v1.0.md 生成各层级能力对比报告
```

---

## 版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.1 | 2026-04-14 | 新增「一点五」自上而下传导；L1 扩展 CEO-09～CEO-14 与工具矩阵/统计更新 |
| v1.0 | - | 既有分层能力配置 |

**文档结束**