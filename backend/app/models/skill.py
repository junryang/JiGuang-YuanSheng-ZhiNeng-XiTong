from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SkillCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = ""
    category: str = Field("common", description="common|backend|frontend|agent|testing|marketing")
    level: str = Field("middle", description="senior|middle|junior")
    linked_agent_ids: List[str] = Field(default_factory=list)


class SkillUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    level: Optional[str] = None
    linked_agent_ids: Optional[List[str]] = None


class SkillOut(BaseModel):
    id: str
    name: str
    description: str = ""
    category: str
    level: str
    linked_agent_ids: List[str] = Field(default_factory=list)

    @classmethod
    def from_record(cls, raw: Dict[str, Any]) -> "SkillOut":
        return cls.model_validate(dict(raw))
