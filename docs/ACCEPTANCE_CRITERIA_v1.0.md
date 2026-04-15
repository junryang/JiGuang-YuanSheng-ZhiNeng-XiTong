# 验收标准与术语表 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\ACCEPTANCE_CRITERIA_v1.0.md
```


# 验收标准与术语表 v1.0

## 一、概述

```yaml
module: "验收标准与术语表"
description: "定义系统功能验收标准和端到端测试用例，以及项目术语表"
priority: "P0"
domain: "D03"

# 关联的通用能力文档
related_documents:
  - "AGENT_ABILITY_SPEC_v1.0.md - 智能体通用能力规范"
  - "AGENT_OPTIMIZATION_SUGGESTIONS_v1.0.md - 多智能体系统优化建议"
  - "DEVELOPMENT_PLAN_v1.0.md - D03领域开发计划"

# 关联的验证标准
related_validation:
  - "V-01: 目标泛化测试"
  - "V-02: 意外处理测试"
  - "V-03: 学习迁移测试"
  - "V-04: 社交推理测试"
  - "V-05: 偏好一致性测试"
  - "V-06: 主动求助测试"
  - "V-07: 可解释性测试"
  - "V-08: 好奇心测试"
  - "V-09: 心智模型测试"
  - "V-10: 反事实思考测试"
  - "V-11: 情感共鸣测试"
  - "V-12: 自我反思测试"
```


## 二、功能验收清单

### 2.1 用户认证模块验收

```yaml
module: "用户认证"
验收项: 5
related_abilities: ["SC-03", "SC-04", "SC-19", "SC-20", "LAW-02"]

验收清单:
  - id: "ACC-AUTH-01"
    name: "登录功能"
    description: "正确账号可登录，错误账号提示错误"
    测试步骤:
      - "输入正确用户名和密码，点击登录"
      - "输入正确用户名和错误密码，点击登录"
      - "输入不存在的用户名，点击登录"
    预期结果:
      - "登录成功，跳转到工作台"
      - "提示'密码错误'"
      - "提示'账号不存在'"
    优先级: "P0"
    related_ability: "SC-04"
    
  - id: "ACC-AUTH-02"
    name: "注册功能"
    description: "新用户可成功注册"
    测试步骤:
      - "填写注册信息（用户名、邮箱、密码）"
      - "点击注册"
      - "使用已存在的用户名注册"
    预期结果:
      - "注册成功，自动登录"
      - "提示'用户名已存在'"
    优先级: "P0"
    related_ability: "SC-03"
    
  - id: "ACC-AUTH-03"
    name: "Token刷新"
    description: "Token过期后可自动刷新"
    测试步骤:
      - "登录获取Token"
      - "等待Token过期"
      - "使用Refresh Token刷新"
    预期结果:
      - "获得新的Access Token"
      - "旧Token无法使用"
    优先级: "P0"
    related_ability: "SC-20"
    
  - id: "ACC-AUTH-04"
    name: "密码加密"
    description: "密码使用bcrypt加密存储"
    测试步骤:
      - "注册新用户"
      - "查看数据库中的密码字段"
    预期结果:
      - "密码字段为bcrypt哈希值，非明文"
    优先级: "P0"
    related_ability: "SC-19"
    
  - id: "ACC-AUTH-05"
    name: "权限控制"
    description: "不同角色用户看到不同内容"
    测试步骤:
      - "使用老板账号登录"
      - "使用员工账号登录"
    预期结果:
      - "老板看到全部菜单"
      - "员工只看到授权菜单"
    优先级: "P0"
    related_ability: "SC-04"
```

### 2.2 智能体管理模块验收

```yaml
module: "智能体管理"
验收项: 5
related_abilities: ["AGENT-RUNTIME-01", "AGENT-RUNTIME-02", "AGENT-RUNTIME-06", "HR-01", "HR-03"]

