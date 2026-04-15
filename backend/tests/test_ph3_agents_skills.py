from fastapi.testclient import TestClient

from app.api import ceo_router
from app.main import app


client = TestClient(app)

_LAW_MIN = ["LAW-04", "LAW-05"]


def test_ceo_planning_project_mgmt_intent():
    r = client.post(
        "/api/v1/ceo/planning",
        json={
            "instruction": "检查项目进度并安排下周里程碑评审",
            "environment": "dev",
            "law": _LAW_MIN,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["intent"]["primary"] == "project_mgmt"
    assert len(body["subtasks"]) >= 2
    first = body["subtasks"][0]
    assert set(["title", "suggested_domain", "priority", "kind", "context"]).issubset(first.keys())
    assert first["suggested_domain"] in {"D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08"}
    assert first["priority"] in {"P0", "P1", "P2", "P3"}
    assert "explainability" in body
    assert "matched_keywords" in body["intent"]
    assert isinstance(body["intent"]["matched_keywords"], list)
    assert "scores" in body["intent"]


def test_ceo_planning_with_project_context():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "Ctx",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning",
        json={
            "instruction": "推进开发",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW_MIN,
        },
    )
    assert r.status_code == 200
    assert r.json()["resources"]["project_id"] == pid


def test_ceo_planning_normalizes_invalid_suggested_domain():
    old_plan = ceo_router.ceo_plan

    def fake_plan(_instruction: str, _project: dict | None = None) -> dict:
        return {
            "intent": {"primary": "project_mgmt", "labels": ["project_mgmt"], "confidence": 0.8},
            "subtasks": [
                {
                    "title": "非法域兜底任务",
                    "suggested_domain": "D99",
                    "priority": "P1",
                    "kind": "plan",
                    "context": "x",
                }
            ],
            "resources": {"suggested_roles": ["L1-CEO"], "project_name": None, "project_id": None},
            "rationale": "test",
            "explainability": {"rule_set": "test", "signals": []},
        }

    ceo_router.ceo_plan = fake_plan
    try:
        r = client.post(
            "/api/v1/ceo/planning",
            json={
                "instruction": "任意",
                "environment": "dev",
                "law": _LAW_MIN,
            },
        )
    finally:
        ceo_router.ceo_plan = old_plan

    assert r.status_code == 200
    assert r.json()["subtasks"][0]["suggested_domain"] == "D03"


def test_ceo_planning_engineering_performance_adds_perf_task():
    r = client.post(
        "/api/v1/ceo/planning",
        json={
            "instruction": "优化接口性能并安排回归",
            "environment": "dev",
            "law": _LAW_MIN,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["intent"]["primary"] == "engineering"
    names = [x["title"] for x in body["subtasks"]]
    assert "建立性能基线与回归阈值" in names


def test_ceo_planning_multi_intent_mixes_secondary_task():
    r = client.post(
        "/api/v1/ceo/planning",
        json={
            "instruction": "推进项目里程碑进度，并同步营销投放策略",
            "environment": "dev",
            "law": _LAW_MIN,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["intent"]["primary"] == "project_mgmt"
    assert "marketing" in body["intent"]["labels"]
    assert len(body["subtasks"]) >= 4
    secondary = [x for x in body["subtasks"] if x.get("source_intent") == "marketing"]
    assert secondary


def test_skills_crud_and_link_agent():
    aid = client.get("/api/v1/agents").json()["items"][0]["id"]
    r = client.post(
        "/api/v1/skills",
        json={
            "name": "FastAPI 路由",
            "category": "backend",
            "level": "senior",
            "linked_agent_ids": [aid],
        },
    )
    assert r.status_code == 201
    sid = r.json()["id"]
    lst = client.get("/api/v1/skills", params={"category": "backend"})
    assert any(x["id"] == sid for x in lst.json()["items"])
    u = client.put(f"/api/v1/skills/{sid}", json={"description": "掌握依赖注入"})
    assert u.status_code == 200
    assert u.json()["description"] == "掌握依赖注入"
    assert client.delete(f"/api/v1/skills/{sid}").status_code == 204


def test_delegation_and_working_memory():
    agents = client.get("/api/v1/agents").json()["items"]
    assert len(agents) >= 1
    if len(agents) >= 2:
        from_id, to_id = agents[0]["id"], agents[1]["id"]
    else:
        # 旧 state.json 可能仅有单智能体：退化为自委托以验证存储与接口
        from_id = to_id = agents[0]["id"]
    d = client.post(
        "/api/v1/collaboration/delegations",
        json={
            "from_agent_id": from_id,
            "to_agent_id": to_id,
            "objective": "协调 D02 资源",
            "contract": {
                "acceptance_criteria": "完成跨部门协调并同步结果",
                "deliverables": ["协作结论纪要", "风险清单"],
                "due_date": None,
            },
        },
    )
    assert d.status_code == 201
    lid = d.json()["id"]
    assert d.json()["contract"]["acceptance_criteria"] == "完成跨部门协调并同步结果"
    assert len(d.json()["contract"]["deliverables"]) == 2
    miss = client.post(
        "/api/v1/collaboration/delegations",
        json={"from_agent_id": from_id, "to_agent_id": to_id, "objective": "缺契约应失败"},
    )
    assert miss.status_code == 422
    one = client.get(f"/api/v1/collaboration/delegations/{lid}")
    assert one.status_code == 200
    assert one.json()["id"] == lid
    miss_get = client.get("/api/v1/collaboration/delegations/dlg-missing-zzzz")
    assert miss_get.status_code == 404
    assert miss_get.json()["detail"]["error_code"] == "DELEGATION_NOT_FOUND"
    q = client.get("/api/v1/collaboration/delegations", params={"from_agent_id": from_id, "limit": 500})
    assert any(x["id"] == lid for x in q.json()["items"])

    pa = client.patch(f"/api/v1/collaboration/delegations/{lid}", json={"status": "accepted"})
    assert pa.status_code == 200
    assert pa.json()["status"] == "accepted"
    pd = client.patch(f"/api/v1/collaboration/delegations/{lid}", json={"status": "done"})
    assert pd.status_code == 200
    assert pd.json()["status"] == "done"
    miss_patch = client.patch("/api/v1/collaboration/delegations/dlg-not-exists-xxx", json={"status": "open"})
    assert miss_patch.status_code == 404
    assert miss_patch.json()["detail"]["error_code"] == "DELEGATION_NOT_FOUND"
    assert client.patch(f"/api/v1/collaboration/delegations/{lid}", json={"status": "bogus"}).status_code == 422

    miss_del = client.delete("/api/v1/collaboration/delegations/dlg-not-exists-del")
    assert miss_del.status_code == 404
    assert miss_del.json()["detail"]["error_code"] == "DELEGATION_NOT_FOUND"
    de = client.delete(f"/api/v1/collaboration/delegations/{lid}")
    assert de.status_code == 204
    assert client.get(f"/api/v1/collaboration/delegations/{lid}").status_code == 404

    evs = client.get("/api/v1/audit/events", params={"limit": 500}).json()["events"]
    related = [e for e in evs if lid in e.get("reason", "")]
    et = {e["event_type"] for e in related}
    assert "delegation.create" in et
    assert "delegation.patch" in et
    assert "delegation.delete" in et

    wm = client.post(
        f"/api/v1/agents/{from_id}/memory/working",
        json={"content": "记住：优先处理审批队列"},
    )
    assert wm.status_code == 201
    hist = client.get(f"/api/v1/agents/{from_id}/memory/working")
    assert hist.status_code == 200
    assert any("审批" in x["content"] for x in hist.json()["items"])
