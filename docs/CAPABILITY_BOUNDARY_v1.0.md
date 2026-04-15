# 自研 vs 第三方能力边界分析 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\CAPABILITY_BOUNDARY_v1.0.md
```


# 自研 vs 第三方能力边界分析 v1.0

## 一、决策框架概述

```yaml
# 决策原则 - 对齐通用能力架构
decision_principles:
  - principle: "核心能力自研"
    description: "与系统核心价值直接相关的能力，自研以保持控制权"
    related_abilities:
      - "AGENT-RUNTIME-01: 智能体主循环"
      - "AGENT-RUNTIME-02: 长期目标与个人偏好"
      - "CL-06: 合同网协议"
      - "META-01: 能力扩展"
    
  - principle: "成熟能力集成"
    description: "市场上已有成熟解决方案的能力，优先集成"
    related_abilities:
      - "WEB-01~11: 互联网工具调用"
      - "EM-01~11: 外部模型调用"
    
  - principle: "差异化自研"
    description: "能形成差异化竞争优势的能力，自研并优化"
    related_abilities:
      - "AGENT-RUNTIME-06: 心智模型维护"
      - "AGENT-RUNTIME-11: 自我反思"
      - "LN-04: 双循环学习"
    
  - principle: "成本效益平衡"
    description: "自研成本 > 3倍集成成本时，优先集成"

# 决策矩阵
decision_matrix:
  build:
    conditions:
      - "核心差异化能力"
      - "市场无成熟方案"
      - "数据安全要求高"
      - "长期高频使用"
    examples:
      - "智能体核心运行时"
      - "心智模型维护"
      - "合同网协议"
      
  buy:
    conditions:
      - "市场方案成熟"
      - "非核心能力"
      - "自研成本过高"
      - "需要快速上线"
    examples:
      - "图像/视频生成"
      - "多模态理解"
      - "多平台分发"
      
  hybrid:
    conditions:
      - "核心编排自研 + 能力调用集成"
      - "需要定制化 + 基础能力成熟"
      - "数据敏感 + 非敏感部分可外包"
    examples:
      - "文本生成（自研品牌语调 + 集成大模型）"
      - "工作流自动化（自研编排 + 集成工具）"
```


## 二、能力边界详细配置

### 2.1 文本生成

```yaml
# 文本生成能力 - 对齐EM-01~05外部模型调用能力
capability: "text_generation"
name: "文本生成"
description: "生成文章、文案、代码注释、文档等文本内容"

# 关联通用能力
related_abilities:
  - "EM-01: 多模型路由"
  - "EM-02: 模型负载均衡"
  - "EM-03: 模型降级"
  - "EM-04: 模型缓存"
  - "EM-05: 模型成本控制"
  - "EM-11: 模型调用配额"

# 自研分析
build:
  feasibility: "high"
  difficulty: "medium"
  estimated_weeks: 4
  advantages:
    - "可深度定制品牌语调"
    - "数据不出域，安全可控"
    - "与智能体系统深度集成"
  disadvantages:
    - "需要大量训练数据"
    - "需要持续的模型优化"
    - "效果可能不如专业工具"
    
# 第三方分析
buy:
  options:
    - name: "Jasper"
      cost: "$49-499/月"
      features:
        - "50+文案模板"
        - "品牌语调学习"
        - "多语言支持"
        - "SEO优化"
      api_available: true
      
    - name: "Copy.ai"
      cost: "$36-186/月"
      features:
        - "100+创作工具"
        - "团队协作"
        - "工作流自动化"
      api_available: true
      
    - name: "DeepSeek/GPT-4"
      cost: "按Token计费"
      features:
        - "通用文本生成"
        - "代码生成"
        - "推理能力"
      api_available: true

# 建议方案
recommendation:
  strategy: "hybrid"
  build_scope:
    - "核心智能体对话生成（基于EM-01多模型路由）"
    - "代码生成（基于EX-01代码生成）"
    - "品牌语调微调"
  buy_scope:
    - "营销文案批量生成"
    - "SEO内容优化"
    - "多语言翻译"
    