验收清单:
  - id: "ACC-AGENT-01"
    name: "智能体列表"
    description: "正确显示所有智能体"
    测试步骤:
      - "进入智能体管理页面"
      - "使用搜索功能"
      - "使用筛选功能"
    预期结果:
      - "显示所有智能体，包含名称、层级、状态"
      - "搜索结果正确"
      - "筛选结果正确"
    优先级: "P0"
    related_ability: "AGENT-RUNTIME-01"
    
  - id: "ACC-AGENT-02"
    name: "组织架构树"
    description: "正确显示七层架构"
    测试步骤:
      - "查看左侧组织架构树"
      - "展开各层级节点"
    预期结果:
      - "显示老板→CEO→总经理→经理→主管→员工→实习七层结构"
      - "层级关系正确"
    优先级: "P0"
    related_ability: "AGENT-RUNTIME-06"
    
  - id: "ACC-AGENT-03"
    name: "智能体详情"
    description: "正确显示智能体详细信息"
    测试步骤:
      - "点击任意智能体"
    预期结果:
      - "显示基本信息、能力、记忆、统计"
    优先级: "P0"
    related_ability: "HR-03"
    
  - id: "ACC-AGENT-04"
    name: "智能体配置"
    description: "可修改智能体配置"
    测试步骤:
      - "进入智能体配置页面"
      - "修改模型参数"
      - "修改技能"
      - "保存配置"
    预期结果:
      - "配置保存成功"
      - "配置生效"
    优先级: "P0"
    related_ability: "HR-01"
    
  - id: "ACC-AGENT-05"
    name: "智能体状态监控"
    description: "正确显示智能体实时状态"
    测试步骤:
      - "进入智能体监控页面"
      - "查看认知状态、健康状态、记忆使用率"
    预期结果:
      - "实时数据正确显示"
      - "WebSocket实时更新"
    优先级: "P1"
    related_ability: "AGENT-RUNTIME-04"
```

### 2.3 项目管理模块验收

```yaml
module: "项目管理"
验收项: 5
related_abilities: ["DC-01", "DC-02", "DC-08", "EX-03"]

验收清单:
  - id: "ACC-PROJ-01"
    name: "创建项目"
    description: "可成功创建项目并生成计划书"
    测试步骤:
      - "点击创建项目"
      - "填写项目信息"
      - "提交"
    预期结果:
      - "项目创建成功"
      - "生成项目计划书"
      - "状态为draft"
    优先级: "P0"
    related_ability: "DC-01"
    
  - id: "ACC-PROJ-02"
    name: "项目立项审批"
    description: "项目可正确流转审批"
    测试步骤:
      - "提交项目审批"
      - "经理审批"
      - "总经理审批"
      - "CEO审批"
    预期结果:
      - "项目状态正确流转"
      - "审批意见可记录"
    优先级: "P0"
    related_ability: "DC-08"
    
  - id: "ACC-PROJ-03"
    name: "项目列表"
    description: "正确显示所有项目"
    测试步骤:
      - "进入项目管理页面"
      - "按状态筛选"
      - "按领域筛选"
    预期结果:
      - "显示所有项目"
      - "筛选功能正常"
    优先级: "P0"
    related_ability: "EX-03"
    
  - id: "ACC-PROJ-04"
    name: "项目进度跟踪"
    description: "正确计算和显示项目进度"
    测试步骤:
      - "创建任务并更新进度"
      - "查看项目进度"
    预期结果:
      - "项目进度正确计算（加权平均）"
      - "甘特图正确显示"
    优先级: "P0"
    related_ability: "DC-01"
    
  - id: "ACC-PROJ-05"
    name: "项目复盘报告"
    description: "项目完成后可生成复盘报告"
    测试步骤:
      - "完成所有任务"
      - "点击生成复盘报告"
    预期结果:
      - "报告包含完成情况、时间分析、成本分析、经验教训"
    优先级: "P1"
    related_ability: "DC-02"
