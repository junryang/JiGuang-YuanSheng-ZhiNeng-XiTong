# 组织架构设计 - 纪光元生智能系统

**文件路径**: `docs/ORGANIZATION_ARCHITECTURE_v1.0.md`


# 组织架构设计文档


## 一、七层组织架构

```yaml
organization:
  name: "纪光元生智能系统组织架构"
  version: "v1.0"
  total_levels: 7
  
  levels:
    - level: 0
      name: "老板"
      role_type: "human"
      role_code: "BOSS"
      naming: "固定为'老板'"
      permissions: "全部权限"
      report_to: null
      core_responsibilities:
        - "战略决策"
        - "资源审批"
        - "最终验收"
      interaction: "仅与CEO智能体对话"
      
    - level: 1
      name: "CEO智能体"
      role_type: "agent"
      role_code: "CEO"
      naming: "固定为'主脑'"
      permissions: "战略级"
      report_to: "老板"
      core_responsibilities:
        - "理解老板意图"
        - "拆解为可执行目标"
        - "分配资源给各领域"
        - "协调跨领域协作"
        - "汇总结果向老板汇报"
      core_abilities:
        - "战略规划"
        - "意图拆解"
        - "资源分配"
        - "多领域协调"
        
    - level: 2
      name: "总经理智能体"
      role_type: "agent"
      role_code: "GM"
      naming: "{领域名称}总经理"
      permissions: "领域级"
      report_to: "CEO"
      core_responsibilities:
        - "管理特定开发领域的整体规划"
        - "领域内项目立项审批"
        - "跨项目资源调配"
        - "领域能力建设"
      core_abilities:
        - "领域规划"
        - "项目立项审批"
        - "跨项目资源调配"
        
    - level: 3
      name: "经理智能体"
      role_type: "agent"
      role_code: "MGR"
      naming: "{项目名称}经理"
      permissions: "项目级"
      report_to: "总经理"
      core_responsibilities:
        - "管理具体项目的执行"
        - "项目计划制定"
        - "任务分解与分配"
        - "进度跟踪与风险识别"
        - "团队协调"
      core_abilities:
        - "项目计划"
        - "任务分解"
        - "进度跟踪"
        - "风险识别"
        
    - level: 4
      name: "主管智能体"
      role_type: "agent"
      role_code: "LEAD"
      naming: "{部门名称}主管"
      permissions: "部门级"
      report_to: "经理"
      core_responsibilities:
        - "管理职能部门的工作分配"
        - "技术方案评审"
        - "代码质量把控"
        - "团队技能管理"
        - "跨部门协调"
      core_abilities:
        - "技术方案评审"
        - "代码质量把控"
        - "团队技能管理"
        
    - level: 5
      name: "员工智能体"
      role_type: "agent"
      role_code: "EMP"
      naming: "{岗位级别}{岗位名称}"
      permissions: "执行级"
      report_to: "主管"
      core_responsibilities:
        - "执行具体任务"
        - "代码编写"
        - "测试执行"
        - "文档撰写"
        - "技术调研"
      core_abilities:
        - "代码编写"
        - "测试执行"
        - "文档撰写"
        - "技术调研"
        
    - level: 6
      name: "实习智能体"
      role_type: "agent"
      role_code: "INT"
      naming: "实习{岗位名称}"
      permissions: "辅助级"
      report_to: "员工"
      core_responsibilities:
        - "辅助支持"
        - "代码审查辅助"
        - "日志分析"
        - "知识检索"
        - "文档整理"
      core_abilities:
        - "代码审查辅助"
        - "日志分析"
        - "知识检索"
        - "文档整理"
```


## 二、权限矩阵

