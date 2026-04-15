from datetime import date

from fastapi.testclient import TestClient

from app.main import app
from app.api.routes import _risk_alert_cooldown_minutes, _risk_alert_trigger_score
from app.services.progress_service import project_risk_summary, weighted_progress_percent


client = TestClient(app)


def test_weighted_progress_formula():
    tasks = [
        {"progress": 100, "estimated_hours": 10, "status": "in_progress"},
        {"progress": 0, "estimated_hours": 10, "status": "pending"},
    ]
    pct, meta = weighted_progress_percent(tasks)
    assert abs(pct - 50.0) < 0.01
    assert meta["denominator"] == 20.0


def test_completed_task_counts_as_100_progress():
    tasks = [{"progress": 0, "estimated_hours": 5, "status": "completed"}]
    pct, _ = weighted_progress_percent(tasks)
    assert pct == 100.0


def test_project_progress_and_gantt():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "进度甘特",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "A",
            "progress": 80,
            "estimated_hours": 2,
            "start_date": "2026-04-01",
            "end_date": "2026-04-10",
        },
    )
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "B",
            "progress": 20,
            "estimated_hours": 8,
            "status": "in_progress",
        },
    )

    pr = client.get(f"/api/v1/projects/{pid}/progress")
    assert pr.status_code == 200
    body = pr.json()
    assert body["task_count"] == 2
    # (80*2 + 20*8) / 10 = 320/10 = 32
    assert abs(body["overall_progress"] - 32.0) < 0.1
    assert "risk_summary" in body
    assert body["risk_summary"]["risk_level"] in {"low", "medium", "high"}
    assert body["risk_summary"]["blocked_task_count"] == 0
    assert body["risk_alert_triggered"] is False
    assert "risk_alert_state" in body
    assert "cooldown_minutes" in body["risk_alert_state"]

    gg = client.get(f"/api/v1/projects/{pid}/gantt")
    assert gg.status_code == 200
    names = {t["name"] for t in gg.json()["tasks"]}
    assert names == {"A", "B"}
    a = next(t for t in gg.json()["tasks"] if t["name"] == "A")
    assert a["start_date"] == "2026-04-01"


def test_put_project_milestones_shown_in_progress():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "里程碑",
            "domain": "D03",
            "project_type": "optimization",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    ms = [{"id": "m1", "name": "联调", "target_date": "2026-05-01", "done": False}]
    u = client.put(f"/api/v1/projects/{pid}", json={"milestones": ms})
    assert u.status_code == 200
    pr = client.get(f"/api/v1/projects/{pid}/progress")
    assert pr.json()["milestones"][0]["name"] == "联调"


def test_project_risk_summary_counts_and_level():
    summary = project_risk_summary(
        [
            {"status": "blocked", "progress": 10, "end_date": "2026-04-01"},
            {"status": "in_progress", "progress": 0, "end_date": "2026-03-01"},
            {"status": "pending", "progress": 0, "end_date": "2026-02-01"},
            {"status": "completed", "progress": 100, "end_date": "2026-01-01"},
        ],
        today=date(2026, 4, 15),
    )
    assert summary["blocked_task_count"] == 1
    assert summary["overdue_task_count"] == 3
    assert summary["no_progress_in_progress_count"] == 1
    assert summary["risk_score"] == 10
    assert summary["risk_level"] == "high"


def test_project_progress_high_risk_triggers_alert_once():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "高风险项目",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "blocked-task",
            "status": "blocked",
            "progress": 10,
            "end_date": "2026-01-01",
        },
    )
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "overdue-in-progress",
            "status": "in_progress",
            "progress": 0,
            "end_date": "2026-01-01",
        },
    )

    first = client.get(f"/api/v1/projects/{pid}/progress")
    assert first.status_code == 200
    body1 = first.json()
    assert body1["risk_summary"]["risk_level"] == "high"
    assert body1["risk_alert_triggered"] is True
    assert body1["risk_alert_state"]["last_alert_at"] is not None
    assert body1["risk_alert_state"]["next_eligible_at"] is not None

    discussion = client.get(f"/api/v1/projects/{pid}/discussion")
    assert discussion.status_code == 200
    assert any("[PROJECT_RISK_ALERT]" in x["body"] for x in discussion.json()["items"])

    second = client.get(f"/api/v1/projects/{pid}/progress")
    assert second.status_code == 200
    body2 = second.json()
    assert body2["risk_summary"]["risk_level"] == "high"
    assert body2["risk_alert_triggered"] is False
    assert body2["risk_alert_state"]["cooldown_active"] in {True, False}

    audit = client.get("/api/v1/audit/events", params={"event_type_prefix": "project_risk_alert", "limit": 50})
    assert audit.status_code == 200
    events = audit.json()["events"]
    assert any(e["event_type"] == "project_risk_alert" for e in events)


def test_risk_alert_cooldown_minutes_uses_policy_and_fallback():
    class _Engine:
        def __init__(self, block):
            self._block = block

        def get_environment_policy(self, _environment):
            return self._block

    assert _risk_alert_cooldown_minutes(_Engine({"risk_alert_cooldown_minutes": 12}), "dev") == 12
    assert _risk_alert_cooldown_minutes(_Engine({"risk_alert_cooldown_minutes": "x"}), "dev") == 30
    assert _risk_alert_cooldown_minutes(_Engine({"risk_alert_cooldown_minutes": -5}), "dev") == 0


def test_risk_alert_trigger_score_uses_policy_and_fallback():
    class _Engine:
        def __init__(self, block):
            self._block = block

        def get_environment_policy(self, _environment):
            return self._block

    assert _risk_alert_trigger_score(_Engine({"risk_alert_trigger_score": 8}), "dev") == 8
    assert _risk_alert_trigger_score(_Engine({"risk_alert_trigger_score": "x"}), "dev") == 6
    assert _risk_alert_trigger_score(_Engine({"risk_alert_trigger_score": -2}), "dev") == 0


