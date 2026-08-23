from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_codebase_archaeology_is_read_only_and_evidence_qualified():
    root=Path('skills/codebase-archaeology'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('do not mutate discovered projects','counterevidence','coverage and exclusions','forensic-architecture-reconstruction','stop before any move/delete/archive/merge/reset/clean/install'):
        assert phrase in low
    assert (root/'references/bounded-discovery.md').exists()
    assert (root/'references/canonicality-and-lineage.md').exists()
