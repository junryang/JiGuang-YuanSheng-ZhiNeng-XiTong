from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.deps import get_audit_store, get_json_store, get_policy_engine
from app.core.policy_engine import PolicyEngine
from app.core.store import JsonStore
from app.models.project_stage import (
    Deliverable,
    ProjectStage,
    StageApproveRequest,
    StageCompleteRequest,
    StageDeliverableUploadResponse,
    StageStartResponse,
)
from app.services.project_stage_engine import ProjectStageEngine


router = APIRouter(tags=["project_stages"])

_STAGE_AUDIT_POLICY_ID = "project_stage_flow"
_STAGE_AUDIT_POLICY_VERSION = "v1"


def _engine(store: JsonStore) -> ProjectStageEngine:
    return ProjectStageEngine(store=store)


def _parse_dt(value: object) -> datetime | None:
    if value is None:
        return None
    s = str(value).strip()
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _minutes_between(start: datetime | None, end: datetime | None) -> float | None:
    if not start or not end:
        return None
    try:
        return round((end - start).total_seconds() / 60.0, 1)
    except Exception:
        return None


def _pick_current_stage(stages: list[dict]) -> dict | None:
    if not stages:
        return None
    for status in ("in_progress", "review", "pending", "completed"):
        hit = next((s for s in stages if str(s.get("status") or "") == status), None)
        if hit:
            return hit
    return stages[0]

def _should_emit_timeout_alert(
    *,
    store: JsonStore,
    project_id: str,
    marker: str,
    cooldown_minutes: int,
) -> bool:
    try:
        items, _total = store.list_project_discussions(project_id, limit=50, offset=0)
    except Exception:
        return True
    window_end = datetime.now(timezone.utc)
    window_start = window_end - timedelta(minutes=max(0, int(cooldown_minutes)))
    for item in items:
        if marker not in str(item.get("body", "")):
            continue
        created_at = _parse_dt(item.get("created_at"))
        if created_at and created_at >= window_start:
            return False
    return True


def _stage_timeout_alert_cooldown_minutes(engine: PolicyEngine, environment: str) -> int:
    block = engine.get_environment_policy(environment) if environment else {}
    raw = block.get("stage_timeout_alert_cooldown_minutes")
    if raw is None:
        raw = block.get("risk_alert_cooldown_minutes", 30)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = 30
    return max(0, value)


def _stage_timeout_alert_enabled(engine: PolicyEngine, environment: str) -> bool:
    block = engine.get_environment_policy(environment) if environment else {}
    raw = block.get("stage_timeout_alert_enabled", True)
    if isinstance(raw, bool):
        return raw
    text = str(raw).strip().lower()
    if text in {"0", "false", "no", "off"}:
        return False
    return True


def _stage_timeout_alert_allow_force(engine: PolicyEngine, environment: str) -> bool:
    block = engine.get_environment_policy(environment) if environment else {}
    raw = block.get("stage_timeout_alert_allow_force", environment == "dev")
    if isinstance(raw, bool):
        return raw
    text = str(raw).strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    return environment == "dev"


def _stage_timeout_alert_overdue_threshold_minutes(engine: PolicyEngine, environment: str, *, kind: str) -> int:
    """
    kind: "stage" | "approval"
    """
    block = engine.get_environment_policy(environment) if environment else {}
    key = (
        "stage_timeout_alert_stage_overdue_threshold_minutes"
        if kind == "stage"
        else "stage_timeout_alert_approval_overdue_threshold_minutes"
    )
    raw = block.get(key, 0)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        value = 0
    return max(0, value)



def _project_env_or_default(store: JsonStore, project_id: str) -> str:
    try:
        proj = store.get_project(project_id)
        return str(proj.get("environment") or "dev")
    except Exception:
        return "dev"


def _audit_stage(
    *,
    audit,
    request: Request,
    environment: str,
    event_type: str,
    allowed: bool,
    reason: str,
    reason_code: str,
    context: dict,
) -> None:
    try:
        audit.add(
            event_type=event_type,
            policy_id=_STAGE_AUDIT_POLICY_ID,
            policy_version=_STAGE_AUDIT_POLICY_VERSION,
            environment=environment,
            allowed=allowed,
            reason=reason,
            reason_code=reason_code,
            endpoint=str(request.url.path),
            context=context,
        )
    except Exception:
        # 审计写入失败不阻断主流程
        return


