from datetime import date

from fastapi.testclient import TestClient

from app.main import app
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
