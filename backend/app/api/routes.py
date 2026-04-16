from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.core.deps import get_audit_store, get_json_store, get_policy_engine
from app.services.chat_service import chunk_text_for_sse, resolve_assistant_text
from app.services.model_router import public_llm_status
from app.services.progress_service import build_gantt_payload, project_risk_summary, weighted_progress_percent
from app.core.policy_engine import PolicyEngine
from app.core.policy_guard import require_policy_allowed, require_policy_sequence
from app.core.staging_gates import require_staging_yaml_acks
from app.models.agent import AgentOut
from app.schemas.common_enums import DomainCode, Environment, ProjectStatus, ProjectType, RuntimeMode


router = APIRouter()


_RISK_BODY_PATTERN = re.compile(
    r"project=(?P<project>.*?);\s*risk_score=(?P<risk_score>\d+);\s*"
    r"blocked=(?P<blocked>\d+);\s*overdue=(?P<overdue>\d+);\s*"
    r"stalled=(?P<stalled>\d+);\s*action=(?P<action>[A-Za-z0-9_\-]+)"
)


def _normalize_agent_payload(raw: dict[str, Any]) -> dict[str, Any]:
    out = AgentOut.from_record(raw).model_dump(mode="json", by_alias=True)
    tags = out.get("tags")
    if not isinstance(tags, list):
        out["tags"] = []
    runtime_state = out.get("runtime_state")
    if not isinstance(runtime_state, dict):
        runtime_state = {}
    if "cognitive_load" not in runtime_state:
        runtime_state["cognitive_load"] = 0.0
    out["runtime_state"] = runtime_state
    return out


def _parse_risk_alert_body(body: str) -> dict[str, Any]:
    m = _RISK_BODY_PATTERN.search(str(body or ""))
    if not m:
        return {"raw_fields_valid": False, "parse_error_code": "PATTERN_MISMATCH"}
    risk_score = int(m.group("risk_score"))
    risk_level = "high" if risk_score >= 6 else ("medium" if risk_score >= 3 else "low")
    return {
        "raw_fields_valid": True,
        "parse_error_code": "OK",
        "project_name": m.group("project"),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "blocked_task_count": int(m.group("blocked")),
        "overdue_task_count": int(m.group("overdue")),
        "no_progress_in_progress_count": int(m.group("stalled")),
        "action": m.group("action"),
    }


def _parse_utc_iso(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _minutes_since(value: datetime | None, now: datetime) -> float | None:
    if value is None:
        return None
    delta = now - value
    if delta.total_seconds() < 0:
        return 0.0
    return round(delta.total_seconds() / 60.0, 1)


def _extract_push_attempts(context: dict[str, Any]) -> int | None:
    for key in ("push_attempts", "push_retry_count", "retry_count"):
        raw = context.get(key)
        if raw is None:
            continue
        try:
            value = int(raw)
        except (TypeError, ValueError):
            continue
        return max(0, value)
    return None


def _maybe_emit_project_risk_alert(
    *,
    project_id: str,
    project_name: str,
    risk_summary: dict[str, Any],
    cooldown_minutes: int,
    trigger_score: int,
    store,
    audit,
) -> bool:
    """
    当项目风险为 high 时，自动沉淀讨论提醒与审计事件。
    为避免重复刷屏：仅在最近窗口内无同类提醒时触发。
    """
    risk_score_now = int(risk_summary.get("risk_score", 0) or 0)
    if risk_score_now < max(0, int(trigger_score)):
        return False

    existing_items, _total = store.list_project_discussions(project_id, limit=50, offset=0)
    marker = "[PROJECT_RISK_ALERT]"
    window_end = datetime.now(timezone.utc)
    window_start = window_end - timedelta(minutes=max(0, int(cooldown_minutes)))
    for item in existing_items:
        if marker not in str(item.get("body", "")):
            continue
        created_at = _parse_utc_iso(item.get("created_at"))
        if created_at and created_at >= window_start:
            return False

    risk_score = int(risk_summary.get("risk_score", 0))
    blocked = int(risk_summary.get("blocked_task_count", 0))
    overdue = int(risk_summary.get("overdue_task_count", 0))
    stalled = int(risk_summary.get("no_progress_in_progress_count", 0))
    body = (
        f"{marker} project={project_name}; risk_score={risk_score}; "
        f"blocked={blocked}; overdue={overdue}; stalled={stalled}; "
        "action=review_risk_board_and_assign_owner"
    )
    store.add_project_discussion(project_id, "system-risk-bot", body)
    audit.add(
        event_type="project_risk_alert",
        policy_id="project_risk_monitor",
        policy_version="v1",
        environment="dev",
        allowed=True,
        reason="project risk level reached high",
        reason_code="PROJECT_RISK_HIGH",
        endpoint=f"/api/v1/projects/{project_id}/progress",
        context={
            "project_id": project_id,
            "risk_summary": risk_summary,
        },
    )
    return True


def _risk_alert_cooldown_minutes(engine: PolicyEngine, environment: str) -> int:
    block = engine.get_environment_policy(environment) if environment else {}
    raw = block.get("risk_alert_cooldown_minutes", 30)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = 30
    return max(0, value)


def _risk_alert_trigger_score(engine: PolicyEngine, environment: str) -> int:
    block = engine.get_environment_policy(environment) if environment else {}
    raw = block.get("risk_alert_trigger_score", 6)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = 6
    return max(0, value)


def _latest_risk_alert_at(project_id: str, store) -> datetime | None:
    marker = "[PROJECT_RISK_ALERT]"
    items, _total = store.list_project_discussions(project_id, limit=100, offset=0)
    for item in items:
        if marker not in str(item.get("body", "")):
            continue
        created_at = _parse_utc_iso(item.get("created_at"))
        if created_at:
            return created_at
    return None


def _risk_alert_state(*, project_id: str, cooldown_minutes: int, store) -> dict[str, Any]:
    latest = _latest_risk_alert_at(project_id, store)
    if latest is None:
        return {
            "cooldown_minutes": cooldown_minutes,
            "last_alert_at": None,
            "next_eligible_at": None,
            "cooldown_active": False,
        }
    now = datetime.now(timezone.utc)
    next_eligible = latest + timedelta(minutes=max(0, cooldown_minutes))
    return {
        "cooldown_minutes": cooldown_minutes,
        "last_alert_at": latest.isoformat(),
        "next_eligible_at": next_eligible.isoformat(),
        "cooldown_active": now < next_eligible,
    }


def _risk_alert_history(
    project_id: str, store, *, limit: int = 5, offset: int = 0, cooldown_minutes: int = 30
) -> list[dict[str, Any]]:
    marker = "[PROJECT_RISK_ALERT]"
    items, _total = store.list_project_discussions(project_id, limit=100, offset=0)
    rows: list[dict[str, Any]] = []
    valid_offset = max(0, int(offset))
    matched = 0
    for item in items:
        body = str(item.get("body", ""))
        if marker not in body:
            continue
        if matched < valid_offset:
            matched += 1
            continue
        created_at = str(item.get("created_at") or "")
        created_dt = _parse_utc_iso(created_at)
        cooldown_start_at = created_dt.isoformat() if created_dt else None
        cooldown_end_at = (created_dt + timedelta(minutes=max(0, cooldown_minutes))).isoformat() if created_dt else None
        cooldown_active_now = bool(
            created_dt and datetime.now(timezone.utc) < (created_dt + timedelta(minutes=max(0, cooldown_minutes)))
        )
        rows.append(
            {
                "id": item.get("id"),
                "author": item.get("author"),
                "created_at": created_at,
                "body": body,
                "parsed": _parse_risk_alert_body(body),
                "cooldown_snapshot": {
                    "cooldown_minutes": max(0, cooldown_minutes),
                    "cooldown_start_at": cooldown_start_at,
                    "cooldown_end_at": cooldown_end_at,
                    "cooldown_active_now": cooldown_active_now,
                },
            }
        )
        if len(rows) >= max(1, min(int(limit), 50)):
            break
    return rows


def _risk_alert_history_total(project_id: str, store) -> int:
    marker = "[PROJECT_RISK_ALERT]"
    items, _total = store.list_project_discussions(project_id, limit=500, offset=0)
    return sum(1 for item in items if marker in str(item.get("body", "")))


def _risk_alert_history_has_more(project_id: str, store, *, offset: int, limit: int) -> bool:
    total = _risk_alert_history_total(project_id=project_id, store=store)
    return max(0, int(offset)) + max(1, min(int(limit), 50)) < total


class PolicyEvalRequest(BaseModel):
    policy_id: str = Field(..., description="e.g. CEO-POLICY-13")
    environment: Environment = Field(..., description="dev|staging|prod")
    context: dict = Field(default_factory=dict)


class HighRiskPublishRequest(BaseModel):
    title: str
    content: str
    environment: Environment = Field(..., description="dev|staging|prod")
    law: list[str] = Field(default_factory=list)
    approved: bool = False


class RuntimeModeRequest(BaseModel):
    mode: RuntimeMode = Field(..., description="normal|degraded")


class CreateSessionRequest(BaseModel):
    title: str = "default"


class SendMessageRequest(BaseModel):
    message: str
    environment: Environment = "dev"
    law: list[str] = Field(default_factory=list)


class StagingPrecheck(BaseModel):
    """staging 环境创建项目时的预检：人工四项 + 与 ceo_policy.environment_policy.staging 键一一对齐的 ack。"""

    owner_confirmed: bool = False
    contract_validated: bool = False
    rollback_plan_ack: bool = False
    audit_trail_ready: bool = False
    staging_policy_acks: dict[str, bool] = Field(
        default_factory=dict,
        description="须覆盖 YAML 中 staging 块全部键，且值为 true（表示已读并确认该条环境策略）",
    )


class OrchestrationPlanRequest(BaseModel):
    """主脑多工具编排入口（CEO-POLICY-09）。"""

    name: str = "adhoc"
    steps: list[str] = Field(default_factory=list, description="工具/步骤标识，如 MCP、WEB-04")
    environment: Environment = Field("dev", description="dev|staging|prod")
    law: list[str] = Field(default_factory=list)
    use_optional_tools: bool = False
    approved: bool = Field(False, description="staging/prod 在 high_risk_requires_approval 下启用可选工具链时需 true")


class CreateProjectRequest(BaseModel):
    name: str
    domain: DomainCode = Field(..., description="D01-D08 等业务域编码")
    project_type: ProjectType = Field(..., description="new_feature|optimization|bug_fix")
    environment: Environment = Field("dev", description="dev|staging|prod")
    law: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list, description="项目标签（v1.1）")
    acceptance_contract: str = Field("", description="委托/验收约定引用（CEO-POLICY-12）")
    staging_precheck: StagingPrecheck | None = None


