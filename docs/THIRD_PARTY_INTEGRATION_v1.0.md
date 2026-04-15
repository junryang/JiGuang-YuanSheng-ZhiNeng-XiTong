# 第三方工具集成方案 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\THIRD_PARTY_INTEGRATION_v1.0.md
```


# 第三方工具集成方案 v1.0

## 一、能力总览

```yaml
module: "第三方工具集成"
description: "集成各类第三方工具，包括多平台分发、内容生成、视频生成、营销Agent、媒体发稿、数据分析"
priority: "P0"
domain: "营销中心"

# 关联的通用能力
related_abilities:
  - "EX-03: API调用"
  - "EX-04: 数据库操作"
  - "EX-05: 文件操作"
  - "EX-08: 消息发送"
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"
  - "EX-12: 批量执行"
  - "EM-01: 多模型路由"
  - "EM-02: 模型负载均衡"
  - "EM-03: 模型降级"
  - "EM-04: 模型缓存"
  - "EM-06: 并发配额感知"
  - "EM-07: 并发队列管理"
  - "EM-08: 智能请求调度"
  - "EM-09: 动态并发调整"
  - "EM-10: 多模型并发分担"
  - "SC-04: 权限检查"
  - "SC-06: 速率限制"
  - "WEB-04: API调用与集成"

tools:
  total_count: 6
  categories:
    - "多平台分发"
    - "内容生成"
    - "视频生成"
    - "营销Agent"
    - "媒体发稿"
    - "数据分析"
```


## 二、第三方工具配置

### 2.1 多平台分发 - 聚媒通

```yaml
# 聚媒通配置
tool_id: "jumeitong"
name: "聚媒通"
category: "distribution"
description: "国内60+平台+海外平台一键分发"
priority: "P0"
integration_type: "api"
api_version: "v2"

# API配置
api_config:
  base_url: "https://api.jumeitong.com/v2"
  auth_type: "apikey"
  rate_limit: "100/分钟"
  timeout: 30
  
# 功能特性
features:
  - "国内60+平台一键分发"
  - "海外平台支持"
  - "定时发布"
  - "数据统计"
  - "账号管理"
  
# 支持的平台
supported_platforms:
  domestic:
    - "wechat"      # 微信公众号
    - "douyin"      # 抖音
    - "kuaishou"    # 快手
    - "bilibili"    # B站
    - "zhihu"       # 知乎
    - "weibo"       # 微博
    - "xiaohongshu" # 小红书
    - "toutiao"     # 今日头条
    - "baijiahao"   # 百家号
    - "sohu"        # 搜狐号
    - "netease"     # 网易号
    - "yidian"      # 一点号
  international:
    - "facebook"
    - "twitter"
    - "instagram"
    - "linkedin"
    - "youtube"
    - "tiktok"

# API端点
api_endpoints:
  - method: "POST"
    path: "/publish"
    description: "发布内容"
    
  - method: "POST"
    path: "/publish/batch"
    description: "批量发布"
    
  - method: "GET"
    path: "/publish/status/{task_id}"
    description: "查询发布状态"
    
  - method: "GET"
    path: "/accounts"
    description: "获取账号列表"
    
  - method: "POST"
    path: "/accounts/add"
    description: "添加账号"
    
  - method: "GET"
    path: "/statistics"
    description: "获取统计数据"

