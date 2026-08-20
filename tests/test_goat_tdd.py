from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_tdd_preserves_observed_red_green_contract():
    text=Path('skills/test-driven-development/SKILL.md').read_text(); lower=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for required in ('prove red','minimal','prove green','vertical behavior slice','contain first','systematic-debugging'):
        assert required in lower
