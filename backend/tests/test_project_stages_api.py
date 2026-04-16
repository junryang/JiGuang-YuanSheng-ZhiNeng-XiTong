from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_project_stages_end_to_end():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-demo",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/stages")
    assert r.status_code == 200
    stages = r.json()
    assert isinstance(stages, list)
    assert len(stages) == 9
    assert stages[0]["id"] == "P01"
    assert stages[0]["status"] == "pending"
    assert stages[0]["deliverables"][0]["template"] == "market_analysis_report_template.md"
    assert isinstance(stages[0]["deliverables"][0].get("schema"), (dict, type(None)))
    assert isinstance(stages[0]["participants"], list)
    assert len(stages[0]["participants"]) >= 2
    assert any(p.get("role") == "营销主管" for p in stages[0]["participants"])
    # 条件审批：P04 预算不超限时，实际审批人为默认 CEO
    p04 = next(s for s in stages if s.get("id") == "P04")
    assert p04["approval"]["approver_role"] == "CEO"
    assert p04["approval"]["approver_level"] == "L1"

    upd = client.put(f"/api/v1/projects/{pid}", json={"budget": 200000})
    assert upd.status_code == 200
    stages2 = client.get(f"/api/v1/projects/{pid}/stages").json()
    p04b = next(s for s in stages2 if s.get("id") == "P04")
    assert p04b["approval"]["approver_role"] == "老板"
    assert p04b["approval"]["approver_level"] == "L0"

    s1 = client.post(f"/api/v1/projects/{pid}/stages/P01/start")
    assert s1.status_code == 200
    assert s1.json()["stage"]["status"] == "in_progress"

    c1 = client.post(
        f"/api/v1/projects/{pid}/stages/P01/complete",
        json={"deliverables": [{"name": "市场分析报告", "content_text": "ok"}], "comments": "done"},
    )
    assert c1.status_code == 200
    # P01 在规范中要求审批；complete 后进入 review，approve 后才推进下一阶段
    assert c1.json()["stage"]["status"] == "review"

    p2 = client.get(f"/api/v1/projects/{pid}/stages/P02")
    assert p2.status_code == 200
    assert p2.json()["status"] == "pending"

    a1 = client.post(
        f"/api/v1/projects/{pid}/stages/P01/approve",
        json={"approved": True, "comments": "approved", "approver_role": "总经理", "approver_level": "L2"},
    )
    assert a1.status_code == 200
    assert a1.json()["stage"]["status"] == "approved"
    assert isinstance(a1.json()["stage"].get("approval_history"), list)
    assert len(a1.json()["stage"]["approval_history"]) >= 1

    bad_ap = client.post(
        f"/api/v1/projects/{pid}/stages/P01/approve",
        json={"approved": True, "comments": "bad", "approver_role": "老板", "approver_level": "L0"},
    )
    assert bad_ap.status_code == 400
    assert bad_ap.json()["detail"]["error_code"] == "APPROVER_MISMATCH"

    bad_half = client.post(
        f"/api/v1/projects/{pid}/stages/P01/approve",
        json={"approved": True, "comments": "half", "approver_role": "总经理"},
    )
    assert bad_half.status_code == 400
    assert bad_half.json()["detail"]["error_code"] == "APPROVER_ID_INCOMPLETE"

    p2b = client.get(f"/api/v1/projects/{pid}/stages/P02")
    assert p2b.status_code == 200
    assert p2b.json()["status"] == "in_progress"

    ev = client.get(
        "/api/v1/audit/events",
        params={"event_type_prefix": "project_stage_", "limit": 50},
    )
    assert ev.status_code == 200
    events = ev.json()["events"]
    assert any(e.get("event_type") == "project_stage_start" for e in events)
    assert any(e.get("event_type") == "project_stage_complete" for e in events)
    assert any(e.get("event_type") == "project_stage_approve" for e in events)
    # 任一事件须携带 project_id/stage_id 便于追溯
    assert any((e.get("context") or {}).get("project_id") == pid for e in events)
    assert any((e.get("context") or {}).get("stage_id") == "P01" for e in events)

    disc = client.get(f"/api/v1/projects/{pid}/discussion")
    assert disc.status_code == 200
    items = disc.json()["items"]
    assert any("[STAGE_APPROVAL]" in str(x.get("body", "")) and "stage_id=P01" in str(x.get("body", "")) for x in items)


