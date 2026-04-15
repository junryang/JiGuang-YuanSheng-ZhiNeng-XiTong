# 领域切换机制 - Cursor开发格式
## （基于通用能力模块整合版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\DOMAIN_SWITCH_MECHANISM_v1.0.md
```


# 领域切换机制 v1.0


## 一、概述

```yaml
module:
  name: "领域切换机制"
  description: |
    当系统需要开发新领域项目时，自动完成领域识别、模板加载、智能体初始化和项目启动。
    基于通用能力规范中的感知、决策、执行能力实现。
  domain: "D03"
  priority: "P0"

  related_abilities:
    - "PC-01: 自然语言理解"
    - "PC-04: 意图识别"
    - "PC-05: 实体抽取"
    - "DC-01: 任务规划"
    - "DC-06: 方案生成"
    - "HR-01: 智能体创建与配置"
    - "HR-02: 智能体培训与学习路径"
    - "META-01: 能力扩展"
    - "AGENT-RUNTIME-01: 智能体主循环"
```


## 二、领域切换流程

```yaml
# 领域切换五步法 - 对齐通用能力

step_1_identify:
  name: "识别领域类型"
  description: "根据项目描述自动识别所属领域"
  input: "项目描述文本"
  output: "domain_id (D01-D08)"
  method: "关键词匹配 + 语义理解"
  related_ability: "PC-04 意图识别"
  
step_2_load_template:
  name: "加载领域模板"
  description: "根据领域ID加载对应的组织架构和技能配置模板"
  input: "domain_id"
  output: "组织架构配置 + 技能配置"
  source: "MULTI_DOMAIN_PLAN_v1.0.md + DEPARTMENT_CAPABILITY_MATRIX_v1.0.md"
  related_ability: "DC-01 任务规划"
  
step_3_init_agents:
  name: "初始化智能体"
  description: "按模板创建L0-L6层级的智能体实例（L0为老板层）"
  input: "组织架构配置"
  output: "智能体实例列表"
  method: "按模板创建L0-L6智能体"
  related_ability: "HR-01 智能体创建与配置"
  
step_4_configure_skills:
  name: "配置专属技能"
  description: "为各智能体加载领域专属技能"
  input: "domain_id + 智能体列表"
  output: "技能绑定的智能体"
  method: "为各智能体加载领域专属技能"
  related_ability: "HR-02 智能体培训与学习路径"
  
step_5_start_project:
  name: "启动项目"
  description: "创建项目并进入全生命周期管理"
  input: "项目信息 + 智能体团队"
  output: "进行中的项目"
  method: "进入项目全生命周期管理"
  related_ability: "PM-01 项目创建"
```


## 三、领域识别规则

### 3.1 关键词映射表

```yaml
# 领域关键词配置 - 对齐PC-04意图识别

domain_keywords:
  D01_website:
    keywords:
      - "网站"
      - "Web"
      - "网页"
      - "前后端"
      - "前端开发"
      - "后端开发"
      - "API接口"
      - "数据库设计"
    confidence: 0.9
    related_ability: "PC-04"
    
  D02_miniprogram:
    keywords:
      - "小程序"
      - "微信小程序"
      - "支付宝小程序"
      - "百度小程序"
      - "抖音小程序"
      - "uni-app"
      - "Taro"
    confidence: 0.9
    related_ability: "PC-04"
    
  D03_multi_agent:
    keywords:
      - "智能体"
      - "多智能体"
      - "Agent"
      - "Multi-Agent"
      - "智能体协同"
      - "智能体编排"
      - "自举"
    confidence: 0.95
    related_ability: "PC-04"
    
  D04_embodied:
    keywords:
      - "具身智能"
      - "机器人"
      - "ROS"
      - "硬件"
      - "传感器"
      - "运动控制"
      - "SLAM"
      - "物理仿真"
    confidence: 0.85
    related_ability: "PC-04"
    
  D05_mobile:
    keywords:
      - "App"
      - "移动App"
      - "iOS"
      - "Android"
      - "React Native"
      - "Flutter"
      - "手机应用"
      - "移动端"
    confidence: 0.9
    related_ability: "PC-04"
    
  D06_ai_model:
    keywords:
      - "AI模型"
      - "模型训练"
      - "模型微调"
      - "深度学习"
      - "PyTorch"
      - "TensorFlow"
      - "LLM"
      - "大模型"
      - "推理部署"
    confidence: 0.9
    related_ability: "PC-04"
    
  D07_data_platform:
    keywords:
      - "数据平台"
      - "数据仓库"
      - "数据管道"
      - "ETL"
      - "BI"
      - "数据可视化"
      - "大数据"
      - "Spark"
      - "Flink"
    confidence: 0.85
    related_ability: "PC-04"
    
  D08_saas:
    keywords:
      - "SaaS"
      - "多租户"
      - "订阅"
      - "企业级"
      - "企业服务"
      - "B2B"
    confidence: 0.85
    related_ability: "PC-04"
