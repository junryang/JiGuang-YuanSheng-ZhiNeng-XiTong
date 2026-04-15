# 项目管理模块 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\PROJECT_MANAGEMENT_MODULE_v1.0.md
```


# 项目管理模块 v1.0

## 一、模块数据模型

```python
# 项目数据模型
class Project:
    id: str                    # 项目ID，格式：JYIS-YYYY-XXX（与 PROJECT_PLAN_TEMPLATE_v1.0.md 一致）
    name: str                  # 项目名称
    plan: ProjectPlan          # 项目计划书
    status: ProjectStatus      # 项目状态
    owner_id: str              # 负责人ID（L3经理）
    domain: str                # 所属领域（D01-D08）
    created_at: datetime       # 创建时间
    updated_at: datetime       # 更新时间
    progress: int              # 进度百分比 0-100
    start_date: date           # 实际开始日期
    end_date: date             # 实际结束日期

# 项目状态枚举
class ProjectStatus:
    DRAFT = "draft"            # 草稿
    PENDING_APPROVAL = "pending_approval"  # 待审批
    APPROVED = "approved"      # 已批准
    REJECTED = "rejected"      # 已驳回
    IN_PROGRESS = "in_progress" # 进行中
    COMPLETED = "completed"    # 已完成
    CANCELLED = "cancelled"    # 已取消

# 项目计划书数据模型
class ProjectPlan:
    project_name: str          # 项目名称
    project_code: str          # 项目编号
    domain: str                # 所属领域
    project_type: str          # 类型：new_feature/optimization/bug_fix
    goals: ProjectGoals        # 项目目标
    scope: ProjectScope        # 项目范围
    resources: ResourceRequest  # 资源需求
    schedule: ProjectSchedule   # 时间计划
    risks: RiskAssessment       # 风险评估
    budget: Budget              # 预算

# 项目目标
class ProjectGoals:
    business: List[str]        # 业务目标列表
    technical: List[str]       # 技术目标列表
    kpi: List[KPI]             # 成功指标列表

# KPI定义
class KPI:
    name: str                  # 指标名称
    target: str                # 目标值
    measure: str               # 测量方式

# 项目范围
class ProjectScope:
    includes: List[str]        # 包含功能列表
    excludes: List[str]        # 不包含功能列表

# 资源需求
class ResourceRequest:
    agents: Dict[str, Dict[str, int]]  # 智能体需求
    compute: ComputeResource          # 计算资源
    external: List[str]               # 外部依赖

# 计算资源
class ComputeResource:
    cpu: str                   # CPU规格
    memory: str                # 内存规格
    gpu: str                   # GPU规格
    storage: str               # 存储规格

# 时间计划
class ProjectSchedule:
    start_date: date           # 计划开始日期
    end_date: date             # 计划结束日期
    milestones: List[Milestone] # 里程碑列表

# 里程碑
class Milestone:
    name: str                  # 里程碑名称
    date: date                 # 目标日期
    deliverable: str           # 交付物
    acceptance_criteria: str   # 验收标准

# 风险评估
class RiskAssessment:
    technical: List[Risk]      # 技术风险
    resource: List[Risk]       # 资源风险
    mitigation: List[str]      # 应对措施

# 风险
class Risk:
    description: str           # 风险描述
    probability: str           # 概率：high/medium/low
    impact: str                # 影响：high/medium/low

# 预算
class Budget:
    development: float         # 开发成本
    operation: float           # 运营成本
    total: float               # 总预算
```


## 二、功能详细定义

### 2.1 PM-01 项目创建

```yaml
# PM-01 项目创建
function_id: "PM-01"
name: "项目创建"
description: "创建新项目，填写项目计划书"
priority: "P0"
assigned_to: "L3 经理"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/projects"
    request_body: "ProjectPlan"
    response: "Project"

# 前端页面
frontend:
  page: "/projects/create"
  component: "ProjectCreate.vue"
  fields:
    - name: "基本信息表单"
      fields: ["项目名称", "项目类型", "所属领域"]
    - name: "项目目标表单"
      fields: ["业务目标", "技术目标", "KPI"]
    - name: "项目范围表单"
      fields: ["包含功能", "不包含功能"]
    - name: "资源需求表单"
      fields: ["智能体人力", "计算资源", "外部依赖"]
    - name: "时间计划表单"
      fields: ["开始日期", "结束日期", "里程碑"]
    - name: "风险评估表单"
      fields: ["技术风险", "资源风险", "应对措施"]
    - name: "预算表单"
      fields: ["开发成本", "运营成本"]

