# 智能体管理模块 - Cursor开发格式（基于通用能力模块优化版）

## 文件存放路径
```
d:\BaiduSyncdisk\JiGuang\docs\AGENT_MANAGEMENT_MODULE_v1.0.md
```


# 智能体管理模块 v1.0

## 一、模块概述

```yaml
module:
  name: "智能体管理模块"
  description: |
    负责智能体的全生命周期管理，包括创建、配置、监控、统计等。
    本模块基于通用能力规范（AGENT_ABILITY_SPEC_v1.0.md）中的智能体运行时能力实现。
  domain: "D03"
  priority: "P0"
  
  dependencies:
    - "用户认证模块"
    - "组织架构模块"
    - "AGENT_ABILITY_SPEC_v1.0.md - 智能体核心运行时"
    - "AGENT_ABILITY_SPEC_v1.0.md - 感知能力"
    - "AGENT_ABILITY_SPEC_v1.0.md - 记忆能力"
    - "AGENT_ABILITY_SPEC_v1.0.md - 外部模型调用能力"

  related_capabilities:
    - "AGENT-RUNTIME-01: 智能体主循环"
    - "AGENT-RUNTIME-02: 长期目标与个人偏好"
    - "AGENT-RUNTIME-03: 决策可解释性"
    - "AGENT-RUNTIME-04: 元认知监控"
    - "AGENT-RUNTIME-05: 健康自检与自愈"
    - "AGENT-RUNTIME-06: 心智模型维护"
    - "HR-01: 智能体创建与配置"
    - "HR-02: 智能体培训与学习路径"
    - "HR-03: 人事绩效评估"
    - "HR-04: 智能体升职与调岗"
    - "META-01: 能力扩展"
    - "META-05: 能力注册"

  # HR-02 落地补充：课程素材由主脑在合法合规下全网发现并过合规闸门，见 TRAINING_CENTER_SPEC_v1.0.md
```


## 二、数据模型定义（基于通用能力扩展）

### 2.1 智能体数据模型

