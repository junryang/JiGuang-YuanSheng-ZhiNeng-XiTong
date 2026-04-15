# 国内自媒体平台配置 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\DOMESTIC_PLATFORMS_CONFIG_v1.0.md
```


# 国内自媒体平台配置 v1.0

## 一、平台数据模型

```python
# 平台配置数据模型
class PlatformConfig:
    id: str                    # 平台唯一标识
    name: str                  # 平台名称
    category: str              # 类别：portal/short_video/social/tech/enterprise
    content_types: List[str]   # 支持的内容类型
    api_type: str              # API类型：official/third_party
    api_version: str           # API版本
    auth_type: str             # 认证方式：oauth/apikey/wechat_login
    priority: str              # 优先级：P0/P1/P2/P3
    status: str                # 状态：active/developing/planned
    rate_limit: RateLimit      # 接口限制
    config_fields: List[ConfigField]  # 配置字段

# 接口限制
class RateLimit:
    requests_per_day: int      # 每日请求上限
    requests_per_minute: int   # 每分钟请求上限
    concurrent: int            # 并发数限制

# 配置字段
class ConfigField:
    name: str                  # 字段名
    type: str                  # 类型：string/secret/oauth_file
    required: bool             # 是否必填
    description: str           # 说明
    placeholder: str           # 示例值
