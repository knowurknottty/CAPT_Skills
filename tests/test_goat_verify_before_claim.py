from pathlib import Path
from goat_forge.forge_contract import validate_forge_candidate

def test_promoted_verify_before_claim_is_scoped_and_progressively_disclosed():
    root=Path('skills/verify-before-claim'); text=(root/'SKILL.md').read_text(); lower=text.lower()
    assert validate_forge_candidate(text)==[]
    assert len(text.split()) <= 750
    assert {'VERIFIED','INFERRED','UNVERIFIED','BLOCKED'} <= set(text.replace('`','').split())
    assert (root/'references/claim-proof-matrix.md').exists()
    assert (root/'references/evidence-preservation-and-falsification.md').exists()
    for required in ('atomize the claim','match evidence to wording','preserve unexpected failure evidence','falsify material claims'):
        assert required in lower