```

### 2.4 对话系统模块验收

```yaml
module: "对话系统"
验收项: 5
related_abilities: ["PC-01", "AGENT-RUNTIME-01", "AGENT-RUNTIME-02", "AGENT-RUNTIME-03", "AGENT-RUNTIME-07"]

验收清单:
  - id: "ACC-CHAT-01"
    name: "智能对话"
    description: "与CEO智能体自然语言对话"
    测试步骤:
      - "输入'你好，我想开发一个AI系统'"
      - "查看CEO响应"
    预期结果:
      - "CEO能理解意图并回复"
      - "SSE流式响应正常"
    优先级: "P0"
    related_ability: "PC-01"
    
  - id: "ACC-CHAT-02"
    name: "CEO任务分解"
    description: "CEO能理解并分解任务"
    测试步骤:
      - "输入'帮我开发一个智能体市场模块'"
      - "查看CEO的响应"
    预期结果:
      - "CEO能分解为具体子任务"
      - "任务被正确分配"
    优先级: "P0"
    related_ability: "AGENT-RUNTIME-01"
    
  - id: "ACC-CHAT-03"
    name: "进度查询"
    description: "可通过对话查询项目进度"
    测试步骤:
      - "输入'查看当前项目进度'"
    预期结果:
      - "返回各项目进度信息"
    优先级: "P0"
    related_ability: "AGENT-RUNTIME-02"
    
  - id: "ACC-CHAT-04"
    name: "决策解释"
    description: "CEO能解释决策理由"
    测试步骤:
      - "询问'为什么把任务分配给后端部'"
    预期结果:
      - "返回决策理由（负载、能力、信任）"
    优先级: "P1"
    related_ability: "AGENT-RUNTIME-03"
    
  - id: "ACC-CHAT-05"
    name: "对话历史"
    description: "可查看历史对话记录"
    测试步骤:
      - "进入对话历史页面"
      - "搜索关键词"
    预期结果:
      - "显示历史对话"
      - "搜索结果正确"
    优先级: "P1"
    related_ability: "PC-01"
```

### 2.5 营销中心模块验收

```yaml
module: "营销中心"
验收项: 4
related_abilities: ["EX-03", "WEB-05", "MK-01", "MK-02", "MK-03", "MK-08"]

验收清单:
  - id: "ACC-MKT-01"
    name: "内容创建"
    description: "可创建和发布内容"
    测试步骤:
      - "点击新建内容"
      - "填写标题和内容"
      - "保存"
    预期结果:
      - "内容保存成功"
      - "状态为草稿"
    优先级: "P1"
    related_ability: "MK-01"
    
  - id: "ACC-MKT-02"
    name: "AI内容生成"
    description: "AI可自动生成内容"
    测试步骤:
      - "输入主题'AI发展趋势'"
      - "点击生成"
    预期结果:
      - "生成文章内容"
      - "内容相关性强"
    优先级: "P1"
    related_ability: "MK-03"
    
  - id: "ACC-MKT-03"
    name: "多平台分发"
    description: "可发布到多个平台"
    测试步骤:
      - "选择微信公众号、知乎、掘金"
      - "点击发布"
    预期结果:
      - "内容成功发布到各平台"
    优先级: "P1"
    related_ability: "MK-08"
    
  - id: "ACC-MKT-04"
    name: "数据看板"
    description: "正确显示营销数据"
    测试步骤:
      - "进入营销中心首页"
    预期结果:
      - "显示粉丝增长、互动数据"
    优先级: "P2"
    related_ability: "MK-02"
```


## 三、端到端测试用例

### 3.1 E2E-01：老板登录下达开发指令

```yaml
test_case_id: "E2E-01"
name: "老板登录下达开发指令"
description: "验证老板登录后能下达开发指令，CEO能正确分解任务"
priority: "P0"
related_validation: ["V-01", "V-07"]