# 业务规则
business_rules:
  - "项目名称不能为空，长度2-100字符"
  - "项目编号自动生成，格式：JYIS-YYYY-XXX"
  - "项目类型必须选择"
  - "开始日期不能晚于结束日期"
  - "里程碑至少包含1个"
  - "创建后状态为 draft"

# 错误处理
error_handling:
  - code: "PM-01-001"
    message: "项目名称不能为空"
  - code: "PM-01-002"
    message: "开始日期不能晚于结束日期"
  - code: "PM-01-003"
    message: "至少需要设置一个里程碑"
```


### 2.2 PM-02 项目立项

```yaml
# PM-02 项目立项
function_id: "PM-02"
name: "项目立项"
description: "CEO审批项目立项申请"
priority: "P0"
assigned_to: "L1 CEO（主脑）"

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/projects/{project_id}/submit"
    description: "提交审批"
    response: "提交结果"
    
  - method: "GET"
    endpoint: "/api/v1/projects/pending-approvals"
    description: "获取待审批项目列表"
    response: "List[Project]"
    
  - method: "POST"
    endpoint: "/api/v1/projects/{project_id}/approve"
    description: "批准项目"
    request_body: 
      comment: "审批意见"
    response: "审批结果"
    
  - method: "POST"
    endpoint: "/api/v1/projects/{project_id}/reject"
    description: "驳回项目"
    request_body:
      comment: "驳回原因"
    response: "驳回结果"

# 审批流程
approval_workflow:
  - step: 1
    level: "L3"
    approver: "经理（项目负责人）"
    action: "提交审批"
    
  - step: 2
    level: "L2"
    approver: "总经理（领域负责人）"
    action: "初审"
    
  - step: 3
    level: "L1"
    approver: "CEO（主脑）"
    action: "终审"
    
  - step: 4
    level: "L0"
    approver: "老板"
    action: "最终批准（可选，预算超限时触发）"

# 审批规则
approval_rules:
  - "项目预算 < 5万：L3审批即可"
  - "项目预算 5-20万：需L2+L3审批"
  - "项目预算 > 20万：需L1+L2+L3审批"
  - "项目涉及跨领域：需L1审批"
  - "项目涉及外部数据安全：需L0审批"

# 前端页面
frontend:
  page: "/projects/approvals"
  component: "ProjectApproval.vue"
  features:
    - "待审批项目列表"
    - "项目计划书预览"
    - "风险评估可视化"
    - "审批意见输入"
    - "批准/驳回按钮"
```


### 2.3 PM-03 任务分解

```yaml
# PM-03 任务分解
function_id: "PM-03"
name: "任务分解"
description: "经理将项目分解为可执行任务"
priority: "P0"
assigned_to: "L3 经理"

# 任务数据模型
class Task:
    id: str                    # 任务ID
    project_id: str            # 所属项目ID
    name: str                  # 任务名称
    description: str           # 任务描述
    priority: str              # 优先级：P0/P1/P2/P3
    status: TaskStatus         # 任务状态
    progress: int              # 进度 0-100
    parent_id: str             # 父任务ID（支持层级）
    assignee_level: str        # 指派的层级
    assignee_role: str         # 指派的岗位
    estimated_hours: float     # 预估工时
    actual_hours: float        # 实际工时
    dependencies: List[str]    # 依赖任务ID列表
    start_date: date           # 计划开始日期
    end_date: date             # 计划结束日期
    completed_at: datetime     # 实际完成时间

# 任务状态枚举
class TaskStatus:
    PENDING = "pending"        # 待开始
    ASSIGNED = "assigned"      # 已指派
    IN_PROGRESS = "in_progress" # 进行中
    COMPLETED = "completed"    # 已完成
    FAILED = "failed"          # 失败
    CANCELLED = "cancelled"    # 已取消

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/projects/{project_id}/tasks/decompose"
    description: "AI辅助任务分解"
    request_body:
      project_plan: "ProjectPlan"
    response: "List[Task]"
    
  - method: "GET"
    endpoint: "/api/v1/projects/{project_id}/tasks"
    description: "获取项目任务列表"
    response: "List[Task]"
    
  - method: "POST"
    endpoint: "/api/v1/projects/{project_id}/tasks"
    description: "手动创建任务"
    request_body: "Task"
    response: "Task"
    
  - method: "PUT"
    endpoint: "/api/v1/tasks/{task_id}"
    description: "更新任务"
    request_body: "Task"
    response: "Task"
    
  - method: "DELETE"
    endpoint: "/api/v1/tasks/{task_id}"
    description: "删除任务"

