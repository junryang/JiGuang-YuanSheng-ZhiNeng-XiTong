# 自研能力建设规划 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\SELF_DEV_ROADMAP_v1.0.md
```


# 自研能力建设规划 v1.0

## 一、总体规划

```yaml
# 规划概述
roadmap:
  name: "营销中心自研能力建设规划"
  total_duration: "12+个月"
  phases: 5
  
  principle: |
    自研软件具备基础内容生成能力（基于现有大模型），
    但对于专业级图像/视频生成和多平台一键分发，
    优先集成成熟的第三方工具，避免重复造轮子。

# 时间线总览
timeline: |
  Phase 1 (当前)    Phase 2 (2-3月)    Phase 3 (3-6月)    Phase 4 (6-12月)    Phase 5 (12月+)
       │                 │                 │                 │                  │
       ▼                 ▼                 ▼                 ▼                  ▼
  ┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │ 文本内容 │    │ 内容工作流   │    │   图像生成   │    │   视频生成   │    │  全模态      │
  │ 生成     │───▶│ 编排         │───▶│              │───▶│              │───▶│  智能体      │
  └──────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                 │                 │                 │                  │
       ▼                 ▼                 ▼                 ▼                  ▼
  基于DeepSeek      多Agent协作       集成SD/DALL-E     集成专业视频AI     全链路自主
  品牌语调微调      策划→写作→审核     支持品牌风格      工具集成           创意到分发
```

## 1.1 长期目标与发布策略

- 长期目标：达到“与人类团队无差别的通用自主智能体”。
- 工程策略：按 `AGENT_MATURITY_MODEL_v1.0.md` 分级推进（M1→M4）。
- 发布约束：每一阶段上线必须满足 `PRD_v2.0.md` 与 `PRODUCTION_RUNTIME_ASSUMPTIONS_v1.0.md` 的门禁，不以“全能力一次到位”为发布条件。


## 二、Phase 1：文本内容生成

```yaml
# Phase 1 配置
phase: 1
name: "文本内容生成"
duration: "当前"
status: "in_progress"  # planned/in_progress/completed
priority: "P0"

# 能力清单
capabilities:
  - id: "TEXT-01"
    name: "基础文本生成"
    description: "基于DeepSeek等大模型生成文章、文案、脚本"
    implementation: "大模型API调用"
    status: "completed"
    
  - id: "TEXT-02"
    name: "品牌语调微调"
    description: "学习品牌语调，生成符合品牌风格的内容"
    implementation: "Few-shot learning + 提示词工程"
    status: "in_progress"
    
  - id: "TEXT-03"
    name: "多格式适配"
    description: "同一内容适配不同平台格式"
    implementation: "内容重写 + 格式转换"
    status: "planned"
    
  - id: "TEXT-04"
    name: "SEO优化"
    description: "自动优化关键词、标题、描述"
    implementation: "SEO规则引擎 + 大模型"
    status: "planned"

# 技术实现
implementation:
  base_model: "DeepSeek-V3"
  fine_tuning: "LoRA微调"
  prompt_template: |
    你是一个【品牌名称】的内容创作者。
    品牌语调：【品牌语调描述】
    目标受众：【受众描述】
    
    请根据以下要求生成内容：
    【具体要求】
    
  api_endpoint: "/api/v1/generation/text"

# 验收标准
acceptance_criteria:
  - "生成内容语法正确率 > 99%"
  - "品牌语调一致性 > 85%"
  - "内容原创性 > 90%"
  - "生成速度 < 3秒/500字"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/generation/text/generate"
    description: "生成文本"
    request_body:
      prompt: "string"
      style: "string"
      length: "short|medium|long"
    response:
      content: "string"
      usage: "dict"
      
  - method: "POST"
    endpoint: "/api/v1/generation/text/optimize"
    description: "优化文本"
    request_body:
      content: "string"
      optimization_type: "seo|readability|style"
    response:
      optimized_content: "string"
