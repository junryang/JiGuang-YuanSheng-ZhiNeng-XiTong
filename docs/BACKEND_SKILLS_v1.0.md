# 后端部员工专属能力 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\BACKEND_SKILLS_v1.0.md
```


# 后端部员工专属能力 v1.0

## 一、能力总览

```yaml
department: "后端部"
layer: "L5_员工"
description: "后端部员工专属技术能力，用于API开发、数据库设计、性能优化、安全加固"
priority: "P0"

# 关联的通用能力
related_abilities:
  - "EX-01: 代码生成"
  - "EX-03: API调用"
  - "EX-04: 数据库操作"
  - "EX-05: 文件操作"
  - "EX-09: 并行执行"
  - "EX-10: 异步执行"
  - "EX-12: 批量执行"
  - "EX-13: 幂等执行"
  - "SC-01: 代码沙箱"
  - "SC-03: 敏感信息检测"
  - "SC-04: 权限检查"
  - "QL-01: 代码质量感知"
  - "QL-02: 输出置信度评估"
  - "QL-05: 质量验证"

skills:
  total_count: 16
  categories:
    - "API开发"
    - "数据库设计"
    - "性能优化"
    - "安全加固"
    - "架构设计"
    - "测试与文档"
```


## 二、API开发能力

```yaml
# API开发能力集 - 对齐通用能力EX-03 API调用、SC-04权限检查

category: "API开发"
description: "开发RESTful/GraphQL API，包括设计、实现、文档、版本管理"
related_abilities: ["EX-03", "SC-04", "EX-13"]

skills:
  - id: "BE-API-01"
    name: "RESTful API设计"
    description: "遵循RESTful规范设计API，包括资源命名、HTTP方法、状态码"
    input: "业务需求、数据模型"
    output: "API设计文档、OpenAPI规范"
    implementation: "OpenAPI/Swagger生成器"
    examples:
      - "设计用户管理API，包含CRUD操作"
      - "设计订单API，支持分页和筛选"
    priority: "P0"
    related_ability: "EX-03"
    
  - id: "BE-API-02"
    name: "GraphQL API开发"
    description: "开发GraphQL API，设计Schema、Resolver、数据加载器"
    input: "数据模型、查询需求"
    output: "GraphQL Schema、Resolver代码"
    implementation: "GraphQL框架（Apollo/Graphene）"
    examples:
      - "设计用户和订单的GraphQL查询"
      - "实现批量数据加载器避免N+1查询"
    priority: "P1"
    related_ability: "EX-03"
    
  - id: "BE-API-03"
    name: "API版本管理"
    description: "管理API版本，支持平滑升级和废弃"
    input: "API变更需求"
    output: "版本兼容方案、迁移指南"
    implementation: "URL路径版本/Header版本"
    examples:
      - "将v1 API升级到v2，保持v1可用"
      - "废弃旧版API，通知调用方迁移"
    priority: "P1"
    related_ability: "EX-03"
    
  - id: "BE-API-04"
    name: "API认证授权"
    description: "实现API认证（JWT/OAuth）和授权（RBAC）"
    input: "安全需求"
    output: "认证授权代码"
    implementation: "JWT、OAuth2、RBAC"
    examples:
      - "实现JWT token生成和验证"
      - "实现基于角色的API权限控制"
    priority: "P0"
    related_ability: "SC-04"
    
  - id: "BE-API-05"
    name: "API限流"
    description: "实现API限流，防止滥用。对应通用能力SC-06速率限制"
    input: "限流策略（用户/IP/API）"
    output: "限流代码"
    implementation: "令牌桶、滑动窗口、Redis"
    examples:
      - "实现每用户每分钟100次请求限制"
      - "实现IP级别的限流"
    priority: "P0"
    related_ability: "SC-06"
    
  - id: "BE-API-06"
    name: "API文档生成"
    description: "自动生成API文档"
    input: "代码注解/OpenAPI规范"
    output: "API文档（Swagger/Redoc）"
    implementation: "Swagger UI、ReDoc"
    examples:
      - "从FastAPI自动生成Swagger文档"
      - "生成Markdown格式的API文档"
    priority: "P0"
    related_ability: "EX-14"
    
  - id: "BE-API-07"
    name: "API错误处理"
    description: "统一API错误响应格式和错误码。对应通用能力QL-05质量验证"
    input: "异常类型"
    output: "错误响应"
    implementation: "全局异常处理器"
    examples:
      - "统一返回格式: {code, message, data}"
      - "定义业务错误码: 10001-参数错误"
    priority: "P0"
    related_ability: "QL-05"
    
  - id: "BE-API-08"
    name: "API请求验证"
    description: "验证API请求参数的有效性。对应通用能力QL-04质量自检"
    input: "请求数据、验证规则"
    output: "验证结果、错误信息"
    implementation: "Pydantic/JSON Schema验证"
    examples:
      - "验证邮箱格式是否正确"
      - "验证日期范围是否合法"
    priority: "P0"
    related_ability: "QL-04"
