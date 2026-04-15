# 多平台分发能力 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\MULTI_PLATFORM_DISTRIBUTION_v1.0.md
```


# 多平台分发能力 v1.0

## 一、能力总览

```yaml
module: "多平台分发"
description: "支持国内外多平台内容一键发布、定时发布、错峰发布、账号管理、多语言适配"
priority: "P0"
domain: "营销中心"

# 关联的通用能力
related_abilities:
  - "EX-03: API调用"
  - "EX-08: 消息发送"
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"
  - "EX-11: 定时执行"
  - "EX-12: 批量执行"
  - "WEB-05: 社交媒体交互"
  - "WEB-06: 在线文档与协作工具"
  - "AUTO-05: 智能定时与触发任务"
  - "EM-01: 多模型路由"
  - "EM-04: 模型缓存"
  - "PC-01: 自然语言理解"

functions:
  total_count: 6
  categories:
    - "平台分发"
    - "时间调度"
    - "账号管理"
    - "多语言处理"
```


## 二、功能详细设计

### 2.1 MK-08 国内平台分发

```yaml
# MK-08 国内平台分发
function_id: "MK-08"
name: "国内平台分发"
description: "一键发布到微信公众号、抖音、知乎、B站、微博、小红书等国内平台"
priority: "P0"
implementation: "集成聚媒通等第三方工具"
related_abilities: ["EX-03", "EX-08", "WEB-05", "EX-09"]

# 支持的国内平台
platforms_domestic:
  - id: "wechat"
    name: "微信公众号"
    category: "social"
    api_type: "official"
    rate_limit: "100/天"
    
  - id: "douyin"
    name: "抖音"
    category: "video"
    api_type: "official"
    rate_limit: "50/天"
    
  - id: "zhihu"
    name: "知乎"
    category: "qa"
    api_type: "official"
    rate_limit: "200/天"
    
  - id: "bilibili"
    name: "B站"
    category: "video"
    api_type: "official"
    rate_limit: "50/天"
    
  - id: "weibo"
    name: "微博"
    category: "social"
    api_type: "official"
    rate_limit: "200/天"
    
  - id: "xiaohongshu"
    name: "小红书"
    category: "social"
    api_type: "official"
    rate_limit: "100/天"
    
  - id: "juejin"
    name: "掘金"
    category: "tech"
    api_type: "official"
    rate_limit: "50/天"
    
  - id: "csdn"
    name: "CSDN"
    category: "tech"
    api_type: "official"
    rate_limit: "100/天"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/distribute/domestic"
    description: "国内平台分发"
    request_body:
      content: "string"
      platforms: "List[str]"
      media_files: "List[str]"
      schedule_time: "datetime"
    response:
      task_id: "string"
      results: "List[DistributionResult]"

# 数据模型
class DistributionResult:
    platform: str
    success: bool
    post_id: Optional[str]
    url: Optional[str]
    error: Optional[str]
    timestamp: datetime

# 实现示例
class DomesticDistributor:
    """国内平台分发器 - 对齐EX-03 API调用、WEB-05社交媒体交互"""
    
    def __init__(self):
        self.platform_apis = {
            "wechat": WechatAPI(),
            "douyin": DouyinAPI(),
            "zhihu": ZhihuAPI(),
            "bilibili": BilibiliAPI(),
            "weibo": WeiboAPI(),
            "xiaohongshu": XiaohongshuAPI()
        }
        self.rate_limiter = RateLimiter()  # 对齐SC-06速率限制
    
    async def distribute(self, content: str, platforms: List[str], 
                         media_files: List[str] = None) -> List[DistributionResult]:
        """分发到多个平台 - 使用并行执行（EX-09）"""
        tasks = []
        for platform in platforms:
            if platform in self.platform_apis:
                tasks.append(self._publish_to_platform(platform, content, media_files))
        
        # 并行执行（对齐EX-09）
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return self._format_results(platforms, results)
    
    async def _publish_to_platform(self, platform: str, content: str, 
                                    media_files: List[str]) -> DistributionResult:
        """发布到单个平台 - 对齐EX-03 API调用"""
        try:
            # 限流控制（对齐SC-06）
            await self.rate_limiter.acquire(platform)
            
            api = self.platform_apis[platform]
            
            # 内容适配
            adapted_content = await self._adapt_content(content, platform)
            
            # 调用平台API（对齐EX-03）
            if media_files:
                result = await api.post_with_media(adapted_content, media_files)
            else:
                result = await api.post(adapted_content)
            
            return DistributionResult(
                platform=platform,
                success=True,
                post_id=result.post_id,
                url=result.url,
                timestamp=datetime.now()
            )
        except Exception as e:
            return DistributionResult(
                platform=platform,
                success=False,
                error=str(e),
                timestamp=datetime.now()
            )