class UpdateProjectRequest(BaseModel):
    name: str | None = None
    domain: DomainCode | None = None
    project_type: ProjectType | None = None
    environment: Environment | None = None
    tags: list[str] | None = None
    milestones: Optional[List[Dict[str, Any]]] = None
    retrospective_report: str | None = Field(None, max_length=20000, description="项目复盘报告（Markdown 或纯文本）")


class ProjectStatusBody(BaseModel):
    status: ProjectStatus = Field(
        ...,
        description="draft|pending_approval|approved|rejected|in_progress|completed|cancelled",
    )


class SubmitApprovalBody(BaseModel):
    approval_chain: list[str] | None = Field(
        default=None,
        description="审批链层级编码，默认 L3→L2→L1（经理→总经理→主脑）",
    )


class ApproveBody(BaseModel):
    level: str = Field(..., description="当前节点层级，须与 approval.chain[step] 一致")


class RejectBody(BaseModel):
    level: str = Field(..., description="当前节点层级")
    reason: str = Field(..., min_length=1)


class ApprovalApplicationRequest(BaseModel):
    project_id: str = Field(..., min_length=1)
    approval_chain: list[str] | None = Field(default=None, description="可选覆盖默认审批链")


class ApprovalActionRequest(BaseModel):
    level: str = Field(..., min_length=1)
    reason: str | None = None


class ProjectDiscussionPost(BaseModel):
    body: str = Field(..., min_length=1, max_length=8000)
    author: str = Field("anonymous", max_length=80)


class AgentReflectRequest(BaseModel):
    instruction: str = Field("请基于当前任务做一次简短复盘，并给出下一步改进项。", max_length=2000)
    environment: Environment = Field("dev", description="dev|staging|prod")
    law: list[str] = Field(default_factory=lambda: ["LAW-05"])


class WebhookCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    url: str = Field(..., min_length=1, max_length=2000)
    events: list[str] = Field(default_factory=list, description="事件列表，如 project.updated、task.created")
    enabled: bool = True
    secret: str = Field("", max_length=256)


class WebhookUpdateRequest(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=120)
    url: str | None = Field(None, min_length=1, max_length=2000)
    events: list[str] | None = None
    enabled: bool | None = None
    secret: str | None = Field(None, max_length=256)


class GitSyncAuditEventRequest(BaseModel):
    branch: str = Field("main", min_length=1, max_length=128)
    status: str = Field(..., description="success|failure|skipped")
    message: str = Field("", max_length=2000)
    source: str = Field("git_auto_sync.ps1", max_length=120)
    environment: Environment = Field("dev", description="dev|staging|prod")
    context: dict[str, Any] = Field(default_factory=dict)


class AgentBatchCreateItem(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    level: str = Field(..., description="L0-L6")
    role: str = Field(..., description="CEO|GM|PM|LEAD|EMPLOYEE|INTERN")
    status: str = Field("online", description="online|offline|busy|error|degraded")
    parent_id: str | None = None
    domain: DomainCode | None = None


class AgentBatchCreateRequest(BaseModel):
    items: list[AgentBatchCreateItem] = Field(..., min_length=1, max_length=100)


class AgentSkillsReplaceRequest(BaseModel):
    skill_ids: list[str] = Field(default_factory=list, description="将智能体技能关联替换为该列表")


def _validate_staging_precheck(payload: CreateProjectRequest, engine: PolicyEngine) -> None:
    if payload.environment != "staging":
        return
    p = payload.staging_precheck
    if not p:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "STAGING_PRECHECK_INCOMPLETE",
                "reason": "staging 环境必须提供 staging_precheck 且全部通过",
            },
        )
    if not (p.owner_confirmed and p.contract_validated and p.rollback_plan_ack and p.audit_trail_ready):
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "STAGING_PRECHECK_INCOMPLETE",
                "reason": "staging 预检项未全部确认",
                "fields": {
                    "owner_confirmed": p.owner_confirmed,
                    "contract_validated": p.contract_validated,
                    "rollback_plan_ack": p.rollback_plan_ack,
                    "audit_trail_ready": p.audit_trail_ready,
                },
            },
        )
    require_staging_yaml_acks(engine=engine, acks=p.staging_policy_acks)

    staging = engine.get_environment_policy("staging")
    if staging.get("strict_law_bundle"):
        law = payload.law or []
        if "LAW-04" not in law or "LAW-05" not in law:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "STAGING_STRICT_LAW_BUNDLE",
                    "reason": "staging.strict_law_bundle 为 true 时 law 须包含 LAW-04 与 LAW-05",
                    "law": law,
                },
            )


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/agents/org-tree")
def agents_org_tree(store=Depends(get_json_store)):
    return {"roots": store.get_org_tree()}


