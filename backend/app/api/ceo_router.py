from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from app.agents.ceo_agent import plan as ceo_plan
from app.core.deps import get_audit_store, get_json_store, get_policy_engine
from app.core.policy_guard import require_policy_allowed
from app.core.store import JsonStore
from app.schemas.common_enums import empty_priority_counts, VALID_DOMAIN_CODES
from app.schemas.ceo import (
    CEOPlanningApplyRequest,
    CEOPlanningApplyResponse,
    CEOPlanningRequest,
    CEOPlanningResponse,
)

router = APIRouter(tags=["ceo"])


def _count_by_priority(rows: list[dict]) -> dict[str, int]:
    out = empty_priority_counts()
    for row in rows:
        p = str(row.get("priority", "P2"))
        if p in out:
            out[p] += 1
    return out


def _count_by_intent_source(rows: list[dict], primary_intent: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        src = str(row.get("source_intent") or primary_intent).strip() or primary_intent
        out[src] = out.get(src, 0) + 1
    return out


def _safe_domain_code(value: object) -> str:
    code = str(value or "").strip().upper()
    return code if code in VALID_DOMAIN_CODES else "D03"


def _normalize_plan_subtasks(plan: dict) -> None:
    for st in list(plan.get("subtasks", [])):
        st["suggested_domain"] = _safe_domain_code(st.get("suggested_domain"))


def _normalize_task_name(value: object) -> str:
    name = str(value or "").strip()
    return name or "未命名任务"


def _normalize_name_key(value: object) -> str:
    return str(value or "").strip().lower()


def _resolve_no_op_reason(
    *,
    planned_count: int,
    filtered_count: int,
    to_apply_count: int,
    created_or_would_create_count: int,
    skipped_duplicates: int,
) -> str:
    if created_or_would_create_count != 0:
        return ""
    if planned_count == 0:
        return "PLAN_EMPTY"
    if filtered_count == 0:
        return "FILTERED_OUT"
    if to_apply_count == 0:
        return "LIMITED_TO_ZERO"
    if skipped_duplicates > 0:
        return "DEDUPED_ALL"
    return "NO_ELIGIBLE_TASKS"


def _select_subtasks(
    subtasks: list[dict], create_priorities: list[str], max_create_tasks: int | None
) -> tuple[list[dict], list[dict]]:
    if create_priorities:
        allowed = set(create_priorities)
        filtered = [st for st in subtasks if str(st.get("priority", "P2")) in allowed]
    else:
        filtered = subtasks
    to_apply = filtered if max_create_tasks is None else filtered[:max_create_tasks]
    return filtered, to_apply


def _get_project_or_404(store: JsonStore, project_id: str) -> dict:
    try:
        return store.get_project(project_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


def _build_preview_dependency_graph(
    task_names: list[str], base_task_id: str | None
) -> tuple[list[dict], list[dict]]:
    dependency_preview: list[dict] = []
    dependency_edges: list[dict] = []
    prev_preview_id = base_task_id
    for name in task_names:
        current_preview_id = f"preview-{len(dependency_edges) + 1}"
        dependency_preview.append({"name": name, "depends_on_task_id": prev_preview_id})
        dependency_edges.append(
            {
                "task_id": current_preview_id,
                "task_name": name,
                "depends_on_task_ids": [prev_preview_id] if prev_preview_id else [],
            }
        )
        prev_preview_id = current_preview_id
    return dependency_preview, dependency_edges


def _build_applied_dependency_edges(tasks: list[dict]) -> list[dict]:
    return [
        {
            "task_id": str(t.get("id", "")),
            "depends_on_task_ids": [str(x) for x in (t.get("dependencies") or []) if str(x)],
        }
        for t in tasks
        if str(t.get("id", ""))
    ]


def _dry_run_execution_defaults() -> dict:
    return {
        "created_tasks": [],
        "created_task_ids": [],
        "created_task_id_map": {},
        "applied_dependency_edges": [],
        "applied_count": 0,
        "applied_by_priority": empty_priority_counts(),
        "applied_by_intent_source": {},
        "intent_source_delta": {},
        "applied_risk_flags": [],
        "applied_risk_summary": {"high": [], "medium": []},
        "applied_risk_score": 0,
        "risk_alignment": "consistent",
        "next_action_hint": "READY_TO_APPLY",
        "decision_snapshot": {},
    }


def _execution_would_defaults() -> dict:
    return {
        "would_create": 0,
        "would_filter": 0,
        "would_apply": 0,
        "would_apply_by_priority": empty_priority_counts(),
        "would_skip_duplicates": 0,
        "would_skip_duplicate_names": [],
        "would_create_task_names": [],
        "would_create_by_intent_source": {},
        "would_dependency_preview": [],
        "would_dependency_edges": [],
        "would_risk_flags": [],
        "would_risk_summary": {"high": [], "medium": []},
        "would_risk_score": 0,
        "would_no_op": False,
        "would_no_op_reason": "",
    }


def _intent_source_delta(estimated: dict[str, int], applied: dict[str, int]) -> dict[str, int]:
    keys = set(estimated.keys()) | set(applied.keys())
    delta: dict[str, int] = {}
    for k in keys:
        d = int(applied.get(k, 0)) - int(estimated.get(k, 0))
        if d != 0:
            delta[k] = d
    return delta


def _build_would_risk_flags(
    *,
    planned_count: int,
    filtered_count: int,
    to_apply_count: int,
    would_skip_duplicates: int,
    would_no_op_reason: str,
) -> list[str]:
    flags: list[str] = []
    if to_apply_count < filtered_count:
        flags.append("LIMIT_TRUNCATION")
    if filtered_count < planned_count:
        flags.append("PRIORITY_FILTER_IMPACT")
    if would_skip_duplicates > 0:
        flags.append("DEDUPE_IMPACT")
    if would_no_op_reason:
        flags.append(f"NO_OP_{would_no_op_reason}")
    return flags


def _build_applied_risk_flags(
    *,
    planned_count: int,
    filtered_count: int,
    applied_count: int,
    skipped_duplicates: int,
    no_op_reason: str,
) -> list[str]:
    flags: list[str] = []
    if applied_count < filtered_count:
        flags.append("LIMIT_OR_RUNTIME_TRUNCATION")
    if filtered_count < planned_count:
        flags.append("PRIORITY_FILTER_IMPACT")
    if skipped_duplicates > 0:
        flags.append("DEDUPE_IMPACT")
    if no_op_reason:
        flags.append(f"NO_OP_{no_op_reason}")
    return flags


def _build_would_risk_summary(flags: list[str]) -> dict[str, list[str]]:
    high_prefixes = ("NO_OP_",)
    high_exact = {"DEDUPE_IMPACT", "LIMIT_TRUNCATION"}
    summary = {"high": [], "medium": []}
    for flag in flags:
        if flag in high_exact or any(flag.startswith(p) for p in high_prefixes):
            summary["high"].append(flag)
        else:
            summary["medium"].append(flag)
    return summary


def _calc_would_risk_score(summary: dict[str, list[str]]) -> int:
    high = len(summary.get("high", []))
    medium = len(summary.get("medium", []))
    return high * 10 + medium * 3


def _next_action_hint(*, risk_alignment: str, high_count: int, dry_run: bool) -> str:
    if dry_run:
        if high_count >= 2:
            return "REVIEW_HIGH_RISK_BEFORE_APPLY"
        if high_count == 1:
            return "TUNE_PARAMS_THEN_APPLY"
        return "READY_TO_APPLY"
    if risk_alignment == "drifted":
        return "RECHECK_PLAN_AND_RERUN_DRY_RUN"
    return "EXECUTION_OK_CONTINUE"


def _build_decision_snapshot(
    *,
    dry_run: bool,
    risk_alignment: str,
    would_risk_score: int,
    applied_risk_score: int,
    next_action_hint: str,
    intent_source_delta: dict[str, int],
) -> dict[str, object]:
    score = int(applied_risk_score if not dry_run else would_risk_score)
    risk_diff = int(applied_risk_score) - int(would_risk_score)
    if risk_diff > 0:
        risk_trend = "up"
    elif risk_diff < 0:
        risk_trend = "down"
    else:
        risk_trend = "flat"
    if score >= 20:
        confidence_band = "low"
    elif score >= 10:
        confidence_band = "medium"
    else:
        confidence_band = "high"
    blocking_reasons: list[dict[str, str]] = []
    for key, value in intent_source_delta.items():
        if int(value) < 0:
            blocking_reasons.append(
                {
                    "code": "INTENT_SOURCE_REDUCED",
                    "message": f"意图来源 {key} 的执行任务数低于预估",
                    "severity": "high",
                }
            )
    if confidence_band == "low":
        blocking_reasons.append(
            {
                "code": "HIGH_RISK_SCORE",
                "message": "风险分值较高，建议先复核后再执行",
                "severity": "high",
            }
        )
    if dry_run:
        if confidence_band == "high":
            recommended_mode = "apply_now"
        elif confidence_band == "medium":
            recommended_mode = "dry_run_again"
        else:
            recommended_mode = "manual_review"
    else:
        if risk_alignment == "drifted":
            recommended_mode = "dry_run_again"
        elif confidence_band == "low":
            recommended_mode = "manual_review"
        else:
            recommended_mode = "apply_now"
    if recommended_mode == "manual_review":
        ui_priority = "p0"
    elif recommended_mode == "dry_run_again":
        ui_priority = "p1"
    else:
        ui_priority = "p2"
    if recommended_mode == "manual_review":
        recommended_actions = ["open_risk_panel", "notify_owner", "require_manual_approval"]
    elif recommended_mode == "dry_run_again":
        recommended_actions = ["adjust_filters_or_limits", "rerun_dry_run"]
    else:
        recommended_actions = ["apply_now", "track_execution_result"]
    return {
        "dry_run": dry_run,
        "risk_alignment": risk_alignment,
        "would_risk_score": int(would_risk_score),
        "applied_risk_score": int(applied_risk_score),
        "risk_diff": risk_diff,
        "risk_trend": risk_trend,
        "confidence_band": confidence_band,
        "recommended_mode": recommended_mode,
        "ui_priority": ui_priority,
        "recommended_actions": recommended_actions,
        "next_action_hint": next_action_hint,
        "intent_source_delta": dict(intent_source_delta),
        "blocking_reasons": blocking_reasons,
    }


def _build_decision_log_body(
    *,
    dry_run: bool,
    next_action_hint: str,
    snapshot: dict[str, object],
) -> str:
    mode = "DRY_RUN" if dry_run else "APPLY"
    recommended_mode = str(snapshot.get("recommended_mode", ""))
    ui_priority = str(snapshot.get("ui_priority", ""))
    confidence_band = str(snapshot.get("confidence_band", ""))
    risk_alignment = str(snapshot.get("risk_alignment", ""))
    risk_diff = int(snapshot.get("risk_diff", 0))
    actions = ", ".join(str(x) for x in (snapshot.get("recommended_actions") or []))
    return (
        f"[CEO_DECISION][{mode}] next_action_hint={next_action_hint}; "
        f"recommended_mode={recommended_mode}; ui_priority={ui_priority}; "
        f"confidence_band={confidence_band}; risk_alignment={risk_alignment}; "
        f"risk_diff={risk_diff}; recommended_actions={actions}"
    )


def _append_decision_discussion(
    *,
    store: JsonStore,
    project_id: str,
    dry_run: bool,
    next_action_hint: str,
    snapshot: dict[str, object],
) -> str | None:
    try:
        row = store.add_project_discussion(
            project_id=project_id,
            author="ceo-system",
            body=_build_decision_log_body(
                dry_run=dry_run,
                next_action_hint=next_action_hint,
                snapshot=snapshot,
            ),
        )
        return str(row.get("id")) if row.get("id") else None
    except Exception:
        # 决策日志沉淀失败不应阻断主流程。
        return None


def _append_decision_audit(
    *,
    audit,
    request: Request,
    environment: str,
    dry_run: bool,
    next_action_hint: str,
    decision_log_id: str | None,
    snapshot: dict[str, object],
) -> None:
    try:
        audit.add(
            event_type="ceo_planning_apply_decision",
            policy_id="CEO-POLICY-09",
            policy_version="runtime",
            environment=environment,
            allowed=True,
            reason=f"decision snapshot generated ({'dry_run' if dry_run else 'apply'})",
            reason_code="DECISION_SNAPSHOT",
            endpoint=str(request.url.path),
            context={
                "dry_run": dry_run,
                "next_action_hint": next_action_hint,
                "recommended_mode": snapshot.get("recommended_mode"),
                "ui_priority": snapshot.get("ui_priority"),
                "confidence_band": snapshot.get("confidence_band"),
                "risk_alignment": snapshot.get("risk_alignment"),
                "risk_diff": snapshot.get("risk_diff"),
                "decision_log_id": decision_log_id,
            },
        )
    except Exception:
        # 审计写入失败不阻断主流程。
        return


@router.post("/ceo/planning", response_model=CEOPlanningResponse)
def ceo_planning(
    payload: CEOPlanningRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
    store: JsonStore = Depends(get_json_store),
):
    require_policy_allowed(
        engine=engine,
        audit=audit,
        request=request,
        policy_id="CEO-POLICY-09",
        environment=payload.environment,
        context={"law": payload.law or [], "explainable": True},
        event_type="ceo_planning_policy_09",
    )
    project = None
    if payload.project_id:
        project = _get_project_or_404(store, payload.project_id)
    plan = ceo_plan(payload.instruction, project)
    _normalize_plan_subtasks(plan)
    return plan


@router.post("/ceo/planning/apply", response_model=CEOPlanningApplyResponse)
def ceo_planning_apply(
    payload: CEOPlanningApplyRequest,
    request: Request,
    engine=Depends(get_policy_engine),
    audit=Depends(get_audit_store),
    store: JsonStore = Depends(get_json_store),
):
    require_policy_allowed(
        engine=engine,
        audit=audit,
        request=request,
        policy_id="CEO-POLICY-09",
        environment=payload.environment,
        context={"law": payload.law or [], "explainable": True},
        event_type="ceo_planning_apply_policy_09",
    )
    project = _get_project_or_404(store, payload.project_id)
    plan = ceo_plan(payload.instruction, project)
    _normalize_plan_subtasks(plan)
    subtasks = list(plan.get("subtasks", []))
    filtered, to_apply = _select_subtasks(
        subtasks=subtasks,
        create_priorities=[str(x) for x in payload.create_priorities],
        max_create_tasks=payload.max_create_tasks,
    )
    existing_name_set: set[str] = set()
    preview_base_task_id: str | None = None
    if payload.dedupe_by_name:
        existing, _total = store.list_tasks(project_id=payload.project_id, limit=500, offset=0)
        existing_name_set = {
            key for key in (_normalize_name_key(t.get("name", "")) for t in existing) if key
        }
    if payload.start_after_task_id:
        try:
            base_task = store.get_task(payload.start_after_task_id)
        except KeyError as e:
            raise HTTPException(status_code=404, detail=str(e))
        if str(base_task.get("project_id")) != payload.project_id:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "TASK_PROJECT_MISMATCH",
                    "reason": "start_after_task_id does not belong to project_id",
                },
            )
        preview_base_task_id = str(base_task["id"])
    elif payload.link_to_latest_existing:
        existing, _total = store.list_tasks(project_id=payload.project_id, limit=500, offset=0)
        if existing:
            preview_base_task_id = str(existing[-1]["id"])
    if payload.dry_run:
        would_skip_duplicates = 0
        skipped_duplicate_names: list[str] = []
        would_create_task_names: list[str] = []
        would_create_rows: list[dict] = []
        if payload.dedupe_by_name:
            local_seen = set(existing_name_set)
            for st in to_apply:
                original_name = _normalize_task_name(st.get("title"))
                nm = _normalize_name_key(original_name)
                if not nm.strip():
                    continue
                if nm in local_seen:
                    would_skip_duplicates += 1
                    skipped_duplicate_names.append(original_name)
                else:
                    local_seen.add(nm)
                    would_create_task_names.append(original_name)
                    would_create_rows.append(st)
        else:
            would_create_task_names = [_normalize_task_name(st.get("title")) for st in to_apply]
            would_create_rows = list(to_apply)
        dependency_preview, would_dependency_edges = _build_preview_dependency_graph(
            would_create_task_names, preview_base_task_id
        )
        would_apply_by_priority = _count_by_priority(to_apply)
        primary_intent = str((plan.get("intent") or {}).get("primary") or "general_coordination")
        would_create_by_intent_source = _count_by_intent_source(would_create_rows, primary_intent)
        would_no_op = len(would_create_task_names) == 0
        would_no_op_reason = _resolve_no_op_reason(
            planned_count=len(subtasks),
            filtered_count=len(filtered),
            to_apply_count=len(to_apply),
            created_or_would_create_count=len(would_create_task_names),
            skipped_duplicates=would_skip_duplicates,
        )
        would_risk_flags = _build_would_risk_flags(
            planned_count=len(subtasks),
            filtered_count=len(filtered),
            to_apply_count=len(to_apply),
            would_skip_duplicates=would_skip_duplicates,
            would_no_op_reason=would_no_op_reason,
        )
        would_risk_summary = _build_would_risk_summary(would_risk_flags)
        would_risk_score = _calc_would_risk_score(would_risk_summary)
        next_action_hint = _next_action_hint(
            risk_alignment="consistent",
            high_count=len(would_risk_summary.get("high", [])),
            dry_run=True,
        )
        decision_snapshot = _build_decision_snapshot(
            dry_run=True,
            risk_alignment="consistent",
            would_risk_score=would_risk_score,
            applied_risk_score=0,
            next_action_hint=next_action_hint,
            intent_source_delta={},
        )
        decision_log_id = _append_decision_discussion(
            store=store,
            project_id=payload.project_id,
            dry_run=True,
            next_action_hint=next_action_hint,
            snapshot=decision_snapshot,
        )
        _append_decision_audit(
            audit=audit,
            request=request,
            environment=payload.environment,
            dry_run=True,
            next_action_hint=next_action_hint,
            decision_log_id=decision_log_id,
            snapshot=decision_snapshot,
        )
        return {
            "plan": plan,
            **_dry_run_execution_defaults(),
            "filtered_count": len(filtered),
            "planned_count": len(subtasks),
            "skipped_duplicates": would_skip_duplicates,
            "skipped_duplicate_names": skipped_duplicate_names,
            "no_op": would_no_op,
            "no_op_reason": would_no_op_reason,
            "would_create": len(subtasks),
            "would_filter": len(filtered),
            "would_apply": len(to_apply),
            "would_apply_by_priority": would_apply_by_priority,
            "would_skip_duplicates": would_skip_duplicates,
            "would_skip_duplicate_names": skipped_duplicate_names,
            "would_create_task_names": would_create_task_names,
            "would_create_by_intent_source": would_create_by_intent_source,
            "would_dependency_preview": dependency_preview,
            "would_dependency_edges": would_dependency_edges,
            "would_risk_flags": would_risk_flags,
            "would_risk_summary": would_risk_summary,
            "would_risk_score": would_risk_score,
            "next_action_hint": next_action_hint,
            "decision_snapshot": decision_snapshot,
            "decision_log_id": decision_log_id,
            "would_no_op": would_no_op,
            "would_no_op_reason": would_no_op_reason,
        }
    created: list[dict] = []
    applied_source_rows: list[dict] = []
    prev_id: str | None = preview_base_task_id
    skipped_duplicates = 0
    skipped_duplicate_names: list[str] = []
    for st in to_apply:
        task_name = _normalize_task_name(st.get("title"))
        task_name_key = _normalize_name_key(task_name)
        if payload.dedupe_by_name and task_name_key and task_name_key in existing_name_set:
            skipped_duplicates += 1
            skipped_duplicate_names.append(task_name)
            continue
        dom = _safe_domain_code(st.get("suggested_domain"))
        desc = f"【{dom}】{st.get('context', '')}"
        record = {
            "project_id": payload.project_id,
            "name": task_name,
            "description": desc,
            "priority": str(st.get("priority", "P2")),
            "status": "pending",
            "dependencies": [prev_id] if prev_id else [],
        }
        try:
            t = store.create_task(record)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        created.append(t)
        applied_source_rows.append(st)
        if payload.dedupe_by_name:
            existing_name_set.add(_normalize_name_key(t.get("name", "")))
        prev_id = str(t["id"])
    no_op_reason = _resolve_no_op_reason(
        planned_count=len(subtasks),
        filtered_count=len(filtered),
        to_apply_count=len(to_apply),
        created_or_would_create_count=len(created),
        skipped_duplicates=skipped_duplicates,
    )
    applied_by_priority = _count_by_priority(created)
    primary_intent = str((plan.get("intent") or {}).get("primary") or "general_coordination")
    applied_by_intent_source = _count_by_intent_source(applied_source_rows, primary_intent)
    estimated_by_intent_source = _count_by_intent_source(to_apply, primary_intent)
    intent_source_delta = _intent_source_delta(estimated_by_intent_source, applied_by_intent_source)
    applied_risk_flags = _build_applied_risk_flags(
        planned_count=len(subtasks),
        filtered_count=len(filtered),
        applied_count=len(created),
        skipped_duplicates=skipped_duplicates,
        no_op_reason=no_op_reason,
    )
    applied_risk_summary = _build_would_risk_summary(applied_risk_flags)
    applied_risk_score = _calc_would_risk_score(applied_risk_summary)
    would_risk_flags = _build_would_risk_flags(
        planned_count=len(subtasks),
        filtered_count=len(filtered),
        to_apply_count=len(to_apply),
        would_skip_duplicates=skipped_duplicates,
        would_no_op_reason=no_op_reason,
    )
    would_risk_summary = _build_would_risk_summary(would_risk_flags)
    would_risk_score = _calc_would_risk_score(would_risk_summary)
    risk_alignment = "consistent" if applied_risk_score <= would_risk_score else "drifted"
    next_action_hint = _next_action_hint(
        risk_alignment=risk_alignment,
        high_count=len(applied_risk_summary.get("high", [])),
        dry_run=False,
    )
    decision_snapshot = _build_decision_snapshot(
        dry_run=False,
        risk_alignment=risk_alignment,
        would_risk_score=would_risk_score,
        applied_risk_score=applied_risk_score,
        next_action_hint=next_action_hint,
        intent_source_delta=intent_source_delta,
    )
    decision_log_id = _append_decision_discussion(
        store=store,
        project_id=payload.project_id,
        dry_run=False,
        next_action_hint=next_action_hint,
        snapshot=decision_snapshot,
    )
    _append_decision_audit(
        audit=audit,
        request=request,
        environment=payload.environment,
        dry_run=False,
        next_action_hint=next_action_hint,
        decision_log_id=decision_log_id,
        snapshot=decision_snapshot,
    )
    created_task_ids = [str(t.get("id", "")) for t in created if str(t.get("id", ""))]
    created_task_id_map = {
        str(t.get("name", "")): str(t.get("id", ""))
        for t in created
        if str(t.get("name", "")) and str(t.get("id", ""))
    }
    applied_dependency_edges = _build_applied_dependency_edges(created)
    return {
        "plan": plan,
        "created_tasks": created,
        "created_task_ids": created_task_ids,
        "created_task_id_map": created_task_id_map,
        "applied_dependency_edges": applied_dependency_edges,
        "applied_count": len(created),
        "applied_by_priority": applied_by_priority,
        "applied_by_intent_source": applied_by_intent_source,
        "intent_source_delta": intent_source_delta,
        "applied_risk_flags": applied_risk_flags,
        "applied_risk_summary": applied_risk_summary,
        "applied_risk_score": applied_risk_score,
        "risk_alignment": risk_alignment,
        "next_action_hint": next_action_hint,
        "decision_snapshot": decision_snapshot,
        "decision_log_id": decision_log_id,
        "filtered_count": len(filtered),
        "planned_count": len(subtasks),
        "skipped_duplicates": skipped_duplicates,
        "skipped_duplicate_names": skipped_duplicate_names,
        "no_op": len(created) == 0,
        "no_op_reason": no_op_reason,
        **_execution_would_defaults(),
    }