# 实现示例
class JumeitongAdapter:
    """聚媒通适配器 - 对齐EX-03 API调用、EM-06并发配额感知"""
    
    def __init__(self):
        self.base_url = "https://api.jumeitong.com/v2"
        self.api_key = os.getenv("JUMEITONG_API_KEY")
        self.rate_limiter = RateLimiter(max_per_minute=100)  # 对齐SC-06
        self.quota_manager = QuotaManager()  # 对齐EM-06
    
    async def publish(self, content: str, platforms: List[str], 
                      media_files: List[str] = None,
                      schedule_time: datetime = None) -> dict:
        """发布内容 - 对齐EX-03"""
        # 检查配额（对齐EM-06）
        if not await self.quota_manager.check_quota("jumeitong"):
            raise QuotaExceededError("API quota exceeded")
        
        # 限流控制（对齐SC-06）
        await self.rate_limiter.acquire()
        
        # 构建请求
        data = {
            "content": content,
            "platforms": platforms,
            "media_files": media_files or []
        }
        if schedule_time:
            data["schedule_time"] = schedule_time.isoformat()
        
        # 调用API（对齐EX-03）
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/publish",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            ) as resp:
                result = await resp.json()
                
                # 记录配额使用
                await self.quota_manager.record_usage("jumeitong", 1)
                
                return result
    
    async def batch_publish(self, contents: List[dict]) -> List[dict]:
        """批量发布 - 对齐EX-12批量执行"""
        tasks = []
        for content in contents:
            task = self.publish(
                content=content["content"],
                platforms=content["platforms"],
                media_files=content.get("media_files"),
                schedule_time=content.get("schedule_time")
            )
            tasks.append(task)
        
        # 并行执行（对齐EX-09）
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
```

### 2.2 内容生成 - Jasper / Copy.ai

```yaml
# Jasper配置
tool_id: "jasper"
name: "Jasper"
category: "content_generation"
description: "高质量品牌内容生成"
priority: "P1"
integration_type: "api"

# API配置
api_config:
  base_url: "https://api.jasper.ai/v1"
  auth_type: "apikey"
  rate_limit: "50/分钟"
  timeout: 60

# 功能特性
features:
  - "50+文案模板"
  - "品牌语调学习"
  - "多语言支持"
  - "SEO优化"
  - "长文生成"

# API端点
api_endpoints:
  - method: "POST"
    path: "/generate"
    description: "生成内容"
    
  - method: "POST"
    path: "/templates"
    description: "获取模板列表"
    
  - method: "POST"
    path: "/brand/voice"
    description: "品牌语调配置"

# Copy.ai配置
tool_id: "copyai"
name: "Copy.ai"
category: "content_generation"
description: "100+创作工具"
priority: "P1"
integration_type: "api"

api_config:
  base_url: "https://api.copy.ai/v1"
  auth_type: "apikey"
  rate_limit: "100/分钟"
  timeout: 30

features:
  - "100+创作工具"
  - "团队协作"
  - "工作流自动化"
  - "多语言支持"

# 统一适配器
class ContentGenerationAdapter:
    """内容生成适配器 - 对齐EM-01多模型路由、EM-02负载均衡"""
    
    def __init__(self):
        self.tools = {
            "jasper": JasperAdapter(),
            "copyai": CopyAIAdapter()
        }
        self.model_router = ModelRouter()  # 对齐EM-01
        self.load_balancer = LoadBalancer()  # 对齐EM-02
    
    async def generate(self, prompt: str, tool: str = None,
                       template: str = None, params: dict = None) -> str:
        """生成内容 - 对齐EM-01"""
        # 工具选择（对齐EM-01）
        if not tool:
            tool = await self.model_router.route(
                task_type="content_generation",
                prompt_length=len(prompt),
                quality_required=params.get("quality", "high") if params else "high"
            )
        
        adapter = self.tools.get(tool)
        if not adapter:
            raise ValueError(f"Unknown tool: {tool}")
        
        # 负载均衡（对齐EM-02）
        await self.load_balancer.acquire(tool)
        
        try:
            result = await adapter.generate(prompt, template, params)
            return result
        finally:
            await self.load_balancer.release(tool)
```

### 2.3 视频生成 - 网易千梦引擎

```yaml
# 网易千梦引擎配置
tool_id: "qianmeng"
name: "网易千梦引擎"
category: "video_generation"
description: "AI视频全自动化生成"
priority: "P1"
integration_type: "api"

# API配置
api_config:
  base_url: "https://qianmeng.163.com/api"
  auth_type: "apikey"
  rate_limit: "10/分钟"
  timeout: 300

# 功能特性
features:
  - "文本生成视频"
  - "数字人播报"
  - "模板视频"
  - "视频编辑"
  - "批量生成"

