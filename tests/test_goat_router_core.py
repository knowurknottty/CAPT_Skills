from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_goat_router_is_compact_domain_neutral_and_contract_clean():
    text = Path('skills/goat-skill-router-core-contract/SKILL.md').read_text()
    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    lower = text.lower()
    for leaked in ('android', 'capt', 'play store'):
        assert leaked not in lower
    assert 'exactly one primary' in lower
    assert 'zero to two support' in lower
    assert '`pass`, `fix`, `no-go`, or `blocked`' in lower