```


## 三、数据库设计能力

```yaml
# 数据库设计能力集 - 对齐通用能力EX-04数据库操作

category: "数据库设计"
description: "设计数据模型、索引、查询优化"
related_abilities: ["EX-04", "QL-01"]

skills:
  - id: "BE-DB-01"
    name: "数据建模"
    description: "设计数据模型，包括实体、关系、约束"
    input: "业务需求"
    output: "ER图、数据模型文档"
    implementation: "ER建模工具、SQLAlchemy/Prisma"
    examples:
      - "设计用户-订单-商品的数据模型"
      - "设计多对多关系的关联表"
    priority: "P0"
    related_ability: "EX-04"
    
  - id: "BE-DB-02"
    name: "索引设计"
    description: "设计数据库索引，优化查询性能。对应通用能力QL-01代码质量感知"
    input: "查询模式、数据量"
    output: "索引创建语句"
    implementation: "B-Tree、Hash、全文索引"
    examples:
      - "为用户表的email字段创建唯一索引"
      - "为订单表的user_id和created_at创建复合索引"
    priority: "P0"
    related_ability: "QL-01"
    
  - id: "BE-DB-03"
    name: "SQL优化"
    description: "优化慢查询SQL语句。对应通用能力EX-04数据库操作"
    input: "慢查询日志"
    output: "优化后的SQL、执行计划分析"
    implementation: "EXPLAIN分析、查询重写"
    examples:
      - "优化N+1查询问题"
      - "将子查询改写为JOIN"
    priority: "P0"
    related_ability: "EX-04"
    
  - id: "BE-DB-04"
    name: "数据库迁移"
    description: "管理数据库Schema变更。对应通用能力EX-13幂等执行"
    input: "模型变更"
    output: "迁移脚本"
    implementation: "Alembic、Flyway、Liquibase"
    examples:
      - "添加新字段的迁移脚本"
      - "数据迁移和回滚"
    priority: "P0"
    related_ability: "EX-13"
    
  - id: "BE-DB-05"
    name: "分库分表"
    description: "设计分库分表策略"
    input: "数据量、访问模式"
    output: "分片方案"
    implementation: "ShardingSphere、Vitess"
    examples:
      - "按用户ID哈希分表"
      - "按时间分区"
    priority: "P2"
    related_ability: "EX-04"
    
  - id: "BE-DB-06"
    name: "读写分离"
    description: "配置主从复制和读写分离。对应通用能力EX-09并行执行"
    input: "读写比例"
    output: "读写分离配置"
    implementation: "数据库代理、中间件"
    examples:
      - "主库处理写请求，从库处理读请求"
      - "配置负载均衡策略"
    priority: "P1"
    related_ability: "EX-09"
    
  - id: "BE-DB-07"
    name: "数据备份恢复"
    description: "设计数据备份和恢复方案"
    input: "RPO/RTO要求"
    output: "备份脚本、恢复流程"
    implementation: "pg_dump、mysqldump、WAL归档"
    examples:
      - "每日全量备份"
      - "点时间恢复"
    priority: "P1"
    related_ability: "EX-05"
    
  - id: "BE-DB-08"
    name: "数据库监控"
    description: "监控数据库性能和健康状态。对应通用能力QL-07质量趋势分析"
    input: "数据库指标"
    output: "监控仪表盘、告警"
    implementation: "Prometheus + Grafana"
    examples:
      - "监控连接数、QPS、慢查询"
      - "设置CPU/内存告警阈值"
    priority: "P1"
    related_ability: "QL-07"