```yaml
permission_matrix:
  description: "按角色分配的权限矩阵"
  
  system_operations:
    - operation: "系统配置"
      boss: true
      ceo: true
      gm: false
      manager: false
      lead: false
      employee: false
      intern: false
      
    - operation: "跨领域审批"
      boss: true
      ceo: true
      gm: false
      manager: false
      lead: false
      employee: false
      intern: false
      
    - operation: "领域内审批"
      boss: true
      ceo: true
      gm: true
      manager: false
      lead: false
      employee: false
      intern: false
      
    - operation: "项目内审批"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: false
      employee: false
      intern: false
      
    - operation: "创建项目"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: false
      employee: false
      intern: false
      
    - operation: "创建任务"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: false
      intern: false
      
    - operation: "执行任务"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: true
      intern: false
      
    - operation: "查看报告"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: true
      intern: true
      
    - operation: "辅助执行"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: false
      intern: true
      
    - operation: "创建智能体"
      boss: true
      ceo: true
      gm: true
      manager: false
      lead: false
      employee: false
      intern: false
      
    - operation: "配置智能体"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: false
      intern: false
      
    - operation: "查看代码"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: true
      intern: true
      
    - operation: "修改代码"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: true
      intern: false
      
    - operation: "查看记忆"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: true
      intern: true
      
    - operation: "修改记忆"
      boss: true
      ceo: true
      gm: true
      manager: true
      lead: true
      employee: false
      intern: false
```


## 三、D03领域专属组织架构

```yaml
d03_organization:
  domain_id: "D03"
  domain_name: "多智能体协同软件开发"
  
  departments:
    - id: "DEP-01"
      name: "产品部"
      lead: "产品主管"
      employees:
        - title: "资深产品经理"
          count: 1
      interns:
        - title: "实习产品助理"
          count: 1
      responsibilities:
        - "需求分析"
        - "产品规划"
        - "用户研究"
        - "PRD撰写"
        
    - id: "DEP-02"
      name: "设计部"
      lead: "设计主管"
      employees:
        - title: "资深UI设计师"
          count: 1
      interns:
        - title: "实习设计助理"
          count: 1
      responsibilities:
        - "界面设计"
        - "交互设计"
        - "视觉规范"
        - "原型设计"
        
    - id: "DEP-03"
      name: "前端部"
      lead: "前端主管"
      employees:
        - title: "资深前端工程师"
          count: 2
      interns:
        - title: "实习前端助理"
          count: 1
      responsibilities:
        - "前端架构"
        - "组件开发"
        - "性能优化"
        - "响应式设计"
        
    - id: "DEP-04"
      name: "后端部"
      lead: "后端主管"
      employees:
        - title: "资深后端工程师"
          count: 2
      interns:
        - title: "实习后端助理"
          count: 1
      responsibilities:
        - "API开发"
        - "数据库设计"
        - "安全加固"
        - "性能优化"
        
    - id: "DEP-05"
      name: "智能体部"
      lead: "智能体主管"
      employees:
        - title: "资深智能体工程师"
          count: 2
      interns:
        - title: "实习智能体助理"
          count: 1
      responsibilities:
        - "智能体创建"
        - "智能体编排"
        - "记忆配置"
        - "技能配置"
        
    - id: "DEP-06"
      name: "测试部"
      lead: "测试主管"
      employees:
        - title: "资深测试工程师"
          count: 1
      interns:
        - title: "实习测试助理"
          count: 1
      responsibilities:
        - "单元测试"
        - "集成测试"
        - "质量保障"
        - "缺陷追踪"
        
    - id: "DEP-07"
      name: "运维部"
      lead: "运维主管"
      employees:
        - title: "资深运维工程师"
          count: 1
      interns:
        - title: "实习运维助理"
          count: 1
      responsibilities:
        - "部署上线"
        - "监控告警"
        - "备份恢复"
        - "性能监控"
        
    - id: "DEP-08"
      name: "营销部"
      lead: "营销主管"
      employees:
        - title: "资深内容运营"
          count: 1
      interns:
        - title: "实习运营助理"
          count: 1
      responsibilities:
        - "内容创作"
        - "多平台分发"
        - "数据分析"
        - "SEO优化"
```


## 四、汇报关系

```yaml
reporting_lines:
  - from: "L6实习智能体"
    to: "L5员工智能体"
    type: "direct"
    
  - from: "L5员工智能体"
    to: "L4主管"
    type: "direct"
    
  - from: "L4主管"
    to: "L3经理"
    type: "direct"
    
  - from: "L3经理"
    to: "L2总经理"
    type: "direct"
    
  - from: "L2总经理"
    to: "L1 CEO"
    type: "direct"
    
  - from: "L1 CEO"
    to: "L0老板"
    type: "direct"

communication_rules:
  - rule: "下级主动向上级汇报任务完成情况"
  - rule: "上级向下级下达指令，下级必须确认接收"
  - rule: "同级之间可协作沟通，但需抄送上级"
  - rule: "跨层级沟通需经过直接上级（老板除外）"
  - rule: "紧急情况可越级上报，但事后需通知直接上级"
```