@router.get("/projects/{project_id}/stages")
def list_project_stages(project_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        items = _engine(store).list_stages(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return items


@router.get("/projects/{project_id}/stages/timeline")
def get_project_stages_timeline(project_id: str, store: JsonStore = Depends(get_json_store)):
    """
    Timeline view derived from stage runtime fields.
    This repo's stage store is JSON-based; we keep the response lightweight and stable.
    """
    try:
        stages = _engine(store).list_stages(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    items = []
    for s in stages:
        start_dt = _parse_dt(s.get("start_date"))
        end_dt = _parse_dt(s.get("end_date"))
        items.append(
            {
                "stage_id": s.get("id"),
                "name": s.get("name"),
                "phase": s.get("phase"),
                "order": s.get("order"),
                "status": s.get("status"),
                "start_date": s.get("start_date"),
                "end_date": s.get("end_date"),
                "duration_minutes": _minutes_between(start_dt, end_dt),
            }
        )
    items.sort(key=lambda x: int(x.get("order") or 0))
    return {"project_id": project_id, "items": items, "total": len(items)}


@router.get("/projects/{project_id}/stages/health")
def get_project_stages_health(project_id: str, store: JsonStore = Depends(get_json_store)):
    """
    Health/overdue signals for the current stage.
    - stage timeout: based on stage.start_date + timeout_days
    - approval timeout: based on stage.end_date (complete -> review time) + approval.timeout_hours
    """
    try:
        stages = _engine(store).list_stages(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

    cur = _pick_current_stage(stages) or {}
    now = datetime.now().astimezone()
    start_dt = _parse_dt(cur.get("start_date"))
    end_dt = _parse_dt(cur.get("end_date"))

    timeout_days = int(cur.get("timeout_days") or 0)
    stage_timeout_minutes = max(0, timeout_days) * 24 * 60

    approval = cur.get("approval") or {}
    timeout_hours = int(approval.get("timeout_hours") or 0)
    approval_timeout_minutes = max(0, timeout_hours) * 60

    stage_overdue_minutes = None
    if start_dt and stage_timeout_minutes > 0:
        mins = _minutes_between(start_dt, now)
        if mins is not None:
            stage_overdue_minutes = max(0.0, round(mins - float(stage_timeout_minutes), 1))

    approval_overdue_minutes = None
    if str(cur.get("status") or "") == "review" and end_dt and approval_timeout_minutes > 0:
        mins = _minutes_between(end_dt, now)
        if mins is not None:
            approval_overdue_minutes = max(0.0, round(mins - float(approval_timeout_minutes), 1))

    return {
        "project_id": project_id,
        "current_stage": {
            "stage_id": cur.get("id"),
            "name": cur.get("name"),
            "phase": cur.get("phase"),
            "order": cur.get("order"),
            "status": cur.get("status"),
            "start_date": cur.get("start_date"),
            "end_date": cur.get("end_date"),
        },
        "stage_timeout_minutes": stage_timeout_minutes,
        "approval_timeout_minutes": approval_timeout_minutes if str(cur.get("status") or "") == "review" else None,
        "stage_overdue": bool(stage_overdue_minutes is not None and stage_overdue_minutes > 0),
        "approval_overdue": bool(approval_overdue_minutes is not None and approval_overdue_minutes > 0),
        "stage_overdue_minutes": stage_overdue_minutes,
        "approval_overdue_minutes": approval_overdue_minutes,
    }


@router.post("/projects/{project_id}/stages/health/check")
def check_and_emit_project_stage_timeout_alert(
    project_id: str,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit=Depends(get_audit_store),
    engine: PolicyEngine = Depends(get_policy_engine),
    force: bool = Query(False, description="dev-only: force emit for rehearsal/testing"),
    cooldown_minutes: int | None = Query(
        None, ge=0, le=24 * 60, description="dedupe cooldown window in minutes (default from policy when omitted)"
    ),
    stage_overdue_threshold_minutes: int | None = Query(
        None, ge=0, le=365 * 24 * 60, description="stage overdue threshold minutes (default from policy when omitted)"
    ),
    approval_overdue_threshold_minutes: int | None = Query(
        None, ge=0, le=365 * 24 * 60, description="approval overdue threshold minutes (default from policy when omitted)"
    ),
):
    """
    Explicit check endpoint (no side effects in GET):
    - When stage/approval overdue: emit a project discussion marker + audit event (non-blocking).
    - Dedupe: skip emitting when a same marker exists in cooldown window.
    """
    env = _project_env_or_default(store, project_id)
    effective_cooldown = (
        int(cooldown_minutes)
        if cooldown_minutes is not None
        else _stage_timeout_alert_cooldown_minutes(engine, env)
    )
    effective_stage_threshold = (
        int(stage_overdue_threshold_minutes)
        if stage_overdue_threshold_minutes is not None
        else _stage_timeout_alert_overdue_threshold_minutes(engine, env, kind="stage")
    )
    effective_approval_threshold = (
        int(approval_overdue_threshold_minutes)
        if approval_overdue_threshold_minutes is not None
        else _stage_timeout_alert_overdue_threshold_minutes(engine, env, kind="approval")
    )
    if not _stage_timeout_alert_enabled(engine, env):
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_timeout_alert",
            allowed=False,
            reason="stage timeout alert disabled by policy",
            reason_code="STAGE_TIMEOUT_ALERT_DISABLED",
            context={"project_id": project_id, "force": bool(force), "cooldown_minutes": effective_cooldown},
        )
        return {
            "status": "skipped",
            "emitted": False,
            "reason_code": "DISABLED",
            "health": None,
            "thresholds": {
                "stage_overdue_threshold_minutes": effective_stage_threshold,
                "approval_overdue_threshold_minutes": effective_approval_threshold,
            },
            "hits": {"stage_overdue_hit": False, "approval_overdue_hit": False},
        }

    if force and not _stage_timeout_alert_allow_force(engine, env):
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_timeout_alert",
            allowed=False,
            reason="force not allowed by policy",
            reason_code="STAGE_TIMEOUT_ALERT_FORCE_NOT_ALLOWED",
            context={"project_id": project_id, "force": True, "cooldown_minutes": effective_cooldown},
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "FORCE_NOT_ALLOWED",
                "reason": "force=true is only allowed in dev",
            },
        )
    health = get_project_stages_health(project_id=project_id, store=store)
    cur = health.get("current_stage") or {}

    stage_overdue_minutes = health.get("stage_overdue_minutes")
    approval_overdue_minutes = health.get("approval_overdue_minutes")
    stage_overdue_hit = bool(
        health.get("stage_overdue")
        and stage_overdue_minutes is not None
        and float(stage_overdue_minutes) >= float(effective_stage_threshold)
    )
    approval_overdue_hit = bool(
        health.get("approval_overdue")
        and approval_overdue_minutes is not None
        and float(approval_overdue_minutes) >= float(effective_approval_threshold)
    )
    is_overdue = bool(stage_overdue_hit or approval_overdue_hit)
    if force and env == "dev":
        is_overdue = True

    marker = "[STAGE_TIMEOUT_ALERT]"
    if not is_overdue:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_timeout_alert",
            allowed=True,
            reason="not overdue",
            reason_code="STAGE_TIMEOUT_ALERT_NOT_OVERDUE",
            context={
                "project_id": project_id,
                "health": health,
                "force": bool(force),
                "cooldown_minutes": effective_cooldown,
                "stage_overdue_threshold_minutes": effective_stage_threshold,
                "approval_overdue_threshold_minutes": effective_approval_threshold,
                "stage_overdue_hit": stage_overdue_hit,
                "approval_overdue_hit": approval_overdue_hit,
            },
        )
        return {
            "status": "no_alert",
            "emitted": False,
            "health": health,
            "thresholds": {
                "stage_overdue_threshold_minutes": effective_stage_threshold,
                "approval_overdue_threshold_minutes": effective_approval_threshold,
            },
            "hits": {
                "stage_overdue_hit": stage_overdue_hit,
                "approval_overdue_hit": approval_overdue_hit,
            },
        }

    can_emit = _should_emit_timeout_alert(
        store=store,
        project_id=project_id,
        marker=marker,
        cooldown_minutes=effective_cooldown,
    )
    if not can_emit:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_timeout_alert",
            allowed=False,
            reason="cooldown active",
            reason_code="STAGE_TIMEOUT_ALERT_SKIPPED_COOLDOWN",
            context={
                "project_id": project_id,
                "health": health,
                "force": bool(force),
                "cooldown_minutes": effective_cooldown,
                "stage_overdue_threshold_minutes": effective_stage_threshold,
                "approval_overdue_threshold_minutes": effective_approval_threshold,
                "stage_overdue_hit": stage_overdue_hit,
                "approval_overdue_hit": approval_overdue_hit,
            },
        )
        return {
            "status": "skipped",
            "emitted": False,
            "reason_code": "COOLDOWN_ACTIVE",
            "health": health,
            "thresholds": {
                "stage_overdue_threshold_minutes": effective_stage_threshold,
                "approval_overdue_threshold_minutes": effective_approval_threshold,
            },
            "hits": {
                "stage_overdue_hit": stage_overdue_hit,
                "approval_overdue_hit": approval_overdue_hit,
            },
        }

    # Emit discussion (non-blocking best-effort).
    try:
        stage_id = str(cur.get("stage_id") or "")
        stage_name = str(cur.get("name") or "")
        stage_status = str(cur.get("status") or "")
        body = (
            f"{marker} project_id={project_id}; stage_id={stage_id}; "
            f"stage={stage_name}; status={stage_status}; env={env}; "
            f"stage_overdue={health.get('stage_overdue')}; approval_overdue={health.get('approval_overdue')}; "
            f"stage_overdue_minutes={health.get('stage_overdue_minutes')}; "
            f"approval_overdue_minutes={health.get('approval_overdue_minutes')}; "
            f"force={bool(force)}"
        )[:8000]
        store.add_project_discussion(project_id, author="stage-timeout-bot", body=body)
    except Exception:
        pass

    _audit_stage(
        audit=audit,
        request=request,
        environment=env,
        event_type="project_stage_timeout_alert",
        allowed=True,
        reason="timeout alert emitted",
        reason_code="STAGE_TIMEOUT_ALERT_EMITTED",
        context={
            "project_id": project_id,
            "health": health,
            "force": bool(force),
            "cooldown_minutes": effective_cooldown,
            "stage_overdue_threshold_minutes": effective_stage_threshold,
            "approval_overdue_threshold_minutes": effective_approval_threshold,
            "stage_overdue_hit": stage_overdue_hit,
            "approval_overdue_hit": approval_overdue_hit,
        },
    )
    return {
        "status": "emitted",
        "emitted": True,
        "health": health,
        "thresholds": {
            "stage_overdue_threshold_minutes": effective_stage_threshold,
            "approval_overdue_threshold_minutes": effective_approval_threshold,
        },
        "hits": {
            "stage_overdue_hit": stage_overdue_hit,
            "approval_overdue_hit": approval_overdue_hit,
        },
    }


