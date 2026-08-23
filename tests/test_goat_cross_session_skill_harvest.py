from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_cross_session_harvest_emits_candidates_not_mutations():
    root=Path('skills/cross-session-skill-harvest'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('do not create, patch, register, install, or delete live skills','at least two distinct episodes','falsify the pattern','never pad source counts','hand off to curation'):
        assert phrase in low
    assert (root/'references/harvest-candidate-schema.md').exists()