# API端点
api_endpoints:
  - method: "POST"
    path: "/video/generate"
    description: "生成视频"
    
  - method: "GET"
    path: "/video/task/{task_id}"
    description: "查询任务状态"
    
  - method: "POST"
    path: "/digital-human"
    description: "数字人生成"
    
  - method: "GET"
    path: "/templates"
    description: "获取模板列表"

# 实现示例
class QianmengAdapter:
    """网易千梦引擎适配器 - 对齐EX-10异步执行、EM-06并发配额感知"""
    
    def __init__(self):
        self.base_url = "https://qianmeng.163.com/api"
        self.api_key = os.getenv("QIANMENG_API_KEY")
        self.quota_manager = QuotaManager()  # 对齐EM-06
        self.queue_manager = QueueManager()  # 对齐EM-07
    
    async def generate_video(self, script: str, template_id: str = None,
                             duration: int = 60, digital_human: bool = False) -> str:
        """生成视频 - 对齐EX-10异步执行"""
        # 检查配额（对齐EM-06）
        if not await self.quota_manager.check_quota("qianmeng"):
            # 加入队列（对齐EM-07）
            task_id = await self.queue_manager.enqueue("qianmeng", {
                "script": script,
                "template_id": template_id,
                "duration": duration,
                "digital_human": digital_human
            })
            return {"task_id": task_id, "status": "queued"}
        
        # 构建请求
        data = {
            "script": script,
            "duration": duration,
            "digital_human": digital_human
        }
        if template_id:
            data["template_id"] = template_id
        
        # 调用API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/video/generate",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            ) as resp:
                result = await resp.json()
                
                # 记录配额使用
                await self.quota_manager.record_usage("qianmeng", 1)
                
                return result
    
    async def get_task_status(self, task_id: str) -> dict:
        """查询任务状态"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/video/task/{task_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as resp:
                return await resp.json()
```

### 2.4 营销Agent - Simplified / Agent Cloud

```yaml
# Simplified配置
tool_id: "simplified"
name: "Simplified"
category: "marketing_agent"
description: "多Agent营销编排"
priority: "P2"
integration_type: "api"

api_config:
  base_url: "https://api.simplified.com/v1"
  auth_type: "apikey"
  rate_limit: "100/分钟"
  timeout: 30

features:
  - "AI设计"
  - "视频编辑"
  - "社交媒体管理"
  - "内容日历"
  - "团队协作"

# Agent Cloud配置
tool_id: "agentcloud"
name: "Agent Cloud"
category: "marketing_agent"
description: "多Agent营销编排"
priority: "P2"
integration_type: "api"

api_config:
  base_url: "https://api.agentcloud.com/v1"
  auth_type: "apikey"
  rate_limit: "50/分钟"
  timeout: 30

features:
  - "多Agent编排"
  - "工作流自动化"
  - "任务调度"
  - "监控告警"

# 统一适配器
class MarketingAgentAdapter:
    """营销Agent适配器 - 对齐EM-01多模型路由、EM-03模型降级"""
    
    def __init__(self):
        self.tools = {
            "simplified": SimplifiedAdapter(),
            "agentcloud": AgentCloudAdapter()
        }
        self.model_router = ModelRouter()  # 对齐EM-01
        self.fallback_manager = FallbackManager()  # 对齐EM-03
    
    async def execute_workflow(self, workflow_config: dict) -> dict:
        """执行营销工作流 - 对齐EM-01、EM-03"""
        # 选择工具（对齐EM-01）
        tool = await self.model_router.route(
            task_type="marketing_workflow",
            complexity=workflow_config.get("complexity", "medium")
        )
        
        try:
            adapter = self.tools.get(tool)
            result = await adapter.execute(workflow_config)
            return result
        except Exception as e:
            # 降级处理（对齐EM-03）
            fallback_result = await self.fallback_manager.fallback(
                primary_tool=tool,
                workflow_config=workflow_config,
                error=e
            )
            return fallback_result
```

### 2.5 媒体发稿 - 传声港

```yaml
# 传声港配置
tool_id: "chuanshenggang"
name: "传声港"
category: "media_distribution"
description: "央级/门户媒体发稿"
priority: "P1"
integration_type: "platform"

# API配置
api_config:
  base_url: "https://api.chuanshenggang.com/v1"
  auth_type: "apikey"
  rate_limit: "50/分钟"
  timeout: 60

# 功能特性
features:
  - "20000+媒体资源"
  - "智能选媒推荐"
  - "一键批量发布"
  - "收录效果追踪"
  - "传播数据分析"

# 媒体分类
media_categories:
  central:
    - "人民网"
    - "新华网"
    - "央视网"
    - "中国日报网"
    - "中国经济网"
    - "科技日报"
  gateway:
    - "新浪网"
    - "网易"
    - "腾讯网"
    - "搜狐"
    - "凤凰网"
  vertical:
    - "36氪"
    - "虎嗅"
    - "CSDN"
    - "掘金"
  international:
    - "路透社"
    - "雅虎财经"
    - "美联社"
    - "彭博社"
    - "TechCrunch"

# API端点
api_endpoints:
  - method: "GET"
    path: "/media/list"
    description: "获取媒体列表"
    
  - method: "POST"
    path: "/articles"
    description: "创建稿件"
    
  - method: "POST"
    path: "/orders"
    description: "创建发稿订单"
    
  - method: "GET"
    path: "/orders/{id}/status"
    description: "查询订单状态"
    
  - method: "GET"
    path: "/orders/{id}/report"
    description: "获取发布报告"

# 实现示例
class ChuanshenggangAdapter:
    """传声港适配器 - 对齐EX-03 API调用、EM-06并发配额感知"""
    
    def __init__(self):
        self.base_url = "https://api.chuanshenggang.com/v1"
        self.api_key = os.getenv("CHUANSHENGANG_API_KEY")
        self.rate_limiter = RateLimiter(max_per_minute=50)  # 对齐SC-06
    
    async def get_media_list(self, category: str = None, 
                              keyword: str = None) -> List[dict]:
        """获取媒体列表"""
        await self.rate_limiter.acquire()
        
        params = {}
        if category:
            params["category"] = category
        if keyword:
            params["keyword"] = keyword
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/media/list",
                headers={"Authorization": f"Bearer {self.api_key}"},
                params=params
            ) as resp:
                return await resp.json()
    
    async def create_order(self, title: str, content: str,
                           media_ids: List[str],
                           schedule_time: datetime = None) -> dict:
        """创建发稿订单"""
        await self.rate_limiter.acquire()
        
        data = {
            "title": title,
            "content": content,
            "media_ids": media_ids
        }
        if schedule_time:
            data["schedule_time"] = schedule_time.isoformat()
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/orders",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json=data
            ) as resp:
                return await resp.json()
    
    async def get_order_status(self, order_id: str) -> dict:
        """查询订单状态"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/orders/{order_id}/status",
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as resp:
                return await resp.json()
