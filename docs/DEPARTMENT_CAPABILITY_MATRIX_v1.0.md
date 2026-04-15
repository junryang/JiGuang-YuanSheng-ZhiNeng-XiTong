# 部门能力矩阵 - 纪光元生智能系统
## （基于通用能力模块完整版 - 最终修订版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\DEPARTMENT_CAPABILITY_MATRIX_v1.0.md
```


# 部门能力矩阵 v1.0


## 一、能力矩阵总览

```yaml
department_matrix:
  version: "v1.0"
  domain: "D03"
  domain_name: "多智能体协同软件开发"
  last_updated: "2026-01-11"
  
  # 部门分类
  department_categories:
    - category: "core"
      name: "核心研发部门"
      description: "负责产品研发和技术实现的核心部门"
      departments: ["产品部", "设计部", "前端部", "后端部", "智能体部", "测试部", "运维部"]
      
    - category: "support"
      name: "支撑服务部门"
      description: "提供人力、财务、法务等支撑服务的部门"
      departments: ["人事行政部", "财务部", "法务合规部", "战略发展部", "信息技术部"]
      
    - category: "business"
      name: "业务拓展部门"
      description: "负责市场、销售、客户关系的业务部门"
      departments: ["营销部", "销售部", "客户成功部", "生态合作部", "渠道管理部"]
      
    - category: "governance"
      name: "治理监管部门"
      description: "负责审计、风控、质量、合规的监督部门"
      departments: ["内部审计部", "风险管理部", "质量管理部", "安全合规部"]

  departments:
    # ========== 核心研发部门 ==========
    - id: "DEP-01"
      name: "产品部"
      category: "core"
      lead: "产品主管"
      employees: ["资深产品经理"]
      interns: ["实习产品助理"]
      related_abilities: ["PD-01", "PD-02", "PD-03", "PD-04", "PD-05", "PD-06"]
      priority: "P0"
      
    - id: "DEP-02"
      name: "设计部"
      category: "core"
      lead: "设计主管"
      employees: ["资深UI设计师", "交互设计师"]
      interns: ["实习设计助理"]
      related_abilities: ["DS-01", "DS-02", "DS-03", "DS-04", "DS-05"]
      priority: "P0"
      
    - id: "DEP-03"
      name: "前端部"
      category: "core"
      lead: "前端主管"
      employees: ["资深前端工程师 x2"]
      interns: ["实习前端助理"]
      related_abilities: ["FE-01", "FE-02", "FE-03", "FE-04", "FE-05", "FE-06"]
      priority: "P0"
      
    - id: "DEP-04"
      name: "后端部"
      category: "core"
      lead: "后端主管"
      employees: ["资深后端工程师 x2"]
      interns: ["实习后端助理"]
      related_abilities: ["BE-01", "BE-02", "BE-03", "BE-04", "BE-05", "BE-06"]
      priority: "P0"
      
    - id: "DEP-05"
      name: "智能体部"
      category: "core"
      lead: "智能体主管"
      employees: ["资深智能体工程师 x2"]
      interns: ["实习智能体助理"]
      related_abilities: ["AG-01", "AG-02", "AG-03", "AG-04", "AG-05", "AG-06"]
      priority: "P0"
      
    - id: "DEP-06"
      name: "测试部"
      category: "core"
      lead: "测试主管"
      employees: ["资深测试工程师", "自动化测试工程师"]
      interns: ["实习测试助理"]
      related_abilities: ["QA-01", "QA-02", "QA-03", "QA-04", "QA-05", "QA-06"]
      priority: "P0"
      
    - id: "DEP-07"
      name: "运维部"
      category: "core"
      lead: "运维主管"
      employees: ["资深运维工程师", "SRE工程师"]
      interns: ["实习运维助理"]
      related_abilities: ["OPS-01", "OPS-02", "OPS-03", "OPS-04", "OPS-05", "OPS-06"]
      priority: "P0"
      
    # ========== 支撑服务部门 ==========
    - id: "DEP-08"
      name: "人事行政部"
      category: "support"
      lead: "人事行政主管"
      employees: ["资深HRBP", "招聘专员", "行政专员", "薪酬专员"]
      interns: ["实习人事助理"]
      related_abilities: ["HR-01", "HR-02", "HR-03", "HR-04", "HR-05", "ADMIN-01", "ADMIN-02", "ADMIN-03"]
      priority: "P1"
      
    - id: "DEP-09"
      name: "财务部"
      category: "support"
      lead: "财务主管"
      employees: ["资深财务分析师", "会计专员", "出纳", "税务专员"]
      interns: ["实习财务助理"]
      related_abilities: ["FIN-01", "FIN-02", "FIN-03", "FIN-04", "FIN-05"]
      priority: "P1"
      
    - id: "DEP-10"
      name: "法务合规部"
      category: "support"
      lead: "法务合规主管"
      employees: ["资深法务顾问", "合规专员", "知识产权专员"]
      interns: ["实习法务助理"]
      related_abilities: ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05", "COMP-01", "COMP-02"]
      priority: "P1"
      
    - id: "DEP-11"
      name: "战略发展部"
      category: "support"
      lead: "战略发展主管"
      employees: ["资深战略分析师", "行业研究员", "投资经理"]
      interns: ["实习战略助理"]
      related_abilities: ["STRAT-01", "STRAT-02", "STRAT-03", "STRAT-04"]
      priority: "P2"
      
    - id: "DEP-19"
      name: "信息技术部"
      category: "support"
      lead: "IT主管"
      employees: ["网络工程师", "系统管理员", "桌面支持"]
      interns: ["实习IT助理"]
      related_abilities: ["IT-01", "IT-02", "IT-03"]
      priority: "P1"
      
    # ========== 业务拓展部门 ==========
    - id: "DEP-12"
      name: "营销部"
      category: "business"
      lead: "营销主管"
      employees: ["资深内容运营", "品牌专员", "SEO专员", "社交媒体运营"]
      interns: ["实习运营助理"]
      related_abilities: ["MK-01", "MK-02", "MK-03", "MK-04", "MK-05", "MK-06", "MK-07", "MK-08"]
      priority: "P1"
      
    - id: "DEP-13"
      name: "销售部"
      category: "business"
      lead: "销售主管"
      employees: ["资深销售经理 x2", "售前工程师", "商务专员"]
      interns: ["实习销售助理"]
      related_abilities: ["SALES-01", "SALES-02", "SALES-03", "SALES-04", "SALES-05"]
      priority: "P2"
      
    - id: "DEP-14"
      name: "客户成功部"
      category: "business"
      lead: "客户成功主管"
      employees: ["客户成功经理 x2", "技术支持工程师", "客户培训师"]
      interns: ["实习客户成功助理"]
      related_abilities: ["CS-01", "CS-02", "CS-03", "CS-04", "CS-05"]
      priority: "P2"
      
    - id: "DEP-15"
      name: "生态合作部"
      category: "business"
      lead: "生态合作主管"
      employees: ["生态合作经理", "开发者关系专员", "联盟拓展专员"]
      interns: ["实习合作助理"]
      related_abilities: ["ECO-01", "ECO-02", "ECO-03", "ECO-04"]
      priority: "P2"
      
    - id: "DEP-20"
      name: "渠道管理部"
      category: "business"
      lead: "渠道主管"
      employees: ["渠道经理 x2", "渠道运营专员"]
      interns: ["实习渠道助理"]
      related_abilities: ["CH-01", "CH-02", "CH-03"]
      priority: "P2"
      
    # ========== 治理监管部门 ==========
    - id: "DEP-16"
      name: "内部审计部"
      category: "governance"
      lead: "审计主管"
      employees: ["资深审计师", "IT审计师"]
      interns: ["实习审计助理"]
      related_abilities: ["AUDIT-01", "AUDIT-02", "AUDIT-03", "AUDIT-04"]
      priority: "P2"
      
    - id: "DEP-17"
      name: "风险管理部"
      category: "governance"
      lead: "风控主管"
      employees: ["风控分析师", "信用评估师"]
      interns: ["实习风控助理"]
      related_abilities: ["RISK-01", "RISK-02", "RISK-03", "RISK-04"]
      priority: "P2"
      
    - id: "DEP-18"
      name: "质量管理部"
      category: "governance"
      lead: "质量主管"
      employees: ["质量保证工程师", "过程改进专员"]
      interns: ["实习质量助理"]
      related_abilities: ["QM-01", "QM-02", "QM-03", "QM-04"]
      priority: "P2"
      
    - id: "DEP-21"
      name: "安全合规部"
      category: "governance"
      lead: "安全合规主管"
      employees: ["安全工程师", "合规审计师", "数据隐私官"]
      interns: ["实习安全助理"]
      related_abilities: ["SEC-01", "SEC-02", "SEC-03", "SEC-04", "SEC-05"]
      priority: "P1"
