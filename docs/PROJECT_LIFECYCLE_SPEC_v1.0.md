# 项目生命周期阶段规范 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\PROJECT_LIFECYCLE_SPEC_v1.0.md
```


# 项目生命周期阶段规范 v1.0

## 一、阶段总览

> 裁决说明：涉及测试覆盖率门槛冲突时，以 `docs/quality_standards.md` 为基线。

```yaml
# 项目生命周期9个阶段

project_lifecycle:
  total_stages: 9
  stages:
    - id: "P01"
      name: "市场调研"
      phase: "planning"
      
    - id: "P02"
      name: "需求分析"
      phase: "planning"
      
    - id: "P03"
      name: "项目计划书"
      phase: "planning"
      
    - id: "P04"
      name: "立项审批"
      phase: "approval"
      
    - id: "P05"
      name: "技术方案"
      phase: "design"
      
    - id: "P06"
      name: "开发执行"
      phase: "execution"
      
    - id: "P07"
      name: "测试验收"
      phase: "testing"
      
    - id: "P08"
      name: "部署上线"
      phase: "deployment"
      
    - id: "P09"
      name: "项目复盘"
      phase: "review"
```


## 二、阶段详细定义

### 2.1 P01 市场调研

```yaml
stage:
  id: "P01"
  name: "市场调研"
  phase: "planning"
  order: 1
  
  # 负责人配置
  owner:
    role: "营销主管"
    level: "L4"
    department: "营销部"
  
  # 参与角色
  participants:
    - role: "营销主管"
      level: "L4"
      responsibility: "组织调研，审核报告"
    - role: "资深内容运营"
      level: "L5"
      responsibility: "执行调研，收集数据"
    - role: "实习运营助理"
      level: "L6"
      responsibility: "整理数据，协助分析"
  
  # 产出物定义
  deliverables:
    - name: "市场分析报告"
      type: "document"
      template: "market_analysis_report_template.md"
      required: true
      schema:
        title: "string"
        date: "date"
        author: "string"
        executive_summary: "string"
        market_size: "object"
        competition_analysis: "array"
        target_audience: "array"
        swot_analysis: "object"
        recommendations: "array"
  
  # 审批配置
  approval:
    required: true
    approver:
      role: "总经理"
      level: "L2"
    timeout_hours: 48
    auto_approve_if_no_response: false
  
  # 输入依赖
  input_dependencies:
    - type: "external_data"
      source: "市场数据API"
      required: true
  
  # 超时配置
  timeout_days: 5
  
  # 状态流转
  status_flow:
    - "pending"      # 待开始
    - "in_progress"  # 进行中
    - "review"       # 审核中
    - "approved"     # 已通过
    - "rejected"     # 已驳回
    - "completed"    # 已完成
```


### 2.2 P02 需求分析

```yaml
stage:
  id: "P02"
  name: "需求分析"
  phase: "planning"
  order: 2
  
  owner:
    role: "产品主管"
    level: "L4"
    department: "产品部"
  
  participants:
    - role: "产品主管"
      level: "L4"
      responsibility: "组织需求分析，审核需求文档"
    - role: "资深产品经理"
      level: "L5"
      responsibility: "执行需求分析，编写需求文档"
    - role: "实习产品助理"
      level: "L6"
      responsibility: "整理需求，协助编写文档"
  
  deliverables:
    - name: "需求规格说明书"
      type: "document"
      template: "prd_template.md"
      required: true
      schema:
        title: "string"
        version: "string"
        creation_date: "date"
        authors: "array"
        stakeholders: "array"
        background: "string"
        goals: "array"
        functional_requirements: "array"
        non_functional_requirements: "array"
        user_stories: "array"
        acceptance_criteria: "array"
  
  approval:
    required: true
    approver:
      role: "总经理"
      level: "L2"
    timeout_hours: 48
  
  timeout_days: 5
```


### 2.3 P03 项目计划书

```yaml
stage:
  id: "P03"
  name: "项目计划书"
  phase: "planning"
  order: 3
  
  owner:
    role: "经理"
    level: "L3"
    department: "项目管理部"
  
  participants:
    - role: "经理"
      level: "L3"
      responsibility: "制定项目计划"
    - role: "各主管"
      level: "L4"
      responsibility: "提供部门资源估算"
    - role: "各员工"
      level: "L5"
      responsibility: "提供任务时间估算"
  
  deliverables:
    - name: "项目计划书"
      type: "document"
      template: "project_plan_template.md"
      required: true
      schema:
        project_name: "string"
        project_id: "string"
        version: "string"
        creation_date: "date"
        project_manager: "string"
        executive_summary: "string"
        scope: "object"
        schedule: "object"
        resources: "object"
        budget: "object"
        risk_management: "object"
        communication_plan: "object"
        quality_plan: "object"
  
  approval:
    required: true
    approver:
      role: "CEO"
      level: "L1"
    timeout_hours: 72
    required_documents:
      - "需求规格说明书"
  
  timeout_days: 3