@router.get("/projects/{project_id}/stages/{stage_id}")
def get_project_stage(project_id: str, stage_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        stage = _engine(store).get_stage(project_id, stage_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return stage


@router.post("/projects/{project_id}/stages/{stage_id}/start")
def start_project_stage(
    project_id: str,
    stage_id: str,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit=Depends(get_audit_store),
):
    env = _project_env_or_default(store, project_id)
    try:
        stage = _engine(store).start_stage(project_id, stage_id)
    except ValueError as e:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_start",
            allowed=False,
            reason=str(e),
            reason_code="STAGE_START_INVALID",
            context={"project_id": project_id, "stage_id": stage_id},
        )
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_start",
            allowed=False,
            reason=str(e),
            reason_code="STAGE_START_NOT_FOUND",
            context={"project_id": project_id, "stage_id": stage_id},
        )
        raise HTTPException(status_code=404, detail=str(e))
    _audit_stage(
        audit=audit,
        request=request,
        environment=env,
        event_type="project_stage_start",
        allowed=True,
        reason="stage started",
        reason_code="STAGE_STARTED",
        context={"project_id": project_id, "stage_id": stage_id, "status": stage.status},
    )
    return {"status": "success", "stage": stage.model_dump(mode="json", by_alias=True)}


@router.post("/projects/{project_id}/stages/{stage_id}/complete")
def complete_project_stage(
    project_id: str,
    stage_id: str,
    payload: StageCompleteRequest,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit=Depends(get_audit_store),
):
    env = _project_env_or_default(store, project_id)
    try:
        stage = _engine(store).complete_stage(
            project_id, stage_id, deliverables=payload.deliverables, comments=payload.comments
        )
    except ValueError as e:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_complete",
            allowed=False,
            reason=str(e),
            reason_code="STAGE_COMPLETE_INVALID",
            context={"project_id": project_id, "stage_id": stage_id},
        )
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_complete",
            allowed=False,
            reason=str(e),
            reason_code="STAGE_COMPLETE_NOT_FOUND",
            context={"project_id": project_id, "stage_id": stage_id},
        )
        raise HTTPException(status_code=404, detail=str(e))
    _audit_stage(
        audit=audit,
        request=request,
        environment=env,
        event_type="project_stage_complete",
        allowed=True,
        reason="stage completed",
        reason_code="STAGE_COMPLETED",
        context={
            "project_id": project_id,
            "stage_id": stage_id,
            "status": stage.status,
            "deliverable_count": len(payload.deliverables),
        },
    )
    return {"status": "success", "stage": stage.model_dump(mode="json", by_alias=True)}


