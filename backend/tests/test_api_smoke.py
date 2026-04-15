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


def test_git_sync_audit_ingest_endpoint():
    ok = client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "main",
            "status": "success",
            "message": "sync ok",
            "source": "git_auto_sync.ps1",
            "environment": "dev",
            "context": {"retry_count": 1},
        },
    )
    assert ok.status_code == 201
    assert ok.json()["accepted"] is True
    assert ok.json()["reason_code"] == "GIT_SYNC_SUCCESS"

    bad = client.post(
        "/api/v1/ops/git-sync/events",
        json={"branch": "main", "status": "unknown", "environment": "dev"},
    )
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "INVALID_GIT_SYNC_STATUS"


def test_git_sync_summary_endpoint():
    client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "main",
            "status": "success",
            "source": "git_sync_once.ps1",
            "environment": "dev",
            "context": {"status": "success", "branch": "main", "push_attempts": 1, "audit_delivery": "success"},
        },
    )
    client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "main",
            "status": "failure",
            "source": "git_auto_sync.ps1",
            "environment": "dev",
            "context": {"status": "failure", "branch": "main", "push_attempts": 2, "audit_delivery": "failed"},
        },
    )
    client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "release/2026w16",
            "status": "skipped",
            "source": "git_auto_sync.ps1",
            "environment": "dev",
            "context": {"status": "skipped", "branch": "release/2026w16", "push_attempts": 0, "audit_delivery": "failed"},
        },
    )
    r = client.get("/api/v1/ops/git-sync/summary", params={"days": 7, "environment": "dev"})
    assert r.status_code == 200
    body = r.json()
    assert body["days"] == 7
    assert body["environment"] == "dev"
    assert "totals" in body
    assert "success_rate" in body
    assert "failure_rate" in body
    assert "last_success_at" in body
    assert "last_failure_at" in body
    assert "last_skipped_at" in body
    assert "last_event_at" in body
    assert "minutes_since_last_success" in body
    assert "minutes_since_last_failure" in body
    assert "minutes_since_last_skipped" in body
    assert "minutes_since_last_event" in body
    assert "consecutive_failure_streak" in body
    assert "consecutive_non_success_streak" in body
    assert "sync_health_level" in body
    assert "sync_health_warning" in body
    assert "bucket_count" in body
    assert "non_empty_bucket_count" in body
    assert "top_branches" in body
    assert "top_source_branches" in body
    assert "failure_reason_distribution" in body
    assert "failure_reason_timeline" in body
    assert "avg_push_attempts" in body
    assert "max_push_attempts" in body
    assert "push_attempt_sample_count" in body
    assert "audit_delivery_success_count" in body
    assert "audit_delivery_failed_count" in body
    assert "audit_delivery_success_rate" in body
    assert "audit_delivery_failure_rate" in body
    assert "last_audit_delivery_success_at" in body
    assert "last_audit_delivery_failed_at" in body
    assert "minutes_since_last_audit_delivery_success" in body
    assert "minutes_since_last_audit_delivery_failed" in body
    assert body["granularity"] == "day"
    assert body["bucket_label_format"] == "raw"
    assert isinstance(body["timeline"], list)
    assert len(body["timeline"]) == 7
    assert "bucket_label" in body["timeline"][0]
    assert body["timeline"][0]["bucket_label"] == body["timeline"][0]["bucket"]
    assert body["bucket_count"] == len(body["timeline"])
    assert 0 <= body["non_empty_bucket_count"] <= body["bucket_count"]
    assert body["totals"]["total"] >= 3
    assert isinstance(body["last_success_at"], str)
    assert isinstance(body["last_failure_at"], str)
    assert isinstance(body["last_skipped_at"], str)
    assert isinstance(body["last_event_at"], str)
    assert isinstance(body["minutes_since_last_success"], float)
    assert isinstance(body["minutes_since_last_failure"], float)
    assert isinstance(body["minutes_since_last_skipped"], float)
    assert isinstance(body["minutes_since_last_event"], float)
    assert isinstance(body["consecutive_failure_streak"], int)
    assert isinstance(body["consecutive_non_success_streak"], int)
    assert body["sync_health_level"] in {"healthy", "warning", "high_risk"}
    assert isinstance(body["sync_health_warning"], bool)
    assert isinstance(body["avg_push_attempts"], float)
    assert isinstance(body["max_push_attempts"], int)
    assert isinstance(body["push_attempt_sample_count"], int)
    assert isinstance(body["audit_delivery_success_count"], int)
    assert isinstance(body["audit_delivery_failed_count"], int)
    assert isinstance(body["audit_delivery_success_rate"], float)
    assert isinstance(body["audit_delivery_failure_rate"], float)
    assert isinstance(body["last_audit_delivery_success_at"], str)
    assert isinstance(body["last_audit_delivery_failed_at"], str)
    assert isinstance(body["minutes_since_last_audit_delivery_success"], float)
    assert isinstance(body["minutes_since_last_audit_delivery_failed"], float)
    assert len(body["top_branches"]) >= 1
    assert "branch" in body["top_branches"][0]
    assert len(body["top_source_branches"]) >= 1
    assert "source" in body["top_source_branches"][0]
    assert "branch" in body["top_source_branches"][0]
    assert any(item["reason_code"] == "GIT_SYNC_FAILURE" for item in body["failure_reason_distribution"])
    assert isinstance(body["failure_reason_timeline"], list)
    assert len(body["failure_reason_timeline"]) == len(body["timeline"])
    assert all(len(x["reasons"]) <= 5 for x in body["failure_reason_timeline"])

    r_top = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 7, "environment": "dev", "top_n_reasons": 1},
    )
    assert r_top.status_code == 200
    top_body = r_top.json()
    assert all(len(x["reasons"]) <= 1 for x in top_body["failure_reason_timeline"])

    r_no_empty = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 7, "environment": "dev", "include_empty_buckets": False},
    )
    assert r_no_empty.status_code == 200
    ne = r_no_empty.json()
    assert ne["include_empty_buckets"] is False
    assert all(int(x.get("total", 0)) > 0 for x in ne["timeline"])
    assert len(ne["failure_reason_timeline"]) == len(ne["timeline"])
    assert ne["non_empty_bucket_count"] == len(ne["timeline"])
    assert ne["bucket_count"] >= ne["non_empty_bucket_count"]

    r_branch = client.get("/api/v1/ops/git-sync/summary", params={"days": 7, "environment": "dev", "branch": "main"})
    assert r_branch.status_code == 200
    b = r_branch.json()
    assert b["branch"] == "main"
    assert b["totals"]["success"] >= 1
    assert b["totals"]["failure"] >= 1

    r_source = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 7, "environment": "dev", "source": "git_auto_sync.ps1"},
    )
    assert r_source.status_code == 200
    s = r_source.json()
    assert s["source"] == "git_auto_sync.ps1"
    assert s["totals"]["failure"] >= 1

    r_hour = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 1, "environment": "dev", "granularity": "hour", "bucket_label_format": "human"},
    )
    assert r_hour.status_code == 200
    h = r_hour.json()
    assert h["granularity"] == "hour"
    assert h["bucket_label_format"] == "human"
    assert len(h["timeline"]) == 24
    assert h["tz"] == "UTC"
    assert "UTC" in h["timeline"][0]["bucket_label"]

    r_tz = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 1, "environment": "dev", "granularity": "hour", "bucket_label_format": "human", "tz": "Asia/Shanghai"},
    )
    assert r_tz.status_code == 200
    tzb = r_tz.json()
    assert tzb["tz"] == "Asia/Shanghai"
    assert len(tzb["timeline"]) == 24

    r_range = client.get(
        "/api/v1/ops/git-sync/summary",
        params={
            "days": 7,
            "environment": "dev",
            "since": "2026-01-01T00:00:00Z",
            "until": "2099-01-01T00:00:00Z",
        },
    )
    assert r_range.status_code == 200
    rr = r_range.json()
    assert rr["since"] is not None
    assert rr["until"] is not None

    bad = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 1, "environment": "dev", "granularity": "minute"},
    )
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "INVALID_GRANULARITY"

    bad_range = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 1, "environment": "dev", "since": "2099-01-01T00:00:00Z", "until": "2026-01-01T00:00:00Z"},
    )
    assert bad_range.status_code == 400
    assert bad_range.json()["detail"]["error_code"] == "INVALID_TIME_RANGE"

    bad_bucket = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 1, "environment": "dev", "bucket_label_format": "pretty"},
    )
    assert bad_bucket.status_code == 400
    assert bad_bucket.json()["detail"]["error_code"] == "INVALID_BUCKET_LABEL_FORMAT"

    bad_tz = client.get(
        "/api/v1/ops/git-sync/summary",
        params={"days": 1, "environment": "dev", "tz": "Mars/Olympus"},
    )
    assert bad_tz.status_code == 400
    assert bad_tz.json()["detail"]["error_code"] == "INVALID_TIMEZONE"