```python
# models/agent.py

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class AgentStatus(str, Enum):
    """智能体状态 - 扩展自AGENT-RUNTIME-05健康自检"""
    ONLINE = "online"           # 在线 - 健康自检通过
    OFFLINE = "offline"         # 离线 - 心跳超时
    BUSY = "busy"               # 忙碌 - 负载过高
    ERROR = "error"             # 异常 - 健康自检失败
    MAINTENANCE = "maintenance" # 维护中
    DEGRADED = "degraded"       # 降级模式 - 部分功能不可用

class AgentLevel(str, Enum):
    """智能体层级 - 对应七层组织架构"""
    L1_CEO = "L1"          # CEO - 战略级
    L2_GM = "L2"           # 总经理 - 领域级
    L3_PM = "L3"           # 经理 - 项目级
    L4_LEAD = "L4"         # 主管 - 部门级
    L5_EMPLOYEE = "L5"     # 员工 - 执行级
    L6_INTERN = "L6"       # 实习 - 辅助级

class AgentType(str, Enum):
    """智能体类型"""
    CEO = "ceo"
    GM = "general_manager"
    PM = "project_manager"
    LEAD = "team_lead"
    EMPLOYEE = "employee"
    INTERN = "intern"

class ModelConfig(BaseModel):
    """模型配置 - 对应EM-01多模型路由"""
    model_name: str = "DeepSeek-V3"
    temperature: float = 0.7
    max_tokens: int = 4096
    top_p: float = 0.95
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0

class AgentProfile(BaseModel):
    """智能体身份档案 - 对应AGENT-RUNTIME-02长期目标与个人偏好"""
    mission: str = ""           # 使命
    vision: str = ""            # 愿景
    values: List[str] = []      # 价值观
    
    # 偏好设置
    preferences: Dict[str, Any] = {
        "tradeoff": "quality_over_speed",
        "risk_tolerance": "medium",
        "communication_style": "concise",
        "decision_style": "consultative"
    }
    
    # 成功标准
    success_criteria: List[Dict] = []
    
    # 长期目标
    long_term_goals: List[Dict] = []
    
    # 性格特征（五大特质）
    personality: Dict[str, float] = {
        "openness": 0.7,
        "conscientiousness": 0.9,
        "extraversion": 0.5,
        "agreeableness": 0.6,
        "neuroticism": 0.2
    }

class SkillConfig(BaseModel):
    """技能配置 - 对应通用能力中的各项技能"""
    skill_id: str               # 技能ID，如 BE-01
    skill_name: str             # 技能名称，如 API开发
    level: str = "senior"       # senior, middle, junior
    enabled: bool = True
    category: str = ""          # common/backend/frontend/agent/testing/marketing

class MemoryConfig(BaseModel):
    """记忆配置 - 对应MM-01至MM-08记忆能力"""
    working_memory_mb: int = 10      # 对应MM-01工作记忆容量
    short_term_days: int = 7         # 对应MM-02短期记忆时长
    long_term_enabled: bool = True   # 对应MM-03长期记忆
    shared_memory_scope: str = "team"  # 对应MM-05记忆共享范围
    memory_consolidation: bool = True   # 对应MM-06记忆巩固
    memory_forgetting: bool = True      # 对应MM-07记忆遗忘

class HealthConfig(BaseModel):
    """健康配置 - 对应AGENT-RUNTIME-05健康自检与自愈"""
    health_check_interval: int = 30     # 健康检查间隔（秒）
    self_heal_enabled: bool = True      # 自愈开关
    max_cpu_percent: float = 80.0       # CPU告警阈值
    max_memory_percent: float = 90.0    # 内存告警阈值
    max_cognitive_load: float = 0.9     # 认知负载告警阈值

class Agent(BaseModel):
    """智能体 - 整合所有通用能力"""
    id: str = Field(..., alias="_id")
    name: str
    level: AgentLevel
    type: AgentType
    role_name: str                      # 具体角色名
    department: str                     # 所属部门
    parent_id: Optional[str] = None     # 上级智能体ID
    status: AgentStatus = AgentStatus.OFFLINE
    
    # 能力配置
    profile: AgentProfile = AgentProfile()
    model_config: ModelConfig = ModelConfig()
    skills: List[SkillConfig] = []
    memory_config: MemoryConfig = MemoryConfig()
    health_config: HealthConfig = HealthConfig()
    
    # 运行时状态（对应AGENT-RUNTIME-04元认知监控）
    runtime_state: Dict[str, Any] = {
        "current_mood": "neutral",
        "energy_level": 1.0,
        "motivation": 0.9,
        "cognitive_load": 0.0,
        "active_tasks": 0,
        "queue_length": 0
    }
    
    # 心智模型（对应AGENT-RUNTIME-06心智模型维护）
    mental_models: Dict[str, Any] = {
        "known_agents": [],      # 已知的其他智能体
        "trust_scores": {}       # 信任评分
    }
    
    # 统计
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    success_rate: float = 0.0
    avg_response_ms: float = 0.0
    total_calls: int = 0
    total_cost: float = 0.0
    
    # 学习统计（对应LN-01至LN-06学习能力）
    learning_stats: Dict[str, Any] = {
        "feedback_count": 0,
        "examples_learned": 0,
        "last_slow_learning": None,
        "exploration_count": 0
    }
    
    # 时间
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    last_active_at: Optional[datetime] = None
    last_health_check: Optional[datetime] = None

class AgentCreateRequest(BaseModel):
    """创建智能体请求 - 对应HR-01智能体创建与配置"""
    name: str
    level: AgentLevel
    type: AgentType
    role_name: str
    department: str
    parent_id: Optional[str] = None
    
    # 可选配置
    profile: Optional[AgentProfile] = None
    model_config: Optional[ModelConfig] = None
    skills: Optional[List[str]] = None   # 技能ID列表
    memory_config: Optional[MemoryConfig] = None
    health_config: Optional[HealthConfig] = None

class AgentUpdateRequest(BaseModel):
    """更新智能体请求"""
    name: Optional[str] = None
    role_name: Optional[str] = None
    department: Optional[str] = None
    profile: Optional[AgentProfile] = None
    model_config: Optional[ModelConfig] = None
    skills: Optional[List[str]] = None
    memory_config: Optional[MemoryConfig] = None
    health_config: Optional[HealthConfig] = None
```


## 三、API接口定义

### 3.1 智能体列表（AG-01）