# AI任务分解规则
ai_decompose_rules:
  - "根据项目目标自动生成顶层任务"
  - "根据技术目标生成技术任务"
  - "根据资源需求生成资源配置任务"
  - "根据里程碑生成关键节点任务"
  - "自动识别任务间的依赖关系"
  - "自动预估任务工时（基于历史数据）"

# 前端页面
frontend:
  page: "/projects/{project_id}/tasks"
  component: "TaskDecompose.vue"
  features:
    - "WBS树形结构展示"
    - "拖拽调整任务层级"
    - "任务详情编辑"
    - "依赖关系连线"
    - "AI辅助分解按钮"
    - "工时预估"
    - "任务指派"
```


### 2.4 PM-04 进度跟踪

```yaml
# PM-04 进度跟踪
function_id: "PM-04"
name: "进度跟踪"
description: "实时查看项目进度"
priority: "P0"
assigned_to: "L3 经理, L4 主管, L5 员工"

# 进度数据模型
class Progress:
    project_id: str            # 项目ID
    overall_progress: int      # 整体进度 0-100
    task_completion: int       # 任务完成数/总数
    time_elapsed: float        # 已用时间（天）
    time_remaining: float      # 剩余时间（天）
    health_status: str         # 健康状态：on_track/at_risk/delayed
    risks: List[Risk]          # 当前风险列表
    updated_at: datetime       # 最后更新时间

# API接口
api:
  - method: "GET"
    endpoint: "/api/v1/projects/{project_id}/progress"
    description: "获取项目进度"
    response: "Progress"
    
  - method: "GET"
    endpoint: "/api/v1/projects/{project_id}/gantt"
    description: "获取甘特图数据"
    response: "GanttData"
    
  - method: "POST"
    endpoint: "/api/v1/tasks/{task_id}/progress"
    description: "更新任务进度"
    request_body:
      progress: "int"
      comment: "string"
    response: "Task"
    
  - method: "GET"
    endpoint: "/api/v1/projects/dashboard"
    description: "获取项目仪表盘数据"
    response: "DashboardData"

# 进度计算规则
progress_rules:
  - "项目整体进度 = 加权平均(任务进度 × 任务权重)"
  - "任务权重 = 预估工时 / 项目总工时"
  - "时间偏差 = (实际已用时间 - 计划已用时间) / 计划总时间"
  - "健康状态判断：偏差<10% = on_track, 10%-20% = at_risk, >20% = delayed"

# WebSocket实时推送
websocket:
  - endpoint: "/ws/projects/{project_id}/progress"
    events:
      - "task_progress_updated"
      - "task_status_changed"
      - "milestone_reached"
      - "risk_detected"

# 前端页面
frontend:
  page: "/projects/{project_id}/progress"
  component: "ProjectProgress.vue"
  features:
    - "进度仪表盘（KPI卡片）"
    - "甘特图可视化"
    - "燃尽图"
    - "任务列表（按状态分组）"
    - "进度更新表单"
    - "风险预警提示"
    - "实时WebSocket更新"
```


### 2.5 PM-05 项目复盘

```yaml
# PM-05 项目复盘
function_id: "PM-05"
name: "项目复盘"
description: "项目完成后生成复盘报告"
priority: "P1"
assigned_to: "L3 经理"

# 复盘报告数据模型
class ReviewReport:
    project_id: str            # 项目ID
    project_name: str          # 项目名称
    generated_at: datetime     # 生成时间
    generated_by: str          # 生成人ID
    
    # 完成情况
    completion:
      status: str              # 状态：success/partial/failed
      completion_rate: float   # 完成率 %
      kpi_achievement: Dict    # KPI达成情况
    
    # 时间分析
    time_analysis:
      planned_days: int        # 计划天数
      actual_days: int         # 实际天数
      variance_days: int       # 偏差天数
      variance_rate: float     # 偏差率 %
    
    # 成本分析
    cost_analysis:
      planned_cost: float      # 计划成本
      actual_cost: float       # 实际成本
      variance: float          # 偏差
      variance_rate: float     # 偏差率 %
    
    # 问题总结
    issues:
      - type: str              # 类型：技术/资源/管理
        description: str       # 问题描述
        root_cause: str        # 根本原因
        solution: str          # 解决方案
    
    # 经验教训
    lessons:
      - type: str              # 类型：成功经验/失败教训
        content: str           # 内容
        action_item: str       # 改进措施
    
    # 团队表现
    team_performance:
      - role: str              # 角色
        name: str              # 智能体名称
        contribution: str      # 贡献
        rating: float          # 评分 1-5

