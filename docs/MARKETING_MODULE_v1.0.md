# 营销中心模块 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\MARKETING_MODULE_v1.0.md
```


# 营销中心模块 v1.0

## 一、模块定位与核心能力

```yaml
# 模块定位
module:
  name: "营销中心"
  english_name: "Marketing Center"
  description: "纪光元生智能系统的对外发声与品牌运营中枢"
  owner: "L4 营销主管"
  owner_note: "模块日常牵头角色；跨域预算与重大发布审批仍以 ORGANIZATION 中 L2 营销总经理为准"
  
  # 四大核心能力
  core_capabilities:
    - name: "全平台覆盖"
      description: "国内+国外所有主流自媒体与社交平台"
      priority: "P0"
      
    - name: "智能内容生成"
      description: "自研AI能力 + 第三方工具对接"
      priority: "P0"
      
    - name: "接单与变现"
      description: "连接技术接单平台，实现能力变现"
      priority: "P1"
      
    - name: "数据驱动优化"
      description: "多维度数据分析与策略建议"
      priority: "P1"

  # 与财务、数据域对齐：运营收入 vs 账载收入见 DATA_ANALYTICS_INSIGHT_v1.0.md §1.1
```


## 二、平台覆盖矩阵

### 2.1 平台数据模型

```python
# 平台数据模型
class Platform:
    id: str                    # 平台ID
    name: str                  # 平台名称
    category: str              # 类别：domestic/overseas/social/media/tech/order
    content_types: List[str]   # 支持的内容类型
    api_type: str              # API类型：official/third_party/manual
    api_endpoint: str          # API端点
    auth_type: str             # 认证类型：oauth/apikey/none
    priority: str              # 优先级：P0/P1/P2/P3
    status: str                # 状态：active/developing/planned
    config_fields: List[Field] # 配置字段列表

# 平台配置字段
class Field:
    name: str                  # 字段名
    type: str                  # 类型：string/secret/oauth
    required: bool             # 是否必填
    description: str           # 说明