```

### 3.2 领域识别算法

```python
# 领域识别器 - 对齐PC-04意图识别

class DomainIdentifier:
    """根据项目描述识别领域类型"""
    
    def __init__(self):
        self.keywords_map = {
            "D01": ["网站", "Web", "前后端", "API"],
            "D02": ["小程序", "微信小程序", "支付宝小程序"],
            "D03": ["智能体", "多智能体", "Agent", "协同"],
            "D04": ["具身智能", "机器人", "硬件", "ROS"],
            "D05": ["App", "移动", "iOS", "Android"],
            "D06": ["AI模型", "训练", "微调", "深度学习"],
            "D07": ["数据平台", "数据仓库", "ETL", "BI"],
            "D08": ["SaaS", "多租户", "订阅", "企业级"]
        }
        self.related_ability = "PC-04"
    
    def identify(self, description: str) -> dict:
        """
        识别领域
        返回: {
            "domain_id": "D03",
            "confidence": 0.95,
            "matched_keywords": ["智能体", "多智能体"],
            "related_ability": "PC-04"
        }
        """
        scores = {}
        matched = {}
        
        for domain_id, keywords in self.keywords_map.items():
            score = 0
            matched_keywords = []
            for kw in keywords:
                if kw.lower() in description.lower():
                    score += 1
                    matched_keywords.append(kw)
            if score > 0:
                scores[domain_id] = score / len(keywords)
                matched[domain_id] = matched_keywords
        
        if not scores:
            return {
                "domain_id": "D03",
                "confidence": 0.5,
                "matched_keywords": [],
                "reason": "未匹配到关键词，使用默认领域",
                "related_ability": "PC-04"
            }
        
        best_domain = max(scores, key=scores.get)
        
        return {
            "domain_id": best_domain,
            "confidence": scores[best_domain],
            "matched_keywords": matched[best_domain],
            "reason": f"匹配到关键词: {matched[best_domain]}",
            "related_ability": "PC-04"
        }
```


## 四、领域切换配置

### 4.1 完整配置结构

```yaml
# domain_switch_config.yaml

domain_switch:
  enabled: true
  default_domain: "D03"
  related_ability: "DC-01"
  
  # 触发条件
  triggers:
    - type: "keyword"
      description: "项目描述中包含领域关键词"
      related_ability: "PC-04"
    - type: "manual"
      description: "用户手动指定领域"
    - type: "template"
      description: "使用预设项目模板"
  
  # 领域映射
  mapping:
    D01:
      name: "网站开发"
      template: "web_dev_template"
      department_config: "DEP-01,DEP-02,DEP-03,DEP-04,DEP-06,DEP-07"
      required_skills: ["响应式布局", "RESTful API", "数据库设计"]
      estimated_setup_time: "5分钟"
      related_ability: "DC-01"
      
    D02:
      name: "小程序开发"
      template: "miniprogram_template"
      department_config: "DEP-01,DEP-02,DEP-03,DEP-04,DEP-06"
      required_skills: ["微信小程序API", "跨端框架", "微信支付"]
      estimated_setup_time: "5分钟"
      related_ability: "DC-01"
      
    D03:
      name: "多智能体协同"
      template: "multi_agent_template"
      department_config: "DEP-01,DEP-02,DEP-03,DEP-04,DEP-05,DEP-06,DEP-07,DEP-12"
      required_skills: ["智能体编排", "多智能体通信", "记忆系统"]
      estimated_setup_time: "2分钟"
      related_ability: "DC-01"
      
    D04:
      name: "具身智能开发"
      template: "embodied_template"
      department_config: "DEP-01,DEP-02,DEP-04,DEP-05,DEP-06"
      required_skills: ["ROS/ROS2", "传感器融合", "运动规划"]
      estimated_setup_time: "10分钟"
      related_ability: "DC-01"
      
    D05:
      name: "移动App开发"
      template: "mobile_app_template"
      department_config: "DEP-01,DEP-02,DEP-03,DEP-04,DEP-06"
      required_skills: ["Swift/Kotlin", "跨平台框架", "应用发布"]
      estimated_setup_time: "10分钟"
      related_ability: "DC-01"
      
    D06:
      name: "AI模型开发"
      template: "ai_model_template"
      department_config: "DEP-01,DEP-04,DEP-05,DEP-06"
      required_skills: ["PyTorch/TensorFlow", "模型训练", "GPU管理"]
      estimated_setup_time: "10分钟"
      related_ability: "DC-01"
      
    D07:
      name: "数据平台开发"
      template: "data_platform_template"
      department_config: "DEP-01,DEP-04,DEP-06,DEP-07"
      required_skills: ["数据仓库", "ETL管道", "BI可视化"]
      estimated_setup_time: "10分钟"
      related_ability: "DC-01"
      
    D08:
      name: "企业SaaS开发"
      template: "saas_template"
      department_config: "DEP-01,DEP-02,DEP-03,DEP-04,DEP-06,DEP-07,DEP-12"
      required_skills: ["多租户架构", "订阅管理", "SSO集成"]
      estimated_setup_time: "10分钟"
      related_ability: "DC-01"