def test_analytics_reports_project_execution_and_ops_risk():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "analytics-demo",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "r1", "status": "blocked", "progress": 0, "end_date": "2026-01-01"},
    )
    client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "r2", "status": "in_progress", "progress": 0, "end_date": "2026-01-01"},
    )
    _ = client.get(f"/api/v1/projects/{pid}/progress")
    _ = client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "main",
            "status": "failure",
            "source": "git_auto_sync.ps1",
            "environment": "dev",
            "context": {
                "status": "failure",
                "branch": "main",
                "push_attempts": 2,
                "audit_delivery": "failed",
            },
        },
    )
    _ = client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "main",
            "status": "success",
            "source": "git_sync_once.ps1",
            "environment": "dev",
            "context": {
                "status": "success",
                "branch": "main",
                "push_attempts": 1,
                "audit_delivery": "success",
            },
        },
    )

    pe = client.get("/api/v1/analytics/reports", params={"report_type": "project_execution", "environment": "dev"})
    assert pe.status_code == 200
    peb = pe.json()
    assert peb["report_type"] == "project_execution"
    assert peb["project_count"] >= 1
    assert "risk_distribution" in peb
    assert "top_risk_projects" in peb

    ops = client.get("/api/v1/analytics/reports", params={"report_type": "ops_risk", "days": 7, "environment": "dev"})
    assert ops.status_code == 200
    opsb = ops.json()
    assert opsb["report_type"] == "ops_risk"
    assert "project_risk_alert_event_count" in opsb
    assert "git_sync_success_count" in opsb
    assert "git_sync_failure_count" in opsb
    assert "git_sync_skipped_count" in opsb
    assert "git_sync_success_rate" in opsb
    assert "git_sync_failure_rate" in opsb
    assert "git_sync_skipped_rate" in opsb
    assert "git_sync_audit_delivery_failed_count" in opsb
    assert "git_sync_audit_delivery_success_count" in opsb
    assert "git_sync_audit_delivery_failure_rate" in opsb
    assert "git_sync_audit_delivery_success_rate" in opsb
    assert "git_sync_net_success_rate" in opsb
    assert "git_sync_failure_pressure_index" in opsb
    assert "git_sync_event_density_per_day" in opsb
    assert "git_sync_success_density_per_day" in opsb
    assert "git_sync_failure_density_per_day" in opsb
    assert "git_sync_skipped_density_per_day" in opsb
    assert "git_sync_net_success_density_per_day" in opsb
    assert "git_sync_top_failure_reason_code" in opsb
    assert "git_sync_top_failure_reason_count" in opsb
    assert "git_sync_top_failure_reason_rate" in opsb
    assert "git_sync_avg_push_attempts" in opsb
    assert "git_sync_max_push_attempts" in opsb
    assert "git_sync_push_attempt_sample_count" in opsb
    assert "git_sync_consecutive_failure_streak" in opsb
    assert "git_sync_consecutive_non_success_streak" in opsb
    assert "git_sync_health_level" in opsb
    assert "git_sync_health_warning" in opsb
    assert "last_git_sync_event_at" in opsb
    assert "minutes_since_last_git_sync_event" in opsb
    assert "last_git_sync_success_at" in opsb
    assert "minutes_since_last_git_sync_success" in opsb
    assert "last_git_sync_failure_at" in opsb
    assert "minutes_since_last_git_sync_failure" in opsb
    assert isinstance(opsb["git_sync_success_rate"], float)
    assert isinstance(opsb["git_sync_failure_rate"], float)
    assert isinstance(opsb["git_sync_skipped_rate"], float)
    assert isinstance(opsb["git_sync_audit_delivery_failed_count"], int)
    assert isinstance(opsb["git_sync_audit_delivery_success_count"], int)
    assert isinstance(opsb["git_sync_audit_delivery_failure_rate"], float)
    assert isinstance(opsb["git_sync_audit_delivery_success_rate"], float)
    assert isinstance(opsb["git_sync_net_success_rate"], float)
    assert isinstance(opsb["git_sync_failure_pressure_index"], float)
    assert isinstance(opsb["git_sync_event_density_per_day"], float)
    assert isinstance(opsb["git_sync_success_density_per_day"], float)
    assert isinstance(opsb["git_sync_failure_density_per_day"], float)
    assert isinstance(opsb["git_sync_skipped_density_per_day"], float)
    assert isinstance(opsb["git_sync_net_success_density_per_day"], float)
    assert isinstance(opsb["git_sync_top_failure_reason_code"], str)
    assert isinstance(opsb["git_sync_top_failure_reason_count"], int)
    assert isinstance(opsb["git_sync_top_failure_reason_rate"], float)
    assert isinstance(opsb["git_sync_avg_push_attempts"], float)
    assert isinstance(opsb["git_sync_max_push_attempts"], int)
    assert isinstance(opsb["git_sync_push_attempt_sample_count"], int)
    assert isinstance(opsb["git_sync_consecutive_failure_streak"], int)
    assert isinstance(opsb["git_sync_consecutive_non_success_streak"], int)
    assert opsb["git_sync_health_level"] in {"healthy", "warning", "high_risk"}
    assert isinstance(opsb["git_sync_health_warning"], bool)
    assert isinstance(opsb["last_git_sync_event_at"], str)
    assert isinstance(opsb["minutes_since_last_git_sync_event"], float)
    assert isinstance(opsb["last_git_sync_success_at"], str)
    assert isinstance(opsb["minutes_since_last_git_sync_success"], float)
    assert isinstance(opsb["last_git_sync_failure_at"], str)
    assert isinstance(opsb["minutes_since_last_git_sync_failure"], float)
    assert opsb["ops_risk_level"] in {"low", "medium", "high"}

    bad = client.get("/api/v1/analytics/reports", params={"report_type": "unknown"})
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "INVALID_REPORT_TYPE"


