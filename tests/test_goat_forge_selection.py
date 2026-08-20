from pathlib import Path

import pytest

from goat_forge.inventory import SkillRecord
from goat_forge.staging import DonorSelection, select_exact_donors


def rec(name: str, lane: str, relative: str, digest: str) -> SkillRecord:
    return SkillRecord(
        source_lane=lane,
        source_path=f"~/.hermes/{relative}",
        relative_path=relative,
        name=name,
        description=f"Use when {name} is needed",
        file_count=1,
        byte_count=100,
        symlink_count=0,
        tree_sha256=digest,
        frontmatter_status="OK",
        discovery_status=lane.upper(),
    )


def test_exact_donor_selection_disambiguates_duplicate_names():
    live = rec("systematic-debugging", "live", "software/systematic-debugging", "a" * 64)
    bundled = rec("systematic-debugging", "bundled", "software/systematic-debugging", "b" * 64)
    selection = DonorSelection(
        name="systematic-debugging",
        source_lane="bundled",
        relative_path="software/systematic-debugging",
        tree_sha256="b" * 64,
        action="REWRITE",
    )

    selected = select_exact_donors([live, bundled], [selection])

    assert selected == [(bundled, selection)]


def test_exact_donor_selection_rejects_digest_drift():
    record = rec("alpha", "live", "software/alpha", "a" * 64)
    selection = DonorSelection(
        name="alpha", source_lane="live", relative_path="software/alpha",
        tree_sha256="b" * 64, action="HARDEN",
    )

    with pytest.raises(ValueError, match="digest"):
        select_exact_donors([record], [selection])


def test_exact_donor_selection_rejects_missing_or_duplicate_manifest_rows():
    record = rec("alpha", "live", "software/alpha", "a" * 64)
    selection = DonorSelection(
        name="alpha", source_lane="live", relative_path="software/alpha",
        tree_sha256="a" * 64, action="HARDEN",
    )
    missing = DonorSelection(
        name="missing", source_lane="live", relative_path="software/missing",
        tree_sha256="c" * 64, action="REWRITE",
    )

    with pytest.raises(ValueError, match="missing donor"):
        select_exact_donors([record], [missing])
    with pytest.raises(ValueError, match="duplicate selection"):
        select_exact_donors([record], [selection, selection])