```


## 二、通用能力映射表

```yaml
# 部门能力与通用能力映射
general_ability_mapping:
  # ========== 人事行政部 ==========
  HR-01_智能体创建与配置:
    department: "人事行政部"
    related_abilities: ["AGENT-RUNTIME-01", "META-01", "HR-01"]
    priority: "P0"
    
  HR-02_智能体培训与学习路径:
    department: "人事行政部"
    related_abilities: ["LN-01", "LN-02", "LN-04", "HR-02"]
    priority: "P1"
    
  HR-03_人事绩效评估:
    department: "人事行政部"
    related_abilities: ["AGENT-RUNTIME-04", "HR-03"]
    priority: "P1"
    
  HR-04_智能体升职与调岗:
    department: "人事行政部"
    related_abilities: ["HR-04"]
    priority: "P2"
    
  HR-05_团队建设与协作优化:
    department: "人事行政部"
    related_abilities: ["HR-05", "CL-06"]
    priority: "P2"
    
  ADMIN-01_行政事务管理:
    department: "人事行政部"
    related_abilities: ["FILE-01", "FILE-04"]
    priority: "P1"
    
  ADMIN-02_办公资源管理:
    department: "人事行政部"
    related_abilities: ["RS-01", "RS-06"]
    priority: "P1"
    
  ADMIN-03_员工关系管理:
    department: "人事行政部"
    related_abilities: ["AGENT-RUNTIME-10"]
    priority: "P2"
    
  # ========== 财务部 ==========
  FIN-01_预算管理:
    department: "财务部"
    related_abilities: ["RS-06", "EM-05"]
    priority: "P0"
    
  FIN-02_成本核算:
    department: "财务部"
    related_abilities: ["EM-05", "RS-06"]
    priority: "P0"
    
  FIN-03_费用报销:
    department: "财务部"
    related_abilities: ["APPROVE-01"]
    priority: "P1"
    
  FIN-04_财务分析:
    department: "财务部"
    related_abilities: ["CG-04", "AGENT-RUNTIME-09"]
    priority: "P2"
    
  FIN-05_税务管理:
    department: "财务部"
    related_abilities: ["LAW-01"]
    priority: "P1"
    
  # ========== 法务合规部 ==========
  LAW-01_内容合规审核:
    department: "法务合规部"
    related_abilities: ["LAW-01", "SC-03"]
    priority: "P0"
    
  LAW-02_数据隐私保护:
    department: "法务合规部"
    related_abilities: ["LAW-02"]
    priority: "P0"
    
  LAW-03_版权与知识产权保护:
    department: "法务合规部"
    related_abilities: ["LAW-03"]
    priority: "P1"
    
  LAW-04_访问合法性检查:
    department: "法务合规部"
    related_abilities: ["LAW-04"]
    priority: "P0"
    
  LAW-05_合规报告与审计:
    department: "法务合规部"
    related_abilities: ["LAW-05"]
    priority: "P1"
    
  COMP-01_合同管理:
    department: "法务合规部"
    related_abilities: ["LAW-03", "FILE-01"]
    priority: "P1"
    
  COMP-02_诉讼管理:
    department: "法务合规部"
    related_abilities: ["LAW-01"]
    priority: "P2"
    
  # ========== 战略发展部 ==========
  STRAT-01_市场分析:
    department: "战略发展部"
    related_abilities: ["KNOW-01", "KNOW-02"]
    priority: "P1"
    
  STRAT-02_竞争分析:
    department: "战略发展部"
    related_abilities: ["KNOW-03", "CG-02"]
    priority: "P1"
    
  STRAT-03_战略规划:
    department: "战略发展部"
    related_abilities: ["DC-01", "AGENT-RUNTIME-02"]
    priority: "P2"
    
  STRAT-04_投资分析:
    department: "战略发展部"
    related_abilities: ["AGENT-RUNTIME-09"]
    priority: "P2"
    
  # ========== 营销部 ==========
  MK-01_内容创作:
    department: "营销部"
    related_abilities: ["EM-01", "EM-02", "EX-14", "EX-15"]
    priority: "P0"
    
  MK-02_多平台分发:
    department: "营销部"
    related_abilities: ["WEB-05", "MK-08"]
    priority: "P0"
    
  MK-03_品牌管理:
    department: "营销部"
    related_abilities: ["AGENT-RUNTIME-02"]
    priority: "P1"
    
  MK-04_SEO优化:
    department: "营销部"
    related_abilities: ["KNOW-02"]
    priority: "P2"
    
  MK-05_社交媒体运营:
    department: "营销部"
    related_abilities: ["WEB-05"]
    priority: "P1"
    
  MK-06_数据分析:
    department: "营销部"
    related_abilities: ["CG-04"]
    priority: "P1"
    
  MK-07_活动策划:
    department: "营销部"
    related_abilities: ["DC-06"]
    priority: "P2"
    
  MK-08_广告投放:
    department: "营销部"
    related_abilities: ["WEB-04"]
    priority: "P2"
    
  # ========== 销售部 ==========
  SALES-01_客户开发:
    department: "销售部"
    related_abilities: ["CL-04"]
    priority: "P1"
    
  SALES-02_报价管理:
    department: "销售部"
    related_abilities: ["DC-11"]
    priority: "P1"
    
  SALES-03_合同谈判:
    department: "销售部"
    related_abilities: ["CL-04"]
    priority: "P2"
    
  SALES-04_销售预测:
    department: "销售部"
    related_abilities: ["CG-04"]
    priority: "P2"
    
  SALES-05_客户关系维护:
    department: "销售部"
    related_abilities: ["AGENT-RUNTIME-10"]
    priority: "P1"
    
  # ========== 客户成功部 ==========
  CS-01_客户 onboarding:
    department: "客户成功部"
    related_abilities: ["LN-02"]
    priority: "P1"
    
  CS-02_客户培训:
    department: "客户成功部"
    related_abilities: ["LN-02"]
    priority: "P1"
    
  CS-03_技术支持:
    department: "客户成功部"
    related_abilities: ["EX-03", "KNOW-02"]
    priority: "P1"
    
  CS-04_客户健康度监控:
    department: "客户成功部"
    related_abilities: ["QL-07"]
    priority: "P2"
    
  CS-05_续约管理:
    department: "客户成功部"
    related_abilities: ["PR-04"]
    priority: "P2"
    
  # ========== 生态合作部 ==========
  ECO-01_伙伴招募:
    department: "生态合作部"
    related_abilities: ["CL-04"]
    priority: "P2"
    
  ECO-02_伙伴赋能:
    department: "生态合作部"
    related_abilities: ["LN-02"]
    priority: "P2"
    
  ECO-03_集成对接:
    department: "生态合作部"
    related_abilities: ["WEB-04", "EX-03"]
    priority: "P2"
    
  ECO-04_生态运营:
    department: "生态合作部"
    related_abilities: ["CL-12"]
    priority: "P2"
    
  # ========== 信息技术部 ==========
  IT-01_网络管理:
    department: "信息技术部"
    related_abilities: ["SC-04"]
    priority: "P1"
    
  IT-02_系统管理:
    department: "信息技术部"
    related_abilities: ["OPS-01", "OPS-02"]
    priority: "P1"
    
  IT-03_资产管理:
    department: "信息技术部"
    related_abilities: ["RS-01"]
    priority: "P1"
    
  # ========== 渠道管理部 ==========
  CH-01_渠道招募:
    department: "渠道管理部"
    related_abilities: ["CL-04"]
    priority: "P2"
    
  CH-02_渠道培训:
    department: "渠道管理部"
    related_abilities: ["LN-02"]
    priority: "P2"
    
  CH-03_渠道激励:
    department: "渠道管理部"
    related_abilities: ["MOT-01"]
    priority: "P2"
    
  # ========== 内部审计部 ==========
  AUDIT-01_操作审计:
    department: "内部审计部"
    related_abilities: ["SC-07"]
    priority: "P0"
    
  AUDIT-02_合规审计:
    department: "内部审计部"
    related_abilities: ["LAW-05"]
    priority: "P1"
    
  AUDIT-03_财务审计:
    department: "内部审计部"
    related_abilities: ["FIN-02"]
    priority: "P2"
    
  AUDIT-04_IT审计:
    department: "内部审计部"
    related_abilities: ["SC-07"]
    priority: "P2"
    
  # ========== 风险管理部 ==========
  RISK-01_风险评估:
    department: "风险管理部"
    related_abilities: ["DC-08", "CG-06"]
    priority: "P1"
    
  RISK-02_风险监控:
    department: "风险管理部"
    related_abilities: ["QL-07"]
    priority: "P1"
    
  RISK-03_风险处置:
    department: "风险管理部"
    related_abilities: ["DC-01"]
    priority: "P2"
    
  RISK-04_危机管理:
    department: "风险管理部"
    related_abilities: ["AGENT-RUNTIME-05"]
    priority: "P2"
    
  # ========== 质量管理部 ==========
  QM-01_质量标准制定:
    department: "质量管理部"
    related_abilities: ["QL-01"]
    priority: "P1"
    
  QM-02_质量检查:
    department: "质量管理部"
    related_abilities: ["QL-05", "QA-01"]
    priority: "P1"
    
  QM-03_过程改进:
    department: "质量管理部"
    related_abilities: ["LN-06"]
    priority: "P2"
    
  QM-04_质量报告:
    department: "质量管理部"
    related_abilities: ["QL-07"]
    priority: "P2"
    
  # ========== 安全合规部 ==========
  SEC-01_安全策略制定:
    department: "安全合规部"
    related_abilities: ["SC-04"]
    priority: "P0"
    
  SEC-02_安全监控:
    department: "安全合规部"
    related_abilities: ["SC-07"]
    priority: "P0"
    
  SEC-03_漏洞管理:
    department: "安全合规部"
    related_abilities: ["SC-03"]
    priority: "P0"
    
  SEC-04_应急响应:
    department: "安全合规部"
    related_abilities: ["AGENT-RUNTIME-05"]
    priority: "P1"
    
  SEC-05_安全审计:
    department: "安全合规部"
    related_abilities: ["SC-07"]
    priority: "P1"
