from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_frozen_baseline_integration_preserves_proven_layers():
    root=Path('skills/frozen-baseline-integration'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('authoritative remote target ref','do not squash/rebase/force-push proven layers','detect supersession','metadata repair must not masquerade as ancestry repair','verify integrated target fresh'):
        assert phrase in low
    assert (root/'references/supersession-and-retargeting.md').exists()
