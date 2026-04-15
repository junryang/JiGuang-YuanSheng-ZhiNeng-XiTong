from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthz():
    resp = client.get("/healthz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["policy_engine"]["loaded"] is True


def test_openapi_docs_and_redoc():
    d = client.get("/docs")
    assert d.status_code == 200
    assert b"swagger" in d.content.lower() or b"openapi" in d.content.lower()
    r = client.get("/redoc")
    assert r.status_code == 200


def test_core_routes():
    ag = client.get("/api/v1/agents")
    assert ag.status_code == 200
    body = ag.json()
    assert "items" in body and "total" in body
    assert client.get("/api/v1/projects").status_code == 200
    s = client.post("/api/v1/chat/sessions", json={"title": "day1"})
    assert s.status_code == 200
    sid = s.json()["id"]
    m = client.post(
        f"/api/v1/chat/sessions/{sid}/messages",
        json={"message": "hello", "environment": "dev", "law": ["LAW-05"]},
    )
    assert m.status_code == 200


def test_policy_rejects_missing_law_04():
    resp = client.post(
        "/api/v1/policy/evaluate",
        json={
            "policy_id": "CEO-POLICY-13",
            "environment": "prod",
            "context": {"law": ["LAW-01", "LAW-02", "LAW-03", "LAW-05"]},
        },
    )
    assert resp.status_code == 403
    assert resp.json()["detail"]["error_code"] in {"LAW_04_REQUIRED", "LAW_BUNDLE_REQUIRED"}


def test_high_risk_publish_requires_full_law_chain():
    resp = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "x",
            "content": "y",
            "environment": "staging",
            "law": ["LAW-01", "LAW-02", "LAW-03", "LAW-05"],
            "approved": True,
        },
    )
    assert resp.status_code == 403


def test_degraded_mode_blocks_high_risk_publish():
    mode = client.post("/api/v1/runtime/mode", json={"mode": "degraded"})
    assert mode.status_code == 200

    resp = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "x",
            "content": "y",
            "environment": "prod",
            "law": ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"],
            "approved": True,
        },
    )
    assert resp.status_code == 403

    restore = client.post("/api/v1/runtime/mode", json={"mode": "normal"})
    assert restore.status_code == 200


def test_runtime_mode_rejects_invalid_value():
    r = client.post("/api/v1/runtime/mode", json={"mode": "safe"})
    assert r.status_code == 422


def test_prod_publish_requires_approval():
    resp = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "x",
            "content": "y",
            "environment": "prod",
            "law": ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"],
            "approved": False,
        },
    )
    assert resp.status_code == 403
    assert resp.json()["detail"]["error_code"] == "PROD_APPROVAL_REQUIRED"


def test_staging_publish_requires_approval():
    resp = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "x",
            "content": "y",
            "environment": "staging",
            "law": ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"],
            "approved": False,
        },
    )
    assert resp.status_code == 403
    assert resp.json()["detail"]["error_code"] == "STAGING_APPROVAL_REQUIRED"


def test_publish_success_and_audit_events_available():
    resp = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "ok",
            "content": "ok",
            "environment": "prod",
            "law": ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"],
            "approved": True,
        },
    )
    assert resp.status_code == 200

    audit = client.get("/api/v1/audit/events")
    assert audit.status_code == 200
    events = audit.json()["events"]
    assert len(events) > 0
    assert "policy_id" in events[-1]
    assert "policy_version" in events[-1]
    assert "environment" in events[-1]
    assert "reason" in events[-1]
    assert "reason_code" in events[-1]
    assert "context" in events[-1]


def test_audit_events_filters_by_event_type_prefix():
    agents = client.get("/api/v1/agents").json()["items"]
    assert len(agents) >= 1
    aid = agents[0]["id"]
    d = client.post(
        "/api/v1/collaboration/delegations",
        json={
            "from_agent_id": aid,
            "to_agent_id": aid,
            "objective": "audit prefix filter",
            "contract": {
                "acceptance_criteria": "完成审计前缀过滤验证",
                "deliverables": ["过滤结果截图"],
                "due_date": None,
            },
        },
    )
    assert d.status_code == 201

    r = client.get("/api/v1/audit/events", params={"event_type_prefix": "delegation", "limit": 80})
    assert r.status_code == 200
    evs = r.json()["events"]
    assert evs
    assert all(str(e.get("event_type", "")).startswith("delegation") for e in evs)
    assert all(str(e.get("policy_id", "")) == "collaboration" for e in evs)
    assert all(str(e.get("environment", "")) == "dev" for e in evs)

    rp = client.get("/api/v1/audit/events", params={"policy_id": "collaboration", "limit": 80})
    assert rp.status_code == 200
    evs_p = rp.json()["events"]
    assert evs_p
    assert all(str(e.get("policy_id", "")) == "collaboration" for e in evs_p)

    re = client.get("/api/v1/audit/events", params={"environment": "dev", "limit": 80})
    assert re.status_code == 200
    evs_e = re.json()["events"]
    assert evs_e
    assert all(str(e.get("environment", "")) == "dev" for e in evs_e)

    r2 = client.get("/api/v1/audit/events", params={"event_type_prefix": "no_such_prefix_xyz", "limit": 20})
    assert r2.status_code == 200
    assert r2.json()["events"] == []


