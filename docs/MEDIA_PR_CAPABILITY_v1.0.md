# 媒体发稿能力 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\MEDIA_PR_CAPABILITY_v1.0.md
```


# 媒体发稿能力 v1.0

## 一、能力总览

```yaml
module: "媒体发稿"
description: "支持央级、门户、垂直媒体资源管理，智能发稿、收录跟踪、GEO优化"
priority: "P1"
domain: "营销中心"

# 关联的通用能力
related_abilities:
  - "PC-01: 自然语言理解"
  - "PC-02: 代码理解"
  - "CG-01: 推理能力"
  - "CG-04: 数值推理"
  - "DC-03: 工具选择"
  - "DC-06: 方案生成"
  - "EX-03: API调用"
  - "EX-08: 消息发送"
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"
  - "EX-11: 定时执行"
  - "EX-12: 批量执行"
  - "WEB-02: 搜索引擎查询"
  - "WEB-03: 网页内容解析"
  - "WEB-04: API调用与集成"
  - "EM-01: 多模型路由"
  - "EM-04: 模型缓存"
  - "QL-01: 代码质量感知"
  - "QL-05: 质量验证"

functions:
  total_count: 4
  categories:
    - "媒体资源管理"
    - "智能发稿"
    - "效果追踪"
    - "内容优化"
```


## 二、媒体渠道配置

```yaml
# 媒体渠道分类
media_channels:
  central_media:  # 央级官媒
    - id: "people"
      name: "人民网"
      price: "50-200元/篇"
      coverage: "全国"
      audience: "政府、企业、高端人群"
      advantage: "最高权威性"
      
    - id: "xinhua"
      name: "新华网"
      price: "50-200元/篇"
      coverage: "全国"
      audience: "政府、企业、大众"
      advantage: "国家级通讯社"
      
    - id: "cctv"
      name: "央视网"
      price: "50-180元/篇"
      coverage: "全国"
      audience: "大众"
      advantage: "央视背书"
      
    - id: "china_daily"
      name: "中国日报网"
      price: "50-150元/篇"
      coverage: "国内外"
      audience: "涉外人群、外企"
      advantage: "英文传播"
      
    - id: "ce_cn"
      name: "中国经济网"
      price: "40-120元/篇"
      coverage: "全国"
      audience: "经济界、企业"
      advantage: "经济领域权威"
      
    - id: "st_daily"
      name: "科技日报"
      price: "40-120元/篇"
      coverage: "全国"
      audience: "科技界、科研人员"
      advantage: "科技领域权威"

  gateway_media:  # 综合门户
    - id: "sina"
      name: "新浪网"
      price: "5-50元/篇"
      coverage: "全国"
      audience: "大众"
      advantage: "流量大，传播范围广"
      
    - id: "netease"
      name: "网易"
      price: "5-50元/篇"
      coverage: "全国"
      audience: "年轻人群"
      advantage: "年轻用户群体"
      
    - id: "tencent"
      name: "腾讯网"
      price: "5-50元/篇"
      coverage: "全国"
      audience: "大众"
      advantage: "腾讯生态"
      
    - id: "sohu"
      name: "搜狐"
      price: "5-40元/篇"
      coverage: "全国"
      audience: "大众"
      advantage: "老牌门户"
      
    - id: "ifeng"
      name: "凤凰网"
      price: "10-60元/篇"
      coverage: "全国"
      audience: "中高端人群"
      advantage: "品质内容"

  vertical_media:  # 垂直行业
    - id: "36kr"
      name: "36氪"
      price: "30-200元/篇"
      coverage: "科技圈"
      audience: "创业者、投资人"
      advantage: "科技创投第一媒体"
      
    - id: "huxiu"
      name: "虎嗅"
      price: "30-180元/篇"
      coverage: "科技圈"
      audience: "创业者、科技爱好者"
      advantage: "深度内容"
      
    - id: "csdn"
      name: "CSDN"
      price: "10-50元/篇"
      coverage: "技术圈"
      audience: "开发者"
      advantage: "中国最大开发者社区"
      
    - id: "juejin"
      name: "掘金"
      price: "免费"
      coverage: "技术圈"
      audience: "年轻开发者"
      advantage: "高质量技术内容"
      
    - id: "woshipm"
      name: "人人都是产品经理"
      price: "10-50元/篇"
      coverage: "产品圈"
      audience: "产品经理、运营"
      advantage: "产品经理第一社区"

  international_media:  # 海外媒体
    - id: "reuters"
      name: "路透社"
      price: "200-1000美元/篇"
      coverage: "全球"
      audience: "全球读者"
      advantage: "全球顶级通讯社"
      
    - id: "yahoo_finance"
      name: "雅虎财经"
      price: "100-500美元/篇"
      coverage: "全球"
      audience: "投资者"
      advantage: "财经领域影响力"
      
    - id: "ap"
      name: "美联社"
      price: "200-800美元/篇"
      coverage: "全球"
      audience: "全球读者"
      advantage: "美国顶级通讯社"
      
    - id: "bloomberg"
      name: "彭博社"
      price: "300-1200美元/篇"
      coverage: "全球"
      audience: "金融从业者"
      advantage: "金融数据权威"
      
    - id: "techcrunch"
      name: "TechCrunch"
      price: "150-600美元/篇"
      coverage: "全球科技圈"
      audience: "科技从业者"
      advantage: "科技创投第一媒体"