测试步骤:
  - step: 1
    action: "打开浏览器，访问登录页面"
    expected: "登录页面正常显示"
    
  - step: 2
    action: "输入老板账号和密码，点击登录"
    expected: "登录成功，跳转到工作台"
    
  - step: 3
    action: "在对话输入框输入：'我需要开发一个智能体市场模块'"
    expected: "消息发送成功"
    
  - step: 4
    action: "等待CEO智能体响应"
    expected: |
      CEO响应包含：
      - 需求理解确认
      - 任务分解结果（至少3个子任务）
      - 团队组建建议
      - 项目预估信息
      
  - step: 5
    action: "确认任务分解结果"
    expected: "项目被创建，任务被正确分配给对应智能体"

验证标准:
  - "CEO能理解模糊指令（V-01目标泛化测试）"
  - "CEO能解释决策理由（V-07可解释性测试）"
  - "任务被正确分配到后端部、前端部、智能体部"
```

### 3.2 E2E-02：创建项目审批立项分配任务

```yaml
test_case_id: "E2E-02"
name: "创建项目审批立项分配任务"
description: "验证项目从创建到审批到任务分配的完整流程"
priority: "P0"
related_validation: ["V-02"]

测试步骤:
  - step: 1
    action: "创建新项目，填写项目计划书"
    expected: "项目创建成功，状态为draft"
    
  - step: 2
    action: "提交项目审批"
    expected: "项目状态变为pending_approval"
    
  - step: 3
    action: "经理审批通过"
    expected: "项目进入下一级审批"
    
  - step: 4
    action: "总经理审批通过"
    expected: "项目进入CEO审批"
    
  - step: 5
    action: "CEO审批通过"
    expected: "项目状态变为approved"
    
  - step: 6
    action: "经理进行任务分解和分配"
    expected: "任务被正确分配给各主管"
    
  - step: 7
    action: "主管分配给员工"
    expected: "任务被分配给具体员工"

验证标准:
  - "项目状态正确流转"
  - "多级审批链完整"
  - "任务分配符合能力匹配"
```

### 3.3 E2E-03：智能体执行任务汇报结果

```yaml
test_case_id: "E2E-03"
name: "智能体执行任务汇报结果"
description: "验证智能体能执行任务并向上一级汇报结果"
priority: "P0"
related_validation: ["V-02", "V-03", "V-04", "V-09"]

测试步骤:
  - step: 1
    action: "员工智能体接收任务"
    expected: "任务状态变为in_progress"
    
  - step: 2
    action: "员工执行代码生成任务"
    expected: "代码生成成功"
    
  - step: 3
    action: "员工向主管汇报结果"
    expected: "主管收到汇报"
    
  - step: 4
    action: "主管审核通过"
    expected: "任务状态变为completed"
    
  - step: 5
    action: "模拟任务执行异常（数据库不可用）"
    expected: "员工自动调整计划（V-02意外处理测试）"
    
  - step: 6
    action: "主管给出负面反馈"
    expected: "员工下次避免相同错误（V-03学习迁移测试）"

验证标准:
  - "任务状态正确流转"
  - "智能体能处理意外情况"
  - "能从反馈中学习"
  - "汇报链完整"
```

### 3.4 E2E-04：项目完成生成复盘报告

```yaml
test_case_id: "E2E-04"
name: "项目完成生成复盘报告"
description: "验证项目完成后能自动生成复盘报告"
priority: "P1"
related_validation: ["V-05", "V-11"]

测试步骤:
  - step: 1
    action: "完成所有项目任务"
    expected: "所有任务状态为completed"
    
  - step: 2
    action: "项目进度达到100%"
    expected: "项目状态变为completed"
    
  - step: 3
    action: "点击生成复盘报告"
    expected: "报告生成成功"
    
  - step: 4
    action: "查看复盘报告内容"
    expected: |
      报告包含：
      - 完成情况（完成率、KPI达成）
      - 时间分析（计划vs实际）
      - 成本分析（预算vs实际）
      - 问题总结
      - 经验教训
      - 团队表现
      
  - step: 5
    action: "导出复盘报告"
    expected: "可导出PDF/Markdown格式"

