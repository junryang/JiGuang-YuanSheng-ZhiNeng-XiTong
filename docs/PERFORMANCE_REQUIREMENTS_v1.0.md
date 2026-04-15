# 性能需求规范 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\PERFORMANCE_REQUIREMENTS_v1.0.md
```


# 性能需求规范 v1.0

## 一、概述

```yaml
module: "性能需求"
description: "定义系统的性能指标要求，包括响应时间、并发能力、可用性等"
priority: "P0"
domain: "非功能需求"

# 关联的通用能力
related_abilities:
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"
  - "EX-11: 定时执行"
  - "EX-12: 批量执行"
  - "SC-06: 速率限制"
  - "MT-01: 自我监控"
  - "MT-05: 能力扩展"
  - "MT-07: 资源配置"
  - "MT-09: 速度-质量权衡"
  - "PO-01: 响应时间优化"
  - "PO-02: 吞吐量优化"
  - "PO-03: 内存优化"
  - "PO-05: 批处理优化"
  - "EM-02: 模型负载均衡"
  - "EM-04: 模型缓存"
  - "EM-09: 动态并发调整"

performance_targets:
  total_count: 4
  categories:
    - "API响应时间"
    - "页面加载时间"
    - "并发能力"
    - "系统可用性"
```


## 二、性能指标详细设计

### 2.1 API响应时间

```yaml
# API响应时间要求
metric_id: "PERF-01"
name: "API响应时间"
description: "API接口从接收到请求到返回响应的总耗时。注意：普通查询/写入类以毫秒级为准；长耗时生成类（如 MK-01）以 `PERFORMANCE_METRICS_v1.0.md` 中 PERF-01/验收清单为准，勿与本节 CRUD 目标混用。"
target: "按 api_response_targets 分类；生成类长任务另见 PERFORMANCE_METRICS（MK-01：P95≤180s，单次≤300s）"
priority: "P0"
related_abilities: ["PO-01", "EM-04", "EX-09"]

# 按API类型细分
api_response_targets:
  - category: "查询类API"
    endpoints:
      - "GET /api/v1/agents"
      - "GET /api/v1/projects"
      - "GET /api/v1/tasks"
    p95_target: "200ms"
    p99_target: "300ms"
    optimization: ["PO-01", "EM-04"]
    
  - category: "写入类API"
    endpoints:
      - "POST /api/v1/agents"
      - "POST /api/v1/projects"
      - "PUT /api/v1/tasks/{id}"
    p95_target: "300ms"
    p99_target: "800ms"
    optimization: ["EX-09", "EX-10"]
    
  - category: "AI生成类API"
    endpoints:
      - "POST /api/v1/code/generate"
      - "POST /api/v1/chat/messages"
    p95_target: "5s"
    p99_target: "10s"
    optimization: ["EM-02", "EM-04", "EX-10"]
    note: "AI生成类API采用流式响应，首字返回应纳入“P95 ≤ 180秒，单次 ≤ 300秒”验收口径"
    
  - category: "批量操作API"
    endpoints:
      - "POST /api/v1/agents/batch"
      - "POST /api/v1/tasks/batch"
    p95_target: "5s"
    p99_target: "15s"
    optimization: ["EX-12", "EX-09"]

# 实现示例
class APIPerformanceOptimizer:
    """API性能优化器 - 对齐PO-01响应时间优化、EM-04模型缓存"""
    
    def __init__(self):
        self.cache_manager = CacheManager()  # 对齐EM-04
        self.parallel_executor = ParallelExecutor()  # 对齐EX-09
        self.batch_processor = BatchProcessor()  # 对齐EX-12
    
    async def optimize_query(self, query_func, cache_key: str, ttl: int = 300):
        """查询优化 - 使用缓存（对齐EM-04）"""
        # 检查缓存
        cached = await self.cache_manager.get(cache_key)
        if cached:
            return cached
        
        # 执行查询
        result = await query_func()
        
        # 缓存结果
        await self.cache_manager.set(cache_key, result, ttl=ttl)
        
        return result
    
    async def optimize_parallel(self, tasks: List[Callable], max_concurrent: int = 10):
        """并行优化 - 对齐EX-09并行执行"""
        return await self.parallel_executor.run(tasks, max_concurrent)
    
    async def optimize_batch(self, items: List, batch_func, batch_size: int = 100):
        """批量优化 - 对齐EX-12批量执行"""
        return await self.batch_processor.process(items, batch_func, batch_size)

