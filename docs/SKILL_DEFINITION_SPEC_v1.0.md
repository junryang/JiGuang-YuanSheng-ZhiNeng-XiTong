# 技能定义规范 - Cursor开发格式

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\SKILL_DEFINITION_SPEC_v1.0.md
```


# 技能定义规范 v1.0

## 一、技能元数据完整定义

```yaml
# 技能定义标准格式

skill:
  # 基础信息
  id: "string"                 # 唯一标识，格式: {CATEGORY}-{NUMBER}
  name: "string"               # 技能名称
  name_en: "string"            # 英文名称（可选）
  version: "string"            # 版本号，如 "1.0.0"
  
  # 等级配置
  level: "enum"                # 资深/中级/实习
  level_requirements:          # 各等级要求
    intern:                    # 实习等级
      required_training_hours: 40
      required_practice_count: 10
    junior:                    # 中级
      required_training_hours: 80
      required_practice_count: 30
    senior:                    # 资深
      required_training_hours: 160
      required_practice_count: 100
  
  # 描述信息
  description: "string"        # 技能描述
  detailed_description: "string"  # 详细描述
  use_cases:                   # 使用场景
    - "场景1"
    - "场景2"
  
  # 输入输出定义
  input_schema:                # JSON Schema格式
    type: "object"
    properties: {}
    required: []
  output_schema:               # JSON Schema格式
    type: "object"
    properties: {}
    required: []
  
  # 依赖关系
  dependencies:                # 依赖的其他技能ID列表
    - "SKILL-01"
    - "SKILL-02"
  optional_dependencies:       # 可选依赖
    - "SKILL-03"
  
  # 示例
  examples:                    # 示例用法列表
    - name: "示例名称"
      description: "示例描述"
      input: {}
      output: {}
      explanation: "解释说明"
  
  # 标签
  tags:                        # 标签列表
    - "category"
    - "keyword"
  
  # 执行配置
  execution:
    timeout_seconds: 30        # 超时时间
    max_retries: 3             # 最大重试次数
    requires_approval: false   # 是否需要审批
    allowed_agents:            # 允许使用的智能体层级
      - "L4"
      - "L5"
      - "L6"
  
  # 资源需求
  resources:
    cpu: "0.5"                 # CPU核心数
    memory: "512Mi"            # 内存
    gpu: false                 # 是否需要GPU
    network: true              # 是否需要网络
  
  # 评估标准
  evaluation:
    success_criteria:          # 成功标准
      - "标准1"
      - "标准2"
    quality_metrics:           # 质量指标
      - name: "accuracy"
        target: 0.95
      - name: "response_time"
        target: 5.0
```


## 二、技能定义数据模型

```python
# skills/models.py

from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class SkillLevel(str, Enum):
    """技能等级"""
    INTERN = "实习"
    JUNIOR = "中级"
    SENIOR = "资深"


class ExecutionConfig(BaseModel):
    """执行配置"""
    timeout_seconds: int = 30
    max_retries: int = 3
    requires_approval: bool = False
    allowed_agents: List[str] = Field(default=["L4", "L5", "L6"])


class ResourceConfig(BaseModel):
    """资源配置"""
    cpu: str = "0.5"
    memory: str = "512Mi"
    gpu: bool = False
    network: bool = True


class QualityMetric(BaseModel):
    """质量指标"""
    name: str
    target: float


class EvaluationConfig(BaseModel):
    """评估配置"""
    success_criteria: List[str] = Field(default_factory=list)
    quality_metrics: List[QualityMetric] = Field(default_factory=list)


class SkillExample(BaseModel):
    """技能示例"""
    name: str
    description: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    explanation: str


