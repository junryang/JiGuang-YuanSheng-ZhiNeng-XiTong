from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml
from app.schemas.common_enums import Environment


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str
    error_code: str
    policy_id: str
    environment: Environment
    version: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class PolicyEngine:
    def __init__(self, policy_path: Path) -> None:
        self.policy_path = policy_path
        self._raw = self._load_yaml()
        self._policy_index = {p["id"]: p for p in self._raw.get("policies", [])}
        self.version = str(self._raw.get("version", "unknown"))

    def _load_yaml(self) -> Dict[str, Any]:
        with self.policy_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def health(self) -> Dict[str, Any]:
        envs = list((self._raw.get("environment_policy") or {}).keys())
        return {
            "loaded": bool(self._policy_index),
            "policy_count": len(self._policy_index),
            "environments": envs,
        }

    def get_environment_policy(self, environment: Environment) -> Dict[str, Any]:
        """返回 ceo_policy.engine.yaml 中 environment_policy 下指定环境的配置快照。"""
        block = self._raw.get("environment_policy") or {}
        raw = block.get(environment)
        if raw is None:
            return {}
        if not isinstance(raw, dict):
            return {}
        return dict(raw)

    def evaluate(self, policy_id: str, environment: Environment, context: Dict[str, Any]) -> PolicyDecision:
        policy = self._policy_index.get(policy_id)
        if not policy:
            return PolicyDecision(
                allowed=False,
                reason=f"Unknown policy: {policy_id}",
                error_code="POLICY_UNKNOWN",
                policy_id=policy_id,
                environment=environment,
                version=self.version,
            )

        # Hard stop for known deny conditions used in current YAML design.
        deny_rules: List[str] = policy.get("deny_if", [])
        for rule in deny_rules:
            if rule == "missing(LAW-04)" and "LAW-04" not in context.get("law", []):
                return PolicyDecision(False, "missing LAW-04", "LAW_04_REQUIRED", policy_id, environment, self.version)
            if rule == "missing(LAW-05)" and "LAW-05" not in context.get("law", []):
                return PolicyDecision(False, "missing LAW-05", "LAW_05_REQUIRED", policy_id, environment, self.version)
            if rule == "missing_acceptance_contract" and not context.get("acceptance_contract"):
                return PolicyDecision(
                    False, "missing acceptance contract", "CONTRACT_REQUIRED", policy_id, environment, self.version
                )
            if rule == "unexplainable_decision" and not context.get("explainable", False):
                return PolicyDecision(
                    False, "decision not explainable", "EXPLAINABILITY_REQUIRED", policy_id, environment, self.version
                )
            if rule == "degraded_mode && high_risk_action":
                if context.get("degraded_mode") and context.get("high_risk_action"):
                    return PolicyDecision(
                        False,
                        "high risk action forbidden in degraded mode",
                        "DEGRADED_HIGH_RISK_FORBIDDEN",
                        policy_id,
                        environment,
                        self.version,
                    )
            if rule.startswith("missing_any("):
                body = rule.removeprefix("missing_any(").removesuffix(")")
                required = [x.strip() for x in body.split(",")]
                missing = [x for x in required if x not in context.get("law", [])]
                if missing:
                    return PolicyDecision(
                        False,
                        f"missing required laws: {','.join(missing)}",
                        "LAW_BUNDLE_REQUIRED",
                        policy_id,
                        environment,
                        self.version,
                    )

        return PolicyDecision(True, "allowed", "OK", policy_id, environment, self.version)
