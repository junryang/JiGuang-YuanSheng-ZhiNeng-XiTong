from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _new_project():
    r = client.post(
        "/api/v1/projects",
        json={
            "name": "讨论区",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert r.status_code == 200
    return r.json()["id"]


def test_project_discussion_list_and_post():
    pid = _new_project()
    g = client.get(f"/api/v1/projects/{pid}/discussion")
    assert g.status_code == 200
    assert g.json()["total"] == 0

    p = client.post(
        f"/api/v1/projects/{pid}/discussion",
        json={"body": "第一条留言", "author": "老板"},
    )
    assert p.status_code == 201
    assert p.json()["body"] == "第一条留言"

    g2 = client.get(f"/api/v1/projects/{pid}/discussion")
    assert g2.json()["total"] == 1
    assert g2.json()["items"][0]["author"] == "老板"


def test_project_discussion_404_project():
    r = client.get("/api/v1/projects/nonexistent-id/discussion")
    assert r.status_code == 404
