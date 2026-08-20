import shutil
from pathlib import Path

from goat_forge.inventory import iter_skill_records
from goat_forge.profile_inventory import discover_profile_roots, inventory_profile_variants


def make_skill(root: Path, relative: str, name: str, body: str = "Use when needed.\n") -> Path:
    skill = root / relative
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Use when {name} is needed\n---\n# {name}\n{body}"
    )
    return skill


def test_discover_profile_roots_skips_backups_and_empty_profiles(tmp_path: Path):
    profiles = tmp_path / "profiles"
    make_skill(profiles / "author" / "skills", "writing", "writing")
    (profiles / "empty" / "skills").mkdir(parents=True)
    make_skill(profiles / "author.bak.123" / "skills", "old", "old")

    roots = discover_profile_roots(profiles)

    assert list(roots) == ["author"]
    assert roots["author"] == profiles / "author" / "skills"


def test_profile_inventory_deduplicates_base_and_profile_projections(tmp_path: Path):
    live = tmp_path / "live"
    alpha = make_skill(live, "alpha", "alpha")
    base = iter_skill_records({"live": live})

    profiles = tmp_path / "profiles"
    author = profiles / "author" / "skills"
    researcher = profiles / "researcher" / "skills"
    marketing = profiles / "marketing" / "skills"
    forge = profiles / "forge" / "skills"

    shutil.copytree(alpha, author / "alpha")
    beta = make_skill(researcher, "beta", "beta", "Unique beta procedure.\n")
    shutil.copytree(beta, marketing / "beta")
    make_skill(forge, "beta", "beta", "Distinct beta variant with verification evidence.\n")

    result = inventory_profile_variants(discover_profile_roots(profiles), base)

    assert len(result.records) == 2
    assert {record.name for record in result.records} == {"beta"}
    assert all(record.source_lane == "profile" for record in result.records)
    assert all(record.discovery_status == "PROFILE" for record in result.records)
    assert len(result.projections) == 3
    base_projection = next(p for p in result.projections if p.base_match)
    assert base_projection.profiles == ("author",)
    assert len(base_projection.source_paths) == 1

    shared = next(p for p in result.projections if set(p.profiles) == {"marketing", "researcher"})
    assert shared.base_match is False
    assert len(shared.source_paths) == 2

    distinct = [p for p in result.projections if p.base_match is False]
    assert len(distinct) == 2
    assert len({p.tree_sha256 for p in distinct}) == 2


def test_profile_variant_relative_path_identifies_selected_profile(tmp_path: Path):
    profiles = tmp_path / "profiles"
    make_skill(profiles / "zeta" / "skills", "group/novel", "novel")
    make_skill(profiles / "alpha" / "skills", "group/novel", "novel", "different bytes\n")

    result = inventory_profile_variants(discover_profile_roots(profiles), [])

    assert [record.relative_path for record in result.records] == [
        "alpha/group/novel",
        "zeta/group/novel",
    ]