```


## 四、性能优化能力

```yaml
# 性能优化能力集 - 对齐通用能力EX-09并行执行、EX-10异步执行、EX-12批量执行

category: "性能优化"
description: "识别和解决性能瓶颈，优化系统响应"
related_abilities: ["EX-09", "EX-10", "EX-12", "QL-01"]

skills:
  - id: "BE-PERF-01"
    name: "性能分析"
    description: "分析系统性能瓶颈。对应通用能力QL-01代码质量感知"
    input: "性能指标、慢请求"
    output: "瓶颈分析报告"
    implementation: "Profiling工具、APM"
    examples:
      - "使用py-spy分析CPU热点"
      - "分析数据库慢查询"
    priority: "P0"
    related_ability: "QL-01"
    
  - id: "BE-PERF-02"
    name: "缓存设计"
    description: "设计多级缓存策略"
    input: "数据访问模式"
    output: "缓存架构方案"
    implementation: "Redis、Memcached、本地缓存"
    examples:
      - "热点数据缓存，TTL=1小时"
      - "缓存穿透、雪崩、击穿防护"
    priority: "P0"
    related_ability: "EX-03"
    
  - id: "BE-PERF-03"
    name: "异步处理"
    description: "使用消息队列实现异步处理。对应通用能力EX-10异步执行"
    input: "耗时任务"
    output: "异步处理代码"
    implementation: "Celery、RabbitMQ、Kafka"
    examples:
      - "邮件发送异步处理"
      - "报表生成异步任务"
    priority: "P0"
    related_ability: "EX-10"
    
  - id: "BE-PERF-04"
    name: "并发优化"
    description: "优化并发处理能力。对应通用能力EX-09并行执行"
    input: "高并发场景"
    output: "并发优化代码"
    implementation: "连接池、线程池、协程"
    examples:
      - "配置数据库连接池大小"
      - "使用asyncio提升IO密集型任务"
    priority: "P1"
    related_ability: "EX-09"
    
  - id: "BE-PERF-05"
    name: "批量处理"
    description: "批量处理优化，减少IO次数。对应通用能力EX-12批量执行"
    input: "多条数据操作"
    output: "批量处理代码"
    implementation: "批量插入、批量查询"
    examples:
      - "批量插入1000条数据"
      - "使用IN查询替代循环查询"
    priority: "P1"
    related_ability: "EX-12"
    
  - id: "BE-PERF-06"
    name: "代码优化"
    description: "优化代码算法和数据结构。对应通用能力QL-01代码质量感知"
    input: "低效代码"
    output: "优化后代码"
    implementation: "算法优化、数据结构选择"
    examples:
      - "将O(n²)算法优化为O(n log n)"
      - "使用Set替代List进行成员检查"
    priority: "P1"
    related_ability: "QL-01"
```


## 五、安全加固能力

```yaml
# 安全加固能力集 - 对齐通用能力SC-01代码沙箱、SC-03敏感信息检测、SC-04权限检查

category: "安全加固"
description: "代码安全审计和修复，防范常见安全漏洞"
related_abilities: ["SC-01", "SC-03", "SC-04"]

