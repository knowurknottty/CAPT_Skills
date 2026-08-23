from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_continuous_research_cycle_preserves_state_and_marginal_value():
    root = Path("skills/continuous-research-cycle")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "net-new external evidence",
        "marginal-value gate",
        "artifact re-validation into substitute research",
        "orphan evidence directory",
        "exact next-cycle priorities",
    ):
        assert required in lower
    assert (root / "references/cycle-state-contract.md").exists()
    assert (root / "references/source-identity.md").exists()
