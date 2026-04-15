# 国外自媒体平台配置 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\OVERSEAS_PLATFORMS_CONFIG_v1.0.md
```


# 国外自媒体平台配置 v1.0

## 一、平台数据模型

```python
# 国外平台配置数据模型
class OverseasPlatformConfig:
    id: str                    # 平台唯一标识
    name: str                  # 平台名称
    category: str              # 类别：social_media/professional/tech/messaging
    content_types: List[str]   # 支持的内容类型
    api_type: str              # API类型：official/third_party
    api_version: str           # API版本
    auth_type: str             # 认证方式：oauth/apikey/bot_token
    priority: str              # 优先级：P1/P2/P3
    status: str                # 状态：active/developing/planned
    rate_limit: RateLimit      # 接口限制
    config_fields: List[ConfigField]  # 配置字段
    webhook_supported: bool    # 是否支持Webhook
    webhook_events: List[str]  # Webhook事件类型

# 接口限制
class RateLimit:
    requests_per_day: int      # 每日请求上限
    requests_per_minute: int   # 每分钟请求上限
    concurrent: int            # 并发数限制
    quota_cost: float          # 配额消耗系数

# 配置字段
class ConfigField:
    name: str                  # 字段名
    type: str                  # 类型：string/secret/oauth_file/redirect_uri
    required: bool             # 是否必填
    description: str           # 说明
    placeholder: str           # 示例值
