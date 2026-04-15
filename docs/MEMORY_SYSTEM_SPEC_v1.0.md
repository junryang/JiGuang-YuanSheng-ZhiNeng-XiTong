# 智能体记忆系统规范 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\MEMORY_SYSTEM_SPEC_v1.0.md
```


# 智能体记忆系统规范 v1.0

## 一、记忆类型总览

```yaml
# 五级记忆架构

memory_types:
  WORKING:
    name: "工作记忆"
    level: "L1"
    description: "当前任务的临时上下文，任务结束后清理"
    
  SHORT_TERM:
    name: "短期记忆"
    level: "L2"
    description: "最近N次对话/任务的记忆，支持时间衰减"
    
  LONG_TERM:
    name: "长期记忆"
    level: "L3"
    description: "重要经验、学习成果的永久存储"
    
  SHARED:
    name: "共享记忆"
    level: "L4"
    description: "团队知识、最佳实践，部门/项目内共享"
    
  GLOBAL:
    name: "全局记忆"
    level: "L5"
    description: "系统级知识、通用规则，所有智能体共享"
```


## 二、工作记忆（Working Memory）

```yaml
memory_type: "WORKING"
name: "工作记忆"
description: "当前任务的临时上下文，任务结束后自动清理"

# 存储配置
storage:
  type: "redis"
  ttl: "任务结束后立即清理"
  max_size: "根据层级配置"
  encoding: "json"

# 按层级容量配置
capacity_by_level:
  L1_CEO: "10MB"
  L2_GM: "8MB"
  L3_PM: "5MB"
  L4_LEAD: "5MB"
  L5_EMP: "2MB"
  L6_INT: "1MB"

# 存储内容结构
content_schema:
  task_id: "string"        # 当前任务ID
  context: "object"        # 任务上下文
  messages: "array"        # 最近对话消息
  temp_vars: "object"      # 临时变量
  status: "string"         # 任务状态

# API接口
apis:
  - name: "set_working_memory"
    method: "POST"
    endpoint: "/api/v1/memory/working"
    request:
      agent_id: "string"
      task_id: "string"
      data: "object"
    response:
      success: "boolean"
      
  - name: "get_working_memory"
    method: "GET"
    endpoint: "/api/v1/memory/working/{agent_id}/{task_id}"
    response:
      data: "object"
      
  - name: "clear_working_memory"
    method: "DELETE"
    endpoint: "/api/v1/memory/working/{agent_id}/{task_id}"
    response:
      success: "boolean"

# 数据模型
data_model:
  WorkingMemory:
    agent_id: str
    task_id: str
    context: dict
    messages: List[dict]
    temp_vars: dict
    status: str
    created_at: datetime
    updated_at: datetime
```


## 三、短期记忆（Short-Term Memory）

```yaml
memory_type: "SHORT_TERM"
name: "短期记忆"
description: "最近N次对话/任务的记忆，支持时间衰减"

# 存储配置
storage:
  type: "vector_database"
  backend: "chroma"
  ttl: "7天（可配置）"
  max_items: "1000条/智能体"
  decay_enabled: true

# 按层级时长配置
ttl_by_level:
  L1_CEO: "7天"
  L2_GM: "7天"
  L3_PM: "5天"
  L4_LEAD: "5天"
  L5_EMP: "3天"
  L6_INT: "1天"

# 衰减策略
decay_strategy:
  type: "exponential"
  half_life: "24小时"
  formula: "score = initial_score * exp(-time / half_life)"

# 存储内容结构
content_schema:
  memory_id: "string"
  agent_id: "string"
  content: "text"
  embedding: "vector(1536)"
  importance: "float"      # 0-1，初始重要性
  score: "float"           # 当前得分（含衰减）
  created_at: "datetime"
  last_accessed: "datetime"
  metadata:
    type: "conversation|task|learning"
    source: "string"
    tags: "array"

# API接口
apis:
  - name: "store_short_term"
    method: "POST"
    endpoint: "/api/v1/memory/short-term"
    request:
      agent_id: "string"
      content: "string"
      importance: "float"
      metadata: "object"
    response:
      memory_id: "string"
      
  - name: "retrieve_short_term"
    method: "POST"
    endpoint: "/api/v1/memory/short-term/retrieve"
    request:
      agent_id: "string"
      query: "string"
      limit: "int"
    response:
      memories: "array"
      
  - name: "decay_short_term"
    method: "POST"
    endpoint: "/api/v1/memory/short-term/decay"
    description: "定时任务，执行记忆衰减"
    
  - name: "cleanup_short_term"
    method: "DELETE"
    endpoint: "/api/v1/memory/short-term/cleanup"
    description: "清理过期记忆"