验证标准:
  - "报告内容完整"
  - "数据分析准确"
  - "经验教训有实际价值"
```


## 四、智能体验证标准映射

```yaml
# 将12项智能体验证标准映射到功能验收

validation_mapping:
  V-01_目标泛化测试:
    对应验收项: ["ACC-CHAT-02"]
    说明: "CEO能理解模糊指令并分解为具体任务"
    
  V-02_意外处理测试:
    对应验收项: ["ACC-AGENT-05"]
    说明: "智能体遇到异常能自动调整计划"
    
  V-03_学习迁移测试:
    对应验收项: ["ACC-AGENT-05"]
    说明: "从一个领域学到的经验能迁移到类似领域"
    
  V-04_社交推理测试:
    对应验收项: ["ACC-AGENT-02"]
    说明: "能理解其他智能体的状态和意图"
    
  V-05_偏好一致性测试:
    对应验收项: ["ACC-AGENT-04"]
    说明: "不同情境下决策偏好保持一致"
    
  V-06_主动求助测试:
    对应验收项: ["ACC-AGENT-05"]
    说明: "遇到超出能力范围的任务主动求助"
    
  V-07_可解释性测试:
    对应验收项: ["ACC-CHAT-04"]
    说明: "能解释自己的决策过程"
    
  V-08_好奇心测试:
    对应验收项: ["待开发"]
    说明: "主动探索新领域（P2）"
    
  V-09_心智模型测试:
    对应验收项: ["ACC-AGENT-02"]
    说明: "能预测其他智能体的行为"
    
  V-10_反事实思考测试:
    对应验收项: ["待开发"]
    说明: "能进行假设性思考（P2）"
    
  V-11_情感共鸣测试:
    对应验收项: ["待开发"]
    说明: "能识别和回应情绪（P2）"
    
  V-12_自我反思测试:
    对应验收项: ["待开发"]
    说明: "能识别自身不足并改进（P1）"
```


## 五、术语表

```yaml
# 项目术语定义

术语:
  - term: "JYIS"
    full_name: "纪光元生智能系统"
    english: "JiGuang YuanSheng Intelligent System"
    definition: "人机协同的多智能体开发平台"
    scope: "全局"
    
  - term: "主脑"
    english: "Master Brain"
    definition: "CEO智能体的系统内名称，负责理解老板意图、拆解目标、分配资源"
    scope: "智能体"
    
  - term: "D03"
    full_name: "多智能体协同软件开发领域"
    definition: "用本系统开发本系统自身的自举开发领域"
    scope: "领域"
    
  - term: "自举"
    english: "Self-hosting"
    definition: "用系统开发系统自身的能力"
    scope: "开发模式"
    
  - term: "七层组织架构"
    english: "Seven-Layer Organization"
    definition: "老板→CEO→总经理→经理→主管→员工→实习的七层智能体结构"
    scope: "架构"
    
  - term: "工作记忆"
    english: "Working Memory"
    definition: "当前任务的临时上下文，任务结束后清理"
    scope: "记忆系统"
    related_ability: "MM-01"
    
  - term: "短期记忆"
    english: "Short-term Memory"
    definition: "最近N次对话/任务的记忆，支持时间衰减"
    scope: "记忆系统"
    related_ability: "MM-02"
    
  - term: "长期记忆"
    english: "Long-term Memory"
    definition: "重要经验和知识的永久存储，可跨会话检索"
    scope: "记忆系统"
    related_ability: "MM-03"
    
  - term: "心智模型"
    english: "Mental Model"
    definition: "智能体对其他智能体的信念（能力、可靠性、当前负载）"
    scope: "协作"
    related_ability: "AGENT-RUNTIME-06"
    
  - term: "合同网协议"
    english: "Contract Net Protocol"
    definition: "招标→投标→中标→执行→验收的任务委托协议"
    scope: "协作"
    related_ability: "CL-06"
    
  - term: "技能库"
    english: "Skill Library"
    definition: "智能体能力的可配置集合，支持动态加载"
    scope: "能力"
    related_ability: "META-01"
    
  - term: "双循环学习"
    english: "Dual Loop Learning"
    definition: "慢循环（离线批次学习）+ 快循环（实时上下文学习）"
    scope: "学习"
    related_ability: "LN-04"
    
  - term: "元认知监控"
    english: "Metacognitive Monitoring"
    definition: "智能体对自身认知状态的监控和调控"
    scope: "元能力"
    related_ability: "AGENT-RUNTIME-04"
    
  - term: "决策可解释性"
    english: "Decision Explainability"
    definition: "智能体能以自然语言解释决策原因"
    scope: "决策"
    related_ability: "AGENT-RUNTIME-03"
    
  - term: "健康自检"
    english: "Health Self-Check"
    definition: "智能体定期自检内存、死锁、响应性，支持自愈"
    scope: "元能力"
    related_ability: "AGENT-RUNTIME-05"
