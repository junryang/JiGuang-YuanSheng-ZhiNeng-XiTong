# 系统监控模块 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\SYSTEM_MONITOR_MODULE_v1.0.md
```


# 系统监控模块 v1.0

## 一、模块概述

```yaml
module:
  name: "系统监控模块"
  description: |
    负责系统健康状态监控、资源使用监控、性能指标采集、告警管理等。
    本模块基于通用能力规范（AGENT_ABILITY_SPEC_v1.0.md）中的智能体运行时能力实现。
  domain: "平台运营中心"
  priority: "P1"

# 关联的通用能力
related_abilities:
  - "AGENT-RUNTIME-04: 元认知监控"
  - "AGENT-RUNTIME-05: 健康自检与自愈"
  - "AGENT-RUNTIME-11: 自我反思"
  - "PC-03: 日志理解"
  - "PC-07: 文档理解"
  - "CG-04: 数值推理"
  - "CG-07: 抽象能力"
  - "QL-01: 代码质量感知"
  - "QL-07: 质量趋势分析"
  - "EX-03: API调用"
  - "EX-08: 消息发送"
  - "EX-11: 定时执行"
  - "SC-07: 操作审计"
  - "META-04: 能力自省"

functions:
  total_count: 4
  categories:
    - "系统状态监控"
    - "资源监控"
    - "性能指标监控"
    - "告警管理"
```


## 二、数据模型定义

### 2.1 系统状态数据模型

```python
# models/system_monitor.py

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel

class SystemHealthStatus(str, Enum):
    """系统健康状态"""
    HEALTHY = "healthy"          # 健康
    DEGRADED = "degraded"        # 降级
    UNHEALTHY = "unhealthy"      # 不健康
    UNKNOWN = "unknown"          # 未知

class ComponentStatus(str, Enum):
    """组件状态"""
    UP = "up"                    # 正常运行
    DOWN = "down"                # 宕机
    DEGRADED = "degraded"        # 降级
    MAINTENANCE = "maintenance"  # 维护中

class SystemStatus(BaseModel):
    """系统状态"""
    overall_status: SystemHealthStatus
    version: str
    uptime_seconds: int
    environment: str  # dev, staging, prod
    components: Dict[str, ComponentHealth]
    last_updated: datetime

class ComponentHealth(BaseModel):
    """组件健康状态"""
    name: str
    status: ComponentStatus
    message: Optional[str]
    last_check: datetime
    response_time_ms: Optional[float]

class ResourceMetrics(BaseModel):
    """资源指标"""
    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_total_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float
    network_rx_mbps: float
    network_tx_mbps: float
    fd_count: int
    thread_count: int

class PerformanceMetrics(BaseModel):
    """性能指标"""
    timestamp: datetime
    api_endpoint: str
    method: str
    p50_ms: float
    p95_ms: float
    p99_ms: float
    throughput_rps: float
    error_rate: float
    success_count: int
    failure_count: int

class AlertRule(BaseModel):
    """告警规则"""
    id: str
    name: str
    description: str
    metric: str  # cpu_percent, memory_percent, api_latency, etc.
    condition: str  # >, <, >=, <=, ==
    threshold: float
    duration_seconds: int  # 持续时间
    severity: str  # info, warning, critical
    channels: List[str]  # feishu, wechat, email, webhook
    enabled: bool
    created_at: datetime
    updated_at: datetime

class Alert(BaseModel):
    """告警实例"""
    id: str
    rule_id: str
    rule_name: str
    severity: str
    metric: str
    current_value: float
    threshold: float
    message: str
    status: str  # firing, resolved
    fired_at: datetime
    resolved_at: Optional[datetime]
    acknowledged_by: Optional[str]
    acknowledged_at: Optional[datetime]