```


## 二、平台配置清单

### 2.1 综合门户类

```yaml
# 综合门户平台配置
portal_platforms:
  # P0 平台
  - id: "wechat_mp"
    name: "微信公众号"
    category: "portal"
    content_types: ["article", "image", "video", "audio"]
    api_type: "official"
    api_version: "v2"
    auth_type: "wechat_login"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 100000
      requests_per_minute: 500
      concurrent: 10
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "公众号AppID"
        placeholder: "wx1234567890abcdef"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "公众号AppSecret"
        placeholder: "1234567890abcdef1234567890abcdef"
        
  - id: "toutiao"
    name: "今日头条"
    category: "portal"
    content_types: ["article", "micro_article", "video"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 300
      concurrent: 5
    config_fields:
      - name: "client_key"
        type: "string"
        required: true
        description: "头条Client Key"
      - name: "client_secret"
        type: "secret"
        required: true
        description: "头条Client Secret"
        
  - id: "baijiahao"
    name: "百家号"
    category: "portal"
    content_types: ["article", "image", "video"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 30000
      requests_per_minute: 200
      concurrent: 5
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "百家号AppID"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "百家号AppSecret"

  # P1 平台
  - id: "sohu"
    name: "搜狐号"
    category: "portal"
    content_types: ["article", "image"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 20000
      requests_per_minute: 100
      concurrent: 3
    config_fields:
      - name: "api_key"
        type: "string"
        required: true
        description: "搜狐API Key"
      - name: "api_secret"
        type: "secret"
        required: true
        description: "搜狐API Secret"
        
  - id: "163"
    name: "网易号"
    category: "portal"
    content_types: ["article", "image", "video"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 20000
      requests_per_minute: 100
      concurrent: 3
    config_fields:
      - name: "app_key"
        type: "string"
        required: true
        description: "网易App Key"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "网易App Secret"
        
  - id: "tencent_news"
    name: "腾讯新闻"
    category: "portal"
    content_types: ["article", "video"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 20000
      requests_per_minute: 100
      concurrent: 3
    config_fields:
      - name: "open_id"
        type: "string"
        required: true
        description: "腾讯开放平台OpenID"
      - name: "access_token"
        type: "secret"
        required: true
        description: "访问令牌"

  # P2 平台
  - id: "sina_kandian"
    name: "新浪看点"
    category: "portal"
    content_types: ["article", "image"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P2"
    status: "planned"
    rate_limit:
      requests_per_day: 10000
      requests_per_minute: 50
      concurrent: 2
    config_fields:
      - name: "api_key"
        type: "string"
        required: true
        description: "新浪API Key"
      - name: "api_secret"
        type: "secret"
        required: true
        description: "新浪API Secret"
```


### 2.2 短视频类

```yaml
# 短视频平台配置
short_video_platforms:
  # P0 平台
  - id: "douyin"
    name: "抖音"
    category: "short_video"
    content_types: ["video", "image", "图文"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 200
      concurrent: 5
    config_fields:
      - name: "client_key"
        type: "string"
        required: true
        description: "抖音Client Key"
      - name: "client_secret"
        type: "secret"
        required: true
        description: "抖音Client Secret"
        
  - id: "kuaishou"
    name: "快手"
    category: "short_video"
    content_types: ["video", "image"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 30000
      requests_per_minute: 150
      concurrent: 5
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "快手App ID"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "快手App Secret"
        
  - id: "shipinhao"
    name: "视频号"
    category: "short_video"
    content_types: ["video", "image"]
    api_type: "official"
    api_version: "v1"
    auth_type: "wechat_login"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 30000
      requests_per_minute: 150
      concurrent: 5
    config_fields:
      - name: "finder_id"
        type: "string"
        required: true
        description: "视频号ID"
      - name: "token"
        type: "secret"
        required: true
        description: "视频号Token"
        
  - id: "bilibili"
    name: "B站"
    category: "short_video"
    content_types: ["video", "article", "dynamic"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 200
      concurrent: 10
    config_fields:
      - name: "access_key"
        type: "string"
        required: true
        description: "B站Access Key"
      - name: "access_secret"
        type: "secret"
        required: true
        description: "B站Access Secret"
        
  - id: "xiaohongshu"
    name: "小红书"
    category: "short_video"
    content_types: ["note", "image", "video"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 30000
      requests_per_minute: 100
      concurrent: 5
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "小红书App ID"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "小红书App Secret"
```


### 2.3 社交/社区类

```yaml
# 社交社区平台配置
social_platforms:
  # P0 平台
  - id: "weibo"
    name: "微博"
    category: "social"
    content_types: ["post", "image", "video", "article"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 100000
      requests_per_minute: 500
      concurrent: 10
    config_fields:
      - name: "app_key"
        type: "string"
        required: true
        description: "微博App Key"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "微博App Secret"
        
  - id: "zhihu"
    name: "知乎"
    category: "social"
    content_types: ["article", "answer", "video", "pin"]
    api_type: "official"
    api_version: "v4"
    auth_type: "oauth"
    priority: "P0"
    status: "planned"
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 200
      concurrent: 5
    config_fields:
      - name: "client_id"
        type: "string"
        required: true
        description: "知乎Client ID"
      - name: "client_secret"
        type: "secret"
        required: true
        description: "知乎Client Secret"

  # P2 平台
  - id: "douban"
    name: "豆瓣"
    category: "social"
    content_types: ["post", "image", "review"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P2"
    status: "planned"
    rate_limit:
      requests_per_day: 10000
      requests_per_minute: 50
      concurrent: 2
    config_fields:
      - name: "api_key"
        type: "string"
        required: true
        description: "豆瓣API Key"
      - name: "api_secret"
        type: "secret"
        required: true
        description: "豆瓣API Secret"
```


### 2.4 垂直专业类

```yaml
# 垂直专业平台配置
tech_platforms:
  # P1 平台
  - id: "juejin"
    name: "掘金"
    category: "tech"
    content_types: ["article", "image"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 10000
      requests_per_minute: 50
      concurrent: 3
    config_fields:
      - name: "user_id"
        type: "string"
        required: true
        description: "掘金用户ID"
      - name: "token"
        type: "secret"
        required: true
        description: "掘金Token"
        
  - id: "csdn"
    name: "CSDN"
    category: "tech"
    content_types: ["article", "blog", "code"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 10000
      requests_per_minute: 50
      concurrent: 3
    config_fields:
      - name: "username"
        type: "string"
        required: true
        description: "CSDN用户名"
      - name: "api_key"
        type: "secret"
        required: true
        description: "CSDN API Key"
        
  - id: "segmentfault"
    name: "思否"
    category: "tech"
    content_types: ["article", "answer"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 5000
      requests_per_minute: 30
      concurrent: 2
    config_fields:
      - name: "client_id"
        type: "string"
        required: true
        description: "思否Client ID"
      - name: "client_secret"
        type: "secret"
        required: true
        description: "思否Client Secret"

  # P2 平台
  - id: "woshipm"
    name: "人人都是产品经理"
    category: "tech"
    content_types: ["article"]
    api_type: "manual"
    api_version: ""
    auth_type: "none"
    priority: "P2"
    status: "planned"
    rate_limit:
      requests_per_day: 0
      requests_per_minute: 0
      concurrent: 0
    config_fields:
      - name: "account"
        type: "string"
        required: true
        description: "账号"
      - name: "password"
        type: "secret"
        required: true
        description: "密码"
      note: "暂不支持API，需手动发布"
```


### 2.5 企业办公类

```yaml
# 企业办公平台配置
enterprise_platforms:
  # P1 平台
  - id: "feishu_doc"
    name: "飞书文档"
    category: "enterprise"
    content_types: ["document", "wiki"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 200
      concurrent: 10
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "飞书App ID"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "飞书App Secret"
        
  - id: "wecom"
    name: "企业微信"
    category: "enterprise"
    content_types: ["article", "image", "text"]
    api_type: "official"
    api_version: "v3"
    auth_type: "corp_secret"
    priority: "P1"
    status: "planned"
    rate_limit:
      requests_per_day: 100000
      requests_per_minute: 500
      concurrent: 20
    config_fields:
      - name: "corp_id"
        type: "string"
        required: true
        description: "企业微信Corp ID"
      - name: "corp_secret"
        type: "secret"
        required: true
        description: "企业微信Corp Secret"
      - name: "agent_id"
        type: "string"
        required: true
        description: "应用Agent ID"
```


## 三、平台汇总清单

```yaml
# 国内平台汇总
domestic_platforms_summary:
  total_count: 22
  
  by_priority:
    P0: 9
    P1: 9
    P2: 4
    
  by_category:
    portal: 7
    short_video: 5
    social: 3
    tech: 4
    enterprise: 2
    
  by_api_type:
    official: 20
    manual: 2
    
  platforms_list:
    - id: "wechat_mp"
      name: "微信公众号"
      priority: "P0"
      category: "portal"
    - id: "toutiao"
      name: "今日头条"
      priority: "P0"
      category: "portal"
    - id: "baijiahao"
      name: "百家号"
      priority: "P0"
      category: "portal"
    - id: "douyin"
      name: "抖音"
      priority: "P0"
      category: "short_video"
    - id: "kuaishou"
      name: "快手"
      priority: "P0"
      category: "short_video"
    - id: "shipinhao"
      name: "视频号"
      priority: "P0"
      category: "short_video"
    - id: "bilibili"
      name: "B站"
      priority: "P0"
      category: "short_video"
    - id: "xiaohongshu"
      name: "小红书"
      priority: "P0"
      category: "short_video"
    - id: "weibo"
      name: "微博"
      priority: "P0"
      category: "social"
    - id: "zhihu"
      name: "知乎"
      priority: "P0"
      category: "social"
    - id: "sohu"
      name: "搜狐号"
      priority: "P1"
      category: "portal"
    - id: "163"
      name: "网易号"
      priority: "P1"
      category: "portal"
    - id: "tencent_news"
      name: "腾讯新闻"
      priority: "P1"
      category: "portal"
    - id: "juejin"
      name: "掘金"
      priority: "P1"
      category: "tech"
    - id: "csdn"
      name: "CSDN"
      priority: "P1"
      category: "tech"
    - id: "segmentfault"
      name: "思否"
      priority: "P1"
      category: "tech"
    - id: "feishu_doc"
      name: "飞书文档"
      priority: "P1"
      category: "enterprise"
    - id: "wecom"
      name: "企业微信"
      priority: "P1"
      category: "enterprise"
    - id: "sina_kandian"
      name: "新浪看点"
      priority: "P2"
      category: "portal"
    - id: "douban"
      name: "豆瓣"
      priority: "P2"
      category: "social"
    - id: "woshipm"
      name: "人人都是产品经理"
      priority: "P2"
      category: "tech"
```


## 四、数据库表结构

```sql
-- 平台配置表
CREATE TABLE marketing_platforms (
    id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL,
    content_types TEXT[] NOT NULL,
    api_type VARCHAR(20) NOT NULL,
    api_version VARCHAR(10),
    auth_type VARCHAR(20) NOT NULL,
    priority VARCHAR(10) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'planned',
    rate_limit JSONB,
    config_fields JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 平台连接表
CREATE TABLE marketing_platform_connections (
    id UUID PRIMARY KEY,
    platform_id UUID REFERENCES marketing_platforms(id),
    account_name VARCHAR(100) NOT NULL,
    auth_data JSONB NOT NULL,
    enabled BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMP,
    sync_status VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- 平台内容映射表
CREATE TABLE marketing_platform_content_mappings (
    id UUID PRIMARY KEY,
    platform_id UUID REFERENCES marketing_platforms(id),
    content_type VARCHAR(20) NOT NULL,
    mapping_rules JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```


## 五、API接口

```yaml
# 平台管理API
api:
  # 获取平台列表
  - method: "GET"
    endpoint: "/api/v1/marketing/platforms"
    description: "获取所有平台列表"
    query_params:
      category: "string"
      priority: "string"
    response: "List[PlatformConfig]"
    
  # 获取平台详情
  - method: "GET"
    endpoint: "/api/v1/marketing/platforms/{id}"
    description: "获取平台详情"
    response: "PlatformConfig"
    
  # 连接平台账号
  - method: "POST"
    endpoint: "/api/v1/marketing/platforms/{id}/connect"
    description: "连接平台账号"
    request_body:
      account_name: "string"
      auth_data: "object"
    response: "PlatformConnection"
    
  # 断开平台连接
  - method: "DELETE"
    endpoint: "/api/v1/marketing/platforms/{id}/disconnect"
    description: "断开平台连接"
    response: "success"
    
  # 测试连接
  - method: "POST"
    endpoint: "/api/v1/marketing/platforms/{id}/test"
    description: "测试平台连接"
    response: "TestResult"
```


## 六、在Cursor中使用

```bash
# 1. 查看所有平台配置
@docs/DOMESTIC_PLATFORMS_CONFIG_v1.0.md 列出所有国内平台配置

# 2. 添加新平台
@docs/DOMESTIC_PLATFORMS_CONFIG_v1.0.md 按照格式添加一个新平台：微信视频号

# 3. 实现平台连接
@docs/DOMESTIC_PLATFORMS_CONFIG_v1.0.md 实现微信公众号的OAuth连接功能

# 4. 实现内容发布
@docs/DOMESTIC_PLATFORMS_CONFIG_v1.0.md 实现内容发布到抖音的API调用
```


**文档结束**