@router.get("/agents")
def agents(
    store=Depends(get_json_store),
    level: str | None = None,
    status: str | None = None,
    q: str | None = None,
    capability_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
):
    items, total = store.list_agents(level=level, status=status, q=q, limit=limit, offset=offset)
    if capability_id:
        cap = str(capability_id).strip()
        items = [a for a in items if cap in list((a.get("skill_config") or {}).get("skill_ids") or [])]
        total = len(items)
    return {
        "items": [_normalize_agent_payload(a) for a in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/agents/{agent_id}")
def agent_detail(agent_id: str, store=Depends(get_json_store)):
    try:
        raw = store.get_agent(agent_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return _normalize_agent_payload(raw)


@router.post("/agents/{agent_id}/reflect")
def reflect_agent(
    agent_id: str,
    payload: AgentReflectRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
    store=Depends(get_json_store),
):
    require_policy_allowed(
        engine=engine,
        audit=audit,
        request=request,
        policy_id="CEO-POLICY-11",
        environment=payload.environment,
        context={"law": payload.law or ["LAW-05"], "explainable": True},
        event_type="agent_reflect_policy",
    )
    try:
        agent = store.get_agent(agent_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    status = str(agent.get("status", "unknown"))
    role = str(agent.get("role", "UNKNOWN"))
    reflection_text = (
        f"[SELF_REFLECTION] agent={agent_id}; role={role}; status={status}; "
        f"instruction={payload.instruction}; "
        "improvement=clarify_next_actions_and_risk_owner"
    )
    memory = store.append_working_memory(agent_id, reflection_text)
    audit.add(
        event_type="agent_reflect_triggered",
        policy_id="AGENT-RUNTIME-11",
        policy_version="v1",
        environment=payload.environment,
        allowed=True,
        reason="agent self reflection persisted",
        reason_code="AGENT_REFLECTION_CREATED",
        endpoint=f"/api/v1/agents/{agent_id}/reflect",
        context={"agent_id": agent_id, "memory_id": memory.get("id")},
    )
    return {
        "agent_id": agent_id,
        "reflection": {
            "memory_id": memory.get("id"),
            "content": memory.get("content"),
            "created_at": memory.get("created_at"),
        },
    }


@router.post("/agents/batch", status_code=201)
def create_agents_batch(payload: AgentBatchCreateRequest, store=Depends(get_json_store)):
    created: list[dict[str, Any]] = []
    for item in payload.items:
        try:
            created_row = store.create_agent(item.model_dump())
        except ValueError as e:
            raise HTTPException(status_code=400, detail={"error_code": "INVALID_PARENT_AGENT", "reason": str(e)})
        created.append(_normalize_agent_payload(created_row))
    return {"items": created, "total": len(created)}


@router.get("/agents/{agent_id}/skills")
def list_agent_skills(agent_id: str, store=Depends(get_json_store)):
    try:
        rows = store.list_agent_skills(agent_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"items": rows, "total": len(rows)}


@router.put("/agents/{agent_id}/skills")
def replace_agent_skills(agent_id: str, payload: AgentSkillsReplaceRequest, store=Depends(get_json_store)):
    try:
        rows = store.replace_agent_skills(agent_id, payload.skill_ids)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"items": rows, "total": len(rows)}


@router.get("/projects")
def projects(store=Depends(get_json_store)):
    return store.list_projects()


@router.get("/projects/pending-approvals")
def list_pending_approvals(store=Depends(get_json_store)):
    return {"items": store.list_projects_pending_approval()}


@router.get("/approvals/pending")
def list_pending_approvals_v11(
    store=Depends(get_json_store),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    rows = store.list_projects_pending_approval()
    total = len(rows)
    off = max(0, int(offset))
    lim = max(1, min(int(limit), 500))
    return {"items": rows[off : off + lim], "total": total, "limit": lim, "offset": off}


@router.post("/projects/{project_id}/submit")
def submit_project_for_approval(
    project_id: str,
    payload: SubmitApprovalBody,
    store=Depends(get_json_store),
):
    try:
        return store.submit_for_approval(project_id, chain=payload.approval_chain)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/approve")
def approve_project(project_id: str, payload: ApproveBody, store=Depends(get_json_store)):
    try:
        return store.approve_project_step(project_id, payload.level)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/projects/{project_id}/reject")
def reject_project(project_id: str, payload: RejectBody, store=Depends(get_json_store)):
    try:
        return store.reject_project_approval(project_id, payload.level, payload.reason)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/approvals/applications", status_code=201)
def create_approval_application(payload: ApprovalApplicationRequest, store=Depends(get_json_store)):
    try:
        return store.submit_for_approval(payload.project_id, chain=payload.approval_chain)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/approvals/{approval_id}/approve")
def approve_application(approval_id: str, payload: ApprovalActionRequest, store=Depends(get_json_store)):
    try:
        return store.approve_project_step(approval_id, payload.level)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/approvals/{approval_id}/reject")
def reject_application(approval_id: str, payload: ApprovalActionRequest, store=Depends(get_json_store)):
    reason = str(payload.reason or "").strip()
    if not reason:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "APPROVAL_REJECT_REASON_REQUIRED", "reason": "reason is required when rejecting approval"},
        )
    try:
        return store.reject_project_approval(approval_id, payload.level, reason)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/projects/{project_id}/progress")
def project_progress(
    project_id: str,
    engine=Depends(get_policy_engine),
    store=Depends(get_json_store),
    audit=Depends(get_audit_store),
):
    try:
        proj = store.get_project(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    tasks, _total = store.list_tasks(project_id=project_id, limit=500, offset=0)
    overall, calc_meta = weighted_progress_percent(tasks)
    risk = project_risk_summary(tasks)
    cooldown_minutes = _risk_alert_cooldown_minutes(engine, str(proj.get("environment") or "dev"))
    trigger_score = _risk_alert_trigger_score(engine, str(proj.get("environment") or "dev"))
    risk_alert_triggered = _maybe_emit_project_risk_alert(
        project_id=project_id,
        project_name=str(proj.get("name", project_id)),
        risk_summary=risk,
        cooldown_minutes=cooldown_minutes,
        trigger_score=trigger_score,
        store=store,
        audit=audit,
    )
    completed = sum(1 for t in tasks if str(t.get("status")) == "completed")
    risk_alert_state = _risk_alert_state(project_id=project_id, cooldown_minutes=cooldown_minutes, store=store)
    return {
        "project_id": project_id,
        "project_status": proj.get("status"),
        "overall_progress": round(overall, 2),
        "calculation": calc_meta,
        "risk_summary": risk,
        "risk_alert_triggered": risk_alert_triggered,
        "risk_alert_state": risk_alert_state,
        "risk_alert_trigger_score": trigger_score,
        "task_count": len(tasks),
        "completed_task_count": completed,
        "milestones": proj.get("milestones") or [],
    }


@router.get("/projects/{project_id}/overview")
def project_overview(
    project_id: str,
    engine=Depends(get_policy_engine),
    store=Depends(get_json_store),
    risk_alert_limit: int = Query(5, ge=1, le=50, description="风险提醒历史返回条数，最大 50"),
    risk_alert_history_offset: int = Query(0, ge=0, description="风险提醒历史偏移量（分页）"),
):
    try:
        proj = store.get_project(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    tasks, _total = store.list_tasks(project_id=project_id, limit=500, offset=0)
    overall, calc_meta = weighted_progress_percent(tasks)
    risk = project_risk_summary(tasks)
    cooldown_minutes = _risk_alert_cooldown_minutes(engine, str(proj.get("environment") or "dev"))
    risk_alert_state = _risk_alert_state(project_id=project_id, cooldown_minutes=cooldown_minutes, store=store)
    risk_alert_history = _risk_alert_history(
        project_id=project_id,
        store=store,
        limit=risk_alert_limit,
        offset=risk_alert_history_offset,
        cooldown_minutes=cooldown_minutes,
    )
    risk_alert_history_total = _risk_alert_history_total(project_id=project_id, store=store)
    risk_alert_history_has_more = _risk_alert_history_has_more(
        project_id=project_id, store=store, offset=risk_alert_history_offset, limit=risk_alert_limit
    )
    risk_alert_history_next_offset = (
        risk_alert_history_offset + len(risk_alert_history) if risk_alert_history_has_more else None
    )
    risk_alert_history_prev_offset = max(0, risk_alert_history_offset - risk_alert_limit) if risk_alert_history_offset > 0 else None
    completed = sum(1 for t in tasks if str(t.get("status")) == "completed")
    team_items = store.project_team_from_tasks(project_id)
    discussions, discussion_total = store.list_project_discussions(project_id, limit=5, offset=0)
    return {
        "project": proj,
        "progress": {
            "overall_progress": round(overall, 2),
            "calculation": calc_meta,
            "task_count": len(tasks),
            "completed_task_count": completed,
            "milestones": proj.get("milestones") or [],
        },
        "risk_summary": risk,
        "risk_alert_state": risk_alert_state,
        "risk_alert_history": risk_alert_history,
        "risk_alert_history_returned_count": len(risk_alert_history),
        "risk_alert_history_page_size": risk_alert_limit,
        "risk_alert_history_total": risk_alert_history_total,
        "risk_alert_history_has_more": risk_alert_history_has_more,
        "risk_alert_history_next_offset": risk_alert_history_next_offset,
        "risk_alert_history_prev_offset": risk_alert_history_prev_offset,
        "risk_alert_history_pagination": {
            "offset": max(0, risk_alert_history_offset),
            "limit": max(1, min(risk_alert_limit, 50)),
            "returned_count": len(risk_alert_history),
            "total": risk_alert_history_total,
            "has_more": risk_alert_history_has_more,
            "next_offset": risk_alert_history_next_offset,
            "prev_offset": risk_alert_history_prev_offset,
        },
        "team": {
            "items": team_items,
            "member_group_count": len(team_items),
        },
        "discussion": {
            "recent_items": discussions,
            "total": discussion_total,
        },
    }


@router.get("/projects/{project_id}/gantt")
def project_gantt(project_id: str, store=Depends(get_json_store)):
    try:
        store.get_project(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    tasks, _total = store.list_tasks(project_id=project_id, limit=500, offset=0)
    return build_gantt_payload(project_id, tasks)


@router.get("/projects/{project_id}/team")
def project_team(project_id: str, store=Depends(get_json_store)):
    try:
        items = store.project_team_from_tasks(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"items": items}


@router.get("/projects/{project_id}/discussion")
def list_project_discussion(
    project_id: str,
    store=Depends(get_json_store),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    try:
        items, total = store.list_project_discussions(project_id, limit=limit, offset=offset)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.post("/projects/{project_id}/discussion", status_code=201)
def post_project_discussion(project_id: str, payload: ProjectDiscussionPost, store=Depends(get_json_store)):
    try:
        return store.add_project_discussion(project_id, payload.author, payload.body)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/projects/{project_id}")
def get_project(project_id: str, store=Depends(get_json_store)):
    try:
        return store.get_project(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/projects")
def create_project(
    payload: CreateProjectRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
    store=Depends(get_json_store),
):
    _validate_staging_precheck(payload, engine)

    contract_ref = payload.acceptance_contract.strip()
    if payload.environment == "dev" and not contract_ref:
        contract_ref = "dev-placeholder-contract"

    ctx12 = {
        "law": payload.law or ["LAW-05"],
        "acceptance_contract": contract_ref,
    }
    require_policy_allowed(
        engine=engine,
        audit=audit,
        request=request,
        policy_id="CEO-POLICY-12",
        environment=payload.environment,
        context=ctx12,
        event_type="project_create_policy_12",
    )

    record = {
        "name": payload.name,
        "domain": payload.domain,
        "project_type": payload.project_type,
        "environment": payload.environment,
        "status": "draft",
        "law": payload.law,
        "tags": [str(x).strip() for x in (payload.tags or []) if str(x).strip()][:20],
        "acceptance_contract": contract_ref,
        "staging_precheck": payload.staging_precheck.model_dump() if payload.staging_precheck else None,
    }
    return store.create_project(record)


@router.put("/projects/{project_id}")
def update_project(project_id: str, payload: UpdateProjectRequest, store=Depends(get_json_store)):
    patch = payload.model_dump(exclude_none=True)
    if not patch:
        try:
            return store.get_project(project_id)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e))
    try:
        return store.update_project(project_id, patch)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/projects/{project_id}")
def delete_project(project_id: str, store=Depends(get_json_store)):
    try:
        store.delete_project(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=204)


@router.patch("/projects/{project_id}/status")
def patch_project_status(project_id: str, payload: ProjectStatusBody, store=Depends(get_json_store)):
    try:
        return store.transition_project_status(project_id, payload.status)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error_code": "INVALID_STATUS_TRANSITION", "reason": str(e)})


@router.post("/chat/sessions")
def create_chat_session(payload: CreateSessionRequest, store=Depends(get_json_store)):
    return store.create_session(payload.title)


@router.get("/chat/sessions")
def list_chat_sessions(store=Depends(get_json_store)):
    return store.list_sessions()


@router.get("/chat/history")
def chat_history(
    store=Depends(get_json_store),
    limit: int = Query(20, ge=1, le=200, description="返回最近会话数量"),
    message_limit: int = Query(20, ge=1, le=500, description="每个会话返回的消息条数"),
):
    sessions = store.list_sessions()
    recent_sessions = sessions[-max(1, min(int(limit), 200)) :]
    rows: list[dict[str, Any]] = []
    for s in recent_sessions:
        sid = str(s.get("id"))
        try:
            msgs = store.get_messages(sid)
        except KeyError:
            msgs = []
        tail = msgs[-max(1, min(int(message_limit), 500)) :]
        rows.append(
            {
                "id": sid,
                "title": s.get("title"),
                "message_count": len(msgs),
                "messages": tail,
            }
        )
    return {"sessions": rows, "total_sessions": len(sessions), "returned_sessions": len(rows)}


@router.get("/chat/sessions/{session_id}/messages")
def list_session_messages(session_id: str, store=Depends(get_json_store)):
    try:
        return {"messages": store.get_messages(session_id)}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/llm/status")
def llm_status():
    return public_llm_status()


@router.post("/chat/sessions/{session_id}/messages")
async def send_chat_message(
    session_id: str,
    payload: SendMessageRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
    store=Depends(get_json_store),
):
    require_policy_allowed(
        engine=engine,
        audit=audit,
        request=request,
        policy_id="CEO-POLICY-11",
        environment=payload.environment,
        context={"law": payload.law or ["LAW-05"], "explainable": True},
        event_type="chat_dispatch_policy",
    )
    try:
        user_msg = store.add_message(session_id, "user", payload.message)
        history = store.get_messages(session_id)
        assistant_text = await resolve_assistant_text(history)
        assistant_msg = store.add_message(session_id, "assistant", assistant_text)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"messages": [user_msg, assistant_msg]}


@router.post("/chat/sessions/{session_id}/messages/stream")
async def stream_chat_message(
    session_id: str,
    payload: SendMessageRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
    store=Depends(get_json_store),
):
    require_policy_allowed(
        engine=engine,
        audit=audit,
        request=request,
        policy_id="CEO-POLICY-11",
        environment=payload.environment,
        context={"law": payload.law or ["LAW-05"], "explainable": True},
        event_type="chat_dispatch_policy_stream",
    )
    try:
        store.add_message(session_id, "user", payload.message)
        history = store.get_messages(session_id)
        full_text = await resolve_assistant_text(history)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    async def event_gen():
        yield f"data: {json.dumps({'type': 'start'}, ensure_ascii=False)}\n\n".encode("utf-8")
        # v1.1: 在正式输出 delta 前先发送可解释的 thinking_steps 事件。
        thinking_steps = [
            "读取最近会话上下文并识别用户意图",
            "结合策略门禁与历史记忆生成回复草稿",
            "整理输出为可读答复并分片流式返回",
        ]
        yield f"data: {json.dumps({'type': 'thinking_steps', 'steps': thinking_steps}, ensure_ascii=False)}\n\n".encode(
            "utf-8"
        )
        for part in chunk_text_for_sse(full_text):
            payload_line = {"type": "delta", "content": part}
            yield f"data: {json.dumps(payload_line, ensure_ascii=False)}\n\n".encode("utf-8")
            await asyncio.sleep(0)
        assistant_msg = store.add_message(session_id, "assistant", full_text)
        yield f"data: {json.dumps({'type': 'done', 'assistant_message': assistant_msg}, ensure_ascii=False)}\n\n".encode(
            "utf-8"
        )

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@router.get("/policy/environment/{environment}")
def get_environment_policy_snapshot(environment: Environment, engine=Depends(get_policy_engine)):
    block = engine.get_environment_policy(environment)
    if not block:
        raise HTTPException(status_code=404, detail=f"environment_policy.{environment} 未配置")
    return {"environment": environment, "policy": block}


@router.post("/orchestration/plans")
def create_orchestration_plan(
    payload: OrchestrationPlanRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
):
    require_policy_allowed(
        engine=engine,
        audit=audit,
        request=request,
        policy_id="CEO-POLICY-09",
        environment=payload.environment,
        context={"law": payload.law or [], "explainable": True},
        event_type="orchestration_plan_policy_09",
    )

    env_pol = engine.get_environment_policy(payload.environment)
    if payload.use_optional_tools and env_pol.get("high_risk_requires_approval") and not payload.approved:
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": "OPTIONAL_TOOLS_APPROVAL_REQUIRED",
                "reason": "当前环境 high_risk_requires_approval=true，启用可选工具链需 approved=true",
                "environment": payload.environment,
            },
        )

    if env_pol.get("strict_law_bundle"):
        law = payload.law or []
        if "LAW-04" not in law or "LAW-05" not in law:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "STRICT_LAW_BUNDLE",
                    "reason": "strict_law_bundle 为 true 时 law 须包含 LAW-04 与 LAW-05",
                    "environment": payload.environment,
                },
            )

    plan_ref = f"plan-{uuid4().hex[:12]}"
    return {
        "plan_ref": plan_ref,
        "name": payload.name,
        "steps": payload.steps,
        "environment": payload.environment,
        "use_optional_tools": payload.use_optional_tools,
    }


