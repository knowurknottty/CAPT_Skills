from pathlib import Path

import pytest

from goat_forge.paths import ForgePaths, validate_source_roots


def test_forge_paths_keep_source_lanes_distinct(tmp_path: Path):
    repo = tmp_path / "repo"
    live = tmp_path / "live"
    bundled = tmp_path / "bundled"
    optional = tmp_path / "optional"
    for path in (repo, live, bundled, optional):
        path.mkdir()

    paths = ForgePaths(repo, live, bundled, optional)

    assert paths.repo_root == repo
    assert paths.hermes_live == live
    assert paths.hermes_bundled == bundled
    assert paths.hermes_optional == optional
    assert paths.staging_root == repo / "staging"


def test_validate_source_roots_fails_closed_on_missing_source(tmp_path: Path):
    repo = tmp_path / "repo"
    live = tmp_path / "live"
    bundled = tmp_path / "bundled"
    optional = tmp_path / "optional-missing"
    for path in (repo, live, bundled):
        path.mkdir()

    paths = ForgePaths(repo, live, bundled, optional)

    with pytest.raises(FileNotFoundError, match="hermes_optional"):
        validate_source_roots(paths)
