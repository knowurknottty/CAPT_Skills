from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_forensic_architecture_reconstruction_is_evidence_first():
    root = Path("skills/forensic-architecture-reconstruction")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "evidence hierarchy",
        "map executable architecture",
        "compute references/import/call/build reachability",
        "presence is not enforcement",
        "separate reconstruction from evolution",
    ):
        assert required in lower
    assert all(token in text for token in ("VERIFIED", "INFERRED", "UNRESOLVED", "CONTRADICTED"))
    assert (root / "references/reconstruction-evidence-contract.md").exists()
    assert (root / "references/reachability-and-generation.md").exists()
