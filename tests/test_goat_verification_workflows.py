from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_verification_workflows_has_narrow_strategy_authority():
    root = Path("skills/verification-workflows")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    assert "verify-before-claim" in lower
    assert "owns the final claim/evidence status" in lower
    assert "systematic-debugging" in lower
    assert "cross the real boundary" in lower
    assert "never edit the frozen authority" in lower
    assert (root / "references/verification-modes.md").exists()
    assert (root / "references/high-rigor-recipes.md").exists()