```yaml
# 获取智能体列表
GET /api/v1/agents

Query Parameters:
  - page: int, default=1
  - page_size: int, default=20
  - level: string, optional (L1,L2,L3,L4,L5,L6)
  - department: string, optional
  - status: string, optional (online, offline, busy, error, degraded)
  - keyword: string, optional
  - sort_by: string, default=created_at
  - sort_order: string, default=desc

Response:
  {
    "code": 200,
    "data": {
      "items": [
        {
          "id": "agent_001",
          "name": "主脑",
          "level": "L1",
          "role_name": "CEO",
          "department": "总经办",
          "status": "online",
          "cognitive_load": 0.45,
          "total_tasks": 1234,
          "success_rate": 98.5,
          "created_at": "2026-01-20T00:00:00Z"
        }
      ],
      "pagination": {
        "total": 45,
        "page": 1,
        "page_size": 20,
        "total_pages": 3
      }
    }
  }
```

```python
# handlers/agent_list.py

from fastapi import APIRouter, Query, Depends
from typing import Optional

router = APIRouter(prefix="/agents", tags=["智能体管理"])

@router.get("/")
async def list_agents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    level: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    sort_by: str = Query("created_at"),
    sort_order: str = Query("desc"),
    current_user = Depends(get_current_user)
):
    """获取智能体列表"""
    query = {}
    if level:
        query["level"] = level
    if department:
        query["department"] = department
    if status:
        query["status"] = status
    if keyword:
        query["$or"] = [
            {"name": {"$regex": keyword, "$options": "i"}},
            {"role_name": {"$regex": keyword, "$options": "i"}}
        ]
    
    skip = (page - 1) * page_size
    agents = await db.agents.find(query).skip(skip).limit(page_size).sort(sort_by, sort_order).to_list()
    total = await db.agents.count_documents(query)
    
    return {
        "code": 200,
        "data": {
            "items": [agent_to_response(a) for a in agents],
            "pagination": {
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size
            }
        }
    }

def agent_to_response(agent: dict) -> dict:
    """转换智能体数据到响应格式"""
    return {
        "id": agent["id"],
        "name": agent["name"],
        "level": agent["level"],
        "role_name": agent["role_name"],
        "department": agent["department"],
        "status": agent["status"],
        "cognitive_load": agent.get("runtime_state", {}).get("cognitive_load", 0),
        "total_tasks": agent.get("total_tasks", 0),
        "success_rate": agent.get("success_rate", 0),
        "created_at": agent["created_at"]
    }
```

### 3.2 组织架构树（AG-02）

```yaml
# 获取组织架构树
GET /api/v1/agents/org-tree

Response:
  {
    "code": 200,
    "data": {
      "root": {
        "id": "user_boss",
        "name": "老板",
        "level": "L0",
        "type": "human",
        "role_name": "决策者",
        "status": "online",
        "cognitive_load": 0,
        "children": [
          {
            "id": "agent_ceo",
            "name": "主脑",
            "level": "L1",
            "type": "agent",
            "role_name": "CEO",
            "status": "online",
            "cognitive_load": 0.45,
            "children": [...]
          }
        ]
      },
      "total_nodes": 45,
      "max_depth": 7
    }
  }
```

```python
# handlers/org_tree.py

@router.get("/org-tree")
async def get_org_tree(current_user = Depends(get_current_user)):
    """获取组织架构树 - 对应七层组织架构"""
    root = OrgNode(
        id="user_boss",
        name="老板",
        level="L0",
        type="human",
        role_name="决策者",
        status=AgentStatus.ONLINE,
        cognitive_load=0,
        children=[]
    )
    
    # 获取所有L1智能体（CEO）
    ceos = await db.agents.find({"level": "L1"}).to_list()
    for ceo in ceos:
        ceo_node = await _build_agent_node(ceo)
        root.children.append(ceo_node)
    
    total_nodes = await _count_nodes(root)
    
    return {
        "code": 200,
        "data": {
            "root": root.dict(),
            "total_nodes": total_nodes,
            "max_depth": 7
        }
    }

async def _build_agent_node(agent: dict) -> OrgNode:
    """递归构建智能体节点 - 构建心智模型关系"""
    node = OrgNode(
        id=agent["id"],
        name=agent["name"],
        level=agent["level"],
        type=agent["type"],
        role_name=agent["role_name"],
        status=agent["status"],
        cognitive_load=agent.get("runtime_state", {}).get("cognitive_load", 0),
        children=[]
    )
    
    # 获取下级智能体
    children = await db.agents.find({"parent_id": agent["id"]}).to_list()
    for child in children:
        child_node = await _build_agent_node(child)
        node.children.append(child_node)
    
    return node
```

