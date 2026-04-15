from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException

from app.core.policy_engine import PolicyEngine


def require_staging_yaml_acks(*, engine: PolicyEngine, acks: Dict[str, Any]) -> None:
    """staging 预检：对 environment_policy.staging 的每个键要求显式 ack（值为 True）。"""
    staging = engine.get_environment_policy("staging")
    if not staging:
        raise HTTPException(
            status_code=500,
            detail={"error_code": "STAGING_POLICY_CONFIG_MISSING", "reason": "policy YAML 缺少 staging 环境块"},
        )
    missing = [k for k in staging if not acks.get(k)]
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "STAGING_POLICY_ACKS_INCOMPLETE",
                "reason": "staging 须对 environment_policy.staging 全部键提交 staging_policy_acks 且为 true",
                "missing_ack_keys": missing,
                "required_keys": list(staging.keys()),
            },
        )
