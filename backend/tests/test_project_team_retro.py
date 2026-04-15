from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _new_project():
    r = client.post(
        "/api/v1/projects",
        json={
            "name": "团队与复盘",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert r.status_code == 200
    return r.json()["id"]


def test_project_team_from_task_assignees():
    pid = _new_project()
    c = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "子任务 A",
            "assignee_level": "L3",
            "assignee_role": "PM",
        },
    )
    assert c.status_code == 201
    g = client.get(f"/api/v1/projects/{pid}/team")
    assert g.status_code == 200
    items = g.json()["items"]
    assert len(items) == 1
    assert items[0]["task_count"] == 1
    assert items[0]["assignee_level"] == "L3"
    assert items[0]["assignee_role"] == "PM"


def test_project_team_404():
    r = client.get("/api/v1/projects/missing-proj/team")
    assert r.status_code == 404


def test_project_retrospective_put_and_get():
    pid = _new_project()
    u = client.put(
        f"/api/v1/projects/{pid}",
        json={"retrospective_report": "本轮完成联调与文档补齐。"},
    )
    assert u.status_code == 200
    assert u.json().get("retrospective_report") == "本轮完成联调与文档补齐。"
    g = client.get(f"/api/v1/projects/{pid}")
    assert g.json().get("retrospective_report") == "本轮完成联调与文档补齐。"
