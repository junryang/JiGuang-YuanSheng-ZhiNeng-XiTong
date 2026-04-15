from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from fastapi.testclient import TestClient

from app.main import app


pytestmark = pytest.mark.day3_gate

client = TestClient(app)

FULL_LAW = ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"]
MISSING_LAW = ["LAW-01", "LAW-02", "LAW-03", "LAW-05"]
EMPTY_LAW: list[str] = []
LAW_MAP = {
    "FULL_LAW": FULL_LAW,
    "MISSING_LAW": MISSING_LAW,
    "EMPTY_LAW": EMPTY_LAW,
}

_MATRIX_PATH = Path(__file__).resolve().parents[2] / "docs" / "DAY3_POLICY_GATE_MATRIX_CASES_v1.0.yaml"
_MATRIX = yaml.safe_load(_MATRIX_PATH.read_text(encoding="utf-8"))


def _law_from_ref(ref: str) -> list[str]:
    return list(LAW_MAP[ref])


def _expand_context(ctx: dict) -> dict:
    out = dict(ctx)
    if "law_ref" in out:
        out["law"] = _law_from_ref(str(out.pop("law_ref")))
    return out


def _assert_keys(d: dict, required: tuple[str, ...], where: str) -> None:
    missing = [k for k in required if k not in d]
    assert not missing, f"{where} missing keys: {missing}"


def _validate_matrix_schema(m: dict) -> None:
    _assert_keys(
        m,
        (
            "version",
            "publish_cases",
            "policy_eval_cases",
            "orchestration_cases",
            "approval_cases",
            "audit_consistency_cases",
            "security_sampling_cases",
        ),
        "matrix root",
    )
    assert isinstance(m["version"], str) and m["version"]
    for i, c in enumerate(m["publish_cases"]):
        _assert_keys(
            c,
            ("name", "runtime_mode", "environment", "law_ref", "approved", "expected_status", "expected_error_code"),
            f"publish_cases[{i}]",
        )
        assert c["runtime_mode"] in ("normal", "degraded")
        assert c["environment"] in ("dev", "staging", "prod")
        assert c["law_ref"] in LAW_MAP
        assert isinstance(c["approved"], bool)
        assert int(c["expected_status"]) in (200, 400, 403, 404, 422)

    for i, c in enumerate(m["policy_eval_cases"]):
        _assert_keys(
            c,
            ("name", "policy_id", "environment", "context", "expected_status", "allowed_error_codes"),
            f"policy_eval_cases[{i}]",
        )
        assert c["environment"] in ("dev", "staging", "prod")
        assert isinstance(c["context"], dict)
        assert c["context"].get("law_ref") in LAW_MAP
        assert int(c["expected_status"]) in (200, 403)
        assert isinstance(c["allowed_error_codes"], list)

    for i, c in enumerate(m["orchestration_cases"]):
        _assert_keys(
            c,
            ("name", "environment", "law_ref", "use_optional_tools", "approved", "expected_statuses", "allowed_error_codes"),
            f"orchestration_cases[{i}]",
        )
        assert c["environment"] in ("dev", "staging", "prod")
        assert c["law_ref"] in LAW_MAP
        assert isinstance(c["use_optional_tools"], bool)
        assert isinstance(c["approved"], bool)
        assert isinstance(c["expected_statuses"], list) and c["expected_statuses"]
        assert all(int(x) in (200, 400, 403, 404, 422) for x in c["expected_statuses"])
        assert isinstance(c["allowed_error_codes"], list)

    for i, c in enumerate(m["approval_cases"]):
        _assert_keys(c, ("case", "expected_status", "expected_project_status"), f"approval_cases[{i}]")
        assert int(c["expected_status"]) in (200, 400, 404)
        assert c["expected_project_status"] in ("pending_approval", "approved", "rejected", None)

    for i, c in enumerate(m["audit_consistency_cases"]):
        _assert_keys(c, ("params", "expect_nonempty"), f"audit_consistency_cases[{i}]")
        assert isinstance(c["params"], dict)
        allowed_keys = {"event_type_prefix", "policy_id", "environment", "reason_code_prefix"}
        assert set(c["params"]).issubset(allowed_keys)
        assert isinstance(c["expect_nonempty"], bool)

    for i, c in enumerate(m["security_sampling_cases"]):
        _assert_keys(
            c,
            (
                "name",
                "kind",
                "environment",
                "runtime_mode",
                "law_ref",
                "approved",
                "expected_status",
                "allowed_error_codes",
            ),
            f"security_sampling_cases[{i}]",
        )
        assert c["kind"] in ("publish", "orchestration")
        assert c["environment"] in ("staging", "prod")
        assert c["runtime_mode"] in ("normal", "degraded")
        assert c["law_ref"] in LAW_MAP
        assert isinstance(c["approved"], bool)
        assert int(c["expected_status"]) in (200, 400, 403, 404, 422)
        assert isinstance(c["allowed_error_codes"], list)
        if c["kind"] == "orchestration":
            assert isinstance(c.get("use_optional_tools", False), bool)


