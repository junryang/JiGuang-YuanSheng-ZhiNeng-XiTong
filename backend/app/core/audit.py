from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from app.schemas.common_enums import Environment


@dataclass
class AuditEvent:
    timestamp: str
    event_type: str
    policy_id: str
    policy_version: str
    environment: Environment
    allowed: bool
    reason: str
    reason_code: str
    endpoint: str
    context: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AuditStore:
    def __init__(self) -> None:
        self._events: List[AuditEvent] = []

    def add(
        self,
        *,
        event_type: str,
        policy_id: str,
        policy_version: str,
        environment: Environment,
        allowed: bool,
        reason: str,
        reason_code: str = "UNSPECIFIED",
        endpoint: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._events.append(
            AuditEvent(
                timestamp=datetime.now(timezone.utc).isoformat(),
                event_type=event_type,
                policy_id=policy_id,
                policy_version=policy_version,
                environment=environment,
                allowed=allowed,
                reason=reason,
                reason_code=reason_code,
                endpoint=endpoint,
                context=context or {},
            )
        )

    def list(
        self,
        limit: int = 100,
        *,
        event_type_prefix: Optional[str] = None,
        policy_id: Optional[str] = None,
        environment: Optional[Environment] = None,
    ) -> List[Dict[str, Any]]:
        evs = [e.to_dict() for e in self._events]
        if event_type_prefix and str(event_type_prefix).strip():
            pfx = str(event_type_prefix).strip()
            evs = [e for e in evs if str(e.get("event_type", "")).startswith(pfx)]
        if policy_id and str(policy_id).strip():
            pid = str(policy_id).strip()
            evs = [e for e in evs if str(e.get("policy_id", "")) == pid]
        if environment and str(environment).strip():
            env = str(environment).strip()
            evs = [e for e in evs if str(e.get("environment", "")) == env]
        return evs[-limit:]

    def summary(
        self,
        *,
        days: int = 7,
        event_type_prefix: Optional[str] = None,
        policy_id: Optional[str] = None,
        environment: Optional[Environment] = None,
        reason_code_prefix: Optional[str] = None,
        stage_timeout_hit_only: Optional[bool] = None,
        stage_timeout_env: Optional[Environment] = None,
        stage_timeout_policy_id: Optional[str] = None,
        stage_timeout_reason_code: Optional[str] = None,
        stage_timeout_group_by: Optional[str] = None,
        top_limit: int = 5,
    ) -> Dict[str, Any]:
        ndays = max(1, min(int(days), 31))
        tops = max(1, min(int(top_limit), 20))
        rows = self.list(
            limit=5000,
            event_type_prefix=event_type_prefix,
            policy_id=policy_id,
            environment=environment,
        )
        if reason_code_prefix and str(reason_code_prefix).strip():
            rpfx = str(reason_code_prefix).strip()
            rows = [e for e in rows if str(e.get("reason_code", "")).startswith(rpfx)]
        if stage_timeout_hit_only is not None:
            filtered_rows: List[Dict[str, Any]] = []
            for e in rows:
                if str(e.get("event_type", "")) != "project_stage_timeout_alert":
                    continue
                ctx = e.get("context") or {}
                hits = ctx.get("hits") or {}
                # Backward-compatible: support both nested `hits.*` and legacy top-level context keys.
                stage_hit = bool(hits.get("stage_overdue_hit") is True or ctx.get("stage_overdue_hit") is True)
                approval_hit = bool(hits.get("approval_overdue_hit") is True or ctx.get("approval_overdue_hit") is True)
                merged_hit = bool(stage_hit or approval_hit)
                if merged_hit == bool(stage_timeout_hit_only):
                    filtered_rows.append(e)
            rows = filtered_rows
        if stage_timeout_env and str(stage_timeout_env).strip():
            target_env = str(stage_timeout_env).strip()
            rows = [
                e
                for e in rows
                if str(e.get("event_type", "")) == "project_stage_timeout_alert"
                and str(e.get("environment", "")) == target_env
            ]
        if stage_timeout_policy_id and str(stage_timeout_policy_id).strip():
            target_policy_id = str(stage_timeout_policy_id).strip()
            rows = [
                e
                for e in rows
                if str(e.get("event_type", "")) == "project_stage_timeout_alert"
                and str(e.get("policy_id", "")) == target_policy_id
            ]
        if stage_timeout_reason_code and str(stage_timeout_reason_code).strip():
            target_reason_code = str(stage_timeout_reason_code).strip()
            rows = [
                e
                for e in rows
                if str(e.get("event_type", "")) == "project_stage_timeout_alert"
                and str(e.get("reason_code", "")) == target_reason_code
            ]
        now = datetime.now(timezone.utc).date()
        ordered_days: List[str] = []
        day_map: Dict[str, Dict[str, int]] = {}
        for i in range(ndays - 1, -1, -1):
            d = (now - timedelta(days=i)).isoformat()
            ordered_days.append(d)
            day_map[d] = {"total": 0, "denied": 0}

        deny_map: Dict[str, int] = {}
        for ev in rows:
            ts = str(ev.get("timestamp", ""))
            day = ts[:10]
            if day in day_map:
                day_map[day]["total"] += 1
                if not bool(ev.get("allowed", False)):
                    day_map[day]["denied"] += 1
            if not bool(ev.get("allowed", False)):
                rc = str(ev.get("reason_code") or "UNKNOWN")
                deny_map[rc] = deny_map.get(rc, 0) + 1

        trend = []
        for d in ordered_days:
            total = day_map[d]["total"]
            denied = day_map[d]["denied"]
            allowed = max(0, total - denied)
            allowed_rate = round((allowed / total) * 100, 1) if total > 0 else 100.0
            trend.append(
                {
                    "day": d,
                    "total": total,
                    "denied": denied,
                    "allowed": allowed,
                    "allowed_rate": allowed_rate,
                }
            )
        top_reasons = [{"reason_code": k, "count": v} for k, v in sorted(deny_map.items(), key=lambda x: x[1], reverse=True)[:tops]]
        total_events = len(rows)
        total_denied = sum(1 for e in rows if not bool(e.get("allowed", False)))
        total_allowed = max(0, total_events - total_denied)
        denied_rate = round((total_denied / total_events) * 100, 1) if total_events > 0 else 0.0
        allowed_rate = round((total_allowed / total_events) * 100, 1) if total_events > 0 else 100.0
        # Stage timeout alert explainability aggregates (for ops dashboard).
        sta_rows = [e for e in rows if str(e.get("event_type", "")) == "project_stage_timeout_alert"]
        sta_total = len(sta_rows)
        sta_hit = 0
        sta_miss = 0
        sta_env_map: Dict[str, Dict[str, int]] = {}
        for ev in sta_rows:
            ctx = ev.get("context") or {}
            hits = ctx.get("hits") or {}
            stage_hit = bool(hits.get("stage_overdue_hit") is True or ctx.get("stage_overdue_hit") is True)
            approval_hit = bool(hits.get("approval_overdue_hit") is True or ctx.get("approval_overdue_hit") is True)
            merged_hit = bool(stage_hit or approval_hit)
            if merged_hit:
                sta_hit += 1
            else:
                sta_miss += 1
            env = str(ev.get("environment") or "unknown")
            cell = sta_env_map.setdefault(env, {"total": 0, "hit_count": 0, "miss_count": 0})
            cell["total"] += 1
            if merged_hit:
                cell["hit_count"] += 1
            else:
                cell["miss_count"] += 1
        sta_hit_rate = round((sta_hit / sta_total) * 100, 1) if sta_total > 0 else 0.0
        sta_env_breakdown = [
            {
                "environment": k,
                "total": v["total"],
                "hit_count": v["hit_count"],
                "miss_count": v["miss_count"],
                "hit_rate": round((v["hit_count"] / v["total"]) * 100, 1) if v["total"] > 0 else 0.0,
            }
            for k, v in sorted(sta_env_map.items(), key=lambda x: x[0])
        ]
        sta_grouped: List[Dict[str, Any]] = []
        group_key = str(stage_timeout_group_by or "").strip().lower()
        if group_key in {"environment", "reason_code"}:
            grouped_map: Dict[str, Dict[str, int]] = {}
            for ev in sta_rows:
                ctx = ev.get("context") or {}
                hits = ctx.get("hits") or {}
                stage_hit = bool(hits.get("stage_overdue_hit") is True or ctx.get("stage_overdue_hit") is True)
                approval_hit = bool(hits.get("approval_overdue_hit") is True or ctx.get("approval_overdue_hit") is True)
                merged_hit = bool(stage_hit or approval_hit)
                gval = (
                    str(ev.get("environment") or "unknown")
                    if group_key == "environment"
                    else str(ev.get("reason_code") or "UNKNOWN")
                )
                cell = grouped_map.setdefault(gval, {"total": 0, "hit_count": 0, "miss_count": 0})
                cell["total"] += 1
                if merged_hit:
                    cell["hit_count"] += 1
                else:
                    cell["miss_count"] += 1
            sta_grouped = [
                {
                    "group": g,
                    "total": v["total"],
                    "hit_count": v["hit_count"],
                    "miss_count": v["miss_count"],
                    "hit_rate": round((v["hit_count"] / v["total"]) * 100, 1) if v["total"] > 0 else 0.0,
                }
                for g, v in sorted(grouped_map.items(), key=lambda x: x[0])
            ]
        return {
            "days": ndays,
            "trend": trend,
            "top_reasons": top_reasons,
            "total_events": total_events,
            "total_allowed": total_allowed,
            "total_denied": total_denied,
            "allowed_rate": allowed_rate,
            "denied_rate": denied_rate,
            "stage_timeout_alert_total": sta_total,
            "stage_timeout_alert_hit_count": sta_hit,
            "stage_timeout_alert_miss_count": sta_miss,
            "stage_timeout_alert_hit_rate": sta_hit_rate,
            "stage_timeout_alert_env_breakdown": sta_env_breakdown,
            "stage_timeout_group_by": group_key if group_key in {"environment", "reason_code"} else None,
            "stage_timeout_alert_grouped": sta_grouped,
        }