# 监控配置
monitoring:
  metrics:
    - name: "api_latency_p95"
      type: "histogram"
      labels: ["endpoint", "method"]
      alert_threshold: 500
      alert_severity: "warning"
      
    - name: "api_latency_p99"
      type: "histogram"
      labels: ["endpoint", "method"]
      alert_threshold: 1000
      alert_severity: "critical"
      
    - name: "api_throughput"
      type: "counter"
      labels: ["endpoint", "method"]
      unit: "req/s"
```

### 2.2 页面加载时间

```yaml
# 页面加载时间要求
metric_id: "PERF-02"
name: "页面加载时间"
description: "前端页面从开始加载到完全可交互的时间"
target: "< 3秒"
priority: "P0"
related_abilities: ["PO-01", "EX-09"]

# 按页面类型细分
page_load_targets:
  - page: "首页/仪表盘"
    target_fcp: "1s"      # 首次内容绘制
    target_lcp: "2s"      # 最大内容绘制
    target_tti: "2.5s"    # 可交互时间
    optimization: ["代码分割", "懒加载", "CDN加速"]
    
  - page: "智能体列表"
    target_fcp: "800ms"
    target_lcp: "1.5s"
    target_tti: "2s"
    optimization: ["虚拟滚动", "分页加载"]
    
  - page: "项目详情"
    target_fcp: "1s"
    target_lcp: "2s"
    target_tti: "2.5s"
    optimization: ["骨架屏", "渐进式加载"]
    
  - page: "对话页面"
    target_fcp: "180s"
    target_lcp: "1.5s"
    target_tti: "2s"
    optimization: ["流式渲染", "消息虚拟滚动"]

# 前端性能优化配置
frontend_optimization:
  # 代码分割 - 对齐PO-01
  code_splitting:
    strategy: "route-based"
    chunks:
      - name: "vendor"
        min_size: "200KB"
      - name: "common"
        min_size: "100KB"
        
  # 懒加载 - 对齐PO-01
  lazy_loading:
    components: true
    images: true
    threshold: "200px"
    
  # 资源预加载
  preload:
    - type: "font"
      as: "font"
      crossorigin: true
    - type: "critical-css"
      as: "style"
      
  # 缓存策略 - 对齐EM-04
  caching:
    static_assets:
      ttl: "1年"
      strategy: "cache-first"
    api_responses:
      ttl: "5分钟"
      strategy: "network-first"

# 监控配置
monitoring:
  metrics:
    - name: "fcp"
      description: "First Contentful Paint"
      alert_threshold: 1000
      unit: "ms"
      
    - name: "lcp"
      description: "Largest Contentful Paint"
      alert_threshold: 2000
      unit: "ms"
      
    - name: "tti"
      description: "Time to Interactive"
      alert_threshold: 2500
      unit: "ms"
```

### 2.3 并发用户数

```yaml
# 并发用户数要求
metric_id: "PERF-03"
name: "并发用户数"
description: "系统能够同时支持的活跃用户数量"
target: "支持50个并发用户"
priority: "P0"
related_abilities: ["EX-09", "EM-02", "EM-09", "MT-07"]

# 并发能力细分
concurrency_targets:
  - scenario: "正常浏览"
    concurrent_users: 100
    response_time_p95: "180s"
    optimization: ["MT-07资源配置", "EX-09并行执行"]
    
  - scenario: "AI对话"
    concurrent_users: 50
    response_time_p95: "3s"
    optimization: ["EM-02负载均衡", "EM-09动态并发调整"]
    
  - scenario: "批量操作"
    concurrent_users: 20
    response_time_p95: "10s"
    optimization: ["EX-12批量执行", "EX-10异步执行"]
    
  - scenario: "峰值冲击"
    concurrent_users: 200
    response_time_p95: "2s"
    optimization: ["SC-06速率限制", "MT-09速度-质量权衡"]

# 实现示例
class ConcurrencyManager:
    """并发管理器 - 对齐EM-02模型负载均衡、EM-09动态并发调整"""
    
    def __init__(self):
        self.load_balancer = LoadBalancer()  # 对齐EM-02
        self.dynamic_controller = DynamicConcurrencyController()  # 对齐EM-09
        self.resource_allocator = ResourceAllocator()  # 对齐MT-07
    
    async def handle_request(self, request: Request) -> Response:
        """处理请求 - 动态并发控制"""
        # 获取当前负载
        current_load = await self._get_current_load()
        
        # 动态调整（对齐EM-09）
        if current_load > 0.8:
            await self.dynamic_controller.reduce_concurrency()
        elif current_load < 0.3:
            await self.dynamic_controller.increase_concurrency()
        
        # 负载均衡（对齐EM-02）
        instance = await self.load_balancer.select_instance(request)
        
        return await instance.process(request)
    
    async def scale_resources(self, required_capacity: int):
        """资源扩缩容 - 对齐MT-07资源配置"""
        await self.resource_allocator.adjust(required_capacity)