PUBLISH_CASES = [
    (
        c["name"],
        c["runtime_mode"],
        c["environment"],
        _law_from_ref(c["law_ref"]),
        bool(c["approved"]),
        int(c["expected_status"]),
        c.get("expected_error_code"),
    )
    for c in _MATRIX["publish_cases"]
]

POLICY_EVAL_CASES = [
    (
        c["name"],
        c["policy_id"],
        c["environment"],
        _expand_context(c["context"]),
        int(c["expected_status"]),
        tuple(c.get("allowed_error_codes", [])),
    )
    for c in _MATRIX["policy_eval_cases"]
]

ORCH_CASES = [
    (
        c["name"],
        c["environment"],
        _law_from_ref(c["law_ref"]),
        bool(c["use_optional_tools"]),
        bool(c["approved"]),
        tuple(int(x) for x in c["expected_statuses"]),
        tuple(c.get("allowed_error_codes", [])),
    )
    for c in _MATRIX["orchestration_cases"]
]

APPROVAL_CASES = [
    (
        c["case"],
        int(c["expected_status"]),
        c.get("expected_project_status"),
    )
    for c in _MATRIX["approval_cases"]
]

AUDIT_CONSISTENCY_CASES = [
    (dict(c["params"]), bool(c["expect_nonempty"]))
    for c in _MATRIX["audit_consistency_cases"]
]

SECURITY_SAMPLING_CASES = [
    (
        c["name"],
        c["kind"],
        c["environment"],
        c["runtime_mode"],
        _law_from_ref(c["law_ref"]),
        bool(c["approved"]),
        bool(c.get("use_optional_tools", False)),
        int(c["expected_status"]),
        tuple(c.get("allowed_error_codes", [])),
    )
    for c in _MATRIX["security_sampling_cases"]
]


def _set_runtime_mode(mode: str) -> None:
    r = client.post("/api/v1/runtime/mode", json={"mode": mode})
    assert r.status_code == 200
    assert r.json()["runtime_mode"] == mode


def _eval_policy(policy_id: str, environment: str, context: dict):
    return client.post(
        "/api/v1/policy/evaluate",
        json={"policy_id": policy_id, "environment": environment, "context": context},
    )


def _create_orchestration_plan(
    *,
    environment: str,
    law: list[str],
    use_optional_tools: bool,
    approved: bool,
):
    return client.post(
        "/api/v1/orchestration/plans",
        json={
            "name": "matrix-orch",
            "steps": ["WEB-06", "MCP"],
            "environment": environment,
            "law": law,
            "use_optional_tools": use_optional_tools,
            "approved": approved,
        },
    )


def _create_draft_project(name: str) -> str:
    r = client.post(
        "/api/v1/projects",
        json={
            "name": name,
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    )
    assert r.status_code == 200
    return r.json()["id"]


def _submit_project(pid: str, chain: list[str] | None = None):
    body = {"approval_chain": chain} if chain is not None else {}
    return client.post(f"/api/v1/projects/{pid}/submit", json=body)


def _seed_audit_events_for_consistency() -> None:
    agents = client.get("/api/v1/agents").json()["items"]
    aid = agents[0]["id"]
    _ = client.post(
        "/api/v1/collaboration/delegations",
        json={
            "from_agent_id": aid,
            "to_agent_id": aid,
            "objective": "matrix-audit-consistency",
            "contract": {
                "acceptance_criteria": "生成委托审计事件",
                "deliverables": ["审计记录"],
                "due_date": None,
            },
        },
    )
    _ = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "matrix-audit-consistency",
            "content": "x",
            "environment": "prod",
            "law": MISSING_LAW,
            "approved": False,
        },
    )


