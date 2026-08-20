from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_systematic_debugging_preserves_root_cause_contract():
    text=Path('skills/systematic-debugging/SKILL.md').read_text()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    assert '\\n' not in text
    lower=text.lower()
    for required in ('feedback loop','falsifiable hypotheses','one variable','three materially different fix attempts','regression test'):
        assert required in lower