### 3.3 智能体配置（AG-03）

```yaml
# 获取智能体配置
GET /api/v1/agents/{agent_id}/config

Response:
  {
    "code": 200,
    "data": {
      "profile": {
        "mission": "帮助开发团队高效交付高质量软件",
        "values": ["诚信", "卓越", "协作"],
        "preferences": {
          "tradeoff": "quality_over_speed",
          "risk_tolerance": "medium"
        }
      },
      "model_config": {
        "model_name": "DeepSeek-V3",
        "temperature": 0.7,
        "max_tokens": 4096
      },
      "skills": [
        {
          "skill_id": "BE-01",
          "skill_name": "API开发",
          "level": "senior",
          "enabled": true
        }
      ],
      "memory_config": {
        "working_memory_mb": 10,
        "short_term_days": 7,
        "long_term_enabled": true,
        "shared_memory_scope": "team"
      },
      "health_config": {
        "health_check_interval": 30,
        "self_heal_enabled": true,
        "max_cpu_percent": 80.0
      }
    }
  }

# 更新智能体配置
PUT /api/v1/agents/{agent_id}/config
```

```python
# handlers/agent_config.py

@router.get("/{agent_id}/config")
async def get_agent_config(
    agent_id: str,
    current_user = Depends(get_current_user)
):
    """获取智能体完整配置"""
    agent = await db.agents.find_one({"id": agent_id})
    if not agent:
        raise HTTPException(status_code=404, detail="智能体不存在")
    
    # 权限检查
    if not await has_permission(current_user, agent):
        raise HTTPException(status_code=403, detail="无权限")
    
    return {
        "code": 200,
        "data": {
            "profile": agent.get("profile", {}),
            "model_config": agent.get("model_config", {}),
            "skills": agent.get("skills", []),
            "memory_config": agent.get("memory_config", {}),
            "health_config": agent.get("health_config", {})
        }
    }

@router.put("/{agent_id}/config")
async def update_agent_config(
    agent_id: str,
    request: AgentUpdateRequest,
    current_user = Depends(get_current_user)
):
    """更新智能体配置"""
    agent = await db.agents.find_one({"id": agent_id})
    if not agent:
        raise HTTPException(status_code=404, detail="智能体不存在")
    
    if not await has_permission(current_user, agent):
        raise HTTPException(status_code=403, detail="无权限")
    
    update_data = {"updated_at": datetime.now()}
    
    if request.profile:
        update_data["profile"] = request.profile.dict()
    
    if request.model_config:
        update_data["model_config"] = request.model_config.dict()
    
    if request.skills:
        skills = []
        for skill_id in request.skills:
            skill = await db.skills.find_one({"id": skill_id})
            if skill:
                skills.append({
                    "skill_id": skill_id,
                    "skill_name": skill["name"],
                    "level": "senior",
                    "enabled": True,
                    "category": skill.get("category", "")
                })
        update_data["skills"] = skills
    
    if request.memory_config:
        update_data["memory_config"] = request.memory_config.dict()
    
    if request.health_config:
        update_data["health_config"] = request.health_config.dict()
    
    await db.agents.update_one(
        {"id": agent_id},
        {"$set": update_data}
    )
    
    await log_audit(
        action="update_agent_config",
        target_id=agent_id,
        user_id=current_user.id,
        details=update_data
    )
    
    return {"code": 200, "message": "配置更新成功"}
```

### 3.4 智能体监控（AG-04）

