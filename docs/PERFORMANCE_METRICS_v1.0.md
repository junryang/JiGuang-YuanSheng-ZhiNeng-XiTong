# 性能指标规范 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\PERFORMANCE_METRICS_v1.0.md
```


# 性能指标规范 v1.0

## 一、性能总览

```yaml
module: "性能指标规范"
description: "营销中心各功能模块的性能指标定义和验收标准"
priority: "P0"
domain: "营销中心"

# 关联的通用能力
related_abilities:
  - "EX-01: 代码生成"
  - "EX-03: API调用"
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"
  - "EX-11: 定时执行"
  - "EX-12: 批量执行"
  - "EM-06: 并发配额感知"
  - "EM-07: 并发队列管理"
  - "EM-08: 智能请求调度"
  - "EM-09: 动态并发调整"
  - "EM-10: 多模型并发分担"
  - "SC-06: 速率限制"

metrics:
  total_count: 4
  categories:
    - "内容生成性能"
    - "多平台分发性能"
    - "项目匹配性能"
    - "数据看板性能"
```


## 二、性能指标详细定义

### 2.1 单篇文章生成时间

```yaml
# 单篇文章生成时间性能指标
metric_id: "PERF-01"
name: "单篇文章生成时间"
description: "从输入主题到生成完整文章的总耗时"
target_value: "P95 ≤ 180秒，单次 ≤ 300秒"
unit: "seconds"
priority: "P0"

# 指标定义
definition:
  start_point: "API收到生成请求"
  end_point: "API返回完整生成内容"
  measurement: "end_time - start_time"
  
# 测试条件
test_conditions:
  article_length: "1500字"
  language: "中文"
  model: "DeepSeek-V3"
  concurrent_requests: 1
  
# 性能分层
performance_tiers:
  excellent: "< 60秒"
  good: "60-120秒"
  acceptable: "120-180秒"
  poor: "> 180秒"
  
# SLA承诺
sla:
  p50: "< 90秒"
  p95: "< 150秒"
  p99: "< 180秒"
  availability: "99.5%"

# 监控配置
monitoring:
  metrics:
    - name: "generation_duration_seconds"
      type: "histogram"
      buckets: [30, 60, 90, 120, 150, 180, 240, 300]
      
    - name: "generation_requests_total"
      type: "counter"
      
    - name: "generation_errors_total"
      type: "counter"
      
  alerts:
    - name: "GenerationSlow"
      condition: "generation_duration_seconds > 180"
      severity: "warning"
      message: "文章生成时间超过3分钟"
      
    - name: "GenerationTimeout"
      condition: "generation_duration_seconds > 300"
      severity: "critical"
      message: "文章生成超时"