@router.post("/policy/evaluate")
def evaluate_policy(payload: PolicyEvalRequest, request: Request, engine=Depends(get_policy_engine), audit=Depends(get_audit_store)):
    decision = engine.evaluate(payload.policy_id, payload.environment, payload.context)
    audit.add(
        event_type="policy_evaluate",
        policy_id=decision.policy_id,
        policy_version=decision.version,
        environment=decision.environment,
        allowed=decision.allowed,
        reason=decision.reason,
        endpoint=str(request.url.path),
    )
    if not decision.allowed:
        raise HTTPException(
            status_code=403,
            detail={
                "allowed": False,
                "reason": decision.reason,
                "error_code": decision.error_code,
                "policy_id": decision.policy_id,
                "environment": decision.environment,
                "policy_version": decision.version,
            },
        )
    return {
        "allowed": True,
        "reason": decision.reason,
        "error_code": decision.error_code,
        "policy_id": decision.policy_id,
        "environment": decision.environment,
        "policy_version": decision.version,
    }


@router.post("/runtime/mode")
def set_runtime_mode(payload: RuntimeModeRequest, request: Request):
    request.app.state.runtime_mode = payload.mode
    return {"runtime_mode": payload.mode}


@router.get("/runtime/mode")
def get_runtime_mode(request: Request):
    return {"runtime_mode": request.app.state.runtime_mode}


@router.get("/audit/events")
def list_audit_events(
    limit: int = 100,
    event_type_prefix: str | None = Query(
        None,
        description="仅返回 event_type 以此前缀开头的事件（如 delegation）",
    ),
    policy_id: str | None = Query(
        None,
        description="仅返回匹配 policy_id 的事件（如 collaboration 或 CEO-POLICY-13）",
    ),
    environment: Environment | None = Query(
        None,
        description="仅返回匹配环境的事件（dev|staging|prod）",
    ),
    audit=Depends(get_audit_store),
):
    return {
        "events": audit.list(
            limit=limit,
            event_type_prefix=event_type_prefix,
            policy_id=policy_id,
            environment=environment,
        )
    }


@router.get("/audit/logs")
def list_audit_logs(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    event_type_prefix: str | None = Query(None),
    policy_id: str | None = Query(None),
    environment: Environment | None = Query(None),
    audit=Depends(get_audit_store),
):
    rows = audit.list(
        limit=5000,
        event_type_prefix=event_type_prefix,
        policy_id=policy_id,
        environment=environment,
    )
    total = len(rows)
    off = max(0, int(offset))
    lim = max(1, min(int(limit), 500))
    return {
        "items": rows[off : off + lim],
        "total": total,
        "limit": lim,
        "offset": off,
    }


@router.post("/webhooks", status_code=201)
def create_webhook(payload: WebhookCreateRequest, store=Depends(get_json_store)):
    url = str(payload.url or "").strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "INVALID_WEBHOOK_URL",
                "reason": "url must start with http:// or https://",
            },
        )
    return store.create_webhook(payload.model_dump())