```

### 2.6 数据分析 - 新榜 / 飞瓜

```yaml
# 新榜配置
tool_id: "xinbang"
name: "新榜"
category: "analytics"
description: "社交媒体数据分析"
priority: "P1"
integration_type: "api"

api_config:
  base_url: "https://api.xinbang.com/v1"
  auth_type: "apikey"
  rate_limit: "100/分钟"
  timeout: 30

features:
  - "公众号数据"
  - "视频号数据"
  - "热点追踪"
  - "榜单查询"
  - "竞品分析"

# API端点
api_endpoints:
  - method: "GET"
    path: "/account/rank"
    description: "获取账号排名"
    
  - method: "GET"
    path: "/article/hot"
    description: "获取热门文章"
    
  - method: "GET"
    path: "/account/analysis"
    description: "账号分析"
    
  - method: "GET"
    path: "/trends"
    description: "获取趋势"

# 飞瓜数据配置
tool_id: "feigua"
name: "飞瓜数据"
category: "analytics"
description: "短视频数据分析"
priority: "P1"
integration_type: "api"

api_config:
  base_url: "https://api.feigua.cn/v1"
  auth_type: "apikey"
  rate_limit: "50/分钟"
  timeout: 30

features:
  - "抖音数据"
  - "快手数据"
  - "直播分析"
  - "带货分析"
  - "粉丝画像"