```


## 三、人事行政部能力矩阵

```yaml
department: "人事行政部"
department_id: "DEP-08"
category: "support"
lead_role: "人事行政主管"
employee_roles: ["资深HRBP", "招聘专员", "行政专员", "薪酬专员"]
intern_roles: ["实习人事助理"]

related_abilities:
  - "HR-01: 智能体创建与配置"
  - "HR-02: 智能体培训与学习路径"
  - "HR-03: 人事绩效评估"
  - "HR-04: 智能体升职与调岗"
  - "HR-05: 团队建设与协作优化"
  - "ADMIN-01: 行政事务管理"
  - "ADMIN-02: 办公资源管理"
  - "ADMIN-03: 员工关系管理"

capabilities:
  - id: "HR-01"
    name: "智能体创建与配置"
    description: "根据组织需求自动创建新的智能体，配置角色、层级、能力集、权限边界"
    priority: "P0"
    inputs:
      - "岗位需求"
      - "组织架构规划"
    outputs:
      - "智能体实例"
      - "权限配置"
      - "能力分配"
    dependencies: []
    related_ability: "HR-01"
    
  - id: "HR-02"
    name: "智能体培训与学习路径"
    description: "为新创建的智能体设计个性化学习路径，通过课程、模拟任务、导师指导提升能力"
    priority: "P1"
    inputs:
      - "智能体能力评估"
      - "岗位能力要求"
    outputs:
      - "学习路径"
      - "培训课程"
      - "导师分配"
    dependencies:
      - "HR-01"
    related_ability: "HR-02"
    
  - id: "HR-03"
    name: "人事绩效评估"
    description: "对智能体的工作表现进行量化评估，包括任务完成率、质量、协作度、学习进步"
    priority: "P1"
    inputs:
      - "工作数据"
      - "协作记录"
    outputs:
      - "绩效报告"
      - "评估得分"
      - "改进建议"
    dependencies: []
    related_ability: "HR-03"
    
  - id: "HR-04"
    name: "智能体升职与调岗"
    description: "根据绩效评估和能力发展，自动推荐智能体晋升到更高层级或调整到更适合的岗位"
    priority: "P2"
    inputs:
      - "绩效评估结果"
      - "能力发展轨迹"
    outputs:
      - "晋升推荐"
      - "调岗方案"
      - "权限更新"
    dependencies:
      - "HR-03"
    related_ability: "HR-04"
    
  - id: "HR-05"
    name: "团队建设与协作优化"
    description: "分析智能体团队的结构和协作模式，推荐最佳团队组合，识别协作瓶颈"
    priority: "P2"
    inputs:
      - "团队协作数据"
      - "项目任务历史"
    outputs:
      - "团队优化建议"
      - "协作改进方案"
    dependencies: []
    related_ability: "HR-05"
    
  - id: "ADMIN-01"
    name: "行政事务管理"
    description: "管理日常行政事务，包括会议安排、文档归档、通知发布等"
    priority: "P1"
    inputs:
      - "行政需求"
    outputs:
      - "会议安排"
      - "归档文档"
      - "通知记录"
    dependencies: []
    related_ability: "FILE-01"
    
  - id: "ADMIN-02"
    name: "办公资源管理"
    description: "管理办公资源（计算资源、软件许可、API配额）的分配和使用"
    priority: "P1"
    inputs:
      - "资源申请"
    outputs:
      - "资源分配"
      - "使用统计"
      - "资源预警"
    dependencies: []
    related_ability: "RS-01"
    
  - id: "ADMIN-03"
    name: "员工关系管理"
    description: "管理智能体员工关系，处理投诉、建议、满意度调查"
    priority: "P2"
    inputs:
      - "员工反馈"
      - "满意度调查"
    outputs:
      - "满意度报告"
      - "改进建议"
    dependencies: []
    related_ability: "AGENT-RUNTIME-10"