def test_project_overview_aggregates_progress_risk_team_and_discussion():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "项目概览聚合",
            "domain": "D03",
            "project_type": "optimization",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "team-task-1",
            "status": "in_progress",
            "progress": 50,
            "estimated_hours": 4,
            "assignee_level": "L3",
            "assignee_role": "PM",
        },
    )
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "team-task-2",
            "status": "completed",
            "progress": 0,
            "estimated_hours": 2,
            "assignee_level": "L3",
            "assignee_role": "PM",
        },
    )
    d = client.post(
        f"/api/v1/projects/{pid}/discussion",
        json={"author": "qa", "body": "overview check"},
    )
    assert d.status_code == 201

    r = client.get(f"/api/v1/projects/{pid}/overview")
    assert r.status_code == 200
    body = r.json()
    assert body["project"]["id"] == pid
    assert body["progress"]["task_count"] == 2
    assert body["progress"]["completed_task_count"] == 1
    assert body["risk_summary"]["risk_level"] in {"low", "medium", "high"}
    assert body["risk_alert_state"]["cooldown_minutes"] >= 0
    assert "risk_alert_history" in body
    assert isinstance(body["risk_alert_history"], list)
    assert "risk_alert_history_pagination" in body
    assert "offset" in body["risk_alert_history_pagination"]
    assert "limit" in body["risk_alert_history_pagination"]
    assert body["team"]["member_group_count"] >= 1
    assert len(body["discussion"]["recent_items"]) >= 1


def test_project_overview_includes_risk_alert_history():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "概览风险历史",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "blocked-history",
            "status": "blocked",
            "progress": 0,
            "end_date": "2026-01-01",
        },
    )
    client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "overdue-history",
            "status": "in_progress",
            "progress": 0,
            "end_date": "2026-01-01",
        },
    )
    trigger = client.get(f"/api/v1/projects/{pid}/progress")
    assert trigger.status_code == 200
    assert trigger.json()["risk_alert_triggered"] is True

    ov = client.get(f"/api/v1/projects/{pid}/overview")
    assert ov.status_code == 200
    history = ov.json()["risk_alert_history"]
    assert len(history) >= 1
    assert "[PROJECT_RISK_ALERT]" in history[0]["body"]
    assert "parsed" in history[0]
    parsed = history[0]["parsed"]
    assert parsed["raw_fields_valid"] is True
    assert parsed["parse_error_code"] == "OK"
    assert parsed["risk_score"] >= 0
    assert parsed["risk_level"] in {"low", "medium", "high"}
    assert parsed["blocked_task_count"] >= 0
    assert parsed["overdue_task_count"] >= 0
    assert parsed["no_progress_in_progress_count"] >= 0
    assert "cooldown_snapshot" in history[0]
    cooldown = history[0]["cooldown_snapshot"]
    assert cooldown["cooldown_minutes"] >= 0
    assert cooldown["cooldown_start_at"] is not None
    assert cooldown["cooldown_end_at"] is not None


def test_risk_alert_body_parse_fallback_marks_invalid():
    from app.api.routes import _parse_risk_alert_body

    parsed = _parse_risk_alert_body("not-a-risk-alert-body")
    assert parsed["raw_fields_valid"] is False
    assert parsed["parse_error_code"] == "PATTERN_MISMATCH"


def test_project_overview_respects_risk_alert_limit():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "limit-case",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "t1", "status": "blocked", "progress": 0, "end_date": "2026-01-01"},
    )
    client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "t2", "status": "in_progress", "progress": 0, "end_date": "2026-01-01"},
    )
    client.get(f"/api/v1/projects/{pid}/progress")
    client.post(f"/api/v1/projects/{pid}/discussion", json={"author": "bot", "body": "[PROJECT_RISK_ALERT] project=x; risk_score=9; blocked=1; overdue=1; stalled=1; action=review_risk_board_and_assign_owner"})

    r = client.get(f"/api/v1/projects/{pid}/overview", params={"risk_alert_limit": 1})
    assert r.status_code == 200
    history = r.json()["risk_alert_history"]
    assert len(history) == 1
    assert r.json()["risk_alert_history_returned_count"] == 1
    assert r.json()["risk_alert_history_page_size"] == 1
    assert r.json()["risk_alert_history_total"] >= 2
    assert isinstance(r.json()["risk_alert_history_has_more"], bool)
    assert r.json()["risk_alert_history_has_more"] is True
    assert isinstance(r.json()["risk_alert_history_next_offset"], int)
    assert r.json()["risk_alert_history_prev_offset"] is None

    r2 = client.get(
        f"/api/v1/projects/{pid}/overview",
        params={"risk_alert_limit": 1, "risk_alert_history_offset": 1},
    )
    assert r2.status_code == 200
    history2 = r2.json()["risk_alert_history"]
    assert len(history2) == 1
    assert r2.json()["risk_alert_history_returned_count"] == 1
    assert history2[0]["id"] != history[0]["id"]
    assert isinstance(r2.json()["risk_alert_history_has_more"], bool)
    assert isinstance(r2.json()["risk_alert_history_prev_offset"], int)

    r3 = client.get(
        f"/api/v1/projects/{pid}/overview",
        params={"risk_alert_limit": 10, "risk_alert_history_offset": 0},
    )
    assert r3.status_code == 200
    assert r3.json()["risk_alert_history_returned_count"] == len(r3.json()["risk_alert_history"])
    assert r3.json()["risk_alert_history_has_more"] in {True, False}
    if r3.json()["risk_alert_history_has_more"] is False:
        assert r3.json()["risk_alert_history_next_offset"] is None
