# 接单与变现能力 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\ORDER_REVENUE_CAPABILITY_v1.0.md
```


# 接单与变现能力 v1.0

## 一、能力总览

```yaml
module: "接单与变现"
description: "支持从技术接单平台自动筛选项目、生成报价、辅助沟通、统计收益"
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
  - "DC-07: 方案对比"
  - "DC-08: 风险评估"
  - "DC-11: 成本效益分析"
  - "EX-03: API调用"
  - "EX-08: 消息发送"
  - "EX-09: 并行执行"
  - "EX-12: 批量执行"
  - "WEB-02: 搜索引擎查询"
  - "WEB-03: 网页内容解析"
  - "WEB-04: API调用与集成"
  - "WEB-05: 社交媒体交互"
  - "EM-01: 多模型路由"
  - "EM-04: 模型缓存"
  - "QL-02: 输出置信度评估"
  - "QL-05: 质量验证"
  - "AGENT-RUNTIME-09: 长期价值评估"

functions:
  total_count: 4
  categories:
    - "项目匹配"
    - "报价管理"
    - "沟通辅助"
    - "收益统计"
```


## 二、接单平台配置

```yaml
# 支持的接单平台
platforms:
  domestic:
    - id: "proginn"
      name: "程序员客栈"
      api_type: "official"
      priority: "P0"
      features: ["项目自动抓取", "技能匹配筛选", "报价参考", "接单申请提交"]
      
    - id: "mashangda"
      name: "码上达"
      api_type: "webhook"
      priority: "P0"
      features: ["碎片化任务匹配", "新手友好筛选", "快速报价"]
      
    - id: "coding_mart"
      name: "码市"
      api_type: "official"
      priority: "P1"
      features: ["团队项目匹配", "团队能力展示", "协作报价"]
      
    - id: "shixian"
      name: "实现网"
      api_type: "webhook"
      priority: "P1"
      features: ["企业级项目筛选", "驻场/远程筛选"]
      
    - id: "chengjubao"
      name: "程聚宝"
      api_type: "webhook"
      priority: "P1"
      features: ["高质量项目筛选", "长期合作匹配"]
      
    - id: "zbj"
      name: "猪八戒网"
      api_type: "manual"
      priority: "P2"
      features: ["综合类目筛选", "竞标分析"]
      
  international:
    - id: "upwork"
      name: "Upwork"
      api_type: "official"
      priority: "P1"
      features: ["全球项目匹配", "时区适配", "英语能力评估"]
      
    - id: "toptal"
      name: "Toptal"
      api_type: "manual"
      priority: "P2"
      features: ["高端项目匹配", "严格筛选流程"]
      
    - id: "fiverr"
      name: "Fiverr"
      api_type: "official"
      priority: "P2"
      features: ["服务商品化", "标准化报价", "快速成交"]
      
    - id: "gunio"
      name: "Gun.io"
      api_type: "manual"
      priority: "P2"
      features: ["高品质兼职", "技术筛选"]
      
    - id: "remoteok"
      name: "RemoteOK"
      api_type: "webhook"
      priority: "P2"
      features: ["远程工作匹配", "全职/兼职筛选"]
```


## 三、功能详细设计

### 3.1 MK-14 项目筛选

```yaml
# MK-14 项目筛选
function_id: "MK-14"
name: "项目筛选"
description: "自动从各平台抓取项目并匹配智能体技能，自动筛选匹配技术栈的项目"
priority: "P1"
implementation: "自研 + 平台API"
related_abilities: ["PC-01", "PC-02", "CG-01", "WEB-02", "WEB-03", "WEB-04", "EX-09", "EM-01"]

# 数据模型
class PlatformProject:
    id: str
    platform_id: str
    platform_name: str
    external_id: str
    title: str
    description: str
    budget_min: float
    budget_max: float
    budget_currency: str
    skills: List[str]
    experience_level: str  # junior, middle, senior
    project_type: str  # full_time, part_time, fixed
    duration_days: int
    status: str  # open, closed, awarded
    posted_at: datetime
    url: str
    match_score: Optional[float]
    match_reason: Optional[str]

