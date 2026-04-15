from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.core.deps import get_json_store
from app.core.store import JsonStore
from app.models.skill import SkillCreateRequest, SkillOut, SkillUpdateRequest

router = APIRouter(tags=["skills"])


def _out(s: dict) -> dict:
    return SkillOut.from_record(s).model_dump(mode="json")


@router.post("/skills", status_code=201)
def create_skill(payload: SkillCreateRequest, store: JsonStore = Depends(get_json_store)):
    try:
        return _out(store.create_skill(payload.model_dump()))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/skills")
def list_skills(
    store: JsonStore = Depends(get_json_store),
    category: str | None = None,
    level: str | None = None,
    q: str | None = None,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    items, total = store.list_skills(category=category, level=level, q=q, limit=limit, offset=offset)
    return {"items": [_out(s) for s in items], "total": total, "limit": limit, "offset": offset}


@router.get("/skills/{skill_id}")
def get_skill(skill_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        return _out(store.get_skill(skill_id))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/skills/{skill_id}")
def update_skill(skill_id: str, payload: SkillUpdateRequest, store: JsonStore = Depends(get_json_store)):
    patch = payload.model_dump(exclude_unset=True)
    if not patch:
        try:
            return _out(store.get_skill(skill_id))
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e))
    try:
        return _out(store.update_skill(skill_id, patch))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/skills/{skill_id}")
def delete_skill(skill_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        store.delete_skill(skill_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return Response(status_code=204)