# API接口
api:
  - method: "POST"
    endpoint: "/api/v1/projects/{project_id}/review/generate"
    description: "生成复盘报告"
    response: "ReviewReport"
    
  - method: "GET"
    endpoint: "/api/v1/projects/{project_id}/review"
    description: "获取复盘报告"
    response: "ReviewReport"
    
  - method: "PUT"
    endpoint: "/api/v1/projects/{project_id}/review"
    description: "更新复盘报告"
    request_body: "ReviewReport"
    
  - method: "POST"
    endpoint: "/api/v1/projects/{project_id}/review/export"
    description: "导出复盘报告"
    request_body:
      format: "pdf|md|json"
    response: "file"

# AI复盘分析规则
ai_review_rules:
  - "对比计划与实际的时间差异，分析原因"
  - "对比计划与实际成本，分析超支原因"
  - "分析任务完成率与预估工时的准确性"
  - "识别项目中的关键成功因素"
  - "识别项目中的主要障碍和风险"
  - "从问题中提炼可复用的经验教训"
  - "评估团队协作效率"

# 前端页面
frontend:
  page: "/projects/{project_id}/review"
  component: "ProjectReview.vue"
  features:
    - "复盘报告预览"
    - "KPI达成情况图表"
    - "时间偏差分析图"
    - "成本偏差分析图"
    - "问题清单（可编辑）"
    - "经验教训（可编辑）"
    - "团队表现评分"
    - "导出按钮（PDF/Markdown）"
    - "知识库保存按钮"
```


## 三、API接口汇总

```yaml
# 项目管理模块API汇总

api_summary:
  base_path: "/api/v1"
  
  projects:
    - method: "POST"
      path: "/projects"
      function: "PM-01"
      description: "创建项目"
      
    - method: "GET"
      path: "/projects"
      function: "PM-01/PM-04"
      description: "获取项目列表"
      
    - method: "GET"
      path: "/projects/{id}"
      function: "PM-01/PM-04"
      description: "获取项目详情"
      
    - method: "PUT"
      path: "/projects/{id}"
      function: "PM-01"
      description: "更新项目"
      
    - method: "DELETE"
      path: "/projects/{id}"
      function: "PM-01"
      description: "删除项目"
      
    - method: "POST"
      path: "/projects/{id}/submit"
      function: "PM-02"
      description: "提交审批"
      
    - method: "GET"
      path: "/projects/pending-approvals"
      function: "PM-02"
      description: "待审批列表"
      
    - method: "POST"
      path: "/projects/{id}/approve"
      function: "PM-02"
      description: "批准项目"
      
    - method: "POST"
      path: "/projects/{id}/reject"
      function: "PM-02"
      description: "驳回项目"
      
    - method: "GET"
      path: "/projects/{id}/progress"
      function: "PM-04"
      description: "获取进度"
      
    - method: "GET"
      path: "/projects/{id}/gantt"
      function: "PM-04"
      description: "获取甘特图"
      
    - method: "POST"
      path: "/projects/{id}/review/generate"
      function: "PM-05"
      description: "生成复盘报告"
      
    - method: "GET"
      path: "/projects/{id}/review"
      function: "PM-05"
      description: "获取复盘报告"
      
    - method: "POST"
      path: "/projects/{id}/review/export"
      function: "PM-05"
      description: "导出复盘报告"
      
  tasks:
    - method: "POST"
      path: "/projects/{id}/tasks/decompose"
      function: "PM-03"
      description: "AI任务分解"
      
    - method: "GET"
      path: "/projects/{id}/tasks"
      function: "PM-03"
      description: "获取任务列表"
      
    - method: "POST"
      path: "/projects/{id}/tasks"
      function: "PM-03"
      description: "创建任务"
      
    - method: "PUT"
      path: "/tasks/{id}"
      function: "PM-03"
      description: "更新任务"
      
    - method: "DELETE"
      path: "/tasks/{id}"
      function: "PM-03"
      description: "删除任务"
      
    - method: "POST"
      path: "/tasks/{id}/progress"
      function: "PM-04"
      description: "更新任务进度"