# 监控配置
monitoring:
  metrics:
    - name: "active_users"
      type: "gauge"
      alert_threshold: 80
      alert_severity: "warning"
      
    - name: "concurrent_requests"
      type: "gauge"
      alert_threshold: 100
      alert_severity: "warning"
      
    - name: "request_queue_length"
      type: "gauge"
      alert_threshold: 50
      alert_severity: "critical"
```

### 2.4 系统可用性

```yaml
# 系统可用性要求
metric_id: "PERF-04"
name: "系统可用性"
description: "系统正常运行时间的百分比"
target: "99.5%"
priority: "P0"
related_abilities: ["MT-01", "AGENT-RUNTIME-05"]

# 可用性计算
availability_formula: |
  Availability = (Total Time - Downtime) / Total Time × 100%
  
  允许停机时间:
  - 每月: < 3.6小时
  - 每周: < 50分钟
  - 每天: < 7.2分钟

# SLA分级
sla_tiers:
  - tier: "核心服务"
    components:
      - "用户认证"
      - "智能体管理"
      - "项目管理"
    target_availability: "99.9%"
    allowed_downtime_monthly: "43分钟"
    
  - tier: "重要服务"
    components:
      - "对话系统"
      - "代码生成"
      - "任务调度"
    target_availability: "99.5%"
    allowed_downtime_monthly: "3.6小时"
    
  - tier: "一般服务"
    components:
      - "营销中心"
      - "报表导出"
      - "历史查询"
    target_availability: "99%"
    allowed_downtime_monthly: "7.2小时"

# 实现示例
class AvailabilityManager:
    """可用性管理器 - 对齐MT-01自我监控、AGENT-RUNTIME-05健康自检"""
    
    def __init__(self):
        self.health_checker = HealthChecker()  # 对齐AGENT-RUNTIME-05
        self.monitor = SelfMonitor()  # 对齐MT-01
        self.failover_manager = FailoverManager()
    
    async def check_availability(self) -> AvailabilityReport:
        """检查系统可用性"""
        components_status = await self.health_checker.check_all()
        
        # 计算可用性
        available_components = sum(1 for s in components_status if s.healthy)
        total_components = len(components_status)
        current_availability = available_components / total_components * 100
        
        return AvailabilityReport(
            current_availability=current_availability,
            target_availability=99.5,
            components=components_status,
            uptime=await self._get_uptime(),
            last_incident=await self._get_last_incident()
        )
    
    async def handle_failure(self, component: str):
        """故障处理 - 故障转移"""
        await self.failover_manager.failover(component)
        await self._log_incident(component)

# 监控配置
monitoring:
  metrics:
    - name: "uptime_percentage"
      type: "gauge"
      alert_threshold: 99.5
      alert_severity: "critical"
      unit: "%"
      
    - name: "component_health"
      type: "gauge"
      labels: ["component"]
      alert_threshold: 0
      alert_severity: "critical"
      
    - name: "incident_count"
      type: "counter"
      labels: ["severity"]
      alert_threshold: 3
      alert_period: "month"
```


## 三、性能测试基准

```yaml
# 性能测试配置
performance_testing:
  # 负载测试
  load_test:
    tool: "Locust"
    scenarios:
      - name: "正常负载"
        users: 50
        spawn_rate: 5
        duration: "10m"
        
      - name: "峰值负载"
        users: 200
        spawn_rate: 20
        duration: "5m"
        
      - name: "稳定性测试"
        users: 50
        spawn_rate: 5
        duration: "2h"
        
  # 压力测试
  stress_test:
    tool: "JMeter"
    ramp_up: "5m"
    max_users: 500
    duration: "15m"
    
  # 基准测试
  benchmark_test:
    tool: "wrk"
    connections: 100
    threads: 4
    duration: "30s"
    
# 性能测试用例
test_cases:
  - id: "PT-01"
    name: "API响应时间测试"
    description: "验证各API端点响应时间满足P95 ≤ 180秒，且单次 ≤ 300秒"
    endpoints: ["/api/v1/agents", "/api/v1/projects", "/api/v1/tasks"]
    iterations: 1000
    pass_criteria: "p95_latency <= 180s && single_request_latency <= 300s"
    
  - id: "PT-02"
    name: "并发用户测试"
    description: "验证系统支持50个并发用户"
    concurrent_users: 50
    duration: "5m"
    pass_criteria: "error_rate < 1% and p95_latency < 1s"
    
  - id: "PT-03"
    name: "可用性测试"
    description: "验证系统可用性达到99.5%"
    duration: "7d"
    pass_criteria: "uptime >= 99.5%"
    
  - id: "PT-04"
    name: "页面加载测试"
    description: "验证页面加载时间小于3秒"
    pages: ["/dashboard", "/agents", "/projects"]
    pass_criteria: "lcp < 2.5s and tti < 3s"
