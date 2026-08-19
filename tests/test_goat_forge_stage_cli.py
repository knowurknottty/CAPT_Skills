import json
from pathlib import Path
import subprocess
import sys

from goat_forge.inventory import SkillRecord, tree_digest


def make_record(root: Path, relative: str, name: str) -> SkillRecord:
    skill = root / relative
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Use when {name}\n---\n# {name}\n"
    )
    return SkillRecord(
        source_lane="live", source_path=str(skill), relative_path=relative,
        name=name, description=f"Use when {name}", file_count=1,
        byte_count=(skill / "SKILL.md").stat().st_size, symlink_count=0,
        tree_sha256=tree_digest(skill), frontmatter_status="OK",
        discovery_status="LIVE",
    )


def test_stage_cli_materializes_only_capt_candidates(tmp_path: Path):
    source = tmp_path / "source"
    capt = make_record(source, "mlops/capt-memory", "capt-memory")
    other = make_record(source, "research/deep-research", "deep-research")
    inventory = tmp_path / "inventory.jsonl"
    inventory.write_text(
        "\n".join(json.dumps(r.to_dict(), sort_keys=True) for r in (capt, other)) + "\n"
    )
    repo = tmp_path / "repo"
    repo.mkdir()
    quarantine = tmp_path / "quarantine"

    completed = subprocess.run(
        [sys.executable, "scripts/goat_forge_stage.py", "--repo-root", str(repo),
         "--inventory", str(inventory), "--lane", "capt",
         "--quarantine-root", str(quarantine)],
        capture_output=True, text=True, check=False,
    )

    assert completed.returncode == 0, completed.stderr
    staged = sorted((quarantine / "capt").glob("*/SOURCE.json"))
    assert len(staged) == 1
    metadata = json.loads(staged[0].read_text())
    assert metadata["source"]["name"] == "capt-memory"
    assert not (repo / "skills").exists()
    assert not (repo / "staging").exists()