# 统一适配器
class AnalyticsAdapter:
    """数据分析适配器 - 对齐EM-01多模型路由、EM-04模型缓存"""
    
    def __init__(self):
        self.tools = {
            "xinbang": XinbangAdapter(),
            "feigua": FeiguaAdapter()
        }
        self.model_router = ModelRouter()  # 对齐EM-01
        self.cache_manager = CacheManager()  # 对齐EM-04
    
    async def get_analytics(self, platform: str, metric: str,
                            date_range: dict, use_cache: bool = True) -> dict:
        """获取分析数据 - 对齐EM-01、EM-04"""
        # 检查缓存（对齐EM-04）
        cache_key = f"analytics:{platform}:{metric}:{hash(str(date_range))}"
        if use_cache:
            cached = await self.cache_manager.get(cache_key)
            if cached:
                return cached
        
        # 选择工具（对齐EM-01）
        tool = await self.model_router.route(
            task_type="analytics",
            platform=platform,
            metric=metric
        )
        
        adapter = self.tools.get(tool)
        if not adapter:
            raise ValueError(f"Unknown tool for platform {platform}")
        
        # 获取数据
        result = await adapter.get_analytics(platform, metric, date_range)
        
        # 缓存结果（对齐EM-04）
        await self.cache_manager.set(cache_key, result, ttl=3600)  # 1小时
        
        return result
```


## 三、统一适配器管理器

```yaml
# 工具适配器管理器
adapter_manager:
  description: "统一管理所有第三方工具适配器"
  
  # 适配器注册
  registration:
    - endpoint: "/api/v1/marketing/adapters/register"
      method: "POST"
      description: "注册新适配器"
      
  # 适配器列表
  list:
    - endpoint: "/api/v1/marketing/adapters"
      method: "GET"
      description: "获取适配器列表"
      
  # 适配器健康检查
  health:
    - endpoint: "/api/v1/marketing/adapters/{id}/health"
      method: "GET"
      description: "检查适配器健康状态"

# 实现示例
class ToolAdapterManager:
    """工具适配器管理器 - 对齐EM-06并发配额感知、EM-07队列管理"""
    
    def __init__(self):
        self.adapters = {}
        self.quota_manager = QuotaManager()  # 对齐EM-06
        self.queue_manager = QueueManager()  # 对齐EM-07
        self.health_checker = HealthChecker()
    
    def register_adapter(self, tool_id: str, adapter: BaseAdapter):
        """注册适配器"""
        self.adapters[tool_id] = adapter
    
    async def call(self, tool_id: str, method: str, **kwargs) -> dict:
        """统一调用接口 - 对齐EM-06、EM-07、EM-08"""
        adapter = self.adapters.get(tool_id)
        if not adapter:
            raise ValueError(f"Unknown tool: {tool_id}")
        
        # 健康检查
        if not await self.health_checker.is_healthy(tool_id):
            # 降级处理
            return await self._fallback_call(tool_id, method, **kwargs)
        
        # 检查配额（对齐EM-06）
        if not await self.quota_manager.check_quota(tool_id):
            # 加入队列（对齐EM-07）
            task_id = await self.queue_manager.enqueue(tool_id, {
                "method": method,
                "kwargs": kwargs
            })
            return {"status": "queued", "task_id": task_id}
        
        try:
            # 执行调用
            result = await getattr(adapter, method)(**kwargs)
            
            # 记录配额使用
            await self.quota_manager.record_usage(tool_id, 1)
            
            return result
        except Exception as e:
            # 错误处理
            return await self._handle_error(tool_id, method, e, **kwargs)
    
    async def get_health_status(self) -> dict:
        """获取所有适配器健康状态"""
        status = {}
        for tool_id, adapter in self.adapters.items():
            status[tool_id] = await self.health_checker.check(adapter)
        return status
