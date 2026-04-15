from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field
from app.schemas.common_enums import TaskPriority, TaskStatus


class TaskFieldsBase(BaseModel):
    name: str
    description: str = ""
    priority: TaskPriority = Field("P2", description="P0|P1|P2|P3")
    status: TaskStatus = Field("pending", description="pending|assigned|in_progress|completed|failed|cancelled")
    progress: int = Field(0, ge=0, le=100)
    parent_id: Optional[str] = None
    assignee_level: Optional[str] = None
    assignee_role: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    dependencies: List[str] = Field(default_factory=list)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    completed_at: Optional[str] = None


class TaskCreateRequest(TaskFieldsBase):
    project_id: str


class TaskCreateNestedRequest(TaskFieldsBase):
    """在 /projects/{id}/tasks 下创建时路径已含 project_id。"""


class TaskUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    progress: Optional[int] = Field(None, ge=0, le=100)
    parent_id: Optional[str] = None
    assignee_level: Optional[str] = None
    assignee_role: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    dependencies: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    completed_at: Optional[str] = None


class TaskOut(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    project_id: str
    name: str
    description: str = ""
    priority: TaskPriority = "P2"
    status: TaskStatus = "pending"
    progress: int = 0
    parent_id: Optional[str] = None
    assignee_level: Optional[str] = None
    assignee_role: Optional[str] = None
    estimated_hours: Optional[float] = None
    actual_hours: Optional[float] = None
    dependencies: List[str] = Field(default_factory=list)
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    completed_at: Optional[str] = None

    @classmethod
    def from_record(cls, raw: Dict[str, Any]) -> "TaskOut":
        return cls.model_validate(dict(raw))