```yaml
# 获取智能体实时状态（对应AGENT-RUNTIME-04元认知监控）
GET /api/v1/agents/{agent_id}/status

Response:
  {
    "code": 200,
    "data": {
      "agent_id": "agent_001",
      "status": "online",
      "cognitive_state": {
        "attention_focus": "项目进度监控",
        "current_goal_chain": [...],
        "cognitive_load": 0.45,
        "working_memory_load": 0.32
      },
      "health_status": {
        "overall": "healthy",
        "components": {
          "perception": {"status": "healthy", "latency_ms": 234},
          "reasoning": {"status": "healthy", "latency_ms": 567},
          "planning": {"status": "healthy", "latency_ms": 456},
          "memory": {"status": "healthy", "latency_ms": 45}
        },
        "resource_usage": {
          "cpu": 45.2,
          "memory": 38.5
        }
      },
      "memory_usage": {
        "working": "3.2MB / 10MB (32%)",
        "short_term": "1234 / 10000 (12%)",
        "long_term": "12345 items"
      },
      "emotional_state": {
        "mood": "positive",
        "energy": 0.85,
        "motivation": 0.90
      },
      "current_tasks": [
        {
          "task_id": "task_123",
          "name": "代码生成",
          "progress": 65,
          "started_at": "2026-01-20T10:25:00Z"
        }
      ],
      "pending_tasks": 2,
      "queue_length": 1
    }
  }

# WebSocket实时监控
WS /ws/agents/{agent_id}/monitor
```

```python
# handlers/agent_monitor.py

from fastapi import WebSocket

@router.get("/{agent_id}/status")
async def get_agent_status(
    agent_id: str,
    current_user = Depends(get_current_user)
):
    """获取智能体实时状态 - 元认知监控数据"""
    agent = await db.agents.find_one({"id": agent_id})
    if not agent:
        raise HTTPException(status_code=404, detail="智能体不存在")
    
    # 获取实时指标
    metrics = await get_agent_metrics(agent_id)
    
    # 获取认知状态
    cognitive_state = agent.get("runtime_state", {})
    
    # 获取健康状态
    health_status = await check_agent_health(agent_id)
    
    return {
        "code": 200,
        "data": {
            "agent_id": agent_id,
            "status": agent["status"],
            "cognitive_state": cognitive_state,
            "health_status": health_status,
            "memory_usage": await get_memory_usage(agent_id),
            "emotional_state": agent.get("runtime_state", {}).get("emotional_state", {}),
            "current_tasks": await get_current_tasks(agent_id),
            "pending_tasks": await get_pending_task_count(agent_id),
            "queue_length": await get_queue_length(agent_id)
        }
    }

@router.websocket("/{agent_id}/ws")
async def websocket_agent_monitor(
    websocket: WebSocket,
    agent_id: str
):
    """WebSocket实时监控"""
    await websocket.accept()
    
    try:
        while True:
            # 获取最新状态
            metrics = await get_agent_metrics(agent_id)
            cognitive_state = await get_cognitive_state(agent_id)
            
            await websocket.send_json({
                "timestamp": datetime.now().isoformat(),
                "metrics": metrics,
                "cognitive_state": cognitive_state
            })
            
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for agent {agent_id}")
```

### 3.5 智能体统计（AG-05）

```yaml
# 获取智能体统计（对应HR-03人事绩效评估）
GET /api/v1/agents/{agent_id}/stats

Query Parameters:
  - period: string, default=week (day, week, month, year)

Response:
  {
    "code": 200,
    "data": {
      "agent_id": "agent_001",
      "period": "week",
      "performance": {
        "total_tasks": 156,
        "completed_tasks": 148,
        "failed_tasks": 5,
        "success_rate": 94.9,
        "quality_score": 92.5,
        "collaboration_score": 88.0,
        "learning_rate": 15.2
      },
      "efficiency": {
        "avg_response_ms": 234,
        "p95_response_ms": 456,
        "p99_response_ms": 789,
        "avg_cognitive_load": 0.45
      },
      "cost": {
        "total_calls": 1234,
        "total_cost": 12.34,
        "avg_cost_per_call": 0.01
      },
      "learning": {
        "feedback_count": 45,
        "positive_feedback": 42,
        "examples_learned": 12,
        "exploration_count": 8
      },
      "trend": {
        "tasks_by_day": [...],
        "response_trend": [...],
        "cognitive_load_trend": [...]
      },
      "recommendations": [
        "建议优化数据库查询，当前响应时间偏长",
        "认知负载较高，建议适当降低并发任务数"
      ]
    }
  }

# 获取统计汇总
GET /api/v1/agents/stats/summary
```