```


### 2.4 P04 立项审批

```yaml
stage:
  id: "P04"
  name: "立项审批"
  phase: "approval"
  order: 4
  
  owner:
    role: "CEO"
    level: "L1"
    department: "决策层"
  
  participants:
    - role: "CEO"
      level: "L1"
      responsibility: "审批立项"
    - role: "老板"
      level: "L0"
      responsibility: "最终审批（预算超限时）"
  
  deliverables:
    - name: "立项决议"
      type: "document"
      template: "approval_decision_template.md"
      required: true
      schema:
        project_id: "string"
        decision: "enum(approved,rejected,need_modification)"
        approval_date: "date"
        approver: "string"
        comments: "string"
        conditions: "array"
  
  approval:
    required: true
    approver:
      role: "老板"
      level: "L0"
      condition: "budget > 100000"
    default_approver:
      role: "CEO"
      level: "L1"
  
  timeout_days: 2
```


### 2.5 P05 技术方案

```yaml
stage:
  id: "P05"
  name: "技术方案"
  phase: "design"
  order: 5
  
  owner:
    role: "架构师/主管"
    level: "L4"
    department: "相关技术部门"
  
  participants:
    - role: "架构师"
      level: "L4"
      responsibility: "设计整体技术架构"
    - role: "各主管"
      level: "L4"
      responsibility: "设计子模块技术方案"
    - role: "资深工程师"
      level: "L5"
      responsibility: "技术调研和验证"
  
  deliverables:
    - name: "技术架构设计文档"
      type: "document"
      template: "tech_architecture_template.md"
      required: true
      schema:
        title: "string"
        version: "string"
        authors: "array"
        overview: "string"
        architecture_diagram: "string"
        tech_stack: "array"
        module_design: "array"
        database_design: "object"
        api_design: "object"
        security_design: "object"
        deployment_plan: "object"
  
  approval:
    required: true
    approver:
      role: "总经理"
      level: "L2"
    timeout_hours: 48
  
  timeout_days: 7
```


### 2.6 P06 开发执行

```yaml
stage:
  id: "P06"
  name: "开发执行"
  phase: "execution"
  order: 6
  
  owner:
    role: "各员工"
    level: "L5"
    department: "各技术部门"
  
  participants:
    - role: "员工"
      level: "L5"
      responsibility: "执行开发任务"
    - role: "实习"
      level: "L6"
      responsibility: "辅助开发"
    - role: "主管"
      level: "L4"
      responsibility: "任务分配和质量把控"
    - role: "经理"
      level: "L3"
      responsibility: "进度跟踪"
  
  deliverables:
    - name: "代码"
      type: "code"
      required: true
      quality_gates:
        - "全局测试覆盖率≥80%，核心模块按quality_standards的更高门槛执行"
        - "代码规范检查通过"
        - "无高危安全漏洞"
    
    - name: "技术文档"
      type: "document"
      required: true
    
    - name: "单元测试"
      type: "test"
      required: true
  
  approval:
    required: false
    # 代码审查由主管执行，不需要正式审批
  
  timeout_days: "根据项目规模动态配置"
  
  # 子任务类型
  sub_task_types:
    - name: "编码"
      assignee: "员工"
    - name: "代码审查"
      assignee: "主管"
    - name: "文档编写"
      assignee: "员工"
    - name: "单元测试"
      assignee: "员工"
```


### 2.7 P07 测试验收

```yaml
stage:
  id: "P07"
  name: "测试验收"
  phase: "testing"
  order: 7
  
  owner:
    role: "测试主管"
    level: "L4"
    department: "测试部"
  
  participants:
    - role: "测试主管"
      level: "L4"
      responsibility: "组织测试，审核测试报告"
    - role: "资深测试工程师"
      level: "L5"
      responsibility: "执行测试"
    - role: "实习测试助理"
      level: "L6"
      responsibility: "辅助测试"
  
  deliverables:
    - name: "测试报告"
      type: "document"
      template: "test_report_template.md"
      required: true
      schema:
        project_id: "string"
        test_date: "date"
        test_summary: "object"
        test_cases: "array"
        bug_list: "array"
        coverage_report: "object"
        performance_report: "object"
        security_report: "object"
        conclusion: "enum(pass,fail,conditional_pass)"
        recommendations: "array"
  
  approval:
    required: true
    approver:
      role: "经理"
      level: "L3"
    timeout_hours: 24
  
  timeout_days: 5
  
  # 测试类型
  test_types:
    - "单元测试"
    - "集成测试"
    - "功能测试"
    - "性能测试"
    - "安全测试"
    - "用户验收测试"
