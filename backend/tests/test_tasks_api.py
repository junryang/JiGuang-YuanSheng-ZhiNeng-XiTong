from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _any_project_id() -> str:
    r = client.get("/api/v1/projects")
    assert r.status_code == 200
    lst = r.json()
    if lst:
        return lst[0]["id"]
    c = client.post(
        "/api/v1/projects",
        json={
            "name": "任务测试容器",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert c.status_code == 200
    return c.json()["id"]


def test_task_create_list_get_update_delete():
    pid = _any_project_id()
    c = client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "父任务", "priority": "P0", "description": "d1"},
    )
    assert c.status_code == 201
    tid = c.json()["id"]

    child = client.post(
        f"/api/v1/projects/{pid}/tasks",
        json={"name": "子任务", "parent_id": tid, "priority": "P1"},
    )
    assert child.status_code == 201
    cid = child.json()["id"]
    assert child.json()["parent_id"] == tid

    lst = client.get("/api/v1/tasks", params={"project_id": pid})
    assert lst.status_code == 200
    assert lst.json()["total"] >= 2

    root = client.get("/api/v1/tasks", params={"project_id": pid, "root_only": True})
    assert root.status_code == 200
    assert all(not t.get("parent_id") for t in root.json()["items"])

    g = client.get(f"/api/v1/tasks/{tid}")
    assert g.status_code == 200
    assert g.json()["name"] == "父任务"

    u = client.put(f"/api/v1/tasks/{tid}", json={"progress": 50, "status": "in_progress"})
    assert u.status_code == 200
    assert u.json()["progress"] == 50

    assert client.delete(f"/api/v1/tasks/{cid}").status_code == 204
    assert client.delete(f"/api/v1/tasks/{tid}").status_code == 204


def test_task_delete_blocked_with_children():
    pid = _any_project_id()
    p = client.post("/api/v1/tasks", json={"project_id": pid, "name": "根"}).json()
    client.post(f"/api/v1/projects/{pid}/tasks", json={"name": "子", "parent_id": p["id"]})
    r = client.delete(f"/api/v1/tasks/{p['id']}")
    assert r.status_code == 400


def test_task_circular_dependency_rejected():
    pid = _any_project_id()
    a = client.post("/api/v1/tasks", json={"project_id": pid, "name": "A"}).json()
    b = client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "B", "dependencies": [a["id"]]},
    ).json()
    r = client.put(f"/api/v1/tasks/{a['id']}", json={"dependencies": [b["id"]]})
    assert r.status_code == 400


def test_task_status_transition_guard():
    pid = _any_project_id()
    c = client.post("/api/v1/tasks", json={"project_id": pid, "name": "状态流转任务"})
    assert c.status_code == 201
    tid = c.json()["id"]

    ok = client.put(f"/api/v1/tasks/{tid}", json={"status": "in_progress"})
    assert ok.status_code == 200
    assert ok.json()["status"] == "in_progress"

    bad = client.put(f"/api/v1/tasks/{tid}", json={"status": "pending"})
    assert bad.status_code == 400
    assert "invalid task status transition" in str(bad.json()["detail"])


def test_task_list_rejects_invalid_status_filter():
    r = client.get("/api/v1/tasks", params={"status": "archived"})
    assert r.status_code == 422


def test_task_list_filters_by_assignee_id():
    pid = _any_project_id()
    c = client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "assignee-filter-task", "assignee_id": "agent-ceo"},
    )
    assert c.status_code == 201
    tid = c.json()["id"]

    hit = client.get("/api/v1/tasks", params={"project_id": pid, "assignee_id": "agent-ceo"})
    assert hit.status_code == 200
    assert any(t["id"] == tid for t in hit.json()["items"])

    miss = client.get("/api/v1/tasks", params={"project_id": pid, "assignee_id": "agent-no-such"})
    assert miss.status_code == 200
    assert all(t.get("assignee_id") == "agent-no-such" for t in miss.json()["items"])
