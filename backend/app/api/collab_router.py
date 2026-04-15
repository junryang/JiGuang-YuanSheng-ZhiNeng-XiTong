from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from starlette.responses import Response
from pydantic import BaseModel, Field

from app.core.audit import AuditStore
from app.core.deps import get_audit_store, get_json_store
from app.core.store import JsonStore

router = APIRouter(tags=["collaboration"])


def _error_detail(error_code: str, reason: str, **extra) -> dict:
    d = {"error_code": error_code, "reason": reason}
    d.update(extra)
    return d


def _keyerror_to_not_found(e: KeyError) -> tuple[str, str]:
    reason = str(e)
    low = reason.lower()
    if "agent not found" in low:
        return "AGENT_NOT_FOUND", reason
    if "project not found" in low:
        return "PROJECT_NOT_FOUND", reason
    if "delegation not found" in low:
        return "DELEGATION_NOT_FOUND", reason
    return "RESOURCE_NOT_FOUND", reason


def _audit_collaboration(
    request: Request,
    audit: AuditStore,
    event_type: str,
    reason: str,
    *,
    reason_code: str = "COLLAB_OK",
    context: dict | None = None,
) -> None:
    audit.add(
        event_type=event_type,
        policy_id="collaboration",
        policy_version="0",
        environment="dev",
        allowed=True,
        reason=reason,
        reason_code=reason_code,
        endpoint=request.url.path,
        context=context or {},
    )


class DelegationCreateRequest(BaseModel):
    class DelegationContract(BaseModel):
        acceptance_criteria: str = Field(..., min_length=1, description="验收标准")
        deliverables: list[str] = Field(..., min_length=1, description="交付物清单（至少1项）")
        due_date: str | None = Field(None, description="截止日期（可选，ISO 日期）")

    from_agent_id: str
    to_agent_id: str
    objective: str = Field(..., min_length=1)
    contract: DelegationContract
    project_id: str | None = None
    status: str = Field("open", description="open|accepted|done")


@router.post("/collaboration/delegations", status_code=201)
def create_delegation(
    payload: DelegationCreateRequest,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit: AuditStore = Depends(get_audit_store),
):
    try:
        row = store.create_delegation(payload.model_dump())
    except KeyError as e:
        code, reason = _keyerror_to_not_found(e)
        raise HTTPException(status_code=404, detail=_error_detail(code, reason))
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=_error_detail("DELEGATION_CONTRACT_INVALID", str(e)),
        )
    _audit_collaboration(
        request,
        audit,
        "delegation.create",
        f"id={row.get('id')} from={row.get('from_agent_id')} to={row.get('to_agent_id')}",
        reason_code="DELEGATION_CREATED",
        context={"delegation_id": row.get("id"), "from_agent_id": row.get("from_agent_id"), "to_agent_id": row.get("to_agent_id")},
    )
    return row


@router.get("/collaboration/delegations/{delegation_id}")
def get_delegation(delegation_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        return store.get_delegation(delegation_id)
    except KeyError as e:
        code, reason = _keyerror_to_not_found(e)
        raise HTTPException(status_code=404, detail=_error_detail(code, reason))


@router.get("/collaboration/delegations")
def list_delegations(
    store: JsonStore = Depends(get_json_store),
    from_agent_id: str | None = None,
    to_agent_id: str | None = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    items, total = store.list_delegations(
        from_agent_id=from_agent_id,
        to_agent_id=to_agent_id,
        limit=limit,
        offset=offset,
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}


class DelegationStatusPatch(BaseModel):
    status: Literal["open", "accepted", "done"]


@router.patch("/collaboration/delegations/{delegation_id}")
def patch_delegation_status(
    delegation_id: str,
    payload: DelegationStatusPatch,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit: AuditStore = Depends(get_audit_store),
):
    try:
        row = store.update_delegation_status(delegation_id, payload.status)
    except KeyError as e:
        code, reason = _keyerror_to_not_found(e)
        raise HTTPException(status_code=404, detail=_error_detail(code, reason))
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=_error_detail("INVALID_DELEGATION_STATUS", str(e)),
        )
    _audit_collaboration(
        request,
        audit,
        "delegation.patch",
        f"id={delegation_id} status={payload.status}",
        reason_code="DELEGATION_STATUS_UPDATED",
        context={"delegation_id": delegation_id, "status": payload.status},
    )
    return row


@router.delete("/collaboration/delegations/{delegation_id}", status_code=204)
def delete_delegation(
    delegation_id: str,
    request: Request,
    store: JsonStore = Depends(get_json_store),
    audit: AuditStore = Depends(get_audit_store),
):
    try:
        store.delete_delegation(delegation_id)
    except KeyError as e:
        code, reason = _keyerror_to_not_found(e)
        raise HTTPException(status_code=404, detail=_error_detail(code, reason))
    _audit_collaboration(
        request,
        audit,
        "delegation.delete",
        f"id={delegation_id}",
        reason_code="DELEGATION_DELETED",
        context={"delegation_id": delegation_id},
    )
    return Response(status_code=204)
