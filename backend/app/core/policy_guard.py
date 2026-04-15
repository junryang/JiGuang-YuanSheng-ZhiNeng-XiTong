from __future__ import annotations

from fastapi import HTTPException, Request

from app.core.audit import AuditStore
from app.core.policy_engine import PolicyDecision, PolicyEngine
from app.schemas.common_enums import Environment


def _deny_detail(decision: PolicyDecision) -> dict:
    return {
        "error_code": decision.error_code,
        "reason": decision.reason,
        "policy_id": decision.policy_id,
        "policy_version": decision.version,
        "environment": decision.environment,
    }


def require_policy_allowed(
    *,
    engine: PolicyEngine,
    audit: AuditStore,
    request: Request,
    policy_id: str,
    environment: Environment,
    context: dict,
    event_type: str,
) -> PolicyDecision:
    """评估策略、写入审计；若拒绝则抛出 403 并携带统一 detail 结构。"""
    decision = engine.evaluate(policy_id, environment, context)
    audit.add(
        event_type=event_type,
        policy_id=decision.policy_id,
        policy_version=decision.version,
        environment=decision.environment,
        allowed=decision.allowed,
        reason=decision.reason,
        reason_code=decision.error_code,
        endpoint=str(request.url.path),
        context={"policy_id": decision.policy_id, "environment": decision.environment},
    )
    if not decision.allowed:
        raise HTTPException(status_code=403, detail=_deny_detail(decision))
    return decision


def require_policy_sequence(
    *,
    engine: PolicyEngine,
    audit: AuditStore,
    request: Request,
    environment: Environment,
    gates: list[tuple[str, dict, str]],
) -> list[PolicyDecision]:
    """按顺序执行多道策略门；任一拒绝即抛出。"""
    out: list[PolicyDecision] = []
    for policy_id, context, event_type in gates:
        out.append(
            require_policy_allowed(
                engine=engine,
                audit=audit,
                request=request,
                policy_id=policy_id,
                environment=environment,
                context=context,
                event_type=event_type,
            )
        )
    return out
