from pathlib import Path

from goat_forge.inventory import SkillRecord
from goat_forge.scoring import build_score_index, rank_score_cards, score_skill


def record(
    name: str = "systematic-debugging",
    *,
    status: str = "LIVE",
    frontmatter: str = "OK",
    files: int = 1,
    digest: str = "a" * 64,
    description: str | None = None,
) -> SkillRecord:
    return SkillRecord(
        source_lane="live",
        source_path=f"/tmp/{name}",
        relative_path=f"software/{name}",
        name=name,
        description=description or f"Use when {name} is needed",
        file_count=files,
        byte_count=1000,
        symlink_count=0,
        tree_sha256=digest,
        frontmatter_status=frontmatter,
        discovery_status=status,
    )


def test_verification_and_recovery_raise_structural_score():
    base = """# Debugging
## When to Use
Use when failures are unclear.
## Workflow
1. Reproduce.
2. Isolate.
"""
    strong = base + """## Verification
Run the test and require evidence before PASS.
## Failure Recovery
If blocked, rollback, retry safely, and fail closed.
"""
    weak = score_skill(record(), base)
    hardened = score_skill(record(), strong)
    assert hardened.verification_discipline > weak.verification_discipline
    assert hardened.recovery_semantics > weak.recovery_semantics
    assert hardened.auto_score > weak.auto_score


def test_bounded_trigger_beats_broad_trigger_capture():
    broad = "Use this for any software task or whenever help may be useful."
    bounded = """## When to Use
Use when a reproducible software failure requires root-cause isolation.
## Do Not Use
Do not use for feature design, general refactoring, or known one-line syntax fixes.
"""
    assert score_skill(record(), bounded).trigger_precision > score_skill(record(), broad).trigger_precision


def test_bloated_skill_scores_lower_context_efficiency():
    compact = "# Skill\n## When to Use\nUse when needed.\n" + "Do the work carefully. " * 80
    bloated = "# Skill\n## When to Use\nUse when needed.\n" + "Repeat unbounded detail. " * 1800
    compact_card = score_skill(record(), compact)
    bloated_card = score_skill(record(), bloated)
    assert compact_card.context_efficiency > bloated_card.context_efficiency
    assert compact_card.auto_score > bloated_card.auto_score


def test_malformed_frontmatter_is_penalized():
    text = "# Skill\n## When to Use\nUse when needed.\n## Verification\nVerify evidence.\n"
    good = score_skill(record(frontmatter="OK"), text)
    bad = score_skill(record(frontmatter="MALFORMED"), text)
    assert good.auto_score > bad.auto_score
    assert bad.metadata_penalty < 0


def test_archived_source_is_penalized_without_erasing_quality_signal():
    text = """## When to Use
Use when a failure needs isolation.
## Verification
Verify the fix with the reproducer.
"""
    live = score_skill(record(status="LIVE"), text)
    archived = score_skill(record(status="ARCHIVED"), text)
    assert archived.discovery_penalty < 0
    assert live.auto_score > archived.auto_score


def test_duplicate_and_version_near_duplicate_names_are_penalized():
    one = record("debugging-guide-v1", digest="1" * 64)
    two = record("debugging-guide-v2", digest="2" * 64)
    three = record("debugging-guide-v1", digest="1" * 64)
    index = build_score_index([one, two, three])
    card = score_skill(one, "# Debug\nUse when debugging.\n", index=index)
    assert card.duplication_penalty < 0
    assert index.exact_digest_counts[one.tree_sha256] == 2
    assert index.canonical_name_counts["debugging-guide"] == 3


def test_auto_score_does_not_fake_semantic_judgment():
    card = score_skill(
        record(files=6),
        "# Skill\n## When to Use\nUse when needed.\n## Verification\nVerify with tests.\n",
    )
    assert card.capability_leverage is None
    assert card.uniqueness is None
    assert card.review_state == "AUTO"
    assert 0 <= card.auto_score <= 100


def test_support_files_improve_progressive_disclosure_signal():
    text = "Use when needed. See references/details.md and scripts/check.py."
    thin = score_skill(record(files=1), text)
    supported = score_skill(record(files=6), text)
    assert supported.support_depth > thin.support_depth


def test_rank_score_cards_is_deterministic_on_ties():
    alpha = score_skill(record("alpha", digest="1" * 64), "Use when alpha is needed.")
    beta = score_skill(record("beta", digest="2" * 64), "Use when beta is needed.")
    ranked = rank_score_cards([beta, alpha])
    assert [card.name for card in ranked] == ["alpha", "beta"]


def test_security_and_composition_contracts_are_visible_dimensions():
    weak = "Use when deploying code."
    strong = """Use when deploying code within an approved scope.
## Authority
Do not exceed the declared filesystem scope; delegate secrets to the credential owner.
## Security
Require approval for destructive effects, sandbox untrusted input, and fail closed on authority mismatch.
"""
    weak_card = score_skill(record(), weak)
    strong_card = score_skill(record(), strong)
    assert strong_card.composability > weak_card.composability
    assert strong_card.security_fail_closed > weak_card.security_fail_closed