def test_audit_summary_has_trend_and_top_reasons():
    # 先制造一条拒绝审计事件（便于 top_reasons 非空）
    _ = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "audit summary seed",
            "content": "x",
            "environment": "prod",
            "law": ["LAW-05"],
            "approved": False,
        },
    )
    r = client.get("/api/v1/audit/summary", params={"days": 7, "top_limit": 5})
    assert r.status_code == 200
    j = r.json()
    assert j["days"] == 7
    assert "trend" in j and isinstance(j["trend"], list)
    assert len(j["trend"]) == 7
    assert "allowed_rate" in j["trend"][0]
    assert "allowed" in j["trend"][0]
    assert "denied" in j["trend"][0]
    assert "top_reasons" in j and isinstance(j["top_reasons"], list)
    assert "total_events" in j
    assert "total_allowed" in j
    assert "total_denied" in j
    assert "allowed_rate" in j
    assert "denied_rate" in j
    if j["top_reasons"]:
        assert "reason_code" in j["top_reasons"][0]
        assert "count" in j["top_reasons"][0]
    r2 = client.get("/api/v1/audit/summary", params={"reason_code_prefix": "LAW_"})
    assert r2.status_code == 200
    j2 = r2.json()
    assert "trend" in j2


def test_collab_error_code_for_missing_delegation():
    miss = client.get("/api/v1/collaboration/delegations/dlg-no-such-id")
    assert miss.status_code == 404
    body = miss.json()
    assert "detail" in body
    assert body["detail"]["error_code"] == "DELEGATION_NOT_FOUND"
    assert "reason" in body["detail"]


def test_project_create_dev_minimal():
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "测试项目",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"].startswith("JYIS-")
    assert data["name"] == "测试项目"

    gid = client.get(f"/api/v1/projects/{data['id']}")
    assert gid.status_code == 200
    assert gid.json()["id"] == data["id"]


def test_project_create_rejects_invalid_domain_and_type():
    bad_domain = client.post(
        "/api/v1/projects",
        json={
            "name": "bad-domain",
            "domain": "D09",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert bad_domain.status_code == 422

    bad_type = client.post(
        "/api/v1/projects",
        json={
            "name": "bad-type",
            "domain": "D03",
            "project_type": "refactor",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert bad_type.status_code == 422


def test_project_create_staging_rejects_incomplete_precheck():
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "s",
            "domain": "D01",
            "project_type": "optimization",
            "environment": "staging",
            "law": ["LAW-05"],
            "acceptance_contract": "CTR-001",
        },
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error_code"] == "STAGING_PRECHECK_INCOMPLETE"


def _staging_yaml_acks_all_true() -> dict:
    snap = client.get("/api/v1/policy/environment/staging")
    assert snap.status_code == 200
    keys = snap.json()["policy"].keys()
    return {k: True for k in keys}


def test_policy_environment_snapshot():
    r = client.get("/api/v1/policy/environment/staging")
    assert r.status_code == 200
    assert "strict_law_bundle" in r.json()["policy"]


def test_policy_environment_snapshot_rejects_invalid_environment():
    r = client.get("/api/v1/policy/environment/uat")
    assert r.status_code == 422


def test_audit_events_rejects_invalid_environment_filter():
    r = client.get("/api/v1/audit/events", params={"environment": "uat"})
    assert r.status_code == 422


def test_project_create_staging_ok():
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "预检通过",
            "domain": "D02",
            "project_type": "bug_fix",
            "environment": "staging",
            "law": ["LAW-04", "LAW-05"],
            "acceptance_contract": "CTR-STG-001",
            "staging_precheck": {
                "owner_confirmed": True,
                "contract_validated": True,
                "rollback_plan_ack": True,
                "audit_trail_ready": True,
                "staging_policy_acks": _staging_yaml_acks_all_true(),
            },
        },
    )
    assert resp.status_code == 200
    assert resp.json()["environment"] == "staging"


def test_project_create_staging_rejects_strict_law_without_law04():
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "law 不足",
            "domain": "D02",
            "project_type": "bug_fix",
            "environment": "staging",
            "law": ["LAW-05"],
            "acceptance_contract": "CTR-X",
            "staging_precheck": {
                "owner_confirmed": True,
                "contract_validated": True,
                "rollback_plan_ack": True,
                "audit_trail_ready": True,
                "staging_policy_acks": _staging_yaml_acks_all_true(),
            },
        },
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error_code"] == "STAGING_STRICT_LAW_BUNDLE"


def test_project_create_staging_rejects_partial_yaml_acks():
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "acks 不全",
            "domain": "D02",
            "project_type": "bug_fix",
            "environment": "staging",
            "law": ["LAW-04", "LAW-05"],
            "acceptance_contract": "CTR-X",
            "staging_precheck": {
                "owner_confirmed": True,
                "contract_validated": True,
                "rollback_plan_ack": True,
                "audit_trail_ready": True,
                "staging_policy_acks": {"strict_law_bundle": True},
            },
        },
    )
    assert resp.status_code == 400
    assert resp.json()["detail"]["error_code"] == "STAGING_POLICY_ACKS_INCOMPLETE"


