from fastapi.testclient import TestClient

from app.api import ceo_router
from app.main import app


client = TestClient(app)

_LAW = ["LAW-04", "LAW-05"]


def test_ceo_planning_apply_dry_run():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyDry",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "推进项目进度",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": True,
        },
    )
    assert r.status_code == 200
    assert r.json()["would_create"] >= 1
    assert r.json()["created_tasks"] == []
    assert "would_apply_by_priority" in r.json()
    assert "would_dependency_edges" in r.json()
    assert "would_create_by_intent_source" in r.json()
    assert "would_risk_flags" in r.json()
    assert "would_risk_summary" in r.json()
    assert "would_risk_score" in r.json()
    assert r.json()["risk_alignment"] == "consistent"
    assert r.json()["next_action_hint"] in {
        "READY_TO_APPLY",
        "TUNE_PARAMS_THEN_APPLY",
        "REVIEW_HIGH_RISK_BEFORE_APPLY",
    }
    snap = r.json()["decision_snapshot"]
    assert snap["dry_run"] is True
    assert snap["risk_alignment"] == "consistent"
    assert snap["confidence_band"] in {"low", "medium", "high"}
    assert isinstance(snap["blocking_reasons"], list)
    assert snap["risk_diff"] <= 0
    assert snap["risk_trend"] in {"down", "flat"}
    assert snap["recommended_mode"] in {"apply_now", "dry_run_again", "manual_review"}
    assert snap["ui_priority"] in {"p0", "p1", "p2"}
    assert isinstance(snap["recommended_actions"], list)
    assert len(snap["recommended_actions"]) >= 1
    assert isinstance(r.json()["decision_log_id"], str)
    discussion = client.get(f"/api/v1/projects/{pid}/discussion")
    assert discussion.status_code == 200
    items = discussion.json()["items"]
    assert len(items) >= 1
    assert "[CEO_DECISION][DRY_RUN]" in items[0]["body"]
    assert "recommended_mode=" in items[0]["body"]


def test_ceo_planning_apply_creates_chained_tasks():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyReal",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    before = client.get("/api/v1/tasks", params={"project_id": pid}).json()["total"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
        },
    )
    assert r.status_code == 200
    created = r.json()["created_tasks"]
    assert len(created) >= 2
    after = client.get("/api/v1/tasks", params={"project_id": pid}).json()["total"]
    assert after == before + len(created)
    # 链式依赖：除第一个外应有依赖
    assert any((t.get("dependencies") or []) for t in created)
    assert "applied_by_priority" in r.json()
    assert len(r.json()["created_task_ids"]) == len(created)
    assert all(isinstance(x, str) and x for x in r.json()["created_task_ids"])
    id_map = r.json()["created_task_id_map"]
    assert isinstance(id_map, dict)
    assert len(id_map) == len(created)
    for t in created:
        assert id_map[t["name"]] == t["id"]
    edges = r.json()["applied_dependency_edges"]
    assert isinstance(edges, list)
    assert len(edges) == len(created)
    edge_ids = {e["task_id"] for e in edges}
    assert edge_ids == {t["id"] for t in created}
    assert "applied_by_intent_source" in r.json()
    assert "intent_source_delta" in r.json()
    assert "applied_risk_flags" in r.json()
    assert "applied_risk_summary" in r.json()
    assert "applied_risk_score" in r.json()
    assert r.json()["risk_alignment"] in {"consistent", "drifted"}
    assert r.json()["next_action_hint"] in {"EXECUTION_OK_CONTINUE", "RECHECK_PLAN_AND_RERUN_DRY_RUN"}
    snap = r.json()["decision_snapshot"]
    assert snap["dry_run"] is False
    assert snap["next_action_hint"] == r.json()["next_action_hint"]
    assert snap["confidence_band"] in {"low", "medium", "high"}
    assert isinstance(snap["blocking_reasons"], list)
    assert isinstance(snap["risk_diff"], int)
    assert snap["risk_trend"] in {"up", "down", "flat"}
    assert snap["recommended_mode"] in {"apply_now", "dry_run_again", "manual_review"}
    assert snap["ui_priority"] in {"p0", "p1", "p2"}
    assert isinstance(snap["recommended_actions"], list)
    assert len(snap["recommended_actions"]) >= 1
    assert isinstance(r.json()["decision_log_id"], str)
    discussion = client.get(f"/api/v1/projects/{pid}/discussion")
    assert discussion.status_code == 200
    items = discussion.json()["items"]
    assert len(items) >= 1
    assert "[CEO_DECISION][APPLY]" in items[0]["body"]
    assert "next_action_hint=" in items[0]["body"]


def test_ceo_planning_apply_links_to_latest_existing_task_when_enabled():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyLinkExisting",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    seed = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "seed-task",
            "priority": "P2",
        },
    )
    assert seed.status_code == 201
    seed_id = seed.json()["id"]

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "继续拆解后续执行任务",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "link_to_latest_existing": True,
        },
    )
    assert r.status_code == 200
    created = r.json()["created_tasks"]
    assert len(created) >= 1
    first_deps = created[0].get("dependencies") or []
    assert seed_id in first_deps


