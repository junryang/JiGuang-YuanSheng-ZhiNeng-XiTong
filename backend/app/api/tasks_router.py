from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response

from app.core.deps import get_json_store
from app.core.store import JsonStore
from app.models.task import TaskCreateNestedRequest, TaskCreateRequest, TaskOut, TaskUpdateRequest
from app.schemas.common_enums import TaskStatus

router = APIRouter(tags=["tasks"])


def _to_task_out(t: dict) -> dict:
    return TaskOut.from_record(t).model_dump(mode="json")


@router.get("/projects/{project_id}/tasks")
def list_tasks_for_project(
    project_id: str,
    store: JsonStore = Depends(get_json_store),
    parent_id: str | None = None,
    root_only: bool = Query(False, description="仅返回无 parent 的顶层任务"),
    status: TaskStatus | None = None,
    assignee_id: str | None = Query(None, description="按负责人智能体ID筛选"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    try:
        store.get_project(project_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"project not found: {project_id}")
    items, total = store.list_tasks(
        project_id=project_id,
        assignee_id=assignee_id,
        parent_id=parent_id,
        root_only=root_only,
        status=status,
        limit=limit,
        offset=offset,
    )
    return {"items": [_to_task_out(t) for t in items], "total": total, "limit": limit, "offset": offset}


@router.post("/projects/{project_id}/tasks", status_code=201)
def create_task_for_project(
    project_id: str,
    payload: TaskCreateNestedRequest,
    store: JsonStore = Depends(get_json_store),
):
    body = payload.model_dump()
    body["project_id"] = project_id
    try:
        task = store.create_task(body)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _to_task_out(task)


@router.post("/tasks", status_code=201)
def create_task(payload: TaskCreateRequest, store: JsonStore = Depends(get_json_store)):
    try:
        task = store.create_task(payload.model_dump())
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _to_task_out(task)


@router.get("/tasks")
def list_tasks(
    store: JsonStore = Depends(get_json_store),
    project_id: str | None = None,
    parent_id: str | None = None,
    root_only: bool = Query(False),
    status: TaskStatus | None = None,
    assignee_id: str | None = Query(None, description="按负责人智能体ID筛选"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    items, total = store.list_tasks(
        project_id=project_id,
        assignee_id=assignee_id,
        parent_id=parent_id,
        root_only=root_only,
        status=status,
        limit=limit,
        offset=offset,
    )
    return {"items": [_to_task_out(t) for t in items], "total": total, "limit": limit, "offset": offset}


@router.get("/tasks/{task_id}")
def get_task(task_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        return _to_task_out(store.get_task(task_id))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/tasks/{task_id}")
def update_task(task_id: str, payload: TaskUpdateRequest, store: JsonStore = Depends(get_json_store)):
    patch = payload.model_dump(exclude_unset=True)
    patch.pop("project_id", None)
    if not patch:
        try:
            return _to_task_out(store.get_task(task_id))
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e))
    try:
        return _to_task_out(store.update_task(task_id, patch))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, store: JsonStore = Depends(get_json_store)):
    try:
        store.delete_task(task_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return Response(status_code=204)
