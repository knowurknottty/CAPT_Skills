from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_cross_language_bindings_have_one_semantic_source():
    root=Path('skills/cross-language-schema-bindings'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('normalize once','emit each language from the same model','generate reproducibly','run shared fixtures','prove hermetic consumers','detect repository drift'):
        assert phrase in low
    assert (root/'references/parity-and-determinism.md').exists()
