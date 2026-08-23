from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_deployment_resilience_verification_proves_live_chain_and_recovery():
    root = Path("skills/deployment-resilience-verification")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "stamp provenance",
        "probe live behavior",
        "test dependency failure/degraded mode",
        "not one universal fallback policy",
        "verify rollback/recovery",
        "isolate the layer",
    ):
        assert required in lower
    assert (root / "references/deployment-proof-matrix.md").exists()
    assert (root / "references/failure-and-fallback-tests.md").exists()
