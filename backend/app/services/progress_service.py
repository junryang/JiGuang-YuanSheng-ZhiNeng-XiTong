from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Tuple


def _effective_progress(task: Dict[str, Any]) -> int:
    if str(task.get("status")) == "completed":
        return 100
    return max(0, min(100, int(task.get("progress", 0))))


def _task_weight(task: Dict[str, Any]) -> float:
    raw = task.get("estimated_hours")
    try:
        w = float(raw) if raw is not None else 1.0
    except (TypeError, ValueError):
        w = 1.0
    return w if w > 0 else 1.0


def weighted_progress_percent(tasks: List[Dict[str, Any]]) -> Tuple[float, Dict[str, Any]]:
    """
    加权平均进度：sum(progress_i * weight_i) / sum(weight_i)，
    weight_i 默认取 estimated_hours，缺失或非法时按 1.0。
    """
    if not tasks:
        return 0.0, {"numerator": 0.0, "denominator": 0.0, "task_count": 0}

    numerator = 0.0
    denominator = 0.0
    for t in tasks:
        w = _task_weight(t)
        p = _effective_progress(t)
        numerator += p * w
        denominator += w

    overall = numerator / denominator if denominator > 0 else 0.0
    meta = {
        "numerator": round(numerator, 4),
        "denominator": round(denominator, 4),
        "task_count": len(tasks),
        "method": "weighted_average_by_estimated_hours",
    }
    return overall, meta


def build_gantt_payload(project_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    for t in tasks:
        rows.append(
            {
                "id": t.get("id"),
                "name": t.get("name"),
                "start_date": t.get("start_date"),
                "end_date": t.get("end_date"),
                "progress": _effective_progress(t),
                "status": t.get("status"),
                "parent_id": t.get("parent_id"),
                "dependencies": list(t.get("dependencies") or []),
                "estimated_hours": t.get("estimated_hours"),
                "priority": t.get("priority"),
            }
        )
    return {"project_id": project_id, "tasks": rows}


def _parse_iso_date(value: Any) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def project_risk_summary(tasks: List[Dict[str, Any]], *, today: date | None = None) -> Dict[str, Any]:
    """
    项目执行风险摘要：
    - blocked_task_count: status=blocked
    - overdue_task_count: end_date < today 且任务未完成
    - no_progress_in_progress_count: in_progress 且 progress=0
    """
    if today is None:
        today = date.today()
    blocked = 0
    overdue = 0
    no_progress_in_progress = 0
    for task in tasks:
        status = str(task.get("status") or "").strip()
        progress = int(task.get("progress", 0) or 0)
        if status == "blocked":
            blocked += 1
        if status == "in_progress" and progress <= 0:
            no_progress_in_progress += 1
        due = _parse_iso_date(task.get("end_date"))
        if due and due < today and status != "completed":
            overdue += 1

    score = blocked * 3 + overdue * 2 + no_progress_in_progress
    if score >= 6:
        level = "high"
    elif score >= 3:
        level = "medium"
    else:
        level = "low"
    return {
        "blocked_task_count": blocked,
        "overdue_task_count": overdue,
        "no_progress_in_progress_count": no_progress_in_progress,
        "risk_score": score,
        "risk_level": level,
    }