```


## 三、Phase 2：内容工作流编排

```yaml
# Phase 2 配置
phase: 2
name: "内容工作流编排"
duration: "2-3个月"
status: "planned"
priority: "P0"

# 能力清单
capabilities:
  - id: "WORKFLOW-01"
    name: "多Agent协作"
    description: "策划、写作、审核、分发等多Agent协同"
    implementation: "Agent编排引擎"
    status: "planned"
    
  - id: "WORKFLOW-02"
    name: "工作流可视化"
    description: "拖拽式工作流设计器"
    implementation: "Vue + 流程图组件"
    status: "planned"
    
  - id: "WORKFLOW-03"
    name: "步骤自动执行"
    description: "按预设流程自动执行各步骤"
    implementation: "任务调度器"
    status: "planned"
    
  - id: "WORKFLOW-04"
    name: "人工审核节点"
    description: "支持人工介入审核"
    implementation: "审批流程"
    status: "planned"
    
  - id: "WORKFLOW-05"
    name: "异常处理"
    description: "步骤失败时的自动重试和降级"
    implementation: "错误处理机制"
    status: "planned"

# Agent角色定义
agent_roles:
  - role: "策划Agent"
    description: "负责内容选题和策划"
    capabilities: ["热点追踪", "选题生成", "大纲制定"]
    
  - role: "写作Agent"
    description: "负责内容撰写"
    capabilities: ["文章写作", "文案生成", "多格式适配"]
    
  - role: "审核Agent"
    description: "负责内容审核"
    capabilities: ["质量检查", "合规检查", "品牌一致性检查"]
    
  - role: "分发Agent"
    description: "负责内容分发"
    capabilities: ["平台选择", "定时发布", "效果追踪"]

# 工作流模板
workflow_templates:
  - id: "WF-STANDARD"
    name: "标准内容流程"
    steps:
      - step: 1
        name: "选题策划"
        agent: "策划Agent"
        timeout: 3600
        
      - step: 2
        name: "内容写作"
        agent: "写作Agent"
        timeout: 1800
        
      - step: 3
        name: "内容审核"
        agent: "审核Agent"
        require_approval: true
        timeout: 86400
        
      - step: 4
        name: "多平台分发"
        agent: "分发Agent"
        timeout: 600

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/workflow/create"
    description: "创建工作流"
    
  - method: "POST"
    endpoint: "/api/v1/workflow/{id}/execute"
    description: "执行工作流"
    
  - method: "GET"
    endpoint: "/api/v1/workflow/{id}/status"
    description: "查询状态"
    
  - method: "POST"
    endpoint: "/api/v1/workflow/{id}/approve"
    description: "审核通过"
```


## 四、Phase 3：图像生成

```yaml
# Phase 3 配置
phase: 3
name: "图像生成"
duration: "3-6个月"
status: "planned"
priority: "P1"

# 能力清单
capabilities:
  - id: "IMAGE-01"
    name: "基础图像生成"
    description: "文本生成配图、海报"
    implementation: "集成DALL-E 3 API"
    status: "planned"
    
  - id: "IMAGE-02"
    name: "品牌风格训练"
    description: "训练品牌专属风格模型"
    implementation: "Stable Diffusion微调"
    status: "planned"
    
  - id: "IMAGE-03"
    name: "图像编辑"
    description: "图像修复、扩展、风格转换"
    implementation: "集成图像编辑API"
    status: "planned"
    
  - id: "IMAGE-04"
    name: "批量生成"
    description: "批量生成多张配图"
    implementation: "异步任务队列"
    status: "planned"

