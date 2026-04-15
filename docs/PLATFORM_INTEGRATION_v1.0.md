# 专业与技术接单平台集成 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\PLATFORM_INTEGRATION_v1.0.md
```


# 专业与技术接单平台集成 v1.0

## 一、集成架构概述

```yaml
# 集成策略
integration_strategy:
  principle: "系统不直接替代接单平台，而是作为智能助手"
  capabilities:
    - "自动筛选匹配项目"
    - "生成报价方案"
    - "辅助沟通"
    - "最终引导至目标平台完成交易"
  
  architecture: |
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                         纪光元生智能系统                                    │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │                        接单智能助手                                  │   │
    │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
    │  │  │ 项目匹配  │→│ 报价生成  │→│ 沟通辅助  │→│ 平台引导  │        │   │
    │  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    │                                    │                                        │
    │                                    ▼                                        │
    │  ┌─────────────────────────────────────────────────────────────────────┐   │
    │  │                        平台适配层                                    │   │
    │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐      │   │
    │  │  │程序员客栈│ │ 码上达  │ │ 码市    │ │ 实现网  │ │ Upwork  │      │   │
    │  │  │ API适配 │ │ API适配 │ │ API适配│ │ API适配│ │ API适配│      │   │
    │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘      │   │
    │  └─────────────────────────────────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────────┘
```


## 二、平台数据模型

```python
# 平台定义
class Platform:
    id: str                    # 平台ID
    name: str                  # 平台名称
    code: str                  # 平台代码
    category: str              # 类别：domestic/international
    priority: str              # 优先级：P0/P1/P2
    api_type: str              # API类型：official/webhook/manual
    api_endpoint: str          # API端点
    auth_type: str             # 认证类型：oauth/apikey/none
    
# 项目数据模型
class PlatformProject:
    id: str                    # 项目ID
    platform_id: str           # 所属平台
    title: str                 # 项目标题
    description: str           # 项目描述
    budget: Budget             # 预算
    skills: List[str]          # 所需技能
    experience_level: str      # 经验要求：junior/middle/senior
    project_type: str          # 项目类型：full_time/part_time/fixed
    duration: str              # 项目周期
    status: str                # 状态：open/closed/awarded
    posted_at: datetime        # 发布时间
    url: str                   # 项目链接
    
# 匹配结果
class MatchResult:
    project: PlatformProject   # 匹配的项目
    score: float               # 匹配分数 0-100
    reason: str                # 匹配原因
    suggested_quote: float     # 建议报价
    suggested_approach: str    # 建议方案
    
# 报价方案
class QuoteProposal:
    project_id: str            # 项目ID
    amount: float              # 报价金额
    timeline: str              # 交付时间线
    approach: str              # 技术方案
    portfolio: List[str]       # 作品展示
    questions: List[str]       # 待确认问题
```


## 三、平台详细配置

### 3.1 国内平台

```yaml
# 程序员客栈
- id: "proginn"
  name: "程序员客栈"
  code: "PROGINN"
  category: "domestic"
  priority: "P0"
  api_type: "official"
  api_endpoint: "https://www.proginn.com/api"
  auth_type: "oauth"
  
  features:
    - "项目自动抓取"
    - "技能匹配筛选"
    - "报价参考"
    - "接单申请提交"
    
  user_profile:
    experience: "2-5年"
    positioning: "中高级开发者稳定接单"
    
  matching_rules:
    - "技能匹配度 > 70%"
    - "预算 > 5000元"
    - "项目周期 < 30天"

# 码上达
- id: "mashangda"
  name: "码上达"
  code: "MASHANGDA"
  category: "domestic"
  priority: "P0"
  api_type: "webhook"
  api_endpoint: "https://www.mashangda.com/api"
  auth_type: "apikey"
  
  features:
    - "碎片化任务匹配"
    - "新手友好筛选"
    - "快速报价"
    
  user_profile:
    experience: "0-3年"
    positioning: "新手友好、碎片化接单"
    
  matching_rules:
    - "技能匹配度 > 50%"
    - "预算 500-5000元"
    - "项目周期 < 7天"