outputs:
  - type: "config"
    name: "智能体配置"
    format: "YAML"
  - type: "report"
    name: "绩效报告"
    format: "PDF/JSON"
  - type: "schedule"
    name: "培训计划"
    format: "Calendar"
  - type: "report"
    name: "满意度报告"
    format: "PDF"

workflow:
  - step: 1
    name: "需求分析"
    action: "分析人力需求"
    output: "招聘/创建计划"
  - step: 2
    name: "智能体创建"
    action: "创建新智能体"
    output: "智能体就绪"
  - step: 3
    name: "培训配置"
    action: "配置学习路径"
    output: "培训完成"
  - step: 4
    name: "绩效评估"
    action: "定期评估"
    output: "评估报告"
  - step: 5
    name: "晋升调岗"
    action: "根据评估调整"
    output: "岗位调整"
```


## 四、法务合规部能力矩阵

```yaml
department: "法务合规部"
department_id: "DEP-10"
category: "support"
lead_role: "法务合规主管"
employee_roles: ["资深法务顾问", "合规专员", "知识产权专员"]
intern_roles: ["实习法务助理"]

related_abilities:
  - "LAW-01: 内容合规审核"
  - "LAW-02: 数据隐私保护"
  - "LAW-03: 版权与知识产权保护"
  - "LAW-04: 访问合法性检查"
  - "LAW-05: 合规报告与审计"
  - "COMP-01: 合同管理"
  - "COMP-02: 诉讼管理"

