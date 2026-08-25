from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_security_toolkit_routes_without_aggregating_authority():
    root = Path("skills/security-toolkit")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "separate owner authorization from technical capability",
        "never kill processes by broad name/pattern alone",
        "compose specialist skills rather than copying their mechanics",
        "username/account-name match is not identity proof",
        "alone is not control-efficacy proof",
        "do not turn a blocked security lane into an unrestricted shell",
    ):
        assert required in lower
    assert (root / "references/security-routing-matrix.md").exists()
