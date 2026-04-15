"""营销中心 API（PH4-T04）：看板指标、内容列表、AI 初稿与策略门控发布。"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Tuple

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, Field

from app.core.deps import get_audit_store, get_json_store, get_policy_engine
from app.core.policy_guard import require_policy_sequence
from app.core.store import JsonStore
from app.services.chat_service import resolve_assistant_text

router = APIRouter(prefix="/marketing", tags=["marketing"])

_DEFAULT_PUBLISH_LAW: Tuple[str, ...] = ("LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05")


class MarketingContentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    body: str = Field("", max_length=50000)
    platforms: List[str] = Field(default_factory=list)
    status: Literal["draft", "published", "scheduled"] = "draft"


class MarketingContentUpdate(BaseModel):
    title: str | None = Field(None, max_length=500)
    body: str | None = Field(None, max_length=50000)
    status: Literal["draft", "published", "scheduled"] | None = None
    platforms: List[str] | None = None


class MarketingMetricsPatch(BaseModel):
    fans_growth_7d: int | None = None
    engagement_rate_pct: float | None = None
    reach_7d: int | None = None
    posts_published_7d: int | None = None


class MarketingAiDraftBody(BaseModel):
    hint: str = Field("", max_length=2000, description="额外写作要点")


class MarketingPublishBody(BaseModel):
    """与 POST /contents/publish 相同策略门控（CEO-POLICY-13/14）；law 默认五条合规链。"""

    environment: Literal["dev", "staging", "prod"] = "dev"
    law: List[str] = Field(default_factory=lambda: list(_DEFAULT_PUBLISH_LAW))
    approved: bool = False


@router.get("/dashboard")
def marketing_dashboard(store: JsonStore = Depends(get_json_store)):
    return store.marketing_dashboard()


@router.patch("/metrics")
def marketing_metrics_patch(payload: MarketingMetricsPatch, store: JsonStore = Depends(get_json_store)):
    patch: Dict[str, Any] = {k: v for k, v in payload.model_dump().items() if v is not None}
    return store.patch_marketing_metrics(patch)


@router.get("/contents")
def list_marketing_contents(
    store: JsonStore = Depends(get_json_store),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    items, total = store.list_marketing_contents(limit=limit, offset=offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.post("/contents", status_code=201)
def create_marketing_content(payload: MarketingContentCreate, store: JsonStore = Depends(get_json_store)):
    return store.create_marketing_content(
        payload.title,
        payload.body,
        payload.platforms,
        status=payload.status,
    )


@router.get("/contents/{content_id}")
def get_marketing_content(content_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        return store.get_marketing_content(content_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/contents/{content_id}")
def update_marketing_content(
    content_id: str,
    payload: MarketingContentUpdate,
    store: JsonStore = Depends(get_json_store),
):
    patch = payload.model_dump(exclude_none=True)
    if not patch:
        try:
            return store.get_marketing_content(content_id)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e))
    try:
        return store.update_marketing_content(content_id, patch)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/contents/{content_id}/ai-draft")
async def marketing_ai_draft(
    content_id: str,
    payload: MarketingAiDraftBody,
    store: JsonStore = Depends(get_json_store),
):
    try:
        row = store.get_marketing_content(content_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    hint = payload.hint.strip() or str(row.get("title", ""))
    body_preview = str(row.get("body", ""))[:1200]
    history = [
        {
            "role": "user",
            "content": (
                f"请为以下营销内容写一版可直接微调后多平台分发的中文推广稿（约 200–450 字）。\n"
                f"标题：{row.get('title', '')}\n"
                f"目标平台：{', '.join(row.get('platforms') or []) or '未指定'}\n"
                f"既有正文摘要：\n{body_preview}\n"
                f"写作要点：{hint}"
            ),
        },
    ]
    draft = await resolve_assistant_text(history)
    return {"draft": draft}


@router.post("/contents/{content_id}/publish")
def marketing_publish_through_policy(
    content_id: str,
    payload: MarketingPublishBody,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
    store: JsonStore = Depends(get_json_store),
):
    try:
        row = store.get_marketing_content(content_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))

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
                "marketing_publish_gate_p13",
            ),
            (
                "CEO-POLICY-14",
                {
                    "law": payload.law,
                    "degraded_mode": degraded,
                    "high_risk_action": True,
                },
                "marketing_publish_gate_p14",
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

    title = str(row.get("title", ""))
    body = str(row.get("body", ""))
    publish_text = f"{title}\n\n{body}"[:50000]

    store.append_marketing_publish_event(
        content_id=content_id,
        title=title,
        platforms=list(row.get("platforms") or []),
        environment=payload.environment,
    )

    return {
        "status": "published",
        "title": title,
        "environment": payload.environment,
        "content_id": content_id,
        "excerpt_length": len(publish_text),
    }
