# 项目概述 - 纪光元生智能系统

**文件路径**: `docs/PROJECT_OVERVIEW_v1.0.md`


# 纪光元生智能系统（JYIS）项目概述


## 一、项目身份卡

```yaml
project:
  name: "纪光元生智能系统"
  name_en: "Jiguang Yuansheng Intelligent System"
  abbreviation: "JYIS"
  version: "v2.0"
  domain: "D03"
  domain_name: "多智能体协同软件开发"
  
description: |
  纪光元生智能系统是一个基于人机协同理念的多智能体开发平台。
  用户（老板）只需要与CEO智能体（主脑）对话，系统自动完成
  任务分解、分配、执行和汇报的全流程。

core_values:
  - "人机协同：你只对话CEO，CEO管理所有智能体"
  - "组织化智能体：七层企业架构，职级权限分明"
  - "自举进化：用系统开发系统自身，持续迭代"
  - "模型无关：支持任意大模型接入"
  - "记忆持久：跨会话保留经验和知识"

status:
  phase: "Phase 4 - D03领域开发"
  current_version: "v1.4.14_dev_actual"
  next_milestone: "纪光元生第四阶段完成"
```

## 1.1 目标口径（生产与研究双轨）

- 长期目标：构建与人类团队无差别的通用自主智能体系统。
- 生产口径：每个版本仅交付可验证、可回滚、可审计的能力子集。
- 发布门槛与范围冻结以 `PRD_v2.0.md` 为业务最高基线。


## 二、核心概念模型

### 2.1 人机协作模型

```yaml
human_role:
  name: "老板（BOSS）"
  level: 0
  responsibilities:
    - "战略决策"
    - "资源审批"
    - "最终验收"
  interaction: "仅与CEO智能体对话"

agent_ceo:
  name: "主脑"
  level: 1
  responsibilities:
    - "理解老板意图"
    - "拆解为可执行任务"
    - "分配资源给各领域"
    - "协调跨领域协作"
    - "汇总结果向老板汇报"

agent_hierarchy:
  level_1: "CEO智能体（主脑）- 战略层"
  level_2: "总经理智能体 - 领域层"
  level_3: "经理智能体 - 项目层"
  level_4: "主管智能体 - 部门层"
  level_5: "员工智能体 - 执行层"
  level_6: "实习智能体 - 辅助层"
```

### 2.2 智能体能力分层模型

```yaml
ability_distribution:
  shared_abilities:
    description: "所有智能体共享的基础能力"
    count: 47
    categories:
      - "感知能力（10项）"
      - "基础认知（4项）"
      - "基础执行（10项）"
      - "基础记忆（3项）"
      - "模型调用基础（10项）"
      - "安全基础（4项）"
      - "协作基础（2项）"
    
  tiered_abilities:
    description: "按层级分配的分层能力"
    count: 27
    categories:
      - "决策能力（9项）- 管理层专属"
      - "执行能力（4项）- 技术岗专属"
      - "记忆能力（3项）- 容量范围分层"
      - "模型配额（1项）- 用量分层"
      - "安全审计（2项）- 粒度分层"
      - "协作范围（3项）- 范围分层"
      - "认知强度（5项）- 强度递进"
```

### 2.3 组织架构模型