# API接口
api:
  build_endpoint: "/api/v1/generation/text"
  third_party_adapters:
    - provider: "jasper"
      endpoint: "/api/v1/third-party/jasper/generate"
      related_ability: "EM-01"
    - provider: "copyai"
      endpoint: "/api/v1/third-party/copyai/generate"
      related_ability: "EM-02"
    - provider: "deepseek"
      endpoint: "/api/v1/llm/chat"
      related_ability: "EM-03"
```

### 2.2 图像生成

```yaml
# 图像生成能力
capability: "image_generation"
name: "图像生成"
description: "生成配图、海报、图标、UI素材等图像内容"

# 关联通用能力
related_abilities:
  - "WEB-04: API调用与集成"
  - "EX-15: 图像生成"

# 自研分析
build:
  feasibility: "low"
  difficulty: "high"
  estimated_weeks: 24
  advantages:
    - "完全控制生成质量"
    - "可定制特定风格"
  disadvantages:
    - "需要大量GPU资源"
    - "需要专业AI图像团队"
    - "自研成本极高（百万级）"
    - "效果难以达到主流水平"
    
# 第三方分析
buy:
  options:
    - name: "DALL-E 3"
      cost: "$0.04-0.12/张"
      features:
        - "高精度文本理解"
        - "真实感强"
        - "安全过滤"
      api_available: true
      integration_method: "api"
      
    - name: "Midjourney"
      cost: "$10-120/月"
      features:
        - "高质量艺术风格"
        - "精细控制"
        - "社区活跃"
      api_available: false
      integration_method: "webhook"
      
    - name: "Stable Diffusion"
      cost: "自托管费用"
      features:
        - "开源可定制"
        - "本地部署"
        - "模型多样"
      api_available: true
      integration_method: "self_hosted"

# 建议方案
recommendation:
  strategy: "buy"
  primary: "DALL-E 3"
  secondary: "Stable Diffusion（自托管）"
  use_cases:
    - "文章配图 → DALL-E 3"
    - "海报设计 → Midjourney"
    - "UI图标 → Stable Diffusion"
    
# API接口
api:
  third_party_adapters:
    - provider: "openai_dalle"
      endpoint: "/api/v1/third-party/dalle/generate"
      related_ability: "WEB-04"
      input_schema:
        prompt: "string"
        size: "256x256|512x512|1024x1024"
        quality: "standard|hd"
        n: "int"
```

### 2.3 视频生成

```yaml
# 视频生成能力
capability: "video_generation"
name: "视频生成"
description: "生成短视频、演示视频、产品介绍等视频内容"

# 关联通用能力
related_abilities:
  - "WEB-04: API调用与集成"
  - "EX-17: 视频生成"

# 自研分析
build:
  feasibility: "very_low"
  difficulty: "very_high"
  estimated_weeks: 52+
  disadvantages:
    - "技术门槛极高"
    - "需要专业团队"
    - "GPU资源消耗巨大"
    - "自研成本千万级"
    
# 第三方分析
buy:
  options:
    - name: "Runway"
      cost: "$15-95/月"
      features:
        - "文本生成视频"
        - "视频编辑"
        - "绿幕抠像"
      api_available: true
      
    - name: "网易千梦引擎"
      cost: "企业定制"
      features:
        - "AI视频全自动化"
        - "数字人播报"
        - "模板丰富"
      api_available: true
      note: "国内首选，支持私有化部署"

# 建议方案
recommendation:
  strategy: "buy"
  primary: "网易千梦引擎"
  secondary: "Runway"
  use_cases:
    - "产品介绍视频 → 网易千梦引擎"
    - "创意短视频 → Runway"
    
# API接口
api:
  third_party_adapters:
    - provider: "runway"
      endpoint: "/api/v1/third-party/runway/generate"
      related_ability: "WEB-04"
    - provider: "qianmeng"
      endpoint: "/api/v1/third-party/qianmeng/generate"
      related_ability: "WEB-04"
      note: "网易千梦引擎，国内优先"
```

### 2.4 多模态理解

```yaml
# 多模态理解能力 - 对齐PC-03视觉理解
capability: "multimodal_understanding"
name: "多模态理解"
description: "理解图像、图表、截图、文档等多模态内容"

# 关联通用能力
related_abilities:
  - "PC-03: 视觉理解"
  - "PC-07: 文档理解"
  - "EM-18: 模型多模态"