```


## 三、功能详细设计

### 3.1 SM-01 系统状态

```yaml
# SM-01 系统状态
function_id: "SM-01"
name: "系统状态"
description: "展示系统健康状态、组件状态、运行时长"
priority: "P1"
related_abilities: ["AGENT-RUNTIME-04", "AGENT-RUNTIME-05", "EX-03"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/monitor/status"
    description: "获取系统状态"
    response:
      status: "SystemStatus"
      
  - method: "GET"
    endpoint: "/api/v1/monitor/health"
    description: "健康检查端点"
    response:
      status: "string"
      
  - method: "GET"
    endpoint: "/api/v1/monitor/components"
    description: "获取组件状态列表"
    response:
      components: "List[ComponentHealth]"

# 实现示例
class SystemStatusMonitor:
    """系统状态监控器 - 对齐AGENT-RUNTIME-04元认知监控"""
    
    def __init__(self):
        self.components = [
            "postgres", "redis", "rabbitmq", "chroma",
            "backend_api", "frontend", "websocket", "task_scheduler"
        ]
        self.health_checker = HealthChecker()  # 对齐AGENT-RUNTIME-05
    
    async def get_system_status(self) -> SystemStatus:
        """获取系统状态 - 对齐AGENT-RUNTIME-04"""
        start_time = datetime.now()
        
        # 并行检查各组件
        tasks = [self._check_component(c) for c in self.components]
        results = await asyncio.gather(*tasks)
        
        # 构建组件健康映射
        component_health = {}
        for name, status in zip(self.components, results):
            component_health[name] = status
        
        # 计算整体状态
        unhealthy_count = sum(1 for s in results if s.status == ComponentStatus.DOWN)
        degraded_count = sum(1 for s in results if s.status == ComponentStatus.DEGRADED)
        
        if unhealthy_count > 0:
            overall = SystemHealthStatus.UNHEALTHY
        elif degraded_count > 0:
            overall = SystemHealthStatus.DEGRADED
        else:
            overall = SystemHealthStatus.HEALTHY
        
        # 计算运行时长
        uptime = await self._get_uptime()
        
        return SystemStatus(
            overall_status=overall,
            version=self._get_version(),
            uptime_seconds=uptime,
            environment=os.getenv("ENVIRONMENT", "development"),
            components=component_health,
            last_updated=datetime.now()
        )
    
    async def _check_component(self, name: str) -> ComponentHealth:
        """检查组件健康 - 对齐AGENT-RUNTIME-05"""
        start = time.time()
        try:
            if name == "postgres":
                status = await self._check_postgres()
            elif name == "redis":
                status = await self._check_redis()
            elif name == "rabbitmq":
                status = await self._check_rabbitmq()
            elif name == "backend_api":
                status = await self._check_backend_api()
            else:
                status = ComponentStatus.UP
            
            response_time = (time.time() - start) * 1000
            
            return ComponentHealth(
                name=name,
                status=status,
                last_check=datetime.now(),
                response_time_ms=response_time
            )
        except Exception as e:
            return ComponentHealth(
                name=name,
                status=ComponentStatus.DOWN,
                message=str(e),
                last_check=datetime.now()
            )
```

### 3.2 SM-02 资源监控

```yaml
# SM-02 资源监控
function_id: "SM-02"
name: "资源监控"
description: "监控CPU、内存、磁盘、网络使用情况"
priority: "P1"
related_abilities: ["CG-04", "QL-07", "EX-11"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/monitor/resources"
    description: "获取当前资源使用情况"
    response:
      metrics: "ResourceMetrics"
      
  - method: "GET"
    endpoint: "/api/v1/monitor/resources/history"
    description: "获取资源历史数据"
    query_params:
      metric: "str"  # cpu, memory, disk, network
      hours: "int"
      interval: "str"  # minute, hour
    response:
      history: "List[ResourceMetrics]"
      
  - method: "GET"
    endpoint: "/api/v1/monitor/resources/trend"
    description: "获取资源趋势分析"
    query_params:
      metric: "str"
      hours: "int"
    response:
      trend: "TrendAnalysis"

# 实现示例
class ResourceMonitor:
    """资源监控器 - 对齐CG-04数值推理、QL-07质量趋势分析"""
    
    def __init__(self):
        self.metrics_store = MetricsStore()
        self.trend_analyzer = TrendAnalyzer()  # 对齐QL-07
    
    async def get_current_metrics(self) -> ResourceMetrics:
        """获取当前资源指标 - 对齐CG-04"""
        import psutil
        
        # 获取CPU信息
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 获取内存信息
        memory = psutil.virtual_memory()
        
        # 获取磁盘信息
        disk = psutil.disk_usage('/')
        
        # 获取网络信息
        net_io = psutil.net_io_counters()
        
        metrics = ResourceMetrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory.percent,
            memory_used_mb=memory.used / 1024 / 1024,
            memory_total_mb=memory.total / 1024 / 1024,
            disk_percent=disk.percent,
            disk_used_gb=disk.used / 1024 / 1024 / 1024,
            disk_total_gb=disk.total / 1024 / 1024 / 1024,
            network_rx_mbps=net_io.bytes_recv / 1024 / 1024,
            network_tx_mbps=net_io.bytes_sent / 1024 / 1024,
            fd_count=len(psutil.Process().open_files()),
            thread_count=psutil.Process().num_threads()
        )
        
        # 存储指标
        await self.metrics_store.save(metrics)
        
        return metrics
    
    async def get_trend_analysis(self, metric: str, hours: int = 24) -> TrendAnalysis:
        """获取趋势分析 - 对齐QL-07"""
        # 获取历史数据
        history = await self.metrics_store.get_history(metric, hours)
        
        # 分析趋势（对齐QL-07）
        values = [getattr(m, metric) for m in history]
        
        # 计算移动平均
        moving_avg = self._calculate_moving_average(values, window=10)
        
        # 检测异常
        anomalies = self._detect_anomalies(values)
        
        # 预测未来（对齐CG-04）
        forecast = self._forecast(values, periods=12)
        
        return TrendAnalysis(
            metric=metric,
            current_value=values[-1] if values else 0,
            average_value=sum(values) / len(values) if values else 0,
            max_value=max(values) if values else 0,
            min_value=min(values) if values else 0,
            trend_direction=self._calculate_trend(values),
            anomalies=anomalies,
            moving_average=moving_avg,
            forecast=forecast,
            confidence=self._calculate_confidence(values)
        )
```

### 3.3 SM-03 性能指标

```yaml
# SM-03 性能指标
function_id: "SM-03"
name: "性能指标"
description: "展示API响应时间、吞吐量、错误率"
priority: "P1"
related_abilities: ["EX-03", "CG-04", "QL-01"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/monitor/performance"
    description: "获取当前性能指标"
    query_params:
      endpoint: "str"
      minutes: "int"
    response:
      metrics: "PerformanceMetrics"
      
  - method: "GET"
    endpoint: "/api/v1/monitor/performance/endpoints"
    description: "获取所有API端点列表"
    response:
      endpoints: "List[str]"
      
  - method: "GET"
    endpoint: "/api/v1/monitor/performance/top-slow"
    description: "获取最慢的API端点"
    query_params:
      limit: "int"
    response:
      endpoints: "List[PerformanceMetrics]"

# 实现示例
class PerformanceMonitor:
    """性能监控器 - 对齐EX-03 API调用、CG-04数值推理"""
    
    def __init__(self):
        self.metrics_store = MetricsStore()
        self.middleware = PerformanceMiddleware()
    
    async def get_performance_metrics(self, endpoint: str = None, 
                                       minutes: int = 60) -> List[PerformanceMetrics]:
        """获取性能指标 - 对齐CG-04"""
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=minutes)
        
        # 查询指标
        query = {"timestamp": {"$gte": start_time, "$lte": end_time}}
        if endpoint:
            query["api_endpoint"] = endpoint
        
        metrics = await self.metrics_store.find(query)
        
        # 聚合计算（对齐CG-04）
        if metrics:
            # 计算百分位数
            latencies = [m.p95_ms for m in metrics]
            latencies.sort()
            
            p50 = latencies[int(len(latencies) * 0.5)] if latencies else 0
            p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
            p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0
            
            # 计算吞吐量
            total_requests = sum(m.success_count + m.failure_count for m in metrics)
            throughput = total_requests / (minutes * 60)
            
            # 计算错误率
            total_errors = sum(m.failure_count for m in metrics)
            error_rate = total_errors / total_requests if total_requests > 0 else 0
            
            return PerformanceMetrics(
                timestamp=datetime.now(),
                api_endpoint=endpoint or "all",
                method="ALL",
                p50_ms=p50,
                p95_ms=p95,
                p99_ms=p99,
                throughput_rps=throughput,
                error_rate=error_rate * 100,
                success_count=total_requests - total_errors,
                failure_count=total_errors
            )
        
        return None
    
    async def record_request_metrics(self, endpoint: str, method: str,
                                      status_code: int, duration_ms: float):
        """记录请求指标 - 对齐EX-03"""
        metric = PerformanceMetrics(
            timestamp=datetime.now(),
            api_endpoint=endpoint,
            method=method,
            p95_ms=duration_ms,
            success_count=1 if status_code < 400 else 0,
            failure_count=1 if status_code >= 400 else 0,
            error_rate=0 if status_code < 400 else 100
        )
        
        await self.metrics_store.save(metric)
```

### 3.4 SM-04 告警管理

```yaml
# SM-04 告警管理
function_id: "SM-04"
name: "告警管理"
description: "配置和接收告警规则，支持多渠道通知"
priority: "P2"
related_abilities: ["EX-08", "EX-11", "SC-07", "META-04"]

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/monitor/alerts/rules"
    description: "获取告警规则列表"
    response:
      rules: "List[AlertRule]"
      
  - method: "POST"
    endpoint: "/api/v1/monitor/alerts/rules"
    description: "创建告警规则"
    request_body:
      name: "str"
      metric: "str"
      condition: "str"
      threshold: "float"
      severity: "str"
      channels: "List[str]"
    response:
      rule: "AlertRule"
      
  - method: "PUT"
    endpoint: "/api/v1/monitor/alerts/rules/{id}"
    description: "更新告警规则"
    response:
      rule: "AlertRule"
      
  - method: "DELETE"
    endpoint: "/api/v1/monitor/alerts/rules/{id}"
    description: "删除告警规则"
    
  - method: "GET"
    endpoint: "/api/v1/monitor/alerts/firing"
    description: "获取当前告警"
    response:
      alerts: "List[Alert]"
      
  - method: "POST"
    endpoint: "/api/v1/monitor/alerts/{id}/acknowledge"
    description: "确认告警"
    request_body:
      acknowledged_by: "str"
    response:
      success: "bool"
      
  - method: "POST"
    endpoint: "/api/v1/monitor/alerts/test"
    description: "测试告警通知"
    request_body:
      channel: "str"
    response:
      success: "bool"

# 预置告警规则
default_alert_rules:
  - name: "CPU使用率过高"
    metric: "cpu_percent"
    condition: ">"
    threshold: 80
    duration: 300
    severity: "warning"
    
  - name: "内存使用率过高"
    metric: "memory_percent"
    condition: ">"
    threshold: 90
    duration: 300
    severity: "critical"
    
  - name: "磁盘使用率过高"
    metric: "disk_percent"
    condition: ">"
    threshold: 85
    duration: 600
    severity: "warning"
    
  - name: "API响应时间过长"
    metric: "api_latency_p95"
    condition: ">"
    threshold: 1000
    duration: 300
    severity: "warning"
    
  - name: "API错误率过高"
    metric: "api_error_rate"
    condition: ">"
    threshold: 5
    duration: 300
    severity: "critical"

# 实现示例
class AlertManager:
    """告警管理器 - 对齐EX-08消息发送、EX-11定时执行"""
    
    def __init__(self):
        self.rule_store = RuleStore()
        self.alert_store = AlertStore()
        self.notifier = UnifiedNotifier()  # 对齐EX-08
        self.scheduler = AsyncIOScheduler()  # 对齐EX-11
    
    async def start(self):
        """启动告警检查 - 对齐EX-11"""
        self.scheduler.add_job(
            func=self._check_alerts,
            trigger="interval",
            seconds=30,
            id="alert_checker"
        )
        self.scheduler.start()
    
    async def _check_alerts(self):
        """检查告警规则"""
        rules = await self.rule_store.get_enabled_rules()
        
        for rule in rules:
            # 获取当前指标值
            current_value = await self._get_metric_value(rule.metric)
            
            # 检查是否触发
            triggered = self._evaluate_condition(
                current_value, rule.condition, rule.threshold
            )
            
            if triggered:
                await self._handle_triggered_alert(rule, current_value)
            else:
                await self._handle_resolved_alert(rule, current_value)
    
    async def _handle_triggered_alert(self, rule: AlertRule, current_value: float):
        """处理触发的告警"""
        # 检查是否已有活跃告警
        existing = await self.alert_store.find_active(rule.id)
        
        if not existing:
            # 创建新告警
            alert = Alert(
                id=self._generate_id(),
                rule_id=rule.id,
                rule_name=rule.name,
                severity=rule.severity,
                metric=rule.metric,
                current_value=current_value,
                threshold=rule.threshold,
                message=f"{rule.name}: {current_value} {rule.condition} {rule.threshold}",
                status="firing",
                fired_at=datetime.now()
            )
            await self.alert_store.save(alert)
            
            # 发送通知（对齐EX-08）
            await self._send_notification(alert, rule.channels)
    
    async def _send_notification(self, alert: Alert, channels: List[str]):
        """发送告警通知 - 对齐EX-08"""
        message = self._format_alert_message(alert)
        
        for channel in channels:
            if channel == "feishu":
                await self.notifier.send_feishu(message)
            elif channel == "wechat":
                await self.notifier.send_wechat(message)
            elif channel == "email":
                await self.notifier.send_email(message)
            elif channel == "webhook":
                await self._send_webhook(message)
```


## 四、监控架构图

```yaml
architecture: |
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │                           系统监控架构                                      │
  ├─────────────────────────────────────────────────────────────────────────────┤
  │                                                                             │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         数据采集层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 系统指标    │  │ 应用指标    │  │ 业务指标    │                  │   │
  │  │  │ (psutil)    │  │ (中间件)    │  │ (API)       │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         数据处理层                                   │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 数据聚合    │  │ 趋势分析    │  │ 异常检测    │                  │   │
  │  │  │ (CG-04)     │  │ (QL-07)     │  │ (META-04)   │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         存储层                                       │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 时序数据库  │  │ 告警存储    │  │ 日志存储    │                  │   │
  │  │  │ (InfluxDB)  │  │ (PostgreSQL)│  │ (ELK)       │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                    │                                        │
  │                                    ▼                                        │
  │  ┌─────────────────────────────────────────────────────────────────────┐   │
  │  │                         展示层                                       │   │
  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
  │  │  │ 状态看板    │  │ 资源监控    │  │ 告警中心    │                  │   │
  │  │  │ (SM-01)     │  │ (SM-02)     │  │ (SM-04)     │                  │   │
  │  │  └─────────────┘  └─────────────┘  └─────────────┘                  │   │
  │  └─────────────────────────────────────────────────────────────────────┘   │
  │                                                                             │
  └─────────────────────────────────────────────────────────────────────────────┘
```


## 五、通用能力映射表

```yaml
# 系统监控功能与通用能力映射
general_ability_mapping:
  AGENT-RUNTIME-04_元认知监控:
    mapped_functions: ["SM-01"]
    description: "系统状态监控，类似智能体的元认知"
    
  AGENT-RUNTIME-05_健康自检与自愈:
    mapped_functions: ["SM-01"]
    description: "组件健康检查"
    
  PC-03_日志理解:
    mapped_functions: ["SM-02", "SM-03"]
    description: "理解系统日志和性能日志"
    
  CG-04_数值推理:
    mapped_functions: ["SM-02", "SM-03"]
    description: "资源指标计算、性能指标聚合"
    
  QL-07_质量趋势分析:
    mapped_functions: ["SM-02"]
    description: "资源使用趋势分析"
    
  EX-03_API调用:
    mapped_functions: ["SM-03"]
    description: "API性能指标采集"
    
  EX-08_消息发送:
    mapped_functions: ["SM-04"]
    description: "告警通知发送"
    
  EX-11_定时执行:
    mapped_functions: ["SM-04"]
    description: "定时告警检查"
    
  SC-07_操作审计:
    mapped_functions: ["SM-04"]
    description: "告警操作审计"
    
  META-04_能力自省:
    mapped_functions: ["SM-02", "SM-03"]
    description: "系统性能自省"
```


## 六、数据库表结构

```sql
-- 系统状态表
CREATE TABLE system_status (
    id UUID PRIMARY KEY,
    overall_status VARCHAR(20) NOT NULL,
    version VARCHAR(50),
    uptime_seconds INTEGER,
    environment VARCHAR(20),
    components JSONB,
    created_at TIMESTAMP NOT NULL
);

-- 资源指标表
CREATE TABLE resource_metrics (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    cpu_percent DECIMAL(5,2),
    memory_percent DECIMAL(5,2),
    memory_used_mb DECIMAL(10,2),
    memory_total_mb DECIMAL(10,2),
    disk_percent DECIMAL(5,2),
    disk_used_gb DECIMAL(10,2),
    disk_total_gb DECIMAL(10,2),
    network_rx_mbps DECIMAL(10,2),
    network_tx_mbps DECIMAL(10,2),
    fd_count INTEGER,
    thread_count INTEGER
);

-- 性能指标表
CREATE TABLE performance_metrics (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    api_endpoint VARCHAR(500),
    method VARCHAR(10),
    p50_ms DECIMAL(10,2),
    p95_ms DECIMAL(10,2),
    p99_ms DECIMAL(10,2),
    throughput_rps DECIMAL(10,2),
    error_rate DECIMAL(5,2),
    success_count INTEGER,
    failure_count INTEGER
);

-- 告警规则表
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    metric VARCHAR(100) NOT NULL,
    condition VARCHAR(10) NOT NULL,
    threshold DECIMAL(10,2) NOT NULL,
    duration_seconds INTEGER DEFAULT 0,
    severity VARCHAR(20) NOT NULL,
    channels TEXT[],
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 告警实例表
CREATE TABLE alerts (
    id UUID PRIMARY KEY,
    rule_id UUID REFERENCES alert_rules(id),
    rule_name VARCHAR(200),
    severity VARCHAR(20),
    metric VARCHAR(100),
    current_value DECIMAL(10,2),
    threshold DECIMAL(10,2),
    message TEXT,
    status VARCHAR(20) DEFAULT 'firing',
    fired_at TIMESTAMP,
    resolved_at TIMESTAMP,
    acknowledged_by VARCHAR(100),
    acknowledged_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL
);

-- 索引
CREATE INDEX idx_resource_metrics_timestamp ON resource_metrics(timestamp);
CREATE INDEX idx_performance_metrics_timestamp ON performance_metrics(timestamp);
CREATE INDEX idx_performance_metrics_endpoint ON performance_metrics(api_endpoint);
CREATE INDEX idx_alert_rules_enabled ON alert_rules(enabled);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_fired_at ON alerts(fired_at);
```


## 七、在Cursor中使用

```bash
# 1. 实现系统状态监控
@docs/SYSTEM_MONITOR_MODULE_v1.0.md 实现SM-01系统状态功能，对齐AGENT-RUNTIME-04元认知监控

# 2. 实现资源监控
@docs/SYSTEM_MONITOR_MODULE_v1.0.md 实现SM-02资源监控功能，使用psutil采集CPU、内存、磁盘指标

# 3. 实现性能指标监控
@docs/SYSTEM_MONITOR_MODULE_v1.0.md 实现SM-03性能指标功能，记录API响应时间和错误率

# 4. 实现告警管理
@docs/SYSTEM_MONITOR_MODULE_v1.0.md 实现SM-04告警管理功能，支持飞书、微信多渠道通知
```


## 八、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，4项系统监控功能，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**