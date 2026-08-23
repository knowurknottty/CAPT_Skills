from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_stacked_pr_decomposition_preserves_delta_and_stack_truth():
    root=Path('skills/stacked-pr-decomposition'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('topologically valid','semantically coupled','one primary semantic owner','programmatically prove unique paths/owners','exact head sha','prove terminal equivalence'):
        assert phrase in low
    assert (root/'references/accounting-and-coupling.md').exists()
    assert (root/'references/construction-and-equivalence.md').exists()