@router.post("/projects/{project_id}/stages/{stage_id}/approve")
def approve_project_stage(
    project_id: str,
    stage_id: str,
    payload: StageApproveRequest,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit=Depends(get_audit_store),
):
    env = _project_env_or_default(store, project_id)
    # Environment-level enforcement: staging/prod must provide approver identity
    if env in {"staging", "prod"}:
        if not (payload.approver_role and str(payload.approver_role).strip()) or not (
            payload.approver_level and str(payload.approver_level).strip()
        ):
            _audit_stage(
                audit=audit,
                request=request,
                environment=env,
                event_type="project_stage_approve",
                allowed=False,
                reason="approver identity required in staging/prod",
                reason_code="APPROVER_ID_REQUIRED",
                context={
                    "project_id": project_id,
                    "stage_id": stage_id,
                    "approved": payload.approved,
                    "approver_role": payload.approver_role,
                    "approver_level": payload.approver_level,
                },
            )
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "APPROVER_ID_REQUIRED",
                    "reason": "approver_role/approver_level are required in staging/prod",
                },
            )
    # If either approver field is present, require both (avoid half-identity bypass).
    has_role = bool(payload.approver_role and str(payload.approver_role).strip())
    has_level = bool(payload.approver_level and str(payload.approver_level).strip())
    if (payload.approver_role is not None or payload.approver_level is not None) and (has_role != has_level):
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_approve",
            allowed=False,
            reason="incomplete approver identity",
            reason_code="APPROVER_ID_INCOMPLETE",
            context={
                "project_id": project_id,
                "stage_id": stage_id,
                "approved": payload.approved,
                "approver_role": payload.approver_role,
                "approver_level": payload.approver_level,
            },
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "APPROVER_ID_INCOMPLETE",
                "reason": "approver_role and approver_level must be provided together when present",
            },
        )
    # Approver identity check (backward-compatible): validate only when provided.
    if payload.approver_role or payload.approver_level:
        try:
            stage_row = _engine(store).get_stage(project_id, stage_id)
        except Exception as e:
            stage_row = None
        if stage_row:
            ap = stage_row.get("approval") or {}
            expected_role = str(ap.get("approver_role") or "").strip()
            expected_level = str(ap.get("approver_level") or "").strip()
            got_role = str(payload.approver_role or "").strip()
            got_level = str(payload.approver_level or "").strip()
            if (got_role and expected_role and got_role != expected_role) or (
                got_level and expected_level and got_level != expected_level
            ):
                _audit_stage(
                    audit=audit,
                    request=request,
                    environment=env,
                    event_type="project_stage_approve",
                    allowed=False,
                    reason="approver mismatch",
                    reason_code="APPROVER_MISMATCH",
                    context={
                        "project_id": project_id,
                        "stage_id": stage_id,
                        "approved": payload.approved,
                        "expected_approver_role": expected_role,
                        "expected_approver_level": expected_level,
                        "approver_role": payload.approver_role,
                        "approver_level": payload.approver_level,
                    },
                )
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error_code": "APPROVER_MISMATCH",
                        "reason": "approver_role/approver_level must match stage approval config",
                        "expected": {"role": expected_role, "level": expected_level},
                        "got": {"role": got_role or None, "level": got_level or None},
                    },
                )
    try:
        stage = _engine(store).approve_stage(
            project_id,
            stage_id,
            approved=payload.approved,
            comments=payload.comments,
            approver_role=str(payload.approver_role).strip() if payload.approver_role else None,
            approver_level=str(payload.approver_level).strip() if payload.approver_level else None,
        )
    except ValueError as e:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_approve",
            allowed=False,
            reason=str(e),
            reason_code="STAGE_APPROVE_INVALID",
            context={"project_id": project_id, "stage_id": stage_id, "approved": payload.approved},
        )
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_approve",
            allowed=False,
            reason=str(e),
            reason_code="STAGE_APPROVE_NOT_FOUND",
            context={"project_id": project_id, "stage_id": stage_id, "approved": payload.approved},
        )
        raise HTTPException(status_code=404, detail=str(e))
    _audit_stage(
        audit=audit,
        request=request,
        environment=env,
        event_type="project_stage_approve",
        allowed=bool(payload.approved),
        reason="stage approved" if payload.approved else "stage rejected",
        reason_code="STAGE_APPROVED" if payload.approved else "STAGE_REJECTED",
        context={
            "project_id": project_id,
            "stage_id": stage_id,
            "status": stage.status,
            "comments": payload.comments,
            "approver_role": payload.approver_role,
            "approver_level": payload.approver_level,
        },
    )
    # Persist a discussion log entry for traceability (non-blocking).
    try:
        who = "/".join(
            x for x in [str(payload.approver_level or "").strip(), str(payload.approver_role or "").strip()] if x
        ) or "unknown"
        decision = "approved" if bool(payload.approved) else "rejected"
        body = (
            f"[STAGE_APPROVAL] project_id={project_id}; stage_id={stage_id}; "
            f"decision={decision}; approver={who}; env={env}; "
            f"comments={str(payload.comments or '').strip()}"
        )[:8000]
        store.add_project_discussion(project_id, author="stage-approval-bot", body=body)
    except Exception:
        pass
    return {"status": "success", "stage": stage.model_dump(mode="json", by_alias=True)}