```


### 2.2 国内平台配置

```yaml
# 国内平台清单
domestic_platforms:
  # P0：核心平台
  - id: "wechat_mp"
    name: "微信公众号"
    category: "social"
    content_types: ["article", "image", "video"]
    api_type: "official"
    priority: "P0"
    status: "planned"
    
  - id: "weibo"
    name: "微博"
    category: "social"
    content_types: ["post", "image", "video"]
    api_type: "official"
    priority: "P0"
    status: "planned"
    
  - id: "douyin"
    name: "抖音"
    category: "short_video"
    content_types: ["video", "image"]
    api_type: "official"
    priority: "P0"
    status: "planned"
    
  - id: "zhihu"
    name: "知乎"
    category: "qa"
    content_types: ["article", "answer", "video"]
    api_type: "official"
    priority: "P0"
    status: "planned"
    
  - id: "xiaohongshu"
    name: "小红书"
    category: "social"
    content_types: ["note", "image", "video"]
    api_type: "official"
    priority: "P0"
    status: "planned"
    
  # P1：重要平台
  - id: "bilibili"
    name: "B站"
    category: "video"
    content_types: ["video", "article", "dynamic"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  - id: "toutiao"
    name: "今日头条"
    category: "news"
    content_types: ["article", "video"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  - id: "juejin"
    name: "掘金"
    category: "tech"
    content_types: ["article"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  - id: "csdn"
    name: "CSDN"
    category: "tech"
    content_types: ["article", "blog"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  # P2：扩展平台
  - id: "kuaishou"
    name: "快手"
    category: "short_video"
    content_types: ["video"]
    api_type: "official"
    priority: "P2"
    status: "planned"
    
  - id: "baijiahao"
    name: "百家号"
    category: "news"
    content_types: ["article"]
    api_type: "official"
    priority: "P2"
    status: "planned"
    
  - id: "sohu"
    name: "搜狐号"
    category: "news"
    content_types: ["article"]
    api_type: "official"
    priority: "P2"
    status: "planned"
    
  - id: "163"
    name: "网易号"
    category: "news"
    content_types: ["article"]
    api_type: "official"
    priority: "P2"
    status: "planned"
```


### 2.3 国外平台配置

```yaml
# 国外平台清单
overseas_platforms:
  # P1：核心海外平台
  - id: "twitter"
    name: "X (Twitter)"
    category: "social"
    content_types: ["tweet", "image", "video"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  - id: "linkedin"
    name: "LinkedIn"
    category: "professional"
    content_types: ["post", "article", "image"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  - id: "facebook"
    name: "Facebook"
    category: "social"
    content_types: ["post", "image", "video"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  - id: "instagram"
    name: "Instagram"
    category: "social"
    content_types: ["post", "story", "reel"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  - id: "youtube"
    name: "YouTube"
    category: "video"
    content_types: ["video", "shorts", "post"]
    api_type: "official"
    priority: "P1"
    status: "planned"
    
  # P2：扩展海外平台
  - id: "tiktok"
    name: "TikTok"
    category: "short_video"
    content_types: ["video"]
    api_type: "official"
    priority: "P2"
    status: "planned"
    
  - id: "medium"
    name: "Medium"
    category: "blog"
    content_types: ["article"]
    api_type: "official"
    priority: "P2"
    status: "planned"
    
  - id: "devto"
    name: "Dev.to"
    category: "tech"
    content_types: ["article"]
    api_type: "official"
    priority: "P2"
    status: "planned"
    
  - id: "github"
    name: "GitHub"
    category: "tech"
    content_types: ["readme", "discussion"]
    api_type: "official"
    priority: "P1"
    status: "planned"
```


### 2.4 技术接单平台配置

```yaml
# 技术接单平台清单
order_platforms:
  - id: "proginn"
    name: "程序员客栈"
    category: "order"
    description: "中高级开发者稳定接单"
    api_type: "third_party"
    priority: "P1"
    status: "planned"
    
  - id: "mashangda"
    name: "码上达"
    category: "order"
    description: "新手友好、碎片化接单"
    api_type: "third_party"
    priority: "P1"
    status: "planned"
    
  - id: "upwork"
    name: "Upwork"
    category: "order"
    description: "全球自由职业平台"
    api_type: "official"
    priority: "P2"
    status: "planned"
    
  - id: "codeshifu"
    name: "码市"
    category: "order"
    description: "团队外包项目"
    api_type: "third_party"
    priority: "P2"
    status: "planned"
    
  - id: "fiverr"
    name: "Fiverr"
    category: "order"
    description: "服务商品化平台"
    api_type: "official"
    priority: "P2"
    status: "planned"
```


## 三、功能详细定义

### 3.1 MK-01 数据看板

```yaml
# MK-01 数据看板
function_id: "MK-01"
name: "数据看板"
description: "展示粉丝增长、内容互动数据"
priority: "P0"
assigned_to: "L4 营销主管"

# 数据看板数据模型
class MarketingDashboard:
    # 粉丝数据
    followers:
      total: int               # 总粉丝数
      daily_change: int        # 日变化
      weekly_change: int       # 周变化
      trend: List[DailyData]   # 趋势数据
      
    # 内容数据
    contents:
      published: int           # 已发布数量
      draft: int               # 草稿数量
      scheduled: int           # 定时发布数量
      
    # 互动数据
    engagement:
      likes: int               # 点赞总数
      comments: int            # 评论总数
      shares: int              # 分享总数
      avg_rate: float          # 平均互动率
      
    # 收益数据
    revenue:
      total: float             # 总收益
      monthly: float           # 月收益
      trend: str               # 趋势

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/dashboard"
    description: "获取营销数据看板"
    response: "MarketingDashboard"
    
  - method: "GET"
    endpoint: "/api/v1/marketing/dashboard/platforms"
    description: "获取各平台数据"
    response: "List[PlatformData]"
    
  - method: "GET"
    endpoint: "/api/v1/marketing/dashboard/trends"
    description: "获取趋势数据"
    query_params:
      days: 30
      metric: "followers|engagement|revenue"
    response: "TrendData"

# 前端组件
frontend:
  component: "MarketingDashboard.vue"
  features:
    - "KPI卡片（粉丝数、发布数、互动率、收益）"
    - "粉丝增长趋势图"
    - "内容发布日历"
    - "平台数据对比"
    - "热门内容排行"
    - "实时数据刷新"
```


### 3.2 MK-02 内容管理

```yaml
# MK-02 内容管理
function_id: "MK-02"
name: "内容管理"
description: "创建、编辑、发布营销内容"
priority: "P0"
assigned_to: "L5 资深内容运营"

# 内容数据模型
class MarketingContent:
    id: str
    title: str                 # 标题
    content: str               # 内容正文
    summary: str               # 摘要
    platform_ids: List[str]    # 目标平台
    content_type: str          # 类型：article/image/video
    status: ContentStatus      # 状态
    scheduled_at: datetime     # 定时发布时间
    published_at: datetime     # 实际发布时间
    tags: List[str]            # 标签
    author_id: str             # 作者ID
    created_at: datetime
    updated_at: datetime
    
    # 发布后数据
    engagement: EngagementData # 互动数据

# 内容状态枚举
class ContentStatus:
    DRAFT = "draft"            # 草稿
    REVIEWING = "reviewing"    # 审核中
    SCHEDULED = "scheduled"    # 定时发布
    PUBLISHED = "published"    # 已发布
    FAILED = "failed"          # 发布失败

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/contents"
    description: "获取内容列表"
    query_params:
      status: "string"
      platform: "string"
      page: 1
      page_size: 20
    response: "List[MarketingContent]"
    
  - method: "GET"
    endpoint: "/api/v1/marketing/contents/{id}"
    description: "获取内容详情"
    response: "MarketingContent"
    
  - method: "POST"
    endpoint: "/api/v1/marketing/contents"
    description: "创建内容"
    request_body: "MarketingContent"
    response: "MarketingContent"
    
  - method: "PUT"
    endpoint: "/api/v1/marketing/contents/{id}"
    description: "更新内容"
    request_body: "MarketingContent"
    response: "MarketingContent"
    
  - method: "DELETE"
    endpoint: "/api/v1/marketing/contents/{id}"
    description: "删除内容"
    response: "success"
    
  - method: "POST"
    endpoint: "/api/v1/marketing/contents/{id}/publish"
    description: "发布内容"
    request_body:
      platforms: "List[str]"
      scheduled_at: "datetime"
    response: "PublishResult"

# 前端组件
frontend:
  component: "ContentManagement.vue"
  features:
    - "内容列表（表格/卡片视图）"
    - "富文本编辑器"
    - "平台选择器"
    - "定时发布设置"
    - "内容预览"
    - "发布状态跟踪"
    - "批量操作"
```


### 3.3 MK-03 AI生成内容

```yaml
# MK-03 AI生成内容
function_id: "MK-03"
name: "AI生成内容"
description: "使用AI自动生成营销内容"
priority: "P0"
assigned_to: "L5 资深内容运营 + L1 主脑"

# AI生成请求模型
class AIGenerateRequest:
    topic: str                 # 主题
    platform: str              # 目标平台
    content_type: str          # 内容类型
    tone: str                  # 语气：professional/casual/humorous
    length: str                # 长度：short/medium/long
    keywords: List[str]        # 关键词
    reference_links: List[str] # 参考链接
    brand_voice: str           # 品牌语调

# AI生成响应模型
class AIGenerateResponse:
    title: str                 # 生成的标题
    content: str               # 生成的内容
    summary: str               # 摘要
    tags: List[str]            # 建议标签
    seo_score: int             # SEO评分
    readability_score: int     # 可读性评分

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/ai/generate"
    description: "AI生成内容"
    request_body: "AIGenerateRequest"
    response: "AIGenerateResponse"
    
  - method: "POST"
    endpoint: "/api/v1/marketing/ai/optimize"
    description: "AI优化现有内容"
    request_body:
      content_id: "str"
      optimization_type: "seo|readability|tone"
    response: "AIGenerateResponse"
    
  - method: "POST"
    endpoint: "/api/v1/marketing/ai/rewrite"
    description: "AI改写内容"
    request_body:
      content: "str"
      style: "str"
    response: "AIGenerateResponse"
    
  - method: "POST"
    endpoint: "/api/v1/marketing/ai/translate"
    description: "AI翻译内容"
    request_body:
      content_id: "str"
      target_language: "str"
    response: "AIGenerateResponse"

# AI生成配置
ai_generation_config:
  # 各平台内容模板
  templates:
    wechat_mp:
      title_max_length: 64
      content_min_length: 500
      recommended_length: 1500
      structure: ["开场", "正文", "案例", "总结", "引导"]
      
    zhihu:
      title_max_length: 100
      content_min_length: 300
      recommended_length: 2000
      structure: ["问题重述", "分析", "解决方案", "总结"]
      
    juejin:
      title_max_length: 60
      content_min_length: 200
      recommended_length: 800
      structure: ["背景", "实现", "总结"]
      
    twitter:
      max_length: 280
      structure: ["核心观点", "链接/图片", "话题标签"]
      
  # 品牌语调配置
  brand_voice:
    professional:
      keywords: ["专业", "深度", "权威", "严谨"]
      forbidden: ["夸张", "低俗", "不实"]
    casual:
      keywords: ["轻松", "有趣", "易懂", "亲和"]
      forbidden: ["生硬", "说教"]
    humorous:
      keywords: ["幽默", "调侃", "轻松", "创意"]
      forbidden: ["低俗", "攻击性"]
```


### 3.4 MK-04 多平台发布

```yaml
# MK-04 多平台发布
function_id: "MK-04"
name: "多平台发布"
description: "发布到多个自媒体平台"
priority: "P1"
assigned_to: "L5 资深内容运营"

# 发布任务模型
class PublishTask:
    id: str
    content_id: str
    platform_id: str
    status: PublishStatus
    scheduled_at: datetime
    published_at: datetime
    error_message: str
    retry_count: int
    created_at: datetime

# 发布状态枚举
class PublishStatus:
    PENDING = "pending"        # 等待发布
    PROCESSING = "processing"  # 发布中
    SUCCESS = "success"        # 发布成功
    FAILED = "failed"          # 发布失败

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/publish/batch"
    description: "批量发布到多平台"
    request_body:
      content_id: "str"
      platforms: "List[str]"
      scheduled_at: "datetime"
    response: "List[PublishTask]"
    
  - method: "GET"
    endpoint: "/api/v1/marketing/publish/tasks"
    description: "获取发布任务列表"
    response: "List[PublishTask]"
    
  - method: "GET"
    endpoint: "/api/v1/marketing/publish/status/{task_id}"
    description: "获取发布状态"
    response: "PublishTask"
    
  - method: "POST"
    endpoint: "/api/v1/marketing/publish/cancel/{task_id}"
    description: "取消发布任务"
    response: "success"

# 平台适配器
platform_adapters:
  wechat_mp:
    content_mapping:
      title: "article.title"
      content: "article.content"
      thumb_media_id: "article.thumb"
      author: "article.author"
      
  zhihu:
    content_mapping:
      title: "title"
      content: "content"
      topics: "topics"
      column_id: "column_id"
      
  juejin:
    content_mapping:
      title: "title"
      content: "content"
      category: "category"
      tags: "tags"
      
  twitter:
    content_mapping:
      text: "content"
      media_ids: "media_ids"
```


## 四、API接口汇总

```yaml
# 营销中心模块API汇总

api_summary:
  base_path: "/api/v1/marketing"
  
  # 数据看板
  - method: "GET"
    path: "/dashboard"
    function: "MK-01"
    
  - method: "GET"
    path: "/dashboard/platforms"
    function: "MK-01"
    
  - method: "GET"
    path: "/dashboard/trends"
    function: "MK-01"
    
  # 内容管理
  - method: "GET"
    path: "/contents"
    function: "MK-02"
    
  - method: "GET"
    path: "/contents/{id}"
    function: "MK-02"
    
  - method: "POST"
    path: "/contents"
    function: "MK-02"
    
  - method: "PUT"
    path: "/contents/{id}"
    function: "MK-02"
    
  - method: "DELETE"
    path: "/contents/{id}"
    function: "MK-02"
    
  - method: "POST"
    path: "/contents/{id}/publish"
    function: "MK-02"
    
  # AI生成
  - method: "POST"
    path: "/ai/generate"
    function: "MK-03"
    
  - method: "POST"
    path: "/ai/optimize"
    function: "MK-03"
    
  - method: "POST"
    path: "/ai/rewrite"
    function: "MK-03"
    
  - method: "POST"
    path: "/ai/translate"
    function: "MK-03"
    
  # 批量发布
  - method: "POST"
    path: "/publish/batch"
    function: "MK-04"
    
  - method: "GET"
    path: "/publish/tasks"
    function: "MK-04"
    
  - method: "GET"
    path: "/publish/status/{task_id}"
    function: "MK-04"
    
  - method: "POST"
    path: "/publish/cancel/{task_id}"
    function: "MK-04"
    
  # 平台管理
  - method: "GET"
    path: "/platforms"
    description: "获取平台列表"
    
  - method: "POST"
    path: "/platforms/{id}/connect"
    description: "连接平台账号"
    
  - method: "DELETE"
    path: "/platforms/{id}/disconnect"
    description: "断开平台连接"
```


## 五、数据库表结构

```sql
-- 平台配置表
CREATE TABLE marketing_platforms (
    id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL,
    config JSONB,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL
);

-- 内容表
CREATE TABLE marketing_contents (
    id UUID PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    content_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    tags TEXT[],
    author_id UUID REFERENCES agents(id),
    engagement JSONB,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 发布任务表
CREATE TABLE marketing_publish_tasks (
    id UUID PRIMARY KEY,
    content_id UUID REFERENCES marketing_contents(id),
    platform_id UUID REFERENCES marketing_platforms(id),
    status VARCHAR(20) NOT NULL,
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    created_at TIMESTAMP NOT NULL
);

-- 平台账号连接表
CREATE TABLE marketing_platform_connections (
    id UUID PRIMARY KEY,
    platform_id UUID REFERENCES marketing_platforms(id),
    account_name VARCHAR(100) NOT NULL,
    auth_data JSONB NOT NULL,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```


## 六、前端组件结构

```
frontend/src/views/marketing/
├── MarketingDashboard.vue      # 数据看板
├── ContentManagement.vue        # 内容管理
├── ContentEditor.vue            # 内容编辑器
├── ContentPreview.vue           # 内容预览
├── AIGenerate.vue               # AI生成
├── PublishManager.vue           # 发布管理
├── PlatformManager.vue          # 平台管理
├── AnalyticsReport.vue          # 分析报告
└── components/
    ├── KPICard.vue              # KPI卡片
    ├── TrendChart.vue           # 趋势图
    ├── PlatformSelector.vue     # 平台选择器
    ├── ContentCard.vue          # 内容卡片
    └── PublishStatus.vue        # 发布状态
```


## 七、在Cursor中使用

```bash
# 1. 实现数据看板
@docs/MARKETING_MODULE_v1.0.md 实现MK-01数据看板，包括KPI卡片和趋势图

# 2. 实现内容管理
@docs/MARKETING_MODULE_v1.0.md 实现MK-02内容管理，包括富文本编辑器和发布功能

# 3. 实现AI生成内容
@docs/MARKETING_MODULE_v1.0.md 实现MK-03 AI生成内容，集成大模型生成营销内容

# 4. 实现多平台发布
@docs/MARKETING_MODULE_v1.0.md 实现MK-04多平台发布，支持批量发布到多个平台

# 5. 添加新平台
@docs/MARKETING_MODULE_v1.0.md 按照格式添加一个新平台：小红书
```


**文档结束**