```


## 五、模板数据结构

### 5.1 组织架构模板

```yaml
# templates/web_dev_template.yaml

template_id: "web_dev_template"
domain_id: "D01"
name: "网站开发组织架构"
related_ability: "HR-01"

# 部门配置 - 引用DEPARTMENT_CAPABILITY_MATRIX_v1.0.md
departments:
  - id: "DEP-01"
    name: "产品部"
    required: true
    agents:
      - role: "主管"
        level: 4
        count: 1
      - role: "员工"
        level: 5
        count: 1
      - role: "实习"
        level: 6
        count: 1
        
  - id: "DEP-02"
    name: "设计部"
    required: true
    agents:
      - role: "主管"
        level: 4
        count: 1
      - role: "员工"
        level: 5
        count: 1
      - role: "实习"
        level: 6
        count: 1
        
  - id: "DEP-03"
    name: "前端部"
    required: true
    agents:
      - role: "主管"
        level: 4
        count: 1
      - role: "员工"
        level: 5
        count: 2
      - role: "实习"
        level: 6
        count: 1
        
  - id: "DEP-04"
    name: "后端部"
    required: true
    agents:
      - role: "主管"
        level: 4
        count: 1
      - role: "员工"
        level: 5
        count: 2
      - role: "实习"
        level: 6
        count: 1
        
  - id: "DEP-06"
    name: "测试部"
    required: true
    agents:
      - role: "主管"
        level: 4
        count: 1
      - role: "员工"
        level: 5
        count: 1
      - role: "实习"
        level: 6
        count: 1
        
  - id: "DEP-07"
    name: "运维部"
    required: true
    agents:
      - role: "主管"
        level: 4
        count: 1
      - role: "员工"
        level: 5
        count: 1
      - role: "实习"
        level: 6
        count: 1

# 技能配置 - 引用BACKEND_SKILLS_v1.0.md和FRONTEND_SKILLS_v1.0.md
skills:
  - agent_type: "前端员工"
    required_skills:
      - "FE-01: 组件开发"
      - "FE-02: 状态管理"
      - "FE-03: 响应式设计"
    related_ability: "HR-02"
    
  - agent_type: "后端员工"
    required_skills:
      - "BE-01: API开发"
      - "BE-02: 数据库设计"
      - "BE-03: 性能优化"
    related_ability: "HR-02"

# 估算资源
estimated_resources:
  cpu: "2核"
  memory: "4GB"
  storage: "50GB"
  related_ability: "RS-01"
```


## 六、领域切换API

### 6.1 切换接口定义

```yaml
# API: POST /api/v1/domains/switch

related_abilities:
  - "PC-04: 意图识别"
  - "DC-01: 任务规划"
  - "HR-01: 智能体创建"
  - "PM-01: 项目创建"