class MatchResult:
    project: PlatformProject
    score: float  # 0-100
    reason: str
    matched_skills: List[str]
    missing_skills: List[str]
    confidence: float

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/projects/matched"
    description: "获取匹配的项目列表"
    query_params:
      platforms: "List[str]"
      min_score: "float"
      limit: "int"
    response:
      projects: "List[MatchResult]"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/projects/sync"
    description: "手动触发项目同步"
    response:
      synced_count: "int"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/projects/{project_id}/match-score"
    description: "计算项目匹配分数"
    response:
      match_result: "MatchResult"

# 实现示例
class ProjectMatcher:
    """项目匹配器 - 对齐PC-01自然语言理解、PC-02代码理解、CG-01推理能力"""
    
    def __init__(self):
        self.platform_apis = {
            "proginn": ProginnAPI(),
            "mashangda": MashangdaAPI(),
            "upwork": UpworkAPI()
        }
        self.skill_extractor = SkillExtractor()  # 对齐PC-02
        self.model_router = ModelRouter()  # 对齐EM-01
    
    async def fetch_and_match(self, agent_skills: List[str], 
                               platforms: List[str] = None) -> List[MatchResult]:
        """获取并匹配项目 - 使用并行执行（EX-09）"""
        if not platforms:
            platforms = list(self.platform_apis.keys())
        
        # 并行获取各平台项目（对齐EX-09）
        tasks = [self._fetch_platform_projects(p) for p in platforms]
        all_projects = []
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, list):
                all_projects.extend(result)
        
        # 并行计算匹配分数
        match_tasks = [self._calculate_match_score(p, agent_skills) for p in all_projects]
        match_results = await asyncio.gather(*match_tasks)
        
        # 按分数排序
        sorted_results = sorted(match_results, key=lambda x: x.score, reverse=True)
        
        return sorted_results
    
    async def _fetch_platform_projects(self, platform: str) -> List[PlatformProject]:
        """获取平台项目 - 对齐WEB-04 API调用"""
        api = self.platform_apis.get(platform)
        if not api:
            return []
        
        try:
            # 调用平台API（对齐WEB-04）
            raw_projects = await api.fetch_projects()
            return [self._convert_to_standard(p, platform) for p in raw_projects]
        except Exception as e:
            print(f"Failed to fetch from {platform}: {e}")
            return []
    
    async def _calculate_match_score(self, project: PlatformProject, 
                                      agent_skills: List[str]) -> MatchResult:
        """计算匹配分数 - 对齐PC-01、PC-02、CG-01"""
        # 1. 提取项目所需技能（对齐PC-02）
        project_skills = await self.skill_extractor.extract_from_description(
            project.description, project.title
        )
        
        # 2. 技能匹配计算（对齐CG-01推理）
        matched = set(project_skills) & set(agent_skills)
        missing = set(project_skills) - set(agent_skills)
        
        skill_score = len(matched) / len(project_skills) if project_skills else 0
        
        # 3. 经验匹配（对齐PC-01）
        experience_match = await self._match_experience(project.experience_level, agent_skills)
        
        # 4. 预算匹配
        budget_score = self._budget_match(project.budget_min, project.budget_max)
        
        # 5. 时间匹配
        time_score = self._time_match(project.duration_days)
        
        # 6. 综合得分
        total_score = (
            skill_score * 0.4 +
            experience_match * 0.25 +
            budget_score * 0.2 +
            time_score * 0.15
        ) * 100
        
        # 7. 生成匹配原因（对齐CG-01）
        reason = self._generate_match_reason(matched, missing, total_score)
        
        return MatchResult(
            project=project,
            score=round(total_score, 1),
            reason=reason,
            matched_skills=list(matched),
            missing_skills=list(missing),
            confidence=0.85 if skill_score > 0.6 else 0.6
        )