class SkillDefinition(BaseModel):
    """技能定义"""
    # 基础信息
    id: str = Field(..., pattern=r'^[A-Z]{2,3}-\d{2}$')
    name: str
    name_en: Optional[str] = None
    version: str = "1.0.0"
    
    # 等级配置
    level: SkillLevel
    level_requirements: Dict[str, int] = Field(default={
        "intern": {"training_hours": 40, "practice_count": 10},
        "junior": {"training_hours": 80, "practice_count": 30},
        "senior": {"training_hours": 160, "practice_count": 100}
    })
    
    # 描述信息
    description: str
    detailed_description: Optional[str] = None
    use_cases: List[str] = Field(default_factory=list)
    
    # 输入输出定义
    input_schema: Dict[str, Any] = Field(default={
        "type": "object",
        "properties": {},
        "required": []
    })
    output_schema: Dict[str, Any] = Field(default={
        "type": "object",
        "properties": {},
        "required": []
    })
    
    # 依赖关系
    dependencies: List[str] = Field(default_factory=list)
    optional_dependencies: List[str] = Field(default_factory=list)
    
    # 示例
    examples: List[SkillExample] = Field(default_factory=list)
    
    # 标签
    tags: List[str] = Field(default_factory=list)
    
    # 配置
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    resources: ResourceConfig = Field(default_factory=ResourceConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    
    # 元数据
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_by: Optional[str] = None
    is_active: bool = True
```


## 三、技能示例 - BE-01 API开发

```yaml
# 技能示例：BE-01 API开发

skill:
  id: "BE-01"
  name: "API开发"
  name_en: "API Development"
  version: "1.0.0"
  
  level: "资深"
  
  description: "开发RESTful/GraphQL API，包括路由设计、请求验证、响应格式化"
  
  detailed_description: |
    该技能使智能体能够：
    1. 设计RESTful API路由和端点
    2. 实现请求参数验证和错误处理
    3. 格式化API响应
    4. 编写API文档
    5. 实现GraphQL schema和resolvers
  
  use_cases:
    - "创建用户管理API"
    - "开发RESTful数据接口"
    - "构建GraphQL网关"
  
  input_schema:
    type: "object"
    properties:
      api_type:
        type: "string"
        enum: ["restful", "graphql"]
        description: "API类型"
      endpoints:
        type: "array"
        description: "端点列表"
        items:
          type: "object"
          properties:
            path:
              type: "string"
            method:
              type: "string"
              enum: ["GET", "POST", "PUT", "DELETE", "PATCH"]
            description:
              type: "string"
      request_schema:
        type: "object"
        description: "请求体Schema（JSON Schema格式）"
      response_schema:
        type: "object"
        description: "响应体Schema（JSON Schema格式）"
    required:
      - "api_type"
      - "endpoints"
  
  output_schema:
    type: "object"
    properties:
      code:
        type: "integer"
        description: "状态码"
      message:
        type: "string"
        description: "响应消息"
      data:
        type: "object"
        description: "响应数据"
      endpoints:
        type: "array"
        description: "生成的端点列表"
    required:
      - "code"
      - "data"
  
  dependencies: []
  optional_dependencies:
    - "BE-03"  # 性能优化
    - "BE-04"  # 安全加固
  
  examples:
    - name: "创建用户API"
      description: "创建一个RESTful用户管理API"
      input:
        api_type: "restful"
        endpoints:
          - path: "/users"
            method: "GET"
            description: "获取用户列表"
          - path: "/users"
            method: "POST"
            description: "创建用户"
          - path: "/users/{id}"
            method: "GET"
            description: "获取用户详情"
        request_schema:
          type: "object"
          properties:
            name:
              type: "string"
            email:
              type: "string"
              format: "email"
          required: ["name", "email"]
        response_schema:
          type: "object"
          properties:
            id:
              type: "integer"
            name:
              type: "string"
            email:
              type: "string"
      output:
        code: 200
        message: "success"
        data:
          endpoints:
            - "GET /users"
            - "POST /users"
            - "GET /users/{id}"
      explanation: "成功创建用户管理API，包含三个端点"
  
  tags:
    - "后端"
    - "API"
    - "RESTful"
    - "GraphQL"
  
  execution:
    timeout_seconds: 30
    max_retries: 3
    requires_approval: false
    allowed_agents: ["L4", "L5"]
  
  resources:
    cpu: "0.5"
    memory: "512Mi"
    gpu: false
    network: true
  
  evaluation:
    success_criteria:
      - "API端点可正常访问"
      - "请求验证正确执行"
      - "响应格式符合规范"
    quality_metrics:
      - name: "response_time"
        target: 200
      - name: "error_rate"
        target: 0.01
```


## 四、技能注册表

```python
# skills/registry.py

from typing import Dict, List, Optional
from .models import SkillDefinition, SkillLevel


class SkillRegistry:
    """技能注册表 - 管理所有技能定义"""
    
    def __init__(self):
        self._skills: Dict[str, SkillDefinition] = {}
        self._skills_by_tag: Dict[str, List[str]] = {}
        self._skills_by_level: Dict[SkillLevel, List[str]] = {}
    
    def register(self, skill: SkillDefinition) -> bool:
        """注册技能"""
        if skill.id in self._skills:
            return False
        
        self._skills[skill.id] = skill
        
        # 按标签索引
        for tag in skill.tags:
            if tag not in self._skills_by_tag:
                self._skills_by_tag[tag] = []
            self._skills_by_tag[tag].append(skill.id)
        
        # 按等级索引
        if skill.level not in self._skills_by_level:
            self._skills_by_level[skill.level] = []
        self._skills_by_level[skill.level].append(skill.id)
        
        return True
    
    def get(self, skill_id: str) -> Optional[SkillDefinition]:
        """获取技能定义"""
        return self._skills.get(skill_id)
    
    def list_all(self) -> List[SkillDefinition]:
        """列出所有技能"""
        return list(self._skills.values())
    
    def list_by_tag(self, tag: str) -> List[SkillDefinition]:
        """按标签列出技能"""
        skill_ids = self._skills_by_tag.get(tag, [])
        return [self._skills[sid] for sid in skill_ids if sid in self._skills]
    
    def list_by_level(self, level: SkillLevel) -> List[SkillDefinition]:
        """按等级列出技能"""
        skill_ids = self._skills_by_level.get(level, [])
        return [self._skills[sid] for sid in skill_ids if sid in self._skills]
    
    def list_by_domain(self, domain: str) -> List[SkillDefinition]:
        """按领域列出技能"""
        return [s for s in self._skills.values() if domain in s.tags]
    
    def validate_dependencies(self, skill_ids: List[str]) -> bool:
        """验证技能依赖是否满足"""
        available = set(self._skills.keys())
        required = set()
        
        for sid in skill_ids:
            skill = self._skills.get(sid)
            if skill:
                required.update(skill.dependencies)
        
        return required.issubset(available)
    
    def get_dependency_graph(self) -> Dict[str, List[str]]:
        """获取依赖关系图"""
        graph = {}
        for sid, skill in self._skills.items():
            graph[sid] = skill.dependencies
        return graph
```


## 五、技能执行器

```python
# skills/executor.py

from typing import Dict, Any, Optional
import asyncio
from .models import SkillDefinition, SkillLevel
from .registry import SkillRegistry


class SkillExecutor:
    """技能执行器 - 负责执行技能"""
    
    def __init__(self, registry: SkillRegistry, llm_client):
        self.registry = registry
        self.llm_client = llm_client
    
    async def execute(self, skill_id: str, agent_level: str, 
                      input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行技能"""
        # 1. 获取技能定义
        skill = self.registry.get(skill_id)
        if not skill:
            return {"error": f"Skill {skill_id} not found"}
        
        # 2. 检查权限
        if agent_level not in skill.execution.allowed_agents:
            return {"error": f"Agent level {agent_level} not allowed to execute {skill_id}"}
        
        # 3. 验证输入
        if not self._validate_input(skill, input_data):
            return {"error": "Input validation failed"}
        
        # 4. 检查依赖
        if not self._check_dependencies(skill):
            return {"error": f"Dependencies not satisfied: {skill.dependencies}"}
        
        # 5. 执行技能
        try:
            result = await self._do_execute(skill, input_data)
            return {
                "code": 200,
                "message": "success",
                "data": result
            }
        except asyncio.TimeoutError:
            return {"error": f"Execution timeout after {skill.execution.timeout_seconds}s"}
        except Exception as e:
            return {"error": str(e)}
    
    def _validate_input(self, skill: SkillDefinition, input_data: Dict[str, Any]) -> bool:
        """验证输入"""
        schema = skill.input_schema
        required = schema.get("required", [])
        
        for field in required:
            if field not in input_data:
                return False
        return True
    
    def _check_dependencies(self, skill: SkillDefinition) -> bool:
        """检查依赖"""
        # 简化实现：假设依赖技能都已注册
        return True
    
    async def _do_execute(self, skill: SkillDefinition, 
                          input_data: Dict[str, Any]) -> Dict[str, Any]:
        """实际执行技能逻辑"""
        # 构建执行提示词
        prompt = self._build_prompt(skill, input_data)
        
        # 调用大模型执行
        response = await self.llm_client.chat(prompt)
        
        # 解析输出
        return self._parse_output(response)
    
    def _build_prompt(self, skill: SkillDefinition, input_data: Dict[str, Any]) -> str:
        """构建执行提示词"""
        return f"""
        请执行技能：{skill.name}
        
        技能描述：{skill.description}
        
        输入参数：
        {input_data}
        
        请按照技能规范执行，并返回JSON格式结果。
        """
    
    def _parse_output(self, response: str) -> Dict[str, Any]:
        """解析输出"""
        import json
        try:
            return json.loads(response)
        except:
            return {"raw_output": response}
```


## 六、技能API接口

```yaml
# API接口定义

api_prefix: "/api/v1/skills"

endpoints:
  # 技能管理
  - path: "/"
    method: "GET"
    description: "获取技能列表"
    response: "List[SkillDefinition]"
    
  - path: "/{skill_id}"
    method: "GET"
    description: "获取技能详情"
    response: "SkillDefinition"
    
  - path: "/"
    method: "POST"
    description: "创建技能"
    request: "SkillDefinition"
    response: "SkillDefinition"
    
  - path: "/{skill_id}"
    method: "PUT"
    description: "更新技能"
    request: "SkillDefinition"
    response: "SkillDefinition"
    
  - path: "/{skill_id}"
    method: "DELETE"
    description: "删除技能"
    response: "success"
  
  # 技能执行
  - path: "/{skill_id}/execute"
    method: "POST"
    description: "执行技能"
    request: 
      agent_id: "string"
      input: "object"
    response: "ExecutionResult"
  
  # 技能查询
  - path: "/tags/{tag}"
    method: "GET"
    description: "按标签查询技能"
    response: "List[SkillDefinition]"
    
  - path: "/domain/{domain}"
    method: "GET"
    description: "按领域查询技能"
    response: "List[SkillDefinition]"
    
  - path: "/level/{level}"
    method: "GET"
    description: "按等级查询技能"
    response: "List[SkillDefinition]"
    
  - path: "/dependencies/{skill_id}"
    method: "GET"
    description: "获取技能依赖图"
    response: "DependencyGraph"
```


## 七、技能存储

```python
# skills/repository.py

from typing import Optional, List
import json
from pathlib import Path


class SkillRepository:
    """技能存储仓库"""
    
    def __init__(self, data_dir: str = "./data/skills"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save(self, skill: SkillDefinition) -> bool:
        """保存技能"""
        file_path = self.data_dir / f"{skill.id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(skill.dict(), f, ensure_ascii=False, indent=2, default=str)
        return True
    
    def load(self, skill_id: str) -> Optional[SkillDefinition]:
        """加载技能"""
        file_path = self.data_dir / f"{skill_id}.json"
        if not file_path.exists():
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return SkillDefinition(**data)
    
    def load_all(self) -> List[SkillDefinition]:
        """加载所有技能"""
        skills = []
        for file_path in self.data_dir.glob("*.json"):
            skill = self.load(file_path.stem)
            if skill:
                skills.append(skill)
        return skills
    
    def delete(self, skill_id: str) -> bool:
        """删除技能"""
        file_path = self.data_dir / f"{skill_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False
```


## 八、在Cursor中使用

将本文档保存后，在Cursor中使用以下命令：

```
# 创建新技能
@docs/SKILL_DEFINITION_SPEC_v1.0.md 按照规范创建一个新的技能：BE-05 消息队列开发

# 实现技能注册表
@docs/SKILL_DEFINITION_SPEC_v1.0.md 实现SkillRegistry类的注册和查询功能

# 实现技能执行器
@docs/SKILL_DEFINITION_SPEC_v1.0.md 实现SkillExecutor，支持技能的超时控制和重试机制

# 加载技能库
@docs/SKILL_DEFINITION_SPEC_v1.0.md 从data/skills目录加载所有技能定义并注册
```

---

**文档结束**