```


## 四、第三方工具集成架构图

```yaml
architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                        第三方工具集成架构                                   │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         统一调用层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 配额管理    │  │ 队列管理    │  │ 健康检查    │                  │   │
  │  │  │ (EM-06)     │  │ (EM-07)     │  │ (EM-03)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         适配器层                                     │   │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
  │  │  │ 聚媒通    │  │ Jasper    │  │ 千梦引擎  │  │ 传声港    │        │   │
  │  │  │ 适配器    │  │ 适配器    │  │ 适配器    │  │ 适配器    │        │   │
  │  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐                        │   │
  │  │  │ Simplified│  │ AgentCloud│  │ 新榜/飞瓜 │                        │   │
  │  │  │ 适配器    │  │ 适配器    │  │ 适配器    │                        │   │
  │  │  └───────────┘  └───────────┘  └───────────┘                        │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         工具层                                       │   │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
  │  │  │ 聚媒通    │  │ Jasper    │  │ 千梦引擎  │  │ 传声港    │        │   │
  │  │  │ API       │  │ API       │  │ API       │  │ API       │        │   │
  │  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐                        │   │
  │  │  │ Simplified│  │ AgentCloud│  │ 新榜/飞瓜 │                        │   │
  │  │  │ API       │  │ API       │  │ API       │                        │   │
  │  │  └───────────┘  └───────────┘  └───────────┘                        │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```


## 五、通用能力映射表

```yaml
# 第三方工具集成与通用能力映射
general_ability_mapping:
  EX-03_API调用:
    mapped_tools: ["jumeitong", "jasper", "copyai", "qianmeng", "simplified", "agentcloud", "chuanshenggang", "xinbang", "feigua"]
    description: "所有工具都通过API调用集成"
    
  EX-09_并行执行:
    mapped_tools: ["jumeitong"]
    description: "批量发布时并行执行"
    
  EX-10_异步执行:
    mapped_tools: ["qianmeng"]
    description: "视频生成异步处理"
    
  EX-12_批量执行:
    mapped_tools: ["jumeitong"]
    description: "批量发布内容"
    
  EM-01_多模型路由:
    mapped_tools: ["jasper", "copyai", "simplified", "agentcloud", "xinbang", "feigua"]
    description: "根据任务选择最佳工具"
    
  EM-02_模型负载均衡:
    mapped_tools: ["jasper", "copyai"]
    description: "内容生成负载均衡"
    
  EM-03_模型降级:
    mapped_tools: ["simplified", "agentcloud"]
    description: "主工具故障时降级"
    
  EM-04_模型缓存:
    mapped_tools: ["xinbang", "feigua"]
    description: "分析数据缓存"
    
  EM-06_并发配额感知:
    mapped_tools: ["jumeitong", "qianmeng", "chuanshenggang", "jasper", "copyai"]
    description: "感知API配额"
    
  EM-07_并发队列管理:
    mapped_tools: ["jumeitong", "qianmeng", "chuanshenggang"]
    description: "超配额时排队"
    
  EM-08_智能请求调度:
    mapped_tools: ["jasper", "copyai", "simplified", "agentcloud"]
    description: "智能调度请求"
    
  SC-06_速率限制:
    mapped_tools: ["jumeitong", "jasper", "copyai", "qianmeng", "chuanshenggang", "xinbang", "feigua"]
    description: "所有工具都需要限流"
    
  WEB-04_API调用与集成:
    mapped_tools: ["jumeitong", "jasper", "copyai", "qianmeng", "simplified", "agentcloud", "chuanshenggang", "xinbang", "feigua"]
    description: "所有工具都是API集成"