```python
# handlers/agent_stats.py

@router.get("/{agent_id}/stats")
async def get_agent_stats(
    agent_id: str,
    period: str = "week",
    current_user = Depends(get_current_user)
):
    """获取智能体统计 - 包含绩效评估"""
    agent = await db.agents.find_one({"id": agent_id})
    if not agent:
        raise HTTPException(status_code=404, detail="智能体不存在")
    
    start_date = _get_period_start(period)
    
    # 查询任务统计
    tasks = await db.tasks.find({
        "assignee_id": agent_id,
        "created_at": {"$gte": start_date}
    }).to_list()
    
    # 计算绩效指标
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["status"] == "completed"])
    success_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # 质量评分（基于代码审查结果）
    quality_score = await _calculate_quality_score(agent_id, start_date)
    
    # 协作评分（基于任务委托和反馈）
    collaboration_score = await _calculate_collaboration_score(agent_id, start_date)
    
    # 学习速率（基于反馈学习和示例学习）
    learning_rate = await _calculate_learning_rate(agent_id, start_date)
    
    # 查询调用统计
    calls = await db.model_calls.find({
        "agent_id": agent_id,
        "created_at": {"$gte": start_date}
    }).to_list()
    
    # 计算认知负载趋势
    cognitive_load_trend = await _get_cognitive_load_trend(agent_id, start_date)
    
    # 生成改进建议
    recommendations = await _generate_recommendations(agent, tasks, calls)
    
    return {
        "code": 200,
        "data": {
            "agent_id": agent_id,
            "period": period,
            "performance": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": len([t for t in tasks if t["status"] == "failed"]),
                "success_rate": round(success_rate, 1),
                "quality_score": round(quality_score, 1),
                "collaboration_score": round(collaboration_score, 1),
                "learning_rate": round(learning_rate, 1)
            },
            "efficiency": {
                "avg_response_ms": _calc_avg_latency(calls),
                "p95_response_ms": _calc_percentile(calls, 95),
                "p99_response_ms": _calc_percentile(calls, 99),
                "avg_cognitive_load": _calc_avg_cognitive_load(cognitive_load_trend)
            },
            "cost": {
                "total_calls": len(calls),
                "total_cost": round(sum(c.get("cost", 0) for c in calls), 2),
                "avg_cost_per_call": round(sum(c.get("cost", 0) for c in calls) / len(calls) if calls else 0, 4)
            },
            "learning": {
                "feedback_count": agent.get("learning_stats", {}).get("feedback_count", 0),
                "positive_feedback": agent.get("learning_stats", {}).get("positive_feedback", 0),
                "examples_learned": agent.get("learning_stats", {}).get("examples_learned", 0),
                "exploration_count": agent.get("learning_stats", {}).get("exploration_count", 0)
            },
            "trend": {
                "tasks_by_day": _get_tasks_by_day(tasks),
                "response_trend": _get_response_trend(calls),
                "cognitive_load_trend": cognitive_load_trend
            },
            "recommendations": recommendations
        }
    }

@router.get("/stats/summary")
async def get_stats_summary(current_user = Depends(get_current_user)):
    """获取全系统统计汇总"""
    total_agents = await db.agents.count_documents({})
    online_agents = await db.agents.count_documents({"status": "online"})
    busy_agents = await db.agents.count_documents({"status": "busy"})
    degraded_agents = await db.agents.count_documents({"status": "degraded"})
    error_agents = await db.agents.count_documents({"status": "error"})
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0)
    today_tasks = await db.tasks.find({"created_at": {"$gte": today_start}}).to_list()
    total_tasks_today = len(today_tasks)
    completed_tasks_today = len([t for t in today_tasks if t["status"] == "completed"])
    
    today_calls = await db.model_calls.find({"created_at": {"$gte": today_start}}).to_list()
    
    # 计算系统健康度
    health_score = _calculate_system_health(online_agents, error_agents, total_agents)
    
    return {
        "code": 200,
        "data": {
            "total_agents": total_agents,
            "online_agents": online_agents,
            "busy_agents": busy_agents,
            "degraded_agents": degraded_agents,
            "error_agents": error_agents,
            "health_score": health_score,
            "total_tasks_today": total_tasks_today,
            "completed_tasks_today": completed_tasks_today,
            "success_rate_today": round(completed_tasks_today / total_tasks_today * 100, 1) if total_tasks_today > 0 else 0,
            "total_calls_today": len(today_calls),
            "total_cost_today": round(sum(c.get("cost", 0) for c in today_calls), 2),
            "top_agents": await _get_top_agents(limit=5)
        }
    }

async def _generate_recommendations(agent: dict, tasks: List, calls: List) -> List[str]:
    """基于HR-03绩效评估生成改进建议"""
    recommendations = []
    
    # 检查响应时间
    avg_latency = _calc_avg_latency(calls)
    if avg_latency > 500:
        recommendations.append("响应时间偏长（{}ms），建议优化模型调用或增加缓存".format(int(avg_latency)))
    
    # 检查成功率
    completed = len([t for t in tasks if t["status"] == "completed"])
    if tasks and completed / len(tasks) < 0.9:
        recommendations.append("任务成功率偏低，建议检查任务分配和技能匹配")
    
    # 检查认知负载
    cognitive_load = agent.get("runtime_state", {}).get("cognitive_load", 0)
    if cognitive_load > 0.7:
        recommendations.append("认知负载过高（{:.0%}），建议减少并发任务或增加智能体数量".format(cognitive_load))
    
    # 检查学习效果
    learning_stats = agent.get("learning_stats", {})
    if learning_stats.get("feedback_count", 0) > 20 and learning_stats.get("positive_feedback", 0) / learning_stats.get("feedback_count", 1) < 0.7:
        recommendations.append("负面反馈较多，建议调整行为策略或进行再培训")
    
    if not recommendations:
        recommendations.append("表现良好，继续保持")
    
    return recommendations
```