capabilities:
  - id: "LAW-01"
    name: "内容合规审核"
    description: "对智能体生成或发布的所有内容进行自动合规审核，检测违规内容"
    priority: "P0"
    inputs:
      - "待审核内容"
    outputs:
      - "合规报告"
      - "违规标记"
      - "修改建议"
    dependencies: []
    related_ability: "LAW-01"
    
  - id: "LAW-02"
    name: "数据隐私保护"
    description: "严格遵守数据隐私法规，自动脱敏敏感数据，限制数据收集和使用范围"
    priority: "P0"
    inputs:
      - "用户数据"
      - "数据使用请求"
    outputs:
      - "脱敏数据"
      - "合规确认"
      - "数据操作记录"
    dependencies: []
    related_ability: "LAW-02"
    
  - id: "LAW-03"
    name: "版权与知识产权保护"
    description: "检测内容是否侵权，正确标注来源，遵守CC协议"
    priority: "P1"
    inputs:
      - "生成内容"
      - "引用来源"
    outputs:
      - "版权检测报告"
      - "侵权警告"
      - "来源标注"
    dependencies: []
    related_ability: "LAW-03"
    
  - id: "LAW-04"
    name: "访问合法性检查"
    description: "检查网络资源访问是否违反服务条款、robots.txt、访问频率限制"
    priority: "P0"
    inputs:
      - "访问请求"
    outputs:
      - "合法性判断"
      - "拒绝原因"
    dependencies: []
    related_ability: "LAW-04"
    
  - id: "LAW-05"
    name: "合规报告与审计"
    description: "自动生成合规审计报告，记录所有可能违规的行为"
    priority: "P1"
    inputs:
      - "合规事件"
    outputs:
      - "审计报告"
      - "合规建议"
    dependencies:
      - "LAW-01"
      - "LAW-02"
    related_ability: "LAW-05"
    
  - id: "COMP-01"
    name: "合同管理"
    description: "管理合同模板、审核合同条款、跟踪合同执行"
    priority: "P1"
    inputs:
      - "合同需求"
    outputs:
      - "合同草案"
      - "审核意见"
      - "合同归档"
    dependencies: []
    related_ability: "LAW-03"
    
  - id: "COMP-02"
    name: "诉讼管理"
    description: "管理法律诉讼案件，跟踪案件进展"
    priority: "P2"
    inputs:
      - "案件信息"
    outputs:
      - "案件档案"
      - "进展报告"
    dependencies: []
    related_ability: "LAW-01"