# 实现示例
class GenerationPerformanceMonitor:
    """生成性能监控器 - 对齐EX-01代码生成、EX-10异步执行"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.timer = Timer()
    
    async def measure_generation_time(self, topic: str) -> PerformanceResult:
        """测量生成时间 - 对齐EX-01"""
        start_time = datetime.now()
        
        # 执行生成（对齐EX-01）
        result = await self._generate_article(topic)
        
        # 计算耗时
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 记录指标
        await self.metrics_collector.record(
            metric="generation_duration_seconds",
            value=elapsed,
            labels={
                "topic_length": len(topic),
                "model": "deepseek-v3"
            }
        )
        
        # 判断是否达标
        passed = elapsed <= 180  # 3分钟
        
        return PerformanceResult(
            metric="generation_time",
            value=elapsed,
            target=180,
            passed=passed,
            details={
                "topic": topic,
                "content_length": len(result.content),
                "model": result.model
            }
        )
```

### 2.2 多平台分发完成时间

```yaml
# 多平台分发完成时间性能指标
metric_id: "PERF-02"
name: "多平台分发完成时间"
description: "从提交发布请求到所有目标平台发布完成的总耗时"
target_value: "< 5分钟（10个平台）"
unit: "seconds"
priority: "P0"

# 指标定义
definition:
  start_point: "API收到分发请求"
  end_point: "所有平台返回发布成功确认"
  measurement: "end_time - start_time"
  
# 测试条件
test_conditions:
  platform_count: 10
  content_type: "图文"
  concurrent_execution: true
  
# 性能分层
performance_tiers:
  excellent: "< 120秒"
  good: "120-240秒"
  acceptable: "240-300秒"
  poor: "> 300秒"
  
# SLA承诺
sla:
  p50: "< 180秒"
  p95: "< 240秒"
  p99: "< 300秒"
  availability: "99%"

# 监控配置
monitoring:
  metrics:
    - name: "distribution_duration_seconds"
      type: "histogram"
      buckets: [60, 120, 180, 240, 300, 360, 480, 600]
      
    - name: "distribution_platform_duration_seconds"
      type: "histogram"
      buckets: [10, 20, 30, 60, 90, 120]
      
    - name: "distribution_success_rate"
      type: "gauge"
      
  alerts:
    - name: "DistributionSlow"
      condition: "distribution_duration_seconds > 300"
      severity: "warning"
      message: "多平台分发时间超过5分钟"
      
    - name: "DistributionFailed"
      condition: "distribution_success_rate < 0.9"
      severity: "critical"
      message: "分发成功率低于90%"

# 实现示例
class DistributionPerformanceMonitor:
    """分发性能监控器 - 对齐EX-09并行执行、EX-12批量执行"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.distributor = DomesticDistributor()
    
    async def measure_distribution_time(self, content: str, 
                                         platforms: List[str]) -> PerformanceResult:
        """测量分发时间 - 对齐EX-09"""
        start_time = datetime.now()
        
        # 执行批量分发（对齐EX-09、EX-12）
        results = await self.distributor.batch_publish(content, platforms)
        
        # 计算耗时
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 统计各平台耗时
        platform_durations = {}
        for result in results:
            platform_durations[result.platform] = result.duration_ms / 1000
        
        # 记录指标
        await self.metrics_collector.record(
            metric="distribution_duration_seconds",
            value=elapsed,
            labels={
                "platform_count": len(platforms),
                "success_count": sum(1 for r in results if r.success)
            }
        )
        
        # 判断是否达标（10个平台 < 5分钟）
        expected_target = 180 if len(platforms) <= 5 else 300
        passed = elapsed <= expected_target
        
        return PerformanceResult(
            metric="distribution_time",
            value=elapsed,
            target=expected_target,
            passed=passed,
            details={
                "platform_count": len(platforms),
                "success_count": sum(1 for r in results if r.success),
                "platform_durations": platform_durations,
                "slowest_platform": max(platform_durations, key=platform_durations.get)
            }
        )
```

### 2.3 项目匹配响应时间

```yaml
# 项目匹配响应时间性能指标
metric_id: "PERF-03"
name: "项目匹配响应时间"
description: "从提交匹配请求到返回匹配结果的总耗时"
target_value: "< 10秒"
unit: "seconds"
priority: "P1"

# 指标定义
definition:
  start_point: "API收到匹配请求"
  end_point: "API返回匹配结果列表"
  measurement: "end_time - start_time"
  
# 测试条件
test_conditions:
  project_pool_size: "1000个项目"
  skills_count: "5个技能"
  concurrent_requests: 10
  
# 性能分层
performance_tiers:
  excellent: "< 3秒"
  good: "3-6秒"
  acceptable: "6-10秒"
  poor: "> 10秒"
  
# SLA承诺
sla:
  p50: "< 5秒"
  p95: "< 8秒"
  p99: "< 10秒"
  availability: "99.5%"

# 监控配置
monitoring:
  metrics:
    - name: "matching_duration_seconds"
      type: "histogram"
      buckets: [1, 2, 3, 5, 8, 10, 15, 20]
      
    - name: "matching_projects_scanned"
      type: "histogram"
      buckets: [100, 500, 1000, 5000]
      
    - name: "matching_cache_hit_rate"
      type: "gauge"
      
  alerts:
    - name: "MatchingSlow"
      condition: "matching_duration_seconds > 10"
      severity: "warning"
      message: "项目匹配响应时间超过10秒"
      
    - name: "MatchingCacheMissHigh"
      condition: "matching_cache_hit_rate < 0.5"
      severity: "info"
      message: "匹配缓存命中率低于50%"