```


### 2.8 P08 部署上线

```yaml
stage:
  id: "P08"
  name: "部署上线"
  phase: "deployment"
  order: 8
  
  owner:
    role: "运维主管"
    level: "L4"
    department: "运维部"
  
  participants:
    - role: "运维主管"
      level: "L4"
      responsibility: "组织部署"
    - role: "资深运维工程师"
      level: "L5"
      responsibility: "执行部署"
    - role: "开发员工"
      level: "L5"
      responsibility: "配合部署和验证"
  
  deliverables:
    - name: "部署文档"
      type: "document"
      template: "deployment_guide_template.md"
      required: true
    
    - name: "上线确认单"
      type: "document"
      template: "deployment_confirmation_template.md"
      required: true
      schema:
        project_id: "string"
        deployment_date: "date"
        environment: "enum(dev,test,staging,production)"
        version: "string"
        deployment_status: "enum(success,failed,rollback)"
        verification_results: "array"
        rollback_plan: "object"
        approver: "string"
  
  approval:
    required: true
    approver:
      role: "总经理"
      level: "L2"
    timeout_hours: 24
  
  # 部署策略
  deployment_strategies:
    - "滚动更新"
    - "蓝绿部署"
    - "金丝雀发布"
    - "A/B测试"
  
  timeout_days: 2
```


### 2.9 P09 项目复盘

```yaml
stage:
  id: "P09"
  name: "项目复盘"
  phase: "review"
  order: 9
  
  owner:
    role: "经理"
    level: "L3"
    department: "项目管理部"
  
  participants:
    - role: "经理"
      level: "L3"
      responsibility: "组织复盘会议"
    - role: "各主管"
      level: "L4"
      responsibility: "总结部门经验"
    - role: "各员工"
      level: "L5"
      responsibility: "提供个人总结"
  
  deliverables:
    - name: "复盘报告"
      type: "document"
      template: "retrospective_report_template.md"
      required: true
      schema:
        project_id: "string"
        review_date: "date"
        participants: "array"
        what_went_well: "array"
        what_went_wrong: "array"
        lessons_learned: "array"
        action_items: "array"
        metrics: "object"
        attachments: "array"
  
  approval:
    required: true
    approver:
      role: "CEO"
      level: "L1"
    timeout_hours: 72
  
  # 经验沉淀
  knowledge_extraction:
    - destination: "共享记忆"
      type: "best_practice"
    - destination: "技能库"
      type: "skill_update"
  
  timeout_days: 3
```


## 三、阶段数据模型

```python
# models/project_stage.py