```


## 三、功能详细设计

### 3.1 MK-18 媒体资源库

```yaml
# MK-18 媒体资源库
function_id: "MK-18"
name: "媒体资源库"
description: "管理央级、门户、垂直媒体资源，支持分类筛选、价格查询、效果评估"
priority: "P1"
implementation: "集成发稿平台（传声港等）"
related_abilities: ["EX-03", "WEB-04", "DC-03", "EX-09"]

# 数据模型
class MediaChannel:
    id: str
    name: str
    category: str  # central, gateway, vertical, international
    sub_category: str
    price_min: float
    price_max: float
    price_unit: str
    coverage: str
    audience: str
    advantage: str
    rating: float  # 1-5星
    publish_speed: str  # fast, medium, slow
    seo_impact: float  # SEO影响力分数
    historical_performance: Dict
    enabled: bool

class MediaFilter:
    categories: List[str]
    price_range: Tuple[float, float]
    min_rating: float
    keyword: str
    sort_by: str  # price, rating, speed, seo

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/media/list"
    description: "获取媒体列表"
    query_params:
      category: "str"
      min_price: "float"
      max_price: "float"
      keyword: "str"
      page: "int"
      page_size: "int"
    response:
      channels: "List[MediaChannel]"
      pagination: "dict"
      
  - method: "GET"
    endpoint: "/api/v1/marketing/media/{id}"
    description: "获取媒体详情"
    response:
      channel: "MediaChannel"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/media/recommend"
    description: "智能推荐媒体"
    request_body:
      article_content: "str"
      budget: "float"
      target_audience: "str"
    response:
      recommendations: "List[MediaChannel]"