skills:
  - id: "BE-SEC-01"
    name: "SQL注入防护"
    description: "防止SQL注入攻击。对应通用能力SC-01代码沙箱"
    input: "数据库查询代码"
    output: "安全查询代码"
    implementation: "参数化查询、ORM"
    examples:
      - "使用参数化查询替代字符串拼接"
      - "使用ORM的查询构造器"
    priority: "P0"
    related_ability: "SC-01"
    
  - id: "BE-SEC-02"
    name: "XSS防护"
    description: "防止跨站脚本攻击"
    input: "用户输入、输出内容"
    output: "转义/过滤后的内容"
    implementation: "HTML转义、CSP"
    examples:
      - "对用户输入进行HTML转义"
      - "设置Content-Security-Policy头"
    priority: "P0"
    related_ability: "SC-01"
    
  - id: "BE-SEC-03"
    name: "CSRF防护"
    description: "防止跨站请求伪造"
    input: "状态变更请求"
    output: "CSRF Token验证"
    implementation: "CSRF Token、SameSite Cookie"
    examples:
      - "为表单添加CSRF Token"
      - "验证Referer头"
    priority: "P1"
    related_ability: "SC-04"
    
  - id: "BE-SEC-04"
    name: "敏感信息脱敏"
    description: "对敏感信息进行脱敏处理。对应通用能力SC-03敏感信息检测"
    input: "原始数据"
    output: "脱敏后数据"
    implementation: "正则替换、字段加密"
    examples:
      - "手机号中间4位显示为****"
      - "身份证号部分隐藏"
    priority: "P0"
    related_ability: "SC-03"
    
  - id: "BE-SEC-05"
    name: "密码加密"
    description: "安全存储用户密码"
    input: "明文密码"
    output: "加密哈希"
    implementation: "bcrypt、argon2"
    examples:
      - "使用bcrypt加密密码"
      - "加盐哈希存储"
    priority: "P0"
    related_ability: "SC-03"
    
  - id: "BE-SEC-06"
    name: "密钥管理"
    description: "安全管理API密钥、数据库密码。对应通用能力SC-03敏感信息检测"
    input: "密钥"
    output: "安全存储"
    implementation: "环境变量、密钥管理服务"
    examples:
      - "使用环境变量存储密钥"
      - "定期轮换密钥"
    priority: "P0"
    related_ability: "SC-03"
    
  - id: "BE-SEC-07"
    name: "输入验证"
    description: "验证所有外部输入。对应通用能力QL-04质量自检"
    input: "用户输入、API请求"
    output: "验证结果"
    implementation: "白名单验证、类型检查"
    examples:
      - "验证枚举值是否在允许范围内"
      - "验证文件类型是否为允许类型"
    priority: "P0"
    related_ability: "QL-04"
    
  - id: "BE-SEC-08"
    name: "安全审计日志"
    description: "记录安全相关操作日志。对应通用能力SC-07操作审计"
    input: "安全事件"
    output: "审计日志"
    implementation: "结构化日志、审计表"
    examples:
      - "记录登录成功/失败日志"
      - "记录敏感数据访问日志"
    priority: "P1"
    related_ability: "SC-07"
```


## 六、架构设计能力

```yaml
# 架构设计能力集 - 对齐通用能力DC-01任务规划、DC-06方案生成

category: "架构设计"
description: "系统架构设计和技术选型"
related_abilities: ["DC-01", "DC-06"]

skills:
  - id: "BE-ARCH-01"
    name: "分层架构设计"
    description: "设计清晰的分层架构。对应通用能力DC-01任务规划"
    input: "业务需求"
    output: "架构设计文档"
    implementation: "Controller-Service-Repository模式"
    examples:
      - "设计Controller层处理HTTP请求"
      - "设计Service层处理业务逻辑"
    priority: "P1"
    related_ability: "DC-01"
    
  - id: "BE-ARCH-02"
    name: "微服务设计"
    description: "设计微服务架构"
    input: "业务边界"
    output: "微服务拆分方案"
    implementation: "服务发现、API网关"
    examples:
      - "按业务域拆分微服务"
      - "设计服务间通信协议"
    priority: "P2"
    related_ability: "DC-06"
    
  - id: "BE-ARCH-03"
    name: "消息驱动设计"
    description: "设计事件驱动架构。对应通用能力EX-10异步执行"
    input: "异步场景"
    output: "消息架构方案"
    implementation: "事件总线、消息队列"
    examples:
      - "用户注册后发送欢迎邮件事件"
      - "订单状态变更触发通知事件"
    priority: "P1"
    related_ability: "EX-10"
```


## 七、测试与文档能力

```yaml
# 测试与文档能力集 - 对齐通用能力EX-07测试执行、QL-05质量验证

category: "测试与文档"
description: "单元测试、集成测试、API文档"
related_abilities: ["EX-07", "QL-05"]