# 码市
- id: "coding"
  name: "码市"
  code: "CODING"
  category: "domestic"
  priority: "P1"
  api_type: "official"
  api_endpoint: "https://mart.coding.net/api"
  auth_type: "oauth"
  
  features:
    - "团队项目匹配"
    - "团队能力展示"
    - "协作报价"
    
  user_profile:
    experience: "3-8年"
    positioning: "团队外包项目"
    
  matching_rules:
    - "团队技能覆盖 > 80%"
    - "预算 > 10000元"
    - "项目周期 15-60天"

# 实现网
- id: "shixian"
  name: "实现网"
  code: "SHIXIAN"
  category: "domestic"
  priority: "P1"
  api_type: "webhook"
  api_endpoint: "https://www.shixian.com/api"
  auth_type: "apikey"
  
  features:
    - "企业级项目筛选"
    - "驻场/远程筛选"
    - "合同管理辅助"
    
  user_profile:
    experience: "5-10年"
    positioning: "企业级项目"
    
  matching_rules:
    - "技能匹配度 > 85%"
    - "预算 > 20000元"
    - "有企业项目经验"

# 程聚宝
- id: "chengjubao"
  name: "程聚宝"
  code: "CHENGJUBAO"
  category: "domestic"
  priority: "P1"
  api_type: "webhook"
  api_endpoint: "https://www.chengjubao.com/api"
  auth_type: "apikey"
  
  features:
    - "高质量项目筛选"
    - "长期合作匹配"
    - "信用评估"
    
  user_profile:
    experience: "3-10年"
    positioning: "高质量项目筛选"
    
  matching_rules:
    - "技能匹配度 > 75%"
    - "信用分 > 80"
    - "预算 > 8000元"

# 猪八戒网
- id: "zbj"
  name: "猪八戒网"
  code: "ZBJ"
  category: "domestic"
  priority: "P2"
  api_type: "manual"
  api_endpoint: "https://www.zbj.com/api"
  auth_type: "apikey"
  
  features:
    - "综合类目筛选"
    - "竞标分析"
    - "价格参考"
    
  user_profile:
    experience: "0-10年"
    positioning: "综合外包"
    
  matching_rules:
    - "技能匹配度 > 60%"
    - "预算范围不限"
```


### 3.2 国际平台

```yaml
# Upwork
- id: "upwork"
  name: "Upwork"
  code: "UPWORK"
  category: "international"
  priority: "P1"
  api_type: "official"
  api_endpoint: "https://api.upwork.com/api/v3"
  auth_type: "oauth"
  
  features:
    - "全球项目匹配"
    - "时区适配"
    - "英语能力评估"
    - "美元报价"
    
  user_profile:
    experience: "2-10年"
    positioning: "全球自由职业"
    english_level: "IELTS 6.5+"
    
  matching_rules:
    - "技能匹配度 > 70%"
    - "英语评分 > 4.0"
    - "JSS评分 > 90%"

# Toptal
- id: "toptal"
  name: "Toptal"
  code: "TOPTAL"
  category: "international"
  priority: "P2"
  api_type: "manual"
  api_endpoint: "https://www.toptal.com/api"
  auth_type: "oauth"
  
  features:
    - "高端项目匹配"
    - "严格筛选流程"
    - "专属顾问对接"
    
  user_profile:
    experience: "5-15年"
    positioning: "高端程序员（前10%）"
    english_level: "IELTS 7.5+"
    
  matching_rules:
    - "技能匹配度 > 90%"
    - "通过平台技术测试"
    - "时薪 > $60"

# Fiverr
- id: "fiverr"
  name: "Fiverr"
  code: "FIVERR"
  category: "international"
  priority: "P2"
  api_type: "official"
  api_endpoint: "https://api.fiverr.com/v2"
  auth_type: "oauth"
  
  features:
    - "服务商品化"
    - "标准化报价"
    - "快速成交"
    
  user_profile:
    experience: "0-5年"
    positioning: "新手、标准化服务"
    english_level: "IELTS 5.5+"
    
  matching_rules:
    - "技能匹配度 > 50%"
    - "服务定价合理"
    - "响应时间 < 1小时"