outputs:
  - type: "report"
    name: "合规报告"
    format: "PDF"
  - type: "config"
    name: "合规规则"
    format: "YAML"
  - type: "document"
    name: "合同文件"
    format: "PDF/Markdown"
  - type: "case"
    name: "案件档案"
    format: "Database"

workflow:
  - step: 1
    name: "规则配置"
    action: "配置合规规则"
    output: "规则库"
  - step: 2
    name: "内容审核"
    action: "审核生成内容"
    output: "审核结果"
  - step: 3
    name: "风险评估"
    action: "评估合规风险"
    output: "风险报告"
  - step: 4
    name: "审计报告"
    action: "生成审计报告"
    output: "审计报告"
```


## 五、财务部能力矩阵

```yaml
department: "财务部"
department_id: "DEP-09"
category: "support"
lead_role: "财务主管"
employee_roles: ["资深财务分析师", "会计专员", "出纳", "税务专员"]
intern_roles: ["实习财务助理"]

related_abilities:
  - "FIN-01: 预算管理"
  - "FIN-02: 成本核算"
  - "FIN-03: 费用报销"
  - "FIN-04: 财务分析"
  - "FIN-05: 税务管理"

capabilities:
  - id: "FIN-01"
    name: "预算管理"
    description: "制定和管理项目预算，监控预算执行情况"
    priority: "P0"
    inputs:
      - "项目计划"
      - "历史支出"
    outputs:
      - "预算方案"
      - "预算执行报告"
      - "预算预警"
    dependencies: []
    related_ability: "RS-06"
    
  - id: "FIN-02"
    name: "成本核算"
    description: "核算各项目、各部门的成本支出"
    priority: "P0"
    inputs:
      - "支出记录"
      - "资源使用数据"
    outputs:
      - "成本报表"
      - "成本分析"
    dependencies: []
    related_ability: "EM-05"
    
  - id: "FIN-03"
    name: "费用报销"
    description: "处理费用报销申请，审核报销合规性"
    priority: "P1"
    inputs:
      - "报销申请"
    outputs:
      - "审核结果"
      - "报销记录"
    dependencies: []
    related_ability: "APPROVE-01"
    
  - id: "FIN-04"
    name: "财务分析"
    description: "分析财务数据，提供经营决策支持"
    priority: "P2"
    inputs:
      - "财务数据"
    outputs:
      - "财务分析报告"
      - "经营建议"
    dependencies:
      - "FIN-01"
      - "FIN-02"
    related_ability: "CG-04"
    
  - id: "FIN-05"
    name: "税务管理"
    description: "管理税务申报、税务筹划、税务合规"
    priority: "P1"
    inputs:
      - "财务数据"
    outputs:
      - "税务申报表"
      - "税务筹划方案"
    dependencies: []
    related_ability: "LAW-01"

