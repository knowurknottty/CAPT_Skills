from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_adversarial_integration_audit_is_read_only_and_falsification_first():
    root = Path("skills/adversarial-integration-audit")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    assert "read-only" in lower
    assert "recompute scope from git" in lower
    assert "do not modify production source" in lower
    assert "forbidden side effect remains absent" in lower
    assert all(token in text for token in ("VERIFIED", "INFERRED", "NOT_VERIFIABLE", "FAILED/BLOCKER"))
    assert (root / "references/control-efficacy-audit.md").exists()