```yaml
organization:
  levels:
    - level: 0
      name: "老板"
      role: "human"
      permissions: "全部"
      report_to: null
      
    - level: 1
      name: "CEO智能体"
      role: "agent"
      codename: "主脑"
      permissions: "战略级"
      report_to: "老板"
      
    - level: 2
      name: "总经理智能体"
      role: "agent"
      naming: "{领域名称}总经理"
      permissions: "领域级"
      report_to: "CEO"
      
    - level: 3
      name: "经理智能体"
      role: "agent"
      naming: "{项目名称}经理"
      permissions: "项目级"
      report_to: "总经理"
      
    - level: 4
      name: "主管智能体"
      role: "agent"
      naming: "{部门名称}主管"
      permissions: "部门级"
      report_to: "经理"
      
    - level: 5
      name: "员工智能体"
      role: "agent"
      naming: "{具体岗位}"
      permissions: "执行级"
      report_to: "主管"
      
    - level: 6
      name: "实习智能体"
      role: "agent"
      naming: "实习{岗位}"
      permissions: "辅助级"
      report_to: "员工"

  departments_for_d03:
    - name: "产品部"
      主管: "产品主管"
      员工: ["资深产品经理"]
      实习: ["实习产品助理"]
     
    - name: "设计部"
      主管: "设计主管"
      员工: ["资深UI设计师"]
      实习: ["实习设计助理"]
     
    - name: "前端部"
      主管: "前端主管"
      员工: ["资深前端工程师 x2"]
      实习: ["实习前端助理"]
     
    - name: "后端部"
      主管: "后端主管"
      员工: ["资深后端工程师 x2"]
      实习: ["实习后端助理"]
     
    - name: "智能体部"
      主管: "智能体主管"
      员工: ["资深智能体工程师 x2"]
      实习: ["实习智能体助理"]
     
    - name: "测试部"
      主管: "测试主管"
      员工: ["资深测试工程师"]
      实习: ["实习测试助理"]
     
    - name: "运维部"
      主管: "运维主管"
      员工: ["资深运维工程师"]
      实习: ["实习运维助理"]
     
    - name: "营销部"
      主管: "营销主管"
      员工: ["资深内容运营"]
      实习: ["实习运营助理"]
```


## 三、核心流程

### 3.1 需求到交付完整流程

```yaml
workflow:
  - step: 1
    name: "老板下达指令"
    actor: "老板"
    action: "自然语言对话"
    input: "我需要开发一个AI客服系统"
    output: "原始需求"
    
  - step: 2
    name: "CEO智能体理解"
    actor: "CEO（主脑）"
    action: "意图识别 + 需求分析"
    input: "原始需求"
    output: "结构化需求"
    
  - step: 3
    name: "CEO智能体拆解"
    actor: "CEO（主脑）"
    action: "任务分解 + 资源评估"
    input: "结构化需求"
    output: "任务清单 + 资源需求"
    
  - step: 4
    name: "CEO分配任务"
    actor: "CEO（主脑）"
    action: "委派给对应总经理"
    input: "任务清单"
    output: "分配指令"
    
  - step: 5
    name: "各层智能体执行"
    actor: "总经理/经理/主管/员工"
    action: "逐级分解和执行"
    input: "分配指令"
    output: "执行结果"
    
  - step: 6
    name: "结果逐级汇报"
    actor: "员工→主管→经理→总经理→CEO"
    action: "结果汇总"
    input: "执行结果"
    output: "汇总报告"
    
  - step: 7
    name: "CEO汇报老板"
    actor: "CEO（主脑）"
    action: "结果呈现"
    input: "汇总报告"
    output: "项目交付物"
```

### 3.2 对话驱动开发流程

```yaml
dialog_flow:
  - turn: 1
    speaker: "老板"
    content: "我需要开发一个AI客服系统"
    
  - turn: 2
    speaker: "CEO"
    action: "理解并拆解"
    content: |
      收到。已拆解为以下子任务：
      1. 需求分析（产品部）
      2. UI设计（设计部）
      3. 后端API开发（后端部）
      4. 前端界面开发（前端部）
      5. AI模型接入（智能体部）
      6. 测试验收（测试部）
      预计工期：2周
      是否继续立项？
      
  - turn: 3
    speaker: "老板"
    content: "继续立项"
    
  - turn: 4
    speaker: "CEO"
    content: |
      项目已创建，项目编号：JYIS-2026-001
      项目负责人：Web总经理
      开始时间：明天 09:00
      我会定期向您汇报进度。
```


## 四、系统架构概览

### 4.1 技术架构

