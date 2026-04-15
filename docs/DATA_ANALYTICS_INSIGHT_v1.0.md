# 数据分析与洞察能力 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\DATA_ANALYTICS_INSIGHT_v1.0.md
```


# 数据分析与洞察能力 v1.0

## 一、能力总览

```yaml
module: "数据分析与洞察"
description: "支持多平台数据聚合分析、趋势发现、竞品监控、智能建议"
priority: "P0"
domain: "营销中心"

# 关联的通用能力
related_abilities:
  - "PC-01: 自然语言理解"
  - "PC-09: 情感分析"
  - "CG-01: 推理能力"
  - "CG-04: 数值推理"
  - "CG-06: 因果推断"
  - "CG-09: 不确定性推理"
  - "DC-06: 方案生成"
  - "DC-07: 方案对比"
  - "DC-08: 风险评估"
  - "EX-03: API调用"
  - "EX-09: 并行执行"
  - "EX-12: 批量执行"
  - "WEB-02: 搜索引擎查询"
  - "WEB-03: 网页内容解析"
  - "WEB-04: API调用与集成"
  - "WEB-05: 社交媒体交互"
  - "EM-01: 多模型路由"
  - "EM-04: 模型缓存"
  - "QL-02: 输出置信度评估"
  - "QL-07: 质量趋势分析"
  - "LN-01: 反馈学习"

functions:
  total_count: 5
  categories:
    - "数据可视化"
    - "平台对比"
    - "趋势分析"
    - "竞品监控"
    - "智能建议"
```

## 1.1、营销收入与财务口径对齐（基线）

营销中心（`UI_MARKETING_CENTER_v1.0.md`）与财务中心（`UI_FINANCE_CENTER_v1.0.md`）均展示「收入/收益」类指标时，**必须区分两套口径**，避免同一数字两种含义。

| 指标域 | 定义 | 权威来源 | 典型用途 |
|--------|------|----------|----------|
| **营销运营收入** | 接单与变现链路下的**运营视图**：按订单/平台**结算确认**或**交付确认**统计的金额（含各外接接单平台币种折算规则在实现层统一） | 营销中心数据域 + `ORDER_REVENUE_CAPABILITY_v1.0.md` | 营销总览、接单中心、转化率分析 |
| **财务总收入** | **会计/财务账**口径：权责发生制或现金收付（以财务模块配置为准），含全业务线、税费与核销状态 | `UI_FINANCE_CENTER` / 财务模块凭证与科目 | 损益、预算执行、税务与对账 |

**对账关系（设计约束）**

1. 营销运营收入应能下钻到**订单/项目 ID**，并与财务侧**应收账款/收入确认凭证**建立可追溯关联（允许存在时间性差异）。  
2. 界面展示时在首屏卡片或明细中标注口径标签，例如：`运营确认` / `财务已入账`。  
3. 若两者不一致，以**财务模块已过账数据**作为对外合并报表与合规披露依据；营销中心展示**差异说明**（在途、未开票、退款、跨期）。  

实现时可在数据层区分字段语义，例如 `revenue_marketing_ops` 与 `revenue_gl_confirmed`，具体表结构见本节数据模型中的 `revenue` 字段注释（业务含义以上表为准）。


## 二、数据模型定义

```yaml
# 营销数据模型

data_models:
  # 平台指标
  PlatformMetrics:
    platform: str
    date: date
    metrics:
      followers: int
      new_followers: int
      total_views: int
      daily_views: int
      total_likes: int
      daily_likes: int
      total_comments: int
      daily_comments: int
      total_shares: int
      daily_shares: int
      engagement_rate: float
      conversion_rate: float
      revenue: float  # 营销运营口径（接单/结算视图），非财务总账收入；对齐见上文 §1.1

  # 内容表现
  ContentPerformance:
    content_id: str
    platform: str
    title: str
    publish_date: datetime
    metrics:
      views: int
      likes: int
      comments: int
      shares: int
      saves: int
      click_rate: float
      conversion_rate: float
      revenue: float  # 同上，运营侧归因收入
    sentiment_score: float
    quality_score: float

  # 跨平台对比
  CrossPlatformComparison:
    date_range: dict
    platforms: List[str]
    metrics_comparison:
      - metric_name: str
        platform_values: Dict[str, float]
        best_platform: str
        worst_platform: str
        gap_percentage: float

  # 趋势分析
  TrendAnalysis:
    trend_name: str
    description: str
    growth_rate: float
    peak_time: datetime
    related_keywords: List[str]
    confidence: float
    forecast_next_period: float

  # 竞品分析
  CompetitorAnalysis:
    competitor_name: str
    platform: str
    metrics:
      followers: int
      engagement_rate: float
      avg_views: int
      posting_frequency: int
      top_content: List[dict]
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

  # 智能建议
  SmartSuggestion:
    suggestion_id: str
    type: str  # content, timing, platform, strategy
    title: str
    description: str
    expected_impact: float
    confidence: float
    action_items: List[str]
    priority: str  # high, medium, low