## 五、数据模型定义

```python
# 组织架构数据模型

class AgentLevel:
    """智能体层级枚举"""
    BOSS = 0   # 老板（人类）
    CEO = 1    # CEO智能体
    GM = 2     # 总经理智能体
    MGR = 3    # 经理智能体
    LEAD = 4   # 主管智能体
    EMP = 5    # 员工智能体
    INT = 6    # 实习智能体

class AgentRole:
    """智能体角色"""
    level: int           # 层级
    role_code: str       # 角色代码
    role_name: str       # 角色名称
    permissions: list    # 权限列表
    parent_role: str     # 上级角色

class Agent:
    """智能体实例"""
    id: str              # 唯一标识
    name: str            # 名称（遵循命名规范）
    level: int           # 层级
    role_code: str       # 角色代码
    department_id: str   # 所属部门
    parent_id: str       # 上级智能体ID
    status: str          # 状态
    created_at: datetime # 创建时间
    updated_at: datetime # 更新时间

class Department:
    """部门定义"""
    id: str              # 部门ID
    name: str            # 部门名称
    lead_role: str       # 主管角色
    employee_roles: list # 员工角色列表
    intern_roles: list   # 实习角色列表
    responsibilities: list # 职责列表
```


## 六、多领域扩展规则

```yaml
domain_expansion_rules:
  - rule: "每个新领域自动创建对应的总经理智能体"
    example: "新增D04具身智能开发领域 → 创建'具身智能总经理'"
    
  - rule: "每个领域可根据需要自定义部门结构"
    example: "具身智能领域需要硬件部 → 创建'硬件主管'和'硬件工程师'"
    
  - rule: "通用部门可跨领域共享"
    example: "产品主管同时服务于D01、D02、D03领域"
    
  - rule: "领域间资源可动态调配"
    example: "D03领域任务高峰期，可从D01领域临时调配前端工程师"

domain_templates:
  - domain_id: "D01"
    name: "网站开发"
    default_departments:
      - "产品部"
      - "设计部"
      - "前端部"
      - "后端部"
      - "测试部"
      - "运维部"
      
  - domain_id: "D02"
    name: "小程序开发"
    default_departments:
      - "产品部"
      - "设计部"
      - "小程序部"
      - "后端部"
      - "测试部"
      
  - domain_id: "D03"
    name: "多智能体协同软件开发"
    default_departments:
      - "产品部"
      - "设计部"
      - "前端部"
      - "后端部"
      - "智能体部"
      - "测试部"
      - "运维部"
      - "营销部"
      
  - domain_id: "D04"
    name: "具身智能开发"
    default_departments:
      - "产品部"
      - "设计部"
      - "硬件部"
      - "嵌入式部"
      - "算法部"
      - "测试部"
```


## 七、在Cursor中使用

### 文件存放位置
```
d:\BaiduSyncdisk\JiGuang\docs\ORGANIZATION_ARCHITECTURE_v1.0.md
```

### 在Cursor中引用

**创建组织架构数据模型**：
```
@docs/ORGANIZATION_ARCHITECTURE_v1.0.md 根据组织架构设计，创建Agent和Department的数据模型
```

**实现权限检查**：
```
@docs/ORGANIZATION_ARCHITECTURE_v1.0.md 实现基于角色的权限检查中间件
```

**创建D03领域组织架构**：
```
@docs/ORGANIZATION_ARCHITECTURE_v1.0.md 创建D03领域的8个部门和对应的智能体
```


## 八、相关文档索引

| 文档 | 路径 | 说明 |
|------|------|------|
| 项目概述 | `docs/PROJECT_OVERVIEW_v1.0.md` | 项目整体介绍 |
| 智能体能力规范 | `docs/AGENT_ABILITY_SPEC_v1.0.md` | 142项能力定义（基线） |
| 组织架构设计 | `docs/ORGANIZATION_ARCHITECTURE_v1.0.md` | 本文档 |
| 产品需求文档 | `docs/PRD_v2.0.md` | 发布范围、门槛与优先级基线 |

---

**文档结束**