```

### 2.2 MK-09 国外平台分发

```yaml
# MK-09 国外平台分发
function_id: "MK-09"
name: "国外平台分发"
description: "发布到Facebook、X(Twitter)、LinkedIn、Instagram、YouTube、TikTok等海外平台"
priority: "P1"
implementation: "集成Hootsuite、Buffer等海外工具"
related_abilities: ["EX-03", "EX-08", "WEB-05", "EX-09"]

# 支持的海外平台
platforms_international:
  - id: "facebook"
    name: "Facebook"
    category: "social"
    api_type: "official"
    rate_limit: "200/天"
    
  - id: "twitter"
    name: "X (Twitter)"
    category: "social"
    api_type: "official"
    rate_limit: "300/天"
    
  - id: "linkedin"
    name: "LinkedIn"
    category: "professional"
    api_type: "official"
    rate_limit: "100/天"
    
  - id: "instagram"
    name: "Instagram"
    category: "social"
    api_type: "official"
    rate_limit: "50/天"
    
  - id: "youtube"
    name: "YouTube"
    category: "video"
    api_type: "official"
    rate_limit: "50/天"
    
  - id: "tiktok"
    name: "TikTok"
    category: "video"
    api_type: "official"
    rate_limit: "50/天"
    
  - id: "medium"
    name: "Medium"
    category: "blog"
    api_type: "official"
    rate_limit: "50/天"
    
  - id: "devto"
    name: "Dev.to"
    category: "tech"
    api_type: "official"
    rate_limit: "100/天"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/distribute/international"
    description: "海外平台分发"
    request_body:
      content: "string"
      platforms: "List[str]"
      media_files: "List[str]"
      language: "string"
    response:
      task_id: "string"
      results: "List[DistributionResult]"
```

### 2.3 MK-10 定时发布

```yaml
# MK-10 定时发布
function_id: "MK-10"
name: "定时发布"
description: "预设发布时间，系统自动在指定时间发布内容"
priority: "P0"
implementation: "自研定时调度器"
related_abilities: ["EX-11", "AUTO-05"]

# 数据模型
class ScheduledPost:
    id: str
    content: str
    platforms: List[str]
    media_files: List[str]
    schedule_time: datetime
    status: str  # pending, processing, completed, failed
    created_at: datetime
    executed_at: Optional[datetime]
    results: List[DistributionResult]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/schedule"
    description: "创建定时发布任务"
    request_body:
      content: "string"
      platforms: "List[str]"
      schedule_time: "datetime"
      media_files: "List[str]"
    response:
      task_id: "string"
      scheduled_time: "datetime"

  - method: "GET"
    endpoint: "/api/v1/marketing/schedule/list"
    description: "获取定时任务列表"
    query_params:
      status: "pending|completed|failed"
      start_date: "date"
      end_date: "date"
    response:
      tasks: "List[ScheduledPost]"

  - method: "DELETE"
    endpoint: "/api/v1/marketing/schedule/{task_id}"
    description: "取消定时任务"