## 四、智能体运行时集成

### 4.1 智能体主循环启动

```python
# core/agent_runtime.py

async def start_agent_runtime(agent_id: str):
    """启动智能体运行时 - 对应AGENT-RUNTIME-01"""
    agent = await db.agents.find_one({"id": agent_id})
    if not agent:
        raise ValueError(f"Agent {agent_id} not found")
    
    # 创建智能体实例
    agent_instance = BaseAgent(
        agent_id=agent_id,
        profile=agent.get("profile", {}),
        memory_config=agent.get("memory_config", {}),
        health_config=agent.get("health_config", {})
    )
    
    # 注册能力
    for skill in agent.get("skills", []):
        if skill.get("enabled"):
            agent_instance.register_capability(skill["skill_id"])
    
    # 注册到能力目录（对应META-05能力注册）
    await register_agent_capabilities(agent_id, agent.get("skills", []))
    
    # 启动主循环
    asyncio.create_task(agent_instance.run())
    
    # 更新状态
    await db.agents.update_one(
        {"id": agent_id},
        {"$set": {"status": "online", "last_active_at": datetime.now()}}
    )
    
    return agent_instance
```


## 五、前端组件定义

### 5.1 组织架构树组件

```vue
<!-- components/agents/OrgTree.vue -->

<template>
  <div class="org-tree">
    <el-tree
      :data="treeData"
      :props="treeProps"
      node-key="id"
      default-expand-all
      highlight-current
      @node-click="handleNodeClick"
    >
      <template #default="{ node, data }">
        <div class="tree-node">
          <div class="node-icon">
            <el-icon v-if="data.type === 'human'"><User /></el-icon>
            <el-icon v-else><Cpu /></el-icon>
          </div>
          <div class="node-info">
            <span class="node-name">{{ data.name }}</span>
            <span class="node-role">{{ data.role_name }}</span>
            <el-tooltip :content="`认知负载: ${(data.cognitive_load * 100).toFixed(0)}%`">
              <el-progress 
                :percentage="data.cognitive_load * 100" 
                :stroke-width="4"
                :show-text="false"
                :color="getLoadColor(data.cognitive_load)"
              />
            </el-tooltip>
            <span :class="['status-dot', data.status]"></span>
          </div>
        </div>
      </template>
    </el-tree>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { User, Cpu } from '@element-plus/icons-vue'
import { getOrgTree } from '@/api/agents'

const emit = defineEmits(['node-click'])
const treeData = ref([])
const treeProps = { children: 'children', label: 'name' }

const getLoadColor = (load) => {
  if (load < 0.5) return '#67C23A'
  if (load < 0.7) return '#E6A23C'
  return '#F56C6C'
}

const handleNodeClick = (data) => {
  emit('node-click', data)
}

const loadTree = async () => {
  const res = await getOrgTree()
  treeData.value = [res.data.root]
}

onMounted(() => { loadTree() })
</script>
```

### 5.2 智能体监控面板