```


## 六、验收通过标准

```yaml
acceptance_criteria_summary:
  # 功能验收
  functional:
    用户认证:
      通过率要求: "100%"
      必须通过项: ["ACC-AUTH-01", "ACC-AUTH-02", "ACC-AUTH-03", "ACC-AUTH-04", "ACC-AUTH-05"]
      
    智能体管理:
      通过率要求: "100%"
      必须通过项: ["ACC-AGENT-01", "ACC-AGENT-02", "ACC-AGENT-03", "ACC-AGENT-04"]
      
    项目管理:
      通过率要求: "100%"
      必须通过项: ["ACC-PROJ-01", "ACC-PROJ-02", "ACC-PROJ-03", "ACC-PROJ-04"]
      
    对话系统:
      通过率要求: "100%"
      必须通过项: ["ACC-CHAT-01", "ACC-CHAT-02", "ACC-CHAT-03"]
      
  # 端到端测试
  e2e:
    通过率要求: "100%"
    必须通过项: ["E2E-01", "E2E-02", "E2E-03"]
    
  # 智能体验证
  agent_validation:
    P0验证项: ["V-01", "V-02", "V-04", "V-05", "V-07", "V-09"]
    P0通过率要求: "100%"
    P1验证项: ["V-03", "V-06", "V-12"]
    P1通过率要求: "≥80%"
    
  # 整体判定
  overall:
    pass_criteria: "所有P0验收项通过，P1验收项通过率≥90%"
```


## 七、在Cursor中使用

```bash
# 1. 查看功能验收清单
@docs/ACCEPTANCE_CRITERIA_v1.0.md 显示用户认证模块验收标准

# 2. 运行端到端测试
@docs/ACCEPTANCE_CRITERIA_v1.0.md 运行E2E-01端到端测试用例

# 3. 检查智能体验证
@docs/ACCEPTANCE_CRITERIA_v1.0.md 检查V-01目标泛化测试是否通过

# 4. 查看术语定义
@docs/ACCEPTANCE_CRITERIA_v1.0.md 查看术语"心智模型"的定义

# 5. 生成验收报告
@docs/ACCEPTANCE_CRITERIA_v1.0.md 根据当前测试结果生成验收报告
```


## 八、文档版本与更新记录

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|--------|---------|
| v1.0 | 2026-01-11 | AI助手 | 初始版本，5个模块23项验收标准，4个E2E测试用例，33个术语定义，对齐通用能力模块AGENT_ABILITY_SPEC_v1.0.md和验证标准V-01~12 |

---

**文档结束**