from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.deps import get_audit_store, get_json_store
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

