from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.core.deps import get_json_store
from app.core.store import JsonStore

router = APIRouter(tags=["memory"])


class WorkingMemoryAppend(BaseModel):
    content: str = Field(..., min_length=1)


@router.get("/agents/{agent_id}/memory/working")
def list_working_memory(
    agent_id: str,
    store: JsonStore = Depends(get_json_store),
    limit: int = Query(50, ge=1, le=200),
):
    try:
        return {"items": store.list_working_memories(agent_id, limit=limit)}
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/agents/{agent_id}/memory")
def get_agent_memory(
    agent_id: str,
    store: JsonStore = Depends(get_json_store),
    limit: int = Query(50, ge=1, le=200),
):
    try:
        items = store.list_working_memories(agent_id, limit=limit)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {
        "agent_id": agent_id,
        "working_memory_count": len(items),
        "working_memories": items,
    }


@router.post("/agents/{agent_id}/memory/working", status_code=201)
def append_working_memory(
    agent_id: str,
    payload: WorkingMemoryAppend,
    store: JsonStore = Depends(get_json_store),
):
    try:
        return store.append_working_memory(agent_id, payload.content)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