# 数据模型
data_model:
  ShortTermMemory:
    id: str
    agent_id: str
    content: str
    embedding: List[float]
    importance: float
    score: float
    created_at: datetime
    last_accessed: datetime
    metadata: dict
```


## 四、长期记忆（Long-Term Memory）

```yaml
memory_type: "LONG_TERM"
name: "长期记忆"
description: "重要经验、学习成果的永久存储"

# 存储配置
storage:
  type: "vector_database"
  backend: "chroma"
  ttl: "永久"
  max_items: "无限制"
  importance_threshold: 0.7  # 只有重要性>0.7才转入长期记忆

# 转入条件
promotion_rules:
  - "多次访问的记忆（访问次数>5）"
  - "用户明确标记为重要的记忆"
  - "产生重大成果的经验"
  - "学习到的新技能或知识"
  - "重要性评分持续高于0.7"

# 存储内容结构
content_schema:
  memory_id: "string"
  agent_id: "string"
  content: "text"
  embedding: "vector(1536)"
  importance: "float"       # 0-1，动态更新
  access_count: "int"       # 访问次数
  last_accessed: "datetime"
  created_at: "datetime"
  source: "string"          # 来源：learning/experience/feedback
  lessons: "array"          # 提取的经验教训
  related_memories: "array" # 关联记忆ID

# API接口
apis:
  - name: "store_long_term"
    method: "POST"
    endpoint: "/api/v1/memory/long-term"
    request:
      agent_id: "string"
      content: "string"
      importance: "float"
      source: "string"
    response:
      memory_id: "string"
      
  - name: "retrieve_long_term"
    method: "POST"
    endpoint: "/api/v1/memory/long-term/retrieve"
    request:
      agent_id: "string"
      query: "string"
      limit: "int"
      min_importance: "float"
    response:
      memories: "array"
      
  - name: "update_importance"
    method: "PUT"
    endpoint: "/api/v1/memory/long-term/{memory_id}/importance"
    request:
      delta: "float"
    response:
      new_importance: "float"
      
  - name: "consolidate_memories"
    method: "POST"
    endpoint: "/api/v1/memory/long-term/consolidate"
    description: "记忆巩固：将短期记忆转为长期记忆"

# 数据模型
data_model:
  LongTermMemory:
    id: str
    agent_id: str
    content: str
    embedding: List[float]
    importance: float
    access_count: int
    last_accessed: datetime
    created_at: datetime
    source: str
    lessons: List[str]
    related_memories: List[str]
```


## 五、共享记忆（Shared Memory）

```yaml
memory_type: "SHARED"
name: "共享记忆"
description: "团队知识、最佳实践，部门/项目内共享"

# 存储配置
storage:
  type: "vector_database"
  backend: "chroma"
  ttl: "永久"
  access_control: true

# 共享范围配置
scope_config:
  L1_CEO: "full_system"      # 全系统
  L2_GM: "domain"             # 领域内
  L3_PM: "project"            # 项目内
  L4_LEAD: "department"       # 部门内
  L5_EMP: "team"              # 团队内
  L6_INT: "readonly"          # 只读

# 共享范围映射
scope_mapping:
  full_system:
    name: "全系统"
    visibility: "所有智能体"
    write_permission: ["L1", "L2"]
    
  domain:
    name: "领域内"
    visibility: "同领域智能体"
    write_permission: ["L2", "L3"]
    
  project:
    name: "项目内"
    visibility: "同项目智能体"
    write_permission: ["L3", "L4"]
    
  department:
    name: "部门内"
    visibility: "同部门智能体"
    write_permission: ["L4", "L5"]
    
  team:
    name: "团队内"
    visibility: "同团队智能体"
    write_permission: ["L5"]
    
  readonly:
    name: "只读"
    visibility: "所有智能体可读"
    write_permission: []

# 存储内容结构
content_schema:
  memory_id: "string"
  scope: "string"           # full_system/domain/project/department/team
  creator_id: "string"      # 创建者ID
  content: "text"
  embedding: "vector(1536)"
  category: "string"        # best_practice/knowledge/rule/template
  tags: "array"
  created_at: "datetime"
  updated_at: "datetime"
  version: "int"

# API接口
apis:
  - name: "store_shared_memory"
    method: "POST"
    endpoint: "/api/v1/memory/shared"
    request:
      agent_id: "string"
      scope: "string"
      content: "string"
      category: "string"
      tags: "array"
    response:
      memory_id: "string"
      
  - name: "retrieve_shared_memory"
    method: "POST"
    endpoint: "/api/v1/memory/shared/retrieve"
    request:
      agent_id: "string"
      query: "string"
      scope_filter: "array"
      limit: "int"
    response:
      memories: "array"
      
  - name: "get_shared_memories_by_scope"
    method: "GET"
    endpoint: "/api/v1/memory/shared/scope/{scope}"
    request:
      agent_id: "string" (for permission check)
    response:
      memories: "array"

