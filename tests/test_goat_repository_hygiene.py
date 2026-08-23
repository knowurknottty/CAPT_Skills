from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_repository_hygiene_preserves_unrelated_work():
    root=Path('skills/repository-hygiene'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('filesystem presence and git tracking are separate properties','preserve unique work','define the mutation set','separate concerns','a clean `git status` is not itself proof'):
        assert phrase in low
    assert (root/'references/worktree-and-stash-preservation.md').exists()