from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class StageStatus(str, Enum):
    """阶段状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class StagePhase(str, Enum):
    """阶段阶段"""
    PLANNING = "planning"
    APPROVAL = "approval"
    DESIGN = "design"
    EXECUTION = "execution"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    REVIEW = "review"


class Deliverable(BaseModel):
    """产出物"""
    name: str
    type: str  # document/code/test/config
    template: Optional[str] = None
    required: bool = True
    schema: Optional[Dict[str, Any]] = None
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Approval(BaseModel):
    """审批配置"""
    required: bool = True
    approver_role: str
    approver_level: str
    timeout_hours: int = 48
    auto_approve_if_no_response: bool = False
    condition: Optional[str] = None
    default_approver_role: Optional[str] = None


class Participant(BaseModel):
    """参与者"""
    role: str
    level: str
    responsibility: str


class ProjectStage(BaseModel):
    """项目阶段"""
    id: str
    name: str
    phase: StagePhase
    order: int
    
    # 负责人
    owner_role: str
    owner_level: str
    owner_department: str
    
    # 参与者
    participants: List[Participant] = Field(default_factory=list)
    
    # 产出物
    deliverables: List[Deliverable] = Field(default_factory=list)
    
    # 审批
    approval: Approval
    
    # 配置
    timeout_days: int
    status_flow: List[str] = Field(default_factory=list)
    
    # 实际数据
    project_id: str
    status: StageStatus = StageStatus.PENDING
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    actual_deliverables: List[Deliverable] = Field(default_factory=list)
    comments: Optional[str] = None
```


## 四、阶段流转引擎

```python
# services/stage_engine.py

from typing import Optional
from datetime import datetime, timedelta


class StageEngine:
    """阶段流转引擎"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.stages = self._load_stages(project_id)
    
    def can_transition(self, from_stage_id: str, to_stage_id: str) -> bool:
        """检查是否可以流转"""
        # 获取当前阶段
        current_stage = self._get_stage(from_stage_id)
        
        # 检查当前阶段是否已完成
        if current_stage.status != StageStatus.COMPLETED:
            return False
        
        # 检查目标阶段的前置条件
        target_stage = self._get_stage(to_stage_id)
        
        # 检查产出物是否齐全
        for deliverable in target_stage.deliverables:
            if deliverable.required and not self._has_deliverable(deliverable.name):
                return False
        
        # 检查审批是否通过
        if target_stage.approval.required:
            if not self._is_approved(target_stage.id):
                return False
        
        return True
    
    def start_stage(self, stage_id: str) -> bool:
        """开始阶段"""
        stage = self._get_stage(stage_id)
        
        if stage.status != StageStatus.PENDING:
            return False
        
        stage.status = StageStatus.IN_PROGRESS
        stage.start_date = datetime.now()
        
        self._save_stage(stage)
        return True
    
    def complete_stage(self, stage_id: str, 
                       deliverables: List[Deliverable]) -> bool:
        """完成阶段"""
        stage = self._get_stage(stage_id)
        
        if stage.status != StageStatus.IN_PROGRESS:
            return False
        
        # 验证产出物
        if not self._validate_deliverables(stage, deliverables):
            return False
        
        stage.status = StageStatus.COMPLETED
        stage.end_date = datetime.now()
        stage.actual_deliverables = deliverables
        
        self._save_stage(stage)
        
        # 自动触发下一阶段
        self._auto_trigger_next_stage(stage_id)
        
        return True
    
    def _validate_deliverables(self, stage: ProjectStage, 
                               deliverables: List[Deliverable]) -> bool:
        """验证产出物"""
        required_names = [d.name for d in stage.deliverables if d.required]
        actual_names = [d.name for d in deliverables]
        
        for required in required_names:
            if required not in actual_names:
                return False
        return True
    
    def _auto_trigger_next_stage(self, current_stage_id: str):
        """自动触发下一阶段"""
        next_order = self._get_stage(current_stage_id).order + 1
        next_stage = self._get_stage_by_order(next_order)
        
        if next_stage:
            self.start_stage(next_stage.id)
```


## 五、阶段API接口

```yaml
api_prefix: "/api/v1/projects/{project_id}/stages"

endpoints:
  # 阶段管理
  - path: "/"
    method: "GET"
    description: "获取所有阶段状态"
    response: "List[ProjectStage]"
    
  - path: "/{stage_id}"
    method: "GET"
    description: "获取阶段详情"
    response: "ProjectStage"
    
  - path: "/{stage_id}/start"
    method: "POST"
    description: "开始阶段"
    response: "success"
    
  - path: "/{stage_id}/complete"
    method: "POST"
    description: "完成阶段"
    request: 
      deliverables: "List[Deliverable]"
    response: "success"
    
  - path: "/{stage_id}/approve"
    method: "POST"
    description: "审批阶段"
    request:
      approved: "boolean"
      comments: "string"
    response: "success"
    
  - path: "/{stage_id}/deliverables"
    method: "GET"
    description: "获取阶段产出物"
    response: "List[Deliverable]"
    
  - path: "/{stage_id}/deliverables/{deliverable_name}"
    method: "POST"
    description: "上传产出物"
    request: "file"
    response: "Deliverable"
    
  - path: "/timeline"
    method: "GET"
    description: "获取项目时间线"
    response: "Timeline"
```


## 六、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 实现阶段流转引擎
@docs/PROJECT_LIFECYCLE_SPEC_v1.0.md 实现StageEngine，支持阶段状态流转

# 创建阶段API
@docs/PROJECT_LIFECYCLE_SPEC_v1.0.md 实现项目阶段的所有API接口

# 添加新阶段
@docs/PROJECT_LIFECYCLE_SPEC_v1.0.md 按照规范添加P10：运维监控阶段

# 实现阶段通知
@docs/PROJECT_LIFECYCLE_SPEC_v1.0.md 实现阶段状态变更时的自动通知（飞书/微信）
```

---

**文档结束**