skills:
  - id: "BE-TEST-01"
    name: "单元测试编写"
    description: "编写单元测试用例。对应通用能力EX-07测试执行"
    input: "函数/类"
    output: "测试代码"
    implementation: "pytest、unittest"
    examples:
      - "测试工具函数的边界条件"
      - "使用Mock模拟外部依赖"
    priority: "P0"
    related_ability: "EX-07"
    
  - id: "BE-TEST-02"
    name: "集成测试编写"
    description: "编写集成测试用例。对应通用能力EX-07测试执行"
    input: "API端点"
    output: "集成测试代码"
    implementation: "pytest、TestClient"
    examples:
      - "测试API端点的完整流程"
      - "测试数据库事务"
    priority: "P1"
    related_ability: "EX-07"
    
  - id: "BE-TEST-03"
    name: "测试覆盖率"
    description: "确保测试覆盖率达标。对应通用能力QL-05质量验证"
    input: "测试代码"
    output: "覆盖率报告"
    implementation: "pytest-cov"
    examples:
      - "全局测试覆盖率≥80%，核心模块按quality_standards的更高门槛执行"
      - "识别未覆盖的代码分支"
    priority: "P1"
    related_ability: "QL-05"
    
  - id: "BE-DOC-01"
    name: "技术文档编写"
    description: "编写技术设计文档。对应通用能力EX-14文档生成"
    input: "设计方案"
    output: "技术文档"
    implementation: "Markdown、Mermaid"
    examples:
      - "编写架构设计文档"
      - "绘制系统流程图"
    priority: "P1"
    related_ability: "EX-14"
```


## 八、能力优先级汇总

```yaml
# 按优先级排序 - 对齐通用能力优先级

P0_skills:  # 必须实现（共16项）
  - BE-API-01: "RESTful API设计"
  - BE-API-04: "API认证授权"
  - BE-API-05: "API限流"
  - BE-API-06: "API文档生成"
  - BE-API-07: "API错误处理"
  - BE-API-08: "API请求验证"
  - BE-DB-01: "数据建模"
  - BE-DB-02: "索引设计"
  - BE-DB-03: "SQL优化"
  - BE-DB-04: "数据库迁移"
  - BE-PERF-01: "性能分析"
  - BE-PERF-02: "缓存设计"
  - BE-PERF-03: "异步处理"
  - BE-SEC-01: "SQL注入防护"
  - BE-SEC-02: "XSS防护"
  - BE-SEC-04: "敏感信息脱敏"
  - BE-SEC-05: "密码加密"
  - BE-SEC-06: "密钥管理"
  - BE-SEC-07: "输入验证"
  - BE-TEST-01: "单元测试编写"

P1_skills:  # 近期实现（共11项）
  - BE-API-02: "GraphQL API开发"
  - BE-API-03: "API版本管理"
  - BE-DB-06: "读写分离"
  - BE-DB-07: "数据备份恢复"
  - BE-DB-08: "数据库监控"
  - BE-PERF-04: "并发优化"
  - BE-PERF-05: "批量处理"
  - BE-PERF-06: "代码优化"
  - BE-SEC-03: "CSRF防护"
  - BE-SEC-08: "安全审计日志"
  - BE-ARCH-01: "分层架构设计"
  - BE-ARCH-03: "消息驱动设计"
  - BE-TEST-02: "集成测试编写"
  - BE-TEST-03: "测试覆盖率"
  - BE-DOC-01: "技术文档编写"

P2_skills:  # 远期规划（共2项）
  - BE-DB-05: "分库分表"
  - BE-ARCH-02: "微服务设计"
```

## 九、通用能力映射表

```yaml
# 后端技能与通用能力映射
general_ability_mapping:
  EX-03_API调用:
    mapped_skills: ["BE-API-01", "BE-API-02", "BE-API-03", "BE-API-06", "BE-PERF-02"]
    
  EX-04_数据库操作:
    mapped_skills: ["BE-DB-01", "BE-DB-03", "BE-DB-05", "BE-DB-06"]
    
  EX-05_文件操作:
    mapped_skills: ["BE-DB-07"]
    
  EX-07_测试执行:
    mapped_skills: ["BE-TEST-01", "BE-TEST-02"]
    
  EX-09_并行执行:
    mapped_skills: ["BE-DB-06", "BE-PERF-04"]
    
  EX-10_异步执行:
    mapped_skills: ["BE-PERF-03", "BE-ARCH-03"]
    
  EX-12_批量执行:
    mapped_skills: ["BE-PERF-05"]
    
  EX-13_幂等执行:
    mapped_skills: ["BE-DB-04"]
    
  EX-14_文档生成:
    mapped_skills: ["BE-API-06", "BE-DOC-01"]
    
  SC-06_速率限制:
    mapped_skills: ["BE-API-05"]
    
  SC-01_代码沙箱:
    mapped_skills: ["BE-SEC-01", "BE-SEC-02"]
    
  SC-03_敏感信息检测:
    mapped_skills: ["BE-SEC-04", "BE-SEC-05", "BE-SEC-06"]
    
  SC-04_权限检查:
    mapped_skills: ["BE-API-04", "BE-SEC-03"]
    
  SC-07_操作审计:
    mapped_skills: ["BE-SEC-08"]
    
  QL-01_代码质量感知:
    mapped_skills: ["BE-DB-02", "BE-PERF-01", "BE-PERF-06"]
    
  QL-04_质量自检:
    mapped_skills: ["BE-API-08", "BE-SEC-07"]
    
  QL-05_质量验证:
    mapped_skills: ["BE-API-07", "BE-TEST-03"]
    
  QL-07_质量趋势分析:
    mapped_skills: ["BE-DB-08"]
    
  DC-01_任务规划:
    mapped_skills: ["BE-ARCH-01"]
    
  DC-06_方案生成:
    mapped_skills: ["BE-ARCH-02"]