request:
  project_description: "string"  # 项目描述，用于自动识别
  domain_id: "string"            # 可选，手动指定领域
  project_name: "string"         # 项目名称
  project_budget: "number"       # 项目预算

response:
  code: 200
  data:
    domain_id: "D03"
    domain_name: "多智能体协同软件开发"
    confidence: 0.95
    matched_keywords: ["智能体", "多智能体"]
    related_abilities_used: ["PC-04", "DC-01", "HR-01"]
    
    # 创建的智能体列表
    agents_created:
      total: 25
      by_level:
        L1: 1  # CEO
        L2: 1  # 总经理
        L3: 1  # 经理
        L4: 7  # 主管
        L5: 10 # 员工
        L6: 5  # 实习
    
    # 项目信息
    project:
      id: "proj_001"
      name: "项目名称"
      status: "approved"
      start_date: "2026-01-20"
    
    # 预估时间
    estimated_setup_time: "2分钟"
```


## 七、切换执行器实现

```python
# domain_switch_executor.py - 对齐通用能力

class DomainSwitchExecutor:
    """领域切换执行器"""
    
    def __init__(self):
        self.identifier = DomainIdentifier()          # PC-04
        self.template_loader = TemplateLoader()      # DC-01
        self.agent_factory = AgentFactory()          # HR-01
        self.skill_manager = SkillManager()          # HR-02
        self.project_manager = ProjectManager()      # PM-01
        self.related_abilities = [
            "PC-04", "DC-01", "HR-01", "HR-02", "PM-01"
        ]
    
    async def execute(self, request: SwitchRequest) -> SwitchResult:
        """执行领域切换"""
        
        # Step 1: 识别领域 (PC-04)
        if request.domain_id:
            domain_id = request.domain_id
            confidence = 1.0
            reason = "用户手动指定"
            related_ability = "PC-04"
        else:
            identification = self.identifier.identify(
                request.project_description
            )
            domain_id = identification["domain_id"]
            confidence = identification["confidence"]
            reason = identification["reason"]
            related_ability = identification["related_ability"]
        
        # Step 2: 加载模板 (DC-01)
        template = self.template_loader.load(domain_id)
        
        # Step 3: 创建智能体 (HR-01)
        agents = await self.agent_factory.create_from_template(
            template, 
            project_name=request.project_name
        )
        
        # Step 4: 配置技能 (HR-02)
        await self.skill_manager.assign_skills(agents, domain_id)
        
        # Step 5: 创建项目 (PM-01)
        project = await self.project_manager.create_project(
            name=request.project_name,
            domain_id=domain_id,
            agents=agents,
            budget=request.project_budget
        )
        
        return SwitchResult(
            domain_id=domain_id,
            confidence=confidence,
            reason=reason,
            agents_created=agents,
            project=project,
            related_abilities_used=self.related_abilities
        )
```


## 八、通用能力映射总表

```yaml
# 领域切换功能与通用能力映射

domain_switch_ability_mapping:
  step_1_识别领域类型:
    primary: "PC-04: 意图识别"
    secondary: "PC-05: 实体抽取"
    description: "从项目描述中提取领域信息"
    
  step_2_加载领域模板:
    primary: "DC-01: 任务规划"
    secondary: "DC-06: 方案生成"
    description: "根据领域加载对应的组织架构模板"
    
  step_3_初始化智能体:
    primary: "HR-01: 智能体创建与配置"
    secondary: "META-01: 能力扩展"
    description: "按模板创建L0-L6智能体（含L0老板层）"
    
  step_4_配置专属技能:
    primary: "HR-02: 智能体培训与学习路径"
    secondary: "HR-03: 人事绩效评估"
    description: "为智能体配置领域专属技能"
    
  step_5_启动项目:
    primary: "PM-01: 项目创建"
    secondary: "PM-02: 项目立项"
    description: "创建项目并启动开发流程"
```


## 九、使用示例

### 9.1 自动识别切换

```yaml
# 用户输入
project_description: "我需要开发一个电商网站，包含商品展示、购物车、订单管理功能"

# 系统识别结果 - 使用PC-04
识别结果:
  domain_id: "D01"
  domain_name: "网站开发"
  confidence: 0.9
  matched_keywords: ["网站", "Web"]
  related_ability: "PC-04"
  