# 自研分析
build:
  feasibility: "low"
  difficulty: "very_high"
  estimated_weeks: 40
  disadvantages:
    - "需要多模态训练数据"
    - "需要专业团队"
    - "效果难以达到GPT-4V水平"
    
# 第三方分析
buy:
  options:
    - name: "GPT-4V"
      cost: "按Token计费"
      features:
        - "图像理解"
        - "图表分析"
        - "OCR识别"
      api_available: true
      
    - name: "Qwen-VL"
      cost: "按Token计费"
      features:
        - "中文优化"
        - "图像理解"
      api_available: true

# 建议方案
recommendation:
  strategy: "buy"
  primary: "GPT-4V"
  secondary: "Qwen-VL（国内）"
  use_cases:
    - "UI截图理解 → GPT-4V"
    - "流程图解析 → GPT-4V"
    - "中文文档 → Qwen-VL"
    
# API接口
api:
  third_party_adapters:
    - provider: "openai_gpt4v"
      endpoint: "/api/v1/third-party/gpt4v/understand"
      related_ability: "PC-03"
    - provider: "qwen_vl"
      endpoint: "/api/v1/third-party/qwen-vl/understand"
      related_ability: "PC-03"
```

### 2.5 品牌一致性

```yaml
# 品牌一致性能力 - 对齐AGENT-RUNTIME-02个人偏好
capability: "brand_consistency"
name: "品牌一致性"
description: "保持生成内容与品牌语调、风格一致"

# 关联通用能力
related_abilities:
  - "AGENT-RUNTIME-02: 长期目标与个人偏好"
  - "MK-03: 品牌语调学习"

# 自研分析
build:
  feasibility: "high"
  difficulty: "medium"
  estimated_weeks: 6
  advantages:
    - "深度定制品牌风格"
    - "持续优化品牌模型"
    - "数据安全"
  disadvantages:
    - "需要品牌样本数据"
    - "需要持续维护"
    
# 建议方案
recommendation:
  strategy: "hybrid"
  build_scope:
    - "品牌语料库构建"
    - "风格微调模型"
    - "一致性评分算法"
  buy_scope:
    - "品牌指南管理"
    - "术语库维护"
    
# API接口
api:
  build_endpoint: "/api/v1/brand/consistency/check"
  build_endpoint: "/api/v1/brand/style/learn"
  related_ability: "AGENT-RUNTIME-02"
```

### 2.6 工作流自动化

```yaml
# 工作流自动化能力 - 对齐AUTO-03工作流自动化编排
capability: "workflow_automation"
name: "工作流自动化"
description: "编排多步骤、多工具的内容创作工作流"

# 关联通用能力
related_abilities:
  - "AUTO-03: 工作流自动化编排"
  - "DC-01: 任务规划"
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"

# 自研分析
build:
  feasibility: "high"
  difficulty: "medium"
  estimated_weeks: 8
  advantages:
    - "与智能体系统深度集成"
    - "完全可控的工作流"
    - "可扩展性强"
  disadvantages:
    - "需要持续维护"
    - "初期开发投入大"
    
# 建议方案
recommendation:
  strategy: "build"
  reason: "工作流编排是智能体系统的核心能力，应与Agent架构深度集成（AUTO-03）"
  build_scope:
    - "工作流引擎"
    - "任务编排器"
    - "步骤执行器"
    - "错误处理机制"
    
# API接口
api:
  build_endpoint: "/api/v1/workflow/create"
  build_endpoint: "/api/v1/workflow/{id}/execute"
  build_endpoint: "/api/v1/workflow/{id}/status"
  related_ability: "AUTO-03"
```

### 2.7 多平台分发

```yaml
# 多平台分发能力 - 对齐WEB-05社交媒体交互
capability: "multi_platform_distribution"
name: "多平台分发"
description: "一键发布内容到多个自媒体平台"

# 关联通用能力
related_abilities:
  - "WEB-05: 社交媒体交互"
  - "MK-08: 多平台分发"

# 自研分析
build:
  feasibility: "low"
  difficulty: "high"
  estimated_weeks: 16
  disadvantages:
    - "需要对接数十个平台API"
    - "每个平台都需要维护"
    - "API变更频繁"
    - "自研成本高"
    
