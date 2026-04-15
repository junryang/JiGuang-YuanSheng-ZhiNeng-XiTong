from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field
from app.schemas.common_enums import DomainCode, Environment, TaskPriority, TaskStatus


class CEOPlanningRequest(BaseModel):
    instruction: str = Field(..., min_length=1, description="自然语言高层目标")
    project_id: str | None = None
    environment: Environment = Field("dev", description="dev|staging|prod")
    law: list[str] = Field(default_factory=list)


class CEOPlanningApplyRequest(BaseModel):
    instruction: str = Field(..., min_length=1)
    project_id: str = Field(..., description="子任务将创建在该项目下")
    environment: Environment = Field("dev", description="dev|staging|prod")
    law: list[str] = Field(default_factory=list)
    dry_run: bool = Field(False, description="为 true 时仅返回规划，不落库创建任务")
    link_to_latest_existing: bool = Field(
        False,
        description="为 true 时将首个新任务依赖到该项目最近一个已有任务，便于续接任务链",
    )
    max_create_tasks: int | None = Field(
        None,
        ge=1,
        le=50,
        description="限制本次最多落库创建任务数；为空表示按规划全量创建",
    )
    create_priorities: list[TaskPriority] = Field(
        default_factory=list,
        description="仅创建这些优先级的子任务；为空表示不过滤",
    )
    dedupe_by_name: bool = Field(
        False,
        description="为 true 时按项目内任务名去重：已存在同名任务则跳过创建",
    )
    start_after_task_id: str | None = Field(
        None,
        description="显式指定任务链起点；若提供，则首个新任务将依赖该任务",
    )


class PlanningIntent(BaseModel):
    primary: str
    labels: list[str] = Field(default_factory=list)
    confidence: float
    matched_keywords: list[str] = Field(default_factory=list)
    scores: dict[str, int] = Field(default_factory=dict)


class PlanningSubtask(BaseModel):
    title: str
    suggested_domain: DomainCode
    priority: TaskPriority
    kind: str
    context: str
    source_intent: str | None = None


class PlanningResources(BaseModel):
    suggested_roles: list[str] = Field(default_factory=list)
    project_name: str | None = None
    project_id: str | None = None


class PlanningExplainabilitySignal(BaseModel):
    type: str
    primary: str
    labels: list[str] = Field(default_factory=list)
    matched_keywords: list[str] = Field(default_factory=list)
    score: int = 0


class PlanningExplainability(BaseModel):
    rule_set: str
    signals: list[PlanningExplainabilitySignal] = Field(default_factory=list)


class CEOPlanningResponse(BaseModel):
    intent: PlanningIntent
    subtasks: list[PlanningSubtask] = Field(default_factory=list)
    resources: PlanningResources
    rationale: str
    explainability: PlanningExplainability


class PlanningTaskItem(BaseModel):
    id: str
    project_id: str
    name: str
    description: str = ""
    priority: TaskPriority = "P2"
    status: TaskStatus = "pending"
    progress: int = 0
    parent_id: str | None = None
    assignee_level: str | None = None
    assignee_role: str | None = None
    estimated_hours: int | float | None = None
    actual_hours: int | float | None = None
    dependencies: list[str] = Field(default_factory=list)
    start_date: str | None = None
    end_date: str | None = None
    completed_at: str | None = None


class DependencyPreviewItem(BaseModel):
    name: str
    depends_on_task_id: str | None = None


class DependencyEdgeItem(BaseModel):
    task_id: str
    depends_on_task_ids: list[str] = Field(default_factory=list)
    task_name: str | None = None


class CEOPlanningApplyResponse(BaseModel):
    plan: CEOPlanningResponse
    created_tasks: list[PlanningTaskItem] = Field(default_factory=list)
    created_task_ids: list[str] = Field(default_factory=list)
    created_task_id_map: dict[str, str] = Field(default_factory=dict)
    applied_dependency_edges: list[DependencyEdgeItem] = Field(default_factory=list)
    applied_count: int = 0
    applied_by_priority: dict[str, int] = Field(default_factory=dict)
    applied_by_intent_source: dict[str, int] = Field(default_factory=dict)
    intent_source_delta: dict[str, int] = Field(default_factory=dict)
    applied_risk_flags: list[str] = Field(default_factory=list)
    applied_risk_summary: dict[str, list[str]] = Field(default_factory=dict)
    applied_risk_score: int = 0
    risk_alignment: str = "consistent"
    next_action_hint: str = ""
    decision_snapshot: dict[str, object] = Field(default_factory=dict)
    decision_log_id: str | None = None
    filtered_count: int = 0
    planned_count: int = 0
    skipped_duplicates: int = 0
    skipped_duplicate_names: list[str] = Field(default_factory=list)
    no_op: bool = False
    no_op_reason: str = ""
    would_create: int = 0
    would_filter: int = 0
    would_apply: int = 0
    would_apply_by_priority: dict[str, int] = Field(default_factory=dict)
    would_skip_duplicates: int = 0
    would_skip_duplicate_names: list[str] = Field(default_factory=list)
    would_create_task_names: list[str] = Field(default_factory=list)
    would_create_by_intent_source: dict[str, int] = Field(default_factory=dict)
    would_dependency_preview: list[DependencyPreviewItem] = Field(default_factory=list)
    would_dependency_edges: list[DependencyEdgeItem] = Field(default_factory=list)
    would_risk_flags: list[str] = Field(default_factory=list)
    would_risk_summary: dict[str, list[str]] = Field(default_factory=dict)
    would_risk_score: int = 0
    would_no_op: bool = False
    would_no_op_reason: str = ""