# 实现示例
class ScheduleManager:
    """定时发布管理器 - 对齐EX-11定时执行、AUTO-05智能定时触发"""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()  # 对齐EX-11
        self.task_store = TaskStore()
    
    async def schedule_post(self, content: str, platforms: List[str], 
                            schedule_time: datetime, media_files: List[str] = None) -> str:
        """创建定时发布任务"""
        task_id = self._generate_task_id()
        
        task = ScheduledPost(
            id=task_id,
            content=content,
            platforms=platforms,
            media_files=media_files,
            schedule_time=schedule_time,
            status="pending",
            created_at=datetime.now()
        )
        
        await self.task_store.save(task)
        
        # 添加定时任务（对齐EX-11）
        self.scheduler.add_job(
            func=self._execute_scheduled_post,
            trigger="date",
            run_date=schedule_time,
            args=[task_id],
            id=task_id
        )
        
        return task_id
    
    async def _execute_scheduled_post(self, task_id: str):
        """执行定时发布 - 对齐AUTO-05智能触发"""
        task = await self.task_store.get(task_id)
        if not task or task.status != "pending":
            return
        
        task.status = "processing"
        await self.task_store.update(task)
        
        # 调用分发器（对齐EX-03）
        distributor = DomesticDistributor()
        results = await distributor.distribute(task.content, task.platforms, task.media_files)
        
        task.status = "completed" if all(r.success for r in results) else "failed"
        task.executed_at = datetime.now()
        task.results = results
        await self.task_store.update(task)
```

### 2.4 MK-11 错峰发布

```yaml
# MK-11 错峰发布
function_id: "MK-11"
name: "错峰发布"
description: "基于数据分析智能选择各平台的最佳发布时间，提升曝光率"
priority: "P1"
implementation: "自研 + 数据分析"
related_abilities: ["PC-01", "EM-01", "EM-04", "DC-07"]

# 数据模型
class OptimalTimeSlot:
    platform: str
    best_time: datetime
    confidence: float
    reasoning: str
    alternative_times: List[datetime]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/optimize-time"
    description: "智能选择最佳发布时间"
    request_body:
      content: "string"
      platforms: "List[str]"
      date_range: "dict"
    response:
      optimal_times: "List[OptimalTimeSlot]"

# 实现示例
class PeakTimeOptimizer:
    """错峰发布优化器 - 对齐PC-01自然语言理解、EM-01多模型路由"""
    
    def __init__(self):
        self.analytics_engine = AnalyticsEngine()
        self.content_analyzer = ContentAnalyzer()  # 对齐PC-01
        self.model_router = ModelRouter()  # 对齐EM-01
    
    async def get_optimal_times(self, content: str, platforms: List[str], 
                                 date_range: dict) -> List[OptimalTimeSlot]:
        """智能选择最佳发布时间"""
        optimal_times = []
        
        for platform in platforms:
            # 1. 分析内容类型（对齐PC-01）
            content_type = await self.content_analyzer.analyze(content)
            
            # 2. 获取平台历史数据
            historical_data = await self.analytics_engine.get_platform_stats(platform)
            
            # 3. 获取目标受众活跃时段
            audience_active_hours = await self._get_audience_active_hours(platform, content_type)
            
            # 4. 考虑竞品发布时段
            competitor_posts = await self._get_competitor_schedule(platform)
            
            # 5. 综合计算最佳时间（对齐DC-07方案对比）
            best_time = await self._calculate_optimal_time(
                historical_data, 
                audience_active_hours, 
                competitor_posts,
                date_range
            )
            
            # 6. 生成备选时间
            alternative_times = self._generate_alternatives(best_time, 3)
            
            optimal_times.append(OptimalTimeSlot(
                platform=platform,
                best_time=best_time,
                confidence=self._calculate_confidence(historical_data),
                reasoning=self._generate_reasoning(content_type, audience_active_hours),
                alternative_times=alternative_times
            ))
        
        return optimal_times
    
    async def _calculate_optimal_time(self, historical_data, audience_hours, 
                                       competitor_posts, date_range) -> datetime:
        """计算最优发布时间 - 多因素加权"""
        # 使用多模型路由（对齐EM-01）选择最佳算法
        model = await self.model_router.route(task_type="time_optimization")
        
        # 计算时间分数
        scores = {}
        for hour in range(0, 24):
            score = (
                historical_data.get_engagement_score(hour) * 0.4 +
                audience_hours.get_activity_score(hour) * 0.3 +
                (1 - competitor_posts.get_density(hour)) * 0.2 +
                self._get_base_score(hour) * 0.1
            )
            scores[hour] = score
        
        best_hour = max(scores, key=scores.get)
        return datetime.now().replace(hour=best_hour, minute=0, second=0)