def test_policy_gate_matrix_yaml_schema_valid():
    _validate_matrix_schema(_MATRIX)


@pytest.mark.parametrize(
    ("name", "runtime_mode", "environment", "law", "approved", "expected_status", "expected_error_code"),
    PUBLISH_CASES,
)
def test_publish_policy_gate_matrix(
    name: str,
    runtime_mode: str,
    environment: str,
    law: list[str],
    approved: bool,
    expected_status: int,
    expected_error_code: str | None,
):
    _set_runtime_mode(runtime_mode)
    try:
        r = client.post(
            "/api/v1/contents/publish",
            json={
                "title": f"matrix-{name}",
                "content": "policy-matrix",
                "environment": environment,
                "law": law,
                "approved": approved,
            },
        )
        assert r.status_code == expected_status
        if expected_status == 200:
            data = r.json()
            assert data["status"] == "published"
            assert data["environment"] == environment
            return
        body = r.json()
        detail = body.get("detail", {})
        if expected_error_code is not None:
            assert detail.get("error_code") == expected_error_code
    finally:
        _set_runtime_mode("normal")


def test_policy_gate_matrix_audit_has_required_fields():
    # 触发一次拒绝，确保审计可观测字段完整
    _set_runtime_mode("normal")
    _ = client.post(
        "/api/v1/contents/publish",
        json={
            "title": "matrix-audit",
            "content": "matrix-audit",
            "environment": "prod",
            "law": MISSING_LAW,
            "approved": False,
        },
    )
    r = client.get("/api/v1/audit/events", params={"event_type_prefix": "publish_gate_", "limit": 20})
    assert r.status_code == 200
    events = r.json()["events"]
    assert events
    last = events[-1]
    assert "policy_id" in last
    assert "environment" in last
    assert "reason_code" in last
    assert "reason" in last
    assert "context" in last


@pytest.mark.parametrize(
    ("name", "policy_id", "environment", "context", "expected_status", "allowed_error_codes"),
    POLICY_EVAL_CASES,
)
def test_policy_evaluate_matrix(
    name: str,
    policy_id: str,
    environment: str,
    context: dict,
    expected_status: int,
    allowed_error_codes: tuple[str, ...],
):
    r = _eval_policy(policy_id, environment, context)
    assert r.status_code == expected_status
    data = r.json()
    if expected_status == 200:
        assert data["allowed"] is True
        assert data["policy_id"] == policy_id
        assert data["environment"] == environment
        return
    detail = data.get("detail", {})
    assert detail.get("allowed") is False
    assert detail.get("policy_id") == policy_id
    assert detail.get("environment") == environment
    if allowed_error_codes:
        assert detail.get("error_code") in allowed_error_codes


@pytest.mark.parametrize(
    (
        "name",
        "environment",
        "law",
        "use_optional_tools",
        "approved",
        "expected_statuses",
        "allowed_error_codes",
    ),
    ORCH_CASES,
)
def test_orchestration_plan_gate_matrix(
    name: str,
    environment: str,
    law: list[str],
    use_optional_tools: bool,
    approved: bool,
    expected_statuses: tuple[int, ...],
    allowed_error_codes: tuple[str, ...],
):
    r = _create_orchestration_plan(
        environment=environment,
        law=law,
        use_optional_tools=use_optional_tools,
        approved=approved,
    )
    assert r.status_code in expected_statuses
    body = r.json()
    if r.status_code == 200:
        assert str(body.get("plan_ref", "")).startswith("plan-")
        assert body.get("environment") == environment
        assert body.get("use_optional_tools") == use_optional_tools
        return
    detail = body.get("detail", {})
    if allowed_error_codes:
        assert detail.get("error_code") in allowed_error_codes