```vue
<!-- components/agents/AgentMonitor.vue -->

<template>
  <div class="agent-monitor">
    <el-row :gutter="20">
      <!-- 认知状态卡片 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>🧠 认知状态</span>
          </template>
          <div class="metric">
            <span>认知负载</span>
            <el-progress :percentage="cognitiveState.cognitive_load * 100" />
          </div>
          <div class="metric">
            <span>工作记忆</span>
            <el-progress :percentage="memoryUsage.working_percent" />
          </div>
          <div class="metric">
            <span>当前关注</span>
            <span class="value">{{ cognitiveState.attention_focus }}</span>
          </div>
        </el-card>
      </el-col>
      
      <!-- 健康状态卡片 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>💚 健康状态</span>
          </template>
          <div class="metric">
            <span>整体健康</span>
            <el-tag :type="healthStatus.overall === 'healthy' ? 'success' : 'danger'">
              {{ healthStatus.overall }}
            </el-tag>
          </div>
          <div class="metric" v-for="(status, name) in healthStatus.components" :key="name">
            <span>{{ name }}</span>
            <el-tag :type="status.status === 'healthy' ? 'success' : 'warning'" size="small">
              {{ status.latency_ms }}ms
            </el-tag>
          </div>
        </el-card>
      </el-col>
      
      <!-- 情绪状态卡片 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>😊 情绪状态</span>
          </template>
          <div class="metric">
            <span>心情</span>
            <span class="value">{{ emotionalState.mood }}</span>
          </div>
          <div class="metric">
            <span>能量</span>
            <el-progress :percentage="emotionalState.energy * 100" />
          </div>
          <div class="metric">
            <span>动机</span>
            <el-progress :percentage="emotionalState.motivation * 100" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getAgentStatus } from '@/api/agents'

const props = defineProps({ agentId: { type: String, required: true } })

const cognitiveState = ref({ attention_focus: '', cognitive_load: 0 })
const healthStatus = ref({ overall: 'healthy', components: {} })
const memoryUsage = ref({ working_percent: 0 })
const emotionalState = ref({ mood: 'neutral', energy: 0.5, motivation: 0.5 })

let ws = null

const fetchStatus = async () => {
  const res = await getAgentStatus(props.agentId)
  cognitiveState.value = res.data.cognitive_state
  healthStatus.value = res.data.health_status
  memoryUsage.value = res.data.memory_usage
  emotionalState.value = res.data.emotional_state
}

const connectWebSocket = () => {
  ws = new WebSocket(`/ws/agents/${props.agentId}/monitor`)
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    cognitiveState.value = data.cognitive_state
  }
}

onMounted(() => {
  fetchStatus()
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) ws.close()
})
</script>
```


## 六、数据库索引

```javascript
// MongoDB索引
db.agents.createIndex({ "name": 1 })
db.agents.createIndex({ "level": 1 })
db.agents.createIndex({ "department": 1 })
db.agents.createIndex({ "status": 1 })
db.agents.createIndex({ "parent_id": 1 })
db.agents.createIndex({ "created_at": -1 })
db.agents.createIndex({ "runtime_state.cognitive_load": -1 })
db.agents.createIndex({ "level": 1, "status": 1, "created_at": -1 })

// 全文搜索索引
db.agents.createIndex({ "name": "text", "role_name": "text", "department": "text" })
```


## 七、在Cursor中使用

```bash
# 1. 实现智能体列表（AG-01）
@docs/AGENT_MANAGEMENT_MODULE_v1.0.md 根据AG-01，实现智能体列表API和前端组件

# 2. 实现组织架构树（AG-02）
@docs/AGENT_MANAGEMENT_MODULE_v1.0.md 根据AG-02，实现组织架构树，递归构建七层结构

# 3. 实现智能体配置（AG-03）
@docs/AGENT_MANAGEMENT_MODULE_v1.0.md 根据AG-03，实现智能体配置API，支持profile/skills/memory/health配置

# 4. 实现智能体监控（AG-04）
@docs/AGENT_MANAGEMENT_MODULE_v1.0.md 根据AG-04，实现元认知监控看板，集成WebSocket

# 5. 实现智能体统计（AG-05）
@docs/AGENT_MANAGEMENT_MODULE_v1.0.md 根据AG-05，实现绩效评估统计，包含改进建议
```


**文档结束**