```

### 2.5 MK-12 账号分组管理

```yaml
# MK-12 账号分组管理
function_id: "MK-12"
name: "账号分组管理"
description: "多账号批量操作，支持按平台、类型、地区等分组管理"
priority: "P1"
implementation: "集成第三方工具 + 自研分组管理"
related_abilities: ["EX-03", "EX-12", "WEB-05"]

# 数据模型
class AccountGroup:
    id: str
    name: str
    description: str
    platforms: List[str]
    accounts: List[SocialAccount]
    created_at: datetime

class SocialAccount:
    id: str
    platform: str
    username: str
    access_token: str
    expires_at: datetime
    status: str  # active, expired, error
    groups: List[str]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/accounts/groups"
    description: "创建账号分组"
    request_body:
      name: "string"
      description: "string"
      account_ids: "List[str]"
    response:
      group_id: "string"

  - method: "GET"
    endpoint: "/api/v1/marketing/accounts/groups"
    description: "获取分组列表"
    response:
      groups: "List[AccountGroup]"

  - method: "POST"
    endpoint: "/api/v1/marketing/batch-publish"
    description: "批量发布到分组内所有账号"
    request_body:
      group_id: "string"
      content: "string"
      media_files: "List[str]"
    response:
      task_id: "string"
      results: "List[DistributionResult]"

# 实现示例
class AccountGroupManager:
    """账号分组管理器 - 对齐EX-12批量执行"""
    
    def __init__(self):
        self.group_store = GroupStore()
        self.batch_executor = BatchExecutor()  # 对齐EX-12
    
    async def create_group(self, name: str, account_ids: List[str], 
                           description: str = "") -> AccountGroup:
        """创建账号分组"""
        accounts = await self._get_accounts(account_ids)
        
        group = AccountGroup(
            id=self._generate_id(),
            name=name,
            description=description,
            platforms=list(set(a.platform for a in accounts)),
            accounts=accounts,
            created_at=datetime.now()
        )
        
        await self.group_store.save(group)
        return group
    
    async def batch_publish(self, group_id: str, content: str, 
                            media_files: List[str] = None) -> BatchResult:
        """批量发布到分组内所有账号 - 对齐EX-12"""
        group = await self.group_store.get(group_id)
        if not group:
            raise ValueError(f"Group {group_id} not found")
        
        # 构建批量任务
        tasks = []
        for account in group.accounts:
            distributor = self._get_distributor(account.platform)
            tasks.append({
                "distributor": distributor,
                "account": account,
                "content": content,
                "media_files": media_files
            })
        
        # 批量执行（对齐EX-12）
        results = await self.batch_executor.execute(tasks, max_concurrent=5)
        
        return BatchResult(
            total=len(tasks),
            success=sum(1 for r in results if r.success),
            failed=sum(1 for r in results if not r.success),
            details=results
        )
```

### 2.6 MK-13 多语言适配

```yaml
# MK-13 多语言适配
function_id: "MK-13"
name: "多语言适配"
description: "内容自动翻译适配海外平台，支持多语言本地化"
priority: "P2"
implementation: "集成翻译API（DeepL、Google Translate等）"
related_abilities: ["PC-01", "EM-01", "EM-04"]

# 支持的语言
supported_languages:
  - code: "zh-CN"
    name: "简体中文"
  - code: "zh-TW"
    name: "繁体中文"
  - code: "en-US"
    name: "英语"
  - code: "ja-JP"
    name: "日语"
  - code: "ko-KR"
    name: "韩语"
  - code: "fr-FR"
    name: "法语"
  - code: "de-DE"
    name: "德语"
  - code: "es-ES"
    name: "西班牙语"
  - code: "pt-BR"
    name: "葡萄牙语"
  - code: "ru-RU"
    name: "俄语"
  - code: "ar-SA"
    name: "阿拉伯语"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/translate"
    description: "内容多语言翻译"
    request_body:
      content: "string"
      source_lang: "string"
      target_langs: "List[str]"
      preserve_formatting: "bool"
    response:
      translations: "Dict[str, string]"