```


## 四、通用能力映射表

```yaml
# 性能需求与通用能力映射
general_ability_mapping:
  PO-01_响应时间优化:
    mapped_metrics: ["PERF-01", "PERF-02"]
    description: "优化API响应时间和页面加载时间"
    
  PO-02_吞吐量优化:
    mapped_metrics: ["PERF-03"]
    description: "提升系统并发处理能力"
    
  EM-02_模型负载均衡:
    mapped_metrics: ["PERF-03"]
    description: "AI服务负载均衡"
    
  EM-04_模型缓存:
    mapped_metrics: ["PERF-01"]
    description: "缓存API响应结果"
    
  EM-09_动态并发调整:
    mapped_metrics: ["PERF-03"]
    description: "动态调整并发数"
    
  EX-09_并行执行:
    mapped_metrics: ["PERF-01", "PERF-03"]
    description: "并行处理请求"
    
  EX-10_异步执行:
    mapped_metrics: ["PERF-01"]
    description: "异步处理长耗时任务"
    
  EX-12_批量执行:
    mapped_metrics: ["PERF-01"]
    description: "批量处理优化"
    
  SC-06_速率限制:
    mapped_metrics: ["PERF-03"]
    description: "限流保护"
    
  MT-01_自我监控:
    mapped_metrics: ["PERF-04"]
    description: "系统状态监控"
    
  MT-07_资源配置:
    mapped_metrics: ["PERF-03"]
    description: "动态资源分配"
    
  MT-09_速度-质量权衡:
    mapped_metrics: ["PERF-03"]
    description: "峰值时降级处理"
    
  AGENT-RUNTIME-05_健康自检:
    mapped_metrics: ["PERF-04"]
    description: "组件健康检查"
```


## 五、监控告警配置

```yaml
# Prometheus告警规则
alerting_rules:
  - name: "API响应时间过高"
    expr: "histogram_quantile(0.95, sum(rate(api_latency_seconds_bucket[5m])) by (le, endpoint)) > 0.5"
    for: "5m"
    severity: "warning"
    annotations:
      summary: "API {{ $labels.endpoint }} 响应时间过高"
      
  - name: "API响应时间严重过高"
    expr: "histogram_quantile(0.95, sum(rate(api_latency_seconds_bucket[5m])) by (le, endpoint)) > 1"
    for: "2m"
    severity: "critical"
    annotations:
      summary: "API {{ $labels.endpoint }} 响应时间严重过高"
      
  - name: "系统可用性下降"
    expr: "up{job='jyis'} == 0"
    for: "1m"
    severity: "critical"
    annotations:
      summary: "服务 {{ $labels.instance }} 不可用"
      
  - name: "并发用户过高"
    expr: "active_users > 80"
    for: "5m"
    severity: "warning"
    annotations:
      summary: "活跃用户数超过80，当前值 {{ $value }}"
      
  - name: "错误率过高"
    expr: "sum(rate(http_requests_total{status=~'5..'}[5m])) / sum(rate(http_requests_total[5m])) > 0.05"
    for: "5m"
    severity: "critical"
    annotations:
      summary: "API错误率超过5%"
```


## 六、在Cursor中使用

```bash
# 1. 实现API性能优化
@docs/PERFORMANCE_REQUIREMENTS_v1.0.md 实现PERF-01 API响应时间优化，使用PO-01响应时间优化和EM-04模型缓存能力

# 2. 实现并发管理
@docs/PERFORMANCE_REQUIREMENTS_v1.0.md 实现PERF-03并发管理，使用EM-02负载均衡和EM-09动态并发调整

# 3. 实现可用性监控
@docs/PERFORMANCE_REQUIREMENTS_v1.0.md 实现PERF-04系统可用性监控，使用MT-01自我监控能力

# 4. 配置性能测试
@docs/PERFORMANCE_REQUIREMENTS_v1.0.md 根据性能测试基准配置负载测试和压力测试

# 5. 配置监控告警
@docs/PERFORMANCE_REQUIREMENTS_v1.0.md 根据告警规则配置Prometheus告警
```


## 七、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，4项性能指标，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**