@pytest.mark.parametrize(
    ("case", "expected_status", "expected_project_status"),
    APPROVAL_CASES,
)
def test_approval_action_matrix(case: str, expected_status: int, expected_project_status: str | None):
    pid = _create_draft_project(f"approval-matrix-{case}")
    if case == "submit_draft_ok":
        r = _submit_project(pid)
    elif case == "resubmit_pending_rejected":
        assert _submit_project(pid).status_code == 200
        r = _submit_project(pid)
    elif case == "approve_wrong_level_rejected":
        assert _submit_project(pid, ["L3", "L2"]).status_code == 200
        r = client.post(f"/api/v1/projects/{pid}/approve", json={"level": "L2"})
    elif case == "approve_single_step_ok":
        assert _submit_project(pid, ["L3"]).status_code == 200
        r = client.post(f"/api/v1/projects/{pid}/approve", json={"level": "L3"})
    elif case == "reject_wrong_level_rejected":
        assert _submit_project(pid, ["L3", "L2"]).status_code == 200
        r = client.post(f"/api/v1/projects/{pid}/reject", json={"level": "L2", "reason": "wrong level"})
    elif case == "reject_current_level_ok":
        assert _submit_project(pid, ["L3", "L2"]).status_code == 200
        r = client.post(f"/api/v1/projects/{pid}/reject", json={"level": "L3", "reason": "budget"})
    else:
        raise AssertionError(f"unknown case: {case}")

    assert r.status_code == expected_status
    if expected_project_status is not None:
        assert r.json()["status"] == expected_project_status


@pytest.mark.parametrize(
    ("params", "expect_nonempty"),
    AUDIT_CONSISTENCY_CASES,
)
def test_audit_events_and_summary_consistency_matrix(params: dict, expect_nonempty: bool):
    _seed_audit_events_for_consistency()
    events_params = {k: v for k, v in params.items() if k != "reason_code_prefix"}
    events_resp = client.get("/api/v1/audit/events", params={**events_params, "limit": 5000})
    assert events_resp.status_code == 200
    events = events_resp.json()["events"]
    rpfx = params.get("reason_code_prefix")
    if rpfx:
        events = [e for e in events if str(e.get("reason_code", "")).startswith(str(rpfx))]

    summary_resp = client.get("/api/v1/audit/summary", params={**params, "days": 31, "top_limit": 10})
    assert summary_resp.status_code == 200
    summary = summary_resp.json()

    if expect_nonempty:
        assert len(events) > 0
        assert summary["total_events"] > 0
    else:
        assert len(events) == 0
        assert summary["total_events"] == 0

    assert summary["total_events"] == len(events)
    total_from_trend = sum(int(x.get("total", 0)) for x in summary.get("trend", []))
    denied_from_trend = sum(int(x.get("denied", 0)) for x in summary.get("trend", []))
    assert total_from_trend == summary["total_events"]
    assert denied_from_trend == summary["total_denied"]


@pytest.mark.parametrize(
    (
        "name",
        "kind",
        "environment",
        "runtime_mode",
        "law",
        "approved",
        "use_optional_tools",
        "expected_status",
        "allowed_error_codes",
    ),
    SECURITY_SAMPLING_CASES,
)
def test_security_high_risk_approval_sampling_matrix(
    name: str,
    kind: str,
    environment: str,
    runtime_mode: str,
    law: list[str],
    approved: bool,
    use_optional_tools: bool,
    expected_status: int,
    allowed_error_codes: tuple[str, ...],
):
    """D3-05 抽测：未审批高风险动作在 staging/prod 必须拒绝。"""
    _set_runtime_mode(runtime_mode)
    try:
        if kind == "publish":
            r = client.post(
                "/api/v1/contents/publish",
                json={
                    "title": f"d3-05-{name}",
                    "content": "security-sampling",
                    "environment": environment,
                    "law": law,
                    "approved": approved,
                },
            )
        elif kind == "orchestration":
            r = _create_orchestration_plan(
                environment=environment,
                law=law,
                use_optional_tools=use_optional_tools,
                approved=approved,
            )
        else:
            raise AssertionError(f"unknown kind: {kind}")

        assert r.status_code == expected_status
        if expected_status != 200 and allowed_error_codes:
            detail = r.json().get("detail", {})
            assert detail.get("error_code") in allowed_error_codes
    finally:
        _set_runtime_mode("normal")