# 实现示例
class MultiLanguageAdapter:
    """多语言适配器 - 对齐PC-01自然语言理解、EM-01多模型路由"""
    
    def __init__(self):
        self.translation_apis = {
            "deepl": DeepLAPI(),
            "google": GoogleTranslateAPI(),
            "baidu": BaiduTranslateAPI()
        }
        self.model_router = ModelRouter()  # 对齐EM-01
        self.cache_manager = CacheManager()  # 对齐EM-04模型缓存
    
    async def translate(self, content: str, source_lang: str, 
                        target_langs: List[str], 
                        preserve_formatting: bool = True) -> Dict[str, str]:
        """多语言翻译 - 对齐PC-01、EM-01"""
        translations = {}
        
        for target_lang in target_langs:
            if source_lang == target_lang:
                translations[target_lang] = content
                continue
            
            # 检查缓存（对齐EM-04）
            cache_key = f"translation:{hash(content)}:{source_lang}:{target_lang}"
            cached = await self.cache_manager.get(cache_key)
            if cached:
                translations[target_lang] = cached
                continue
            
            # 选择最佳翻译API（对齐EM-01）
            api = await self.model_router.route(
                task_type="translation",
                source_lang=source_lang,
                target_lang=target_lang,
                content_length=len(content)
            )
            
            # 执行翻译
            translation = await api.translate(
                content, 
                source_lang=source_lang, 
                target_lang=target_lang,
                preserve_formatting=preserve_formatting
            )
            
            # 缓存结果（对齐EM-04）
            await self.cache_manager.set(cache_key, translation, ttl=86400)  # 24小时
            
            translations[target_lang] = translation
        
        return translations
    
    async def localize(self, content: str, target_region: str) -> str:
        """本地化适配（不仅是翻译，还包括文化适配）"""
        # 对齐PC-01理解内容意图
        intent = await self._analyze_intent(content)
        
        # 根据目标区域调整表达方式
        localized = await self._adapt_culture(content, target_region, intent)
        
        return localized
```

## 三、平台分发架构图

```yaml
architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           多平台分发架构                                    │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         分发调度层                                   │   │
  │  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐           │   │
  │  │  │ 实时分发引擎  │  │ 定时调度器    │  │ 错峰优化器    │           │   │
  │  │  │ (EX-09并行)   │  │ (EX-11定时)   │  │ (DC-07方案)   │           │   │
  │  │  └───────────────┘  └───────────────┘  └───────────────┘           │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         平台适配层                                   │   │
  │  │  ┌─────────────────────────────────────────────────────────────┐   │   │
  │  │  │                      统一分发接口                           │   │   │
  │  │  │                    (EX-03 API调用)                          │   │   │
  │  │  └─────────────────────────────────────────────────────────────┘   │   │
  │  │         │               │               │               │          │   │
  │  │         ▼               ▼               ▼               ▼          │   │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │   │
  │  │  │ 国内平台  │  │ 海外平台  │  │ 技术社区  │  │ 短视频平台 │       │   │
  │  │  │ 适配器    │  │ 适配器    │  │ 适配器    │  │ 适配器    │       │   │
  │  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         目标平台层                                   │   │
  │  │  微信公众号 | 抖音 | 知乎 | B站 | 微博 | 小红书 | 掘金 | CSDN        │   │
  │  │  Facebook | X | LinkedIn | Instagram | YouTube | TikTok | Medium   │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```

## 四、通用能力映射表

```yaml
# 多平台分发功能与通用能力映射
general_ability_mapping:
  EX-03_API调用:
    mapped_functions: ["MK-08", "MK-09", "MK-12"]
    description: "调用各平台API进行内容发布"
    
  EX-08_消息发送:
    mapped_functions: ["MK-08", "MK-09"]
    description: "发送内容到各平台"
    
  EX-09_并行执行:
    mapped_functions: ["MK-08", "MK-09", "MK-12"]
    description: "并行发布到多个平台"
    
  EX-10_异步执行:
    mapped_functions: ["MK-10"]
    description: "定时发布异步执行"
    
  EX-11_定时执行:
    mapped_functions: ["MK-10"]
    description: "按预设时间触发发布"
    
  EX-12_批量执行:
    mapped_functions: ["MK-12"]
    description: "批量发布到分组账号"
    
  SC-06_速率限制:
    mapped_functions: ["MK-08", "MK-09"]
    description: "控制各平台API调用频率"
    
  WEB-05_社交媒体交互:
    mapped_functions: ["MK-08", "MK-09", "MK-12"]
    description: "与社交媒体平台交互"
    
  AUTO-05_智能定时触发:
    mapped_functions: ["MK-10", "MK-11"]
    description: "智能选择发布时间"
    
  EM-01_多模型路由:
    mapped_functions: ["MK-11", "MK-13"]
    description: "选择最佳翻译API和优化算法"
    
  EM-04_模型缓存:
    mapped_functions: ["MK-13"]
    description: "缓存翻译结果"
    
  PC-01_自然语言理解:
    mapped_functions: ["MK-11", "MK-13"]
    description: "分析内容类型和意图"
    
  DC-07_方案对比:
    mapped_functions: ["MK-11"]
    description: "对比不同时间方案选择最优"
