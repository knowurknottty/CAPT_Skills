from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_registry_driven_ecosystem_has_one_metadata_authority():
    root = Path("skills/registry-driven-ecosystem")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "model semantic relationships",
        "field-level provenance",
        "separate authored from generated artifacts",
        "validate semantics, not just json shape",
        "build reproducibly",
        "must not fork canonical project/system facts",
    ):
        assert required in lower
    assert (root / "references/relationship-and-provenance.md").exists()
    assert (root / "references/compatibility-and-generation.md").exists()