def test_ceo_planning_apply_can_start_after_specific_task():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyStartAfter",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    seed = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "manual-anchor-task",
            "priority": "P1",
        },
    )
    assert seed.status_code == 201
    seed_id = seed.json()["id"]

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "start_after_task_id": seed_id,
        },
    )
    assert r.status_code == 200
    created = r.json()["created_tasks"]
    assert len(created) >= 1
    assert seed_id in (created[0].get("dependencies") or [])


def test_ceo_planning_apply_dry_run_dependency_preview_with_start_after_task():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyDryStartAfterPreview",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    seed = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "manual-anchor-task",
            "priority": "P1",
        },
    )
    assert seed.status_code == 201
    seed_id = seed.json()["id"]

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": True,
            "start_after_task_id": seed_id,
            "max_create_tasks": 1,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["would_apply"] == 1
    assert len(body["would_dependency_preview"]) == 1
    assert body["would_dependency_preview"][0]["depends_on_task_id"] == seed_id
    assert len(body["would_dependency_edges"]) == 1
    assert body["would_dependency_edges"][0]["depends_on_task_ids"] == [seed_id]


def test_ceo_planning_apply_start_after_task_must_belong_to_same_project():
    pid_a = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyStartAfterA",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    pid_b = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyStartAfterB",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    seed = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid_b,
            "name": "other-project-anchor",
            "priority": "P1",
        },
    )
    assert seed.status_code == 201
    seed_id = seed.json()["id"]

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid_a,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "start_after_task_id": seed_id,
        },
    )
    assert r.status_code == 400
    detail = r.json()["detail"]
    assert detail["error_code"] == "TASK_PROJECT_MISMATCH"


def test_ceo_planning_apply_respects_max_create_tasks_limit():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyLimit",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "max_create_tasks": 1,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert len(body["created_tasks"]) == 1
    assert body["applied_count"] == 1
    assert body["planned_count"] >= body["applied_count"]


def test_ceo_planning_apply_filters_by_priorities_before_create():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyPriorityFilter",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "create_priorities": ["P1"],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["planned_count"] >= 3
    assert body["filtered_count"] == 1
    assert body["applied_count"] == 1
    assert len(body["created_tasks"]) == 1
    assert body["created_tasks"][0]["priority"] == "P1"


def test_ceo_planning_apply_dedupe_by_name_skips_existing_tasks():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyDedupe",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    seed = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "对齐目标与范围",
            "priority": "P0",
        },
    )
    assert seed.status_code == 201

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "dedupe_by_name": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["planned_count"] >= 3
    assert body["skipped_duplicates"] >= 1
    assert "对齐目标与范围" in body["skipped_duplicate_names"]
    assert all(t["name"] != "对齐目标与范围" for t in body["created_tasks"])


def test_ceo_planning_apply_dry_run_returns_duplicate_name_preview():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyDedupeDry",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    seed = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "对齐目标与范围",
            "priority": "P0",
        },
    )
    assert seed.status_code == 201

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": True,
            "dedupe_by_name": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["would_skip_duplicates"] >= 1
    assert "对齐目标与范围" in body["would_skip_duplicate_names"]
    assert "对齐目标与范围" not in body["would_create_task_names"]
    assert len(body["would_create_task_names"]) >= 1
    assert body["would_no_op"] is False
    assert body["would_no_op_reason"] == ""


def test_ceo_planning_apply_dry_run_returns_final_create_preview_after_filters():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyDryPreview",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": True,
            "create_priorities": ["P1"],
            "max_create_tasks": 1,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["would_filter"] == 1
    assert body["would_apply"] == 1
    assert body["would_skip_duplicates"] == 0
    assert body["would_create_task_names"] == ["同步风险与资源"]
    assert body["would_dependency_preview"][0]["name"] == "同步风险与资源"
    assert body["would_dependency_preview"][0]["depends_on_task_id"] is None
    assert body["would_no_op"] is False
    assert body["would_apply_by_priority"]["P1"] == 1
    assert body["would_apply_by_priority"]["P0"] == 0
    assert body["would_no_op_reason"] == ""
    assert "PRIORITY_FILTER_IMPACT" in body["would_risk_flags"]


def test_ceo_planning_apply_dry_run_returns_no_op_reason_when_deduped_all():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyDryNoOpReason",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    for name in ("对齐目标与范围", "拆解工作包与依赖", "同步风险与资源"):
        seed = client.post(
            "/api/v1/tasks",
            json={
                "project_id": pid,
                "name": name,
                "priority": "P1",
            },
        )
        assert seed.status_code == 201

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": True,
            "dedupe_by_name": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["would_no_op"] is True
    assert body["would_no_op_reason"] == "DEDUPED_ALL"
    assert "DEDUPE_IMPACT" in body["would_risk_flags"]
    assert "NO_OP_DEDUPED_ALL" in body["would_risk_flags"]
    assert "NO_OP_DEDUPED_ALL" in body["would_risk_summary"]["high"]
    assert body["would_risk_score"] >= 20
    assert body["next_action_hint"] == "REVIEW_HIGH_RISK_BEFORE_APPLY"