```

## 五、数据库表结构

```sql
-- 定时发布任务表
CREATE TABLE scheduled_posts (
    id UUID PRIMARY KEY,
    content TEXT NOT NULL,
    platforms TEXT[] NOT NULL,
    media_files TEXT[],
    schedule_time TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL,
    executed_at TIMESTAMP,
    results JSONB,
    created_by UUID REFERENCES agents(id)
);

-- 账号分组表
CREATE TABLE account_groups (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    platforms TEXT[],
    created_at TIMESTAMP NOT NULL,
    created_by UUID REFERENCES agents(id)
);

-- 社交账号表
CREATE TABLE social_accounts (
    id UUID PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(100) NOT NULL,
    access_token TEXT NOT NULL,
    expires_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active',
    group_ids UUID[],
    created_at TIMESTAMP NOT NULL
);

-- 平台分发记录表
CREATE TABLE distribution_logs (
    id UUID PRIMARY KEY,
    task_id UUID,
    platform VARCHAR(50) NOT NULL,
    content TEXT,
    post_id VARCHAR(200),
    post_url VARCHAR(500),
    status VARCHAR(20),
    error_message TEXT,
    duration_ms INTEGER,
    created_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_scheduled_posts_time ON scheduled_posts(schedule_time);
CREATE INDEX idx_scheduled_posts_status ON scheduled_posts(status);
CREATE INDEX idx_distribution_logs_task ON distribution_logs(task_id);
CREATE INDEX idx_distribution_logs_platform ON distribution_logs(platform);
```

## 六、在Cursor中使用

```bash
# 1. 实现国内平台分发
@docs/MULTI_PLATFORM_DISTRIBUTION_v1.0.md 实现MK-08国内平台分发，集成聚媒通API，使用EX-03和EX-09通用能力

# 2. 实现定时发布
@docs/MULTI_PLATFORM_DISTRIBUTION_v1.0.md 实现MK-10定时发布，使用EX-11定时执行能力

# 3. 实现错峰发布
@docs/MULTI_PLATFORM_DISTRIBUTION_v1.0.md 实现MK-11错峰发布，使用EM-01多模型路由和DC-07方案对比

# 4. 实现账号分组管理
@docs/MULTI_PLATFORM_DISTRIBUTION_v1.0.md 实现MK-12账号分组管理，使用EX-12批量执行能力

# 5. 实现多语言适配
@docs/MULTI_PLATFORM_DISTRIBUTION_v1.0.md 实现MK-13多语言适配，集成DeepL API，使用PC-01和EM-01能力
```

## 七、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，6项多平台分发功能，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**