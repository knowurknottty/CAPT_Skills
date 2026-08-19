from pathlib import Path

import pytest

from goat_forge.inventory import SkillRecord, tree_digest
from goat_forge.staging import stage_skill, staging_id


def record_for(path: Path, *, lane: str = "live", relative: str = "group/alpha") -> SkillRecord:
    return SkillRecord(
        source_lane=lane,
        source_path=str(path),
        relative_path=relative,
        name="alpha",
        description="Use when alpha",
        file_count=1,
        byte_count=(path / "SKILL.md").stat().st_size,
        symlink_count=0,
        tree_sha256=tree_digest(path),
        frontmatter_status="OK",
        discovery_status="LIVE",
    )


def make_source(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    source.mkdir()
    (source / "SKILL.md").write_text("---\nname: alpha\ndescription: Use when alpha\n---\n# Alpha\n")
    return source


def test_staging_id_is_collision_safe_across_source_paths():
    first = staging_id("live", "mlops/alpha")
    second = staging_id("optional", "mlops/alpha")
    third = staging_id("live", "other/alpha")
    assert len({first, second, third}) == 3
    assert first.startswith("live__")


def test_stage_skill_preserves_bytes_and_digest(tmp_path: Path):
    source = make_source(tmp_path)
    record = record_for(source)
    quarantine = tmp_path / "quarantine"
    repo = tmp_path / "repo"

    staged = stage_skill(record, "capt", quarantine, repo)

    copied = staged.root / "original"
    assert (copied / "SKILL.md").read_bytes() == (source / "SKILL.md").read_bytes()
    assert staged.source_sha256 == record.tree_sha256
    assert staged.staged_sha256 == record.tree_sha256
    assert (staged.root / "SOURCE.json").exists()


def test_stage_skill_refuses_to_overwrite_immutable_original(tmp_path: Path):
    source = make_source(tmp_path)
    record = record_for(source)
    quarantine = tmp_path / "quarantine"
    repo = tmp_path / "repo"
    stage_skill(record, "capt", quarantine, repo)

    with pytest.raises(FileExistsError):
        stage_skill(record, "capt", quarantine, repo)


def test_stage_skill_rejects_quarantine_inside_repo(tmp_path: Path):
    source = make_source(tmp_path)
    record = record_for(source)
    repo = tmp_path / "repo"
    repo.mkdir()
    quarantine = repo / "quarantine"

    with pytest.raises(ValueError, match="outside"):
        stage_skill(record, "capt", quarantine, repo)


def test_stage_skill_preserves_internal_symlinks(tmp_path: Path):
    source = make_source(tmp_path)
    (source / "reference.txt").write_text("reference")
    (source / "reference-link").symlink_to("reference.txt")
    record = record_for(source)
    record = SkillRecord(**{**record.to_dict(), "file_count": 2, "symlink_count": 1,
                            "tree_sha256": tree_digest(source)})
    quarantine = tmp_path / "quarantine"
    repo = tmp_path / "repo"

    staged = stage_skill(record, "capt", quarantine, repo)
    copied_link = staged.root / "original" / "reference-link"
    assert copied_link.is_symlink()
    assert copied_link.readlink().as_posix() == "reference.txt"
    assert staged.staged_sha256 == record.tree_sha256


def test_capt_candidate_selection_is_token_aware_and_live_only(tmp_path: Path):
    from goat_forge.staging import is_capt_candidate

    source = make_source(tmp_path)
    capt = record_for(source, relative="mlops/capt-memory")
    archive = SkillRecord(**{**capt.to_dict(), "discovery_status": "ARCHIVED"})
    unrelated = SkillRecord(**{**capt.to_dict(), "name": "capture-screen",
                               "relative_path": "media/capture-screen"})

    assert is_capt_candidate(capt) is True
    assert is_capt_candidate(archive) is False
    assert is_capt_candidate(unrelated) is False