def test_audit_logs_endpoint_with_pagination():
    _ = client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "main",
            "status": "success",
            "source": "git_sync_once.ps1",
            "environment": "dev",
            "context": {"status": "success", "branch": "main"},
        },
    )
    _ = client.post(
        "/api/v1/ops/git-sync/events",
        json={
            "branch": "main",
            "status": "failure",
            "source": "git_auto_sync.ps1",
            "environment": "dev",
            "context": {"status": "failure", "branch": "main"},
        },
    )
    r = client.get(
        "/api/v1/audit/logs",
        params={"event_type_prefix": "git_sync_status", "environment": "dev", "limit": 1, "offset": 0},
    )
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert body["limit"] == 1
    assert body["offset"] == 0
    assert body["total"] >= 1
    assert len(body["items"]) <= 1


def test_create_webhook_endpoint():
    ok = client.post(
        "/api/v1/webhooks",
        json={
            "name": "build-callback",
            "url": "https://example.com/hook",
            "events": ["project.updated", "task.created"],
            "enabled": True,
            "secret": "abc",
        },
    )
    assert ok.status_code == 201
    body = ok.json()
    assert body["id"].startswith("wh-")
    assert body["name"] == "build-callback"
    assert body["url"] == "https://example.com/hook"
    assert body["enabled"] is True

    bad = client.post(
        "/api/v1/webhooks",
        json={"name": "bad", "url": "ftp://example.com/hook", "events": []},
    )
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "INVALID_WEBHOOK_URL"


