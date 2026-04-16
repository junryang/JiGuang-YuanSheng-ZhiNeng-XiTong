from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class StageStatus(str, Enum):
    """阶段运行状态"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class StagePhase(str, Enum):
    """阶段阶段（生命周期子阶段）"""

    PLANNING = "planning"
    APPROVAL = "approval"
    DESIGN = "design"
    EXECUTION = "execution"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    REVIEW = "review"


class Deliverable(BaseModel):
    """阶段交付物定义/归档记录（用于 definition 与 actual）"""

    # pydantic v2 会对一些内置字段名（如 BaseModel 的 schema 相关方法）进行保护；
    # 这里使用别名保留对外字段名 `schema`，同时避免同名字段触发警告。
    model_config = ConfigDict(protected_namespaces=())

    name: str
    type: str = "document"  # document/code/test/config
    template: Optional[str] = None
    required: bool = True
    schema_def: Optional[Dict[str, Any]] = Field(default=None, alias="schema")
    url: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # 非 spec 字段：用于上传/补齐后的内容落盘（JSON 存储）
    content_text: Optional[str] = None


class Approval(BaseModel):
    """阶段审批配置"""

    required: bool = True
    approver_role: str
    approver_level: str
    timeout_hours: int = 48
    auto_approve_if_no_response: bool = False
    condition: Optional[str] = None
    default_approver_role: Optional[str] = None
    default_approver_level: Optional[str] = None


class Participant(BaseModel):
    """阶段参与者（用于组织信息展示/审批追溯）"""

    role: str
    level: str
    responsibility: str


class ApprovalHistoryItem(BaseModel):
    timestamp: datetime
    approved: bool
    approver_role: Optional[str] = None
    approver_level: Optional[str] = None
    comments: Optional[str] = None


class ProjectStage(BaseModel):
    """项目阶段：包含阶段定义 + 运行态"""

    id: str
    name: str
    phase: StagePhase
    order: int

    owner_role: str
    owner_level: str
    owner_department: str

    participants: List[Participant] = Field(default_factory=list)
    deliverables: List[Deliverable] = Field(default_factory=list)
    approval: Approval

    timeout_days: int
    status: StageStatus = StageStatus.PENDING

    # 运行态
    project_id: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    actual_deliverables: List[Deliverable] = Field(default_factory=list)
    comments: Optional[str] = None
    approval_history: List[ApprovalHistoryItem] = Field(default_factory=list)


class StageStartResponse(BaseModel):
    status: str = "success"
    stage: ProjectStage


class StageCompleteRequest(BaseModel):
    deliverables: List[Deliverable] = Field(min_length=1, max_length=50)
    comments: Optional[str] = Field(default=None, max_length=20000)


class StageCompleteResponse(BaseModel):
    status: str = "success"
    stage: ProjectStage


class StageApproveRequest(BaseModel):
    approved: bool
    comments: Optional[str] = Field(default=None, max_length=20000)
    approver_role: Optional[str] = Field(default=None, max_length=80, description="可选：发起审批动作的角色，用于校验谁在审批")
    approver_level: Optional[str] = Field(default=None, max_length=10, description="可选：发起审批动作的层级，用于校验谁在审批")


class StageApproveResponse(BaseModel):
    status: str = "success"
    stage: ProjectStage


class StageDeliverableUploadResponse(BaseModel):
    status: str = "success"
    stage_id: str
    deliverable: Deliverable

