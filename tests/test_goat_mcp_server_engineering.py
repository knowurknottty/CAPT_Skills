from pathlib import Path

from goat_forge.forge_contract import validate_forge_candidate


def test_promoted_mcp_server_engineering_preserves_protocol_and_effect_boundaries():
    root = Path("skills/mcp-server-engineering")
    text = (root / "SKILL.md").read_text()
    lower = text.lower()

    assert validate_forge_candidate(text) == []
    assert len(text.split()) <= 750
    for required in (
        "prefer multiple explicit capabilities",
        "protocol-level success must not wrap",
        "stray stdout is protocol corruption",
        "assume clients may issue overlapping requests",
        "preflight fail-closed obligations",
        "authoritative state",
        "test over a real transport/client",
        "never log raw credential-bearing environment",
    ):
        assert required in lower
    assert (root / "references/mcp-conformance-matrix.md").exists()