# Gun.io
- id: "gunio"
  name: "Gun.io"
  code: "GUNIO"
  category: "international"
  priority: "P2"
  api_type: "manual"
  api_endpoint: "https://gun.io/api"
  auth_type: "oauth"
  
  features:
    - "高品质兼职"
    - "技术筛选"
    - "长期合作"
    
  user_profile:
    experience: "5-12年"
    positioning: "资深开发者"
    english_level: "IELTS 7.0+"
    
  matching_rules:
    - "技能匹配度 > 80%"
    - "技术栈深度匹配"
    - "时薪 > $80"

# RemoteOK
- id: "remoteok"
  name: "RemoteOK"
  code: "REMOTEOK"
  category: "international"
  priority: "P2"
  api_type: "webhook"
  api_endpoint: "https://remoteok.com/api"
  auth_type: "apikey"
  
  features:
    - "远程工作匹配"
    - "全职/兼职筛选"
    - "地域不限"
    
  user_profile:
    experience: "2-10年"
    positioning: "远程工作者"
    english_level: "IELTS 6.0+"
    
  matching_rules:
    - "技能匹配度 > 60%"
    - "远程经验 > 1年"
    - "时区可重叠 > 4小时"
```


## 四、功能详细设计

### 4.1 项目自动匹配

```yaml
# 功能：项目自动匹配
function_id: "PI-01"
name: "项目自动匹配"
description: "自动从各平台抓取项目并匹配智能体技能"
priority: "P0"

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/platform/projects/matched"
    description: "获取匹配的项目列表"
    response: "List[MatchResult]"
    
  - method: "POST"
    endpoint: "/api/v1/platform/projects/sync"
    description: "手动触发项目同步"
    response: "sync_result"
    
  - method: "POST"
    endpoint: "/api/v1/platform/projects/{project_id}/match-score"
    description: "计算项目匹配分数"
    response: "MatchResult"

# 匹配算法
matching_algorithm:
  factors:
    - name: "技能匹配"
      weight: 0.35
      description: "项目所需技能与智能体技能的匹配度"
      
    - name: "经验匹配"
      weight: 0.20
      description: "项目经验要求与智能体经验的匹配度"
      
    - name: "预算匹配"
      weight: 0.15
      description: "项目预算与智能体期望的匹配度"
      
    - name: "时间匹配"
      weight: 0.15
      description: "项目周期与智能体可用时间的匹配度"
      
    - name: "历史匹配"
      weight: 0.10
      description: "类似项目的成功历史"
      
    - name: "信用匹配"
      weight: 0.05
      description: "智能体在平台上的信用评分"

# 定时同步配置
sync_schedule:
  domestic_platforms:
    cron: "*/30 * * * *"       # 每30分钟
    platforms: ["proginn", "mashangda", "coding", "shixian", "chengjubao"]
    
  international_platforms:
    cron: "0 */2 * * *"        # 每2小时
    platforms: ["upwork", "fiverr", "remoteok"]
```


### 4.2 报价生成

```yaml
# 功能：报价生成
function_id: "PI-02"
name: "报价生成"
description: "根据项目需求自动生成报价方案"
priority: "P0"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/platform/projects/{project_id}/quote/generate"
    description: "生成报价方案"
    response: "QuoteProposal"
    
  - method: "POST"
    endpoint: "/api/v1/platform/projects/{project_id}/quote/submit"
    description: "提交报价"
    request_body:
      proposal: "QuoteProposal"
    response: "submission_result"

# 报价计算规则
quote_calculation:
  hourly_rate:
    junior: 50-100             # 元/小时
    middle: 100-200
    senior: 200-400
    expert: 400-800
    
  fixed_price:
    base_formula: "estimated_hours * hourly_rate * 1.2"  # 20%风险缓冲
    min_price: 500             # 最低报价
    max_price: 100000          # 最高报价
    
  adjustment_factors:
    - name: "复杂度"
      range: [0.8, 1.5]
    - name: "紧急度"
      range: [1.0, 2.0]
    - name: "长期合作"
      range: [0.7, 1.0]
    - name: "平台抽成"
      range: [1.05, 1.25]