# 实现示例
class MatchingPerformanceMonitor:
    """匹配性能监控器 - 对齐EM-04模型缓存、EM-06并发配额感知"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.cache_manager = CacheManager()  # 对齐EM-04
        self.quota_manager = QuotaManager()  # 对齐EM-06
    
    async def measure_matching_time(self, skills: List[str]) -> PerformanceResult:
        """测量匹配时间 - 对齐EM-04"""
        start_time = datetime.now()
        
        # 检查缓存（对齐EM-04）
        cache_key = f"match:{hash(tuple(sorted(skills)))}"
        cached_result = await self.cache_manager.get(cache_key)
        
        if cached_result:
            # 缓存命中
            elapsed = (datetime.now() - start_time).total_seconds()
            return PerformanceResult(
                metric="matching_time",
                value=elapsed,
                target=10,
                passed=True,
                details={
                    "cache_hit": True,
                    "cached_result_count": len(cached_result)
                }
            )
        
        # 执行匹配（对齐EM-06）
        result = await self._perform_matching(skills)
        
        # 计算耗时
        elapsed = (datetime.now() - start_time).total_seconds()
        
        # 缓存结果（对齐EM-04）
        await self.cache_manager.set(cache_key, result, ttl=300)  # 5分钟
        
        # 记录指标
        await self.metrics_collector.record(
            metric="matching_duration_seconds",
            value=elapsed,
            labels={
                "skills_count": len(skills),
                "cache_hit": False
            }
        )
        
        # 判断是否达标
        passed = elapsed <= 10
        
        return PerformanceResult(
            metric="matching_time",
            value=elapsed,
            target=10,
            passed=passed,
            details={
                "skills": skills,
                "result_count": len(result),
                "cache_hit": False
            }
        )
```

### 2.4 数据看板刷新延迟

```yaml
# 数据看板刷新延迟性能指标
metric_id: "PERF-04"
name: "数据看板刷新延迟"
description: "从数据源更新到看板显示最新数据的时间差"
target_value: "< 1分钟"
unit: "seconds"
priority: "P0"

# 指标定义
definition:
  start_point: "数据源数据更新时间"
  end_point: "看板UI刷新完成时间"
  measurement: "end_time - start_point"
  
# 测试条件
test_conditions:
  data_sources: 5个平台
  metrics_count: 10个指标
  concurrent_users: 50
  
# 性能分层
performance_tiers:
  excellent: "< 15秒"
  good: "15-30秒"
  acceptable: "30-60秒"
  poor: "> 60秒"
  
# SLA承诺
sla:
  p50: "< 30秒"
  p95: "< 45秒"
  p99: "< 60秒"
  availability: "99.5%"

# 监控配置
monitoring:
  metrics:
    - name: "dashboard_refresh_delay_seconds"
      type: "histogram"
      buckets: [5, 10, 15, 30, 45, 60, 90, 120]
      
    - name: "dashboard_data_age_seconds"
      type: "gauge"
      
    - name: "dashboard_api_response_time"
      type: "histogram"
      buckets: [0.5, 1, 2, 5, 10, 20]
      
  alerts:
    - name: "DashboardStale"
      condition: "dashboard_data_age_seconds > 60"
      severity: "warning"
      message: "看板数据超过1分钟未更新"
      
    - name: "DashboardRefreshSlow"
      condition: "dashboard_refresh_delay_seconds > 60"
      severity: "critical"
      message: "看板刷新延迟超过1分钟"

# 实现示例
class DashboardPerformanceMonitor:
    """看板性能监控器 - 对齐EX-03 API调用、EX-09并行执行"""
    
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.data_fetcher = DataFetcher()
        self.cache_manager = CacheManager()
    
    async def measure_refresh_delay(self, platforms: List[str]) -> PerformanceResult:
        """测量刷新延迟 - 对齐EX-09"""
        # 记录数据源时间
        source_timestamps = await self._get_source_timestamps(platforms)
        source_time = max(source_timestamps.values())
        
        start_time = datetime.now()
        
        # 并行获取数据（对齐EX-09）
        tasks = [self._fetch_platform_data(p) for p in platforms]
        results = await asyncio.gather(*tasks)
        
        # 更新缓存
        await self.cache_manager.set("dashboard_data", results, ttl=60)
        
        # 计算刷新延迟
        refresh_time = datetime.now()
        delay = (refresh_time - source_time).total_seconds()
        
        # 记录指标
        await self.metrics_collector.record(
            metric="dashboard_refresh_delay_seconds",
            value=delay,
            labels={
                "platform_count": len(platforms),
                "data_sources": ",".join(platforms)
            }
        )
        
        # 判断是否达标
        passed = delay <= 60
        
        return PerformanceResult(
            metric="dashboard_refresh_delay",
            value=delay,
            target=60,
            passed=passed,
            details={
                "platforms": platforms,
                "source_timestamps": source_timestamps,
                "source_time": source_time,
                "refresh_time": refresh_time,
                "delay_seconds": delay,
                "data_age": await self._get_data_age()
            }
        )
    
    async def _get_source_timestamps(self, platforms: List[str]) -> Dict[str, datetime]:
        """获取各数据源最新时间戳"""
        timestamps = {}
        for platform in platforms:
            latest_data = await self.data_fetcher.get_latest(platform)
            timestamps[platform] = latest_data.timestamp
        return timestamps
```


## 三、性能测试配置

```yaml
# 性能测试配置

performance_test_config:
  # 负载测试
  load_test:
    duration: "10分钟"
    concurrency:
      start: 1
      end: 100
      step: 10
    ramp_up: "2分钟"
    
  # 压力测试
  stress_test:
    duration: "5分钟"
    concurrency: 200
    spike: true
    
  # 稳定性测试
  stability_test:
    duration: "2小时"
    concurrency: 50
    acceptable_error_rate: "0.1%"
    
  # 峰值测试
  peak_test:
    duration: "1分钟"
    concurrency: 500
    expected_response: "限流保护"

# 测试场景
test_scenarios:
  - name: "正常负载"
    concurrency: 10
    duration: "10分钟"
    expected_p95: "< 目标值"
    
  - name: "高负载"
    concurrency: 50
    duration: "10分钟"
    expected_p95: "< 目标值 * 1.5"
    
  - name: "峰值负载"
    concurrency: 100
    duration: "5分钟"
    expected_p95: "< 目标值 * 2"
```


## 四、性能基准数据

```yaml
# 性能基准数据

performance_baselines:
  generation:
    empty_prompt: "2秒"
    short_prompt_100: "30秒"
    medium_prompt_500: "90秒"
    long_prompt_1500: "150秒"
    
  distribution:
    single_platform: "10秒"
    three_platforms: "30秒"
    five_platforms: "60秒"
    ten_platforms: "120秒"
    
  matching:
    small_pool_100: "1秒"
    medium_pool_1000: "3秒"
    large_pool_10000: "8秒"
    
  dashboard:
    single_platform: "5秒"
    three_platforms: "15秒"
    five_platforms: "25秒"
```


## 五、性能监控仪表盘

```yaml
# 性能监控仪表盘配置

performance_dashboard:
  panels:
    - title: "API响应时间"
      metrics:
        - "generation_duration_seconds"
        - "distribution_duration_seconds"
        - "matching_duration_seconds"
        - "dashboard_refresh_delay_seconds"
      visualization: "line_chart"
      time_range: "last_1_hour"
      
    - title: "P95响应时间趋势"
      metrics:
        - "p95_generation_time"
        - "p95_distribution_time"
        - "p95_matching_time"
      visualization: "area_chart"
      time_range: "last_24_hours"
      
    - title: "错误率"
      metrics:
        - "generation_error_rate"
        - "distribution_error_rate"
        - "matching_error_rate"
      visualization: "gauge"
      thresholds:
        warning: 1
        critical: 5
        
    - title: "系统吞吐量"
      metrics:
        - "requests_per_second"
        - "concurrent_requests"
      visualization: "line_chart"
      time_range: "last_1_hour"
```


## 六、在Cursor中使用

```bash
# 1. 运行文章生成性能测试
@docs/PERFORMANCE_METRICS_v1.0.md 运行PERF-01文章生成性能测试，验证生成时间<3分钟

# 2. 运行多平台分发性能测试
@docs/PERFORMANCE_METRICS_v1.0.md 运行PERF-02多平台分发性能测试，验证10个平台<5分钟

# 3. 运行项目匹配性能测试
@docs/PERFORMANCE_METRICS_v1.0.md 运行PERF-03项目匹配性能测试，验证响应时间<10秒

# 4. 运行数据看板刷新延迟测试
@docs/PERFORMANCE_METRICS_v1.0.md 运行PERF-04数据看板刷新延迟测试，验证延迟<1分钟

# 5. 运行完整性能测试套件
@docs/PERFORMANCE_METRICS_v1.0.md 运行所有性能指标测试，生成性能报告
```


## 七、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，4项性能指标定义，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**