# 实现示例
class MediaLibrary:
    """媒体资源库 - 对齐EX-03 API调用、DC-03工具选择"""
    
    def __init__(self):
        self.platform_api = ChuanshenggangAPI()  # 集成传声港
        self.cache_manager = CacheManager()  # 对齐EM-04
    
    async def get_media_list(self, filters: MediaFilter) -> List[MediaChannel]:
        """获取媒体列表 - 支持缓存"""
        # 检查缓存（对齐EM-04）
        cache_key = f"media_list:{hash(str(filters))}"
        cached = await self.cache_manager.get(cache_key)
        if cached:
            return cached
        
        # 调用发稿平台API（对齐EX-03）
        raw_media = await self.platform_api.get_media_list(
            category=filters.categories,
            min_price=filters.price_range[0],
            max_price=filters.price_range[1]
        )
        
        # 转换并排序
        channels = [self._convert_to_channel(m) for m in raw_media]
        
        # 应用筛选
        if filters.min_rating:
            channels = [c for c in channels if c.rating >= filters.min_rating]
        if filters.keyword:
            channels = [c for c in channels if filters.keyword.lower() in c.name.lower()]
        
        # 排序
        if filters.sort_by == "price":
            channels.sort(key=lambda x: x.price_min)
        elif filters.sort_by == "rating":
            channels.sort(key=lambda x: x.rating, reverse=True)
        elif filters.sort_by == "seo":
            channels.sort(key=lambda x: x.seo_impact, reverse=True)
        
        # 缓存结果
        await self.cache_manager.set(cache_key, channels, ttl=3600)  # 1小时
        
        return channels
    
    async def recommend_media(self, article_content: str, budget: float, 
                               target_audience: str) -> List[MediaChannel]:
        """智能推荐媒体 - 对齐DC-03工具选择、CG-01推理能力"""
        # 1. 分析文章内容（对齐PC-01）
        article_type = await self._analyze_article_type(article_content)
        
        # 2. 确定目标受众匹配
        audience_match = self._match_audience(target_audience)
        
        # 3. 获取所有可用媒体
        all_media = await self.get_media_list(MediaFilter())
        
        # 4. 计算推荐分数（对齐CG-01）
        scored_media = []
        for media in all_media:
            score = (
                self._content_match_score(article_type, media) * 0.3 +
                self._audience_match_score(target_audience, media) * 0.25 +
                self._budget_match_score(budget, media) * 0.2 +
                media.rating / 5 * 0.15 +
                media.seo_impact * 0.1
            )
            scored_media.append((media, score))
        
        # 5. 排序并返回Top N
        scored_media.sort(key=lambda x: x[1], reverse=True)
        return [media for media, score in scored_media[:10]]
```

### 3.2 MK-19 智能发稿

```yaml
# MK-19 智能发稿
function_id: "MK-19"
name: "智能发稿"
description: "一键提交多篇稿件到多个媒体，支持批量提交、定时发布"
priority: "P1"
implementation: "集成发稿平台"
related_abilities: ["EX-03", "EX-08", "EX-09", "EX-10", "EX-11", "EX-12", "AUTO-05"]

# 数据模型
class PressReleaseTask:
    id: str
    title: str
    content: str
    summary: str
    keywords: List[str]
    media_ids: List[str]
    total_cost: float
    status: str  # draft, submitted, publishing, published, partial, failed, cancelled
    scheduled_time: Optional[datetime]
    submitted_time: Optional[datetime]
    completed_time: Optional[datetime]
    results: List[PressResult]
    created_at: datetime

class PressResult:
    media_id: str
    media_name: str
    success: bool
    url: Optional[str]
    published_time: Optional[datetime]
    error: Optional[str]

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/press/submit"
    description: "提交发稿任务"
    request_body:
      title: "str"
      content: "str"
      media_ids: "List[str]"
      scheduled_time: "datetime"
    response:
      task_id: "str"
      estimated_cost: "float"
      
  - method: "GET"
    endpoint: "/api/v1/marketing/press/task/{id}"
    description: "查询发稿任务状态"
    response:
      task: "PressReleaseTask"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/press/task/{id}/cancel"
    description: "取消发稿任务"
    response:
      success: "bool"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/press/batch-submit"
    description: "批量提交多篇稿件"
    request_body:
      articles: "List[dict]"
      media_ids: "List[str]"
    response:
      task_ids: "List[str]"