```yaml
architecture:
  backend:
    framework: "FastAPI"
    language: "Python 3.11+"
    database: "PostgreSQL 16+"
    cache: "Redis 7+"
    queue: "RabbitMQ"
    vector_db: "Chroma/Qdrant"
    
  frontend:
    framework: "Vue 3"
    build_tool: "Vite"
    state_management: "Pinia"
    ui_library: "Element Plus"
    
  deployment:
    container: "Docker"
    orchestration: "Kubernetes"
    ci_cd: "GitHub Actions"
    monitoring: "Prometheus + Grafana"
    logging: "ELK Stack"
    
  ai_integration:
    models:
      - provider: "DeepSeek"
        status: "integrated"
        priority: "P0"
      - provider: "OpenAI GPT-4"
        status: "planned"
        priority: "P1"
      - provider: "Claude"
        status: "planned"
        priority: "P1"
      - provider: "通义千问"
        status: "planned"
        priority: "P2"
    adapter: "统一模型适配器"
    features:
      - "多模型路由"
      - "并发配额管理"
      - "自动降级"
      - "成本控制"
```

### 4.2 数据架构

```yaml
data_layers:
  - layer: "业务数据"
    storage: "PostgreSQL"
    tables:
      - "users"
      - "agents"
      - "projects"
      - "tasks"
      - "messages"
      
  - layer: "向量数据"
    storage: "Chroma/Qdrant"
    collections:
      - "agent_memories"
      - "knowledge_base"
      - "code_embeddings"
      
  - layer: "缓存数据"
    storage: "Redis"
    use_cases:
      - "会话缓存"
      - "任务队列"
      - "实时状态"
      
  - layer: "消息数据"
    storage: "RabbitMQ"
    use_cases:
      - "智能体间通信"
      - "异步任务"
      - "事件广播"
```


## 五、开发阶段规划

### 5.1 阶段划分

```yaml
phases:
  phase_1:
    name: "核心架构搭建"
    duration: "第1周"
    deliverables:
      - "七层智能体数据模型"
      - "组织架构树API"
      - "CEO智能体基础对话"
      - "用户认证系统"
    priority: "P0"
    
  phase_2:
    name: "项目管理实现"
    duration: "第2周"
    deliverables:
      - "项目CRUD"
      - "任务CRUD"
      - "立项审批流程"
      - "进度跟踪"
    priority: "P0"
    
  phase_3:
    name: "智能体能力增强"
    duration: "第3周"
    deliverables:
      - "技能库系统"
      - "记忆系统"
      - "外部模型调用"
      - "并发配额管理"
    priority: "P1"
    
  phase_4:
    name: "前端与集成"
    duration: "第4周"
    deliverables:
      - "老板工作台"
      - "项目详情页"
      - "营销中心"
      - "飞书/微信集成"
    priority: "P1"
```

### 5.2 里程碑

```yaml
milestones:
  - name: "M1: 基础架构可用"
    date: "第1周末"
    criteria:
      - "CEO能理解并回应简单指令"
      - "组织架构树正确显示"
      
  - name: "M2: 项目管理可用"
    date: "第2周末"
    criteria:
      - "可创建项目并审批立项"
      - "任务可分配和跟踪"
      
  - name: "M3: 智能体能力完整"
    date: "第3周末"
    criteria:
      - "技能库可配置"
      - "记忆可存储检索"
      - "多模型可调用"
      
  - name: "M4: 系统完整可用"
    date: "第4周末"
    criteria:
      - "完整UI可用"
      - "可对接外部工具"
      - "自举开发验证通过"
```


## 六、成功指标