def test_project_stage_complete_requires_required_deliverables():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-demo-2",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    pid = p.json()["id"]

    s1 = client.post(f"/api/v1/projects/{pid}/stages/P01/start")
    assert s1.status_code == 200

    # 缺少必需交付物：市场分析报告
    c1 = client.post(
        f"/api/v1/projects/{pid}/stages/P01/complete",
        json={"deliverables": [{"name": "不存在的交付物"}]},
    )
    assert c1.status_code == 400


def test_stage_approve_requires_approver_identity_in_staging():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-staging-approver",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]

    # 切到 staging 以触发“审批人身份强制”
    u = client.put(f"/api/v1/projects/{pid}", json={"environment": "staging"})
    assert u.status_code == 200

    s1 = client.post(f"/api/v1/projects/{pid}/stages/P01/start")
    assert s1.status_code == 200
    c1 = client.post(
        f"/api/v1/projects/{pid}/stages/P01/complete",
        json={"deliverables": [{"name": "市场分析报告", "content_text": "ok"}]},
    )
    assert c1.status_code == 200
    assert c1.json()["stage"]["status"] == "review"

    bad = client.post(
        f"/api/v1/projects/{pid}/stages/P01/approve",
        json={"approved": True, "comments": "missing approver id"},
    )
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "APPROVER_ID_REQUIRED"

    ok = client.post(
        f"/api/v1/projects/{pid}/stages/P01/approve",
        json={"approved": True, "comments": "ok", "approver_role": "总经理", "approver_level": "L2"},
    )
    assert ok.status_code == 200


def test_project_stage_deliverable_upload_replaces_same_name_and_rejects_unknown():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-demo-3",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]

    s1 = client.post(f"/api/v1/projects/{pid}/stages/P01/start")
    assert s1.status_code == 200

    up1 = client.post(
        f"/api/v1/projects/{pid}/stages/P01/deliverables/%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A",
        json={"name": "ignored-by-path", "type": "document", "content_text": "v1"},
    )
    assert up1.status_code == 200
    assert up1.json()["deliverable"]["name"] == "市场分析报告"

    up2 = client.post(
        f"/api/v1/projects/{pid}/stages/P01/deliverables/%E5%B8%82%E5%9C%BA%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A",
        json={"name": "ignored-by-path", "type": "document", "content_text": "v2"},
    )
    assert up2.status_code == 200

    listed = client.get(f"/api/v1/projects/{pid}/stages/P01/deliverables")
    assert listed.status_code == 200
    items = listed.json()["items"]
    assert len(items) == 1
    assert items[0]["name"] == "市场分析报告"
    assert items[0]["content_text"] == "v2"

    bad = client.post(
        f"/api/v1/projects/{pid}/stages/P01/deliverables/%E4%B8%8D%E5%AD%98%E5%9C%A8%E7%9A%84%E4%BA%A4%E4%BB%98%E7%89%A9",
        json={"name": "x", "type": "document", "content_text": "bad"},
    )
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "UNKNOWN_DELIVERABLE"


def test_project_stages_timeline_endpoint_basic_shape():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-timeline",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]

    tl = client.get(f"/api/v1/projects/{pid}/stages/timeline")
    assert tl.status_code == 200
    body = tl.json()
    assert body["project_id"] == pid
    assert isinstance(body["items"], list)
    assert body["total"] == 9
    assert len(body["items"]) == 9
    assert body["items"][0]["stage_id"] == "P01"
    assert body["items"][0]["order"] == 1
    assert body["items"][0]["start_date"] is None
    assert body["items"][0]["end_date"] is None
    assert body["items"][0]["duration_minutes"] is None


def test_project_stages_health_endpoint_basic_shape():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-health",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]

    r = client.get(f"/api/v1/projects/{pid}/stages/health")
    assert r.status_code == 200
    body = r.json()
    assert body["project_id"] == pid
    assert isinstance(body["current_stage"], dict)
    assert body["current_stage"]["stage_id"] == "P01"
    assert body["stage_timeout_minutes"] > 0
    assert body["approval_timeout_minutes"] is None
    assert body["stage_overdue"] in (True, False)
    assert body["approval_overdue"] in (True, False)