# 自动创建的组织架构 - 使用HR-01
创建智能体:
  - 产品主管 x1
  - 资深产品经理 x1
  - 设计主管 x1
  - 资深UI设计师 x1
  - 前端主管 x1
  - 资深前端工程师 x2
  - 后端主管 x1
  - 资深后端工程师 x2
  - 测试主管 x1
  - 资深测试工程师 x1
  - 运维主管 x1
  - 资深运维工程师 x1

# 总计: 14个智能体
```

### 9.2 手动指定切换

```yaml
# 用户输入
project_description: "开发一个具身智能机器人项目"
domain_id: "D04"  # 手动指定

# 系统响应
识别结果:
  domain_id: "D04"
  domain_name: "具身智能开发"
  confidence: 1.0
  reason: "用户手动指定"
  related_ability: "PC-04"
  
estimated_setup_time: "10分钟"
```

### 9.3 对话式切换（对齐AGENT-RUNTIME-01）

```yaml
# 与CEO智能体对话 - 使用AGENT-RUNTIME-01主循环
用户: "我要开发一个AI客服系统"

主脑: [思考过程 - AGENT-RUNTIME-03]
      正在识别领域类型...
      
      根据您的描述，识别为【D01 网站开发】领域。
      置信度: 92%
      匹配关键词: ["AI", "客服", "系统"]
      
      是否确认使用此领域？
      
用户: "确认"

主脑: [行动计划 - DC-01]
      正在为您创建项目团队...
      
      ✅ 已创建14个智能体 (HR-01)
      ✅ 已配置领域专属技能 (HR-02)
      ✅ 项目"AI客服系统"已创建 (PM-01)
      
      项目负责人: Web总经理
      预计完成时间: 2周后
      
      是否现在查看项目详情？
```


## 十、配置检查清单

```yaml
# 部署前检查 - 对齐通用能力

checklist:
  - [ ] 领域关键词映射表已配置 (PC-04)
  - [ ] 8个领域的组织架构模板已准备 (DC-01)
  - [ ] 各领域专属技能已定义 (HR-02)
  - [ ] 领域识别API已实现 (PC-04)
  - [ ] 模板加载器已测试 (DC-01)
  - [ ] 智能体工厂已实现 (HR-01)
  - [ ] 切换执行器已集成
  - [ ] CEO智能体已支持对话式切换 (AGENT-RUNTIME-01)
```


## 十一、在Cursor中使用

### 11.1 保存文件后使用

将本文档保存后，在Cursor中使用以下命令：

```bash
# 实现领域识别器（对齐PC-04）
@docs/DOMAIN_SWITCH_MECHANISM_v1.0.md 实现DomainIdentifier类，基于PC-04意图识别能力

# 实现模板加载器（对齐DC-01）
@docs/DOMAIN_SWITCH_MECHANISM_v1.0.md 实现TemplateLoader，从YAML文件加载组织架构模板

# 实现切换API（对齐HR-01）
@docs/DOMAIN_SWITCH_MECHANISM_v1.0.md 实现POST /api/v1/domains/switch接口，集成HR-01智能体创建

# 测试自动识别（对齐PC-04）
@docs/DOMAIN_SWITCH_MECHANISM_v1.0.md 测试"开发一个微信小程序"能正确识别为D02领域

# 集成到CEO智能体（对齐AGENT-RUNTIME-01）
@docs/DOMAIN_SWITCH_MECHANISM_v1.0.md 将领域切换能力集成到CEO智能体的主循环中
```

### 11.2 集成到主系统

```bash
# 在项目概述中引用（当前仓库无PRD文件）
@docs/PROJECT_OVERVIEW_v1.0.md 结合DOMAIN_SWITCH_MECHANISM，在CEO智能体中增加领域识别和切换能力

# 在部门能力矩阵中引用
@docs/DEPARTMENT_CAPABILITY_MATRIX_v1.0.md 根据DOMAIN_SWITCH_MECHANISM的领域模板，配置各部门的智能体需求

# 在多领域规划中引用
@docs/MULTI_DOMAIN_PLAN_v1.0.md 根据DOMAIN_SWITCH_MECHANISM的识别规则，完善各领域的关键词映射
```


## 十二、版本更新记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-11 | 初始版本，对齐AGENT_ABILITY_SPEC_v1.0.md通用能力 |

---

**文档结束**