@router.get("/projects/{project_id}/stages/{stage_id}/deliverables")
def list_stage_deliverables(project_id: str, stage_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        items = _engine(store).list_stage_deliverables(project_id, stage_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"items": [d.model_dump(mode="json", by_alias=True) for d in items]}


@router.post("/projects/{project_id}/stages/{stage_id}/deliverables/{deliverable_name}")
def upload_stage_deliverable(
    project_id: str,
    stage_id: str,
    deliverable_name: str,
    payload: Deliverable,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit=Depends(get_audit_store),
):
    """
    Minimal JSON-based deliverable upload for this repo.
    For large file workflows, a future iteration can switch to UploadFile.
    """
    env = _project_env_or_default(store, project_id)
    try:
        stage = _engine(store).get_stage(project_id, stage_id)
    except (ValueError, KeyError) as e:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_deliverable_upload",
            allowed=False,
            reason=str(e),
            reason_code="DELIVERABLE_STAGE_NOT_FOUND",
            context={"project_id": project_id, "stage_id": stage_id, "deliverable_name": deliverable_name},
        )
        raise HTTPException(status_code=400 if isinstance(e, ValueError) else 404, detail=str(e))

    defined_names = {
        str(d.get("name", "")).strip()
        for d in (stage.get("deliverables") or [])
        if str(d.get("name", "")).strip()
    }
    if deliverable_name not in defined_names:
        _audit_stage(
            audit=audit,
            request=request,
            environment=env,
            event_type="project_stage_deliverable_upload",
            allowed=False,
            reason="unknown deliverable",
            reason_code="UNKNOWN_DELIVERABLE",
            context={"project_id": project_id, "stage_id": stage_id, "deliverable_name": deliverable_name},
        )
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "UNKNOWN_DELIVERABLE",
                "reason": f"deliverable_name must be one of {sorted(defined_names)}",
            },
        )

    actual = list(stage.get("actual_deliverables") or [])
    # Normalize name to path param.
    payload_dict = payload.model_dump(mode="json", by_alias=True)
    payload_dict["name"] = deliverable_name
    actual = [row for row in actual if str(row.get("name", "")).strip() != deliverable_name]
    actual.append(payload_dict)
    stage["actual_deliverables"] = actual
    # Keep stage status unchanged; user can complete stage with full deliverables set.
    store.update_project(project_id, {"stages": [s if str(s.get("id")) != stage_id else stage for s in store.get_project(project_id).get("stages", [])]})
    _audit_stage(
        audit=audit,
        request=request,
        environment=env,
        event_type="project_stage_deliverable_upload",
        allowed=True,
        reason="deliverable uploaded",
        reason_code="DELIVERABLE_UPLOADED",
        context={
            "project_id": project_id,
            "stage_id": stage_id,
            "deliverable_name": deliverable_name,
            "content_len": len(str(payload_dict.get("content_text") or "")),
        },
    )
    return StageDeliverableUploadResponse(
        stage_id=stage_id,
        deliverable=Deliverable.model_validate(payload_dict),
    ).model_dump(mode="json", by_alias=True)