# 工具集成策略
integration:
  primary: "DALL-E 3"
  secondary: "Stable Diffusion (自托管)"
  
  use_cases:
    - scenario: "文章配图"
      tool: "DALL-E 3"
      priority: "high"
      
    - scenario: "品牌海报"
      tool: "Stable Diffusion"
      priority: "medium"
      
    - scenario: "UI图标"
      tool: "Stable Diffusion"
      priority: "low"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/generation/image/generate"
    description: "生成图像"
    request_body:
      prompt: "string"
      style: "string"
      size: "string"
    response:
      image_url: "string"
      
  - method: "POST"
    endpoint: "/api/v1/generation/image/train-style"
    description: "训练品牌风格"
    request_body:
      style_name: "string"
      sample_images: "List[file]"
    response:
      model_id: "string"
```


## 五、Phase 4：视频生成

```yaml
# Phase 4 配置
phase: 4
name: "视频生成"
duration: "6-12个月"
status: "planned"
priority: "P2"

# 能力清单
capabilities:
  - id: "VIDEO-01"
    name: "短视频生成"
    description: "文本生成短视频"
    implementation: "集成Runway/Pika API"
    status: "planned"
    
  - id: "VIDEO-02"
    name: "数字人播报"
    description: "AI数字人视频生成"
    implementation: "集成网易千梦引擎"
    status: "planned"
    
  - id: "VIDEO-03"
    name: "PPT转视频"
    description: "将演示文稿转换为视频"
    implementation: "集成HeyGen"
    status: "planned"
    
  - id: "VIDEO-04"
    name: "视频编辑"
    description: "自动剪辑、添加字幕、配乐"
    implementation: "集成视频编辑API"
    status: "planned"

# 工具集成策略
integration:
  primary: "网易千梦引擎"
  secondary: "Runway"
  
  use_cases:
    - scenario: "产品介绍视频"
      tool: "网易千梦引擎"
      priority: "high"
      
    - scenario: "创意短视频"
      tool: "Runway"
      priority: "medium"
      
    - scenario: "数字人播报"
      tool: "网易千梦引擎"
      priority: "high"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/generation/video/generate"
    description: "生成视频"
    request_body:
      script: "string"
      style: "string"
      duration: "int"
    response:
      video_url: "string"
      task_id: "string"
```


## 六、Phase 5：全模态智能体

```yaml
# Phase 5 配置
phase: 5
name: "全模态智能体"
duration: "12个月+"
status: "planned"
priority: "P3"

# 能力清单
capabilities:
  - id: "FULL-01"
    name: "全链路自主"
    description: "从创意到分发的全自动化"
    implementation: "多模态Agent编排"
    status: "planned"
    
  - id: "FULL-02"
    name: "跨模态理解"
    description: "理解图文、视频等多模态内容"
    implementation: "多模态大模型集成"
    status: "planned"
    
  - id: "FULL-03"
    name: "智能决策"
    description: "自主决策内容策略和渠道选择"
    implementation: "强化学习 + 数据分析"
    status: "planned"
    
  - id: "FULL-04"
    name: "持续优化"
    description: "根据效果数据持续优化策略"
    implementation: "闭环反馈系统"
    status: "planned"

# 目标架构
target_architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                         全模态智能体                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         理解层                                       │   │
  │  │  文本理解 | 图像理解 | 视频理解 | 音频理解 | 用户意图               │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         决策层                                       │   │
  │  │  策略规划 | 内容选题 | 渠道选择 | 预算分配 | 时机决策               │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         执行层                                       │   │
  │  │  文本生成 | 图像生成 | 视频生成 | 分发发布 | 效果追踪               │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  └─────────────────────────────────────────────────────────────────────────────┘
```


## 七、阶段对比总览

```yaml
# 各阶段对比
phases_comparison:
  - phase: 1
    name: "文本内容生成"
    capabilities: 4
    complexity: "低"
    dependency: "大模型API"
    output: "文本内容"
    
  - phase: 2
    name: "内容工作流编排"
    capabilities: 5
    complexity: "中"
    dependency: "Agent框架"
    output: "自动化流程"
    
  - phase: 3
    name: "图像生成"
    capabilities: 4
    complexity: "中高"
    dependency: "DALL-E/SD"
    output: "图像内容"
    
  - phase: 4
    name: "视频生成"
    capabilities: 4
    complexity: "高"
    dependency: "专业视频AI"
    output: "视频内容"
    
  - phase: 5
    name: "全模态智能体"
    capabilities: 4
    complexity: "很高"
    dependency: "多模态大模型"
    output: "全链路自主"