```


## 六、数据库表结构

```sql
-- 第三方工具配置表
CREATE TABLE third_party_tools (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    api_endpoint VARCHAR(500) NOT NULL,
    auth_type VARCHAR(20) NOT NULL,
    rate_limit INTEGER DEFAULT 100,
    timeout INTEGER DEFAULT 30,
    enabled BOOLEAN DEFAULT TRUE,
    priority INTEGER DEFAULT 0,
    config JSONB,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 工具调用记录表
CREATE TABLE tool_call_logs (
    id UUID PRIMARY KEY,
    tool_id UUID REFERENCES third_party_tools(id),
    method VARCHAR(100) NOT NULL,
    request JSONB,
    response JSONB,
    status VARCHAR(20),
    duration_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL
);

-- 工具配额表
CREATE TABLE tool_quotas (
    id UUID PRIMARY KEY,
    tool_id UUID REFERENCES third_party_tools(id),
    quota_type VARCHAR(50) NOT NULL,  -- daily, monthly
    limit_value INTEGER NOT NULL,
    used_value INTEGER DEFAULT 0,
    reset_time TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 工具健康状态表
CREATE TABLE tool_health_status (
    id UUID PRIMARY KEY,
    tool_id UUID REFERENCES third_party_tools(id),
    status VARCHAR(20) DEFAULT 'healthy',
    last_check TIMESTAMP,
    error_count INTEGER DEFAULT 0,
    avg_latency_ms INTEGER,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_third_party_tools_category ON third_party_tools(category);
CREATE INDEX idx_third_party_tools_enabled ON third_party_tools(enabled);
CREATE INDEX idx_tool_call_logs_tool ON tool_call_logs(tool_id);
CREATE INDEX idx_tool_call_logs_created ON tool_call_logs(created_at);
CREATE INDEX idx_tool_quotas_tool ON tool_quotas(tool_id);
CREATE INDEX idx_tool_health_status_tool ON tool_health_status(tool_id);
```


## 七、初始化数据

```sql
-- 初始化第三方工具配置
INSERT INTO third_party_tools (id, name, code, category, api_endpoint, auth_type, rate_limit, priority, created_at) VALUES
(uuid_generate_v4(), '聚媒通', 'jumeitong', 'distribution', 'https://api.jumeitong.com/v2', 'apikey', 100, 1, NOW()),
(uuid_generate_v4(), 'Jasper', 'jasper', 'content_generation', 'https://api.jasper.ai/v1', 'apikey', 50, 2, NOW()),
(uuid_generate_v4(), 'Copy.ai', 'copyai', 'content_generation', 'https://api.copy.ai/v1', 'apikey', 100, 2, NOW()),
(uuid_generate_v4(), '网易千梦引擎', 'qianmeng', 'video_generation', 'https://qianmeng.163.com/api', 'apikey', 10, 2, NOW()),
(uuid_generate_v4(), '传声港', 'chuanshenggang', 'media_distribution', 'https://api.chuanshenggang.com/v1', 'apikey', 50, 2, NOW()),
(uuid_generate_v4(), '新榜', 'xinbang', 'analytics', 'https://api.xinbang.com/v1', 'apikey', 100, 2, NOW()),
(uuid_generate_v4(), '飞瓜数据', 'feigua', 'analytics', 'https://api.feigua.cn/v1', 'apikey', 50, 2, NOW()),
(uuid_generate_v4(), 'Simplified', 'simplified', 'marketing_agent', 'https://api.simplified.com/v1', 'apikey', 100, 3, NOW()),
(uuid_generate_v4(), 'Agent Cloud', 'agentcloud', 'marketing_agent', 'https://api.agentcloud.com/v1', 'apikey', 50, 3, NOW());
```


## 八、在Cursor中使用

```bash
# 1. 实现聚媒通适配器
@docs/THIRD_PARTY_INTEGRATION_v1.0.md 实现JumeitongAdapter，支持多平台分发，集成EX-03和EM-06能力

# 2. 实现内容生成适配器
@docs/THIRD_PARTY_INTEGRATION_v1.0.md 实现ContentGenerationAdapter，支持Jasper和Copy.ai，集成EM-01和EM-02能力

# 3. 实现千梦引擎适配器
@docs/THIRD_PARTY_INTEGRATION_v1.0.md 实现QianmengAdapter，支持视频生成，集成EX-10和EM-06能力

# 4. 实现传声港适配器
@docs/THIRD_PARTY_INTEGRATION_v1.0.md 实现ChuanshenggangAdapter，支持媒体发稿，集成EX-03和SC-06能力

# 5. 实现数据分析适配器
@docs/THIRD_PARTY_INTEGRATION_v1.0.md 实现AnalyticsAdapter，支持新榜和飞瓜，集成EM-01和EM-04能力

# 6. 实现统一适配器管理器
@docs/THIRD_PARTY_INTEGRATION_v1.0.md 实现ToolAdapterManager，统一管理所有第三方工具调用
```


## 九、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，6类第三方工具集成方案，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**