outputs:
  - type: "report"
    name: "预算报告"
    format: "Excel/PDF"
  - type: "report"
    name: "成本报表"
    format: "Excel"
  - type: "record"
    name: "报销记录"
    format: "Database"
  - type: "report"
    name: "财务分析报告"
    format: "PDF"

workflow:
  - step: 1
    name: "预算编制"
    action: "编制年度/项目预算"
    output: "预算方案"
  - step: 2
    name: "预算执行"
    action: "监控预算执行"
    output: "执行报告"
  - step: 3
    name: "成本核算"
    action: "核算成本"
    output: "成本报表"
  - step: 4
    name: "财务分析"
    action: "分析财务状况"
    output: "分析报告"
```


## 六、部门协作关系图

```yaml
collaboration_graph:
  description: "部门间协作关系（完整版）"
  
  flows:
    # ========== 核心研发流程 ==========
    - from: "产品部"
      to: ["设计部", "后端部", "测试部", "智能体部"]
      items: ["PRD文档", "用户故事", "功能清单"]
      
    - from: "设计部"
      to: ["前端部"]
      items: ["设计稿", "组件库", "切图资源"]
      
    - from: "后端部"
      to: ["前端部", "智能体部", "测试部"]
      items: ["API接口", "API文档", "数据模型"]
      
    - from: "智能体部"
      to: ["前端部", "后端部"]
      items: ["智能体配置", "工作流定义"]
      
    - from: "前端部"
      to: ["测试部"]
      items: ["开发版本"]
      
    - from: "测试部"
      to: ["产品部", "前端部", "后端部"]
      items: ["测试报告", "缺陷报告"]
      
    - from: "运维部"
      to: ["所有部门"]
      items: ["部署环境", "监控面板"]
      
    # ========== 支撑服务流程 ==========
    - from: "人事行政部"
      to: ["所有部门"]
      items: ["智能体配置", "培训计划", "绩效评估"]
      
    - from: "财务部"
      to: ["所有部门"]
      items: ["预算", "成本核算", "报销"]
      
    - from: "法务合规部"
      to: ["所有部门"]
      items: ["合规审核", "合同审核", "隐私保护"]
      
    - from: "战略发展部"
      to: ["产品部", "营销部"]
      items: ["市场分析", "战略规划"]
      
    - from: "信息技术部"
      to: ["所有部门"]
      items: ["IT支持", "网络服务", "系统维护"]
      
    # ========== 业务拓展流程 ==========
    - from: "营销部"
      to: ["产品部", "销售部"]
      items: ["营销内容", "品牌素材", "市场洞察"]
      
    - from: "销售部"
      to: ["产品部", "客户成功部"]
      items: ["客户需求", "销售数据", "合同"]
      
    - from: "客户成功部"
      to: ["产品部", "营销部"]
      items: ["客户反馈", "成功案例", "技术支持记录"]
      
    - from: "生态合作部"
      to: ["产品部", "智能体部"]
      items: ["合作伙伴需求", "集成方案", "API对接"]
      
    - from: "渠道管理部"
      to: ["销售部", "营销部"]
      items: ["渠道政策", "渠道数据", "培训材料"]
      
    # ========== 治理监督流程 ==========
    - from: "内部审计部"
      to: ["所有部门"]
      items: ["审计报告", "整改建议"]
      
    - from: "风险管理部"
      to: ["所有部门"]
      items: ["风险评估", "风险预警"]
      
    - from: "质量管理部"
      to: ["所有部门"]
      items: ["质量标准", "质量报告", "改进建议"]
      
    - from: "安全合规部"
      to: ["所有部门"]
      items: ["安全策略", "安全监控", "合规要求"]
