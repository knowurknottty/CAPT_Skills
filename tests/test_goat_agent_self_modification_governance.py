from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_self_modification_governance_separates_authorship_and_permission():
    root=Path('skills/agent-self-modification-governance'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('authorship is not permission','enumerate future-behavior stores and writers','capture recovery state before control changes','outside runtime discovery','prove the guard fires','run negative controls','reject self-correction as authority'):
        assert phrase in low
    assert (root/'references/self-modification-control-plane.md').exists()