```


## 三、功能详细设计

### 3.1 MK-22 数据看板

```yaml
# MK-22 数据看板
function_id: "MK-22"
name: "数据看板"
description: "展示粉丝增长、互动数据、收益统计的综合看板"
priority: "P0"
implementation: "自研 + 平台API"
related_abilities: ["EX-03", "EX-09", "CG-04", "WEB-04"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/dashboard/overview"
    description: "获取数据看板概览"
    query_params:
      platforms: "List[str]"
      date_range: "str"  # today, week, month, custom
      start_date: "date"
      end_date: "date"
    response:
      overview: "DashboardOverview"

  - method: "GET"
    endpoint: "/api/v1/marketing/dashboard/trends"
    description: "获取趋势数据"
    query_params:
      metric: "str"  # followers, views, engagement, revenue
      platforms: "List[str]"
      days: "int"
    response:
      trend_data: "List[dict]"

  - method: "GET"
    endpoint: "/api/v1/marketing/dashboard/top-content"
    description: "获取表现最佳的内容"
    query_params:
      platform: "str"
      limit: "int"
      sort_by: "str"  # views, likes, shares, conversion
    response:
      contents: "List[ContentPerformance]"

# 实现示例
class MarketingDashboard:
    """营销数据看板 - 对齐CG-04数值推理、EX-09并行执行"""
    
    def __init__(self):
        self.platform_apis = {
            "wechat": WechatAPI(),
            "douyin": DouyinAPI(),
            "zhihu": ZhihuAPI(),
            "bilibili": BilibiliAPI(),
            "weibo": WeiboAPI(),
            "xiaohongshu": XiaohongshuAPI()
        }
        self.cache_manager = CacheManager()  # 对齐EM-04
    
    async def get_overview(self, platforms: List[str], 
                           date_range: str) -> DashboardOverview:
        """获取数据看板概览 - 使用并行执行（EX-09）"""
        # 并行获取各平台数据（对齐EX-09）
        tasks = [self._fetch_platform_metrics(p, date_range) for p in platforms]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 聚合数据（对齐CG-04）
        total_metrics = {
            "total_followers": 0,
            "new_followers": 0,
            "total_views": 0,
            "total_engagement": 0,
            "total_revenue": 0,
            "avg_engagement_rate": 0
        }
        
        platform_breakdown = []
        for i, result in enumerate(results):
            if isinstance(result, dict):
                for key in total_metrics:
                    if key in result:
                        total_metrics[key] += result.get(key, 0)
                platform_breakdown.append({
                    "platform": platforms[i],
                    "metrics": result
                })
        
        # 计算平均互动率
        if platform_breakdown:
            total_metrics["avg_engagement_rate"] = sum(
                p["metrics"].get("engagement_rate", 0) for p in platform_breakdown
            ) / len(platform_breakdown)
        
        return DashboardOverview(
            summary=total_metrics,
            platform_breakdown=platform_breakdown,
            last_updated=datetime.now()
        )
    
    async def _fetch_platform_metrics(self, platform: str, 
                                       date_range: str) -> dict:
        """获取平台指标 - 对齐EX-03 API调用"""
        # 检查缓存（对齐EM-04）
        cache_key = f"metrics:{platform}:{date_range}"
        cached = await self.cache_manager.get(cache_key)
        if cached:
            return cached
        
        api = self.platform_apis.get(platform)
        if not api:
            return {}
        
        try:
            # 调用平台API（对齐EX-03）
            metrics = await api.get_metrics(date_range=date_range)
            
            # 缓存结果（TTL=5分钟）
            await self.cache_manager.set(cache_key, metrics, ttl=300)
            
            return metrics
        except Exception as e:
            print(f"Failed to fetch metrics from {platform}: {e}")
            return {}
```

### 3.2 MK-23 跨平台对比

```yaml
# MK-23 跨平台对比
function_id: "MK-23"
name: "跨平台对比"
description: "对比各平台表现，识别最佳平台和薄弱环节"
priority: "P1"
implementation: "自研"
related_abilities: ["CG-04", "DC-07", "QL-07"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/compare/platforms"
    description: "跨平台对比"
    query_params:
      platforms: "List[str]"
      metrics: "List[str]"
      date_range: "str"
    response:
      comparison: "CrossPlatformComparison"

  - method: "GET"
    endpoint: "/api/v1/marketing/compare/ranking"
    description: "平台排名"
    query_params:
      metric: "str"
      date_range: "str"
    response:
      ranking: "List[dict]"

# 实现示例
class PlatformComparator:
    """跨平台对比器 - 对齐CG-04数值推理、DC-07方案对比"""
    
    async def compare_platforms(self, platforms: List[str], 
                                 metrics: List[str],
                                 date_range: str) -> CrossPlatformComparison:
        """跨平台对比"""
        # 获取各平台数据
        dashboard = MarketingDashboard()
        platform_data = {}
        
        for platform in platforms:
            metrics_data = await dashboard._fetch_platform_metrics(platform, date_range)
            platform_data[platform] = metrics_data
        
        # 计算对比结果（对齐CG-04）
        comparisons = []
        for metric in metrics:
            values = {}
            for platform, data in platform_data.items():
                values[platform] = data.get(metric, 0)
            
            # 找出最佳和最差平台
            best_platform = max(values, key=values.get)
            worst_platform = min(values, key=values.get)
            
            # 计算差距
            if values.get(best_platform, 0) > 0:
                gap = (values[best_platform] - values[worst_platform]) / values[best_platform] * 100
            else:
                gap = 0
            
            comparisons.append({
                "metric_name": metric,
                "platform_values": values,
                "best_platform": best_platform,
                "worst_platform": worst_platform,
                "gap_percentage": round(gap, 1)
            })
        
        # 生成优化建议（对齐DC-07）
        recommendations = self._generate_recommendations(comparisons)
        
        return CrossPlatformComparison(
            date_range={"start": start_date, "end": end_date},
            platforms=platforms,
            metrics_comparison=comparisons,
            recommendations=recommendations
        )
```

### 3.3 MK-24 趋势分析

```yaml
# MK-24 趋势分析
function_id: "MK-24"
name: "趋势分析"
description: "发现内容趋势和热点，预测未来走势"
priority: "P1"
implementation: "自研 + 第三方（新榜、飞瓜等）"
related_abilities: ["CG-04", "CG-06", "CG-09", "QL-07", "WEB-02"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/trends/hot-topics"
    description: "获取热门话题"
    query_params:
      platform: "str"
      category: "str"
      days: "int"
    response:
      topics: "List[HotTopic]"

  - method: "GET"
    endpoint: "/api/v1/marketing/trends/forecast"
    description: "趋势预测"
    query_params:
      metric: "str"
      platform: "str"
      days: "int"
    response:
      forecast: "TrendForecast"

  - method: "GET"
    endpoint: "/api/v1/marketing/trends/insights"
    description: "获取趋势洞察"
    query_params:
      date_range: "str"
    response:
      insights: "List[TrendInsight]"

# 实现示例
class TrendAnalyzer:
    """趋势分析器 - 对齐CG-04数值推理、CG-06因果推断"""
    
    def __init__(self):
        self.third_party_apis = {
            "xinbang": XinbangAPI(),  # 新榜
            "feigua": FeiguaAPI()     # 飞瓜数据
        }
    
    async def detect_trends(self, platform: str, days: int = 30) -> List[TrendAnalysis]:
        """检测趋势 - 对齐CG-04、CG-06"""
        # 获取历史数据
        historical_data = await self._get_historical_data(platform, days)
        
        # 时间序列分析（对齐CG-04）
        trends = []
        
        # 1. 识别上升趋势
        rising = self._detect_rising_trends(historical_data)
        for item in rising:
            trends.append(TrendAnalysis(
                trend_name=item["name"],
                description=f"{item['name']}呈现上升趋势",
                growth_rate=item["growth_rate"],
                peak_time=item["peak_time"],
                related_keywords=item["keywords"],
                confidence=item["confidence"],
                forecast_next_period=self._forecast_next(item)
            ))
        
        # 2. 识别季节性模式（对齐CG-06因果推断）
        seasonal = self._detect_seasonal_patterns(historical_data)
        trends.extend(seasonal)
        
        # 3. 识别突发热点
        spikes = self._detect_anomaly_spikes(historical_data)
        trends.extend(spikes)
        
        # 按置信度排序
        trends.sort(key=lambda x: x.confidence, reverse=True)
        
        return trends
    
    async def forecast_metric(self, metric: str, platform: str, 
                               days: int = 30) -> TrendForecast:
        """趋势预测 - 对齐CG-04、CG-09不确定性推理"""
        # 获取历史数据
        history = await self._get_metric_history(metric, platform, days * 2)
        
        # 使用时间序列预测模型
        if len(history) > 30:
            # 简单移动平均预测
            window = 7
            moving_avg = sum(history[-window:]) / window
            
            # 计算趋势
            trend = (history[-1] - history[-window]) / history[-window] if history[-window] > 0 else 0
            
            # 预测未来（对齐CG-04）
            predictions = []
            for i in range(1, days + 1):
                pred = moving_avg * (1 + trend * i / days)
                predictions.append(pred)
            
            # 计算置信区间（对齐CG-09）
            std_dev = self._calculate_std_dev(history)
            confidence_interval = {
                "lower": [p - 1.96 * std_dev for p in predictions],
                "upper": [p + 1.96 * std_dev for p in predictions]
            }
            
            return TrendForecast(
                metric=metric,
                platform=platform,
                predictions=predictions,
                confidence_interval=confidence_interval,
                confidence=0.85,
                method="moving_average"
            )
        
        return TrendForecast(
            metric=metric,
            platform=platform,
            predictions=[],
            confidence=0.3,
            method="insufficient_data"
        )
```

### 3.4 MK-25 竞品监控

```yaml
# MK-25 竞品监控
function_id: "MK-25"
name: "竞品监控"
description: "监控竞品内容动态，进行SWOT分析"
priority: "P2"
implementation: "集成第三方（新榜、飞瓜、SimilarWeb等）"
related_abilities: ["WEB-02", "WEB-03", "CG-01", "WEB-05"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/competitors/list"
    description: "获取竞品列表"
    response:
      competitors: "List[Competitor]"

  - method: "POST"
    endpoint: "/api/v1/marketing/competitors/add"
    description: "添加竞品"
    request_body:
      name: "str"
      platform: "str"
      account_id: "str"
    response:
      competitor: "Competitor"

  - method: "GET"
    endpoint: "/api/v1/marketing/competitors/{id}/analysis"
    description: "获取竞品分析"
    response:
      analysis: "CompetitorAnalysis"

  - method: "GET"
    endpoint: "/api/v1/marketing/competitors/benchmark"
    description: "行业基准对比"
    response:
      benchmark: "IndustryBenchmark"

# 实现示例
class CompetitorMonitor:
    """竞品监控器 - 对齐WEB-02搜索引擎查询、WEB-03网页内容解析"""
    
    def __init__(self):
        self.third_party_apis = {
            "xinbang": XinbangAPI(),
            "feigua": FeiguaAPI(),
            "similarweb": SimilarWebAPI()
        }
    
    async def analyze_competitor(self, competitor_id: str) -> CompetitorAnalysis:
        """竞品分析 - 对齐CG-01推理能力"""
        competitor = await self._get_competitor(competitor_id)
        
        # 获取竞品数据
        metrics = await self._fetch_competitor_metrics(competitor)
        
        # SWOT分析（对齐CG-01）
        strengths = self._identify_strengths(metrics)
        weaknesses = self._identify_weaknesses(metrics)
        opportunities = self._identify_opportunities(metrics)
        threats = self._identify_threats(metrics)
        
        # 获取竞品热门内容
        top_content = await self._get_top_content(competitor)
        
        return CompetitorAnalysis(
            competitor_name=competitor.name,
            platform=competitor.platform,
            metrics=metrics,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            top_content=top_content,
            benchmark_score=self._calculate_benchmark_score(metrics),
            updated_at=datetime.now()
        )
    
    async def get_industry_benchmark(self, platform: str, category: str) -> IndustryBenchmark:
        """行业基准对比"""
        # 获取行业平均数据
        avg_metrics = await self._get_industry_average(platform, category)
        
        # 获取自身数据
        my_metrics = await self._get_my_metrics(platform)
        
        # 对比分析
        comparison = []
        for metric, avg_value in avg_metrics.items():
            my_value = my_metrics.get(metric, 0)
            comparison.append({
                "metric": metric,
                "my_value": my_value,
                "industry_avg": avg_value,
                "percentile": self._calculate_percentile(my_value, avg_value),
                "gap": my_value - avg_value
            })
        
        return IndustryBenchmark(
            platform=platform,
            category=category,
            comparison=comparison,
            overall_rank=self._calculate_rank(comparison)
        )
```

### 3.5 MK-26 智能建议

```yaml
# MK-26 智能建议
function_id: "MK-26"
name: "智能建议"
description: "基于数据提供优化建议，包括内容、时机、平台策略"
priority: "P1"
implementation: "自研AI"
related_abilities: ["CG-01", "DC-06", "QL-02", "LN-01", "EM-01"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/suggestions"
    description: "获取智能建议"
    query_params:
      type: "str"  # content, timing, platform, strategy
      limit: "int"
    response:
      suggestions: "List[SmartSuggestion]"

  - method: "POST"
    endpoint: "/api/v1/marketing/suggestions/{id}/feedback"
    description: "建议反馈"
    request_body:
      helpful: "bool"
      comment: "str"
    response:
      success: "bool"

  - method: "GET"
    endpoint: "/api/v1/marketing/suggestions/history"
    description: "建议历史"
    response:
      history: "List[SmartSuggestion]"

# 实现示例
class SmartSuggestionEngine:
    """智能建议引擎 - 对齐CG-01推理能力、DC-06方案生成"""
    
    def __init__(self):
        self.model_router = ModelRouter()  # 对齐EM-01
        self.feedback_learner = FeedbackLearner()  # 对齐LN-01
    
    async def generate_suggestions(self, suggestion_type: str = "all",
                                    limit: int = 10) -> List[SmartSuggestion]:
        """生成智能建议 - 对齐CG-01、DC-06"""
        suggestions = []
        
        # 获取分析数据
        dashboard = MarketingDashboard()
        overview = await dashboard.get_overview(
            platforms=["wechat", "douyin", "zhihu", "bilibili"],
            date_range="week"
        )
        
        trend_analyzer = TrendAnalyzer()
        trends = await trend_analyzer.detect_trends("all", days=30)
        
        # 内容建议（对齐CG-01）
        if suggestion_type in ["all", "content"]:
            content_suggestions = await self._generate_content_suggestions(
                overview, trends
            )
            suggestions.extend(content_suggestions)
        
        # 时机建议
        if suggestion_type in ["all", "timing"]:
            timing_suggestions = await self._generate_timing_suggestions(overview)
            suggestions.extend(timing_suggestions)
        
        # 平台建议
        if suggestion_type in ["all", "platform"]:
            platform_suggestions = await self._generate_platform_suggestions(overview)
            suggestions.extend(platform_suggestions)
        
        # 策略建议
        if suggestion_type in ["all", "strategy"]:
            strategy_suggestions = await self._generate_strategy_suggestions(
                overview, trends
            )
            suggestions.extend(strategy_suggestions)
        
        # 按优先级排序
        suggestions.sort(key=lambda x: (x.priority == "high", x.expected_impact), reverse=True)
        
        # 应用置信度评估（对齐QL-02）
        for s in suggestions:
            s.confidence = self._calculate_suggestion_confidence(s)
        
        return suggestions[:limit]
    
    async def _generate_content_suggestions(self, overview: DashboardOverview,
                                             trends: List[TrendAnalysis]) -> List[SmartSuggestion]:
        """生成内容建议 - 对齐DC-06方案生成"""
        suggestions = []
        
        # 基于趋势的建议
        for trend in trends[:3]:
            suggestions.append(SmartSuggestion(
                suggestion_id=self._generate_id(),
                type="content",
                title=f"抓住「{trend.trend_name}」趋势",
                description=f"「{trend.trend_name}」正在上升，增长率为{trend.growth_rate:.1%}，建议创作相关内容",
                expected_impact=trend.growth_rate * 100,
                confidence=trend.confidence,
                action_items=[
                    f"创作与{trend.trend_name}相关的3-5篇内容",
                    f"使用关键词：{', '.join(trend.related_keywords[:5])}",
                    "在趋势高峰期前24小时内发布"
                ],
                priority="high" if trend.growth_rate > 0.3 else "medium"
            ))
        
        # 基于表现的建议
        if overview.summary.get("avg_engagement_rate", 0) < 0.02:
            suggestions.append(SmartSuggestion(
                suggestion_id=self._generate_id(),
                type="content",
                title="互动率偏低，建议优化内容形式",
                description=f"当前平均互动率为{overview.summary['avg_engagement_rate']:.1%}，低于行业基准",
                expected_impact=15.0,
                confidence=0.75,
                action_items=[
                    "增加问答互动环节",
                    "使用更多视觉元素（图片/视频）",
                    "在结尾添加行动号召"
                ],
                priority="high"
            ))
        
        return suggestions
    
    async def record_feedback(self, suggestion_id: str, helpful: bool, comment: str = None):
        """记录建议反馈 - 对齐LN-01反馈学习"""
        await self.feedback_learner.record_feedback(
            suggestion_id=suggestion_id,
            helpful=helpful,
            comment=comment,
            timestamp=datetime.now()
        )
        
        # 更新建议模型
        if helpful:
            await self.feedback_learner.reinforce(suggestion_id)
        else:
            await self.feedback_learner.penalize(suggestion_id)
```

## 四、数据分析架构图

```yaml
architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           数据分析架构                                      │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         数据采集层                                   │   │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
  │  │  │ 平台API   │  │ 第三方API │  │ Webhook   │  │ 数据导入  │        │   │
  │  │  │ (EX-03)   │  │ (WEB-04)  │  │           │  │           │        │   │
  │  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         数据处理层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 数据清洗    │  │ 标准化     │  │ 聚合计算    │                  │   │
  │  │  │             │  │             │  │ (CG-04)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         分析计算层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 趋势分析    │  │ 对比分析    │  │ 预测分析    │                  │   │
  │  │  │ (CG-04)     │  │ (DC-07)     │  │ (CG-06)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         洞察输出层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 数据看板    │  │ 智能建议    │  │ 竞品报告    │                  │   │
  │  │  │ (MK-22)     │  │ (MK-26)     │  │ (MK-25)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```

## 五、通用能力映射表

```yaml
# 数据分析功能与通用能力映射
general_ability_mapping:
  PC-01_自然语言理解:
    mapped_functions: ["MK-24", "MK-26"]
    description: "理解热点话题、生成自然语言建议"
    
  PC-09_情感分析:
    mapped_functions: ["MK-22", "MK-24"]
    description: "分析用户评论情感倾向"
    
  CG-01_推理能力:
    mapped_functions: ["MK-24", "MK-25", "MK-26"]
    description: "趋势推理、竞品分析、策略推理"
    
  CG-04_数值推理:
    mapped_functions: ["MK-22", "MK-23", "MK-24"]
    description: "数据聚合、指标计算、趋势预测"
    
  CG-06_因果推断:
    mapped_functions: ["MK-24", "MK-26"]
    description: "识别因果关系、预测干预效果"
    
  CG-09_不确定性推理:
    mapped_functions: ["MK-24"]
    description: "预测置信区间"
    
  DC-06_方案生成:
    mapped_functions: ["MK-26"]
    description: "生成优化建议方案"
    
  DC-07_方案对比:
    mapped_functions: ["MK-23"]
    description: "跨平台表现对比"
    
  DC-08_风险评估:
    mapped_functions: ["MK-26"]
    description: "评估建议实施风险"
    
  EX-03_API调用:
    mapped_functions: ["MK-22", "MK-24", "MK-25"]
    description: "调用平台和第三方API"
    
  EX-09_并行执行:
    mapped_functions: ["MK-22"]
    description: "并行获取多平台数据"
    
  WEB-02_搜索引擎查询:
    mapped_functions: ["MK-24", "MK-25"]
    description: "搜索热点和竞品信息"
    
  WEB-03_网页内容解析:
    mapped_functions: ["MK-24", "MK-25"]
    description: "解析搜索结果和竞品内容"
    
  WEB-04_API调用与集成:
    mapped_functions: ["MK-22", "MK-24", "MK-25"]
    description: "集成第三方数据源"
    
  EM-01_多模型路由:
    mapped_functions: ["MK-26"]
    description: "选择最佳建议生成策略"
    
  EM-04_模型缓存:
    mapped_functions: ["MK-22"]
    description: "缓存数据看板结果"
    
  QL-02_输出置信度评估:
    mapped_functions: ["MK-24", "MK-26"]
    description: "评估预测和建议置信度"
    
  QL-07_质量趋势分析:
    mapped_functions: ["MK-23", "MK-24"]
    description: "分析质量指标变化趋势"
    
  LN-01_反馈学习:
    mapped_functions: ["MK-26"]
    description: "从用户反馈中学习优化建议"
```

## 六、数据库表结构

```sql
-- 平台指标数据表
CREATE TABLE platform_metrics (
    id UUID PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    date DATE NOT NULL,
    followers INTEGER DEFAULT 0,
    new_followers INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    daily_views INTEGER DEFAULT 0,
    total_likes INTEGER DEFAULT 0,
    daily_likes INTEGER DEFAULT 0,
    total_comments INTEGER DEFAULT 0,
    daily_comments INTEGER DEFAULT 0,
    total_shares INTEGER DEFAULT 0,
    daily_shares INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,2),
    conversion_rate DECIMAL(5,2),
    revenue DECIMAL(10,2),
    created_at TIMESTAMP NOT NULL,
    UNIQUE(platform, date)
);

-- 内容表现表
CREATE TABLE content_performance (
    id UUID PRIMARY KEY,
    content_id VARCHAR(200) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    title VARCHAR(500),
    publish_date TIMESTAMP,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    click_rate DECIMAL(5,2),
    conversion_rate DECIMAL(5,2),
    revenue DECIMAL(10,2),
    sentiment_score DECIMAL(5,2),
    quality_score DECIMAL(5,2),
    created_at TIMESTAMP NOT NULL
);

-- 趋势分析表
CREATE TABLE trend_analysis (
    id UUID PRIMARY KEY,
    trend_name VARCHAR(200) NOT NULL,
    description TEXT,
    growth_rate DECIMAL(5,2),
    peak_time TIMESTAMP,
    related_keywords TEXT[],
    confidence DECIMAL(5,2),
    forecast_next_period DECIMAL(10,2),
    created_at TIMESTAMP NOT NULL
);

-- 竞品表
CREATE TABLE competitors (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    account_id VARCHAR(200),
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 竞品分析表
CREATE TABLE competitor_analysis (
    id UUID PRIMARY KEY,
    competitor_id UUID REFERENCES competitors(id),
    metrics JSONB,
    strengths TEXT[],
    weaknesses TEXT[],
    opportunities TEXT[],
    threats TEXT[],
    top_content JSONB,
    benchmark_score DECIMAL(5,2),
    created_at TIMESTAMP NOT NULL
);

-- 智能建议表
CREATE TABLE smart_suggestions (
    id UUID PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    expected_impact DECIMAL(5,2),
    confidence DECIMAL(5,2),
    action_items TEXT[],
    priority VARCHAR(20),
    helpful_count INTEGER DEFAULT 0,
    not_helpful_count INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_platform_metrics_platform ON platform_metrics(platform);
CREATE INDEX idx_platform_metrics_date ON platform_metrics(date);
CREATE INDEX idx_content_performance_platform ON content_performance(platform);
CREATE INDEX idx_content_performance_publish ON content_performance(publish_date);
CREATE INDEX idx_trend_analysis_created ON trend_analysis(created_at);
CREATE INDEX idx_competitors_platform ON competitors(platform);
CREATE INDEX idx_smart_suggestions_type ON smart_suggestions(type);
CREATE INDEX idx_smart_suggestions_priority ON smart_suggestions(priority);
```

## 七、在Cursor中使用

```bash
# 1. 实现数据看板
@docs/DATA_ANALYTICS_INSIGHT_v1.0.md 实现MK-22数据看板，集成多平台API，使用EX-09并行执行

# 2. 实现跨平台对比
@docs/DATA_ANALYTICS_INSIGHT_v1.0.md 实现MK-23跨平台对比，使用CG-04数值推理和DC-07方案对比

# 3. 实现趋势分析
@docs/DATA_ANALYTICS_INSIGHT_v1.0.md 实现MK-24趋势分析，集成新榜API，使用CG-04和CG-06能力

# 4. 实现竞品监控
@docs/DATA_ANALYTICS_INSIGHT_v1.0.md 实现MK-25竞品监控，集成飞瓜数据API，使用WEB-02和CG-01能力

# 5. 实现智能建议
@docs/DATA_ANALYTICS_INSIGHT_v1.0.md 实现MK-26智能建议，使用CG-01推理和LN-01反馈学习
```

## 八、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，5项数据分析功能，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**