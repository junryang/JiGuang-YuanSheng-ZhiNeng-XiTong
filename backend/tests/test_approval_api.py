from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _new_draft_project() -> str:
    r = client.post(
        "/api/v1/projects",
        json={
            "name": "审批流测试",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert r.status_code == 200
    return r.json()["id"]


def test_approval_submit_pending_list_three_step_approve():
    pid = _new_draft_project()
    sub = client.post(f"/api/v1/projects/{pid}/submit", json={"approval_chain": ["L3", "L2", "L1"]})
    assert sub.status_code == 200
    assert sub.json()["status"] == "pending_approval"
    assert sub.json()["approval"]["step"] == 0

    pend = client.get("/api/v1/projects/pending-approvals")
    assert pend.status_code == 200
    assert any(p["id"] == pid for p in pend.json()["items"])

    assert client.post(f"/api/v1/projects/{pid}/approve", json={"level": "L3"}).status_code == 200
    mid = client.get(f"/api/v1/projects/{pid}").json()
    assert mid["status"] == "pending_approval"
    assert mid["approval"]["step"] == 1

    assert client.post(f"/api/v1/projects/{pid}/approve", json={"level": "L2"}).status_code == 200
    fin = client.post(f"/api/v1/projects/{pid}/approve", json={"level": "L1"}).json()
    assert fin["status"] == "approved"
    assert fin["approval"]["step"] == 3


def test_approval_reject_wrong_level():
    pid = _new_draft_project()
    client.post(f"/api/v1/projects/{pid}/submit", json={})
    r = client.post(f"/api/v1/projects/{pid}/approve", json={"level": "L2"})
    assert r.status_code == 400


def test_approval_reject_flow():
    pid = _new_draft_project()
    client.post(f"/api/v1/projects/{pid}/submit", json={"approval_chain": ["L3"]})
    r = client.post(f"/api/v1/projects/{pid}/reject", json={"level": "L3", "reason": "预算不足"})
    assert r.status_code == 200
    assert r.json()["status"] == "rejected"
    assert "预算" in r.json()["approval"]["reject_reason"]


def test_pending_approvals_not_shadowed_by_project_id():
    """pending-approvals 不得被 /projects/{id} 误匹配（路由顺序）。"""
    r = client.get("/api/v1/projects/pending-approvals")
    assert r.status_code == 200
    assert "items" in r.json()