# 报价模板
quote_templates:
  - name: "标准模板"
    sections:
      - "项目理解"
      - "技术方案"
      - "时间安排"
      - "报价明细"
      - "交付物清单"
      - "售后服务"
      
  - name: "快速模板"
    sections:
      - "报价金额"
      - "预计工期"
      - "主要交付物"
```


### 4.3 沟通辅助

```yaml
# 功能：沟通辅助
function_id: "PI-03"
name: "沟通辅助"
description: "辅助智能体与客户沟通"
priority: "P1"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/platform/projects/{project_id}/communication/suggest"
    description: "生成沟通建议"
    request_body:
      context: "string"        # 对话上下文
    response:
      suggested_reply: "string"
      questions: "List[str]"
      
  - method: "POST"
    endpoint: "/api/v1/platform/projects/{project_id}/communication/analyze"
    description: "分析客户意图"
    request_body:
      message: "string"
    response:
      intent: "string"
      sentiment: "string"
      key_points: "List[str]"

# 沟通模板
communication_templates:
  - scenario: "初次接触"
    template: |
      您好，我是【智能体名称】。
      
      我看到您在【平台名称】上发布了【项目名称】的项目。
      
      我对这个项目很感兴趣，我的技术栈包括：【技能列表】。
      
      我之前有【X年】的【领域】开发经验，曾为【客户案例】提供服务。
      
      请问您方便详细聊聊项目需求吗？
      
  - scenario: "报价说明"
    template: |
      感谢您的信任。
      
      根据项目需求，我的报价方案如下：
      
      📊 报价明细：
      • 开发费用：¥【金额】
      • 预计工期：【X】天
      • 交付物：【清单】
      
      报价包含：
      ✅ 【服务1】
      ✅ 【服务2】
      
      不包含：
      ❌ 【不包含项】
      
      如有疑问，随时沟通。
      
  - scenario: "进度汇报"
    template: |
      【项目名称】项目进度汇报
      
      当前进度：【进度】%
      
      已完成：
      ✅ 【完成项1】
      ✅ 【完成项2】
      
      进行中：
      🔄 【进行中项】
      
      下一步计划：
      📋 【计划项】
      
      预计【日期】完成。
```


## 五、数据模型汇总

```python
# 平台集成数据模型

class PlatformConfig:
    """平台配置"""
    id: str
    name: str
    code: str
    category: str
    priority: str
    api_type: str
    api_endpoint: str
    auth_config: dict
    enabled: bool
    sync_cron: str
    created_at: datetime
    updated_at: datetime

class PlatformProject:
    """平台项目"""
    id: str
    platform_id: str
    external_id: str
    title: str
    description: str
    budget_min: float
    budget_max: float
    budget_currency: str
    skills: List[str]
    experience_level: str
    project_type: str
    duration_days: int
    status: str
    posted_at: datetime
    url: str
    raw_data: dict
    created_at: datetime
    updated_at: datetime

class ProjectMatch:
    """项目匹配"""
    id: str
    project_id: str
    agent_id: str
    match_score: float
    match_details: dict
    suggested_quote: float
    status: str  # pending/accepted/rejected
    created_at: datetime

class QuoteSubmission:
    """报价提交"""
    id: str
    project_id: str
    agent_id: str
    amount: float
    currency: str
    timeline_days: int
    proposal_content: dict
    status: str  # submitted/accepted/rejected/expired
    submitted_at: datetime
    responded_at: datetime

class CommunicationLog:
    """沟通记录"""
    id: str
    project_id: str
    agent_id: str
    direction: str  # inbound/outbound
    content: str
    intent: str
    sentiment: str
    created_at: datetime
