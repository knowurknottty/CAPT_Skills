from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_macos_computer_use_is_bound_verified_and_fail_closed():
    root = Path("skills/macos-computer-use")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "discover the active contract",
        "bind the target",
        "target semantically first",
        "do not claim background/focus behavior",
        "reconcile whether the effect occurred",
        "tool call succeeded",
        "prompt injection",
        "another automation path",
    ):
        assert required in lower
    assert (root / "references/interaction-and-verification.md").exists()
    assert (root / "references/sensitive-ui-and-ax-boundaries.md").exists()
