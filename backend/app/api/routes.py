from __future__ import annotations

import asyncio
import json
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
    acceptance_contract: str = Field("", description="委托/验收约定引用（CEO-POLICY-12）")
    staging_precheck: StagingPrecheck | None = None


class UpdateProjectRequest(BaseModel):
    name: str | None = None
    domain: DomainCode | None = None
    project_type: ProjectType | None = None
    environment: Environment | None = None
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


class ProjectDiscussionPost(BaseModel):
    body: str = Field(..., min_length=1, max_length=8000)
    author: str = Field("anonymous", max_length=80)


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
    limit: int = 50,
    offset: int = 0,
):
    items, total = store.list_agents(level=level, status=status, q=q, limit=limit, offset=offset)
    return {
        "items": [AgentOut.from_record(a).model_dump(mode="json", by_alias=True) for a in items],
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
    return AgentOut.from_record(raw).model_dump(mode="json", by_alias=True)


@router.get("/projects")
def projects(store=Depends(get_json_store)):
    return store.list_projects()


@router.get("/projects/pending-approvals")
def list_pending_approvals(store=Depends(get_json_store)):
    return {"items": store.list_projects_pending_approval()}


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


@router.get("/projects/{project_id}/progress")
def project_progress(project_id: str, store=Depends(get_json_store)):
    try:
        proj = store.get_project(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    tasks, _total = store.list_tasks(project_id=project_id, limit=500, offset=0)
    overall, calc_meta = weighted_progress_percent(tasks)
    risk = project_risk_summary(tasks)
    completed = sum(1 for t in tasks if str(t.get("status")) == "completed")
    return {
        "project_id": project_id,
        "project_status": proj.get("status"),
        "overall_progress": round(overall, 2),
        "calculation": calc_meta,
        "risk_summary": risk,
        "task_count": len(tasks),
        "completed_task_count": completed,
        "milestones": proj.get("milestones") or [],
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