```

### 3.2 MK-15 报价生成

```yaml
# MK-15 报价生成
function_id: "MK-15"
name: "报价生成"
description: "基于项目需求自动生成报价方案，支持固定价格和按小时报价"
priority: "P1"
implementation: "自研"
related_abilities: ["CG-04", "DC-06", "DC-07", "DC-08", "DC-11", "AGENT-RUNTIME-09", "QL-02"]

# 数据模型
class QuoteProposal:
    id: str
    project_id: str
    project_name: str
    quote_type: str  # fixed, hourly
    amount: float
    currency: str
    hourly_rate: Optional[float]
    estimated_hours: Optional[int]
    timeline_days: int
    breakdown: List[QuoteItem]
    assumptions: List[str]
    exclusions: List[str]
    risk_factors: List[RiskFactor]
    confidence: float
    generated_at: datetime

class QuoteItem:
    name: str
    description: str
    amount: float
    hours: Optional[int]

class RiskFactor:
    description: str
    probability: float  # 0-1
    impact: str  # low, medium, high
    mitigation: str

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/quote/generate"
    description: "生成报价方案"
    request_body:
      project_id: "str"
      quote_type: "str"  # fixed, hourly
      options: "dict"
    response:
      proposals: "List[QuoteProposal]"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/quote/compare"
    description: "对比多个报价方案"
    request_body:
      proposal_ids: "List[str]"
    response:
      comparison: "dict"

# 实现示例
class QuoteGenerator:
    """报价生成器 - 对齐DC-06方案生成、DC-07方案对比、DC-08风险评估"""
    
    def __init__(self):
        self.hourly_rates = {
            "junior": 50,
            "middle": 100,
            "senior": 200,
            "expert": 400
        }
        self.risk_assessor = RiskAssessor()  # 对齐DC-08
        self.value_evaluator = LongTermValueEstimator()  # 对齐AGENT-RUNTIME-09
    
    async def generate_quote(self, project: PlatformProject, 
                              quote_type: str = "fixed",
                              agent_level: str = "senior") -> QuoteProposal:
        """生成报价方案 - 对齐DC-06方案生成"""
        # 1. 估算工作量（对齐CG-04数值推理）
        estimated_hours = await self._estimate_workload(project)
        
        # 2. 获取小时费率
        hourly_rate = self.hourly_rates.get(agent_level, 100)
        
        # 3. 计算基础报价（对齐DC-11成本效益分析）
        base_amount = estimated_hours * hourly_rate
        
        # 4. 复杂度系数
        complexity_factor = await self._calculate_complexity_factor(project)
        
        # 5. 紧急度系数
        urgency_factor = self._calculate_urgency_factor(project)
        
        # 6. 长期合作折扣（对齐AGENT-RUNTIME-09）
        long_term_discount = await self.value_evaluator.get_long_term_value(project.client_id)
        
        # 7. 最终报价
        final_amount = base_amount * complexity_factor * urgency_factor * (1 - long_term_discount)
        
        # 8. 风险评估（对齐DC-08）
        risks = await self.risk_assessor.assess(project)
        
        # 9. 报价明细
        breakdown = self._create_breakdown(estimated_hours, hourly_rate, complexity_factor)
        
        # 10. 置信度评估（对齐QL-02）
        confidence = self._calculate_confidence(project, estimated_hours, risks)
        
        return QuoteProposal(
            id=self._generate_id(),
            project_id=project.id,
            project_name=project.title,
            quote_type=quote_type,
            amount=round(final_amount, 2),
            currency=project.budget_currency or "CNY",
            hourly_rate=hourly_rate,
            estimated_hours=estimated_hours,
            timeline_days=self._estimate_timeline(estimated_hours),
            breakdown=breakdown,
            assumptions=self._generate_assumptions(project),
            exclusions=self._generate_exclusions(project),
            risk_factors=risks,
            confidence=confidence,
            generated_at=datetime.now()
        )
    
    async def compare_quotes(self, proposals: List[QuoteProposal]) -> dict:
        """对比报价方案 - 对齐DC-07方案对比"""
        comparison = {
            "best_value": None,
            "best_price": None,
            "best_timeline": None,
            "details": []
        }
        
        for prop in proposals:
            # 计算性价比
            value_score = prop.amount / prop.timeline_days
            
            comparison["details"].append({
                "id": prop.id,
                "amount": prop.amount,
                "timeline_days": prop.timeline_days,
                "value_score": value_score,
                "confidence": prop.confidence,
                "risk_count": len(prop.risk_factors)
            })
        
        # 找出最优
        comparison["best_value"] = min(comparison["details"], key=lambda x: x["value_score"])
        comparison["best_price"] = min(comparison["details"], key=lambda x: x["amount"])
        comparison["best_timeline"] = min(comparison["details"], key=lambda x: x["timeline_days"])
        
        return comparison