```

## 十、技能使用示例

```python
# 技能使用示例 - 资深后端工程师智能体

class SeniorBackendEngineer(BaseAgent):
    """资深后端工程师智能体 - 具备后端部所有P0技能"""
    
    def __init__(self):
        super().__init__()
        self.skills = self._load_skills()
    
    def _load_skills(self) -> List[Skill]:
        """加载技能（对应P0级能力）"""
        return [
            Skill(id="BE-API-01", name="RESTful API设计", executor=self.design_restful_api),
            Skill(id="BE-API-04", name="API认证授权", executor=self.implement_auth),
            Skill(id="BE-API-05", name="API限流", executor=self.implement_rate_limit),
            Skill(id="BE-API-06", name="API文档生成", executor=self.generate_api_doc),
            Skill(id="BE-API-07", name="API错误处理", executor=self.handle_api_error),
            Skill(id="BE-API-08", name="API请求验证", executor=self.validate_request),
            Skill(id="BE-DB-01", name="数据建模", executor=self.design_data_model),
            Skill(id="BE-DB-02", name="索引设计", executor=self.design_index),
            Skill(id="BE-DB-03", name="SQL优化", executor=self.optimize_sql),
            Skill(id="BE-DB-04", name="数据库迁移", executor=self.migrate_database),
            Skill(id="BE-PERF-01", name="性能分析", executor=self.analyze_performance),
            Skill(id="BE-PERF-02", name="缓存设计", executor=self.design_cache),
            Skill(id="BE-PERF-03", name="异步处理", executor=self.implement_async),
            Skill(id="BE-SEC-01", name="SQL注入防护", executor=self.prevent_sql_injection),
            Skill(id="BE-SEC-04", name="敏感信息脱敏", executor=self.mask_sensitive_data),
            Skill(id="BE-SEC-05", name="密码加密", executor=self.encrypt_password),
            Skill(id="BE-SEC-06", name="密钥管理", executor=self.manage_secrets),
            Skill(id="BE-SEC-07", name="输入验证", executor=self.validate_input),
            Skill(id="BE-TEST-01", name="单元测试编写", executor=self.write_unit_test),
        ]
    
    async def design_restful_api(self, requirement: str) -> API设计:
        """设计RESTful API"""
        # 使用通用能力 EX-03 API调用 和 DC-01 任务规划
        pass
```


## 十一、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```bash
# 查看后端部所有能力
@docs/BACKEND_SKILLS_v1.0.md 列出后端部所有P0级能力

# 实现特定能力（带通用能力映射）
@docs/BACKEND_SKILLS_v1.0.md 实现BE-API-01 RESTful API设计能力，基于EX-03 API调用通用能力

# 创建带技能的后端工程师
@docs/BACKEND_SKILLS_v1.0.md 根据P0能力创建资深后端工程师智能体，继承BaseAgent

# 实现API开发能力集
@docs/BACKEND_SKILLS_v1.0.md 实现category API开发下的所有能力，关联通用能力EX-03和SC-04

# 查看技能与通用能力的映射关系
@docs/BACKEND_SKILLS_v1.0.md 显示EX-03 API调用映射了哪些后端技能
```


## 十二、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，16项后端能力，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md |

---

**文档结束**