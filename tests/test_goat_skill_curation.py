from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_skill_curation_cannot_self_authorize_mutation():
    root=Path('skills/skill-curation'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('curation does not grant itself mutation authority','map trigger collisions','preserve provenance','test behavior, not formatting','mutate only through the authorized promotion path'):
        assert phrase in low
    assert (root/'references/curation-dispositions.md').exists()