```

### 3.3 MK-16 接单辅助

```yaml
# MK-16 接单辅助
function_id: "MK-16"
name: "接单辅助"
description: "辅助撰写接单申请、沟通话术，提供模板和智能建议"
priority: "P2"
implementation: "自研"
related_abilities: ["PC-01", "CG-01", "DC-06", "EX-08", "WEB-05", "QL-02"]

# 数据模型
class ApplicationDraft:
    id: str
    project_id: str
    project_name: str
    cover_letter: str
    questions: List[str]
    portfolio_items: List[str]
    availability: str
    rate_expectation: str
    confidence: float
    generated_at: datetime

class CommunicationSuggestion:
    scenario: str  # initial_contact, price_negotiation, progress_update, issue_resolution
    suggested_message: str
    key_points: List[str]
    tone: str  # professional, friendly, urgent
    confidence: float

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/marketing/application/generate"
    description: "生成接单申请"
    request_body:
      project_id: "str"
      quote_id: "str"
      portfolio_ids: "List[str]"
    response:
      application: "ApplicationDraft"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/communication/suggest"
    description: "生成沟通建议"
    request_body:
      context: "str"
      scenario: "str"
    response:
      suggestion: "CommunicationSuggestion"

# 实现示例
class ApplicationAssistant:
    """接单助手 - 对齐PC-01自然语言理解、CG-01推理能力"""
    
    def __init__(self):
        self.template_engine = TemplateEngine()
        self.communication_analyzer = CommunicationAnalyzer()  # 对齐PC-01
    
    async def generate_application(self, project: PlatformProject, 
                                    quote: QuoteProposal,
                                    agent_profile: dict) -> ApplicationDraft:
        """生成接单申请 - 对齐DC-06方案生成"""
        # 1. 分析项目需求（对齐PC-01）
        key_requirements = await self._extract_key_requirements(project.description)
        
        # 2. 匹配个人优势（对齐CG-01）
        advantages = await self._match_advantages(project, agent_profile)
        
        # 3. 生成求职信
        cover_letter = await self.template_engine.render("application", {
            "project_name": project.title,
            "key_requirements": key_requirements,
            "advantages": advantages,
            "relevant_experience": agent_profile.get("experience", []),
            "quote_amount": quote.amount,
            "timeline": quote.timeline_days
        })
        
        # 4. 生成待确认问题
        questions = await self._generate_clarifying_questions(project)
        
        # 5. 置信度评估（对齐QL-02）
        confidence = self._calculate_application_confidence(project, agent_profile)
        
        return ApplicationDraft(
            id=self._generate_id(),
            project_id=project.id,
            project_name=project.title,
            cover_letter=cover_letter,
            questions=questions,
            portfolio_items=agent_profile.get("portfolio", []),
            availability=agent_profile.get("availability", "full_time"),
            rate_expectation=f"¥{quote.amount}",
            confidence=confidence,
            generated_at=datetime.now()
        )
    
    async def suggest_response(self, message: str, scenario: str) -> CommunicationSuggestion:
        """建议回复 - 对齐PC-01、CG-01"""
        # 分析消息意图（对齐PC-01）
        intent = await self.communication_analyzer.analyze_intent(message)
        
        # 分析情感（对齐PC-01）
        sentiment = await self.communication_analyzer.analyze_sentiment(message)
        
        # 根据场景生成回复（对齐CG-01）
        if scenario == "initial_contact":
            suggested = await self._generate_initial_response(intent, sentiment)
            tone = "professional"
        elif scenario == "price_negotiation":
            suggested = await self._generate_negotiation_response(intent, sentiment)
            tone = "friendly"
        elif scenario == "issue_resolution":
            suggested = await self._generate_issue_response(intent, sentiment)
            tone = "empathetic"
        else:
            suggested = await self._generate_general_response(intent, sentiment)
            tone = "neutral"
        
        return CommunicationSuggestion(
            scenario=scenario,
            suggested_message=suggested,
            key_points=self._extract_key_points(suggested),
            tone=tone,
            confidence=0.85
        )
