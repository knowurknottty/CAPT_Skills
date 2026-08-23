from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_deep_research_is_evidence_complete_and_format_neutral():
    root = Path("skills/deep-research")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "build a question map",
        "atomize claims",
        "contradiction/falsification pass",
        "check thread saturation",
        "requested medium",
    ):
        assert required in lower
    assert all(token in text for token in ("VERIFIED", "CORROBORATED", "INFERRED", "CONTESTED", "UNVERIFIED"))
    assert (root / "references/source-and-claim-matrix.md").exists()