```


## 二、平台配置清单

### 2.1 社交媒体类（Social Media）

```yaml
# 社交媒体平台配置
social_media_platforms:
  # P1 平台 - Meta生态
  - id: "facebook"
    name: "Facebook"
    category: "social_media"
    content_types: ["post", "image", "video", "live", "story", "reel"]
    api_type: "official"
    api_version: "v18.0"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: true
    webhook_events: ["feed", "comment", "like", "share"]
    rate_limit:
      requests_per_day: 200000
      requests_per_minute: 200
      concurrent: 10
      quota_cost: 1.0
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "Facebook App ID"
        placeholder: "123456789012345"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "Facebook App Secret"
        placeholder: "abc123def456..."
      - name: "page_id"
        type: "string"
        required: true
        description: "Facebook Page ID"
        placeholder: "123456789012345"
      - name: "page_access_token"
        type: "secret"
        required: true
        description: "Page Access Token"
        placeholder: "EAA..."
        
  - id: "instagram"
    name: "Instagram"
    category: "social_media"
    content_types: ["post", "image", "video", "reel", "story", "carousel"]
    api_type: "official"
    api_version: "v18.0"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: true
    webhook_events: ["media", "comment", "mention"]
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 100
      concurrent: 5
      quota_cost: 1.0
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "Instagram App ID"
        placeholder: "123456789012345"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "Instagram App Secret"
        placeholder: "abc123def456..."
      - name: "ig_user_id"
        type: "string"
        required: true
        description: "Instagram User ID"
        placeholder: "123456789012345"
      - name: "access_token"
        type: "secret"
        required: true
        description: "Instagram Access Token"
        placeholder: "IGQVJ..."
        
  # P1 平台 - X (Twitter)
  - id: "twitter"
    name: "X (Twitter)"
    category: "social_media"
    content_types: ["tweet", "image", "video", "poll", "thread"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: true
    webhook_events: ["tweet", "mention", "retweet", "like"]
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 300
      concurrent: 10
      quota_cost: 1.0
    config_fields:
      - name: "api_key"
        type: "string"
        required: true
        description: "Twitter API Key"
        placeholder: "abc123def456"
      - name: "api_secret"
        type: "secret"
        required: true
        description: "Twitter API Secret"
        placeholder: "xyz789..."
      - name: "access_token"
        type: "secret"
        required: true
        description: "Twitter Access Token"
        placeholder: "123456789-ABC..."
      - name: "access_token_secret"
        type: "secret"
        required: true
        description: "Twitter Access Token Secret"
        placeholder: "abc123..."
        
  # P1 平台 - LinkedIn
  - id: "linkedin"
    name: "LinkedIn"
    category: "social_media"
    content_types: ["post", "image", "video", "article", "carousel"]
    api_type: "official"
    api_version: "v2"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: true
    webhook_events: ["share", "comment", "like"]
    rate_limit:
      requests_per_day: 100000
      requests_per_minute: 100
      concurrent: 5
      quota_cost: 1.0
    config_fields:
      - name: "client_id"
        type: "string"
        required: true
        description: "LinkedIn Client ID"
        placeholder: "78abcdefghijk"
      - name: "client_secret"
        type: "secret"
        required: true
        description: "LinkedIn Client Secret"
        placeholder: "ABC123..."
      - name: "access_token"
        type: "secret"
        required: true
        description: "LinkedIn Access Token"
        placeholder: "AQVJ..."
        
  # P1 平台 - TikTok
  - id: "tiktok"
    name: "TikTok"
    category: "social_media"
    content_types: ["video", "image", "story"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: true
    webhook_events: ["video", "like", "comment", "share"]
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 100
      concurrent: 5
      quota_cost: 1.0
    config_fields:
      - name: "client_key"
        type: "string"
        required: true
        description: "TikTok Client Key"
        placeholder: "sb_abc123..."
      - name: "client_secret"
        type: "secret"
        required: true
        description: "TikTok Client Secret"
        placeholder: "abc123..."
      - name: "access_token"
        type: "secret"
        required: true
        description: "TikTok Access Token"
        placeholder: "act.abc123..."
        
  # P1 平台 - YouTube
  - id: "youtube"
    name: "YouTube"
    category: "social_media"
    content_types: ["video", "short", "post", "live", "playlist"]
    api_type: "official"
    api_version: "v3"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: true
    webhook_events: ["video", "comment", "subscription"]
    rate_limit:
      requests_per_day: 100000
      requests_per_minute: 300
      concurrent: 10
      quota_cost: 1.0
    config_fields:
      - name: "api_key"
        type: "string"
        required: true
        description: "YouTube API Key"
        placeholder: "AIzaSy..."
      - name: "client_id"
        type: "string"
        required: true
        description: "YouTube Client ID"
        placeholder: "123456789-abc.apps.googleusercontent.com"
      - name: "client_secret"
        type: "secret"
        required: true
        description: "YouTube Client Secret"
        placeholder: "GOCSPX-..."
      - name: "channel_id"
        type: "string"
        required: true
        description: "YouTube Channel ID"
        placeholder: "UCxxxxxxxxxxxxxxxxxx"

  # P2 平台 - Pinterest
  - id: "pinterest"
    name: "Pinterest"
    category: "social_media"
    content_types: ["pin", "image", "video", "carousel"]
    api_type: "official"
    api_version: "v5"
    auth_type: "oauth"
    priority: "P2"
    status: "planned"
    webhook_supported: false
    webhook_events: []
    rate_limit:
      requests_per_day: 10000
      requests_per_minute: 50
      concurrent: 3
      quota_cost: 1.0
    config_fields:
      - name: "app_id"
        type: "string"
        required: true
        description: "Pinterest App ID"
        placeholder: "1234567890"
      - name: "app_secret"
        type: "secret"
        required: true
        description: "Pinterest App Secret"
        placeholder: "abc123..."
      - name: "access_token"
        type: "secret"
        required: true
        description: "Pinterest Access Token"
        placeholder: "pina.abc123..."
        
  # P2 平台 - Reddit
  - id: "reddit"
    name: "Reddit"
    category: "social_media"
    content_types: ["post", "image", "video", "poll", "comment"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P2"
    status: "planned"
    webhook_supported: false
    webhook_events: []
    rate_limit:
      requests_per_day: 10000
      requests_per_minute: 60
      concurrent: 3
      quota_cost: 1.0
    config_fields:
      - name: "client_id"
        type: "string"
        required: true
        description: "Reddit Client ID"
        placeholder: "abc123..."
      - name: "client_secret"
        type: "secret"
        required: true
        description: "Reddit Client Secret"
        placeholder: "xyz789..."
      - name: "username"
        type: "string"
        required: true
        description: "Reddit Username"
        placeholder: "your_username"
      - name: "password"
        type: "secret"
        required: true
        description: "Reddit Password"
        placeholder: "********"
      - name: "user_agent"
        type: "string"
        required: true
        description: "Reddit User Agent"
        placeholder: "JYIS/1.0 by your_username"
```


### 2.2 专业社区类（Professional Community）

```yaml
# 专业社区平台配置
professional_platforms:
  # P1 平台 - Medium
  - id: "medium"
    name: "Medium"
    category: "professional"
    content_types: ["article", "series", "image"]
    api_type: "official"
    api_version: "v1"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: false
    webhook_events: []
    rate_limit:
      requests_per_day: 5000
      requests_per_minute: 30
      concurrent: 2
      quota_cost: 1.0
    config_fields:
      - name: "integration_token"
        type: "secret"
        required: true
        description: "Medium Integration Token"
        placeholder: "abc123def456"
      - name: "author_id"
        type: "string"
        required: true
        description: "Medium Author ID"
        placeholder: "1234567890abcdef"
        
  # P1 平台 - GitHub
  - id: "github"
    name: "GitHub"
    category: "professional"
    content_types: ["readme", "discussion", "issue", "release", "gist"]
    api_type: "official"
    api_version: "2022-11-28"
    auth_type: "oauth"
    priority: "P1"
    status: "planned"
    webhook_supported: true
    webhook_events: ["push", "release", "discussion"]
    rate_limit:
      requests_per_day: 5000
      requests_per_minute: 100
      concurrent: 5
      quota_cost: 1.0
    config_fields:
      - name: "personal_access_token"
        type: "secret"
        required: true
        description: "GitHub Personal Access Token"
        placeholder: "github_pat_abc123..."
      - name: "repo_name"
        type: "string"
        required: false
        description: "Repository Name (optional)"
        placeholder: "username/repo"
        
  # P2 平台 - Dev.to
  - id: "devto"
    name: "Dev.to"
    category: "professional"
    content_types: ["article", "series", "comment"]
    api_type: "official"
    api_version: "v1"
    auth_type: "apikey"
    priority: "P2"
    status: "planned"
    webhook_supported: false
    webhook_events: []
    rate_limit:
      requests_per_day: 1000
      requests_per_minute: 30
      concurrent: 2
      quota_cost: 1.0
    config_fields:
      - name: "api_key"
        type: "secret"
        required: true
        description: "Dev.to API Key"
        placeholder: "abc123def456"
      - name: "user_id"
        type: "string"
        required: true
        description: "Dev.to User ID"
        placeholder: "123456"
        
  # P2 平台 - Stack Overflow
  - id: "stackoverflow"
    name: "Stack Overflow"
    category: "professional"
    content_types: ["question", "answer", "comment"]
    api_type: "official"
    api_version: "2.3"
    auth_type: "oauth"
    priority: "P2"
    status: "planned"
    webhook_supported: false
    webhook_events: []
    rate_limit:
      requests_per_day: 300
      requests_per_minute: 10
      concurrent: 1
      quota_cost: 1.0
    config_fields:
      - name: "client_id"
        type: "string"
        required: true
        description: "Stack Overflow Client ID"
        placeholder: "12345"
      - name: "client_secret"
        type: "secret"
        required: true
        description: "Stack Overflow Client Secret"
        placeholder: "abc123..."
      - name: "key"
        type: "string"
        required: true
        description: "Stack Overflow API Key"
        placeholder: "abc123..."
      - name: "access_token"
        type: "secret"
        required: true
        description: "Stack Overflow Access Token"
        placeholder: "abc123..."
```


### 2.3 即时通讯类（Messaging）

```yaml
# 即时通讯平台配置
messaging_platforms:
  # P2 平台 - Telegram
  - id: "telegram"
    name: "Telegram"
    category: "messaging"
    content_types: ["message", "photo", "video", "document", "poll", "channel_post"]
    api_type: "official"
    api_version: "v6"
    auth_type: "bot_token"
    priority: "P2"
    status: "planned"
    webhook_supported: true
    webhook_events: ["message", "callback_query", "channel_post"]
    rate_limit:
      requests_per_day: 100000
      requests_per_minute: 30
      concurrent: 10
      quota_cost: 0.1
    config_fields:
      - name: "bot_token"
        type: "secret"
        required: true
        description: "Telegram Bot Token"
        placeholder: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
      - name: "chat_id"
        type: "string"
        required: true
        description: "Telegram Chat ID (channel/group)"
        placeholder: "-1001234567890"
        
  # P2 平台 - Discord
  - id: "discord"
    name: "Discord"
    category: "messaging"
    content_types: ["message", "embed", "image", "video", "file"]
    api_type: "official"
    api_version: "v10"
    auth_type: "bot_token"
    priority: "P2"
    status: "planned"
    webhook_supported: true
    webhook_events: ["message", "reaction", "member"]
    rate_limit:
      requests_per_day: 50000
      requests_per_minute: 50
      concurrent: 5
      quota_cost: 1.0
    config_fields:
      - name: "bot_token"
        type: "secret"
        required: true
        description: "Discord Bot Token"
        placeholder: "MTIzNDU2Nzg5MDEyMzQ1Njc4OQ.GhIjKl-MnOpQrStUvWxYz"
      - name: "channel_id"
        type: "string"
        required: true
        description: "Discord Channel ID"
        placeholder: "1234567890123456789"
        
  # P2 平台 - WhatsApp
  - id: "whatsapp"
    name: "WhatsApp"
    category: "messaging"
    content_types: ["text", "image", "video", "audio", "document", "template"]
    api_type: "official"
    api_version: "v18.0"
    auth_type: "oauth"
    priority: "P2"
    status: "planned"
    webhook_supported: true
    webhook_events: ["message", "status", "template"]
    rate_limit:
      requests_per_day: 250000
      requests_per_minute: 80
      concurrent: 10
      quota_cost: 1.0
    config_fields:
      - name: "phone_number_id"
        type: "string"
        required: true
        description: "WhatsApp Business Phone Number ID"
        placeholder: "123456789012345"
      - name: "access_token"
        type: "secret"
        required: true
        description: "WhatsApp Access Token"
        placeholder: "EAA..."
      - name: "business_account_id"
        type: "string"
        required: true
        description: "WhatsApp Business Account ID"
        placeholder: "123456789012345"
```


## 三、平台汇总清单

```yaml
# 国外平台汇总
overseas_platforms_summary:
  total_count: 14
  
  by_priority:
    P1: 8
    P2: 6
    
  by_category:
    social_media: 8
    professional: 4
    messaging: 3
    
  by_api_type:
    official: 14
    third_party: 0
    
  platforms_list:
    # P1 平台
    - id: "facebook"
      name: "Facebook"
      priority: "P1"
      category: "social_media"
    - id: "instagram"
      name: "Instagram"
      priority: "P1"
      category: "social_media"
    - id: "twitter"
      name: "X (Twitter)"
      priority: "P1"
      category: "social_media"
    - id: "linkedin"
      name: "LinkedIn"
      priority: "P1"
      category: "social_media"
    - id: "tiktok"
      name: "TikTok"
      priority: "P1"
      category: "social_media"
    - id: "youtube"
      name: "YouTube"
      priority: "P1"
      category: "social_media"
    - id: "medium"
      name: "Medium"
      priority: "P1"
      category: "professional"
    - id: "github"
      name: "GitHub"
      priority: "P1"
      category: "professional"
      
    # P2 平台
    - id: "pinterest"
      name: "Pinterest"
      priority: "P2"
      category: "social_media"
    - id: "reddit"
      name: "Reddit"
      priority: "P2"
      category: "social_media"
    - id: "devto"
      name: "Dev.to"
      priority: "P2"
      category: "professional"
    - id: "stackoverflow"
      name: "Stack Overflow"
      priority: "P2"
      category: "professional"
    - id: "telegram"
      name: "Telegram"
      priority: "P2"
      category: "messaging"
    - id: "discord"
      name: "Discord"
      priority: "P2"
      category: "messaging"
    - id: "whatsapp"
      name: "WhatsApp"
      priority: "P2"
      category: "messaging"
```


## 四、数据库表结构

```sql
-- 国外平台配置表（复用国内平台表，增加字段）
ALTER TABLE marketing_platforms ADD COLUMN webhook_supported BOOLEAN DEFAULT false;
ALTER TABLE marketing_platforms ADD COLUMN webhook_events TEXT[];
ALTER TABLE marketing_platforms ADD COLUMN quota_cost FLOAT DEFAULT 1.0;

-- OAuth回调配置表
CREATE TABLE marketing_oauth_configs (
    id UUID PRIMARY KEY,
    platform_id UUID REFERENCES marketing_platforms(id),
    redirect_uri VARCHAR(500) NOT NULL,
    state VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP
);

-- Webhook订阅表
CREATE TABLE marketing_webhook_subscriptions (
    id UUID PRIMARY KEY,
    platform_id UUID REFERENCES marketing_platforms(id),
    connection_id UUID REFERENCES marketing_platform_connections(id),
    webhook_url VARCHAR(500) NOT NULL,
    events TEXT[] NOT NULL,
    secret VARCHAR(200),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Webhook事件日志表
CREATE TABLE marketing_webhook_events (
    id UUID PRIMARY KEY,
    subscription_id UUID REFERENCES marketing_webhook_subscriptions(id),
    event_type VARCHAR(50) NOT NULL,
    payload JSONB,
    received_at TIMESTAMP NOT NULL DEFAULT NOW(),
    processed BOOLEAN DEFAULT false,
    processed_at TIMESTAMP
);
```


## 五、API接口

```yaml
# 国外平台API
api:
  # OAuth授权
  - method: "GET"
    endpoint: "/api/v1/marketing/oauth/{platform_id}/auth-url"
    description: "获取OAuth授权URL"
    response:
      auth_url: "string"
      state: "string"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/oauth/callback"
    description: "OAuth回调处理"
    request_body:
      platform_id: "string"
      code: "string"
      state: "string"
    response: "ConnectionResult"
    
  # Webhook管理
  - method: "POST"
    endpoint: "/api/v1/marketing/webhook/subscribe"
    description: "订阅Webhook"
    request_body:
      platform_id: "string"
      connection_id: "string"
      events: "List[str]"
    response: "WebhookSubscription"
    
  - method: "DELETE"
    endpoint: "/api/v1/marketing/webhook/subscribe/{id}"
    description: "取消订阅Webhook"
    response: "success"
    
  # 平台特定操作
  - method: "POST"
    endpoint: "/api/v1/marketing/platforms/{platform_id}/post"
    description: "发布内容到平台"
    request_body:
      connection_id: "string"
      content_type: "string"
      content: "object"
    response: "PublishResult"
```


## 六、OAuth流程

```yaml
# OAuth认证流程
oauth_flow:
  step_1: "获取授权URL"
  step_2: "用户授权"
  step_3: "回调获取code"
  step_4: "换取access_token"
  step_5: "刷新token（自动）"
  
# 支持的OAuth类型
oauth_types:
  - type: "authorization_code"
    platforms: ["facebook", "instagram", "linkedin", "tiktok", "youtube", "reddit"]
  - type: "implicit"
    platforms: []
  - type: "client_credentials"
    platforms: ["twitter"]
  - type: "bot_token"
    platforms: ["telegram", "discord"]
```


## 七、在Cursor中使用

```bash
# 1. 查看所有国外平台配置
@docs/OVERSEAS_PLATFORMS_CONFIG_v1.0.md 列出所有国外平台配置

# 2. 实现Facebook OAuth
@docs/OVERSEAS_PLATFORMS_CONFIG_v1.0.md 实现Facebook平台的OAuth认证流程

# 3. 实现Twitter发布
@docs/OVERSEAS_PLATFORMS_CONFIG_v1.0.md 实现发布内容到Twitter的API调用

# 4. 实现GitHub Webhook
@docs/OVERSEAS_PLATFORMS_CONFIG_v1.0.md 实现GitHub Webhook订阅，监听代码推送事件
```


**文档结束**