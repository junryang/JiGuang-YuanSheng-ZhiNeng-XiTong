from __future__ import annotations

from enum import StrEnum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class AgentStatus(StrEnum):
    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    ERROR = "error"
    DEGRADED = "degraded"


class AgentLayer(StrEnum):
    L0 = "L0"
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"


class AgentRole(StrEnum):
    CEO = "CEO"
    GM = "GM"
    PM = "PM"
    LEAD = "LEAD"
    EMPLOYEE = "EMPLOYEE"
    INTERN = "INTERN"


class AgentProfile(BaseModel):
    mission: Optional[str] = None
    vision: Optional[str] = None
    values: Optional[str] = None
    preferences: Optional[str] = None
    success_criteria: Optional[str] = None
    long_term_goals: List[str] = Field(default_factory=list)
    personality: Optional[str] = None


class AgentModelConfig(BaseModel):
    model_id: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class AgentSkillConfig(BaseModel):
    skill_ids: List[str] = Field(default_factory=list)


class AgentMemoryConfig(BaseModel):
    working_memory_slots: Optional[int] = None
    short_term_ttl_minutes: Optional[int] = None
    long_term_enabled: Optional[bool] = None


class AgentHealthConfig(BaseModel):
    last_heartbeat: Optional[str] = None
    error_streak: int = 0


class AgentOut(BaseModel):
    """对外返回的智能体视图（PH1-T01）；兼容 JSON Store 中的稀疏记录。"""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    level: str = Field(..., description="L0-L6")
    role: Optional[str] = Field(None, description="CEO/GM/PM/…")
    status: str = Field(default=AgentStatus.ONLINE, description="online/offline/busy/error/degraded")
    parent_id: Optional[str] = Field(None, description="上级智能体 id，根节点为空")
    domain: Optional[str] = Field(None, description="业务域，如 D02")
    profile: Optional[AgentProfile] = None
    agent_model: Optional[AgentModelConfig] = Field(
        default=None,
        alias="model_config",
        description="模型参数（JSON 字段名仍为 model_config）",
    )
    skill_config: Optional[AgentSkillConfig] = None
    memory_config: Optional[AgentMemoryConfig] = None
    health: Optional[AgentHealthConfig] = None

    @classmethod
    def from_record(cls, raw: Dict[str, Any]) -> "AgentOut":
        return cls.model_validate(dict(raw))