```yaml
kpis:
  efficiency:
    - metric: "需求到交付周期"
      target: "缩短50%"
      measurement: "对比传统开发"
      
    - metric: "代码生成准确率"
      target: "≥85%"
      measurement: "人工抽检"
      
    - metric: "任务自动分配率"
      target: "≥90%"
      measurement: "系统统计"
      
  quality:
    - metric: "代码Bug率"
      target: "降低40%"
      measurement: "测试报告"
      
    - metric: "需求覆盖率"
      target: "100%"
      measurement: "验收测试"
      
  system:
    - metric: "系统可用性"
      target: "99.5%"
      measurement: "监控系统"
      
    - metric: "API响应时间（MK-01验收口径）"
      target: "P95 ≤ 180秒，单次 ≤ 300秒"
      measurement: "性能测试"
      
  user:
    - metric: "用户满意度"
      target: "≥4.5/5"
      measurement: "问卷调查"
      
    - metric: "日均活跃用户"
      target: "≥100"
      measurement: "系统统计"
```


## 七、在Cursor中使用

### 7.1 文件存放位置

```
d:\BaiduSyncdisk\JiGuang\docs\PROJECT_OVERVIEW_v1.0.md
```

### 7.2 在Cursor中引用

**方式一：对话中引用**
```
@docs/PROJECT_OVERVIEW_v1.0.md 根据项目概述，开始开发第一阶段的核心架构
```

**方式二：Composer中引用**
```
@docs/PROJECT_OVERVIEW_v1.0.md 实现七层智能体组织架构的数据模型和API
```

**方式三：多文档联合引用**
```
@docs/PROJECT_OVERVIEW_v1.0.md @docs/AGENT_ABILITY_SPEC_v1.0.md 
根据这两个文档，实现智能体能力注册系统
```


## 八、相关文档索引

| 文档名称 | 路径 | 说明 |
|---------|------|------|
| 项目概述 | `docs/PROJECT_OVERVIEW_v1.0.md` | 本文档 |
| 智能体能力规范 | `docs/AGENT_ABILITY_SPEC_v1.0.md` | 142项能力定义（基线） |
| 产品需求文档 | `docs/PRD_v2.0.md` | 发布范围、门槛与优先级基线 |
| 数据库设计 | `docs/DATABASE_DESIGN_v1.0.md` | 表结构设计 |
| 界面设计 | `docs/UI_UX_DESIGN_v1.0.md` | UI/UX设计 |
| 端点映射 | `docs/ENDPOINT_MAPPING_v1.0.md` | API端点映射 |
| 部署运维 | `docs/DEPLOYMENT_v1.0.md` | 部署配置 |
| 用户手册 | `docs/USER_MANUAL_v1.0.md` | 操作指南 |
| 测试计划 | `docs/TEST_PLAN_v1.0.md` | 测试用例 |
| API变更日志 | `docs/API_CHANGELOG.md` | 版本记录 |
| 文档维护基线 | `docs/DOCUMENTATION_BASELINE_v1.0.md` | 跨文档一致性基线 |
| 分层能力配置 | `docs/LAYER_ABILITY_CONFIG_v1.0.md` | 自上而下能力与主脑工具智能化 |
| 主脑能力映射 | `docs/CEO_ABILITY_RUNTIME_MAPPING_v1.0.md` | CEO-09~14 到 AGENT-RUNTIME/WEB/LAW 对照 |
| 主脑策略配置 | `docs/ceo_policy.engine.yaml` | 按环境策略引擎配置草案 |
| 生产运行假设 | `docs/PRODUCTION_RUNTIME_ASSUMPTIONS_v1.0.md` | 第三方波动、降级策略与门禁 |
| 智能体成熟度模型 | `docs/AGENT_MATURITY_MODEL_v1.0.md` | M1-M4分级与版本目标映射 |
| 文档模块索引 | `docs/DOCS_MODULE_INDEX_v1.0.md` | 文档导航与模块检索入口 |
| UI拆分计划 | `docs/UI_UX_SPLIT_PLAN_v1.0.md` | UI超长文档拆分执行方案 |
| UI迁移日志 | `docs/UI_MIGRATION_WORKLOG_v1.0.md` | UI模块化实迁进度跟踪 |
| UI总文档归档 | `docs/UI_UX_DESIGN_v1.0.archive_before_slim.md` | 精简前完整 UI 备份（只读） |

---

**文档结束**