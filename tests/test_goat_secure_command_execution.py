from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_secure_command_execution_is_positive_grammar_and_fail_closed():
    root = Path("skills/secure-command-execution")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "authorization must be decided upstream",
        "positive capability profile",
        "execute without an implicit shell",
        "redact structurally",
        "forbidden effects",
        "do not fall back to a more permissive executor",
    ):
        assert required in lower
    assert (root / "references/command-capability-profile.md").exists()