@router.get("/webhooks")
def list_webhooks(
    store=Depends(get_json_store),
    enabled: bool | None = Query(None, description="可选按启用状态过滤"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    items, total = store.list_webhooks(enabled=enabled, limit=limit, offset=offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/webhooks/{webhook_id}")
def get_webhook(webhook_id: str, store=Depends(get_json_store)):
    try:
        return store.get_webhook(webhook_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/webhooks/{webhook_id}")
def update_webhook(webhook_id: str, payload: WebhookUpdateRequest, store=Depends(get_json_store)):
    patch = payload.model_dump(exclude_none=True)
    if "url" in patch:
        url = str(patch.get("url") or "").strip()
        if not (url.startswith("http://") or url.startswith("https://")):
            raise HTTPException(
                status_code=400,
                detail={"error_code": "INVALID_WEBHOOK_URL", "reason": "url must start with http:// or https://"},
            )
    try:
        return store.update_webhook(webhook_id, patch)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/webhooks/{webhook_id}")
def delete_webhook(webhook_id: str, store=Depends(get_json_store)):
    try:
        store.delete_webhook(webhook_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=204)


@router.post("/ops/git-sync/events", status_code=201)
def ingest_git_sync_event(payload: GitSyncAuditEventRequest, audit=Depends(get_audit_store)):
    normalized_status = str(payload.status or "").strip().lower()
    if normalized_status not in {"success", "failure", "skipped"}:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "INVALID_GIT_SYNC_STATUS",
                "reason": "status must be one of success|failure|skipped",
            },
        )
    allowed = normalized_status != "failure"
    reason_code = f"GIT_SYNC_{normalized_status.upper()}"
    audit.add(
        event_type="git_sync_status",
        policy_id="git_automation",
        policy_version="v1",
        environment=payload.environment,
        allowed=allowed,
        reason=payload.message or normalized_status,
        reason_code=reason_code,
        endpoint="/api/v1/ops/git-sync/events",
        context={
            "branch": payload.branch,
            "status": normalized_status,
            "source": payload.source,
            **(payload.context or {}),
        },
    )
    return {"accepted": True, "status": normalized_status, "reason_code": reason_code}


@router.get("/ops/git-sync/summary")
def git_sync_summary(
    days: int = Query(7, ge=1, le=31),
    environment: Environment | None = Query(None, description="dev|staging|prod"),
    branch: str | None = Query(None, description="可选分支过滤，如 main"),
    top_branches_limit: int = Query(5, ge=1, le=20),
    granularity: str = Query("day", description="时间粒度: day|hour"),
    since: str | None = Query(None, description="UTC ISO 起始时间，含边界"),
    until: str | None = Query(None, description="UTC ISO 结束时间，含边界"),
    source: str | None = Query(None, description="来源脚本过滤，如 git_auto_sync.ps1"),
    top_n_reasons: int = Query(5, ge=1, le=20, description="失败原因时间序列每个时间桶保留的 topN"),
    include_empty_buckets: bool = Query(True, description="是否包含全 0 时间桶"),
    bucket_label_format: str = Query("raw", description="时间桶标签格式: raw|human"),
    tz: str = Query("UTC", description="human 标签时区，如 UTC/Asia/Shanghai"),
    audit=Depends(get_audit_store),
):
    ndays = max(1, min(int(days), 31))
    all_rows = audit.list(limit=5000, event_type_prefix="git_sync_status", environment=environment)
    norm_branch = str(branch or "").strip()
    norm_source = str(source or "").strip()
    today = datetime.now(timezone.utc).date()
    norm_granularity = str(granularity or "day").strip().lower()
    if norm_granularity not in {"day", "hour"}:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "INVALID_GRANULARITY", "reason": "granularity must be day or hour"},
        )
    norm_bucket_label_format = str(bucket_label_format or "raw").strip().lower()
    if norm_bucket_label_format not in {"raw", "human"}:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "INVALID_BUCKET_LABEL_FORMAT", "reason": "bucket_label_format must be raw or human"},
        )
    normalized_tz = str(tz or "UTC").strip()
    fallback_tz_map = {
        "UTC": timezone.utc,
        "ETC/UTC": timezone.utc,
        "GMT": timezone.utc,
        "ETC/GMT": timezone.utc,
        "ASIA/SHANGHAI": timezone(timedelta(hours=8), name="CST"),
    }
    try:
        target_tz = ZoneInfo(normalized_tz)
    except Exception:
        # Windows + missing tzdata 场景下，兜底接受常见时区别名，避免健康接口因时区库缺失降级失败。
        fallback_tz = fallback_tz_map.get(normalized_tz.upper())
        if fallback_tz is not None:
            target_tz = fallback_tz
        else:
            raise HTTPException(
                status_code=400,
                detail={"error_code": "INVALID_TIMEZONE", "reason": "tz must be a valid IANA timezone"},
            )
    since_dt = _parse_utc_iso(since) if since else None
    until_dt = _parse_utc_iso(until) if until else None
    if (since and since_dt is None) or (until and until_dt is None):
        raise HTTPException(
            status_code=400,
            detail={"error_code": "INVALID_TIME_RANGE", "reason": "since/until must be valid UTC ISO datetime"},
        )
    if since_dt and until_dt and since_dt > until_dt:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "INVALID_TIME_RANGE", "reason": "since must be earlier than or equal to until"},
        )
    day_keys = [(today - timedelta(days=i)).isoformat() for i in range(ndays - 1, -1, -1)]
    hour_count = max(1, min(ndays * 24, 24 * 14))
    now_hour = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    hour_keys = [(now_hour - timedelta(hours=i)).strftime("%Y-%m-%dT%H:00:00+00:00") for i in range(hour_count - 1, -1, -1)]
    bucket_keys = day_keys if norm_granularity == "day" else hour_keys
    by_bucket_map: dict[str, dict[str, int]] = {
        d: {"success": 0, "failure": 0, "skipped": 0, "total": 0} for d in bucket_keys
    }

    totals = {"success": 0, "failure": 0, "skipped": 0, "total": 0}
    branch_totals: dict[str, dict[str, int]] = {}
    source_branch_totals: dict[tuple[str, str], dict[str, int]] = {}
    failure_reason_map: dict[str, int] = {}
    failure_reason_timeline_map: dict[str, dict[str, int]] = {d: {} for d in bucket_keys}
    push_attempt_samples = 0
    push_attempt_sum = 0
    push_attempt_max = 0
    audit_delivery_success_count = 0
    audit_delivery_failed_count = 0
    audit_delivery_invalid_count = 0
    audit_delivery_empty_count = 0
    last_audit_delivery_success_at: datetime | None = None
    last_audit_delivery_failed_at: datetime | None = None
    last_audit_delivery_invalid_at: datetime | None = None
    last_audit_delivery_empty_at: datetime | None = None
    last_audit_delivery_untagged_at: datetime | None = None
    last_success_at: datetime | None = None
    last_failure_at: datetime | None = None
    last_skipped_at: datetime | None = None
    last_event_at: datetime | None = None
    for row in all_rows:
        ts = _parse_utc_iso(row.get("timestamp"))
        if ts is None:
            continue
        if since_dt and ts < since_dt:
            continue
        if until_dt and ts > until_dt:
            continue
        bucket = ts.date().isoformat() if norm_granularity == "day" else ts.replace(minute=0, second=0, microsecond=0).strftime(
            "%Y-%m-%dT%H:00:00+00:00"
        )
        if bucket not in by_bucket_map:
            continue
        context = row.get("context") or {}
        row_branch = str(context.get("branch") or "").strip()
        row_source = str(context.get("source") or "").strip()
        if norm_branch and row_branch != norm_branch:
            continue
        if norm_source and row_source != norm_source:
            continue
        status = str(context.get("status", "")).strip().lower()
        if status not in {"success", "failure", "skipped"}:
            continue
        push_attempts = _extract_push_attempts(context)
        if push_attempts is not None:
            push_attempt_samples += 1
            push_attempt_sum += push_attempts
            if push_attempts > push_attempt_max:
                push_attempt_max = push_attempts
        audit_delivery = str(context.get("audit_delivery", "")).strip().lower()
        if audit_delivery == "success":
            audit_delivery_success_count += 1
            if last_audit_delivery_success_at is None or ts > last_audit_delivery_success_at:
                last_audit_delivery_success_at = ts
        elif audit_delivery == "failed":
            audit_delivery_failed_count += 1
            if last_audit_delivery_failed_at is None or ts > last_audit_delivery_failed_at:
                last_audit_delivery_failed_at = ts
        elif audit_delivery:
            audit_delivery_invalid_count += 1
            if last_audit_delivery_invalid_at is None or ts > last_audit_delivery_invalid_at:
                last_audit_delivery_invalid_at = ts
        else:
            audit_delivery_empty_count += 1
            if last_audit_delivery_empty_at is None or ts > last_audit_delivery_empty_at:
                last_audit_delivery_empty_at = ts
        if last_event_at is None or ts > last_event_at:
            last_event_at = ts
        if status == "success" and (last_success_at is None or ts > last_success_at):
            last_success_at = ts
        if status == "failure" and (last_failure_at is None or ts > last_failure_at):
            last_failure_at = ts
        if status == "skipped" and (last_skipped_at is None or ts > last_skipped_at):
            last_skipped_at = ts
        by_bucket_map[bucket][status] += 1
        by_bucket_map[bucket]["total"] += 1
        totals[status] += 1
        totals["total"] += 1
        if status == "failure":
            reason_code = str(row.get("reason_code") or "UNKNOWN")
            failure_reason_map[reason_code] = failure_reason_map.get(reason_code, 0) + 1
            bucket_reason = failure_reason_timeline_map[bucket]
            bucket_reason[reason_code] = bucket_reason.get(reason_code, 0) + 1
        if row_branch:
            if row_branch not in branch_totals:
                branch_totals[row_branch] = {"success": 0, "failure": 0, "skipped": 0, "total": 0}
            branch_totals[row_branch][status] += 1
            branch_totals[row_branch]["total"] += 1
        if row_source and row_branch:
            key = (row_source, row_branch)
            if key not in source_branch_totals:
                source_branch_totals[key] = {"success": 0, "failure": 0, "skipped": 0, "total": 0}
            source_branch_totals[key][status] += 1
            source_branch_totals[key]["total"] += 1

    filtered_rows: list[tuple[datetime, str]] = []
    for row in all_rows:
        ts = _parse_utc_iso(row.get("timestamp"))
        if ts is None:
            continue
        if since_dt and ts < since_dt:
            continue
        if until_dt and ts > until_dt:
            continue
        context = row.get("context") or {}
        row_branch = str(context.get("branch") or "").strip()
        row_source = str(context.get("source") or "").strip()
        if norm_branch and row_branch != norm_branch:
            continue
        if norm_source and row_source != norm_source:
            continue
        status = str(context.get("status", "")).strip().lower()
        if status not in {"success", "failure", "skipped"}:
            continue
        filtered_rows.append((ts, status))
    filtered_rows.sort(key=lambda x: x[0], reverse=True)

    consecutive_failure_streak = 0
    consecutive_non_success_streak = 0
    for _ts, st in filtered_rows:
        if st == "failure":
            consecutive_failure_streak += 1
        else:
            break
    for _ts, st in filtered_rows:
        if st != "success":
            consecutive_non_success_streak += 1
        else:
            break

    if consecutive_failure_streak >= 3 or consecutive_non_success_streak >= 5:
        sync_health_level = "high_risk"
    elif consecutive_failure_streak >= 1 or consecutive_non_success_streak >= 2:
        sync_health_level = "warning"
    else:
        sync_health_level = "healthy"

    success_rate = round((totals["success"] / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    failure_rate = round((totals["failure"] / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    avg_push_attempts = round(push_attempt_sum / push_attempt_samples, 2) if push_attempt_samples > 0 else 0.0
    audit_delivery_success_rate = (
        round((audit_delivery_success_count / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    )
    audit_delivery_failure_rate = (
        round((audit_delivery_failed_count / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    )
    if audit_delivery_failed_count >= 3 or (totals["total"] > 0 and audit_delivery_success_count == 0):
        audit_delivery_health_level = "high_risk"
    elif audit_delivery_failed_count >= 1:
        audit_delivery_health_level = "warning"
    else:
        audit_delivery_health_level = "healthy"
    audit_delivery_failure_pressure_index = round(
        audit_delivery_failure_rate * (1 + audit_delivery_failed_count), 1
    )
    audit_delivery_net_health_score = round(
        audit_delivery_success_rate - audit_delivery_failure_rate,
        1,
    )
    if audit_delivery_net_health_score <= -20.0:
        audit_delivery_net_health_level = "high_risk"
    elif audit_delivery_net_health_score < 0.0:
        audit_delivery_net_health_level = "warning"
    else:
        audit_delivery_net_health_level = "healthy"
    audit_delivery_success_density_per_day = round(audit_delivery_success_count / ndays, 2)
    audit_delivery_failed_density_per_day = round(audit_delivery_failed_count / ndays, 2)
    audit_delivery_net_density_per_day = round(
        (audit_delivery_success_count - audit_delivery_failed_count) / ndays, 2
    )
    audit_delivery_invalid_density_per_day = round(audit_delivery_invalid_count / ndays, 2)
    audit_delivery_empty_density_per_day = round(audit_delivery_empty_count / ndays, 2)
    audit_delivery_tagged_count = audit_delivery_success_count + audit_delivery_failed_count
    audit_delivery_coverage_rate = (
        round((audit_delivery_tagged_count / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    )
    audit_delivery_untagged_count = max(0, totals["total"] - audit_delivery_tagged_count)
    audit_delivery_untagged_rate = (
        round((audit_delivery_untagged_count / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    )
    audit_delivery_invalid_rate = (
        round((audit_delivery_invalid_count / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    )
    audit_delivery_empty_rate = (
        round((audit_delivery_empty_count / totals["total"]) * 100, 1) if totals["total"] > 0 else 0.0
    )
    audit_delivery_untagged_density_per_day = round(audit_delivery_untagged_count / ndays, 2)
    if last_audit_delivery_invalid_at and last_audit_delivery_empty_at:
        last_audit_delivery_untagged_at = max(last_audit_delivery_invalid_at, last_audit_delivery_empty_at)
    else:
        last_audit_delivery_untagged_at = last_audit_delivery_invalid_at or last_audit_delivery_empty_at
    top_branches = sorted(
        [{"branch": b, **stats} for b, stats in branch_totals.items()],
        key=lambda x: (-x["total"], x["branch"]),
    )[:top_branches_limit]
    top_source_branches = sorted(
        [{"source": s, "branch": b, **stats} for (s, b), stats in source_branch_totals.items()],
        key=lambda x: (-x["total"], x["source"], x["branch"]),
    )[:top_branches_limit]
    failure_reason_distribution = [
        {"reason_code": rc, "count": c}
        for rc, c in sorted(failure_reason_map.items(), key=lambda x: (-x[1], x[0]))
    ]
    failure_reason_timeline = [
        {
            "bucket": d,
            "reasons": [
                {"reason_code": rc, "count": c}
                for rc, c in sorted(failure_reason_timeline_map[d].items(), key=lambda x: (-x[1], x[0]))
            ][:top_n_reasons],
        }
        for d in bucket_keys
    ]
    timeline_rows = [{"bucket": d, **by_bucket_map[d]} for d in bucket_keys]
    bucket_count = len(timeline_rows)
    failure_reason_timeline_rows = failure_reason_timeline
    if not include_empty_buckets:
        timeline_rows = [x for x in timeline_rows if int(x.get("total", 0)) > 0]
        non_empty_buckets = {x["bucket"] for x in timeline_rows}
        failure_reason_timeline_rows = [x for x in failure_reason_timeline if x["bucket"] in non_empty_buckets]
    non_empty_bucket_count = sum(1 for x in timeline_rows if int(x.get("total", 0)) > 0)

    def _bucket_label(raw_bucket: str) -> str:
        if norm_bucket_label_format == "raw":
            return raw_bucket
        if norm_granularity == "day":
            dt = _parse_utc_iso(raw_bucket + "T00:00:00+00:00")
            if not dt:
                return raw_bucket
            return dt.astimezone(target_tz).strftime("%Y-%m-%d")
        # hour 粒度：2026-04-15T09:00:00+00:00 -> 2026-04-15 09:00 UTC
        dt = _parse_utc_iso(raw_bucket)
        if not dt:
            return raw_bucket
        return dt.astimezone(target_tz).strftime("%Y-%m-%d %H:00 %Z")

    timeline_with_label = [{**x, "bucket_label": _bucket_label(str(x["bucket"]))} for x in timeline_rows]
    failure_reason_timeline_with_label = [
        {**x, "bucket_label": _bucket_label(str(x["bucket"]))} for x in failure_reason_timeline_rows
    ]
    silence_threshold_minutes = int(ndays * 24 * 60)
    minutes_since_last_event = _minutes_since(last_event_at, now_hour)
    sync_silence_warning = bool(minutes_since_last_event is None or minutes_since_last_event > float(silence_threshold_minutes))
    sync_silence_overdue_minutes = (
        round(max(0.0, float(minutes_since_last_event) - float(silence_threshold_minutes)), 1)
        if minutes_since_last_event is not None
        else None
    )
    sync_silence_overdue_rate = (
        round((float(sync_silence_overdue_minutes) / float(silence_threshold_minutes)) * 100.0, 1)
        if sync_silence_overdue_minutes is not None and silence_threshold_minutes > 0
        else None
    )
    sync_silence_headroom_minutes = (
        round(max(0.0, float(silence_threshold_minutes) - float(minutes_since_last_event)), 1)
        if minutes_since_last_event is not None
        else None
    )
    if minutes_since_last_event is None:
        sync_silence_state = "missing"
        sync_silence_state_rank = 2
        sync_silence_event_present = False
        sync_silence_state_label = "无事件"
        sync_silence_state_code = "MISSING"
    elif sync_silence_warning:
        sync_silence_state = "overdue"
        sync_silence_state_rank = 1
        sync_silence_event_present = True
        sync_silence_state_label = "已超阈值"
        sync_silence_state_code = "OVERDUE"
    else:
        sync_silence_state = "within"
        sync_silence_state_rank = 0
        sync_silence_event_present = True
        sync_silence_state_label = "阈值内"
        sync_silence_state_code = "WITHIN"
    sync_silence_severity_score = sync_silence_overdue_rate
    if sync_silence_severity_score is None:
        sync_silence_severity_level = "missing"
    elif sync_silence_severity_score >= 100.0:
        sync_silence_severity_level = "high"
    elif sync_silence_severity_score > 0.0:
        sync_silence_severity_level = "medium"
    else:
        sync_silence_severity_level = "low"

    return {
        "days": ndays,
        "environment": environment,
        "branch": branch,
        "source": source,
        "granularity": norm_granularity,
        "include_empty_buckets": include_empty_buckets,
        "bucket_label_format": norm_bucket_label_format,
        "tz": normalized_tz,
        "since": since_dt.isoformat() if since_dt else None,
        "until": until_dt.isoformat() if until_dt else None,
        "totals": totals,
        "success_rate": success_rate,
        "failure_rate": failure_rate,
        "last_success_at": last_success_at.isoformat() if last_success_at else None,
        "last_failure_at": last_failure_at.isoformat() if last_failure_at else None,
        "last_skipped_at": last_skipped_at.isoformat() if last_skipped_at else None,
        "last_event_at": last_event_at.isoformat() if last_event_at else None,
        "minutes_since_last_success": _minutes_since(last_success_at, now_hour),
        "minutes_since_last_failure": _minutes_since(last_failure_at, now_hour),
        "minutes_since_last_skipped": _minutes_since(last_skipped_at, now_hour),
        "minutes_since_last_event": minutes_since_last_event,
        "sync_silence_threshold_minutes": silence_threshold_minutes,
        "sync_silence_warning": sync_silence_warning,
        "sync_silence_overdue_minutes": sync_silence_overdue_minutes,
        "sync_silence_overdue_rate": sync_silence_overdue_rate,
        "sync_silence_headroom_minutes": sync_silence_headroom_minutes,
        "sync_silence_state": sync_silence_state,
        "sync_silence_state_rank": sync_silence_state_rank,
        "sync_silence_event_present": sync_silence_event_present,
        "sync_silence_state_label": sync_silence_state_label,
        "sync_silence_state_code": sync_silence_state_code,
        "sync_silence_severity_score": sync_silence_severity_score,
        "sync_silence_severity_level": sync_silence_severity_level,
        "consecutive_failure_streak": consecutive_failure_streak,
        "consecutive_non_success_streak": consecutive_non_success_streak,
        "sync_health_level": sync_health_level,
        "sync_health_warning": sync_health_level != "healthy",
        "bucket_count": bucket_count,
        "non_empty_bucket_count": non_empty_bucket_count,
        "top_branches": top_branches,
        "top_source_branches": top_source_branches,
        "failure_reason_distribution": failure_reason_distribution,
        "failure_reason_timeline": failure_reason_timeline_with_label,
        "avg_push_attempts": avg_push_attempts,
        "max_push_attempts": push_attempt_max,
        "push_attempt_sample_count": push_attempt_samples,
        "audit_delivery_success_count": audit_delivery_success_count,
        "audit_delivery_failed_count": audit_delivery_failed_count,
        "audit_delivery_success_rate": audit_delivery_success_rate,
        "audit_delivery_failure_rate": audit_delivery_failure_rate,
        "audit_delivery_health_level": audit_delivery_health_level,
        "audit_delivery_health_warning": audit_delivery_health_level != "healthy",
        "audit_delivery_failure_pressure_index": audit_delivery_failure_pressure_index,
        "audit_delivery_net_health_score": audit_delivery_net_health_score,
        "audit_delivery_net_health_level": audit_delivery_net_health_level,
        "audit_delivery_net_health_warning": audit_delivery_net_health_level != "healthy",
        "audit_delivery_success_density_per_day": audit_delivery_success_density_per_day,
        "audit_delivery_failed_density_per_day": audit_delivery_failed_density_per_day,
        "audit_delivery_net_density_per_day": audit_delivery_net_density_per_day,
        "audit_delivery_invalid_density_per_day": audit_delivery_invalid_density_per_day,
        "audit_delivery_empty_density_per_day": audit_delivery_empty_density_per_day,
        "audit_delivery_tagged_count": audit_delivery_tagged_count,
        "audit_delivery_coverage_rate": audit_delivery_coverage_rate,
        "audit_delivery_untagged_count": audit_delivery_untagged_count,
        "audit_delivery_untagged_rate": audit_delivery_untagged_rate,
        "audit_delivery_untagged_density_per_day": audit_delivery_untagged_density_per_day,
        "audit_delivery_invalid_count": audit_delivery_invalid_count,
        "audit_delivery_invalid_rate": audit_delivery_invalid_rate,
        "last_audit_delivery_invalid_at": (
            last_audit_delivery_invalid_at.isoformat() if last_audit_delivery_invalid_at else None
        ),
        "minutes_since_last_audit_delivery_invalid": _minutes_since(last_audit_delivery_invalid_at, now_hour),
        "audit_delivery_empty_count": audit_delivery_empty_count,
        "audit_delivery_empty_rate": audit_delivery_empty_rate,
        "last_audit_delivery_empty_at": (
            last_audit_delivery_empty_at.isoformat() if last_audit_delivery_empty_at else None
        ),
        "minutes_since_last_audit_delivery_empty": _minutes_since(last_audit_delivery_empty_at, now_hour),
        "last_audit_delivery_untagged_at": (
            last_audit_delivery_untagged_at.isoformat() if last_audit_delivery_untagged_at else None
        ),
        "minutes_since_last_audit_delivery_untagged": _minutes_since(last_audit_delivery_untagged_at, now_hour),
        "last_audit_delivery_success_at": (
            last_audit_delivery_success_at.isoformat() if last_audit_delivery_success_at else None
        ),
        "last_audit_delivery_failed_at": (
            last_audit_delivery_failed_at.isoformat() if last_audit_delivery_failed_at else None
        ),
        "minutes_since_last_audit_delivery_success": _minutes_since(last_audit_delivery_success_at, now_hour),
        "minutes_since_last_audit_delivery_failed": _minutes_since(last_audit_delivery_failed_at, now_hour),
        "timeline": timeline_with_label,
    }


@router.get("/analytics/reports")
def analytics_reports(
    report_type: str = Query("project_execution", description="报告类型: project_execution|ops_risk"),
    days: int = Query(7, ge=1, le=31),
    environment: Environment | None = Query(None, description="dev|staging|prod"),
    include_project_ids: bool = Query(True, description="是否返回项目ID列表"),
    store=Depends(get_json_store),
    audit=Depends(get_audit_store),
):
    norm_type = str(report_type or "").strip().lower()
    if norm_type not in {"project_execution", "ops_risk"}:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "INVALID_REPORT_TYPE",
                "reason": "report_type must be one of project_execution|ops_risk",
            },
        )

    projects = store.list_projects()
    if environment:
        projects = [p for p in projects if str(p.get("environment", "")) == str(environment)]

    if norm_type == "project_execution":
        rows: list[dict[str, Any]] = []
        risk_dist = {"low": 0, "medium": 0, "high": 0}
        for p in projects:
            pid = str(p.get("id", ""))
            tasks, _ = store.list_tasks(project_id=pid, limit=500, offset=0)
            overall, _meta = weighted_progress_percent(tasks)
            risk = project_risk_summary(tasks)
            level = str(risk.get("risk_level", "low"))
            if level not in risk_dist:
                level = "low"
            risk_dist[level] += 1
            rows.append(
                {
                    "project_id": pid,
                    "project_name": p.get("name"),
                    "environment": p.get("environment"),
                    "project_status": p.get("status"),
                    "task_count": len(tasks),
                    "overall_progress": round(overall, 2),
                    "risk_score": int(risk.get("risk_score", 0) or 0),
                    "risk_level": level,
                }
            )
        rows_sorted = sorted(rows, key=lambda x: (-int(x["risk_score"]), x["project_id"]))
        avg_progress = round(
            sum(float(x["overall_progress"]) for x in rows_sorted) / len(rows_sorted),
            2,
        ) if rows_sorted else 0.0
        at_risk = [x for x in rows_sorted if str(x["risk_level"]) in {"medium", "high"}]
        response: dict[str, Any] = {
            "report_type": norm_type,
            "days": days,
            "environment": environment,
            "project_count": len(rows_sorted),
            "average_progress": avg_progress,
            "risk_distribution": risk_dist,
            "at_risk_project_count": len(at_risk),
        }
        if include_project_ids:
            response["at_risk_project_ids"] = [x["project_id"] for x in at_risk]
        response["top_risk_projects"] = at_risk[:10]
        return response

    # ops_risk: 汇总近 N 天风险审计与 Git 同步失败信号
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=max(1, int(days)))
    risk_events = audit.list(limit=5000, event_type_prefix="project_risk_alert", environment=environment)
    git_events = audit.list(limit=5000, event_type_prefix="git_sync_status", environment=environment)

    def _within_days(e: dict[str, Any]) -> bool:
        ts = _parse_utc_iso(e.get("timestamp"))
        return bool(ts and ts >= since)

    risk_events = [e for e in risk_events if _within_days(e)]
    git_events = [e for e in git_events if _within_days(e)]
    git_success = sum(1 for e in git_events if str((e.get("context") or {}).get("status", "")).lower() == "success")
    git_failure = sum(1 for e in git_events if str((e.get("context") or {}).get("status", "")).lower() == "failure")
    git_skipped = sum(1 for e in git_events if str((e.get("context") or {}).get("status", "")).lower() == "skipped")
    git_audit_delivery_failed = 0
    git_audit_delivery_success = 0
    for e in git_events:
        context = e.get("context") or {}
        audit_delivery = str(context.get("audit_delivery", "")).strip().lower()
        if audit_delivery == "failed":
            git_audit_delivery_failed += 1
        elif audit_delivery == "success":
            git_audit_delivery_success += 1
    git_audit_delivery_invalid = 0
    git_audit_delivery_empty = 0
    last_git_sync_audit_delivery_invalid_at = None
    last_git_sync_audit_delivery_empty_at = None
    last_git_sync_audit_delivery_untagged_at = None
    for e in git_events:
        context = e.get("context") or {}
        st = str(context.get("status", "")).strip().lower()
        if st not in {"success", "failure", "skipped"}:
            continue
        audit_delivery = str(context.get("audit_delivery", "")).strip().lower()
        if audit_delivery and audit_delivery not in {"success", "failed"}:
            git_audit_delivery_invalid += 1
            ts = _parse_utc_iso(e.get("timestamp"))
            if ts and (
                last_git_sync_audit_delivery_invalid_at is None
                or ts > last_git_sync_audit_delivery_invalid_at
            ):
                last_git_sync_audit_delivery_invalid_at = ts
        elif not audit_delivery:
            git_audit_delivery_empty += 1
            ts = _parse_utc_iso(e.get("timestamp"))
            if ts and (
                last_git_sync_audit_delivery_empty_at is None
                or ts > last_git_sync_audit_delivery_empty_at
            ):
                last_git_sync_audit_delivery_empty_at = ts
    failure_reason_counter: dict[str, int] = {}
    for e in git_events:
        if str((e.get("context") or {}).get("status", "")).lower() != "failure":
            continue
        rc = str(e.get("reason_code") or "UNKNOWN")
        failure_reason_counter[rc] = failure_reason_counter.get(rc, 0) + 1
    git_total = len(git_events)
    push_attempt_sample_count = 0
    push_attempt_sum = 0
    push_attempt_max = 0
    for e in git_events:
        context = e.get("context") or {}
        push_attempts = _extract_push_attempts(context)
        if push_attempts is None:
            continue
        push_attempt_sample_count += 1
        push_attempt_sum += push_attempts
        if push_attempts > push_attempt_max:
            push_attempt_max = push_attempts
    git_sync_avg_push_attempts = round(push_attempt_sum / push_attempt_sample_count, 2) if push_attempt_sample_count > 0 else 0.0
    last_git_sync_audit_delivery_success_at = None
    last_git_sync_audit_delivery_failed_at = None
    for e in git_events:
        ts = _parse_utc_iso(e.get("timestamp"))
        if ts is None:
            continue
        context = e.get("context") or {}
        audit_delivery = str(context.get("audit_delivery", "")).strip().lower()
        if audit_delivery == "success":
            if last_git_sync_audit_delivery_success_at is None or ts > last_git_sync_audit_delivery_success_at:
                last_git_sync_audit_delivery_success_at = ts
        elif audit_delivery == "failed":
            if last_git_sync_audit_delivery_failed_at is None or ts > last_git_sync_audit_delivery_failed_at:
                last_git_sync_audit_delivery_failed_at = ts
    git_success_rate = round((git_success / git_total) * 100, 1) if git_total > 0 else 0.0
    git_failure_rate = round((git_failure / git_total) * 100, 1) if git_total > 0 else 0.0
    git_skipped_rate = round((git_skipped / git_total) * 100, 1) if git_total > 0 else 0.0
    git_audit_delivery_failure_rate = round((git_audit_delivery_failed / git_total) * 100, 1) if git_total > 0 else 0.0
    git_audit_delivery_success_rate = round((git_audit_delivery_success / git_total) * 100, 1) if git_total > 0 else 0.0
    if git_audit_delivery_failed >= 3 or (git_total > 0 and git_audit_delivery_success == 0):
        git_sync_audit_delivery_health_level = "high_risk"
    elif git_audit_delivery_failed >= 1:
        git_sync_audit_delivery_health_level = "warning"
    else:
        git_sync_audit_delivery_health_level = "healthy"
    git_sync_audit_delivery_failure_pressure_index = round(
        git_audit_delivery_failure_rate * (1 + git_audit_delivery_failed), 1
    )
    git_sync_audit_delivery_net_health_score = round(
        git_audit_delivery_success_rate - git_audit_delivery_failure_rate,
        1,
    )
    if git_sync_audit_delivery_net_health_score <= -20.0:
        git_sync_audit_delivery_net_health_level = "high_risk"
    elif git_sync_audit_delivery_net_health_score < 0.0:
        git_sync_audit_delivery_net_health_level = "warning"
    else:
        git_sync_audit_delivery_net_health_level = "healthy"
    git_sync_audit_delivery_success_density_per_day = round(
        git_audit_delivery_success / max(1, int(days)), 2
    )
    git_sync_audit_delivery_failed_density_per_day = round(
        git_audit_delivery_failed / max(1, int(days)), 2
    )
    git_sync_audit_delivery_net_density_per_day = round(
        (git_audit_delivery_success - git_audit_delivery_failed) / max(1, int(days)), 2
    )
    git_sync_audit_delivery_invalid_density_per_day = round(
        git_audit_delivery_invalid / max(1, int(days)), 2
    )
    git_sync_audit_delivery_empty_density_per_day = round(
        git_audit_delivery_empty / max(1, int(days)), 2
    )
    git_sync_audit_delivery_tagged_count = git_audit_delivery_success + git_audit_delivery_failed
    git_sync_audit_delivery_coverage_rate = (
        round((git_sync_audit_delivery_tagged_count / git_total) * 100, 1) if git_total > 0 else 0.0
    )
    git_sync_audit_delivery_untagged_count = max(0, git_total - git_sync_audit_delivery_tagged_count)
    git_sync_audit_delivery_untagged_rate = (
        round((git_sync_audit_delivery_untagged_count / git_total) * 100, 1) if git_total > 0 else 0.0
    )
    git_sync_audit_delivery_invalid_rate = (
        round((git_audit_delivery_invalid / git_total) * 100, 1) if git_total > 0 else 0.0
    )
    git_sync_audit_delivery_empty_rate = (
        round((git_audit_delivery_empty / git_total) * 100, 1) if git_total > 0 else 0.0
    )
    git_sync_audit_delivery_untagged_density_per_day = round(
        git_sync_audit_delivery_untagged_count / max(1, int(days)), 2
    )
    if last_git_sync_audit_delivery_invalid_at and last_git_sync_audit_delivery_empty_at:
        last_git_sync_audit_delivery_untagged_at = max(
            last_git_sync_audit_delivery_invalid_at, last_git_sync_audit_delivery_empty_at
        )
    else:
        last_git_sync_audit_delivery_untagged_at = (
            last_git_sync_audit_delivery_invalid_at or last_git_sync_audit_delivery_empty_at
        )
    git_net_success_rate = round(((git_success - git_failure) / git_total) * 100, 1) if git_total > 0 else 0.0
    git_event_density_per_day = round(git_total / max(1, int(days)), 2)
    git_success_density_per_day = round(git_success / max(1, int(days)), 2)
    git_failure_density_per_day = round(git_failure / max(1, int(days)), 2)
    git_skipped_density_per_day = round(git_skipped / max(1, int(days)), 2)
    git_net_success_density_per_day = round((git_success - git_failure) / max(1, int(days)), 2)
    git_rows: list[tuple[datetime, str]] = []
    for e in git_events:
        ts = _parse_utc_iso(e.get("timestamp"))
        if ts is None:
            continue
        st = str((e.get("context") or {}).get("status", "")).lower()
        if st in {"success", "failure", "skipped"}:
            git_rows.append((ts, st))
    git_rows.sort(key=lambda x: x[0], reverse=True)
    last_git_sync_event_at = git_rows[0][0] if git_rows else None
    last_git_sync_success_at = next((ts for ts, st in git_rows if st == "success"), None)
    last_git_sync_failure_at = next((ts for ts, st in git_rows if st == "failure"), None)
    consecutive_failure_streak = 0
    consecutive_non_success_streak = 0
    for _ts, st in git_rows:
        if st == "failure":
            consecutive_failure_streak += 1
        else:
            break
    for _ts, st in git_rows:
        if st != "success":
            consecutive_non_success_streak += 1
        else:
            break
    git_sync_failure_pressure_index = round(git_failure_rate * (1 + consecutive_failure_streak), 1)
    if consecutive_failure_streak >= 3 or consecutive_non_success_streak >= 5:
        git_sync_health_level = "high_risk"
    elif consecutive_failure_streak >= 1 or consecutive_non_success_streak >= 2:
        git_sync_health_level = "warning"
    else:
        git_sync_health_level = "healthy"
    top_failure_reason_code = None
    top_failure_reason_count = 0
    top_failure_reason_rate = 0.0
    if failure_reason_counter:
        top_failure_reason_code, top_failure_reason_count = sorted(
            failure_reason_counter.items(), key=lambda x: (-x[1], x[0])
        )[0]
        if git_failure > 0:
            top_failure_reason_rate = round((top_failure_reason_count / git_failure) * 100, 1)
    silence_threshold_minutes = int(max(1, int(days)) * 24 * 60)
    minutes_since_last_git_sync_event = _minutes_since(last_git_sync_event_at, now)
    git_sync_event_silence_warning = bool(
        minutes_since_last_git_sync_event is None or minutes_since_last_git_sync_event > float(silence_threshold_minutes)
    )
    git_sync_event_silence_overdue_minutes = (
        round(max(0.0, float(minutes_since_last_git_sync_event) - float(silence_threshold_minutes)), 1)
        if minutes_since_last_git_sync_event is not None
        else None
    )
    git_sync_event_silence_overdue_rate = (
        round((float(git_sync_event_silence_overdue_minutes) / float(silence_threshold_minutes)) * 100.0, 1)
        if git_sync_event_silence_overdue_minutes is not None and silence_threshold_minutes > 0
        else None
    )
    git_sync_event_silence_headroom_minutes = (
        round(max(0.0, float(silence_threshold_minutes) - float(minutes_since_last_git_sync_event)), 1)
        if minutes_since_last_git_sync_event is not None
        else None
    )
    if minutes_since_last_git_sync_event is None:
        git_sync_event_silence_state = "missing"
        git_sync_event_silence_state_rank = 2
        git_sync_event_silence_event_present = False
        git_sync_event_silence_state_label = "无事件"
        git_sync_event_silence_state_code = "MISSING"
    elif git_sync_event_silence_warning:
        git_sync_event_silence_state = "overdue"
        git_sync_event_silence_state_rank = 1
        git_sync_event_silence_event_present = True
        git_sync_event_silence_state_label = "已超阈值"
        git_sync_event_silence_state_code = "OVERDUE"
    else:
        git_sync_event_silence_state = "within"
        git_sync_event_silence_state_rank = 0
        git_sync_event_silence_event_present = True
        git_sync_event_silence_state_label = "阈值内"
        git_sync_event_silence_state_code = "WITHIN"
    git_sync_event_silence_severity_score = git_sync_event_silence_overdue_rate
    if git_sync_event_silence_severity_score is None:
        git_sync_event_silence_severity_level = "missing"
    elif git_sync_event_silence_severity_score >= 100.0:
        git_sync_event_silence_severity_level = "high"
    elif git_sync_event_silence_severity_score > 0.0:
        git_sync_event_silence_severity_level = "medium"
    else:
        git_sync_event_silence_severity_level = "low"
    return {
        "report_type": norm_type,
        "days": days,
        "environment": environment,
        "project_risk_alert_event_count": len(risk_events),
        "git_sync_event_count": len(git_events),
        "git_sync_success_count": git_success,
        "git_sync_failure_count": git_failure,
        "git_sync_skipped_count": git_skipped,
        "git_sync_success_rate": git_success_rate,
        "git_sync_failure_rate": git_failure_rate,
        "git_sync_skipped_rate": git_skipped_rate,
        "git_sync_audit_delivery_failed_count": git_audit_delivery_failed,
        "git_sync_audit_delivery_success_count": git_audit_delivery_success,
        "git_sync_audit_delivery_failure_rate": git_audit_delivery_failure_rate,
        "git_sync_audit_delivery_success_rate": git_audit_delivery_success_rate,
        "git_sync_audit_delivery_health_level": git_sync_audit_delivery_health_level,
        "git_sync_audit_delivery_health_warning": git_sync_audit_delivery_health_level != "healthy",
        "git_sync_audit_delivery_failure_pressure_index": git_sync_audit_delivery_failure_pressure_index,
        "git_sync_audit_delivery_net_health_score": git_sync_audit_delivery_net_health_score,
        "git_sync_audit_delivery_net_health_level": git_sync_audit_delivery_net_health_level,
        "git_sync_audit_delivery_net_health_warning": git_sync_audit_delivery_net_health_level != "healthy",
        "git_sync_audit_delivery_success_density_per_day": git_sync_audit_delivery_success_density_per_day,
        "git_sync_audit_delivery_failed_density_per_day": git_sync_audit_delivery_failed_density_per_day,
        "git_sync_audit_delivery_net_density_per_day": git_sync_audit_delivery_net_density_per_day,
        "git_sync_audit_delivery_invalid_density_per_day": git_sync_audit_delivery_invalid_density_per_day,
        "git_sync_audit_delivery_empty_density_per_day": git_sync_audit_delivery_empty_density_per_day,
        "git_sync_audit_delivery_tagged_count": git_sync_audit_delivery_tagged_count,
        "git_sync_audit_delivery_coverage_rate": git_sync_audit_delivery_coverage_rate,
        "git_sync_audit_delivery_untagged_count": git_sync_audit_delivery_untagged_count,
        "git_sync_audit_delivery_untagged_rate": git_sync_audit_delivery_untagged_rate,
        "git_sync_audit_delivery_untagged_density_per_day": git_sync_audit_delivery_untagged_density_per_day,
        "git_sync_audit_delivery_invalid_count": git_audit_delivery_invalid,
        "git_sync_audit_delivery_invalid_rate": git_sync_audit_delivery_invalid_rate,
        "last_git_sync_audit_delivery_invalid_at": (
            last_git_sync_audit_delivery_invalid_at.isoformat()
            if last_git_sync_audit_delivery_invalid_at
            else None
        ),
        "minutes_since_last_git_sync_audit_delivery_invalid": _minutes_since(
            last_git_sync_audit_delivery_invalid_at, now
        ),
        "git_sync_audit_delivery_empty_count": git_audit_delivery_empty,
        "git_sync_audit_delivery_empty_rate": git_sync_audit_delivery_empty_rate,
        "last_git_sync_audit_delivery_empty_at": (
            last_git_sync_audit_delivery_empty_at.isoformat()
            if last_git_sync_audit_delivery_empty_at
            else None
        ),
        "minutes_since_last_git_sync_audit_delivery_empty": _minutes_since(
            last_git_sync_audit_delivery_empty_at, now
        ),
        "last_git_sync_audit_delivery_untagged_at": (
            last_git_sync_audit_delivery_untagged_at.isoformat()
            if last_git_sync_audit_delivery_untagged_at
            else None
        ),
        "minutes_since_last_git_sync_audit_delivery_untagged": _minutes_since(
            last_git_sync_audit_delivery_untagged_at, now
        ),
        "git_sync_net_success_rate": git_net_success_rate,
        "git_sync_failure_pressure_index": git_sync_failure_pressure_index,
        "git_sync_event_density_per_day": git_event_density_per_day,
        "git_sync_success_density_per_day": git_success_density_per_day,
        "git_sync_failure_density_per_day": git_failure_density_per_day,
        "git_sync_skipped_density_per_day": git_skipped_density_per_day,
        "git_sync_net_success_density_per_day": git_net_success_density_per_day,
        "git_sync_top_failure_reason_code": top_failure_reason_code,
        "git_sync_top_failure_reason_count": top_failure_reason_count,
        "git_sync_top_failure_reason_rate": top_failure_reason_rate,
        "git_sync_avg_push_attempts": git_sync_avg_push_attempts,
        "git_sync_max_push_attempts": push_attempt_max,
        "git_sync_push_attempt_sample_count": push_attempt_sample_count,
        "last_git_sync_audit_delivery_success_at": (
            last_git_sync_audit_delivery_success_at.isoformat() if last_git_sync_audit_delivery_success_at else None
        ),
        "minutes_since_last_git_sync_audit_delivery_success": _minutes_since(last_git_sync_audit_delivery_success_at, now),
        "last_git_sync_audit_delivery_failed_at": (
            last_git_sync_audit_delivery_failed_at.isoformat() if last_git_sync_audit_delivery_failed_at else None
        ),
        "minutes_since_last_git_sync_audit_delivery_failed": _minutes_since(last_git_sync_audit_delivery_failed_at, now),
        "git_sync_consecutive_failure_streak": consecutive_failure_streak,
        "git_sync_consecutive_non_success_streak": consecutive_non_success_streak,
        "git_sync_health_level": git_sync_health_level,
        "git_sync_health_warning": git_sync_health_level != "healthy",
        "last_git_sync_event_at": last_git_sync_event_at.isoformat() if last_git_sync_event_at else None,
        "minutes_since_last_git_sync_event": minutes_since_last_git_sync_event,
        "git_sync_event_silence_threshold_minutes": silence_threshold_minutes,
        "git_sync_event_silence_warning": git_sync_event_silence_warning,
        "git_sync_event_silence_overdue_minutes": git_sync_event_silence_overdue_minutes,
        "git_sync_event_silence_overdue_rate": git_sync_event_silence_overdue_rate,
        "git_sync_event_silence_headroom_minutes": git_sync_event_silence_headroom_minutes,
        "git_sync_event_silence_state": git_sync_event_silence_state,
        "git_sync_event_silence_state_rank": git_sync_event_silence_state_rank,
        "git_sync_event_silence_event_present": git_sync_event_silence_event_present,
        "git_sync_event_silence_state_label": git_sync_event_silence_state_label,
        "git_sync_event_silence_state_code": git_sync_event_silence_state_code,
        "git_sync_event_silence_severity_score": git_sync_event_silence_severity_score,
        "git_sync_event_silence_severity_level": git_sync_event_silence_severity_level,
        "last_git_sync_success_at": last_git_sync_success_at.isoformat() if last_git_sync_success_at else None,
        "minutes_since_last_git_sync_success": _minutes_since(last_git_sync_success_at, now),
        "last_git_sync_failure_at": last_git_sync_failure_at.isoformat() if last_git_sync_failure_at else None,
        "minutes_since_last_git_sync_failure": _minutes_since(last_git_sync_failure_at, now),
        "ops_risk_level": "high" if (git_failure >= 3 or len(risk_events) >= 5) else ("medium" if (git_failure >= 1 or len(risk_events) >= 2) else "low"),
    }


@router.get("/audit/summary")
def audit_summary(
    days: int = Query(7, ge=1, le=31),
    top_limit: int = Query(5, ge=1, le=20),
    event_type_prefix: str | None = Query(None),
    policy_id: str | None = Query(None),
    environment: Environment | None = Query(None),
    reason_code_prefix: str | None = Query(None),
    audit=Depends(get_audit_store),
):
    return audit.summary(
        days=days,
        top_limit=top_limit,
        event_type_prefix=event_type_prefix,
        policy_id=policy_id,
        environment=environment,
        reason_code_prefix=reason_code_prefix,
    )


@router.post("/contents/publish")
def publish_content(
    payload: HighRiskPublishRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
):
    degraded = request.app.state.runtime_mode == "degraded"

    require_policy_sequence(
        engine=engine,
        audit=audit,
        request=request,
        environment=payload.environment,
        gates=[
            (
                "CEO-POLICY-13",
                {"law": payload.law, "high_risk_action": True},
                "publish_gate_p13",
            ),
            (
                "CEO-POLICY-14",
                {
                    "law": payload.law,
                    "degraded_mode": degraded,
                    "high_risk_action": True,
                },
                "publish_gate_p14",
            ),
        ],
    )

    if payload.environment in {"staging", "prod"} and not payload.approved:
        error_code = "STAGING_APPROVAL_REQUIRED" if payload.environment == "staging" else "PROD_APPROVAL_REQUIRED"
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": error_code,
                "reason": f"{payload.environment} publish requires approval",
                "policy": "approval",
            },
        )

    return {"status": "published", "title": payload.title, "environment": payload.environment}