```

### 3.4 MK-17 收益统计

```yaml
# MK-17 收益统计
function_id: "MK-17"
name: "收益统计"
description: "统计各平台收益，提供收入分析、趋势预测、报表导出"
priority: "P2"
implementation: "自研"
related_abilities: ["CG-04", "EX-03", "EX-09", "EX-12", "WEB-04"]

# 数据模型
class RevenueRecord:
    id: str
    platform: str
    project_id: str
    project_name: str
    amount: float
    currency: str
    status: str  # pending, paid, failed
    order_date: datetime
    paid_date: Optional[datetime]
    fee: float  # 平台手续费
    net_amount: float

class RevenueStats:
    period: str  # day, week, month, year, all
    total_revenue: float
    total_orders: int
    avg_order_value: float
    platform_breakdown: Dict[str, float]
    monthly_trend: List[dict]
    projected_next_month: float
    growth_rate: float

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/marketing/revenue/stats"
    description: "获取收益统计"
    query_params:
      period: "str"
      platforms: "List[str]"
      start_date: "date"
      end_date: "date"
    response:
      stats: "RevenueStats"
      
  - method: "GET"
    endpoint: "/api/v1/marketing/revenue/records"
    description: "获取收益记录"
    query_params:
      page: "int"
      page_size: "int"
      status: "str"
    response:
      records: "List[RevenueRecord]"
      pagination: "dict"
      
  - method: "POST"
    endpoint: "/api/v1/marketing/revenue/export"
    description: "导出收益报表"
    request_body:
      format: "str"  # csv, excel, pdf
      period: "str"
    response:
      file_url: "str"

