from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_external_driver_conformance_preserves_host_authority():
    root=Path('skills/external-driver-conformance'); text=(root/'SKILL.md').read_text(); low=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for phrase in ('must not mint host policy decisions','run a bounded real task','treat output as hostile input','exercise interruption and uncertainty','prove removal and substitution'):
        assert phrase in low
    assert (root/'references/authority-boundary-threats.md').exists()
    for leak in ('openharness','ollama','m0-a','m0-b'):
        assert leak not in low
