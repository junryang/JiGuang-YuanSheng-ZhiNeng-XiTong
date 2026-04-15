from pathlib import Path

from app.core.policy_engine import PolicyEngine


def test_policy_engine_loads():
    root = Path(__file__).resolve().parents[2]
    engine = PolicyEngine(root / "docs" / "ceo_policy.engine.yaml")
    health = engine.health()
    assert health["loaded"] is True
    assert health["policy_count"] >= 6
    assert engine.version != "unknown"


def test_get_environment_policy_staging():
    root = Path(__file__).resolve().parents[2]
    engine = PolicyEngine(root / "docs" / "ceo_policy.engine.yaml")
    st = engine.get_environment_policy("staging")
    assert st.get("strict_law_bundle") is True
    assert st.get("max_retry") == 2


def test_policy_13_denies_without_law_04():
    root = Path(__file__).resolve().parents[2]
    engine = PolicyEngine(root / "docs" / "ceo_policy.engine.yaml")
    decision = engine.evaluate(
        policy_id="CEO-POLICY-13",
        environment="staging",
        context={"law": ["LAW-01", "LAW-02", "LAW-03", "LAW-05"]},
    )
    assert decision.allowed is False
    assert "LAW-04" in decision.reason
    assert decision.version == engine.version
