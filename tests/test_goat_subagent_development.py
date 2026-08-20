from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_subagent_development_enforces_isolated_reviewed_execution():
    text=Path('skills/subagent-driven-development/SKILL.md').read_text(); lower=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    for required in ('dependency dag','spec-compliance review first','quality review second','overlapping mutable authority','integrate topologically'):
        assert required in lower
    assert 'delegate_task' not in text