# 数据模型
data_model:
  SharedMemory:
    id: str
    scope: str
    creator_id: str
    content: str
    embedding: List[float]
    category: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    version: int
```


## 六、全局记忆（Global Memory）

```yaml
memory_type: "GLOBAL"
name: "全局记忆"
description: "系统级知识、通用规则，所有智能体共享"

# 存储配置
storage:
  type: "vector_database"
  backend: "chroma"
  ttl: "永久"
  access_control: false     # 所有智能体可读写

# 写入权限
write_permission:
  - "L1_CEO"
  - "L2_GM"
  - "system_administrator"

# 存储内容结构
content_schema:
  memory_id: "string"
  creator_id: "string"
  content: "text"
  embedding: "vector(1536)"
  category: "string"        # system_rule/universal_knowledge/global_config
  priority: "int"           # 1-10，优先级
  effective_from: "datetime"
  effective_to: "datetime"  # 可选，过期时间
  created_at: "datetime"
  updated_at: "datetime"

# API接口
apis:
  - name: "store_global_memory"
    method: "POST"
    endpoint: "/api/v1/memory/global"
    permission: "L1,L2,admin"
    request:
      agent_id: "string"
      content: "string"
      category: "string"
      priority: "int"
    response:
      memory_id: "string"
      
  - name: "retrieve_global_memory"
    method: "POST"
    endpoint: "/api/v1/memory/global/retrieve"
    request:
      query: "string"
      limit: "int"
    response:
      memories: "array"
      
  - name: "list_global_memories"
    method: "GET"
    endpoint: "/api/v1/memory/global"
    request:
      category: "string" (optional)
    response:
      memories: "array"

# 数据模型
data_model:
  GlobalMemory:
    id: str
    creator_id: str
    content: str
    embedding: List[float]
    category: str
    priority: int
    effective_from: datetime
    effective_to: Optional[datetime]
    created_at: datetime
    updated_at: datetime
```


## 七、记忆操作API汇总

```yaml
# 记忆系统统一API

api_prefix: "/api/v1/memory"

endpoints:
  # 工作记忆
  - path: "/working"
    methods: ["POST", "GET", "DELETE"]
    
  # 短期记忆
  - path: "/short-term"
    methods: ["POST", "GET", "DELETE"]
  - path: "/short-term/retrieve"
    methods: ["POST"]
  - path: "/short-term/decay"
    methods: ["POST"]
    
  # 长期记忆
  - path: "/long-term"
    methods: ["POST", "GET", "DELETE"]
  - path: "/long-term/retrieve"
    methods: ["POST"]
  - path: "/long-term/{id}/importance"
    methods: ["PUT"]
  - path: "/long-term/consolidate"
    methods: ["POST"]
    
  # 共享记忆
  - path: "/shared"
    methods: ["POST", "GET"]
  - path: "/shared/retrieve"
    methods: ["POST"]
  - path: "/shared/scope/{scope}"
    methods: ["GET"]
    
  # 全局记忆
  - path: "/global"
    methods: ["POST", "GET"]
  - path: "/global/retrieve"
    methods: ["POST"]
```


## 八、记忆生命周期流程图

```yaml
# 记忆流转流程

memory_flow:
  - stage: "创建"
    action: "智能体产生新记忆"
    storage: "短期记忆"
    
  - stage: "评估"
    action: "计算重要性评分"
    criteria:
      - "访问频率"
      - "用户反馈"
      - "成果价值"
      
  - stage: "巩固"
    condition: "重要性 > 0.7 且访问次数 > 5"
    action: "转入长期记忆"
    
  - stage: "共享"
    condition: "标记为可共享"
    action: "根据权限发布到共享记忆"
    
  - stage: "全局化"
    condition: "系统级知识"
    action: "管理员审核后发布到全局记忆"
    
  - stage: "衰减"
    action: "短期记忆按时间衰减"
    
  - stage: "遗忘"
    condition: "重要性 < 0.1 或超过TTL"
    action: "自动清理"
```


## 九、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 实现工作记忆
@docs/MEMORY_SYSTEM_SPEC_v1.0.md 实现工作记忆的存储和检索功能

# 实现短期记忆衰减
@docs/MEMORY_SYSTEM_SPEC_v1.0.md 实现短期记忆的指数衰减算法

# 实现记忆巩固
@docs/MEMORY_SYSTEM_SPEC_v1.0.md 实现从短期记忆到长期记忆的巩固机制

# 实现共享记忆权限
@docs/MEMORY_SYSTEM_SPEC_v1.0.md 实现共享记忆的基于层级的访问控制
```

---

**文档结束**