def test_orchestration_plan_dev():
    r = client.post(
        "/api/v1/orchestration/plans",
        json={
            "name": "probe",
            "steps": ["AGENT-RUNTIME-01", "WEB-04"],
            "environment": "dev",
            "law": ["LAW-04", "LAW-05"],
        },
    )
    assert r.status_code == 200
    assert r.json()["plan_ref"].startswith("plan-")


def test_orchestration_staging_optional_tools_need_approval():
    r = client.post(
        "/api/v1/orchestration/plans",
        json={
            "steps": ["WEB-06"],
            "environment": "staging",
            "law": ["LAW-04", "LAW-05"],
            "use_optional_tools": True,
            "approved": False,
        },
    )
    assert r.status_code == 403
    assert r.json()["detail"]["error_code"] == "OPTIONAL_TOOLS_APPROVAL_REQUIRED"


def test_orchestration_staging_optional_tools_ok_with_approval():
    r = client.post(
        "/api/v1/orchestration/plans",
        json={
            "steps": ["WEB-06"],
            "environment": "staging",
            "law": ["LAW-04", "LAW-05"],
            "use_optional_tools": True,
            "approved": True,
        },
    )
    assert r.status_code == 200


def test_agents_org_tree_and_detail():
    tree = client.get("/api/v1/agents/org-tree")
    assert tree.status_code == 200
    roots = tree.json()["roots"]
    assert isinstance(roots, list)
    if roots:
        assert "children" in roots[0]
        rid = roots[0]["id"]
        d = client.get(f"/api/v1/agents/{rid}")
        assert d.status_code == 200
        assert d.json()["id"] == rid


def test_agents_filter():
    r = client.get("/api/v1/agents", params={"level": "L2"})
    assert r.status_code == 200
    for item in r.json()["items"]:
        assert item["level"] == "L2"


def test_project_update_delete_and_status():
    c = client.post(
        "/api/v1/projects",
        json={
            "name": "生命周期",
            "domain": "D03",
            "project_type": "optimization",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert c.status_code == 200
    pid = c.json()["id"]
    u = client.put(f"/api/v1/projects/{pid}", json={"name": "生命周期改名"})
    assert u.status_code == 200
    assert u.json()["name"] == "生命周期改名"

    bad = client.patch(f"/api/v1/projects/{pid}/status", json={"status": "approved"})
    assert bad.status_code == 400

    invalid = client.patch(f"/api/v1/projects/{pid}/status", json={"status": "archived"})
    assert invalid.status_code == 422

    ok = client.patch(f"/api/v1/projects/{pid}/status", json={"status": "pending_approval"})
    assert ok.status_code == 200

    de = client.delete(f"/api/v1/projects/{pid}")
    assert de.status_code == 204
    assert client.get(f"/api/v1/projects/{pid}").status_code == 404


def test_chat_session_history_persisted():
    s = client.post("/api/v1/chat/sessions", json={"title": "persist"})
    sid = s.json()["id"]
    client.post(
        f"/api/v1/chat/sessions/{sid}/messages",
        json={"message": "stateful", "environment": "dev", "law": ["LAW-05"]},
    )
    history = client.get(f"/api/v1/chat/sessions/{sid}/messages")
    assert history.status_code == 200
    messages = history.json()["messages"]
    assert any(m["role"] == "assistant" for m in messages)


def test_ceo_planning_apply_decision_audit_events():
    create = client.post(
        "/api/v1/projects",
        json={
            "name": "DecisionAudit",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert create.status_code == 200
    pid = create.json()["id"]

    dry_run = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "推进项目里程碑，并同步营销投放策略",
            "project_id": pid,
            "environment": "dev",
            "law": ["LAW-04", "LAW-05"],
            "dry_run": True,
        },
    )
    assert dry_run.status_code == 200
    assert isinstance(dry_run.json().get("decision_log_id"), str)

    applied = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "推进项目里程碑，并同步营销投放策略",
            "project_id": pid,
            "environment": "dev",
            "law": ["LAW-04", "LAW-05"],
            "dry_run": False,
        },
    )
    assert applied.status_code == 200
    assert isinstance(applied.json().get("decision_log_id"), str)

    events_resp = client.get(
        "/api/v1/audit/events",
        params={"event_type_prefix": "ceo_planning_apply_decision", "limit": 200},
    )
    assert events_resp.status_code == 200
    events = events_resp.json()["events"]
    assert len(events) >= 2
    assert all(e["event_type"] == "ceo_planning_apply_decision" for e in events)
    assert all(e["reason_code"] == "DECISION_SNAPSHOT" for e in events)
    assert all(e["policy_id"] == "CEO-POLICY-09" for e in events)
    assert all(e["context"]["ui_priority"] in {"p0", "p1", "p2"} for e in events)
    assert any(bool(e["context"]["dry_run"]) for e in events)
    assert any(not bool(e["context"]["dry_run"]) for e in events)
