from pathlib import Path

from goat_forge.inventory import SkillRecord
from goat_forge.scoring import build_score_index, score_skill


def record(name: str = "systematic-debugging", *, status: str = "LIVE",
           frontmatter: str = "OK", files: int = 1, digest: str = "a" * 64) -> SkillRecord:
    return SkillRecord(
        source_lane="live", source_path=f"/tmp/{name}", relative_path=f"software/{name}",
        name=name, description=f"Use when {name} is needed", file_count=files,
        byte_count=1000, symlink_count=0, tree_sha256=digest,
        frontmatter_status=frontmatter, discovery_status=status,
    )


def test_verification_and_recovery_language_raise_structural_score():
    base = """# Debugging\n## When to Use\nUse when failures are unclear.\n## Workflow\n1. Reproduce.\n2. Isolate.\n"""
    strong = base + """## Verification\nRun the test and require evidence before PASS.\n## Failure Recovery\nIf blocked, rollback, retry safely, and fail closed.\n"""

    weak_score = score_skill(record(), base).auto_score
    strong_score = score_skill(record(), strong).auto_score

    assert strong_score > weak_score


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


def test_support_files_improve_progressive_disclosure_signal():
    text = "# Skill\n## When to Use\nUse when needed.\nSee references/details.md and scripts/check.py.\n"
    thin = score_skill(record(files=1), text)
    supported = score_skill(record(files=6), text)
    assert supported.support_depth > thin.support_depth