def test_project_stage_timeout_alert_check_endpoint_force_and_cooldown_dedupe():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-timeout-alert",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]

    r1 = client.post(f"/api/v1/projects/{pid}/stages/health/check?force=true&cooldown_minutes=30")
    assert r1.status_code == 200
    body1 = r1.json()
    assert body1["status"] == "emitted"
    assert body1["emitted"] is True
    assert isinstance(body1.get("thresholds"), dict)
    assert isinstance(body1.get("hits"), dict)
    assert "stage_overdue_threshold_minutes" in body1["thresholds"]
    assert "approval_overdue_threshold_minutes" in body1["thresholds"]

    # second call within cooldown should be skipped (dedupe)
    r2 = client.post(f"/api/v1/projects/{pid}/stages/health/check?force=true&cooldown_minutes=30")
    assert r2.status_code == 200
    body2 = r2.json()
    assert body2["status"] == "skipped"
    assert body2["emitted"] is False
    assert body2["reason_code"] == "COOLDOWN_ACTIVE"
    assert isinstance(body2.get("thresholds"), dict)
    assert isinstance(body2.get("hits"), dict)

    disc = client.get(f"/api/v1/projects/{pid}/discussion")
    assert disc.status_code == 200
    items = disc.json()["items"]
    assert sum(1 for x in items if "[STAGE_TIMEOUT_ALERT]" in str(x.get("body", ""))) == 1

    ev = client.get(
        "/api/v1/audit/events",
        params={"event_type_prefix": "project_stage_timeout_alert", "limit": 50},
    )
    assert ev.status_code == 200
    events = ev.json()["events"]
    assert any((e.get("context") or {}).get("project_id") == pid for e in events)


def test_project_stage_timeout_alert_force_not_allowed_in_staging():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-timeout-alert-staging",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]
    u = client.put(f"/api/v1/projects/{pid}", json={"environment": "staging"})
    assert u.status_code == 200

    r = client.post(f"/api/v1/projects/{pid}/stages/health/check?force=true")
    assert r.status_code == 400
    assert r.json()["detail"]["error_code"] == "FORCE_NOT_ALLOWED"


def test_project_stage_timeout_alert_respects_overdue_threshold_minutes():
    p = client.post(
        "/api/v1/projects",
        json={
            "name": "stages-timeout-threshold",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert p.status_code == 200
    pid = p.json()["id"]

    # Make P01 in progress and clearly overdue by setting start_date far in the past.
    from datetime import datetime, timedelta, timezone

    stages = client.get(f"/api/v1/projects/{pid}/stages").json()
    p01 = next(s for s in stages if s.get("id") == "P01")
    p01["status"] = "in_progress"
    p01["start_date"] = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    # Update stages directly in store (UpdateProjectRequest does not accept stages patch).
    from app.core.deps import get_json_store

    store = get_json_store()
    store.update_project(pid, {"stages": stages})

    h = client.get(f"/api/v1/projects/{pid}/stages/health").json()
    assert h["current_stage"]["stage_id"] == "P01"
    assert h["stage_overdue"] is True
    assert h["stage_overdue_minutes"] is not None

    # Threshold higher than overdue -> treated as not overdue -> no alert
    r1 = client.post(
        f"/api/v1/projects/{pid}/stages/health/check?stage_overdue_threshold_minutes=50000&cooldown_minutes=0"
    )
    assert r1.status_code == 200
    assert r1.json()["status"] == "no_alert"
    assert r1.json()["hits"]["stage_overdue_hit"] is False
    assert r1.json()["thresholds"]["stage_overdue_threshold_minutes"] == 50000

    # Low threshold -> emit
    r2 = client.post(
        f"/api/v1/projects/{pid}/stages/health/check?stage_overdue_threshold_minutes=1&cooldown_minutes=30"
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "emitted"
    assert r2.json()["hits"]["stage_overdue_hit"] is True
    assert r2.json()["thresholds"]["stage_overdue_threshold_minutes"] == 1