# 第三方分析
buy:
  options:
    - name: "聚媒通"
      cost: "¥299-999/月"
      features:
        - "国内60+平台"
        - "一键分发"
        - "数据统计"
      api_available: true
      note: "国内首选"
      
    - name: "Hootsuite"
      cost: "$49-739/月"
      features:
        - "海外社交媒体"
        - "多账号管理"
        - "分析报告"
      api_available: true
      note: "海外首选"

# 建议方案
recommendation:
  strategy: "buy"
  primary_domestic: "聚媒通"
  primary_international: "Hootsuite"
  integration_method: "API对接"
  
# API接口
api:
  third_party_adapters:
    - provider: "jumeitong"
      endpoint: "/api/v1/third-party/jumeitong/publish"
      related_ability: "WEB-05"
    - provider: "hootsuite"
      endpoint: "/api/v1/third-party/hootsuite/publish"
      related_ability: "WEB-05"
```


## 三、决策汇总表

```yaml
# 最终决策汇总 - 对齐通用能力优先级
final_decisions:
  - capability: "text_generation"
    strategy: "hybrid"
    build_ratio: 40%
    buy_ratio: 60%
    primary_buy: "DeepSeek/GPT-4"
    related_abilities: ["EM-01", "EM-02", "EM-03", "EM-04", "EM-05"]
    
  - capability: "image_generation"
    strategy: "buy"
    build_ratio: 0%
    buy_ratio: 100%
    primary_buy: "DALL-E 3"
    secondary_buy: "Stable Diffusion"
    related_abilities: ["WEB-04", "EX-15"]
    
  - capability: "video_generation"
    strategy: "buy"
    build_ratio: 0%
    buy_ratio: 100%
    primary_buy: "网易千梦引擎"
    related_abilities: ["WEB-04", "EX-17"]
    
  - capability: "multimodal_understanding"
    strategy: "buy"
    build_ratio: 0%
    buy_ratio: 100%
    primary_buy: "GPT-4V"
    secondary_buy: "Qwen-VL"
    related_abilities: ["PC-03", "EM-18"]
    
  - capability: "brand_consistency"
    strategy: "hybrid"
    build_ratio: 60%
    buy_ratio: 40%
    primary_build: "品牌语调微调"
    related_abilities: ["AGENT-RUNTIME-02", "MK-03"]
    
  - capability: "workflow_automation"
    strategy: "build"
    build_ratio: 100%
    buy_ratio: 0%
    reason: "核心能力，需深度集成（AUTO-03）"
    related_abilities: ["AUTO-03", "DC-01", "EX-09", "EX-10"]
    
  - capability: "multi_platform_distribution"
    strategy: "buy"
    build_ratio: 0%
    buy_ratio: 100%
    primary_buy_domestic: "聚媒通"
    primary_buy_international: "Hootsuite"
    related_abilities: ["WEB-05", "MK-08"]
```


## 四、第三方工具集成配置

```yaml
# 第三方工具统一适配层 - 对齐EM-01~05外部模型调用
third_party_adapters:
  # 文本生成
  - id: "adapter_text_deepseek"
    provider: "deepseek"
    endpoint: "/api/v1/third-party/deepseek"
    auth_type: "apikey"
    rate_limit: 10
    related_ability: "EM-01"
    
  - id: "adapter_text_openai"
    provider: "openai"
    endpoint: "/api/v1/third-party/openai"
    auth_type: "apikey"
    rate_limit: 50
    related_ability: "EM-02"
    
  # 图像生成
  - id: "adapter_image_dalle"
    provider: "dalle"
    endpoint: "/api/v1/third-party/dalle"
    auth_type: "apikey"
    rate_limit: 5
    related_ability: "WEB-04"
    
  # 视频生成
  - id: "adapter_video_qianmeng"
    provider: "qianmeng"
    endpoint: "/api/v1/third-party/qianmeng"
    auth_type: "apikey"
    rate_limit: 10
    related_ability: "WEB-04"
    
  # 多模态
  - id: "adapter_multimodal_gpt4v"
    provider: "gpt4v"
    endpoint: "/api/v1/third-party/gpt4v"
    auth_type: "apikey"
    rate_limit: 20
    related_ability: "PC-03"
    
  # 分发平台
  - id: "adapter_distribute_jumeitong"
    provider: "jumeitong"
    endpoint: "/api/v1/third-party/jumeitong"
    auth_type: "apikey"
    rate_limit: 30
    related_ability: "WEB-05"