def test_list_webhooks_endpoint():
    c1 = client.post(
        "/api/v1/webhooks",
        json={
            "name": "list-hook-enabled",
            "url": "https://example.com/enabled",
            "events": ["project.updated"],
            "enabled": True,
        },
    )
    assert c1.status_code == 201
    c2 = client.post(
        "/api/v1/webhooks",
        json={
            "name": "list-hook-disabled",
            "url": "https://example.com/disabled",
            "events": ["task.created"],
            "enabled": False,
        },
    )
    assert c2.status_code == 201

    all_rows = client.get("/api/v1/webhooks", params={"limit": 50, "offset": 0})
    assert all_rows.status_code == 200
    all_body = all_rows.json()
    assert "items" in all_body and "total" in all_body
    assert all_body["total"] >= 2

    only_enabled = client.get("/api/v1/webhooks", params={"enabled": True, "limit": 50, "offset": 0})
    assert only_enabled.status_code == 200
    eb = only_enabled.json()
    assert all(bool(x.get("enabled", True)) is True for x in eb["items"])


def test_update_and_delete_webhook_endpoint():
    c = client.post(
        "/api/v1/webhooks",
        json={
            "name": "editable-hook",
            "url": "https://example.com/original",
            "events": ["task.created"],
            "enabled": True,
        },
    )
    assert c.status_code == 201
    wid = c.json()["id"]

    u = client.put(
        f"/api/v1/webhooks/{wid}",
        json={
            "name": "editable-hook-updated",
            "url": "https://example.com/updated",
            "enabled": False,
            "events": ["project.updated"],
        },
    )
    assert u.status_code == 200
    body = u.json()
    assert body["id"] == wid
    assert body["name"] == "editable-hook-updated"
    assert body["url"] == "https://example.com/updated"
    assert body["enabled"] is False

    bad = client.put(f"/api/v1/webhooks/{wid}", json={"url": "ftp://invalid"})
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "INVALID_WEBHOOK_URL"

    d = client.delete(f"/api/v1/webhooks/{wid}")
    assert d.status_code == 204

    d2 = client.delete(f"/api/v1/webhooks/{wid}")
    assert d2.status_code == 404