# 实现示例
class RevenueTracker:
    """收益追踪器 - 对齐CG-04数值推理、EX-03 API调用"""
    
    def __init__(self):
        self.platform_apis = {
            "proginn": ProginnAPI(),
            "upwork": UpworkAPI()
        }
    
    async def sync_revenue(self, platforms: List[str] = None) -> int:
        """同步各平台收益 - 使用并行执行（EX-09）"""
        if not platforms:
            platforms = list(self.platform_apis.keys())
        
        # 并行获取各平台收益（对齐EX-09）
        tasks = [self._fetch_platform_revenue(p) for p in platforms]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_synced = 0
        for result in results:
            if isinstance(result, list):
                for record in result:
                    await self._save_revenue_record(record)
                    total_synced += 1
        
        return total_synced
    
    async def get_stats(self, period: str = "month", 
                        platforms: List[str] = None) -> RevenueStats:
        """获取收益统计 - 对齐CG-04数值推理"""
        # 构建查询
        query = self._build_period_query(period)
        if platforms:
            query["platform"] = {"$in": platforms}
        
        # 查询数据库
        records = await db.revenue_records.find(query).to_list()
        
        if not records:
            return self._empty_stats(period)
        
        # 计算统计指标（对齐CG-04）
        total_revenue = sum(r.net_amount for r in records)
        total_orders = len(records)
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # 平台分布
        platform_breakdown = {}
        for r in records:
            platform_breakdown[r.platform] = platform_breakdown.get(r.platform, 0) + r.net_amount
        
        # 月度趋势
        monthly_trend = self._calculate_monthly_trend(records)
        
        # 增长率
        growth_rate = self._calculate_growth_rate(monthly_trend)
        
        # 预测下月收入（对齐CG-04）
        projected = self._project_next_month(monthly_trend)
        
        return RevenueStats(
            period=period,
            total_revenue=round(total_revenue, 2),
            total_orders=total_orders,
            avg_order_value=round(avg_order_value, 2),
            platform_breakdown=platform_breakdown,
            monthly_trend=monthly_trend,
            projected_next_month=round(projected, 2),
            growth_rate=round(growth_rate, 1)
        )
    
    async def _fetch_platform_revenue(self, platform: str) -> List[RevenueRecord]:
        """获取平台收益 - 对齐EX-03 API调用"""
        api = self.platform_apis.get(platform)
        if not api:
            return []
        
        try:
            # 调用平台API（对齐EX-03）
            raw_records = await api.fetch_earnings()
            return [self._convert_to_revenue_record(r, platform) for r in raw_records]
        except Exception as e:
            print(f"Failed to fetch revenue from {platform}: {e}")
            return []
```

## 四、接单流程架构图

```yaml
architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           接单与变现流程                                    │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         项目发现层                                   │   │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │   │
  │  │  │程序员客栈  │  │  码上达   │  │  码市    │  │  Upwork   │        │   │
  │  │  │ API抓取   │  │ Webhook   │  │ API抓取  │  │ API抓取   │        │   │
  │  │  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         项目匹配层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 技能提取    │  │ 匹配计算    │  │ 排序筛选    │                  │   │
  │  │  │ (PC-02)     │  │ (CG-01)     │  │ (EX-09)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         报价决策层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 工作量估算  │  │ 风险评估    │  │ 方案对比    │                  │   │
  │  │  │ (CG-04)     │  │ (DC-08)     │  │ (DC-07)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         沟通执行层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 申请生成    │  │ 沟通建议    │  │ 消息发送    │                  │   │
  │  │  │ (DC-06)     │  │ (PC-01)     │  │ (EX-08)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         收益分析层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 数据同步    │  │ 统计分析    │  │ 报表导出    │                  │   │
  │  │  │ (EX-03)     │  │ (CG-04)     │  │ (EX-12)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```

## 五、通用能力映射表

```yaml
# 接单变现功能与通用能力映射
general_ability_mapping:
  PC-01_自然语言理解:
    mapped_functions: ["MK-14", "MK-16"]
    description: "分析项目需求、沟通意图"
    
  PC-02_代码理解:
    mapped_functions: ["MK-14"]
    description: "提取项目技术栈需求"
    
  CG-01_推理能力:
    mapped_functions: ["MK-14", "MK-16"]
    description: "匹配项目与技能、推理沟通策略"
    
  CG-04_数值推理:
    mapped_functions: ["MK-15", "MK-17"]
    description: "工作量估算、收益统计计算"
    
  DC-06_方案生成:
    mapped_functions: ["MK-15", "MK-16"]
    description: "生成报价方案、接单申请"
    
  DC-07_方案对比:
    mapped_functions: ["MK-15"]
    description: "对比不同报价方案"
    
  DC-08_风险评估:
    mapped_functions: ["MK-15"]
    description: "评估项目风险"
    
  DC-11_成本效益分析:
    mapped_functions: ["MK-15"]
    description: "成本计算和效益分析"
    
  EX-03_API调用:
    mapped_functions: ["MK-14", "MK-17"]
    description: "调用接单平台API"
    
  EX-08_消息发送:
    mapped_functions: ["MK-16"]
    description: "发送接单申请"
    
  EX-09_并行执行:
    mapped_functions: ["MK-14", "MK-17"]
    description: "并行抓取多平台项目"
    
  EX-12_批量执行:
    mapped_functions: ["MK-17"]
    description: "批量导出报表"
    
  WEB-04_API调用与集成:
    mapped_functions: ["MK-14", "MK-17"]
    description: "集成接单平台API"
    
  EM-01_多模型路由:
    mapped_functions: ["MK-14"]
    description: "选择最佳匹配算法"
    
  QL-02_输出置信度评估:
    mapped_functions: ["MK-15", "MK-16"]
    description: "评估报价和申请的置信度"
    
  AGENT-RUNTIME-09_长期价值评估:
    mapped_functions: ["MK-15"]
    description: "评估客户长期合作价值"