```


## 八、资源需求

```yaml
# 各阶段资源需求
resources:
  phase_1:
    compute: "标准 (2核4G)"
    storage: "10GB"
    team: "1-2人"
    cost: "低"
    
  phase_2:
    compute: "标准 (2核4G)"
    storage: "20GB"
    team: "2-3人"
    cost: "中"
    
  phase_3:
    compute: "GPU (1x A10)"
    storage: "100GB"
    team: "2-3人"
    cost: "中高"
    
  phase_4:
    compute: "GPU (2x A100)"
    storage: "500GB"
    team: "3-4人"
    cost: "高"
    
  phase_5:
    compute: "GPU集群"
    storage: "1TB+"
    team: "4-6人"
    cost: "很高"
```


## 九、里程碑检查点

```yaml
# 里程碑定义
milestones:
  phase_1:
    - milestone: "M1.1"
      name: "基础文本生成上线"
      date: "当前"
      deliverable: "文本生成API"
      
    - milestone: "M1.2"
      name: "品牌语调微调完成"
      date: "2周后"
      deliverable: "品牌模型"
      
  phase_2:
    - milestone: "M2.1"
      name: "工作流引擎MVP"
      date: "1个月"
      deliverable: "基础工作流"
      
    - milestone: "M2.2"
      name: "多Agent协作上线"
      date: "2个月"
      deliverable: "完整工作流"
      
  phase_3:
    - milestone: "M3.1"
      name: "DALL-E集成完成"
      date: "3个月"
      deliverable: "图像生成API"
      
    - milestone: "M3.2"
      name: "品牌风格训练完成"
      date: "5个月"
      deliverable: "风格模型"
      
  phase_4:
    - milestone: "M4.1"
      name: "短视频生成上线"
      date: "8个月"
      deliverable: "视频生成API"
      
    - milestone: "M4.2"
      name: "数字人播报上线"
      date: "10个月"
      deliverable: "数字人视频"
      
  phase_5:
    - milestone: "M5.1"
      name: "全模态智能体原型"
      date: "12个月"
      deliverable: "原型系统"
      
    - milestone: "M5.2"
      name: "全链路自动化"
      date: "15个月+"
      deliverable: "正式系统"
```


## 十、数据库表结构

```sql
-- 能力建设规划表
CREATE TABLE self_dev_roadmap (
    id UUID PRIMARY KEY,
    phase INTEGER NOT NULL,
    capability_id VARCHAR(50) NOT NULL,
    capability_name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'planned',
    priority VARCHAR(10),
    estimated_weeks INTEGER,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 里程碑表
CREATE TABLE roadmap_milestones (
    id UUID PRIMARY KEY,
    phase INTEGER NOT NULL,
    milestone_id VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    deliverable TEXT,
    target_date DATE,
    achieved_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL
);
```


## 十一、在Cursor中使用

```bash
# 1. 查看整体规划
@docs/SELF_DEV_ROADMAP_v1.0.md 显示自研能力建设规划

# 2. 开发Phase 1
@docs/SELF_DEV_ROADMAP_v1.0.md 实现Phase 1的文本内容生成能力，包括品牌语调微调

# 3. 开发Phase 2
@docs/SELF_DEV_ROADMAP_v1.0.md 实现Phase 2的内容工作流编排，支持多Agent协作

# 4. 查看里程碑
@docs/SELF_DEV_ROADMAP_v1.0.md 列出所有里程碑和检查点
```


**文档结束**