```


## 五、通用能力映射总表

```yaml
# 自研/集成决策与通用能力的完整映射
capability_decision_mapping:
  # P0级：必须自研的核心能力
  P0_build_required:
    - ability: "AGENT-RUNTIME-01"
      name: "智能体主循环"
      decision: "自研"
      reason: "智能体核心，无替代"
      
    - ability: "AGENT-RUNTIME-02"
      name: "长期目标与个人偏好"
      decision: "自研"
      reason: "差异化核心"
      
    - ability: "AGENT-RUNTIME-06"
      name: "心智模型维护"
      decision: "自研"
      reason: "差异化核心"
      
    - ability: "CL-06"
      name: "合同网协议"
      decision: "自研"
      reason: "协作核心"
      
    - ability: "AUTO-03"
      name: "工作流自动化编排"
      decision: "自研"
      reason: "编排核心"
      
  # P1级：可混合决策
  P1_hybrid:
    - ability: "EM-01~11"
      name: "外部模型调用"
      decision: "混合"
      reason: "集成大模型，自研路由"
      
    - ability: "PC-03"
      name: "视觉理解"
      decision: "集成"
      reason: "使用GPT-4V"
      
    - ability: "EX-15"
      name: "图像生成"
      decision: "集成"
      reason: "使用DALL-E"
      
  # P2级：优先集成
  P2_buy_preferred:
    - ability: "WEB-05"
      name: "社交媒体交互"
      decision: "集成"
      reason: "使用聚媒通"
      
    - ability: "MK-08"
      name: "多平台分发"
      decision: "集成"
      reason: "使用Hootsuite"
```


## 六、数据库表结构

```sql
-- 第三方工具配置表 - 关联通用能力
CREATE TABLE third_party_tools (
    id UUID PRIMARY KEY,
    provider VARCHAR(100) NOT NULL,
    capability VARCHAR(50) NOT NULL,
    related_ability_id VARCHAR(50),  -- 关联通用能力ID
    api_endpoint VARCHAR(500) NOT NULL,
    auth_config JSONB,
    rate_limit INTEGER DEFAULT 10,
    enabled BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 能力决策记录表 - 关联通用能力
CREATE TABLE capability_decisions (
    id UUID PRIMARY KEY,
    capability VARCHAR(100) NOT NULL,
    related_ability_id VARCHAR(50),  -- 关联通用能力ID
    strategy VARCHAR(20) NOT NULL,
    build_ratio INTEGER,
    buy_ratio INTEGER,
    primary_buy VARCHAR(100),
    reason TEXT,
    decided_by UUID REFERENCES agents(id),
    decided_at TIMESTAMP NOT NULL
);

-- 创建索引
CREATE INDEX idx_tools_related_ability ON third_party_tools(related_ability_id);
CREATE INDEX idx_decisions_related_ability ON capability_decisions(related_ability_id);
```


## 七、在Cursor中使用

```bash
# 1. 查看决策汇总
@docs/CAPABILITY_BOUNDARY_v1.0.md 显示最终决策汇总

# 2. 集成第三方工具（关联通用能力）
@docs/CAPABILITY_BOUNDARY_v1.0.md 根据EM-01外部模型调用，集成DALL-E 3图像生成API

# 3. 实现工作流编排（对齐AUTO-03）
@docs/CAPABILITY_BOUNDARY_v1.0.md 根据AUTO-03工作流自动化编排，实现工作流编排引擎

# 4. 配置品牌一致性（对齐AGENT-RUNTIME-02）
@docs/CAPABILITY_BOUNDARY_v1.0.md 根据AGENT-RUNTIME-02个人偏好，实现品牌语调学习和一致性检查

# 5. 查看通用能力映射
@docs/CAPABILITY_BOUNDARY_v1.0.md 显示AGENT-RUNTIME-01的决策是自研还是集成
```


## 八、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，对齐AGENT_ABILITY_SPEC_v1.0.md通用能力 |

---

**文档结束**