def test_get_webhook_endpoint():
    c = client.post(
        "/api/v1/webhooks",
        json={
            "name": "get-hook",
            "url": "https://example.com/get",
            "events": ["project.updated"],
            "enabled": True,
        },
    )
    assert c.status_code == 201
    wid = c.json()["id"]

    g = client.get(f"/api/v1/webhooks/{wid}")
    assert g.status_code == 200
    body = g.json()
    assert body["id"] == wid
    assert body["name"] == "get-hook"

    miss = client.get("/api/v1/webhooks/wh-no-such-id")
    assert miss.status_code == 404


def test_agent_reflect_endpoint():
    agents = client.get("/api/v1/agents").json()["items"]
    assert len(agents) >= 1
    aid = agents[0]["id"]
    r = client.post(
        f"/api/v1/agents/{aid}/reflect",
        json={
            "instruction": "请总结今天执行偏差并给出改进",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["agent_id"] == aid
    assert body["reflection"]["memory_id"].startswith("wm-")
    assert "[SELF_REFLECTION]" in body["reflection"]["content"]

    logs = client.get(
        "/api/v1/audit/events",
        params={"event_type_prefix": "agent_reflect_triggered", "limit": 50},
    )
    assert logs.status_code == 200
    events = logs.json()["events"]
    assert any(e["event_type"] == "agent_reflect_triggered" for e in events)


def test_agents_batch_create_endpoint():
    roots = client.get("/api/v1/agents").json()["items"]
    assert len(roots) >= 1
    parent_id = roots[0]["id"]
    ok = client.post(
        "/api/v1/agents/batch",
        json={
            "items": [
                {
                    "name": "batch-agent-1",
                    "level": "L5",
                    "role": "EMPLOYEE",
                    "status": "online",
                    "parent_id": parent_id,
                    "domain": "D03",
                },
                {
                    "name": "batch-agent-2",
                    "level": "L5",
                    "role": "EMPLOYEE",
                    "status": "busy",
                    "parent_id": parent_id,
                    "domain": "D03",
                },
            ]
        },
    )
    assert ok.status_code == 201
    body = ok.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2
    assert body["items"][0]["id"].startswith("agent-")

    bad = client.post(
        "/api/v1/agents/batch",
        json={
            "items": [
                {
                    "name": "bad-parent",
                    "level": "L5",
                    "role": "EMPLOYEE",
                    "parent_id": "agent-no-such-parent",
                }
            ]
        },
    )
    assert bad.status_code == 400
    assert bad.json()["detail"]["error_code"] == "INVALID_PARENT_AGENT"


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
    assert "risk_alert_cooldown_minutes" in r.json()["policy"]
    assert "risk_alert_trigger_score" in r.json()["policy"]


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

    # v1.1 参数增强：按 capability_id 过滤
    r2 = client.get("/api/v1/agents", params={"capability_id": "CEO-09"})
    assert r2.status_code == 200
    items = r2.json()["items"]
    assert isinstance(items, list)
    if items:
        assert all("CEO-09" in list((x.get("skill_config") or {}).get("skill_ids") or []) for x in items)


def test_agents_response_includes_tags_and_runtime_state():
    r = client.get("/api/v1/agents", params={"limit": 5})
    assert r.status_code == 200
    items = r.json()["items"]
    assert isinstance(items, list)
    if items:
        first = items[0]
        assert "tags" in first
        assert isinstance(first["tags"], list)
        assert "runtime_state" in first
        assert isinstance(first["runtime_state"], dict)
        assert "cognitive_load" in first["runtime_state"]


def test_agent_skills_bind_and_query_endpoint():
    agents = client.get("/api/v1/agents").json()["items"]
    assert len(agents) >= 1
    aid = agents[0]["id"]

    s1 = client.post(
        "/api/v1/skills",
        json={
            "name": "agent-skill-a",
            "category": "agent",
            "level": "middle",
        },
    )
    assert s1.status_code == 201
    s2 = client.post(
        "/api/v1/skills",
        json={
            "name": "agent-skill-b",
            "category": "agent",
            "level": "senior",
        },
    )
    assert s2.status_code == 201
    sid1 = s1.json()["id"]
    sid2 = s2.json()["id"]

    put = client.put(f"/api/v1/agents/{aid}/skills", json={"skill_ids": [sid1, sid2]})
    assert put.status_code == 200
    assert put.json()["total"] == 2

    got = client.get(f"/api/v1/agents/{aid}/skills")
    assert got.status_code == 200
    ids = {x["id"] for x in got.json()["items"]}
    assert sid1 in ids and sid2 in ids


def test_agent_memory_endpoint():
    agents = client.get("/api/v1/agents").json()["items"]
    assert len(agents) >= 1
    aid = agents[0]["id"]

    a = client.post(
        f"/api/v1/agents/{aid}/memory/working",
        json={"content": "memory-a"},
    )
    assert a.status_code == 201
    b = client.post(
        f"/api/v1/agents/{aid}/memory/working",
        json={"content": "memory-b"},
    )
    assert b.status_code == 201

    r = client.get(f"/api/v1/agents/{aid}/memory", params={"limit": 10})
    assert r.status_code == 200
    body = r.json()
    assert body["agent_id"] == aid
    assert "working_memories" in body
    assert body["working_memory_count"] >= 2


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


def test_approvals_pending_endpoint():
    c = client.post(
        "/api/v1/projects",
        json={
            "name": "审批待办项目",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert c.status_code == 200
    pid = c.json()["id"]

    s = client.post(f"/api/v1/projects/{pid}/submit", json={})
    assert s.status_code == 200

    r = client.get("/api/v1/approvals/pending", params={"limit": 500, "offset": 0})
    assert r.status_code == 200
    body = r.json()
    assert "items" in body and "total" in body
    assert body["limit"] == 500
    assert body["offset"] == 0
    assert any(x["id"] == pid for x in body["items"])


def test_approval_application_and_actions_endpoints():
    c = client.post(
        "/api/v1/projects",
        json={
            "name": "审批动作项目",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert c.status_code == 200
    pid = c.json()["id"]

    app_resp = client.post(
        "/api/v1/approvals/applications",
        json={"project_id": pid, "approval_chain": ["L3", "L2"]},
    )
    assert app_resp.status_code == 201
    assert app_resp.json()["status"] == "pending_approval"

    a1 = client.post(f"/api/v1/approvals/{pid}/approve", json={"level": "L3"})
    assert a1.status_code == 200

    bad_reject = client.post(f"/api/v1/approvals/{pid}/reject", json={"level": "L2"})
    assert bad_reject.status_code == 400
    assert bad_reject.json()["detail"]["error_code"] == "APPROVAL_REJECT_REASON_REQUIRED"

    rej = client.post(
        f"/api/v1/approvals/{pid}/reject",
        json={"level": "L2", "reason": "人工驳回验证"},
    )
    assert rej.status_code == 200
    assert rej.json()["status"] == "rejected"


def test_project_create_accepts_tags():
    resp = client.post(
        "/api/v1/projects",
        json={
            "name": "标签项目",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
            "tags": ["v1.1", "analytics"],
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("tags") == ["v1.1", "analytics"]
    assert isinstance(body.get("last_activity"), str)


def test_project_last_activity_updates_after_task_and_discussion():
    create = client.post(
        "/api/v1/projects",
        json={
            "name": "活动时间项目",
            "domain": "D03",
            "project_type": "optimization",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert create.status_code == 200
    pid = create.json()["id"]
    first = create.json().get("last_activity")
    assert isinstance(first, str)

    t = client.post(
        "/api/v1/tasks",
        json={"project_id": pid, "name": "activity-task", "progress": 10},
    )
    assert t.status_code == 201
    after_task = client.get(f"/api/v1/projects/{pid}").json().get("last_activity")
    assert isinstance(after_task, str)
    assert after_task >= first

    d = client.post(
        f"/api/v1/projects/{pid}/discussion",
        json={"author": "qa", "body": "touch activity"},
    )
    assert d.status_code == 201
    after_discussion = client.get(f"/api/v1/projects/{pid}").json().get("last_activity")
    assert isinstance(after_discussion, str)
    assert after_discussion >= after_task


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


def test_chat_history_endpoint():
    s = client.post("/api/v1/chat/sessions", json={"title": "history-api"})
    assert s.status_code == 200
    sid = s.json()["id"]
    m = client.post(
        f"/api/v1/chat/sessions/{sid}/messages",
        json={"message": "history test", "environment": "dev", "law": ["LAW-05"]},
    )
    assert m.status_code == 200

    r = client.get("/api/v1/chat/history", params={"limit": 10, "message_limit": 10})
    assert r.status_code == 200
    body = r.json()
    assert "sessions" in body
    assert "total_sessions" in body
    assert "returned_sessions" in body
    assert any(x["id"] == sid for x in body["sessions"])


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