```

## 六、数据库表结构

```sql
-- 平台项目表
CREATE TABLE platform_projects (
    id UUID PRIMARY KEY,
    platform_id VARCHAR(50) NOT NULL,
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
    match_score DECIMAL(5,2),
    match_reason TEXT,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    UNIQUE(platform_id, external_id)
);

-- 报价方案表
CREATE TABLE quote_proposals (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES platform_projects(id),
    quote_type VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'CNY',
    hourly_rate DECIMAL(10,2),
    estimated_hours INTEGER,
    timeline_days INTEGER,
    breakdown JSONB,
    assumptions TEXT[],
    exclusions TEXT[],
    risk_factors JSONB,
    confidence DECIMAL(5,2),
    status VARCHAR(20) DEFAULT 'draft',
    submitted_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL
);

-- 接单申请记录表
CREATE TABLE applications (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES platform_projects(id),
    quote_id UUID REFERENCES quote_proposals(id),
    cover_letter TEXT,
    questions TEXT[],
    status VARCHAR(20) DEFAULT 'draft',
    submitted_at TIMESTAMP,
    response TEXT,
    created_at TIMESTAMP NOT NULL
);

-- 收益记录表
CREATE TABLE revenue_records (
    id UUID PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    project_id UUID REFERENCES platform_projects(id),
    project_name VARCHAR(500),
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'CNY',
    status VARCHAR(20) DEFAULT 'pending',
    fee DECIMAL(10,2),
    net_amount DECIMAL(10,2),
    order_date TIMESTAMP,
    paid_date TIMESTAMP,
    created_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_platform_projects_platform ON platform_projects(platform_id);
CREATE INDEX idx_platform_projects_status ON platform_projects(status);
CREATE INDEX idx_platform_projects_score ON platform_projects(match_score DESC);
CREATE INDEX idx_quote_proposals_project ON quote_proposals(project_id);
CREATE INDEX idx_revenue_records_platform ON revenue_records(platform);
CREATE INDEX idx_revenue_records_status ON revenue_records(status);
CREATE INDEX idx_revenue_records_order_date ON revenue_records(order_date);
```

## 七、在Cursor中使用

```bash
# 1. 实现项目筛选
@docs/ORDER_REVENUE_CAPABILITY_v1.0.md 实现MK-14项目筛选，集成程序员客栈和Upwork API，使用PC-02和CG-01能力

# 2. 实现报价生成
@docs/ORDER_REVENUE_CAPABILITY_v1.0.md 实现MK-15报价生成，使用CG-04数值推理和DC-08风险评估

# 3. 实现接单辅助
@docs/ORDER_REVENUE_CAPABILITY_v1.0.md 实现MK-16接单辅助，生成接单申请和沟通建议

# 4. 实现收益统计
@docs/ORDER_REVENUE_CAPABILITY_v1.0.md 实现MK-17收益统计，同步各平台收益并生成报表
```

## 八、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，4项接单变现功能，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**