# 实现示例
class PressReleaseManager:
    """智能发稿管理器 - 对齐EX-03 API调用、EX-12批量执行"""
    
    def __init__(self):
        self.platform_api = ChuanshenggangAPI()
        self.task_store = TaskStore()
        self.scheduler = AsyncIOScheduler()  # 对齐EX-11
    
    async def submit_article(self, title: str, content: str, 
                              media_ids: List[str],
                              scheduled_time: datetime = None) -> str:
        """提交发稿 - 支持定时"""
        # 1. 计算费用
        total_cost = await self._calculate_cost(media_ids)
        
        # 2. 创建任务
        task = PressReleaseTask(
            id=self._generate_id(),
            title=title,
            content=content,
            media_ids=media_ids,
            total_cost=total_cost,
            status="draft",
            scheduled_time=scheduled_time,
            created_at=datetime.now()
        )
        await self.task_store.save(task)
        
        # 3. 执行发布
        if scheduled_time:
            # 定时发布（对齐EX-11、AUTO-05）
            self.scheduler.add_job(
                func=self._execute_press,
                trigger="date",
                run_date=scheduled_time,
                args=[task.id]
            )
        else:
            # 立即发布（对齐EX-10异步执行）
            asyncio.create_task(self._execute_press(task.id))
        
        return task.id
    
    async def _execute_press(self, task_id: str):
        """执行发稿 - 对齐EX-03 API调用、EX-09并行执行"""
        task = await self.task_store.get(task_id)
        if not task or task.status != "draft":
            return
        
        task.status = "submitted"
        task.submitted_time = datetime.now()
        await self.task_store.update(task)
        
        # 并行提交到多个媒体（对齐EX-09）
        tasks = [self._submit_to_media(task, media_id) for media_id in task.media_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 汇总结果
        press_results = []
        success_count = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                press_results.append(PressResult(
                    media_id=task.media_ids[i],
                    media_name="",
                    success=False,
                    error=str(result)
                ))
            else:
                press_results.append(result)
                if result.success:
                    success_count += 1
        
        # 更新任务状态
        task.results = press_results
        if success_count == len(task.media_ids):
            task.status = "published"
        elif success_count > 0:
            task.status = "partial"
        else:
            task.status = "failed"
        task.completed_time = datetime.now()
        await self.task_store.update(task)
    
    async def batch_submit(self, articles: List[dict], media_ids: List[str]) -> List[str]:
        """批量提交多篇稿件 - 对齐EX-12批量执行"""
        tasks = []
        for article in articles:
            task_id = await self.submit_article(
                title=article["title"],
                content=article["content"],
                media_ids=media_ids,
                scheduled_time=article.get("scheduled_time")
            )
            tasks.append(task_id)
        return tasks
```

### 3.3 MK-20 收录跟踪

```yaml
# MK-20 收录跟踪
function_id: "MK-20"
name: "收录跟踪"
description: "跟踪百度收录、Google收录、AI引用情况，提供SEO效果分析"
priority: "P1"
implementation: "集成SEO工具（百度站长、Google Search Console）"
related_abilities: ["WEB-02", "WEB-03", "CG-04", "EX-09"]

# 数据模型
class IndexingRecord:
    id: str
    press_task_id: str
    article_title: str
    article_url: str
    baidu_indexed: bool
    baidu_index_time: Optional[datetime]
    google_indexed: bool
    google_index_time: Optional[datetime]
    ai_citations: int
    ai_citation_sources: List[str]
    search_rankings: Dict[str, int]  # keyword -> rank
    daily_views: int
    created_at: datetime
    updated_at: datetime

class SEOAnalysis:
    article_id: str
    overall_score: float
    keyword_ranking: Dict[str, int]
    traffic_estimate: int
    improvement_suggestions: List[str]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/press/task/{id}/indexing"
    description: "获取收录情况"
    response:
      records: "List[IndexingRecord]"
      
  - method: "GET"
    endpoint: "/api/v1/marketing/press/task/{id}/seo-analysis"
    description: "获取SEO分析"
    response:
      analysis: "SEOAnalysis"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/press/task/{id}/reindex"
    description: "手动触发收录检查"
    response:
      task_id: "str"

# 实现示例
class IndexingTracker:
    """收录跟踪器 - 对齐WEB-02搜索引擎查询、WEB-03网页内容解析"""
    
    def __init__(self):
        self.baidu_api = BaiduSearchAPI()  # 对齐WEB-02
        self.google_api = GoogleSearchAPI()
        self.ai_detector = AICitationDetector()
    
    async def track_indexing(self, press_task_id: str, article_url: str) -> IndexingRecord:
        """跟踪收录情况 - 对齐WEB-02、EX-09并行执行"""
        # 并行检查各搜索引擎（对齐EX-09）
        tasks = [
            self._check_baidu_index(article_url),
            self._check_google_index(article_url),
            self._check_ai_citations(article_url)
        ]
        results = await asyncio.gather(*tasks)
        
        baidu_result, google_result, ai_result = results
        
        return IndexingRecord(
            id=self._generate_id(),
            press_task_id=press_task_id,
            article_title="",
            article_url=article_url,
            baidu_indexed=baidu_result["indexed"],
            baidu_index_time=baidu_result["index_time"],
            google_indexed=google_result["indexed"],
            google_index_time=google_result["index_time"],
            ai_citations=ai_result["count"],
            ai_citation_sources=ai_result["sources"],
            search_rankings=await self._get_search_rankings(article_url),
            daily_views=await self._get_daily_views(article_url),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    
    async def _check_baidu_index(self, url: str) -> dict:
        """检查百度收录 - 对齐WEB-02"""
        # 使用百度站长API或site:查询
        query = f"site:{url}"
        results = await self.baidu_api.search(query)
        
        indexed = len(results) > 0
        index_time = results[0].date if indexed else None
        
        return {"indexed": indexed, "index_time": index_time}
    
    async def _check_google_index(self, url: str) -> dict:
        """检查Google收录 - 对齐WEB-02"""
        query = f"site:{url}"
        results = await self.google_api.search(query)
        
        indexed = len(results) > 0
        index_time = results[0].date if indexed else None
        
        return {"indexed": indexed, "index_time": index_time}
    
    async def _check_ai_citations(self, url: str) -> dict:
        """检查AI引用情况 - 对齐WEB-03"""
        # 搜索引用该文章的大模型训练数据
        citations = await self.ai_detector.detect_citations(url)
        
        return {"count": len(citations), "sources": citations}
    
    async def get_seo_analysis(self, article_url: str) -> SEOAnalysis:
        """获取SEO分析 - 对齐CG-04数值推理"""
        # 获取关键词排名
        keywords = await self._extract_keywords(article_url)
        rankings = {}
        for kw in keywords:
            rank = await self._get_ranking(article_url, kw)
            rankings[kw] = rank
        
        # 计算综合得分
        avg_rank = sum(rankings.values()) / len(rankings) if rankings else 100
        overall_score = max(0, 100 - (avg_rank - 1) * 2)
        
        # 估算流量
        traffic = self._estimate_traffic(rankings)
        
        # 生成优化建议
        suggestions = self._generate_seo_suggestions(rankings)
        
        return SEOAnalysis(
            article_id=article_url,
            overall_score=round(overall_score, 1),
            keyword_ranking=rankings,
            traffic_estimate=traffic,
            improvement_suggestions=suggestions
        )
```

### 3.4 MK-21 GEO优化

```yaml
# MK-21 GEO优化
function_id: "MK-21"
name: "GEO优化"
description: "针对AI搜索引擎（ChatGPT、Perplexity、Bing AI等）进行内容优化，提升AI回答中的引用率"
priority: "P2"
implementation: "自研 + 第三方GEO工具"
related_abilities: ["PC-01", "CG-01", "DC-06", "QL-01", "QL-05", "EM-01"]

# 数据模型
class GEOAnalysis:
    article_id: str
    article_content: str
    geo_score: float  # 0-100
    ai_friendliness: float  # AI友好度
    structure_score: float  # 结构化程度
    entity_density: Dict[str, float]  # 实体密度
    question_coverage: List[str]  # 覆盖的问题
    optimization_suggestions: List[str]
    predicted_citation_rate: float  # 预测引用率

class GEOOptimizedContent:
    original_content: str
    optimized_content: str
    changes: List[dict]
    geo_score_before: float
    geo_score_after: float
    improvement: float

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/geo/analyze"
    description: "GEO分析"
    request_body:
      content: "str"
    response:
      analysis: "GEOAnalysis"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/geo/optimize"
    description: "GEO优化"
    request_body:
      content: "str"
      target_ais: "List[str]"  # chatgpt, perplexity, claude, gemini
    response:
      optimized: "GEOOptimizedContent"

# 实现示例
class GEOOptimizer:
    """GEO优化器 - 对齐PC-01自然语言理解、CG-01推理能力"""
    
    def __init__(self):
        self.entity_extractor = EntityExtractor()  # 对齐PC-01
        self.question_generator = QuestionGenerator()
        self.model_router = ModelRouter()  # 对齐EM-01
    
    async def analyze(self, content: str) -> GEOAnalysis:
        """GEO分析 - 对齐PC-01、CG-01、QL-01"""
        # 1. 提取实体（对齐PC-01）
        entities = await self.entity_extractor.extract(content)
        
        # 2. 计算AI友好度（对齐CG-01）
        ai_friendliness = await self._calculate_ai_friendliness(content)
        
        # 3. 评估结构化程度（对齐QL-01）
        structure_score = self._evaluate_structure(content)
        
        # 4. 检查常见问题覆盖
        questions = await self.question_generator.generate(content)
        question_coverage = await self._check_question_coverage(content, questions)
        
        # 5. 计算实体密度
        entity_density = self._calculate_entity_density(content, entities)
        
        # 6. 综合GEO得分
        geo_score = (
            ai_friendliness * 0.3 +
            structure_score * 0.25 +
            len(question_coverage) / len(questions) * 0.25 +
            min(1.0, sum(entity_density.values()) / 0.1) * 0.2
        ) * 100
        
        # 7. 生成优化建议
        suggestions = self._generate_geo_suggestions(
            ai_friendliness, structure_score, question_coverage, entity_density
        )
        
        # 8. 预测引用率（对齐CG-01）
        predicted_rate = self._predict_citation_rate(geo_score)
        
        return GEOAnalysis(
            article_id=self._generate_id(),
            article_content=content[:500],
            geo_score=round(geo_score, 1),
            ai_friendliness=ai_friendliness,
            structure_score=structure_score,
            entity_density=entity_density,
            question_coverage=question_coverage,
            optimization_suggestions=suggestions,
            predicted_citation_rate=predicted_rate
        )
    
    async def optimize(self, content: str, target_ais: List[str] = None) -> GEOOptimizedContent:
        """GEO优化 - 对齐DC-06方案生成、EM-01多模型路由"""
        # 分析原始内容
        before = await self.analyze(content)
        
        # 选择优化策略（对齐EM-01）
        strategy = await self.model_router.route(
            task_type="geo_optimization",
            target_ais=target_ais or ["chatgpt", "perplexity", "claude", "gemini"],
            content_type=self._detect_content_type(content)
        )
        
        # 生成优化内容（对齐DC-06）
        optimized = await self._apply_strategy(content, strategy)
        
        # 验证质量（对齐QL-05）
        optimized = await self._validate_and_fix(optimized)
        
        # 分析优化后
        after = await self.analyze(optimized)
        
        return GEOOptimizedContent(
            original_content=content,
            optimized_content=optimized,
            changes=self._diff_content(content, optimized),
            geo_score_before=before.geo_score,
            geo_score_after=after.geo_score,
            improvement=after.geo_score - before.geo_score
        )
    
    async def _calculate_ai_friendliness(self, content: str) -> float:
        """计算AI友好度 - 对齐PC-01"""
        factors = {
            "clarity": await self._assess_clarity(content),
            "logical_flow": await self._assess_logical_flow(content),
            "evidence_support": await self._assess_evidence(content),
            "formatting": self._assess_formatting(content),
            "schema_markup": self._has_schema_markup(content)
        }
        return sum(factors.values()) / len(factors)
    
    def _generate_geo_suggestions(self, ai_friendliness: float, 
                                   structure_score: float,
                                   question_coverage: List[str],
                                   entity_density: Dict[str, float]) -> List[str]:
        """生成GEO优化建议 - 对齐CG-01"""
        suggestions = []
        
        if ai_friendliness < 0.7:
            suggestions.append("使用更清晰的语言和逻辑结构，便于AI理解")
        
        if structure_score < 0.6:
            suggestions.append("添加标题层级（H1/H2/H3），优化段落结构")
        
        if len(question_coverage) < 5:
            suggestions.append("增加FAQ部分，覆盖用户可能问到的相关问题")
        
        if sum(entity_density.values()) < 0.05:
            suggestions.append("增加专业术语和实体密度，提升领域权威性")
        
        return suggestions
```

## 四、媒体发稿流程架构图

```yaml
architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           媒体发稿流程                                      │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         内容准备层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 稿件生成    │  │ GEO优化     │  │ 关键词提取  │                  │   │
  │  │  │ (MK-01)     │  │ (MK-21)     │  │ (PC-01)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         媒体选择层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 媒体资源库  │  │ 智能推荐    │  │ 预算匹配    │                  │   │
  │  │  │ (MK-18)     │  │ (DC-03)     │  │ (CG-04)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         发稿执行层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 智能发稿    │  │ 定时发布    │  │ 批量提交    │                  │   │
  │  │  │ (MK-19)     │  │ (EX-11)     │  │ (EX-12)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         效果追踪层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 收录跟踪    │  │ SEO分析     │  │ AI引用检测  │                  │   │
  │  │  │ (MK-20)     │  │ (CG-04)     │  │ (WEB-03)    │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```

## 五、通用能力映射表

```yaml
# 媒体发稿功能与通用能力映射
general_ability_mapping:
  PC-01_自然语言理解:
    mapped_functions: ["MK-18", "MK-20", "MK-21"]
    description: "分析文章内容、提取关键词、理解搜索意图"
    
  CG-01_推理能力:
    mapped_functions: ["MK-18", "MK-20", "MK-21"]
    description: "智能推荐媒体、SEO分析推理、GEO评分计算"
    
  CG-04_数值推理:
    mapped_functions: ["MK-18", "MK-19", "MK-20"]
    description: "成本计算、价格匹配、排名分析"
    
  DC-03_工具选择:
    mapped_functions: ["MK-18"]
    description: "选择最优媒体渠道"
    
  DC-06_方案生成:
    mapped_functions: ["MK-21"]
    description: "生成GEO优化方案"
    
  EX-03_API调用:
    mapped_functions: ["MK-18", "MK-19"]
    description: "调用发稿平台API"
    
  EX-08_消息发送:
    mapped_functions: ["MK-19"]
    description: "提交发稿请求"
    
  EX-09_并行执行:
    mapped_functions: ["MK-19", "MK-20"]
    description: "并行提交多篇稿件、并行检查收录"
    
  EX-10_异步执行:
    mapped_functions: ["MK-19"]
    description: "异步处理发稿任务"
    
  EX-11_定时执行:
    mapped_functions: ["MK-19"]
    description: "定时发布稿件"
    
  EX-12_批量执行:
    mapped_functions: ["MK-19"]
    description: "批量提交多篇稿件"
    
  WEB-02_搜索引擎查询:
    mapped_functions: ["MK-20"]
    description: "查询百度/Google收录情况"
    
  WEB-03_网页内容解析:
    mapped_functions: ["MK-20", "MK-21"]
    description: "解析搜索结果、提取引用信息"
    
  WEB-04_API调用与集成:
    mapped_functions: ["MK-18", "MK-19"]
    description: "集成发稿平台API"
    
  EM-01_多模型路由:
    mapped_functions: ["MK-21"]
    description: "选择最优GEO优化策略"
    
  EM-04_模型缓存:
    mapped_functions: ["MK-18"]
    description: "缓存媒体列表数据"
    
  QL-01_代码质量感知:
    mapped_functions: ["MK-21"]
    description: "评估内容结构化程度"
    
  QL-05_质量验证:
    mapped_functions: ["MK-21"]
    description: "验证优化后内容质量"
    
  AUTO-05_智能定时触发:
    mapped_functions: ["MK-19"]
    description: "定时发稿调度"
```

## 六、数据库表结构

```sql
-- 媒体渠道表
CREATE TABLE media_channels (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50),
    price_min DECIMAL(10,2),
    price_max DECIMAL(10,2),
    price_unit VARCHAR(20),
    coverage VARCHAR(100),
    audience TEXT,
    advantage TEXT,
    rating DECIMAL(3,2),
    publish_speed VARCHAR(20),
    seo_impact DECIMAL(5,2),
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL
);

-- 发稿任务表
CREATE TABLE press_tasks (
    id UUID PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    keywords TEXT[],
    media_ids UUID[],
    total_cost DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'draft',
    scheduled_time TIMESTAMP,
    submitted_time TIMESTAMP,
    completed_time TIMESTAMP,
    results JSONB,
    created_by UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 收录记录表
CREATE TABLE indexing_records (
    id UUID PRIMARY KEY,
    press_task_id UUID REFERENCES press_tasks(id),
    article_url VARCHAR(500),
    baidu_indexed BOOLEAN DEFAULT FALSE,
    baidu_index_time TIMESTAMP,
    google_indexed BOOLEAN DEFAULT FALSE,
    google_index_time TIMESTAMP,
    ai_citations INTEGER DEFAULT 0,
    ai_citation_sources TEXT[],
    search_rankings JSONB,
    daily_views INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- GEO分析记录表
CREATE TABLE geo_analysis (
    id UUID PRIMARY KEY,
    article_id VARCHAR(500),
    article_content TEXT,
    geo_score DECIMAL(5,2),
    ai_friendliness DECIMAL(5,2),
    structure_score DECIMAL(5,2),
    entity_density JSONB,
    question_coverage TEXT[],
    optimization_suggestions TEXT[],
    predicted_citation_rate DECIMAL(5,2),
    created_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_media_channels_category ON media_channels(category);
CREATE INDEX idx_media_channels_rating ON media_channels(rating DESC);
CREATE INDEX idx_press_tasks_status ON press_tasks(status);
CREATE INDEX idx_press_tasks_scheduled ON press_tasks(scheduled_time);
CREATE INDEX idx_indexing_records_task ON indexing_records(press_task_id);
CREATE INDEX idx_geo_analysis_article ON geo_analysis(article_id);
```

## 七、在Cursor中使用

```bash
# 1. 实现媒体资源库
@docs/MEDIA_PR_CAPABILITY_v1.0.md 实现MK-18媒体资源库，集成传声港API，支持媒体分类筛选

# 2. 实现智能发稿
@docs/MEDIA_PR_CAPABILITY_v1.0.md 实现MK-19智能发稿，支持单篇和批量提交，使用EX-09并行执行

# 3. 实现收录跟踪
@docs/MEDIA_PR_CAPABILITY_v1.0.md 实现MK-20收录跟踪，集成百度站长和Google Search Console API

# 4. 实现GEO优化
@docs/MEDIA_PR_CAPABILITY_v1.0.md 实现MK-21 GEO优化，针对AI搜索引擎优化内容
```

## 八、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，4项媒体发稿功能，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**