```


## 七、部门完整清单

| 部门ID | 部门名称 | 类别 | 主管 | 员工数 | 优先级 | 状态 |
|--------|---------|------|------|--------|--------|------|
| DEP-01 | 产品部 | 核心研发 | 产品主管 | 1 | P0 | 必需 |
| DEP-02 | 设计部 | 核心研发 | 设计主管 | 2 | P0 | 必需 |
| DEP-03 | 前端部 | 核心研发 | 前端主管 | 2 | P0 | 必需 |
| DEP-04 | 后端部 | 核心研发 | 后端主管 | 2 | P0 | 必需 |
| DEP-05 | 智能体部 | 核心研发 | 智能体主管 | 2 | P0 | 必需 |
| DEP-06 | 测试部 | 核心研发 | 测试主管 | 2 | P0 | 必需 |
| DEP-07 | 运维部 | 核心研发 | 运维主管 | 2 | P0 | 必需 |
| DEP-08 | 人事行政部 | 支撑服务 | 人事行政主管 | 4 | P1 | 必需 |
| DEP-09 | 财务部 | 支撑服务 | 财务主管 | 4 | P1 | 必需 |
| DEP-10 | 法务合规部 | 支撑服务 | 法务合规主管 | 3 | P1 | 必需 |
| DEP-11 | 战略发展部 | 支撑服务 | 战略发展主管 | 3 | P2 | 可选 |
| DEP-12 | 营销部 | 业务拓展 | 营销主管 | 4 | P1 | 必需 |
| DEP-13 | 销售部 | 业务拓展 | 销售主管 | 4 | P2 | 可选 |
| DEP-14 | 客户成功部 | 业务拓展 | 客户成功主管 | 4 | P2 | 可选 |
| DEP-15 | 生态合作部 | 业务拓展 | 生态合作主管 | 3 | P2 | 可选 |
| DEP-16 | 内部审计部 | 治理监管 | 审计主管 | 2 | P2 | 可选 |
| DEP-17 | 风险管理部 | 治理监管 | 风控主管 | 2 | P2 | 可选 |
| DEP-18 | 质量管理部 | 治理监管 | 质量主管 | 2 | P2 | 可选 |
| DEP-19 | 信息技术部 | 支撑服务 | IT主管 | 3 | P1 | 必需 |
| DEP-20 | 渠道管理部 | 业务拓展 | 渠道主管 | 3 | P2 | 可选 |
| DEP-21 | 安全合规部 | 治理监管 | 安全合规主管 | 3 | P1 | 必需 |

**总计**: 21个部门，其中必需部门13个，可选部门8个


## 八、在Cursor中使用

```bash
# 1. 创建部门数据模型
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 根据部门能力矩阵，创建Department和Capability的数据模型

# 2. 实现部门API
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 实现部门管理的CRUD API，包括部门列表、部门详情、部门能力查询

# 3. 实现人事行政部能力（对齐HR-01）
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 实现DEP-08人事行政部的HR-01智能体创建能力

# 4. 实现法务合规部能力（对齐LAW-01）
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 实现DEP-10法务合规部的LAW-01内容合规审核能力

# 5. 实现财务部能力（对齐FIN-01）
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 实现DEP-09财务部的FIN-01预算管理能力

# 6. 实现安全合规部能力（对齐SEC-01）
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 实现DEP-21安全合规部的SEC-01安全策略制定能力

# 7. 生成部门配置数据
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 根据21个部门配置，生成初始化的部门数据
```


## 九、版本更新记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-11 | 初始版本，21个部门，对齐AGENT_ABILITY_SPEC_v1.0.md通用能力 |
| v1.0 | 2026-01-11 | 新增：信息技术部(DEP-19)、渠道管理部(DEP-20)、安全合规部(DEP-21) |
| v1.0 | 2026-01-11 | 扩充：人事行政部、财务部、法务合规部、营销部、销售部、客户成功部、生态合作部的人员配置 |
| v1.0 | 2026-01-11 | 完善：通用能力映射表，覆盖所有21个部门 |
| v1.0 | 2026-01-11 | 新增：部门协作关系图完整版 |

---

**文档结束**