```


## 六、数据库表结构

```sql
-- 平台配置表
CREATE TABLE platform_configs (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(20) NOT NULL,
    priority VARCHAR(10) NOT NULL,
    api_type VARCHAR(20) NOT NULL,
    api_endpoint VARCHAR(500),
    auth_config JSONB,
    enabled BOOLEAN DEFAULT TRUE,
    sync_cron VARCHAR(100),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 平台项目表
CREATE TABLE platform_projects (
    id UUID PRIMARY KEY,
    platform_id UUID REFERENCES platform_configs(id),
    external_id VARCHAR(200) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    budget_min DECIMAL(10,2),
    budget_max DECIMAL(10,2),
    budget_currency VARCHAR(3) DEFAULT 'CNY',
    skills TEXT[],
    experience_level VARCHAR(20),
    project_type VARCHAR(50),
    duration_days INTEGER,
    status VARCHAR(20) DEFAULT 'open',
    posted_at TIMESTAMP,
    url VARCHAR(500),
    raw_data JSONB,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE(platform_id, external_id)
);

-- 项目匹配表
CREATE TABLE project_matches (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES platform_projects(id),
    agent_id UUID REFERENCES agents(id),
    match_score DECIMAL(5,2),
    match_details JSONB,
    suggested_quote DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL,
    UNIQUE(project_id, agent_id)
);

-- 报价提交表
CREATE TABLE quote_submissions (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES platform_projects(id),
    agent_id UUID REFERENCES agents(id),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'CNY',
    timeline_days INTEGER,
    proposal_content JSONB,
    status VARCHAR(20) DEFAULT 'submitted',
    submitted_at TIMESTAMP NOT NULL,
    responded_at TIMESTAMP
);

-- 沟通记录表
CREATE TABLE communication_logs (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES platform_projects(id),
    agent_id UUID REFERENCES agents(id),
    direction VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    intent VARCHAR(50),
    sentiment VARCHAR(20),
    created_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_platform_projects_platform ON platform_projects(platform_id);
CREATE INDEX idx_platform_projects_status ON platform_projects(status);
CREATE INDEX idx_platform_projects_posted ON platform_projects(posted_at);
CREATE INDEX idx_project_matches_agent ON project_matches(agent_id);
CREATE INDEX idx_project_matches_score ON project_matches(match_score DESC);
CREATE INDEX idx_quote_submissions_project ON quote_submissions(project_id);
CREATE INDEX idx_quote_submissions_status ON quote_submissions(status);
```


## 七、API接口汇总

```yaml
# 平台集成API

api_summary:
  base_path: "/api/v1/platform"
  
  projects:
    - method: "GET"
      path: "/projects"
      description: "获取项目列表"
      
    - method: "GET"
      path: "/projects/matched"
      description: "获取匹配项目"
      
    - method: "POST"
      path: "/projects/sync"
      description: "同步项目"
      
    - method: "GET"
      path: "/projects/{id}"
      description: "获取项目详情"
      
  matching:
    - method: "POST"
      path: "/projects/{id}/match-score"
      description: "计算匹配分数"
      
    - method: "GET"
      path: "/matches"
      description: "获取匹配列表"
      
    - method: "POST"
      path: "/matches/{id}/accept"
      description: "接受匹配"
      
    - method: "POST"
      path: "/matches/{id}/reject"
      description: "拒绝匹配"
      
  quote:
    - method: "POST"
      path: "/projects/{id}/quote/generate"
      description: "生成报价"
      
    - method: "POST"
      path: "/projects/{id}/quote/submit"
      description: "提交报价"
      
    - method: "GET"
      path: "/quotes"
      description: "获取报价列表"
      
  communication:
    - method: "POST"
      path: "/projects/{id}/communication/suggest"
      description: "沟通建议"
      
    - method: "POST"
      path: "/projects/{id}/communication/analyze"
      description: "分析消息"
      
    - method: "GET"
      path: "/projects/{id}/communication/history"
      description: "沟通历史"
```


## 八、在Cursor中使用

```bash
# 1. 添加新平台
@docs/PLATFORM_INTEGRATION_v1.0.md 按照格式添加新平台：程序员客栈

# 2. 实现项目匹配
@docs/PLATFORM_INTEGRATION_v1.0.md 实现项目自动匹配功能，包括技能匹配算法

# 3. 实现报价生成
@docs/PLATFORM_INTEGRATION_v1.0.md 实现报价生成功能，支持固定价格和按小时报价

# 4. 配置同步任务
@docs/PLATFORM_INTEGRATION_v1.0.md 配置各平台的定时同步任务
```


**文档结束**