```


## 四、前端页面路由

```yaml
# 前端页面路由

frontend_routes:
  - path: "/projects"
    name: "ProjectList"
    component: "ProjectList.vue"
    description: "项目列表页"
    
  - path: "/projects/create"
    name: "ProjectCreate"
    component: "ProjectCreate.vue"
    description: "创建项目页（PM-01）"
    
  - path: "/projects/approvals"
    name: "ProjectApprovals"
    component: "ProjectApproval.vue"
    description: "项目审批页（PM-02）"
    
  - path: "/projects/{id}"
    name: "ProjectDetail"
    component: "ProjectDetail.vue"
    description: "项目详情页"
    
  - path: "/projects/{id}/tasks"
    name: "TaskDecompose"
    component: "TaskDecompose.vue"
    description: "任务分解页（PM-03）"
    
  - path: "/projects/{id}/progress"
    name: "ProjectProgress"
    component: "ProjectProgress.vue"
    description: "进度跟踪页（PM-04）"
    
  - path: "/projects/{id}/review"
    name: "ProjectReview"
    component: "ProjectReview.vue"
    description: "项目复盘页（PM-05）"
```


## 五、WebSocket事件

```yaml
# WebSocket实时事件

websocket_events:
  - event: "project.created"
    payload:
      project_id: "string"
      project_name: "string"
      
  - event: "project.approved"
    payload:
      project_id: "string"
      approver: "string"
      comment: "string"
      
  - event: "task.progress.updated"
    payload:
      task_id: "string"
      project_id: "string"
      progress: "int"
      updated_by: "string"
      
  - event: "task.status.changed"
    payload:
      task_id: "string"
      old_status: "string"
      new_status: "string"
      
  - event: "milestone.reached"
    payload:
      project_id: "string"
      milestone_name: "string"
      date: "string"
      
  - event: "risk.detected"
    payload:
      project_id: "string"
      risk_description: "string"
      severity: "high|medium|low"
```


## 六、在Cursor中使用

```bash
# 1. 创建项目管理模块
@docs/PROJECT_MANAGEMENT_MODULE_v1.0.md 实现PM-01项目创建功能

# 2. 实现审批流程
@docs/PROJECT_MANAGEMENT_MODULE_v1.0.md 实现PM-02项目立项审批流程，包括L1/L2/L3三级审批

# 3. 实现任务分解
@docs/PROJECT_MANAGEMENT_MODULE_v1.0.md 实现PM-03任务分解，支持WBS树形结构和AI辅助分解

# 4. 实现进度跟踪
@docs/PROJECT_MANAGEMENT_MODULE_v1.0.md 实现PM-04进度跟踪，包括甘特图和WebSocket实时更新

# 5. 实现复盘报告
@docs/PROJECT_MANAGEMENT_MODULE_v1.0.md 实现PM-05项目复盘，自动生成复盘报告
```


## 七、数据库表结构

```sql
-- 项目表
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    plan JSONB NOT NULL,
    status VARCHAR(50) NOT NULL,
    owner_id UUID REFERENCES agents(id),
    domain VARCHAR(10) NOT NULL,
    progress INTEGER DEFAULT 0,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 任务表
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(10) NOT NULL,
    status VARCHAR(50) NOT NULL,
    progress INTEGER DEFAULT 0,
    parent_id UUID REFERENCES tasks(id),
    assignee_level VARCHAR(10),
    assignee_role VARCHAR(50),
    estimated_hours DECIMAL(8,2),
    actual_hours DECIMAL(8,2),
    dependencies UUID[],
    start_date DATE,
    end_date DATE,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- 审批记录表
CREATE TABLE project_approvals (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    level VARCHAR(10) NOT NULL,
    approver_id UUID REFERENCES agents(id),
    approved BOOLEAN NOT NULL,
    comment TEXT,
    created_at TIMESTAMP NOT NULL
);

-- 复盘报告表
CREATE TABLE project_reviews (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id) UNIQUE,
    report JSONB NOT NULL,
    generated_by UUID REFERENCES agents(id),
    generated_at TIMESTAMP NOT NULL
);
```


**文档结束**