def test_ceo_planning_apply_dry_run_marks_limit_truncation_risk():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyDryLimitRisk",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": True,
            "max_create_tasks": 1,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["would_create"] >= 2
    assert body["would_apply"] == 1
    assert "LIMIT_TRUNCATION" in body["would_risk_flags"]
    assert "LIMIT_TRUNCATION" in body["would_risk_summary"]["high"]
    assert body["would_risk_score"] >= 10


def test_ceo_planning_apply_returns_no_op_when_filtered_to_empty():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyNoOp",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "项目里程碑与任务拆解",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "create_priorities": ["P3"],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["planned_count"] >= 1
    assert body["filtered_count"] == 0
    assert body["applied_count"] == 0
    assert body["created_tasks"] == []
    assert body["created_task_ids"] == []
    assert body["created_task_id_map"] == {}
    assert body["applied_dependency_edges"] == []
    assert body["applied_by_intent_source"] == {}
    assert body["intent_source_delta"] == {}
    assert "NO_OP_FILTERED_OUT" in body["applied_risk_flags"]
    assert "NO_OP_FILTERED_OUT" in body["applied_risk_summary"]["high"]
    assert body["applied_risk_score"] >= 10
    assert body["risk_alignment"] == "consistent"
    assert body["no_op"] is True
    assert body["no_op_reason"] == "FILTERED_OUT"
    assert body["applied_by_priority"] == {"P0": 0, "P1": 0, "P2": 0, "P3": 0}


def test_ceo_planning_apply_normalizes_invalid_suggested_domain_before_create():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyInvalidDomainFallback",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]

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
            "/api/v1/ceo/planning/apply",
            json={
                "instruction": "任意",
                "project_id": pid,
                "environment": "dev",
                "law": _LAW,
                "dry_run": False,
            },
        )
    finally:
        ceo_router.ceo_plan = old_plan

    assert r.status_code == 200
    created = r.json()["created_tasks"]
    assert len(created) == 1
    assert created[0]["description"].startswith("【D03】")


def test_ceo_planning_apply_dry_run_returns_intent_source_breakdown():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyIntentBreakdown",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "推进项目里程碑，并同步营销投放策略",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    breakdown = body["would_create_by_intent_source"]
    assert isinstance(breakdown, dict)
    assert breakdown.get("project_mgmt", 0) >= 1
    assert breakdown.get("marketing", 0) >= 1


def test_ceo_planning_apply_returns_applied_intent_source_breakdown():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyAppliedIntentBreakdown",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "推进项目里程碑，并同步营销投放策略",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
        },
    )
    assert r.status_code == 200
    body = r.json()
    breakdown = body["applied_by_intent_source"]
    assert isinstance(breakdown, dict)
    assert len(breakdown) >= 2
    assert breakdown.get("project_mgmt", 0) + breakdown.get("marketing", 0) >= 2
    assert body["intent_source_delta"] == {}
    assert isinstance(body["applied_risk_flags"], list)
    assert isinstance(body["applied_risk_summary"], dict)
    assert isinstance(body["applied_risk_score"], int)
    assert body["risk_alignment"] in {"consistent", "drifted"}


def test_ceo_planning_apply_intent_source_delta_when_deduped():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "ApplyIntentDeltaDeduped",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]

    # 预置一个 marketing 次意图常见任务，触发 dedupe 后应出现来源侧负向偏差
    seed = client.post(
        "/api/v1/tasks",
        json={
            "project_id": pid,
            "name": "明确受众与渠道假设",
            "priority": "P1",
        },
    )
    assert seed.status_code == 201

    r = client.post(
        "/api/v1/ceo/planning/apply",
        json={
            "instruction": "推进项目里程碑，并同步营销投放策略",
            "project_id": pid,
            "environment": "dev",
            "law": _LAW,
            "dry_run": False,
            "dedupe_by_name": True,
        },
    )
    assert r.status_code == 200
    body = r.json()
    delta = body["intent_source_delta"]
    assert isinstance(delta, dict)
    assert any(v < 0 for v in delta.values())
    assert body["risk_alignment"] == "drifted"
    assert body["next_action_hint"] == "RECHECK_PLAN_AND_RERUN_DRY_RUN"
    assert body["decision_snapshot"]["risk_alignment"] == "drifted"
    assert body["decision_snapshot"]["confidence_band"] in {"low", "medium"}
    reasons = body["decision_snapshot"]["blocking_reasons"]
    assert any(r.get("code") == "INTENT_SOURCE_REDUCED" and r.get("severity") == "high" for r in reasons)
    assert body["decision_snapshot"]["risk_diff"] > 0
    assert body["decision_snapshot"]["risk_trend"] == "up"
    assert body["decision_snapshot"]["recommended_mode"] == "dry_run_again"
    assert body["decision_snapshot"]["ui_priority"] == "p1"
    assert "rerun_dry_run" in body["decision_snapshot"]["recommended_actions"]
